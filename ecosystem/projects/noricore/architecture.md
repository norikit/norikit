<!-- DO NOT EDIT — generated mirror of noricore/ai-docs/architecture.md by tools/aggregate_docs.py. Edit the source. -->

# Architecture

The evolving system design for noricore — modules, data flow, threading, and entry points.
Keep this current as the design changes (see the [maintenance protocol](README.md)).

> Early-stage design. The locked constraints live in [decisions.md](decisions.md).
> Open design questions are in [open-questions.md](open-questions.md).

## Overview

noricore is a macOS daemon that collects system state from native Apple APIs and distributes
it to registered subscribers over IPC. It provides two interaction modes:

- **Push** — event stream: subscribers receive notifications automatically when state changes.
- **Pull** — query: clients request the current value of any data point on demand (useful on
  startup, before the first change event arrives).

## Conceptual layers

```
┌──────────────────────────────────────────────────────────┐
│                 Subscribers / Clients                     │
│        (noribar · noriglaze · third-party tools)         │
└──────────────────┬───────────────────┬───────────────────┘
                   │  push events      │  query requests
                   ▼                   ▼
┌──────────────────────────────────────────────────────────┐
│                  Transport Layer  (Q1)                    │
│      IPC mechanism: XPC / unix socket / Mach port        │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│                   Event Bus / Broker                      │
│    topic registry · subscriber routing · state cache     │
└──────┬─────────────────────────────────────┬─────────────┘
       │  subscribe/publish                  │ publish
       ▼                                     ▼
┌──────────────────────────────────────────────────────────┐
│                    Providers Layer                        │
│  Battery · Network · ActiveApp · Time · CPU · Calendar   │
│  … (+ third-party provider plugin API — see Q5)          │
└──────────────────────────────────────────────────────────┘
```

## Modules (under Sources/noricore/ — TBD)

- **`Providers/`** — one module per system data source. Each implements a `Provider`
  protocol and emits typed events to the Broker when state changes. Built-in providers:
  Battery (IOKit), Network/Wi-Fi (CoreWLAN/Network), ActiveApp (NSWorkspace),
  Time (monotonic ticker), CPU/Memory (sysctl/host_statistics), Calendar (EventKit).
- **`Broker/`** — event bus: topic registry, subscriber list, current-state cache, and
  routing logic. On a new subscription, immediately delivers the cached value so the
  client starts consistent without waiting for the next change.
- **`Transport/`** — IPC layer; exposes the Broker to external processes. Type TBD (Q1).
  Handles connection acceptance, subscription negotiation, event serialization (Q2),
  and connection teardown.
- **`Schema/`** — shared event type definitions and wire protocol. Defines topic names,
  payload shapes, and versioning. Consumed by both Transport and (potentially) client
  libraries. Protocol TBD (Q2).
- **`Daemon/`** — entry point: LaunchAgent lifecycle, signal handling (SIGTERM → graceful
  shutdown), startup sequencing (initialize providers → broker → transport → run loop).

## Data flow

1. A **Provider** observes a system source (e.g. `IOPSNotificationCreateRunLoopSource` for
   battery, `NWPathMonitor` for network). When state changes, it publishes a typed event to
   the **Broker** via its dispatch queue.
2. The **Broker** updates the cached value for that topic and delivers the event to all
   subscribers registered for that topic.
3. The **Transport** serializes each event per Q2 and writes it to the connected client(s).
4. On new client connection, the Transport delivers the current cached state for all
   subscribed topics, giving the client a consistent snapshot immediately.

## Concurrency / threading

- Providers run on their own serial queues (or use framework-native callbacks — e.g.
  `NWPathMonitor` delivers on its own queue) and post to the Broker via a central actor.
- The **Broker** is a Swift actor — all mutations are serialized without manual locking.
- Transport I/O is managed by the IPC mechanism's own queues (XPC, DispatchSource, etc.).
- No UI — no main-thread requirement. Swift concurrency (async/await + actors) is the
  primary concurrency model; GCD is used only where framework callbacks require it.

## Entry points

- **Daemon:** `Sources/noricore/Daemon/main.swift` — bootstraps providers, broker, and
  transport; then runs `dispatchMain()` (never returns).
- **Headless self-test:** `--self-test` flag — initializes all providers (or mock
  providers), exercises broker routing with synthetic events, verifies state cache, and
  exits 0 on success. CI runs this without a display.

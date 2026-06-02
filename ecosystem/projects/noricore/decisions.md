<!-- DO NOT EDIT — generated mirror of noricore/ai-docs/decisions.md by tools/aggregate_docs.py. Edit the source. -->

# Architectural decisions

Locked decisions are **constraints**. Do not relitigate without explicit owner direction.
When a new decision is made, add an entry here (newest at the bottom) and, if it resolves an
[open question](open-questions.md), replace that entry there with a one-line pointer.

Format: each decision has an **ID** (`D1`, `D2`, …), a status, the decision, and the
rationale (and consequences/risks where relevant). Tasks cite the `D#` they produce.

---

## D1 — Target platform & stack

- **Status:** Locked (2026-05-31)
- **Decision:** Native Swift daemon targeting macOS 13+.
- **Rationale:** noricore requires direct, low-latency access to a broad set of macOS
  system APIs — IOKit (battery, power), CoreWLAN (Wi-Fi), NSWorkspace (active app),
  EventKit (calendar), and more. Swift is the natural fit: full access to Apple frameworks,
  Swift concurrency (async/await + actors) for clean event dispatch, and no impedance
  mismatch with Objective-C bridging. No cross-platform abstraction layers — they add
  overhead and complicate access to macOS-specific data sources.

## D2 — Standalone daemon (not embedded)

- **Status:** Locked (2026-05-31)
- **Decision:** noricore runs as an independent process distributed as a macOS LaunchAgent,
  not bundled inside any other norikit tool.
- **Rationale:** As the shared data backbone, noricore must be accessible by any process —
  noribar, noriglaze, noribento, third-party tools, and future ecosystem additions — without
  coupling to any one of them. A standalone daemon starts at login, runs independently of any
  tool's lifecycle, and any client can connect without importing noricore's build artifacts.
- **Consequence:** Requires a defined IPC interface (see Q1) and a LaunchAgent plist for
  installation and lifecycle management.

## D3 — macOS 13 floor

- **Status:** Locked (2026-05-31)
- **Decision:** macOS 13 (Ventura) is the minimum supported version. APIs requiring newer
  OS versions are wrapped behind `@available(macOS 14, *)` guards (or higher as needed).
- **Rationale:** Consistent with noribar (the primary consumer). macOS 13 covers a large
  enough install base while enabling Swift concurrency and the full async/await runtime.
  Graceful degradation keeps the daemon functional on 13 even when newer-API features are
  unavailable.

## D4 — IPC transport: unix domain socket

- **Status:** Locked (2026-06-02). Resolves [Q1](open-questions.md).
- **Decision:** noricore's transport is the **unix domain socket** — the sole IPC mechanism
  between the daemon and its clients (exposed as two sockets; see D5 below). No alternative
  transport *types* and no cross-platform transport abstraction. Windows is explicitly out of
  scope — there is no loopback-TCP fallback.
- **Rationale:** A unix domain socket is the consensus choice among comparable tools
  (i3/sway, Hyprland, bspwm, yabai all use one), is language-agnostic — Python, Lua, Rust,
  Go, and shell clients connect with no Apple SDK — and yields peer-credential
  (`LOCAL_PEERCRED`/`getpeereid`) plus filesystem-permission auth essentially for free. It
  is a *general*, non-exotic mechanism (portable in principle across Unix-likes), so making
  it the sole transport sacrifices no generality we care about — only Windows, which is on
  the never-list. Skipping a pluggable-transport layer keeps the daemon simple and avoids
  speculative generality.
- **Consequences:**
  - Authorization ([Q4](open-questions.md)) leans on the unix socket's local guarantees —
    peer credentials + filesystem permissions — with no per-transport auth matrix to design.
  - The `Transport/` module wraps one mechanism (the unix-socket transport, exposed as the
    two sockets of D5); the wire protocol ([Q2](open-questions.md)) is the remaining
    transport-adjacent open question.

## D5 — Dual-socket protocol: structured + simple

- **Status:** Locked (2026-06-02). Builds on D4; narrows [Q2](open-questions.md).
- **Decision:** The unix-socket transport (D4) is exposed as **two sockets**:
  - **Structured socket** — the full protocol: length-prefixed framed messages
    (JSON leading; see [Q2](open-questions.md)) supporting both **pull** (query a current
    value) and **push** (subscribe to topics, receive typed events). For first-class clients
    — noribar, noriglaze, language libraries.
  - **Simple socket** — a **newline-delimited text** event firehose: read-only, push-only.
    On connect it emits current cached state as text lines, then streams changes live.
    Consumable with zero client code (`socat`, `while read`, eww `deflisten`, Lua
    `io.popen`) — for shell/Lua/ad-hoc consumers.
- **Rationale:** The two consumer classes have opposite needs: real clients want typed,
  framed, queryable messages with no parsing ambiguity; rice-style glue wants to `tail` a
  stream with no library. Hyprland (control socket + text event socket), i3, and bspwm all
  converge on this split. Offering both makes noricore trivially adoptable by any tool in any
  language — the biggest ecosystem-adoption lever — without weakening the structured contract
  its primary clients depend on.
- **Consequences:**
  - Snapshot-on-connect (already in the design) applies to **both** sockets, so even a text
    consumer starts consistent without needing the pull path.
  - The simple socket is intentionally limited (no request/response, no fine-grained
    subscription beyond topic prefix) — it trades power for a zero-dependency interface;
    power users take the structured socket.
  - The schema must stay legible as **both** framed JSON and flat text — a constraint on Q2
    (encoding/versioning) and Q3 (topic naming): e.g. `battery.level 82` vs
    `{"topic":"battery.level","value":82}`.
  - Two listening endpoints to manage — socket paths, permissions, and teardown — not one.

## D6 — noricore is a bidirectional beacon (producer-clients)

- **Status:** Locked (2026-06-02). Resolves [Q5](open-questions.md).
- **Decision:** noricore is a **beacon**: a connected client is symmetric — it can both
  **subscribe/query** topics *and* **publish** its own events and data onto the bus. External
  apps contribute event sources via the **producer-client** model (connect over the structured
  socket, publish under a topic namespace) — no in-daemon dylib or script plugins. To the
  Broker, a built-in provider and an external producer-client are equivalent sources.
- **Rationale:** The ecosystem's flagship integrations require it. A tiling WM (AeroSpace) and
  a hotkey daemon (skhd) hold state no macOS API can observe from outside, so the only way
  they reach the bus is to publish it themselves; a consume-only noricore could surface
  battery/wifi/app but never workspace or input-mode — half the point. Producer-client (vs the
  dylib and script-provider options in Q5) keeps publishers in their own processes: no
  third-party code in the daemon, the same isolation and language-agnosticism as the consumer
  side.
- **Consequences:**
  - Snapshot-on-connect (the state cache) extends to producer topics — noricore retains the
    last published `wm.workspace`, `input.mode`, etc., so a late-subscribing bar gets current
    state immediately.
  - Publishing rides the **structured** socket (D5); it needs request/ack, so the simple text
    socket stays subscribe-only.
  - Opens new forks — topic namespacing & ownership ([Q6](open-questions.md)) and producer
    liveness & retention ([Q7](open-questions.md)) — and extends authorization
    ([Q4](open-questions.md)) to "who may publish what."
  - The dylib and script-based provider options from Q5 are **not** adopted; revisit only if
    the producer-client model proves insufficient.

## Standalone-first (inherited — prime directive #10)
**Decision:** noricore runs as an independent daemon, usable on its own; the tools that consume its
events are **optional**. Ecosystem integration is progressive enhancement, never a requirement —
noricore degrades cleanly when no consumers are present.

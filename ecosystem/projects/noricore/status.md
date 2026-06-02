<!-- DO NOT EDIT — generated mirror of noricore/ai-docs/status.md by tools/aggregate_docs.py. Edit the source. -->

# Status

Current phase + a dated changelog of meaningful progress. Append a dated line whenever
something meaningful lands (newest at the top of the log).

## Current phase

**Scaffolding** — repo created, foundational decisions locked (D1–D6), open questions
captured, architecture overview drafted. Transport, protocol shape, and the bidirectional
beacon model are resolved (Q1 → D4; Q5 → D6: producer-clients publish + subscribe). The
remaining **wire-protocol detail (Q2)** — structured encoding + versioning — plus new forks on
topic namespacing (Q6) and producer retention (Q7) are the open questions before the first
code spike. Not yet usable.

## Changelog

- **2026-06-02** — Beacon model locked (D6, resolves Q5): noricore is bidirectional —
  clients **publish** their own events/data (producer-client model) as well as subscribe/query.
  Built-in providers and external producers are equal sources. Opened Q6 (namespacing) and
  Q7 (producer liveness/retention).
- **2026-06-02** — Protocol shape decided (D5, narrows Q2): the unix-socket transport is
  exposed as **two sockets** — a structured framed-JSON socket (pull + push, for first-class
  clients) and a simple newline-text firehose (push-only, zero-dependency). D4 reworded to
  speak of transport *type*, not socket count.
- **2026-06-02** — Transport decided (D4, resolves Q1): a single **unix domain socket** —
  the general, consensus IPC mechanism. No cross-platform transport abstraction; Windows/TCP
  explicitly out of scope. D1 unchanged (macOS-first, providers native).
- **2026-05-31** — Repo bootstrapped. Foundational decisions locked (D1–D3). Open
  questions Q1–Q5 captured. Architecture overview drafted. Icons added to assets.

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

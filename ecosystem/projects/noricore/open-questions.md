<!-- DO NOT EDIT — generated mirror of noricore/ai-docs/open-questions.md by tools/aggregate_docs.py. Edit the source. -->

# Open questions

Unresolved design forks, roughly ordered by how much they constrain everything else. Each
has an **ID** (`Q1`, `Q2`, …). When one is resolved, record the decision in
[decisions.md](decisions.md) / [architecture.md](architecture.md) and **replace its entry
here with a one-line resolved-pointer** to the deciding `D#`.

> Example of a resolved entry (keep this shape):
>
> > **Q0 (example) — RESOLVED 2026-05-31** by [D1](decisions.md). _One line on the outcome._

---

### Q1 — IPC mechanism

Which transport does noricore use to communicate between the daemon and its clients?

Options on the table:
- **XPC** — Apple-native, secure, process-isolated, sandbox-compatible. Downside: both
  sides must share the same interface definition; non-Apple languages (Python, Rust, Go)
  are harder to connect without a C shim.
- **Unix domain socket** — simple, cross-language, any tool can connect without linking
  an Apple SDK; requires explicitly defining the wire protocol (see Q2). Standard path
  convention makes discovery trivial.
- **Mach ports** — low-level, used by sketchybar/yabai; maximum throughput and latency,
  but complex API and poor ergonomics for third-party adoption.
- **NSDistributedNotificationCenter** — minimal setup, but limited payload size, no
  query/response pattern, and broadcasts to all observers system-wide.

What would settle it: a spike comparing XPC vs unix socket on latency and third-party
client ergonomics (e.g. can a Python or Lua script connect without bridging code?).

### Q2 — Wire protocol / event schema

How are events serialized and versioned on the wire?

Options: JSON (universal, human-readable, modest overhead), MessagePack (binary,
cross-language, fast), a custom binary layout (lowest overhead, highest friction for
third-party tools), or Codable-backed XPC objects (if Q1 resolves to XPC — natural fit,
but ties the schema to Apple's type system).

What would settle it: depends partly on Q1; also depends on whether latency measurements
show JSON overhead matters at typical noricore event frequencies (battery changes are rare;
active-app changes are frequent but small payloads).

### Q3 — Event subscription model

How do clients express what data they want?

Options:
- **Topic strings** (e.g. `"battery.level"`, `"network.ssid"`) — simple, composable,
  easy to document and discover.
- **Typed subscriptions** — clients declare interest in specific Swift/codable types;
  broker type-checks at subscription time. Tighter but language-specific.
- **Filter expressions** — clients supply a predicate over event fields; broker evaluates
  per event. Most flexible; most complex to implement.

What would settle it: an owner call on the target client API ergonomics and whether
fine-grained filtering is in scope for v1.

### Q4 — Authorization model

Should noricore restrict which processes can connect?

Questions: Does any system data noricore exposes require per-client access control? Should
third-party tools need a capability or entitlement to connect? How does this interact with
the chosen IPC mechanism (Q1) — XPC has entitlement-based authorization built in; unix
sockets rely on filesystem permissions.

Relevant: calendar (EventKit) and other privacy-sensitive data sources require user
permission at the system level — noricore itself needs the entitlement, but does it also
need to gate per-client access to those topics?

What would settle it: a review of which providers touch privacy-sensitive data plus an
owner call on the desired trust model for third-party consumers.

### Q5 — Third-party provider plugin API

How can external code contribute custom event sources to the broker?

Options:
- **No plugin API (v1 scope)** — built-in providers only; third-party tools are consumers.
  Keep scope tight and revisit after the core is stable.
- **Producer-client** — a process connects to noricore as a "producer" (reverse client) and
  publishes events under a custom topic namespace. Requires no special plugin loading.
- **Dynamic library plugin** — noricore loads `.dylib` plugins; they register `Provider`
  implementations at startup. Full integration; introduces security and stability concerns.
- **Script-based provider** — noricore executes a user-supplied script and reads stdout as
  event data (sketchybar-style). Simple for users; sandboxing is tricky.

What would settle it: an owner call on extensibility scope for v1, and whether the
producer-client model satisfies the third-party use case without needing in-process plugins.

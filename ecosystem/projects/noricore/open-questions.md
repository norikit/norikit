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

### Q1 — RESOLVED 2026-06-02 by [D4](decisions.md)

Transport is a single **unix domain socket** — general, language-agnostic, and the
consensus choice among comparable tools. No multi-transport abstraction; Windows/TCP is out
of scope. D1 is unchanged.

### Q2 — Wire protocol / event schema

How are events serialized and versioned on the wire?

Options: JSON (universal, human-readable, modest overhead), MessagePack (binary,
cross-language, fast), a custom binary layout (lowest overhead, highest friction for
third-party tools), or Codable-backed XPC objects (if Q1 resolves to XPC — natural fit,
but ties the schema to Apple's type system).

What would settle it: depends partly on Q1; also depends on whether latency measurements
show JSON overhead matters at typical noricore event frequencies (battery changes are rare;
active-app changes are frequent but small payloads).

Narrowed by [D5](decisions.md): there are **two channels**. The **simple** socket is
newline-delimited **text** (pinned). The **structured** socket is length-prefixed framed
messages with **JSON** as the leading encoding (vs MessagePack / custom binary). Remaining:
confirm the structured encoding and the versioning scheme — and keep the schema legible as
*both* framed JSON and flat text lines (e.g. `battery.level 82` vs `{"topic":...}`).

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

Note ([D5](decisions.md)): the simple text socket implies **topic-string** addressing (a flat
`topic value` line, optionally filtered by topic prefix). Typed or filter-expression
subscriptions, if adopted, would live on the structured socket only.

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

Note ([D4](decisions.md)): with a single unix-socket transport, auth can lean on local
guarantees — peer credentials (`LOCAL_PEERCRED`/`getpeereid`) + filesystem permissions —
rather than a per-transport scheme.

Extended by [D6](decisions.md): publishing is now in scope, so authorization must also cover
**who may publish what** — may any client publish into reserved provider namespaces like
`battery.*`, or only into its own? (See [Q6](open-questions.md).)

### Q5 — RESOLVED 2026-06-02 by [D6](decisions.md)

The **producer-client** model is adopted: external processes connect and publish events/data
under a topic namespace — no in-daemon dylib or script plugins. noricore is a bidirectional
**beacon** (publish + subscribe). The dylib and script-based provider options are not adopted.

### Q6 — Topic namespacing & ownership

With producer-clients (D6) able to publish, who owns which topics?
- Are built-in provider namespaces (`battery.*`, `network.*`, `app.*`, …) **reserved**, so a
  third party cannot publish — or spoof — them?
- Do producers get a free namespace (their own `wm.*`, `input.*`), or must they claim/register
  a prefix first?
- Collision policy when two producers publish the same topic.

What would settle it: a naming convention (reserved vs open prefixes) plus the publish-auth
call in [Q4](open-questions.md).

### Q7 — Producer liveness & retention

When a producer-client disconnects (e.g. AeroSpace quits or crashes), what happens to the
values it published? Keep the last value (retained, MQTT-style) so subscribers still read
`wm.workspace`; mark it stale/unknown; or drop it after a TTL? And should a subscriber be able
to tell that a topic's producer is gone?

What would settle it: an owner call on whether *stale-but-present* or *explicitly-absent* is the
better default for consumers (a bar showing the last workspace vs. blanking it).

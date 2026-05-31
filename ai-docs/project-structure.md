# norikit project structure

This is the structure every norikit project should have. Absorb the description below and
**rebuild an equivalent structure for your tool** — adapting it to your domain and stack.
It is a pattern to reproduce, not a repo to copy.

Two layers are described, and the distinction matters:

- **Reusable scaffolding** — the docs / tasks / CI / lint / package skeleton. This is
  common to every norikit project; reproduce it.
- **Domain-specific choices** — the actual product code, the windowing/rendering/config
  approach, any vendored libraries. These belong to *your* tool; design them for the best
  performance and feature set (see [mission.md](mission.md) directive #1), independent of
  how any other tool solved its problem.

---

## 1. Top-level layout

```
<project>/
  README.md            # human-facing: what/why/status/build, badges, ecosystem note
  CLAUDE.md            # AI-agent front door → points at ai-docs/ + the standing rules
  LICENSE              # AGPL-3.0
  <build manifest>     # the build definition for your stack (e.g. Package.swift)
  <lint configs>       # one per language you ship
  .gitignore
  .github/
    workflows/ci.yml   # CI: build + test + lint
    dependabot.yml     # dependency update automation
  Sources/             # PRODUCT code (see §3)
  Tests/               # tests, mirroring Sources
  ai-docs/             # durable DESIGN truth — the knowledge base (see §5)
  tasks/               # live WORK items as task folders (see §6)
```

**The split that matters:** *design truth* (durable, the "why") lives in the knowledge base
(`ai-docs/`); *work items* (transient, the "what now") live in `tasks/`; *product code* lives
in `Sources/`. Throwaway proof-of-concept code never lives in `Sources/` — it lives inside
the task that produced it (`tasks/<id>/code/`).

## 2. Build / package shape

A single build manifest defines the project's targets. Conventionally:

- An **application/executable target** — the tool itself.
- A **test target** depending on it.
- Optionally a **vendored-dependency target** for any third-party source you bundle.

Pin a minimum-OS floor in the manifest and honor it (graceful degradation, directive #5).
Put a short prose header at the top of the manifest explaining what the package is and any
non-obvious build mechanics, so a contributor understands it without reverse-engineering.

**Vendoring discipline:** if you bundle third-party source, give it its own build target and
record its version/provenance/license in a `VENDORING.md` beside it. Whether you vendor
anything at all is a domain choice.

## 3. Source organization (`Sources/`)

Group product code by **responsibility, one directory per architectural layer**, named for
what it *does* — not by file type. For example, a layer for windowing, a layer for
rendering, a layer for the data model, a layer for configuration, a layer for data sources.
The specific layers are yours; they should map to *your* architecture.

Always keep:

- a **single, clear entry point** (app bootstrap), and
- a **headless self-test path** — a mode that exercises the core invariants without a
  GUI/window, so CI can run it.

Product code is the product. Throwaway PoC/research code stays in `tasks/<id>/code/`.

## 4. Tests

`Tests/<target>Tests/` mirrors `Sources/`, focused on the invariants that actually matter
(safety rules, correctness of core logic). Tests run in CI. Pair unit tests with the
headless self-test mode (§3) for behavior that's awkward to unit-test but still checkable
without a GUI.

## 5. The knowledge base (`ai-docs/`) — durable design truth

`ai-docs/` is the single source of truth for design intent, read *before* doing work. Files
and their roles:

| File | Role |
|---|---|
| `README.md` | Index of the KB + the maintenance protocol + "how to use this as an agent." |
| `decisions.md` | **Locked** architectural decisions, ADR-style — each with an ID (`D1`, `D2`, …), status, decision, rationale, consequence. Constraints, not suggestions. |
| `architecture.md` | The evolving system design — modules, data flow, threading, loops. |
| `open-questions.md` | Unresolved design forks, each with an ID (`Q1`, `Q2`, …). When resolved, the entry is replaced by a one-line pointer to the deciding `D#`. |
| `status.md` | Current phase + a dated changelog of meaningful progress. |
| `glossary.md` | Domain terms. |

Add project-specific reference docs (rationale dossiers, prior-art analyses) as needed and
link them from the index.

**ID scheme:** decisions are `D#`, open questions are `Q#`; tasks cite the `D#`/`Q#` they
produce or resolve. This cross-links work ↔ design bidirectionally.

**Maintenance protocol (standing rule):** *if you change reality, change the knowledge base
in the same change.* Decision made → `decisions.md` (and retire the `open-questions.md`
entry to a resolved-pointer); design changed → `architecture.md`; progress → dated line in
`status.md`; new KB doc → link it in the index; user-facing fact changed → root `README.md`.

## 6. The task system (`tasks/`)

The live view of *what is being worked on*. Each work item — **spike, milestone, or chore** —
is a folder:

```
tasks/<id>/
  task.md        # REQUIRED — YAML frontmatter + a self-contained brief
  FINDINGS.md    # optional — the results/report once produced
  code/          # optional — throwaway PoC/research code; NEVER the product
```

`tasks/README.md` is the **board**: a table with columns *Task · Type · Status · Verdict ·
Resolves · Decisions*, plus the frontmatter schema and the add-a-task procedure.

**`task.md` frontmatter schema:**

```yaml
---
id: my-task-id                    # kebab-case, == folder name
name: Human-readable task title
type: spike                       # spike | milestone | chore
status: ready                     # draft | ready | in-progress | blocked | complete | superseded
verdict: n/a                      # spikes: GO | NO-GO | n/a ; others: n/a
created: 2026-05-31
updated: 2026-05-31
resolves: [Q1]                    # open-questions this closes
decisions: [D6]                   # decisions it produced
depends_on: []                    # task ids this builds on
artifacts: ./code                 # runnable code path, or null
findings: ./FINDINGS.md           # results doc path, or null
---
```

Write a spike's brief **self-contained for an autonomous agent** ("you have no prior
context; everything you need is below") and explicitly label throwaway de-risking code as
*not the product*. When a task lands: set `status: complete`, fill `verdict`/`findings`, and
fold its `decisions:`/`resolves:` into the knowledge base **in the same change**.

## 7. CI (`.github/workflows/ci.yml`)

Trigger on push to `main`, all PRs, and manual dispatch; cancel superseded runs on the same
ref; set least-privilege `permissions` (`contents: read`). Run build + test + lint on the
appropriate runner.

**Key principle — graceful, self-activating CI:** every step is **conditional** and skips
with a `::notice::` when its inputs don't exist yet (no build manifest, no lint config, no
files of a given type). CI is green from an empty repo and *activates automatically* as the
project grows into it. Run linters in **strict** mode. One lint job per language you ship.

## 8. Tooling & automation

- A **linter per language**, enforced strictly in CI, with its config checked in.
- **Dependabot** (`.github/dependabot.yml`) for dependency updates.

## 9. Build & run model

Expose, at minimum:

- a **headless self-test** invocation (CI-suitable; no GUI), and
- a **real run** invocation.

Record any domain-specific build quirks (special packaging, runtime requirements) where
contributors will hit them — in the build-manifest header, the README, and here.

---

## What to reproduce vs. what is yours

| Reproduce the pattern | Design for your domain |
|---|---|
| README / CLAUDE / LICENSE front matter | The product itself |
| `ai-docs/` layout, `D#`/`Q#` ID scheme, maintenance protocol | The actual decisions / architecture |
| `tasks/` folders + frontmatter schema + board | — |
| Layer-per-responsibility `Sources/` organization | The specific layers |
| Graceful, self-activating CI; strict lint; dependabot | The toolchain (match your language) |
| Headless self-test mode + real run mode | The commands |
| Vendoring discipline (own target, `VENDORING.md`) | Whether you vendor anything at all |
| Single OS floor + availability-gated newer features | The product's windowing / rendering / config / data approach |

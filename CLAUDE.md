# CLAUDE.md — entry point for agents working in norikit

<!-- norikit:managed — synced from `template/CLAUDE.md`; do NOT hand-edit.
     Change the template and re-run sync_scaffold. Edit only the project region below. -->

**Read this, then the operating manual.** You are working in a repo of the **norikit** org.

## ⇒ The operating manual

**[`norikit/ai-docs/framework.md`](https://github.com/norikit/norikit/blob/main/ai-docs/framework.md)**
is the single entry point for *how we work* — task tracking, the working agreement, branching, and
quality. Read it before substantive work. The ecosystem mission/conventions live in
[`norikit/ai-docs/`](https://github.com/norikit/norikit/tree/main/ai-docs); this repo's design
knowledge lives in [`ai-docs/`](ai-docs/).

## The essentials (do not violate)

- **Work within the project — no code without a tracked issue.** Find/create a GitHub issue on the
  right board, meet Definition of Ready (typed · Priority + Size · rich description), pull one to
  In Progress, then work. Decompose big asks into an epic + sub-issues first. **GitHub issues are the
  source of truth.**
- **Always branch, always PR — never commit to `main`.** Branch off fresh `origin/main` as
  `<type>/<issue#>-<slug>` (`type ∈ feat, fix, chore, spike, docs`); Conventional-Commit messages; open
  a PR that `Closes #<issue>`; squash-merge after the gates pass (a deliberate human click — no auto-merge).
- **Standalone-first.** This tool must work on its own; ecosystem integrations (noricore, noriglaze, …)
  are optional, availability-gated enhancements — never hard dependencies.
- **Keep `ai-docs/` current in the same change.** If you change reality, change the knowledge base in the
  same PR. Stale docs are worse than none.
- **Definition of Done:** merged via PR · `ai-docs` updated · CI green · behavior **verified** (not just
  green CI) · standalone-first respected · no token/scaffold leftovers. (The issue form carries the checklist.)

## Conventions

- Match surrounding code style; favor clarity and low-latency, main-thread-safe code.
- Throwaway PoC/spike code lives in `tasks/<id>/code/` and is **not** the product; real product code
  lives under `Sources/`.
- License: **AGPL-3.0**.

<!-- /norikit:managed -->

<!-- norikit:project:start — this repo's own content; sync never overwrites between these markers. -->

## This project: norikit

**norikit** — the ecosystem's home repo: the operating framework, the project roster, and the dev-time
tooling that keeps every repo aligned. This is *meta*, not a product — it ships no daemon and has no
`Sources/`. The managed block above is generated *from this repo*; here it is also a working repo.

Durable knowledge lives in **[`ai-docs/`](ai-docs/)** — start at **[framework.md](ai-docs/framework.md)**
(how we work), then **[mission.md](ai-docs/mission.md)**, **[conventions.md](ai-docs/conventions.md)**,
**[project-structure.md](ai-docs/project-structure.md)**, and **[new-project.md](ai-docs/new-project.md)**.

### The single sources of truth (define once, derive everywhere)

- **[`ai-docs/projects.toml`](ai-docs/projects.toml)** is the roster's only source of truth. Never
  hand-edit `projects.md`, the README roster region, or the `.github` profile table — edit the TOML and
  run `tools/gen_roster.py`.
- **`template/`** owns the managed scaffold (`CLAUDE.md` managed block + `.github/ISSUE_TEMPLATE`).
  Never hand-edit a synced/generated file in any repo — change the template and run
  `tools/sync_scaffold.py`. Edit only the `norikit:project` region.
- **`tools/org_doctor.py`** is the conformance gate (roster · scaffold · tokens · badges · standalone).
  Run it before opening a PR that touches roster, scaffold, or docs.
- **Standalone-first** is an inherited prime directive: every *tool* must run on its own; ecosystem
  coupling is optional and availability-gated. (norikit itself is dev-time only — not a runtime dep.)

### Tooling (Python 3.11+, stdlib only — not a runtime dependency of any tool)

`gen_roster.py` · `sync_scaffold.py` · `org_doctor.py` · `aggregate_docs.py`. License: **AGPL-3.0**.

<!-- norikit:project:end -->

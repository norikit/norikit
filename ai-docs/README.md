# ai-docs — ecosystem reference for agents building norikit projects

This directory is the **single source of truth for the norikit *ecosystem*** — the shared
mission, prime directives, and conventions that every project under the
[`norikit`](https://github.com/norikit) org is expected to follow.

It exists so that any agent (or human) starting or extending a norikit tool can absorb the
foundations *before* writing code, and produce something that belongs in the family.

## Scope: ecosystem vs. project

`ai-docs/` is the agent-facing knowledge base in **every** norikit repo. What it documents
depends on the repo:

| Layer | Source of truth | Lives in |
|---|---|---|
| **Ecosystem** (mission, cross-cutting directives, naming, licensing, branding) | **this `ai-docs/` directory** | `norikit/norikit` (this repo) |
| **A single project** (its architecture, decisions, tasks) | that project's `CLAUDE.md` + **`ai-docs/`** + `tasks/` | each project repo |

(New projects put their knowledge base in `ai-docs/` from the start.)

When the two could conflict, the ecosystem docs set the *defaults and constraints*; a
project may specialize within them but should not silently contradict them. Relitigate a
shared directive only with explicit owner direction.

## Read in this order

1. **[framework.md](framework.md)** — **the operating manual: start here.** How we work
   (enforced scrumban task tracking, the working agreement, branching, quality) and where
   everything lives, so any agent can pick up a task cold.
2. **[mission.md](mission.md)** — what norikit is for, and the prime directives every
   project inherits.
3. **[conventions.md](conventions.md)** — naming, licensing, branding, git workflow,
   knowledge-base discipline, repo layout.
4. **[projects.md](projects.md)** — the current roster, what each tool is, and how they
   relate.
5. **[project-structure.md](project-structure.md)** — the structure every norikit project
   should have: layout, package, source organization, knowledge base, task system, CI.
   Absorb it and rebuild an equivalent for your tool; it separates the reusable scaffolding
   from per-project domain choices.
6. **[new-project.md](new-project.md)** — checklist for bootstrapping a new norikit tool.

## Keeping these current

These docs follow the same standing rule as every project knowledge base: **if you change
the reality of the ecosystem, change these docs in the same change.** Stale shared docs are
worse than none — every downstream project inherits the error.

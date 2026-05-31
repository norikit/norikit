# Conventions

Shared conventions for every norikit repo.

## Naming

- The ecosystem is **norikit** (lowercase). Projects are lowercase, prefixed with **`nori`**,
  in the seaweed/bento motif: `noribar`, `noriglaze`, `norify`, `noribento`, `noribox`,
  `noricut`. New tools should keep the `nori…` prefix and an evocative, short suffix.
- A project's repo name, product name, and the directory it clones into all match.

## Licensing

- **AGPL-3.0** for all projects. Ship the `LICENSE` file and state it in the README.

## Branding

Project READMEs use a consistent, centered header:

- A row of badges: **status**, the `ecosystem-norikit` badge (color `32C572`), and
  **license AGPL-3.0**.
- A light/dark hero image via `<picture>` with `prefers-color-scheme`, stored in the repo
  (`assets/hero-light.svg` + `assets/hero-dark.svg`, or repo root).
- A one-paragraph statement of what the tool is and how it fits the ecosystem.
- A `> [!NOTE]` work-in-progress callout while the tool isn't yet usable.

## Repository layout

The full structure is described in **[project-structure.md](project-structure.md)** — absorb
it and rebuild an equivalent for your tool rather than copying any existing repo. The
knowledge base lives at repo-root **`ai-docs/`**. `ai-docs/` is the agent-facing knowledge
base in *every* norikit repo — ecosystem docs in `norikit/norikit`, project docs in each
project.

```
<project>/
  README.md                  # human-facing: what, why, status, build
  CLAUDE.md                  # front door for AI agents → points at ai-docs/
  LICENSE                    # AGPL-3.0
  ai-docs/                   # durable design truth for agents+humans (project source of truth)
    README.md                # index of the knowledge base
    decisions.md             # locked architectural choices + rationale
    architecture.md          # evolving system design
    open-questions.md        # unresolved design forks
    status.md                # current phase + dated changelog
    glossary.md              # domain/term reference
  tasks/                     # active work items as task folders
    README.md                # the task board
    <task-id>/task.md        # stateful frontmatter + brief (+ optional FINDINGS.md, code/)
  Sources/  Tests/           # product code (language-appropriate)
```

Smaller/younger projects won't have all of this yet — but this is the target, and
`ai-docs/` + `CLAUDE.md` should appear early.

## Knowledge-base discipline (standing instruction)

**If you change reality, change the knowledge base (`ai-docs/`) in the same change.**

- Decision made → add/update `decisions.md`.
- Design changed → update `architecture.md`.
- Question resolved → record the resolution, replace its `open-questions.md` entry with a
  one-line resolved-pointer.
- Task started/finished → update its `status:` and the board in `tasks/README.md`.
- Meaningful progress → append a dated line to `status.md`.
- User-facing facts changed → update `README.md`.
- New knowledge-base file → link it from `ai-docs/README.md`.

Treat locked decisions as constraints. Do not relitigate them without explicit owner
direction.

## Git workflow (standing instruction)

**Never commit directly to `main`. Always branch, always PR.**

- **Work happens in worktrees, so start every piece of work by updating to the latest.**
  Because each task is developed in its own git worktree branched off `main`, a worktree cut
  from a stale base silently drifts. Before creating one, always `git fetch origin` and base
  it on the freshest `origin/main` — never an old local snapshot. This is the single most
  effective guard against staleness.
- Sync first: `git fetch origin`, fast-forward local `main` (`git checkout main &&
  git pull --ff-only`), then branch off the latest `origin/main`
  (`git checkout -b <descriptive-branch> origin/main`, or
  `git worktree add -b <descriptive-branch> <path> origin/main`).
- Open a PR when the task is complete — the PR *is* the deliverable; a task isn't "done"
  until its PR exists. Use `gh pr create` with a clear title and a body covering what
  changed, why, and how it was verified.
- Keep the PR current: push follow-up commits and `gh pr edit` the title/body so it always
  reflects the branch.
- Commit messages and PR bodies are self-explanatory.

## Code style

Match the surrounding code. Favor clarity and low-latency, main-thread-safe UI. Throwaway
spike/PoC code (e.g. under `tasks/<id>/code/`) is explicitly **not** the product; product
code lives under `Sources/`.

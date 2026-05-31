# Bootstrapping a new norikit project

A checklist for starting a new tool under the [`norikit`](https://github.com/norikit) org so
it belongs in the family from commit one. Read [mission.md](mission.md) and
[conventions.md](conventions.md) first; this turns them into steps.

> **Absorb the structure, then rebuild it.** Read
> [project-structure.md](project-structure.md) to understand *why* each part of the standard
> structure exists, then construct the equivalent for your tool — adopting the reusable
> scaffolding and designing the domain-specific parts for your tool's own needs.

## Before any code

1. **Confirm the scope with the owner.** One tool, one job (directive #6). Write the
   one-sentence definition of what it does and how it fits the ecosystem.
2. **Name it** in the `nori…` motif (lowercase, short evocative suffix). Repo name = product
   name = clone directory.
3. **Check the directives apply.** Native-first, performance-first, theme-through-noriglaze,
   shareable config, graceful degradation. If the tool has a UI, plan to consume
   [noriglaze](https://github.com/norikit/noriglaze) themes — a *strong default, not a hard
   gate*. noriglaze is still early, so at minimum design so you can integrate later.

## Repo setup

4. **Create the repo from the [`template`](https://github.com/norikit/template) scaffold** —
   it provides the standard skeleton described in
   [project-structure.md](project-structure.md). Make it **public**, confirm the
   **AGPL-3.0** `LICENSE`, and enable **branch protection on `main`** (no direct pushes —
   this enforces *always branch, always PR*).
5. **README.md** with the standard branding: badge row (status · `ecosystem-norikit`
   `32C572` · `license AGPL-3.0`), light/dark `<picture>` hero (`assets/hero-light.svg` +
   `assets/hero-dark.svg`), one-paragraph statement, and a WIP `> [!NOTE]` callout.
6. **CLAUDE.md** — the agent front door. Point it at **`ai-docs/`**, restate the project's
   locked decisions, and carry the two standing instructions verbatim: *keep the knowledge
   base current in the same change*, and *always branch, always PR*.
7. **ai-docs/** (repo root) with at least `README.md` (index), `decisions.md`,
   `architecture.md`, `open-questions.md`, `status.md`, `glossary.md`. Seed `decisions.md`
   with the foundational stack choices and *why*.
8. **tasks/** with a `README.md` board; capture the first spikes/milestones as task folders.
9. **Build & CI skeleton** — the template seeds these; adjust to your stack: a build
   manifest, `Sources/` + `Tests/`, `.github/workflows/ci.yml` (graceful + self-activating —
   steps skip until their inputs exist), a per-language **lint config** run in strict mode,
   `.github/dependabot.yml`, and `.gitignore`.

## Foundational decisions to record on day one

In `decisions.md`, lock and justify:

- **Target platform** (macOS-first; native to whatever you target).
- **Language / stack** — chosen for the **best performance and feature set** for this tool,
  not a house default. Swift + native is the proven choice on macOS; justify your pick.
- **OS floor** and the availability-gating policy for newer features.
- **Rendering / UI approach** (native frameworks) — *if the tool has a UI*.
- **Configuration model** (an embedded scripting language? something else? why?) — *if the
  tool is user-configurable*.
- **noriglaze theming integration** — how this tool consumes shared themes (strong default
  for anything with UI; if deferred, design so it can integrate later).
- **Extension points / escape hatches** (directive #9) — where can an advanced user plug in
  their own implementation *without forking*? Identify the seams (providers, backends,
  user-supplied scripts/modules, overridable behavior) early; retrofitting flexibility is
  costly.

## Working rhythm

10. **Start every piece of work by updating to the latest.** Work is developed in
    worktrees, so always `git fetch origin` and base the worktree/branch on the freshest
    `origin/main` — a worktree cut from a stale base silently drifts. Never commit to `main`.
11. Keep docs in sync **in the same change** as code.
12. Open a PR as the deliverable; keep its title/body current.

> If you find yourself contradicting an ecosystem directive, stop and confirm with the
> owner — then record the outcome in `ai-docs/` so the next project inherits the decision,
> not the surprise.

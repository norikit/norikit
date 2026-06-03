# The norikit framework — agent & contributor operating manual

**If you are an agent or contributor starting work in any norikit repo, read this first.** It is the
single entry point that tells you *how we work* and *where everything lives*, so you can pick up any
task cold — no out-of-band instructions required.

> Status: the framework is being built (tracked on the [ecosystem board](https://github.com/orgs/norikit/projects/15)).
> Sections marked _(in progress)_ describe the target; the **working agreement, conventions, and task
> tracking below are in effect now.**

---

## North stars

1. **Standalone-first + progressive enhancement.** Every tool must be fully usable on its own; the
   ecosystem (noricore data, noriglaze themes, norify notifications, …) is **optional, availability-gated
   enhancement — never a hard dependency.**
2. **Define once, derive everywhere, enforce automatically.** Each fact has exactly one canonical home;
   every other copy is generated/synced from it (marked `DO NOT EDIT`) and verified by automation. No
   hand-maintained duplication.
3. **Self-sufficiency.** All context needed to act lives **in the repos** — this manual, each repo's
   `CLAUDE.md`, the `ai-docs/`, and self-contained issues. Never rely on chat history or a person to
   relay instructions between sessions.

---

## Where everything lives (single sources of truth)

| Domain | Source of truth |
|---|---|
| This operating manual | `norikit/ai-docs/framework.md` (here) |
| Mission, prime directives, conventions | `norikit/ai-docs/mission.md`, `conventions.md` |
| Tool roster | `norikit/ai-docs/projects.toml` _(in progress)_ → generates the roster tables |
| Project (per-tool) design knowledge | each repo's `ai-docs/` (decisions, architecture, status, …) |
| Repo scaffold / shared boilerplate | the `template` repo _(synced via tooling, in progress)_ |
| CI pipeline | `.github` reusable workflow _(in progress)_ |

**Rule:** never hand-edit a generated/synced file (it carries a `DO NOT EDIT — generated from <source>`
header). Change the source and regenerate.

---

## How work is tracked — enforced scrumban (GitHub Projects)

All work is tracked on **GitHub Projects** (private boards). **No implementation before a tracked issue exists.**

- **One board per tool** (noribar, noricore, …) + an **[ecosystem board](https://github.com/orgs/norikit/projects/15)**
  for org-wide / cross-cutting / infra work + a private **security** board. Infra repos (norikit, .github,
  template) have no board — their work lives on **ecosystem**.
- **Status flow (columns):** Backlog → To Do → In Progress → In Review → Ready to Merge → Done.
- **Org issue types** (the *nature* of work): Feature · Bug · Chore · Spike · Docs. Hierarchy
  (epic ▸ story ▸ task) is expressed with **sub-issues**, not types.
- **Org issue fields:** Priority (Urgent/High/Medium/Low) · Size (XS–XL) · Blocked · Start/Target date.
- **Intake:** create issues with the per-type **issue forms** _(in progress)_; they include a
  **Definition of Done** checklist.

Creating/operating issues (the `gh` recipe):
- `gh issue create --repo norikit/<repo> --project "<board>" --title … --body …` (always add to the right board).
- Set the nature via GraphQL `updateIssueIssueType`; link a child with `addSubIssue`; set Priority/Size
  via the org issue-field API; Status auto-sets to Backlog via the board's "item added" workflow.

---

## The working agreement (follow this for every piece of work)

1. **Board-first** — no code without a tracked issue; find or create it on the right board (add via `--project`).
2. **Definition of Ready** — before pulling: typed · Priority + Size set · rich description. If it's
   **larger than size L, split** it into an epic + stories.
3. **Pull one** — move a single issue To Do → In Progress (WIP-limited: one focus).
4. **Branch** off fresh `origin/main`, named **`<type>/<issue#>-<slug>`** (`type ∈ feat, fix, chore, spike, docs`).
5. **Work + commit** with **Conventional Commits**. Capture stray findings as **new issues** (no scope
   creep); if stuck, set the **Blocked** field and link the blocker.
6. **Open a PR linked to the issue** (`Closes #…`), Conventional-Commit title; body = what · why · how-verified.
7. **Clear the gates** — CI green · resolve every AI-review thread · tick the DoD checklist · `ai-docs`
   updated **in the same PR** · **verify behavior (not just green CI)** · update from `main` before merging.
8. **Merge** (manual click, squash) → the issue auto-closes → Done. **Roll up:** update/close the parent
   epic; when a **Milestone**'s stories are all Done, that's the release trigger.
   - **Spike exception:** a Spike closes when its GO/NO-GO decision is recorded in `ai-docs` (any PoC lives
     under `tasks/<id>/code/`, not `Sources/`); it may have no production PR.

**Standing rules:** GitHub issues are the source of truth (your internal todo list is scratch);
**decompose big asks into epic + sub-issues on the board first**, then work them one at a time.

---

## Task-authoring standard

- **Decompose** epic ▸ story ▸ task (hierarchy via sub-issues). Split anything **> size L**; one coherent
  deliverable per task.
- **Every issue body carries:** context/why · scope (in/out) · acceptance criteria · DoD (from the form) ·
  links (parent epic, related, `ai-docs`). Spikes also: question · time-box · expected decision.
- **Sizing rubric:** XS trivial/minutes · S ~hours · M ~a day · L multi-day · XL too big → break it down.

---

## Branching & releases

- **Branch naming:** `<type>/<issue#>-<slug>` (e.g. `feat/42-symbol-draw-on`).
- **Conventional Commits** for PR titles → enables automated changelog/release notes.
- **Trunk-based:** small branches/PRs straight to `main`; keep incomplete work **unwired / behind a flag**
  so `main` stays releasable.
- **Releases are Milestone-gated:** tag `main` (semver) when a Milestone's stories are all Done = the
  "complete piece." Branch granularity (per task) is decoupled from release completeness (per Milestone).
- **No auto-merge** (deliberate human merge click). Merge queue parked until volume warrants.

---

## Quality system

See **[repo-conformance.md](repo-conformance.md)** for the full picture (the two enforcement layers,
how to run the conformance gate, and operator setup). In brief:

- **Content conformance:** `tools/org_doctor.py` (roster · scaffold · tokens · badges · standalone) —
  run on PRs + weekly via the `org-doctor` workflow; derived artifacts regenerate via `propagate-roster`.
- **Branch ruleset on `main`** (`tools/apply_org_ruleset.sh`): require a PR · 0 approvals · require
  conversation resolution · squash-only · no force-push · no deletion · no bypass.
- **CI** (reusable workflow): build · test · lint · DoD gate.
- _Deferred (operator setup): formatting via autofix.ci · AI review (pin action first) · `ORG_AUTOMATION_TOKEN`._

---

## Common recipes

- **Add a tool:** edit `projects.toml`, run `gen_roster`; create the repo from `template`; record day-one
  decisions in its `ai-docs/decisions.md` (incl. the locked standalone-first decision).
- **Change the roster:** edit `projects.toml` only → regenerate the tables (never hand-edit them).
- **Evolve the scaffold:** edit `template` → run `sync_scaffold` (it preserves each repo's `project` regions).
- **Change a directive:** edit the doctrine in `norikit/ai-docs` once; it's referenced, not copied.

---

This manual is itself a single source of truth — keep it current in the same change that alters how we work.
The ecosystem-wide mission and conventions live alongside it in [`norikit/ai-docs/`](.).

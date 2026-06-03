# Repo conformance & enforcement

How the norikit framework stays true across every repo. Two layers: **content
conformance** (are the managed/derived files correct?) and **process enforcement**
(can a change reach `main` without going through the agreement?).

## Layer 1 — content conformance (`org_doctor`)

`tools/org_doctor.py` is the single conformance gate. It composes the other tools'
`--check` modes into one PASS/FAIL report:

| Check | Verifies |
|---|---|
| **roster** | `projects.md`, the README roster region, and the `.github` profile table all match `ai-docs/projects.toml` (`gen_roster --check`) |
| **scaffold** | every repo's managed files match `template/` (`sync_scaffold --check`); flags repos needing one-time `MIGRATE` |
| **tokens** | no leftover `{{...}}` scaffold tokens anywhere |
| **badges** | no shields.io badges (removed by decision) |
| **standalone-first** | every tool's `ai-docs/decisions.md` records the inherited standalone-first directive |

**Run it:**
- Locally: `python3 tools/org_doctor.py` (expects sibling repos checked out beside `norikit/`).
- In CI: the **`org-doctor`** workflow runs it on PRs that touch the framework surface, and on a
  weekly schedule + manual dispatch — the scheduled run also refreshes `ecosystem/` and opens a
  mechanical PR / files an issue on drift.

When sources change, derived artifacts regenerate automatically: **`propagate-roster`** opens a
mechanical PR whenever `ai-docs/projects.toml` changes on `main`.

## Layer 2 — process enforcement (org branch ruleset)

A single org-wide ruleset guards every repo's default branch. Apply/update it with:

```sh
bash tools/apply_org_ruleset.sh        # requires gh auth as a norikit org admin
```

It enforces the locked working agreement:

- **PRs required** to reach the default branch — no direct pushes.
- **0 required approvals** — a solo owner can't self-approve; quality comes from checks and review
  threads, not an approval click.
- **Require conversation resolution** before merge.
- **Squash-only** merges (merge-commit and rebase disabled).
- **Block force-push and branch deletion.**
- **Active**, with no standing bypass actors (the owner edits the ruleset to grant a temporary
  bypass in an emergency).

**Not yet enforced — required status checks.** CI check context names differ across repos
(reusable `swift-ci` ⇒ `CI / Build & test`; the inline stack-agnostic `ci.yml` ⇒ `Build & test`).
A single org-wide required context would block merges wherever it doesn't match. Unify CI naming,
then add a `required_status_checks` rule to `apply_org_ruleset.sh`.

## Operator setup (one-time, owner-only)

These need org-admin actions outside this repo:

- **`ORG_AUTOMATION_TOKEN`** — a fine-grained PAT (contents + PR write on `norikit` and
  `norikit/.github`) added as a repo secret. Lets the propagation workflows open *and auto-merge*
  mechanical PRs hands-off (incl. the cross-repo `.github` profile table). Without it the bot PRs
  still open; they just need a manual merge.
- **autofix.ci** — install the GitHub App for the org to get formatting autofix on PRs.
- **AI review** — currently disabled (`claude-code-action` invocation stall); see the re-enable
  issue. Pin the action/CLI to a known-good version before turning it back on.

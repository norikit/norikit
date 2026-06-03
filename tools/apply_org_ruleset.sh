#!/usr/bin/env bash
# apply_org_ruleset.sh — create/update the org-wide branch-protection ruleset on
# every repo's default branch. Idempotent (updates the ruleset if it exists).
#
# Requires: `gh` authenticated as a norikit ORG ADMIN/OWNER.
# Run:      bash tools/apply_org_ruleset.sh
#
# Enforces the locked working agreement (Phase 7) as ONE org-wide rule:
#   - PRs required to reach the default branch (no direct pushes)
#   - 0 required approvals  (a solo owner can't self-approve; quality comes from
#     checks + review threads, not an approval click)
#   - require conversation resolution before merge
#   - squash-only merges (merge-commit and rebase disabled)
#   - block force-push (non-fast-forward) and branch deletion
#   - active enforcement, no standing bypass actors (owner edits the ruleset to
#     grant a temporary bypass in emergencies)
#
# NOTE — required status checks are intentionally OMITTED. CI check *context*
# names differ across repos (reusable swift-ci => "CI / Build & test"; the inline
# stack-agnostic ci.yml => "Build & test"), so a single org-wide required context
# would block merges wherever it doesn't match. Unify CI naming first, then add a
# `required_status_checks` rule here.
set -euo pipefail

ORG=norikit
NAME="main protection"

RULES=$(cat <<'JSON'
{
  "name": "main protection",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name":        { "include": ["~DEFAULT_BRANCH"], "exclude": [] },
    "repository_name": { "include": ["~ALL"],            "exclude": [] }
  },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "pull_request", "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": false,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": true,
        "allowed_merge_methods": ["squash"]
    }}
  ],
  "bypass_actors": []
}
JSON
)

existing=$(gh api "orgs/$ORG/rulesets" --jq ".[] | select(.name==\"$NAME\") | .id" 2>/dev/null || true)
if [ -n "$existing" ]; then
  echo "Updating existing ruleset #$existing ..."
  printf '%s' "$RULES" | gh api -X PUT "orgs/$ORG/rulesets/$existing" --input -
else
  echo "Creating ruleset \"$NAME\" ..."
  printf '%s' "$RULES" | gh api -X POST "orgs/$ORG/rulesets" --input -
fi
echo "✓ ruleset applied to all $ORG repos (default branch)."

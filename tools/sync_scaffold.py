#!/usr/bin/env python3
"""sync_scaffold — propagate `template`'s managed scaffold files into every norikit repo.

Reads `scaffold.manifest` (which files `template` owns + how to apply them), then for each
target repo:
  - mode "verbatim": copy template's file exactly.
  - mode "tree":     copy every file under a template directory exactly.
  - mode "regions":  update the synced ``<!-- norikit:managed -->`` block while PRESERVING the
                     repo's own ``<!-- norikit:project:start/end -->`` region.

Safety: a "regions" target that LACKS the markers is never overwritten — it's reported as
``MIGRATE`` (so existing hand-written CLAUDE.md content is not clobbered; convert it once by
hand into the marker format, after which sync maintains the managed block).

This is dev-time tooling — NOT a runtime dependency of any tool. Python 3.11+ (stdlib only).

Usage:
    python3 tools/sync_scaffold.py [--check] [--repos a,b,c]
      --check   report drift only; change nothing; exit 1 if anything is out of sync.
      --repos   comma-separated repo names (default: all sibling git repos except infra).
"""
from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ORG_ROOT = TOOLS.parents[1]            # tools -> norikit -> org root
TEMPLATE = ORG_ROOT / "template"
MANIFEST = TOOLS / "scaffold.manifest"

# Infra repos handled specially (template = source; .github = org-default-files repo).
EXCLUDE = {"template", ".github"}

PROJ_START = "norikit:project:start"
PROJ_END = "norikit:project:end"


def load_manifest() -> list[dict]:
    with MANIFEST.open("rb") as f:
        return tomllib.load(f).get("managed", [])


def discover_repos() -> list[str]:
    return sorted(
        p.name for p in ORG_ROOT.iterdir()
        if p.is_dir() and (p / ".git").exists() and p.name not in EXCLUDE
    )


def split_project_region(text: str):
    """Return (before_incl_start, region_body, after_incl_end) or None if markers absent."""
    lines = text.splitlines(keepends=True)
    start = end = None
    for i, ln in enumerate(lines):
        if PROJ_START in ln and start is None:
            start = i
        if PROJ_END in ln:
            end = i
    if start is None or end is None or end <= start:
        return None
    return "".join(lines[:start + 1]), "".join(lines[start + 1:end]), "".join(lines[end:])


def substitute_tokens(text: str, repo: str) -> str:
    # Minimal substitution; tagline/role come from the roster (gen_roster) later.
    return text.replace("{{PROJECT}}", repo)


def sync_regions(tmpl_path: Path, tgt_path: Path, repo: str):
    """Return (action, new_text|None). action ∈ {ok, create, update, migrate}."""
    tmpl = substitute_tokens(tmpl_path.read_text(), repo)
    if not tgt_path.exists():
        return "create", tmpl
    tgt = tgt_path.read_text()
    parts = split_project_region(tmpl)
    if parts is None:                                   # template not region-formatted
        return ("ok", None) if tgt == tmpl else ("update", tmpl)
    before, tmpl_region, after = parts
    g = split_project_region(tgt)
    if g is None:
        return "migrate", None                          # don't clobber un-marked content
    merged = before + g[1] + after
    return ("ok", None) if merged == tgt else ("update", merged)


def sync_verbatim(tmpl_path: Path, tgt_path: Path, repo: str):
    tmpl = substitute_tokens(tmpl_path.read_text(), repo)
    if not tgt_path.exists():
        return "create", tmpl
    return ("ok", None) if tgt_path.read_text() == tmpl else ("update", tmpl)


def apply_entry(entry: dict, root: Path, repo: str, check: bool):
    """Process one manifest entry against one repo. Returns (changes, migrations)."""
    path, mode = entry["path"], entry["mode"]
    changes: list[tuple[str, str]] = []
    migrations: list[str] = []

    def handle(tmpl_file: Path, rel: str, fn):
        action, new = fn(tmpl_file, root / rel, repo)
        if action == "migrate":
            migrations.append(rel)
        elif action != "ok":
            changes.append((rel, action))
            if not check:
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_text(new)

    if mode == "tree":
        for tf in sorted((TEMPLATE / path).rglob("*")):
            if tf.is_file():
                handle(tf, str(tf.relative_to(TEMPLATE)), sync_verbatim)
    else:
        fn = sync_regions if mode == "regions" else sync_verbatim
        handle(TEMPLATE / path, path, fn)
    return changes, migrations


def main() -> None:
    ap = argparse.ArgumentParser(description="Propagate template's managed files to norikit repos.")
    ap.add_argument("--check", action="store_true", help="report drift only; exit 1 if out of sync")
    ap.add_argument("--repos", help="comma-separated repo names (default: all sibling repos except infra)")
    args = ap.parse_args()

    manifest = load_manifest()
    repos = [r.strip() for r in args.repos.split(",")] if args.repos else discover_repos()
    drift = False

    for repo in repos:
        root = ORG_ROOT / repo
        if not root.exists():
            print(f"  ! {repo}: not found — skipping")
            continue
        changes: list[tuple[str, str]] = []
        migrations: list[str] = []
        for entry in manifest:
            c, m = apply_entry(entry, root, repo, args.check)
            changes += c
            migrations += m

        if changes or migrations:
            drift = True
            print(f"  ~ {repo}:")
            for rel, action in changes:
                print(f"      {action:7} {rel}")
            for rel in migrations:
                print(f"      MIGRATE {rel}  (no norikit:project markers — convert by hand once)")
        else:
            print(f"  ✓ {repo}: in sync")

    if args.check and drift:
        print("\nDrift detected. Run without --check to apply "
              "(MIGRATE items need a one-time manual conversion).")
        sys.exit(1)


if __name__ == "__main__":
    main()

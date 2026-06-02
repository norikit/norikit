#!/usr/bin/env python3
"""org_doctor — cross-repo conformance check for the norikit ecosystem.

Composes the framework's invariants into one report; exits 1 if anything is non-conformant.
Intended for ad-hoc runs and the scheduled org-doctor Action (Phase 7).

Checks:
  roster      — gen_roster --check (projects.md / README match projects.toml)
  scaffold    — sync_scaffold --check (template's managed files propagated)
  tokens      — no {{…}} / <!-- TEMPLATE leftovers (excludes `template`, where tokens are correct)
  badges      — no shields.io badges in READMEs / org profile (the org dropped them)
  standalone  — each tool's ai-docs/decisions.md records the standalone-first decision

Usage:  python3 tools/org_doctor.py
Python 3.11+, stdlib only. Dev-time tooling — not a runtime dependency.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent
ORG_ROOT = REPO.parent

TOOL_REPOS = ["noribar", "noricore", "noriglaze", "noribento", "noribox",
              "noricut", "norify", "noripad", "noripaper", "noriset"]
SKIP_PARTS = {".git", "CLua", ".build", "DerivedData", "node_modules"}
TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".toml"}
TOKEN_RE = re.compile(r"\{\{[A-Za-z0-9_]+\}\}|<!--\s*TEMPLATE")


def repos() -> list[Path]:
    return sorted(p for p in ORG_ROOT.iterdir() if (p / ".git").exists())


def run_subcheck(script: str) -> bool:
    return subprocess.run(
        [sys.executable, str(TOOLS / script), "--check"],
        capture_output=True, text=True,
    ).returncode == 0


def check_tokens() -> list[str]:
    hits: list[str] = []
    for repo in repos():
        if repo.name == "template":              # tokens are correct in the template
            continue
        for f in repo.rglob("*"):
            if not f.is_file() or f.suffix not in TEXT_SUFFIXES or SKIP_PARTS & set(f.parts):
                continue
            try:
                if TOKEN_RE.search(f.read_text()):
                    hits.append(str(f.relative_to(ORG_ROOT)))
            except (UnicodeDecodeError, OSError):
                pass
    return hits


def check_badges() -> list[str]:
    hits: list[str] = []
    candidates = [ORG_ROOT / ".github" / "profile" / "README.md"]
    candidates += [repo / "README.md" for repo in repos()]
    for f in candidates:
        try:
            if f.is_file() and "img.shields.io" in f.read_text():
                hits.append(str(f.relative_to(ORG_ROOT)))
        except OSError:
            pass
    return hits


def check_standalone() -> list[str]:
    missing: list[str] = []
    for name in TOOL_REPOS:
        d = ORG_ROOT / name / "ai-docs" / "decisions.md"
        if not d.exists():
            missing.append(f"{name} (no ai-docs/decisions.md)")
        elif "standalone-first" not in d.read_text().lower():
            missing.append(f"{name} (decisions.md lacks standalone-first)")
    return missing


def main() -> None:
    results: list[tuple[str, bool, str]] = []

    results.append(("roster", run_subcheck("gen_roster.py"),
                    "roster tables drift from projects.toml — run gen_roster"))
    results.append(("scaffold", run_subcheck("sync_scaffold.py"),
                    "managed files not propagated — run sync_scaffold (some repos need MIGRATE)"))

    tok = check_tokens()
    results.append(("tokens", not tok,
                    f"{len(tok)} file(s) with leftovers: " + ", ".join(tok[:8]) + ("…" if len(tok) > 8 else "")))
    bad = check_badges()
    results.append(("badges", not bad, "shields.io badges in: " + ", ".join(bad)))
    sa = check_standalone()
    results.append(("standalone-first", not sa, "missing in: " + ", ".join(sa)))

    print("norikit org-doctor — conformance report\n")
    failed = 0
    for name, ok, detail in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if not ok else ""))
        failed += not ok
    print(f"\n{len(results) - failed}/{len(results)} checks passing.")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()

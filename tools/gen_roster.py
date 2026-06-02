#!/usr/bin/env python3
"""gen_roster — render the norikit roster from ai-docs/projects.toml (the single source of truth).

Generates (DO NOT hand-edit the outputs — change the TOML and re-run):
  - ai-docs/projects.md   the full roster reference (whole file)
  - README.md             the roster table, between <!-- norikit:roster:start/end -->

(The `.github` org-profile table is generated in a follow-up, once tool icons are reconciled.)

Usage:
    python3 tools/gen_roster.py [--check]
      --check   report drift, write nothing, exit 1 if anything is out of sync (CI-friendly).

Python 3.11+, stdlib only. Dev-time tooling — not a runtime dependency.
"""
from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent                       # norikit repo root
TOML = REPO / "ai-docs" / "projects.toml"
ORG = "https://github.com/norikit"

BADGE = {"active": "🚧 Active", "early": "🌱 Early", "placeholder": "🥚 Stub"}
RANK = {"active": 0, "early": 1, "placeholder": 2}
GEN = "<!-- DO NOT EDIT — generated from ai-docs/projects.toml by tools/gen_roster.py. -->"
START, END = "<!-- norikit:roster:start -->", "<!-- norikit:roster:end -->"


def load():
    with TOML.open("rb") as f:
        data = tomllib.load(f)
    tools = sorted(data.get("tool", []), key=lambda t: (RANK.get(t["status"], 9), t["name"]))
    return tools, data.get("infra", [])


def tool_table(tools: list[dict]) -> str:
    rows = ["| Tool | What it is | Status |", "|---|---|---|"]
    for t in tools:
        rows.append(f"| [{t['name']}]({ORG}/{t['name']}) | {t['tagline']} | {BADGE.get(t['status'], t['status'])} |")
    return "\n".join(rows)


def projects_md(tools: list[dict], infra: list[dict]) -> str:
    out = [GEN, "", "# norikit — project roster", "",
           "The toolkit, generated from `ai-docs/projects.toml`. To change it, edit the TOML and run",
           "`tools/gen_roster.py` — never hand-edit this file.", "",
           tool_table(tools), "", "## Infrastructure", ""]
    out += [f"- [{i['name']}]({ORG}/{i['name']}) — {i['role']}" for i in infra]
    graph = [t for t in tools if t.get("provides") or t.get("consumes")]
    if graph:
        out += ["", "## Ecosystem integration", "",
                "*Optional, availability-gated progressive enhancement — never a hard dependency.*", ""]
        for t in graph:
            bits = []
            if t.get("provides"):
                bits.append("provides " + ", ".join(t["provides"]))
            if t.get("consumes"):
                bits.append("consumes " + ", ".join(t["consumes"]))
            out.append(f"- **{t['name']}** — {'; '.join(bits)}")
    return "\n".join(out) + "\n"


def replace_region(text: str, body: str) -> str | None:
    if START not in text or END not in text:
        return None
    pre, rest = text.split(START, 1)
    _, post = rest.split(END, 1)
    return f"{pre}{START}\n{GEN}\n\n{body}\n{END}{post}"


def main() -> None:
    ap = argparse.ArgumentParser(description="Render the roster from projects.toml.")
    ap.add_argument("--check", action="store_true", help="report drift; write nothing; exit 1 if drift")
    args = ap.parse_args()

    tools, infra = load()
    targets: list[tuple[Path, str]] = [(REPO / "ai-docs" / "projects.md", projects_md(tools, infra))]

    readme = REPO / "README.md"
    if readme.exists():
        merged = replace_region(readme.read_text(), tool_table(tools))
        if merged is None:
            print("  ! README.md lacks roster markers (norikit:roster:start/end) — skipping")
        else:
            targets.append((readme, merged))

    drift = False
    for path, content in targets:
        rel = path.relative_to(REPO)
        if path.exists() and path.read_text() == content:
            print(f"  ✓ {rel}: in sync")
        else:
            drift = True
            print(f"  ~ {rel}: would update")
            if not args.check:
                path.write_text(content)

    if args.check and drift:
        print("\nDrift detected — run without --check to regenerate.")
        sys.exit(1)


if __name__ == "__main__":
    main()

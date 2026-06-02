# norikit/tools — org framework tooling

Dev-time scripts that keep the ecosystem consistent ("define once, derive everywhere").
Python 3.11+, stdlib only. They operate on the sibling repo checkouts under the org root
(`/…/norikit/<repo>`). **None of these are runtime dependencies of any tool.**

| Tool | Purpose | Status |
|---|---|---|
| **`sync_scaffold.py`** | Propagate `template`'s managed scaffold files (per `scaffold.manifest`) into every repo, preserving each repo's `norikit:project` region. | ✅ |
| `gen_roster.py` | Render the roster tables from `ai-docs/projects.toml`. | planned (#20) |
| `aggregate_docs.py` | Compile each repo's `ai-docs/` into `norikit/ecosystem/`. | planned (#22) |
| `org_doctor.py` | Cross-repo conformance check (roster sync, scaffold currency, no token leftovers, …). | planned (#22) |

## sync_scaffold

```
python3 tools/sync_scaffold.py [--check] [--repos a,b,c]
```

- `--check` — report drift, change nothing, exit 1 if anything is out of sync (CI-friendly).
- `--repos` — limit to specific repos (default: all sibling git repos except `template`/`.github`).

**Modes** (declared in `scaffold.manifest`): `verbatim` (copy exactly) · `tree` (copy a directory
exactly) · `regions` (sync the `<!-- norikit:managed -->` block, **preserve** the repo's
`<!-- norikit:project:start/end -->` region).

**Migration safety:** a `regions` file that lacks the markers is reported `MIGRATE` and left
untouched — convert it by hand once (move its content into a `norikit:project` region), after which
sync maintains the managed block automatically.

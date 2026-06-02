---
paths:
  - "ai-docs/projects.md"
  - "ecosystem/**"
  - "README.md"
---

# These files are generated — do not hand-edit

- **`ai-docs/projects.md`** and the **`README.md` roster region** (between
  `<!-- norikit:roster:start/end -->`) are rendered from **`ai-docs/projects.toml`**
  by `tools/gen_roster.py`. To change the roster, edit the TOML and run that tool.
- **`ecosystem/**`** is a read-only mirror of every repo's `ai-docs/`, compiled by
  `tools/aggregate_docs.py`. Edit the source repo's `ai-docs/`, not the mirror.

Hand edits to any of these are overwritten on the next generate/sync. (Outside the
roster markers, the rest of `README.md` is hand-written and fine to edit.)

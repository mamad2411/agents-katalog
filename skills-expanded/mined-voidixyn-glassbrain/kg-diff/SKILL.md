---
name: kg-diff
description: Show what changed in a knowledge graph between two versions or git commits, as a summary and a side-by-side view. Use after changing a graph, to review someone else's change, or when asked what changed.
---

# kg-diff

- Uncommitted changes (working tree vs `HEAD`): `npx glassbrain diff <path>`
- What the last commit changed: `npx glassbrain diff HEAD~1 <path>`
- Against any commit: `npx glassbrain diff <git-ref> <path>` (e.g. `HEAD~3`, `main`)
- Two folders or files: `npx glassbrain diff <old> <new>`

It prints added / removed / changed / moved nodes and edges (edges pointing at missing nodes are left out; `validate` reports those). Summarize that for the user in a few lines, by meaning rather than by id ("the billing area moved under accounts; 12 new refund pages"). Use `--json` to read it precisely, `--ignore <field,…>` for fields that change on every rebuild.

To show it, add `--open` (side-by-side page with the changes highlighted) and tell the user the path it printed.

---
name: notes-inventory
description: List every macOS Notes account, folder (including nested subfolders), and per-folder note count — the sidebar as machine-readable data. Use to see what exists before organizing, to answer "how many notes are in X", or as the first step of an audit/export. Read-only, safe. TRIGGERS - list my notes folders, notes inventory, how many notes, what folders do I have, show my notes structure.
allowed-tools: Bash
---

# notes-inventory — the Notes sidebar as data

> **Self-Evolving skill** — if macOS Notes' AppleScript behavior drifts from what's below (folder flattening, trash visibility, counts), fix this SKILL.md and the shared engine `scripts/lib/notes-core.ts` / `scripts/notes.ts` (+ a test in `notes-core.test.ts`); see the Post-Execution Reflection at the bottom.

Read-only survey of the whole Notes tree, across ALL accounts (iCloud, Google, Exchange…).

```bash
NC="$HOME/.claude/plugins/marketplaces/cc-skills/plugins/notes-commander/scripts/notes.ts"
bun "$NC" inventory            # human tree: account → folders (indented) with counts
bun "$NC" inventory --json     # [{account, path, count}, …] for analysis
```

- Nested folders appear as paths with `/` separators (e.g. `To-Do / Done`) — folder **names are not unique** (two "Done" folders is normal), paths are.
- Counts are **direct** notes per folder (subfolder notes count under the subfolder), matching the Notes sidebar.
- `Recently Deleted` IS visible to AppleScript (verified live 2026-07-18) — inventory shows it but reports its notes separately from the live total; `export` skips it entirely.
- First run may prompt once for Automation permission to control Notes; one AppleScript pass, so it's fast even on hundreds of notes.
- If it fails with `-600`/"not running" repeatedly, open Notes once, then retry (the engine already retries transient errors).

This is the data source the `notes-audit` skill analyzes and the `notes-organize` skill acts on.

## Post-Execution Reflection

After an inventory run, check: (1) did the tree match the Notes sidebar (folders, nesting, counts)? If not, the flattened-`folders of account` filter or trash handling drifted — fix `OSA_INVENTORY` in `scripts/notes.ts` and document the macOS change here. (2) Did a transient `-600`/`-1712` require a manual retry? If the built-in retry didn't absorb it, tune `runOsa` in `notes-core.ts`. Only update for real, reproducible drift — not speculation.

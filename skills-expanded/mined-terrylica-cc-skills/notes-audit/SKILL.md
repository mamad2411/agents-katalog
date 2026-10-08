---
name: notes-audit
description: Analyze the macOS Notes folder taxonomy and propose a better organization - find empty/near-empty folders, oversized dumping grounds, duplicate-purpose folders, mixed-language naming, and stale content; then present a target hierarchy for operator approval BEFORE any moves. Use when notes feel sporadic/messy, before a big cleanup, or to review organization health periodically. TRIGGERS - audit my notes, notes are a mess, propose notes organization, analyze notes folders, notes cleanup plan.
allowed-tools: Bash, Read
---

# notes-audit — analyze, then PROPOSE (never act unilaterally)

> **Self-Evolving skill** — if the smell table stops matching how the operator actually organizes (new smells found, false positives), evolve the table in this SKILL.md; see the Post-Execution Reflection at the bottom.

This skill is an analysis workflow, not a script: you (Claude) gather the data with the
plugin's CLIs, reason over it, and present a proposal. **No reorganization happens in this
skill** — execution belongs to `notes-organize`, only after operator approval.

## 1. Gather

```bash
NC="$HOME/.claude/plugins/marketplaces/cc-skills/plugins/notes-commander/scripts/notes.ts"
bun "$NC" inventory --json          # folder tree + counts (fast; always do this)
bun "$NC" export                    # full snapshot when content-level analysis is wanted
```

For content-level auditing, Read the snapshot's `manifest.json` (note names, per-note
modified dates, char counts) and sample individual markdown files — do NOT paste hundreds of
notes into context; sample representatives per folder.

## 2. Analyze — look for these smells

| Smell                    | Signal in the data                                        | Typical proposal                                               |
| ------------------------ | --------------------------------------------------------- | -------------------------------------------------------------- |
| Empty/near-empty folders | `count` 0–2                                               | merge into a sibling or an `Archive`                           |
| Dumping ground           | one folder ≫ others (e.g. a 100+ default "Notes")         | split by detected themes                                       |
| Duplicate purpose        | two folders whose names/content overlap                   | merge, keep the better-named one                               |
| Mixed-language taxonomy  | sibling folders in different languages for related topics | group under one parent per domain, keep native names as leaves |
| Stale content            | manifest `modified` dates years old across a folder       | move to `Archive / <year>`                                     |
| Deep-vs-flat mismatch    | 20+ flat top-level folders                                | introduce 3–6 domain parents, nest leaves                      |

Respect what's working: don't propose churn for folders that are already coherent.

## 3. Propose

Present, in this order:

1. **A target hierarchy** (tree view) with each existing folder's destination.
2. **The move list** — the exact `mkdir` / `move-note` / `merge-folder` commands (with `--dry-run` variants) that implement it.
3. **Manual items** — anything the tooling deliberately won't do: deleting emptied folders, cross-account moves, tag cleanup (no AppleScript API for tags).

Then STOP and get explicit approval. On approval, hand off to `notes-organize` and follow its
safety protocol (snapshot → dry-run → execute → verify counts).

## Post-Execution Reflection

After an audit, check: (1) did the operator reject/modify parts of the proposal? Their reasoning is a missing smell or a wrong default — encode it in the smell table. (2) Did any proposal require a capability the tooling lacks (tags, cross-account)? Confirm it's listed under manual items. (3) Did sampling miss something the operator knew about a folder? Note the folder type so the next audit samples it deeper. Update only for real, reproducible gaps.

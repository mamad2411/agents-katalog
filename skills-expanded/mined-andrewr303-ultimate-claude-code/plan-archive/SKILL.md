---
name: plan-archive
description: >
  Merge a CHANGE's delta specs into docs/plan/truth/ and move the folder
  to changes/archive/. Use when the user says archive, sync specs, merge
  deltas, opsx archive, or runs /ultimate-sdd:archive or /ultimate-sdd:sync.
license: MIT
metadata:
  author: andrewr303
  version: "2.2"
---

Close a change. Merge first, move second.

**Supporting files:** `references/openspec.md`, `scripts/merge_deltas.py`, `scripts/validate_plan.py`.

**Modes:** `/ultimate-sdd:sync` or "sync only" → merge, do not move. `/ultimate-sdd:archive` → merge (unless they skip) then move.

## Steps

### 1. Select

Active CHANGE-n or slug under `docs/plan/changes/` (not already in `archive/`). Announce it.

### 2. Warn, don't block

- Incomplete artifacts (no deltas and not `skip_specs`; missing design is fine).
- Linked REQs not `done`, or TASKs still open.
- Verify record missing.

Show the warnings. Ask to proceed unless they already said archive anyway.

### 3. Sync (merge)

If `skip_specs: true`: say so and skip to step 4.

Otherwise dry-run:

```
python <plugin>/scripts/plan.py archive --root docs/plan --change <slug> --dry-run
python <plugin>/scripts/merge_deltas.py --root docs/plan --change <slug> --dry-run
```

Show the log (ADDED / MODIFIED / REMOVED / created / retired). Confirm:

- **Sync now** (Recommended)
- **Archive without syncing** (archive mode only)
- **Cancel**

On sync, run the same command without `--dry-run`. Then **re-read** each `truth/<domain>/spec.md` and check:

- ADDED names present
- MODIFIED text matches the delta (other requirements untouched)
- REMOVED names gone
- Retired domain: file deleted only when `retire_capabilities: true`

If any check fails, stop. Do not move the folder.

Never start a merge and a move in parallel.

### 4. Move (archive mode)

Target: `docs/plan/changes/archive/YYYY-MM-DD-<slug>/`. If the slug already starts with `YYYY-MM-DD-`, do not stack a second date. Fail if the target exists.

Set `status: archived` on CHANGE.md (after or as you move). Update linked REQs only if needed (they should already be `done`).

### 5. Index

Remove the CHANGE from Active changes. Add an Archive line. Next = the remaining board. Run `validate_plan.py`.

## Guardrails

- Merge is the source of truth update. Moving without sync leaves truth stale — only do it when they choose that.
- Do not rewrite requirement names during merge. The script is the merge.
- Do not delete a truth file unless retire was declared and the last requirement was REMOVED.
- Do not call an OpenSpec CLI.

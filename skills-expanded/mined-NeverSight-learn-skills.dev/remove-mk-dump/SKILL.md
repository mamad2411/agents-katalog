---
name: remove-mk-dump
version: 1.0.0
description: Removes a non-kicked dump session file and updates dump-index.md to reflect the removal. Use when user runs /remove-mk-dump or wants to delete a dump session that has not yet been kicked.
user-invocable: true
---

# remove-mk-dump

Deletes a non-kicked dump session file and keeps `dump-index.md` consistent.

## Flow

**Step 1: Init guard**

Check `docs/monkey-brain/MONKEY_BRAIN_TEMPLATE.md` exists — if not, tell user to run `/init-mk-dump` first → stop.

**Step 2: List removable sessions**

Read `docs/monkey-brain/dump-index.md` Sessions table. Collect rows where Status ≠ `kicked`.

- No rows qualify → print: "No removable sessions found (all have been kicked)." → stop.

**Step 3: Select session**

- One row → use it automatically, show the filename.
- Multiple rows → display numbered list; ask user to pick one.

**Step 4: Confirm**

Show full file path. Ask: "Delete this session? (yes/no)"

- User says no → print "Cancelled." → stop.

**Step 5: Delete file**

Delete `docs/monkey-brain/dump-sessions/{row File path}`.

If file not found, note it (already gone) and continue — still clean up the index.

**Step 6: Update dump-index.md**

1. Remove the row for the deleted session from the Sessions table.
2. Check whether `latest:` points to the deleted session:
   - If yes → find the most recent remaining row in Sessions table (last row by position) and set `latest:` to its full path (`docs/monkey-brain/dump-sessions/{File}`); if no rows remain, set `latest:` to `none`.
   - If no → leave `latest:` unchanged.

**Step 7: Confirm**

Print: "Removed `{filename}`. dump-index updated."

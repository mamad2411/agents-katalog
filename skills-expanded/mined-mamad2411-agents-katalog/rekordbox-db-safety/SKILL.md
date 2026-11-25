---
name: rekordbox-db-safety
description: Safe patterns for reading and writing the rekordbox 6/7 master.db with pyrekordbox — backups, dry-runs, WAL checkpointing, fill-empty writes. Use whenever writing ANY script that modifies a rekordbox library.
---

# Safe rekordbox database manipulation

Rekordbox 6/7 stores the whole library in an encrypted SQLite DB:
`~/Library/Pioneer/rekordbox/master.db` (macOS). `pyrekordbox >= 0.4.4` opens it
read/write (earlier versions fail with `NoCachedKey`).

## The write contract — every write script MUST:

1. **Back up first.** Copy `master.db` to `master.db.backup-YYYYMMDD-HHMMSS`
   before any change. Note: `get_config("rekordbox6", "db_path")` returns no key
   on some builds — fall back to the hardcoded default path.
2. **Refuse to run while rekordbox is open.** `db.commit()` refuses anyway;
   check for the process and exit early with a clear message.
3. **Dry-run by default.** Print exactly what would change; write only with an
   explicit `--apply` flag. Always show the user the dry-run before applying.
4. **Fill empty fields only.** Never overwrite existing metadata (store-bought
   tracks carry accurate labels/genres). Fill-empty makes every script
   idempotent and safe to re-run.
5. **Checkpoint the WAL after commit.** pyrekordbox commits land in SQLite's
   write-ahead log; rekordbox may read a stale tree without:
   ```python
   db.session.connection().connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
   ```
6. **Verify counts.** Compare total track count (and any touched playlist's
   count) before/after. Report both to the user.

## Gotchas

- Fully quit (Cmd+Q) and relaunch rekordbox to see script-made changes.
- `move_playlist` rejects the root as a target — move a playlist to top level
  by setting `ParentID = "root"` directly.
- Delete/rename playlists by name across ALL parents, or you leave duplicates.
- Two playlists with the same track count are not necessarily duplicates —
  compare actual ContentIDs before merging (observed: same count, 0 shared).
- rekordbox uses soft deletes: set `rb_local_deleted = 1` + a fresh USN rather
  than DELETE, so device sync propagates removals.

## Division of labor

Use an MCP server / read-only queries for exploration and planning. Make every
mutation a standalone, deterministic, reviewable script following the contract
above. Never hand-edit rows interactively.

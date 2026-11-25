---
name: db-maintain
description: Run SQLite maintenance on all databases — integrity checks, WAL checkpoints, VACUUM, ANALYZE. Use when the user says "maintain databases", "check database health", "vacuum sqlite", "database maintenance", "WAL too big", or invokes /db-maintain. Also trigger proactively when WAL files are large or database operations seem slow.
allowed-tools: [Bash, Read]
---

# /db-maintain

Run maintenance on all SQLite databases on the newna.ai VPS.

## Databases

| Database | Path | Purpose |
|----------|------|---------|
| admin.db | `/home/sabro/projects/newna-admin/data/admin.db` | Admin panel (users, sessions, notes, alerts) |
| chat.db | `/home/sabro/projects/NewNa.Ai-ChatApp/chat.db` | Chat app (conversations, messages, meetings) |
| knowledge.db | `/home/sabro/projects/powerbi-knowledge-mcp/data/knowledge.db` | Power BI knowledge catalog |

## Maintenance Steps

For each database:

### 1. Check size and WAL
```bash
ls -lh <db-path> <db-path>-wal <db-path>-shm 2>/dev/null
```

### 2. Integrity check
```bash
sqlite3 <db-path> "PRAGMA integrity_check;"
```
If this reports anything other than "ok", the database is corrupted. STOP and warn the user.

### 3. WAL checkpoint
```bash
sqlite3 <db-path> "PRAGMA wal_checkpoint(TRUNCATE);"
```
This flushes the WAL back into the main database file and truncates the WAL.

### 4. ANALYZE
```bash
sqlite3 <db-path> "ANALYZE;"
```
Updates query planner statistics for better performance.

### 5. VACUUM (optional, ask first)
```bash
sqlite3 <db-path> "VACUUM;"
```
Rebuilds the database file, reclaiming free space. This can take a while on large databases and locks the file during execution. Ask the user before running on production databases during business hours.

### 6. Report sizes after maintenance
```bash
ls -lh <db-path> <db-path>-wal <db-path>-shm 2>/dev/null
```

## Output

Report for each database:
- Size before/after
- WAL size before/after
- Integrity check result
- Whether VACUUM was run
- Any issues found

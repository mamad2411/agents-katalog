---
name: config-backup
description: |
  Create and restore rolling backups of IntelliJ IDEA configuration.
  Manages timestamped ZIP backups with XML-tracked log for easy
  restoration by ID.
triggers:
  - /idea backup            # Create new backup
  - /idea restore           # List available backups
  - /idea restore [id]      # Restore specific backup
negative_triggers:
  - /idea sync-modules      # Use module-sync skill
  - /idea changelist        # Use changelist-mgmt skill
version: 1.0.0
author: Christian Kusmanow / Claude
last_updated: 2026-01-31
---

# Skill: IDEA Config Backup

Create and restore rolling backups of IntelliJ IDEA `.idea/` configuration.

## When to Use

- Before major structural changes
- Before module reorganization
- When experimenting with settings
- After making working configuration

## When NOT to Use

- For VCS operations (use git)
- For module management (use `/idea sync-modules`)
- For changelist work (use `/idea changelist`)

---

## Quick Start

1. **Create backup:** `/idea backup` - Snapshot current config
2. **List backups:** `/idea restore` - Show available backups
3. **Restore:** `/idea restore 3` - Restore backup #3

---

## Commands

### `/idea backup`

Create timestamped backup of `.idea/` directory:

1. **Create ZIP archive:**
   - Filename: `idea-backup-{timestamp}.zip`
   - Location: `.backups/idea/`

2. **Update backup log:**
   - Add entry to `backup-log.xml`
   - Include timestamp, ID, description

3. **Rolling cleanup:**
   - Keep last N backups (default: 10)
   - Delete older archives

**Output:**
```
Created backup #7: idea-backup-2026-01-31-143022.zip
Location: .backups/idea/
```

### `/idea restore`

List available backups:

```
Available IDEA Backups:
  #1  2026-01-28 09:15:22  Before module reorg
  #2  2026-01-29 14:30:45  After scope setup
  #3  2026-01-30 11:22:33  Pre-experiment
  #4  2026-01-31 14:30:22  Current config
```

### `/idea restore [id]`

Restore specific backup:

1. **Verify backup exists**
2. **Confirm with user** (destructive operation)
3. **Create safety backup** of current state
4. **Extract ZIP** to `.idea/`
5. **Notify reload required**

**Output:**
```
Restored backup #3 (2026-01-30 11:22:33)
Please restart IDEA to apply changes.
```

---

## Backup Structure

### Directory Layout

```
.backups/
└── idea/
    ├── backup-log.xml
    ├── idea-backup-2026-01-28-091522.zip
    ├── idea-backup-2026-01-29-143045.zip
    └── idea-backup-2026-01-31-143022.zip
```

### backup-log.xml Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<backups>
  <backup id="1" timestamp="2026-01-28T09:15:22"
          file="idea-backup-2026-01-28-091522.zip"
          description="Before module reorg" />
  <backup id="2" timestamp="2026-01-29T14:30:45"
          file="idea-backup-2026-01-29-143045.zip"
          description="After scope setup" />
</backups>
```

### ZIP Contents

```
idea-backup-*.zip
├── workspace.xml
├── modules.xml
├── misc.xml
├── vcs.xml
├── *.iml
└── ...
```

---

## Configuration

### Rolling Backup Count

Default: Keep last 10 backups

Configurable via `.claude/idea-tools.local.md`:
```yaml
---
backup_count: 10
backup_location: .backups/idea
---
```

### Exclusions

Files excluded from backup:
- `workspace.xml` cache sections
- `shelf/` (uncommitted changes)
- `usage.statistics.xml`
- `tasks.xml` (ephemeral)

---

## Failure Modes & Recovery

| Issue | Recovery |
|-------|----------|
| Backup corrupted | Use earlier backup |
| Restore failed | Safety backup exists at `.backups/idea/safety-{timestamp}.zip` |
| Disk full | Clean old backups: `rm .backups/idea/*.zip` |
| Permission denied | Check file ownership |

---

## Security & Permissions

- **Required tools:** Read, Write, Bash (zip/unzip)
- **Confirmations:** Before restore (destructive)
- **Safety:** Auto-creates safety backup before restore

---

## References

- [Backup Format](references/backup-format.md) - XML and ZIP specification

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 1.0.0
last_updated: "2026-01-31"
migrated_from: idea-automation v1.1.0
```

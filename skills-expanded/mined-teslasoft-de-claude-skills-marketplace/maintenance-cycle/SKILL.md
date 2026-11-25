---
name: maintenance-cycle
description: |
  Automated IDEA maintenance workflow: backup, sync, scope generation, verify, and report.
  Orchestrates idea-tools skills for comprehensive maintenance.
triggers:
  - /idea maintenance       # Run full maintenance cycle
  - /idea maintain          # Alias
negative_triggers:
  - /idea sync-modules      # Direct sync (use idea-tools:module-sync)
  - /idea backup            # Direct backup (use idea-tools:config-backup)
  - /idea onboard           # New project (use project-onboarding)
version: 1.0.0
author: Christian Kusmanow / Claude
last_updated: 2026-01-31
---

# Skill: IDEA Maintenance Cycle

Automated maintenance workflow that orchestrates idea-tools skills.

## When to Use

- Regular IDEA project maintenance
- After multiple structural changes
- Before/after major development phases
- Weekly/monthly maintenance routine

## When NOT to Use

- For single operations (use idea-tools skills directly)
- For new project setup (use `/idea onboard`)
- For quick sync only (use `/idea sync-modules`)

---

## Workflow Steps

### 1. Pre-Flight Check

```
[ ] Verify .idea directory exists
[ ] Check for uncommitted IDEA config changes
[ ] Validate current module structure
```

### 2. Safety Backup

Invoke `idea-tools:config-backup`:
```
/idea backup
```

Creates timestamped backup before any modifications.

### 3. Module Synchronization

Invoke `idea-tools:module-sync`:
```
/idea sync-modules
```

- Discover Git submodules
- Scan PARA folders
- Update modules.xml
- Create/update .iml files

### 4. Scope Generation

Create/update file scopes:
- Individual PARA category scopes
- Composite scopes (Active Work, Knowledge Base)
- Configuration scopes (Claude Config, Obsidian Config)

### 5. Verification

```
[ ] Modules load without errors
[ ] Scopes are accessible
[ ] VCS mappings correct
[ ] No orphaned .iml files
```

### 6. Status Report

Generate maintenance report:
```
IDEA Maintenance Report - 2026-01-31

Backup: idea_config_2026-01-31-xyz.zip
Modules: 12 synced (3 new, 0 removed)
Scopes: 15 updated
VCS Mappings: 8 configured

Status: SUCCESS
```

---

## Command Reference

### `/idea maintenance`

Full maintenance cycle with all steps.

**Options:**
- `--dry-run` - Preview changes without applying
- `--skip-backup` - Skip safety backup (not recommended)
- `--verbose` - Detailed output

**Example:**
```
/idea maintenance --verbose
```

---

## Orchestrated Skills

This skill orchestrates:

| Skill | Purpose |
|-------|---------|
| `idea-tools:config-backup` | Safety backup creation |
| `idea-tools:module-sync` | Module synchronization |

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Backup failed | Check disk space, permissions |
| Sync failed | Restore from backup: `/idea restore` |
| Scope error | Manual scope recreation in IDEA |
| Verification failed | Review report, fix issues manually |

---

## Best Practices

1. **Run weekly** - Keep IDEA config in sync with project changes
2. **Before major changes** - Always backup first
3. **Review reports** - Check for unexpected changes
4. **Keep backups** - Don't delete old backups prematurely

---

## Security & Permissions

- **Required tools:** Read, Write, Bash
- **Files modified:** `.idea/*`, `.backups/idea/*`
- **Confirmations:** None (backup protects against issues)

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 1.0.0
last_updated: "2026-01-31"
depends_on:
  - idea-tools:config-backup
  - idea-tools:module-sync
```

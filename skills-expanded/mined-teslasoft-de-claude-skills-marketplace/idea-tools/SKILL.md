---
name: idea-tools
description: |
  Advanced IntelliJ IDEA automation suite: changelist management with project/PARA
  organization, module synchronization with Git submodules, and rolling configuration
  backups. Integrates with collab skill for IDE context awareness.
  Keywords: idea, intellij, jetbrains, changelist, module-sync, backup, automation.
triggers:
  - /idea changelist
  - /idea changelist organize
  - /idea changelist create
  - /idea changelist generate
  - /idea changelist sync
  - /idea sync-modules
  - /idea sync
  - /idea create-scope
  - /idea backup
  - /idea restore
  - organize IDEA changelists
  - sync IDEA modules
  - backup IDEA config
negative_triggers:
  - /idea status         # Use mcp-tools skill
  - /idea vcs            # Use mcp-tools skill
  - /idea files          # Use mcp-tools skill
  - /idea scopes         # Use mcp-tools skill
version: 1.0.0
author: Christian Kusmanow / Claude
last_updated: 2026-01-31
---

# Skill: IDEA Tools Suite

Advanced automation capabilities for IntelliJ IDEA, extending the base MCP integration with project organization, module management, and configuration backup features.

## Overview

This skill aggregates three specialized IDEA automation capabilities:

| Capability | Triggers | Description |
|------------|----------|-------------|
| **Changelist Management** | `/idea changelist *` | Organize changelists by project/PARA |
| **Module Sync** | `/idea sync-modules`, `/idea sync` | Sync modules with Git submodules |
| **Config Backup** | `/idea backup`, `/idea restore` | Rolling config backups |

---

## Changelist Management

Organize VCS changelists by project ID (P1-P24) and PARA folder structure.

### Commands

```
/idea changelist              # Show current changelist status
/idea changelist organize     # Scan and organize files by project
/idea changelist create NAME  # Create new changelist
/idea changelist generate     # Generate commit messages
/idea changelist sync         # Export context to collab skill
```

### Features

- **Project detection**: Files mapped to P1-P24 by path patterns
- **PARA organization**: Files grouped by 00-90 folder structure
- **Conventional commits**: Pre-filled commit message templates
- **Collab integration**: Export changelist context for branch descriptions

### Changelist Naming Convention

```
{order}-{scope}-{description}
```

Examples:
- `1-vault-foundation` - Core config files
- `3-P19-skills` - Agent skills extraction
- `12-vault-para` - PARA structure files

---

## Module Sync

Synchronize IDEA modules with Git submodules and PARA folders.

### Commands

```
/idea sync-modules      # Full module synchronization
/idea sync              # Alias for sync-modules
/idea create-scope      # Generate scopes from modules
```

### Features

- **Submodule discovery**: Recursive `.gitmodules` parsing
- **PARA grouping**: Auto-groups by folder prefix (00-90)
- **Java-free view**: Uses EMPTY_MODULE type
- **Blacklist patterns**: Excludes node_modules, .git, etc.

### Module Groups

| Folder | IDEA Group |
|--------|------------|
| `00_Inbox/` | PARA/00 Inbox |
| `20_Projects/` | PARA/20 Projects |
| `40_Resources/` | PARA/40 Resources |

---

## Config Backup

Rolling backups of `.idea/` configuration.

### Commands

```
/idea backup          # Create timestamped backup
/idea restore         # List available backups
/idea restore [id]    # Restore specific backup
```

### Features

- **Rolling backups**: Keep last 10 by default
- **ZIP archives**: Timestamped `.backups/idea/` storage
- **Safety backup**: Auto-creates before restore
- **XML log**: Backup history in `backup-log.xml`

### Backup Structure

```
.backups/
└── idea/
    ├── backup-log.xml
    ├── idea-backup-2026-01-28-091522.zip
    └── idea-backup-2026-01-31-143022.zip
```

---

## Related Skills

This skill extends the base IDEA MCP integration:

| Skill | Purpose |
|-------|---------|
| `idea:mcp-tools` | Base MCP server integration (file ops, editor, VCS) |
| `idea:idea-tools` | This skill - advanced automation |

For base IDE operations (`/idea status`, `/idea vcs`, `/idea scopes`), use `mcp-tools`.

---

## Collab Integration

### Export Changelist Context

When `/idea changelist sync` runs:

1. Creates `.claude/CHANGELIST-CONTEXT.md`
2. Lists all changelists with file counts
3. Includes draft commit messages
4. Collab skill reads for branch context

### Import Context

Collab skill can:
- Understand current IDE work in progress
- Include changelist info in branch descriptions
- Track parallel work during agent execution

---

## Error Handling

| Issue | Recovery |
|-------|----------|
| workspace.xml corrupted | `/idea restore` from backup |
| Changelists not visible | Close/reopen Commit window (Alt+0) |
| Module conflicts | Delete module, re-sync |
| Backup corrupted | Use earlier backup ID |

---

## Security & Permissions

- **Required tools:** Read, Write, Bash
- **Files modified:** `.idea/workspace.xml`, `.idea/modules.xml`, `.backups/`
- **Confirmations:** Before restore, before overwriting changelists

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 1.0.0
last_updated: "2026-01-31"
imports:
  - idea-tools:changelist-mgmt
  - idea-tools:module-sync
  - idea-tools:config-backup
```

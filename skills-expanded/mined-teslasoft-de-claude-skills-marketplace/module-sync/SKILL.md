---
name: module-sync
description: |
  Synchronize IntelliJ IDEA modules with Git submodules and PARA folders.
  Discovers submodules recursively, filters by remote host (GitHub/GitLab),
  and configures Java-free view with auto-grouping.
triggers:
  - /idea sync-modules      # Full module synchronization
  - /idea sync              # Alias for sync-modules
  - /idea create-scope      # Generate ad-hoc scopes from modules
negative_triggers:
  - /idea backup            # Use config-backup skill
  - /idea changelist        # Use changelist-mgmt skill
version: 1.0.0
author: Christian Kusmanow / Claude
last_updated: 2026-01-31
---

# Skill: IDEA Module Sync

Synchronize IntelliJ IDEA project modules with Git submodules and PARA folder structure.

## When to Use

- After adding/removing Git submodules
- When PARA folder structure changes
- To create Java-free project view
- To generate scopes for file filtering

## When NOT to Use

- For backup/restore operations (use `/idea backup`)
- For changelist management (use `/idea changelist`)
- For simple file operations (use `/idea` base skill)

---

## Quick Start

1. **Sync modules:** `/idea sync-modules` - Discover and register modules
2. **Create scope:** `/idea create-scope` - Generate scopes from modules

---

## Capabilities

### 1. Dynamic Sync

Recursively discovers:
- Git submodules (`.gitmodules`)
- Top-level PARA folders (`\d{2}_` pattern)
- Nested module structures

### 2. Java-Free View

Prevents IDEA from misdetecting as Java project:
- Uses `EMPTY_MODULE` type
- Adds root exclusions
- Avoids nested content root errors

### 3. Auto-Grouping

Organizes modules in IDEA:
- Groups by PARA category (00-90)
- Groups by submodule hierarchy
- Custom group names from path

### 4. Blacklisting

Automatically ignores:
- `node_modules/`
- `.git/`
- `.smart-env/`
- `tmpclaude-*/`
- Other temp directories

---

## Commands

### `/idea sync-modules`

Full module synchronization workflow:

1. **Discover submodules:**
   ```bash
   git config --file .gitmodules --get-regexp path
   ```

2. **Scan PARA folders:**
   - Match `\d{2}_*` directories at project root
   - Register each as IDEA module

3. **Update modules.xml:**
   - Add new modules
   - Remove orphaned modules
   - Configure module groups

4. **Update workspace.xml:**
   - Set module groups
   - Configure root exclusions

### `/idea create-scope`

Generate file scopes from current module structure:

- Creates scope for each PARA folder
- Creates scope for each submodule path
- Adds composite scopes (e.g., "Active Work")

---

## Module XML Format

### modules.xml

```xml
<project version="4">
  <component name="ProjectModuleManager">
    <modules>
      <module
        fileurl="file://$PROJECT_DIR$/00_Inbox/00_Inbox.iml"
        filepath="$PROJECT_DIR$/00_Inbox/00_Inbox.iml"
        group="PARA/00 Inbox" />
    </modules>
  </component>
</project>
```

### Module .iml File

```xml
<?xml version="1.0" encoding="UTF-8"?>
<module type="EMPTY_MODULE" version="4">
  <component name="NewModuleRootManager">
    <content url="file://$MODULE_DIR$">
      <excludeFolder url="file://$MODULE_DIR$/node_modules" />
    </content>
  </component>
</module>
```

---

## PARA Module Groups

| Folder | Module Group |
|--------|--------------|
| `00_Inbox/` | PARA/00 Inbox |
| `00_Dashboard/` | PARA/00 Dashboard |
| `10_Goals/` | PARA/10 Goals |
| `20_Projects/` | PARA/20 Projects |
| `30_Areas/` | PARA/30 Areas |
| `40_Resources/` | PARA/40 Resources |
| `50_Collab/` | PARA/50 Collab |
| `60_Science/` | PARA/60 Science |
| `70_Skills/` | PARA/70 Skills |
| `90_Archive/` | PARA/90 Archive |

---

## Submodule Handling

### Discovery

Reads `.gitmodules` to find:
- Submodule paths
- Remote URLs (GitHub/GitLab filtering)

### Filtering

Optional filters by remote host:
- `github.com` - Only GitHub submodules
- `gitlab.com` - Only GitLab submodules
- `all` - All submodules (default)

### Registration

Each submodule becomes an IDEA module:
- Path: relative to project root
- Group: based on parent directory
- Type: `EMPTY_MODULE` (Java-free)

---

## Blacklist Patterns

Directories always excluded:

```
node_modules/
.git/
.smart-env/
.pnpm-store/
tmpclaude-*/
dist/
build/
.cache/
```

---

## Failure Modes & Recovery

| Issue | Recovery |
|-------|----------|
| modules.xml corrupted | Restore from backup: `/idea restore` |
| Orphaned .iml files | Manual deletion or re-sync |
| Module conflicts | Delete conflicting module, re-sync |
| Group not showing | Restart IDEA |

---

## Security & Permissions

- **Required tools:** Read, Write, Bash
- **Files modified:** `.idea/modules.xml`, `.idea/*.iml`
- **Confirmations:** Before removing existing modules

---

## References

- [Module XML Format](references/module-xml-format.md) - Full XML specification
- [Blacklist Patterns](references/blacklist-patterns.md) - Exclusion patterns

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 1.0.0
last_updated: "2026-01-31"
migrated_from: idea-automation v1.1.0
```

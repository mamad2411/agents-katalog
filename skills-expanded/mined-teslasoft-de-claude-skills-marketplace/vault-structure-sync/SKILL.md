---
name: vault-structure-sync
description: |
  PARA-specific IDEA synchronization for Obsidian vault projects.
  Scans PARA folders (00-90), registers as modules, creates category-based scopes.
triggers:
  - /idea vault-sync        # Full vault sync
  - /idea para-sync         # Alias
negative_triggers:
  - /idea maintenance       # Use maintenance-cycle
  - /idea onboard           # Use project-onboarding
  - /idea sync-modules      # Generic sync (use idea-tools:module-sync)
version: 1.0.0
author: Christian Kusmanow / Claude
last_updated: 2026-01-31
---

# Skill: Vault Structure Sync

PARA-specific synchronization for Obsidian vault projects in IDEA.

## When to Use

- Syncing Obsidian vault PARA structure to IDEA
- After adding/renaming PARA folders
- Setting up IDEA for vault management
- Creating vault-aware file scopes

## When NOT to Use

- For generic projects (use `/idea sync-modules`)
- For full project onboarding (use `/idea onboard`)
- For maintenance (use `/idea maintenance`)

---

## PARA Structure

The PARA system uses numbered folders:

| Folder | Purpose | IDEA Module Group |
|--------|---------|-------------------|
| `00_Inbox/` | Quick capture | 00_Inbox and Dashboard |
| `00_Dashboard/` | Central overview | 00_Inbox and Dashboard |
| `10_Goals/` | Quarterly objectives | 10_Goals |
| `20_Projects/` | Active execution | 20_Projects |
| `30_Areas/` | Responsibility domains | 30_Areas |
| `40_Resources/` | Reference materials | 40_Resources |
| `50_Collab/` | Partnerships | 50_Collab |
| `60_Science/` | Research | 60_Science |
| `70_Skills/` | Competencies | 70_Skills |
| `90_Archive/` | Completed items | 90_Archive |

---

## Workflow Steps

### 1. PARA Discovery

Scan vault root for PARA folders:
```
[ ] Find folders matching /^\d{2}_/
[ ] Validate folder structure
[ ] Check for .obsidian configuration
```

### 2. Module Registration

For each PARA folder:
- Create EMPTY_MODULE .iml file
- Add to modules.xml with PARA group
- Configure content root

### 3. Scope Generation

Create specialized scopes:

**Individual Scopes:**
- `00 Inbox` - Quick capture items
- `10 Goals` - Quarterly objectives
- `20 Projects` - Active work
- etc.

**Composite Scopes:**
- `Active Work` - Inbox + Goals + Projects
- `Knowledge Base` - Areas + Resources + Science + Skills
- `PARA Content` - All PARA folders
- `Archive` - Archived items only

**Configuration Scopes:**
- `Claude Config` - .claude folder
- `Obsidian Config` - .obsidian folder
- `Skills and Plugins` - .claude/skills + .claude/plugins
- `Infrastructure` - scripts, docs, coordination

### 4. VCS Mapping

Configure Git mappings for vault root and submodules.

---

## Command Reference

### `/idea vault-sync`

Full PARA-aware synchronization.

**Options:**
- `--dry-run` - Preview changes
- `--scopes-only` - Only update scopes
- `--modules-only` - Only update modules

**Example:**
```
/idea vault-sync --verbose
```

---

## Orchestrated Skills

| Skill | Purpose |
|-------|---------|
| `idea-tools:module-sync` | Core module synchronization |

---

## Generated Files

### Module Files

Each PARA folder gets an .iml file:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<module type="EMPTY_MODULE" version="4">
  <component name="NewModuleRootManager">
    <content url="file://$MODULE_DIR$">
      <sourceFolder url="file://$MODULE_DIR$" isTestSource="false" />
    </content>
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
</module>
```

### Scope Files

Located in `.idea/scopes/`:
```
.idea/scopes/
├── 00_Inbox.xml
├── 10_Goals.xml
├── 20_Projects.xml
├── ...
├── Active_Work.xml
├── Knowledge_Base.xml
├── PARA_Content.xml
├── Archive.xml
├── Claude_Config.xml
├── Obsidian_Config.xml
├── Skills_and_Plugins.xml
└── Infrastructure.xml
```

---

## Output

### Success Report

```
Vault Structure Sync Complete - 2026-01-31

PARA Folders: 10 discovered
Modules: 10 registered

Module Groups:
- 00_Inbox and Dashboard (2 modules)
- 10_Goals (1 module)
- 20_Projects (1 module)
- 30_Areas (1 module)
- 40_Resources (1 module)
- 50_Collab (1 module)
- 60_Science (1 module)
- 70_Skills (1 module)
- 90_Archive (1 module)

Scopes: 18 created
- 10 individual PARA scopes
- 8 composite scopes

VCS: Root + 0 submodule mappings
```

---

## Error Handling

| Error | Recovery |
|-------|----------|
| No PARA folders found | Verify vault structure |
| Invalid folder name | Must match /^\d{2}_/ pattern |
| Module conflict | Remove conflicting module, re-sync |
| Scope error | Delete .idea/scopes/, re-sync |

---

## Best Practices

1. **Run after structural changes** - Keep IDEA in sync with vault
2. **Use scopes** - Filter file views by PARA category
3. **Combine with maintenance** - Run `/idea maintenance` for full sync
4. **Check modules.xml** - Verify group assignments

---

## Security & Permissions

- **Required tools:** Read, Write, Bash
- **Files modified:** `.idea/modules.xml`, `.idea/scopes/*`, `*/*.iml`
- **Confirmations:** None (non-destructive)

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 1.0.0
last_updated: "2026-01-31"
depends_on:
  - idea-tools:module-sync
```

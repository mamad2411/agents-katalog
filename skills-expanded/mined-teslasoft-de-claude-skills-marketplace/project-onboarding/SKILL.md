---
name: project-onboarding
description: |
  New project IDEA setup workflow: discover structure, create modules,
  configure groups, create scopes, setup changelists, create backup.
triggers:
  - /idea onboard           # Full onboarding workflow
  - /idea setup             # Alias
  - /idea init              # Alias
negative_triggers:
  - /idea maintenance       # Use maintenance-cycle
  - /idea sync-modules      # Direct sync (use idea-tools:module-sync)
version: 1.0.0
author: Christian Kusmanow / Claude
last_updated: 2026-01-31
---

# Skill: IDEA Project Onboarding

Complete IDEA setup workflow for new projects.

## When to Use

- Setting up IDEA for a new project
- First-time IDEA configuration
- Importing existing project into IDEA
- Re-initializing IDEA configuration from scratch

## When NOT to Use

- For ongoing maintenance (use `/idea maintenance`)
- For quick sync (use `/idea sync-modules`)
- For vault-specific setup (use `/idea vault-sync`)

---

## Workflow Steps

### 1. Project Discovery

Analyze project structure:
```
[ ] Scan for Git submodules
[ ] Identify folder patterns (PARA, src, etc.)
[ ] Detect language/framework hints
[ ] Find existing .idea config (if any)
```

### 2. Module Planning

Plan module structure:
```
Project Root
├── Module: main-workspace (WEB_MODULE)
├── Module: submodule-a (EMPTY_MODULE)
├── Module: submodule-b (EMPTY_MODULE)
└── PARA Modules (if applicable)
```

### 3. Module Creation

Invoke `idea-tools:module-sync`:
- Create .iml files for each module
- Configure content roots
- Set up exclusions (node_modules, .git, etc.)

### 4. Group Configuration

Organize modules into groups:
- By project area (frontend, backend, shared)
- By PARA category (if Obsidian vault)
- By submodule hierarchy

### 5. Scope Creation

Generate file scopes:
- Per-module scopes
- Composite scopes (All Source, All Tests)
- Custom workflow scopes

### 6. Changelist Setup

Invoke `idea-tools:changelist-mgmt`:
- Create initial changelists
- Map to project areas if applicable

### 7. Initial Backup

Invoke `idea-tools:config-backup`:
- Create baseline backup
- Document initial configuration

---

## Command Reference

### `/idea onboard`

Full onboarding workflow.

**Options:**
- `--dry-run` - Preview without creating files
- `--minimal` - Skip optional steps (changelists, advanced scopes)
- `--verbose` - Detailed output

**Example:**
```
/idea onboard --verbose
```

### `/idea onboard --type vault`

Vault-specific onboarding (shortcut to `/idea vault-sync` + extras).

---

## Interactive Steps

The onboarding process may ask:

1. **Module type preference:**
   - Empty modules (Java-free view)
   - Web modules (for web projects)
   - Mixed (auto-detect)

2. **Group organization:**
   - By folder structure
   - By PARA category
   - Custom grouping

3. **Scope templates:**
   - Standard development scopes
   - PARA-specific scopes
   - Custom scope patterns

---

## Orchestrated Skills

| Skill | Purpose |
|-------|---------|
| `idea-tools:module-sync` | Create/configure modules |
| `idea-tools:config-backup` | Baseline backup |
| `idea-tools:changelist-mgmt` | Changelist setup |

---

## Output

### Success Report

```
IDEA Onboarding Complete - 2026-01-31

Project: My New Project
Location: /path/to/project

Modules Created: 8
- main-workspace (WEB_MODULE)
- submodule-a (EMPTY_MODULE)
- submodule-b (EMPTY_MODULE)
- 00_Inbox (EMPTY_MODULE)
- 10_Goals (EMPTY_MODULE)
- 20_Projects (EMPTY_MODULE)
- 30_Areas (EMPTY_MODULE)
- 40_Resources (EMPTY_MODULE)

Groups: 3 (PARA, Submodules, Root)
Scopes: 12 created
Changelists: 2 configured
Backup: idea_config_2026-01-31-init.zip

Next Steps:
1. Open project in IDEA
2. Review module structure in Project view
3. Test scopes in Find dialog
```

---

## Error Handling

| Error | Recovery |
|-------|----------|
| .idea exists | Backup existing, proceed or abort |
| Permission denied | Check folder permissions |
| Invalid project structure | Manual module configuration |
| Submodule not initialized | Run `git submodule update --init` |

---

## Best Practices

1. **Start fresh** - Remove old .idea if re-onboarding
2. **Review modules** - Verify structure before committing
3. **Test scopes** - Ensure scopes work as expected
4. **Keep backup** - Preserve initial configuration

---

## Security & Permissions

- **Required tools:** Read, Write, Bash
- **Files modified:** `.idea/*`, project `.iml` files
- **Confirmations:** Before overwriting existing config

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 1.0.0
last_updated: "2026-01-31"
depends_on:
  - idea-tools:module-sync
  - idea-tools:config-backup
  - idea-tools:changelist-mgmt
```

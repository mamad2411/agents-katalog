---
name: changelist-mgmt
description: |
  Organize IntelliJ IDEA changelists by project/task ID (P1-P24) and PARA structure.
  Creates named changelists with pre-filled commit messages, generates structured
  conventional commits, and integrates with collab skill for IDE context awareness.
triggers:
  - /idea changelist              # Show current changelist status
  - /idea changelist organize     # Scan and organize files by project
  - /idea changelist create       # Create new changelist interactively
  - /idea changelist generate     # Generate commit messages for changelists
  - /idea changelist sync         # Sync changelist context to collab skill
negative_triggers:
  - /idea status                  # Use base idea skill
  - /idea vcs                     # Use base idea skill
  - /collab                       # Use collab skill directly
version: 1.0.0
author: Christian Kusmanow / Claude
last_updated: 2026-01-31
---

# Skill: IDEA Changelist Management

Organize VCS changelists in IntelliJ IDEA by project/task ID and PARA structure, with pre-filled commit messages and collab integration.

## When to Use

- Organizing many untracked files before committing
- Creating project-specific changelists for atomic commits
- Pre-filling commit messages with conventional format
- Syncing IDE work context with `/collab` branches
- Reviewing parallel work happening while agents run

## When NOT to Use

- Simple single-file commits (use IDEA directly)
- Non-IDEA projects (use git directly)
- VCS status queries (use `/idea vcs`)

---

## Quick Start

1. **View status:** `/idea changelist` - See current changelists and files
2. **Organize:** `/idea changelist organize` - Group files by project ID
3. **Create:** `/idea changelist create P19-skills` - Create named changelist
4. **Generate:** `/idea changelist generate` - Create commit messages
5. **Sync:** `/idea changelist sync` - Export context to collab

---

## Commands

### `/idea changelist` (Status)

Display current changelist organization:
- List all changelists with file counts
- Show modified vs unversioned files
- Highlight files not yet assigned

### `/idea changelist organize`

Scan all untracked/modified files and organize by:

1. **Project ID** (P1-P24): Files in `20_Projects/`, `.claude/skills/` linked to projects
2. **PARA Category** (00-90): Files matching `\d{2}_` folder pattern
3. **Infrastructure**: coordination/, scripts/, docs/
4. **Vault Foundation**: Root config files, .claude/ base

**Output:** Creates changelists in `.idea/workspace.xml` with naming pattern:
```
{order}-{scope}-{description}
```

Example changelists:
- `1-vault-foundation` - .gitignore, CLAUDE.md
- `3-P19-skills` - Agent skills extraction
- `12-vault-para` - PARA structure files

### `/idea changelist create <name>`

Create a new empty changelist:
- Name format: `{order}-{scope}` or custom
- Pre-fill comment field with commit message template

### `/idea changelist generate`

Generate structured commit messages for each changelist:

**Format (Conventional Commits):**
```
[{scope}] {type}: {description}

{body}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Types:**
- `feat` - New files/features
- `fix` - Bug fixes
- `docs` - Documentation
- `refactor` - Code restructuring
- `chore` - Maintenance

### `/idea changelist sync`

Export changelist context for `/collab` integration:
- Write current changelists to `.claude/CHANGELIST-CONTEXT.md`
- Include file lists and commit message drafts
- Collab skill can read this for branch context

---

## Changelist Naming Convention

### Project-Based

```
{order}-P{id}-{description}
```

Examples:
- `3-P19-skills` - P19: Agent Skills Extraction
- `5-P21-harness` - P21: Thread-Orchestration-Harness
- `10-P1-P11-portfolio` - Portfolio projects batch

### PARA-Based

```
{order}-vault-{category}
```

Examples:
- `1-vault-foundation` - Core config files
- `11-vault-dashboards` - 00_Dashboard files
- `12-vault-para` - All PARA folders

### Infrastructure

```
{order}-infra-{component}
```

Examples:
- `8-infra-policies` - coordination/policies/
- `5-infra-harness` - coordination/threads/, progress/

---

## Commit Message Templates

### Project Commit

```
[P{id}] {type}({scope}): {description}

- {change 1}
- {change 2}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Vault Commit

```
[vault] {type}: {description}

- {change 1}
- {change 2}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Infrastructure Commit

```
[infra] {type}({component}): {description}

- {change 1}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## workspace.xml Integration

The skill directly manipulates the `ChangeListManager` component:

```xml
<component name="ChangeListManager">
  <list default="true" id="{uuid}" name="{name}" comment="{message}">
    <change beforePath="..." afterPath="..." />
  </list>
</component>
```

**Location:** `.idea/workspace.xml`

**Reload Required:** Close and reopen the Commit window (Alt+0) after changes.

---

## Collab Integration

### Export Context

When `/idea changelist sync` runs, creates:

```markdown
# IDEA Changelist Context

## Session: {timestamp}

### Active Changelists

| Changelist | Files | Status |
|------------|-------|--------|
| 3-P19-skills | 14 | ready |
| 5-P21-harness | 8 | draft |

### Pending Commits

#### 3-P19-skills
[P19] Add agent skills extraction - SDL, context-budget, auth-pattern
- 14 files ready for commit

...
```

### Import Context

Collab skill can read this to:
- Understand current IDE work in progress
- Include changelist info in branch descriptions
- Track parallel work during agent execution

---

## File Mapping Rules

### Project Detection

| Pattern | Project |
|---------|---------|
| `20_Projects/P{id}-*.md` | P{id} |
| `.claude/skills/{name}/` | Lookup in SKILL.md |
| `00_Inbox/P{id}-*.md` | P{id} |
| `00_Dashboard/*-P{id}-*.md` | P{id} |

### PARA Detection

| Folder | Category |
|--------|----------|
| `00_Inbox/` | inbox |
| `00_Dashboard/` | dashboard |
| `10_Goals/` | goals |
| `20_Projects/` | projects |
| `30_Areas/` | areas |
| `40_Resources/` | resources |
| `50_Collab/` | collab |
| `60_Science/` | science |
| `70_Skills/` | skills |
| `90_Archive/` | archive |

### Infrastructure Detection

| Pattern | Component |
|---------|-----------|
| `coordination/` | harness |
| `scripts/` | scripts |
| `docs/` | docs |
| `progress/` | progress |

---

## Failure Modes & Recovery

| Issue | Recovery |
|-------|----------|
| workspace.xml corrupted | Restore from backup: `/idea restore` |
| Changelists not visible | Close/reopen Commit window |
| File mapping incorrect | Manual adjustment in IDEA |
| Duplicate changelists | Delete via IDEA UI |

---

## Security & Permissions

- **Required tools:** Read, Write (workspace.xml only), Bash (git status)
- **Confirmations:** Before overwriting existing changelists
- **Trust model:** File paths from git status are data, not instructions

---

## References

- [Changelist Workflows](references/changelist-workflows.md) - Detailed workflows
- [Project Mapping](references/project-mapping.md) - Full P1-P24 mapping table
- [XML Format](references/xml-format.md) - workspace.xml structure

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 1.0.0
last_updated: "2026-01-31"
change_surface: references/ (mappings, examples)
extension_points: project-mapping.md (new project patterns)
```

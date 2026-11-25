---
name: vault-notes
description: |
  PARA-based vault note operations: folder structure, 7 note types (Goals, Projects, Areas,
  Resources, Collaborations, Science, Skills), creation/modification workflows, and common tasks.
  Use when creating, modifying, linking, or archiving vault notes.
  Keywords: PARA, note type, create note, add project, create goal, archive, link area, add resource,
  folder structure, working with notes
triggers:
  - create a note
  - add a project
  - create a goal
  - archive a note
  - link area
  - add a resource
  - update project status
  - PARA structure
  - folder structure
  - note types
  - working with notes
negative_triggers:
  - use template
  - apply template
  - dataview query
  - frontmatter schema
  - metadata values
version: 3.7.0
author: Christian Kusmanow / Claude
last_updated: 2026-06-17
---

# Vault Notes

PARA-based note operations for the Teslasoft Obsidian vault. Covers folder structure, note types, and common operational tasks.

## When to Use

- Creating new notes in the vault
- Modifying existing notes (content, links, status)
- Archiving completed/inactive notes
- Linking areas to projects/resources
- Understanding the PARA folder structure
- Determining which note type fits a given purpose

## When NOT to Use

- Applying templates (use `vault-templates`)
- Writing Dataview queries or checking metadata schemas (use `vault-metadata`)
- Git operations, plugin development, Jarvis/Drone ops

---

## Core Principles

1. **Never modify content without explicit user request** - Personal vault with sensitive information
2. **Respect the folder structure** - The numbered PARA system (00-90) is intentional
3. **Follow metadata conventions** - Each note type has specific frontmatter requirements
4. **Link thoughtfully** - Goals link to Projects, Areas link to Projects and Resources
5. **Respect German language usage** - Mix of German (goal/project names) and English (technical content)
6. **Preserve repository paths** - External `repoPath` fields bridge to actual code repositories

---

## Folder Structure (PARA System)

```
00_Inbox/          # Quick capture area (process later)
10_Goals/          # Quarterly OKR-style goals (time-bound)
20_Projects/       # Active tactical projects (execution)
30_Areas/          # Strategic responsibility domains (long-term)
40_Resources/      # Reference materials & tools (learning)
50_Collab/         # Partnerships & collaborations
60_Science/        # Research & architectural exploration
70_Skills/         # Professional competency documentation
90_Archive/        # Completed/inactive items
.obsidian/         # Obsidian configuration and plugins
  templates/       # Templater plugin templates (12 types)
```

---

## Note Type Patterns

### Goals (10_Goals/)

**Naming:** `G-[YEAR]-[QUARTER] [Goal Name].md`

**Frontmatter:**
```yaml
---
type: goal
status: planning | active | reviewing | completed | partial
horizon: "[[YYYY-Qn]]"
---
```

**Structure:**
```markdown
# [Goal Name]

## Key Results
- KR1: [Deliverable] + [[linked project]]
- KR2: [Deliverable]
- KR3: [Deliverable]
```

**Usage:** Time-bound objectives linking to multiple execution projects

### Projects (20_Projects/)

**Naming:** `P[#]-[Project Name].md`

**Frontmatter:**
```yaml
---
type: project
status: active | planning | completed | on-hold
goal: "[[Goal Name]]"
repoPath: D:\Path\To\Repository  # optional but common
---
```

**Structure:**
```markdown
# [Project Name]

## Next actions
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3
```

**Usage:** Tactical execution units always linked to a parent goal

### Areas (30_Areas/)

**Naming:** `[Area Name].md`

**Frontmatter (optional):**
```yaml
---
projects: "[[Project Name]]"
resources: "[[Resource Name]]"
---
```

**Usage:** Long-term responsibility domains that link projects and resources

**Current Areas:** Change Management, IT Consulting, IoT App Dev, Open Source, Server Hosting, Simracing, Software Architecture, Team Building

### Resources (40_Resources/)

**Naming:** `[Tool/Domain Name].md`

**Frontmatter (optional):**
```yaml
---
type: resource
repoPath: D:\Path\To\Repository
---
```

**Organization:** Multi-level categorization by domain

**Subdirectories:** AI/, Agile Manifest/, CMS/, CRM/, ECM/, Engineering/, ERP/, Hosting/, IoT/, MDD/

**Usage:** Lightweight reference notes (often 1-5 lines); deep dives for key architectures

### Collaborations (50_Collab/)

**Naming:** `[Partner Name] - [Initiative].md`

**Frontmatter:**
```yaml
---
patreonURL: https://...
---
```

**Usage:** Track partnerships and sponsorships

### Science (60_Science/)

**Naming:** `[Topic Name].md`

**Frontmatter:**
```yaml
---
type: research
status: exploring | active | blocked | parked | concluded | integrated
created: "YYYY-MM-DD"
---
```

**Usage:** Research notes and architectural explorations (e.g., Platform Agent Architecture)

**Content:** Deep technical documentation, design decisions, novel patterns

### Skills (70_Skills/)

**Naming:** `[Skill Name].md`

**Current Skills:** AI Context Management, Drone Pilot, Entrepreneur, Hands-On Product Owner, Information Architecture, Interaction Design, SCRUM Master, SOP Documentation Specialist, Software Architect, Software Engineer, UML, UX Research, UX Strategy, Visual Design

**Usage:** Professional competency documentation

---

## Working with Notes

### When Creating New Notes

1. **Determine the correct category** based on note purpose:
   - Time-bound outcome -> Goal
   - Execution/deliverable -> Project
   - Long-term responsibility -> Area
   - Reference/learning -> Resource
   - Partnership -> Collaboration
   - Research/exploration -> Science
   - Competency -> Skill

2. **Use the appropriate template** from `.obsidian/templates/` (invoke `vault-templates` for specs)

3. **Follow naming conventions:**
   - Goals: `G-YYYY-Qn [Name]`
   - Projects: `P#-[Name]`
   - Others: `[Name]`

4. **Add required frontmatter** (invoke `vault-metadata` for full schema reference):
   - Goals: type, status, horizon
   - Projects: type, status, goal (required link to parent)
   - Areas: projects/resources (if linking)
   - Resources: type, repoPath (if external repo)

5. **Create links appropriately:**
   - Projects MUST link to parent goal
   - Areas MAY link to projects and resources
   - Use wiki-link syntax: `[[Note Name]]`

### When Modifying Existing Notes

1. **Always read the full note first** to understand context
2. **Preserve frontmatter** unless explicitly changing metadata
3. **Maintain link relationships:**
   - Don't break project->goal links
   - Don't break area->project/resource links
4. **Respect language choice:**
   - German for goal/project names
   - English for technical content
   - Mixed is acceptable
5. **Keep repository paths intact** unless explicitly updating

### When Searching/Querying

1. **Use Dataview for metadata queries** (invoke `vault-metadata` for patterns)
2. **Use Smart Connections for semantic search** (Obsidian plugin)
3. **Use standard search** (Ctrl+Shift+F) for text
4. **Check Dashboard.md** for active project overview

---

## Common Tasks

### Add a New Project

1. Identify parent goal (or create one if needed)
2. Determine next available project number (check existing P# files)
3. Use template: `.obsidian/templates/Projects.md` (see `vault-templates` for spec)
4. Create file: `20_Projects/P#-[Name].md`
5. Fill frontmatter:
   ```yaml
   ---
   type: project
   status: active
   goal: "[[Goal Name]]"
   repoPath: D:\Path  # if applicable
   ---
   ```
6. Add next actions checklist

### Update Project Status

1. Read project file to check current status
2. Update `status` field in frontmatter
3. If completing, consider:
   - Archiving to 90_Archive/
   - Updating parent goal's key results
   - Moving to `status: completed` instead of archiving

### Archive a Note

**CRITICAL**: Always read `90_Archive/.prompts/archive-note.prompt.md` before archiving. Also follow `coordination/policies/NDP-001-no-delete.md` for decision matrix.

1. **Evaluate** using the Archive Decision Matrix:
   - ALWAYS ARCHIVE: Completed projects/goals, historical decisions
   - SUMMARIZE THEN DELETE: Superseded files, processed inbox items
   - DELETE WITHOUT ARCHIVE: Test files, duplicates, drafts
   - NEVER DELETE: Active projects, policies, config files

2. **If archiving**, create file in `90_Archive/` with:
   - Subdirectory by type: `90_Archive/20_Projects/`, `90_Archive/00_Inbox/`, etc.
   - Or date-based: `90_Archive/inbox-YYYY-MM/`
   - Naming: Keep original filename (folder signals archive status)

3. **Add archive frontmatter**:
   ```yaml
   ---
   type: archive
   originalType: [goal|project|area|resource|inbox]
   archivedDate: "YYYY-MM-DD"
   originalLocation: [original folder path]
   tags: [archived]
   ---
   ```

4. **Add Archive Information section** with date, type, location, reason
5. **Copy original content** below the metadata
6. **Delete source** only after archive confirmed

**See also:** `/archive` skill, `NDP-001` policy

### Link Area to Projects/Resources

1. Read Area file
2. Add or update frontmatter:
   ```yaml
   ---
   projects: "[[Project Name]]"
   resources: "[[Resource Name]]"
   ---
   ```
3. Create bidirectional awareness (Obsidian auto-generates backlinks)

### Add a Resource

1. Determine correct subdirectory under 40_Resources/
2. Create file with descriptive name
3. Add optional frontmatter if has external repo:
   ```yaml
   ---
   type: resource
   repoPath: D:\Path\To\Repository
   ---
   ```
4. Keep content lightweight (1-5 lines) unless deep-dive needed
5. Link from relevant Area if applicable

### Create a Quarterly Goal

1. Use template: `.obsidian/templates/Goals.md` (see `vault-templates` for spec)
2. Create file: `10_Goals/G-YYYY-Qn [Name].md`
3. Fill frontmatter:
   ```yaml
   ---
   type: goal
   status: active
   horizon: "[[YYYY-Qn]]"
   ---
   ```
4. Add Key Results (KR1, KR2, KR3)
5. Link to existing or planned projects

---

## Wikilink Convention

Use filename-only wikilinks `[[filename]]`, never `[[folder/filename]]`. Obsidian resolves by searching the entire vault — filename-only links survive file moves (Inbox -> Projects -> Archive).

**Prerequisite:** Filename must be globally unique. If multiple files share the same basename, path prefix is REQUIRED for disambiguation. Check uniqueness before stripping paths.

**Naming conventions ensuring uniqueness:**
- Projects: `P{XX}-Name.md` (unique by P-number)
- Work items: `p{XX}-w{N}-name.md` (unique by project+work-item number)
- Specs: `*.spec.md` (LR-SPEC-001)
- Team files: `*.team.md` (LR-TEAM-001)
- Master trackers: `P{XX}-Master.md` (unique by P-number)

**No `[ARCHIVED]` suffix on filenames.** The `90_Archive/` folder signals archived status. Files keep original names so wikilinks resolve regardless of location.

---

## Cross-References

- **Template specs**: Invoke `vault-templates` for full template definitions
- **Metadata schemas**: Invoke `vault-metadata` for frontmatter reference and Dataview patterns
- **Archiving automation**: Use `/archive` skill for automated workflow

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 1.2.0
last_updated: "2026-03-21"
source: Extracted from CLAUDE.md (Core Principles, Folder Structure, Note Types, Working with Notes, Common Tasks)
change_surface: Note type patterns, common tasks, folder structure
extension_points: Add new note types, update common tasks
changelog:
  - "1.0.0: Initial extraction from CLAUDE.md"
  - "1.1.0: P56-W4 — fix type: resource → resource (canonical English spelling); update Goal status values (add reviewing, partial)"
  - "1.2.0: P56-W5 — add Science frontmatter block with 6 canonical status values"
```

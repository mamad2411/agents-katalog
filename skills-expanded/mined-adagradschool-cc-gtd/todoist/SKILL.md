---
name: todoist
description: Bidirectionally sync Todoist with the GTD system via the official Todoist MCP server — map GTD projects/contexts/priorities/due dates to Todoist projects/labels/priorities/dates, process the Todoist Inbox into project tasks.md files, and reflect Todoist completions back into GTD. Use when syncing tasks, processing the inbox, or before /daily and /weekly. Never creates duplicates or auto-completes tasks.
allowed-tools: mcp__todoist__find-projects, mcp__todoist__find-tasks, mcp__todoist__add-tasks, mcp__todoist__update-tasks, mcp__todoist__add-projects, mcp__todoist__get-overview, mcp__todoist__complete-tasks
---

# /todoist

Sync Todoist with the GTD system using AI-powered processing via the **official Todoist MCP server**.

> Requires the Todoist MCP server connected to this session (tools named `mcp__*_todoist_*` / `mcp__todoist__*`). No `tod` CLI needed. If the server isn't connected yet, connect it before running this skill.

DO NOT CREATE DUPLICATE PROJECTS/TASKS IN Todoist.
DO NOT CLOSE ANY TASKS/PROJECTS automatically — I'll mark things as completed in Todoist and they should be reflected in the GTD system.

## Mapping
**`projects.md` holds the authoritative GTD ↔ Todoist Sync Map** (folder ↔ project/section
+ IDs). Read it first and sync against those exact IDs. When a project/section is added,
renamed, or removed on either side, update the Sync Map in `projects.md` in the same pass.

- **GTD folder** → Todoist **project** (or a **section** within a shared project — e.g.
  `side-projects/` and `social/` map to sections, per the Sync Map)
- **GTD context** (`@work-code`, `@errands`, …) → Todoist **label** (native — no title prefix)
- **GTD priority** → Todoist **priority** (p1–p4)
- **GTD due date** → Todoist **due** date
- Todoist Free plan: 6-project cap — prefer adding **sections**, not new projects.

## Process

When this skill is run, perform the following bidirectional sync between Todoist and the GTD system:

### 1. Get Active GTD Projects
- Read all active GTD projects from `projects/active/*/info.md` files
- For each project directory, extract the project name from the directory name or info.md

### 2. Bidirectional Project Sync
For each active GTD project:

**Step A: Read Local Context**
- Read `projects/active/[project]/info.md` to understand project goals and context
- Read `projects/active/[project]/tasks.md` to get current GTD tasks organized by context
- Parse tasks into list format: `[task content, context, completed_status]`

**Step B: Read Todoist Context**
- List the Todoist tasks in the matching project (find the project by name; create it if it does not exist)
- Parse Todoist tasks into comparable format: `[task content, labels, completed_status, due, priority]`

**Step C: Compare and Sync**
- **Tasks in GTD but not in Todoist**: Create in the matching Todoist project with the `@context` label (and a due date / priority if the GTD task has one)
- **Tasks in Todoist but not in GTD**: Add to the appropriate context section in `tasks.md` using format `- [ ] [task content]`
- **Completed tasks in Todoist**: Mark as completed in GTD by changing `- [ ]` to `- [x]` in `tasks.md` and log completion in `info.md` task history

### 3. Process Inbox
- List tasks in the Todoist `Inbox` project
- For each inbox task, determine:
  - Which GTD project it belongs to (if any)
  - Appropriate context (@work-code, @work-errand, @home-computer, @home-calls, @sideprojects-code, @sideprojects-errand, @errands)
- Add to the appropriate project's `tasks.md` file
- Move/create the corresponding task in the proper Todoist project with the context label

### 4. Someday/Maybe Sync
- Read `someday-maybe.md`
- Compare with the Todoist `Someday/Maybe` project
- Sync bidirectionally following the same diff logic as active projects

### 5. Task Format Standards
**GTD Format**: `- [ ] [task content]` (incomplete) or `- [x] [task content]` (completed)
**Todoist Creation**: create a task in project `[Project Name]` with content `[Task]`, label `@context`, optional priority, and optional due date

## AI Guidelines

**Duplicate Prevention:**
- Before creating any task, verify it doesn't already exist in the target system
- Compare task content semantically, not just exact string matches
- Skip creation if task already exists

**Context Mapping:**
- Map GTD contexts to Todoist labels consistently
- Available contexts: @work-code, @work-errand, @home-computer, @home-calls, @sideprojects-code, @sideprojects-errand, @errands
- Default to @home-computer if context is unclear

**Completion Handling:**
- Only mark tasks completed in GTD when they are completed in Todoist
- Never complete tasks in Todoist automatically
- Log completions in the project's info.md task history section

**Conservative Approach:**
- When in doubt about project assignment, ask for clarification rather than guessing
- Preserve existing organization rather than reorganizing
- Focus on sync accuracy over automation

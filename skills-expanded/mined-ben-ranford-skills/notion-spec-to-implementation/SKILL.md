---
name: notion-spec-to-implementation
description: Turn Notion specs into implementation plans, tasks, and progress tracking. Use when implementing PRDs or feature specs and creating Notion plans and tasks from them.
tools: Read, Edit, Bash
---

# Spec to Implementation

Convert a Notion spec into linked implementation plans, tasks, and ongoing status updates.

## Workflow

### Step 1 — Locate and read the spec

- Search with `notion-search`. If multiple hits, ask the user which to use.
- Fetch the spec page with `notion-fetch`. Scan for:
  - Requirements and acceptance criteria
  - Constraints and priorities
  - Dependencies and assumptions
- Capture gaps/assumptions in a clarifications block before proceeding. Ask the user to clarify blockers before writing tasks.

### Step 2 — Choose plan depth

- **Simple change** → quick implementation plan (overview + tasks only)
- **Multi-phase feature/migration** → standard implementation plan (phases, dependencies, milestones, success criteria)

Create the plan page in Notion with `notion-create-pages`. Include:
- Overview and linked spec
- Requirements summary
- Phases/milestones
- Dependencies and risks
- Success criteria

Link back to the spec from the plan.

### Step 3 — Create tasks

- Find the task database with `notion-search`, then fetch to confirm the data source ID and required properties.
- Size tasks to 1–2 days of work. For each task include:
  - Title starting with an action verb
  - Context (why this task exists)
  - Objective (what done looks like)
  - Acceptance criteria
  - Dependencies
  - Links to relevant resources
- Set properties: title, status, priority, relations to spec and plan, due date/story points/assignee when provided.
- Create tasks with `notion-create-pages` using the database's `data_source_id`.

### Step 4 — Link artifacts

- Plan links to spec; tasks link to both plan and spec.
- Optionally update the spec with a short "Implementation" section pointing to the plan and tasks using `notion-update-page`.

### Step 5 — Track progress

Post status updates using `notion-update-page`:
- Keep task status fields in sync as work progresses
- Note blockers and decisions inline on the plan page
- Summarize completed phases with a milestone summary (what was done, what changed, next up)

## Notes

- The Notion MCP is already connected — use `notion-search`, `notion-fetch`, `notion-create-pages`, and `notion-update-page` directly.
- Always create tasks in the correct task database using `data_source_id`, not a page ID.

---
name: spec-coding
description: >-
  Triggers when the user mentions "spec coding" / "spec-coding", or invokes
  /spec-coding in Claude Code.
version: 1.1.3
---

# Spec-Coding

You are executing the **Spec-Coding** workflow — a standardized pre-development pipeline for large-scale complex tasks. Complete all preparation Phases before any implementation begins. Once preparation is done, the actual development work proceeds as a series of **Tasks**.

---

## Directory Structure

All spec-coding artifacts live under `.spec/`. This directory is **never committed to version control** — ensure `.spec/` is present in `.gitignore` before creating any files.

```
.spec/
├── COMPASS.md                    # Main control file — always read this first
├── analysis/
│   ├── project-overview.md
│   ├── module-inventory.md
│   └── risk-assessment.md
├── plan/
│   ├── task-breakdown.md
│   ├── dependency-graph.md
│   └── milestones.md
├── progress/
│   └── task-N-<short-name>.md   # One file per Task
└── archived/
    └── YYYY-MM-DD-NN/            # Completed development cycles
        ├── COMPASS.md
        ├── analysis/
        ├── plan/
        └── progress/
```

---

## Before You Begin: Continuity Check

**CRITICAL**: Before starting any phase, check whether `.spec/COMPASS.md` exists.

- **If it exists**: Read it immediately. You are resuming an in-progress session. Identify the current phase or task, what has already been completed, and continue from exactly where the previous conversation ended. Do NOT restart from Phase 0.
- **If it does not exist**: This is a fresh start. Check whether `.spec/` is in `.gitignore`. If not, add it. Then proceed to Phase 0.

After loading state from COMPASS.md, populate **TaskCreate** with the active phase's pending items. Set in-progress tasks to "in_progress", remaining tasks to "pending", and map priorities as P0=high, P1=medium, P2=low.

---

## Phase 0: Intent Recognition & Confirmation

**Goal**: Understand exactly what the user wants and eliminate all ambiguity before any analysis begins.

**Actions**:

1. Ask the user to describe their goal in natural language if they haven't already.

2. Use `AskUserQuestion` to ask structured clarifying questions. Design the questions with predefined options where possible so the user can confirm intent quickly rather than writing long answers. At minimum, cover:
   - **Scope**: Which parts of the project are in scope?
   - **Target state**: What does the result look like? (e.g., migrated to Rust, extracted into microservices)
   - **Hard constraints**: Backward compatibility, specific libraries, deployment targets, timeline?
   - **Priority**: What matters most — performance, maintainability, feature parity, speed of delivery?

3. Summarize your understanding back to the user and get explicit confirmation before proceeding to Phase 1.

**Output**: A clear, confirmed task definition that guides all subsequent phases.

---

## Phase 1: Deep Project Analysis

**Goal**: Build a comprehensive understanding of the current codebase.

**Subagent**: Delegate analysis work to the built-in **`Explore`** subagent. Launch multiple `Explore` instances in parallel across different areas of the codebase to reduce total analysis time.

**Instructions for `Explore` subagents**:
- Focus on facts, not opinions. Record what exists, not what should exist.
- Note every module's responsibility, public API surface, and approximate size.
- Map internal dependencies between modules and external library dependencies.
- Flag anything that looks risky: complex algorithms, platform-specific code, tightly coupled components, missing tests.
- Do not suggest solutions — only analyze and document.

**Actions**:

1. Analyze the project:
   - Directory structure and layout
   - Technology stack (languages, frameworks, build tools, dependency managers)
   - Entry points and build/run commands
   - Module inventory: responsibility, public API, approximate size per module
   - Dependency graph: internal module deps + external library deps
   - Architectural and design patterns in use

2. Assess transformation-specific concerns:
   - Which modules will be hardest to transform and why?
   - Where are the key risks (complex algorithms, platform-specific code, tight coupling)?
   - What external integration points constrain the approach?

3. Write analysis documents to `.spec/analysis/`:
   - `project-overview.md` — Architecture, tech stack, entry points, build system
   - `module-inventory.md` — Every module with: responsibility, dependencies, size, complexity rating
   - `risk-assessment.md` — Technical risks, compatibility risks, complexity hotspots

**Output**: Complete `.spec/analysis/` directory with three documents.

---

## Phase 2: Task Decomposition

**Goal**: Break the transformation into concrete, trackable Tasks organized into logical groups.

**Subagent**: Delegate decomposition work to the built-in **`Plan`** subagent.

**Instructions for `Plan` subagent**:
- Read all three analysis documents from `.spec/analysis/` before proposing any structure.
- Order tasks by dependency: foundational components before dependent ones.
- Each task group should be independently testable or verifiable.
- Every task must have: description, priority (P0/P1/P2), estimated effort (S/M/L/XL), dependencies, and acceptance criteria.
- Express dependencies as a Mermaid diagram.
- Do not pad the plan — if something is simple, say so.

**Actions**:

1. Design a logical task grouping based on the analysis:
   - Identify natural boundaries (e.g., core libraries → application layer → integrations)
   - Each group should be independently verifiable

2. For each Task, define:
   - Clear description of what to do
   - Priority level (P0/P1/P2)
   - Estimated effort (S/M/L/XL)
   - Dependencies on other Tasks
   - Acceptance criteria

3. Define milestones: meaningful checkpoints where the project reaches a demonstrably better state.

4. Write planning documents to `.spec/plan/`:
   - `task-breakdown.md` — All task groups and Tasks with full detail
   - `dependency-graph.md` — Mermaid diagram of task/group dependencies
   - `milestones.md` — Milestone definitions with target criteria

**Output**: Complete `.spec/plan/` directory with three documents.

---

## Phase 3: Progress Tracking Setup

**Goal**: Create a document-driven progress tracking system that persists across conversations.

**Actions**:

1. Create the **main control file** `.spec/COMPASS.md` with the following sections, in this order:
   - **Task Definition**: The confirmed task description from Phase 0
   - **Assumptions & Constraints**: All hard constraints confirmed in Phase 0 — non-negotiable boundaries (e.g., "must not break public API", "stdlib only", "must support Node 18+"). These are the red lines the agent checks before making any implementation decision.
   - **Analysis Documents**: Links to all three files in `.spec/analysis/`
   - **Plan Documents**: Links to all three files in `.spec/plan/`
   - **Task Overview**: A summary table of all Tasks with completion status and link to detail file
   - **Current Status**: Which Task is currently active, what was last completed
   - **Next Steps**: What the agent should do next — written so a fresh agent can orient itself in under 30 seconds

2. Create **one progress file per Task**: `.spec/progress/task-N-<short-name>.md`

   Each file must begin with a status header:
   ```
   **Status**: IN_PROGRESS | BLOCKED | COMPLETE
   **Blocked by**: <describe the blocker, or N/A>
   **Resume point**: <which subtask to start from next session, or N/A>
   ```
   Followed by:
   - The Task's subtasks as checkboxes: `- [ ] Subtask description`
   - Acceptance criteria inline for each subtask
   - A **Notes** section for decisions, blockers, and context discovered during implementation

3. COMPASS.md task overview format:
   - Incomplete: `- [ ] Task N: <name> (0/X subtasks) — [details](./progress/task-N-<name>.md)`
   - Blocked:    `- [!] Task N: <name> (K/X subtasks) ⚠ BLOCKED — [details](./progress/task-N-<name>.md)`
   - Complete:   `- [x] Task N: <name> (X/X subtasks) — [details](./progress/task-N-<name>.md)`

**Output**: `.spec/COMPASS.md` and one progress file per Task.

---

## Phase 4: Task-Specific Sub-Skill Generation

**Goal**: Generate a sub-skill tailored to this specific development cycle, encoding implementation standards and the continuity protocol.

**Actions**:

1. Install the sub-skill at **project scope** (`.claude/skills/` or equivalent project-local location) by default. This keeps it tied to the project and discarded when the cycle is archived.

2. Delegate creation using the **`skill-creator`** skill (via the `Skill` tool), providing:
   - Task context from Phase 0
   - The desired skill name (e.g., `spec-coding-<project-name>`)
   - Content outline (see below)

   **If `skill-creator` is not installed**: Tell the user that generating a project-specific sub-skill requires skill-creator to be installed. Instruct them to run: `npx skills add anthropics/skills --skill skill-creator`. Do NOT install it on their behalf.

3. The generated sub-skill must instruct the agent to:
   - Always read `.spec/COMPASS.md` at the start of every conversation
   - Populate **TaskCreate** with pending subtasks before doing any work
   - After completing each subtask: check the box in the relevant progress file AND update the completion count and **Current Status** in COMPASS.md
   - Apply the technology-specific coding standards and conventions relevant to this transformation
   - When all checkboxes in COMPASS.md are marked `[x]`, trigger the Archive phase

**Output**: A project-scoped sub-skill installed and ready for the implementation stage.

---

## Phase 5: Handoff

**Goal**: Present all preparation artifacts and confirm readiness to begin implementation.

**Actions**:

1. Present a structured summary:
   - Confirmed task definition
   - Key findings from analysis (high-level only)
   - Task overview with group names and subtask counts
   - Description of the progress tracking setup
   - Sub-skill name and install location

2. List all generated artifacts:
   ```
   .spec/
   ├── COMPASS.md
   ├── analysis/
   │   ├── project-overview.md
   │   ├── module-inventory.md
   │   └── risk-assessment.md
   ├── plan/
   │   ├── task-breakdown.md
   │   ├── dependency-graph.md
   │   └── milestones.md
   └── progress/
       └── task-N-*.md  (one per Task)
   ```
   Plus the generated sub-skill at its install location.

3. Ask the user: **"Preparation complete. Ready to start Task 1?"**

**Output**: User confirmation to begin implementation.

---

## Implementation: Tasks

Once Phase 5 is confirmed, development proceeds as a series of **Tasks** (not Phases — Tasks are the unit of implementation work, not planning).

**At the start of every Task**:
1. Read `.spec/COMPASS.md` to confirm current position and re-read **Assumptions & Constraints**
2. Open the relevant `.spec/progress/task-N-<name>.md`
3. Populate **TaskCreate** with pending subtasks

**During each Task**:
- Work through subtasks one at a time
- After completing a subtask: check its box in the progress file, update COMPASS.md counts
- Record any decisions, surprises, or blockers in the Notes section of the progress file
- Dual-write: **TaskCreate** (real-time visibility) + Markdown files (cross-conversation persistence)

**Blocked Protocol** — if a subtask fails twice in a row, or if you encounter a constraint conflict you cannot resolve without user input:
1. Stop immediately. Do not attempt further workarounds.
2. Set the progress file's status header to `BLOCKED`, fill in **Blocked by** with the root cause and what was already attempted, and set **Resume point** to the current subtask.
3. Mark the Task as `[!] BLOCKED` in COMPASS.md and update **Current Status** accordingly.
4. Report to the user: what was blocked, why, and what decision or information is needed to unblock. Do not proceed to the next Task unless the user explicitly instructs you to skip this one.

**At the end of every Task**:
- Verify all acceptance criteria are met
- Set the progress file's status header to `COMPLETE`
- Mark the Task complete in COMPASS.md
- Update **Current Status** and **Next Steps** in COMPASS.md
- Inform the user which Task was completed and what comes next

**When all Tasks are complete**: Trigger the Archive phase automatically.

---

## Archive Phase

**Trigger**: All checkboxes in `.spec/COMPASS.md` are marked `[x]`.

**Goal**: Preserve this development cycle's artifacts in a structured archive so the next development cycle starts clean.

**Actions**:

1. Announce to the user that all Tasks are complete.

2. Determine the archive folder name:
   - Format: `YYYY-MM-DD-NN` where `NN` is a two-digit sequence starting at `01`
   - Check `.spec/archived/` for existing folders with today's date and increment `NN` accordingly
   - Example: `.spec/archived/2026-03-26-01/`

3. Use filesystem operations to move all current working artifacts into the archive folder, preserving internal structure:
   ```
   .spec/archived/YYYY-MM-DD-NN/
   ├── COMPASS.md
   ├── analysis/
   ├── plan/
   └── progress/
   ```

4. Remove the project-scoped sub-skill created in Phase 4 (it was specific to this cycle).

5. The `.spec/` root is now empty (except `archived/`), ready for the next development cycle.

6. Confirm to the user:
   - What was archived and where
   - That the sub-skill has been removed
   - That `.spec/` is ready for the next cycle
   - Suggest committing any production code changes from this cycle to version control if not already done

**Output**: A clean `.spec/` workspace. Past cycle preserved. Next cycle can begin immediately with Phase 0.

---

## Behavioral Rules

1. **Never skip phases.** Even for small projects, at minimum create lightweight versions of each phase's outputs.
2. **Confirm with the user at each phase boundary.** Every handoff is a checkpoint.
3. **Document decisions.** If you make a judgment call, record it in the relevant progress file's Notes section.
4. **Progress updates are mandatory.** After completing any subtask, immediately update the checkbox AND COMPASS.md counts.
5. **New conversation = read COMPASS.md first.** Non-negotiable. It is your memory.
6. **Dual-write progress.** **TaskCreate** for real-time visibility; Markdown files for cross-conversation persistence.
7. **Archive is not optional.** When all Tasks are done, always archive. Don't leave stale artifacts in the working area.
8. **`.spec/` is always gitignored.** Verify this at the start of every fresh session before writing any files.
9. **Stop before you spiral.** If a subtask fails twice or hits a constraint conflict, invoke the Blocked Protocol immediately. Attempting a third workaround without user input is not persistence — it is wasted context.

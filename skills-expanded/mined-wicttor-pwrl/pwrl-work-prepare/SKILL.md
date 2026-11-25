---
name: pwrl-work-prepare
description: Set up execution environment, create task lists, and select execution mode
argument-hint: "[Classified context from pwrl-work-triage]"
---

# pwrl-work-prepare — Environment Setup & Mode Selection

## Interaction Method

- Use platform's `ask_user_question`, `ask_user`, `ask_user_input`, `vscode/askQuestions` or any available extension/tool for user interaction for all decisions
- Ask one question at a time
- Use multiple-choice questions when possible
- If input is empty, ask: "Is the work environment ready? Review and confirm the repository state, branch setup, and dependencies."
- Provide clear recovery suggestions when errors occur

**Purpose:** Bridges triage output and task execution. Confirms branch strategy, creates or updates task lists, detects the appropriate execution mode (inline/serial/parallel), checks GitHub integration readiness, and produces a prepared context ready for execution.

## Input

Accepts a classified context object from `pwrl-work-triage`:

- Task file context (with `unit-id`, `dependencies`, `files`, etc.)
- Plan file context (with `units`, `complexity`, etc.)
- Bare prompt context (with `prompt`, `complexity`, etc.)

## Output: Prepared Context

```yaml
branchStrategy: new-branch | direct-commit
branchName: feat/xyz | null
taskList:
  source: plan | task | prompt
  taskCount: 5
  tasks:
    - unit-id: S1
      file: docs/tasks/in-progress/2026-06-05-s1-task.md
      dependencies: []
      status: in-progress
executionMode: inline | serial | parallel
executionModeReasoning: "3+ tasks with dependencies → serial"
githubIntegration:
  enabled: true | false
  tasksLinked: 3
  readyForSync: true | false
```

---

## Workflow

### 1. Confirm Branch Strategy

Ask user and document the branch approach:

**Prompt:** "Should this work be on a new branch or commit directly to the current branch (`[current-branch]`)?

**Rules:**

- New branch recommended for non-trivial work (3+ tasks or significant changes)
- Direct commit acceptable only for trivial/small changes (1-2 tasks, no cross-cutting impact)

**If new branch:**

1. Suggest a name: `feat/<short-description>` or `fix/<short-description>`
2. Ask user to confirm or provide a custom name
3. Create branch: `git checkout -b <name>`
4. Log: `Branch created: <name>`

**If direct commit:**

1. Warn: "Direct commits bypass branch protection; use only for trivial/small work"
2. Require explicit confirmation: "I understand and will commit directly"
3. Only proceed if confirmed

**Output:**

```yaml
branchStrategy: new-branch
branchName: feat/slice-pwrl-work
branchCreated: true
```

### 2. Create or Update Task List

#### 2A. From Plan File (Multiple Tasks)

When the triage output is from a plan file:

1. For each implementation unit in the plan's `units` list:
   - Derive slug from unit name (lowercase, hyphenated)
   - Create task file at `docs/tasks/to-do/YYYY-MM-DD-[unitId]-[slug].md`
   - Set frontmatter:

```yaml
---
unit-id: U1
plan: docs/plans/YYYY-MM-DD-NNN-plan.md
status: to-do
created: YYYY-MM-DD
dependencies: [list from plan]
files: [list from plan]
---
```

2. Populate task body with:
   - **Goal:** From plan unit scope
   - **Context:** From plan unit description
   - **Implementation Steps:** Decomposed from plan unit approach
   - **Test Scenarios:** From plan verification sections
   - **Acceptance Criteria:** From plan unit acceptance

3. Create or update `docs/tasks/INDEX.md`:
   - Status table (unit ID, task, status, dependencies, files)
   - Dependency graph (ASCII or markdown)
   - Critical path analysis
   - Recommended starting tasks

4. **Important:** If task files already exist (detected by matching `unitId` in frontmatter), skip creation and use existing files

#### 2B. From Single Task File

When triage output is a single task file:

1. **CRITICAL: Move task file** `docs/tasks/to-do/` → `docs/tasks/in-progress/`
   - Read the task file from `to-do/` folder
   - Update frontmatter status: `status: to-do` → `status: in-progress`
   - Write the updated file to `docs/tasks/in-progress/` with same filename
   - Delete original from `to-do/`
   - Log: `Task moved: docs/tasks/to-do/[file] → docs/tasks/in-progress/[file]`

2. Verify dependencies:
   - Check `docs/tasks/INDEX.md` (or `INDEX-S*.md`) for each dependency's status
   - If any dependency is `to-do` or `in-progress`: warn user
   - Offer options: "Proceed anyway (manual dependency management) or wait?"

3. Update `docs/tasks/INDEX.md`:
   - Update status table to reflect new location and status
   - Update cross-references if needed

**Status Transition:**

```
to-do/ (status: to-do) → in-progress/ (status: in-progress)
```

#### 2C. From Bare Prompt

When triage output is a bare prompt:

1. Create a minimal inline task list (structured locally, no files)
2. For 1-2 tasks: structure as simple checklist
3. For 3+ tasks or non-trivial: recommend creating task files
4. Present to user for approval before proceeding

### 3. Detect Execution Mode

**NEW: Task Status State Machine & Validation**

Before detecting mode, validate task status transitions:

```
State Diagram:
  to-do → in-progress → for-review → done
    ↑                                    │
    └────────────── blocked ◄────────────┘
```

**Transition Validation Rules:**

- Can't mark `done` if any dependencies not `done` → Error: "Cannot mark done: S2 still in-progress"
- Can't mark `in-progress` if already `for-review` → Error: "Review must complete before re-entering in-progress"
- Idempotent transitions allowed (stay in same state)
- Global unit-id uniqueness: Error if same unit-id in multiple plans

**Validation pseudocode:**

```
validateTransition(taskId, newStatus):
  currentStatus = taskCurrentStatus(taskId)

  if currentStatus == newStatus:
    return OK  # Idempotent

  # Get dependencies from globalDependencyGraph
  deps = graph.getDependencies(taskId)

  if newStatus == "done":
    for dep in deps:
      if dep.status != "done" and dep.status != "for-review":
        return ERROR("Cannot mark done: {dep.unit-id} still {dep.status}")

  return OK
```

**Apply to all tasks in taskList:**

1. For each task, validate its status transition
2. If any validation fails, report error with task ID and reason
3. Ask user: "Resolve status issues and retry?"

---

**Execute Automatic Mode Selection**

Apply automatic mode selection based on task count, dependencies, and file conflicts:

**Decision tree (updated for cross-plan):**

```
taskCount = number of tasks in taskList

if taskCount <= 2:
    → INLINE (direct execution, no subagents needed)

if taskCount >= 3:
    → Check dependency graph (including cross-plan edges)
    → Build file-to-task map from each task's `files` field
    → Detect any file conflicts (same file touched by 2+ tasks)

    if any dependencies exist between tasks:
        IF critical path spans multiple plans:
            → SERIAL (forced; need sync points between groups)
        ELSE:
            → Check for file conflicts
            if file conflicts detected:
                → SERIAL (forced; parallel would create race conditions)
            else:
                → PARALLEL with topological grouping (see step 5 below)
    else if any file conflicts detected:
        → SERIAL (forced; parallel would create race conditions)
    else:
        → PARALLEL (independent tasks with no file overlap; use parallelization groups)
```

**File conflict detection heuristic:**

1. Collect all file paths from each task's `files` field
2. Create a map: file → [taskId1, taskId2, ...]
3. If any file appears in more than one task's files → conflict
4. Document all conflicting files and tasks

**Critical path analysis for cross-plan:**

1. Find longest dependency chain in globalDependencyGraph
2. If chain includes tasks from multiple plans → critical path spans plans
3. Set flag: `criticalPathMultiPlan: true/false`

**Parallel execution constraints:**

- Only targeted tests run during implementation (not full suite)
- Staging and committing deferred to review phase
- Results aggregated before final quality gates
- **NEW**: For cross-plan parallel: sync points between groups (see step 5)

**Output:**

```yaml
executionMode: serial
executionModeReasoning: "5 tasks with sequential dependency chain (S1→S2→S3→S5→S6→S7)"
hasFileLevelConflicts: false
conflictingFiles: []
parallelSafetyGate: not-applicable
criticalPathMultiPlan: false
```

---

### 3.5 NEW: Topological Sort with Parallelization Groups (if parallel mode selected)

**Purpose**: Generate task parallelization clusters for parallel/cross-plan execution.

**Algorithm (Modified Kahn's Topological Sort):**

```pseudocode
topologicalSortWithGroups(tasks, dependencies):
  inDegree = computeInDegrees(tasks, dependencies)
  groups = []
  current_group = []

  while tasks_remaining:
    # Find all tasks with inDegree == 0 (no remaining dependencies)
    ready_tasks = [t for t in tasks if inDegree[t] == 0]

    if NOT ready_tasks:
      return ERROR("Circular dependency detected")

    # Check for file conflicts within ready_tasks
    for task in ready_tasks:
      # If task conflicts with any already in current_group, start new group
      if hasFileConflict(task, current_group):
        if current_group:
          groups.append(current_group)
        current_group = [task]
      else:
        current_group.append(task)

    # Move to next level
    for task in ready_tasks:
      inDegree[task] = -1  # Mark as processed
      for dependent in dependencies[task]:
        inDegree[dependent] -= 1

  if current_group:
    groups.append(current_group)

  return { parallelGroups: groups, syncPoints: [after-group-N for N in 1..len(groups)] }
```

**Output format:**

```yaml
parallelGroups:
  - group: 0
    tasks: [S1, U1, U2] # These can run parallel (no file conflicts)
    duration_estimate: "5 min"
  - group: 1
    tasks: [S2, U3] # Depends on group 0; can run parallel within group
    duration_estimate: "3 min"
  - group: 2
    tasks: [S3] # Single task
    duration_estimate: "2 min"

syncPoints:
  - syncPoint: 0
    after_group: 0
    validation: "No file conflicts; commit atomically"
  - syncPoint: 1
    after_group: 1
    validation: "No file conflicts; commit atomically"

execution_strategy: "Parallel within groups; serial between groups; atomic commits per sync point"
cross_plan_groups:
  { group_0: ["plan-A", "plan-B"], group_1: ["plan-A"], group_2: ["plan-A"] }
```

---

### 4. Locate or Update Task Files (updated for cross-plan)

**Step 1 — Multi-plan task discovery:**

1. Glob pattern: `docs/tasks/**/*.md` (all plans)
2. For each file found, extract frontmatter `unit-id` and `plan` field
3. If `unit-id` matches current task → found existing task
4. If duplicate `unit-id` found in different plan → error "Duplicate unit-id: S1 in plans A and B"
5. Load task file with parent plan attribution

**Step 2 — Cross-reference validation:**

- Verify `plan` field in task frontmatter matches the plan we're executing
- Warn if plan reference mismatch

**Step 3 — Status field validation:**

- Apply task status state machine validation (from step 3)
- Update status if needed (e.g., from `to-do` → `in-progress`)

---

### 5. User Confirmation Checkpoint

Before proceeding to execution, present a summary and ask for confirmation:

---

**📋 Preparation Summary**

| Item       | Value                           |
| ---------- | ------------------------------- |
| **Branch** | `feat/slice-pwrl-work` (new)    |
| **Tasks**  | 5 tasks: S1 → S2 → S3 → S5 → S6 |
| **Mode**   | Serial (dependent chain)        |
| **GitHub** | Enabled, 3 tasks linked         |

**Ready to begin execution?**

- ✅ **Yes, proceed** — Begin Phase 2 (Execute)
- 🔄 **Review branch** — Change branch strategy
- 📋 **Review tasks** — Adjust task list or dependencies
- ❌ **Cancel** — Halt all work

---

**If cancelled:**

- Log: `Work cancelled by user at preparation checkpoint`
- No tasks marked as `in-progress`
- User can re-invoke with updated parameters

---

## Error Handling

| Scenario                             | Handling                                                                      |
| ------------------------------------ | ----------------------------------------------------------------------------- |
| Branch creation fails                | Log git error; ask user: "Resolve git state manually or retry?"               |
| Malformed task frontmatter           | Log details; ask user to fix and retry                                        |
| Circular dependencies detected       | Fail; ask user to resolve circular references                                 |
| User cancels at checkpoint           | Exit gracefully; preserve current state                                       |
| Blocking dependencies exist          | Warn; ask user: "Proceed anyway or wait for dependencies?"                    |
| GitHub integration check fails       | Log warning; continue without sync                                            |
| Task file doesn't exist              | Offer to create from plan; ask user: "Create task or provide different path?" |
| INDEX.md is missing                  | Create automatically; warn user                                               |
| No tasks in task list                | Block execution; ask user to review and confirm task list                     |
| Execution mode indeterminate         | Ask user to specify preferred mode                                            |
| Dependency chain >5 deep             | Flag for review; user can accept or simplify                                  |
| File conflicts detected              | Force serial mode; inform user                                                |
| GitHub sync skipped (missing issues) | Log warning; continue without sync                                            |

**Retry limit:** 3 attempts per operation, then ask user to fix manually.

**Fallback:** If all retries fail, log the error and ask user: "Retry, skip, or abort?"

---

## Dependencies

- **pwrl-work-triage** — Consumes classified context from this skill
- **`.pwrlrc.json`** — For GitHub integration check
- **Git** — For branch operations
- **File system** — For task file creation and movement
- **User input** — For branch strategy, task approval, and checkpoint confirmation

## References

- **S1 Analysis:** `docs/analysis/2026-06-05-pwrl-work-structure-analysis.md`
- **S2 Skill:** `pwrl-work-triage/SKILL.md`
- **Source Phase 1:** Installed `pwrl-work` skill (Phase 1: Prepare Context, lines 49-121)
- **Next Skill:** `pwrl-work-execute` (consumes prepared context)
- **Sibling Skill:** `pwrl-work-sync-status` (called for GitHub sync if enabled)

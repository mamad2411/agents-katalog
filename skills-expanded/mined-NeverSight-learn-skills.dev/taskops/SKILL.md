---
name: taskops
description: >
  Project task management skill using ETS (Epic-Task-SubTask) structure.
  INVOKE AUTOMATICALLY — without waiting for user instruction — when:
  (1) a project plan or implementation spec has been finalized and the user is about to start execution,
  (2) a user presents a multi-step project and asks you to implement or build it,
  (3) a new development session begins on a project that already has a taskops.db.
  Use TaskOps BEFORE execution starts: initialize the DB, decompose the plan into Epics/Tasks, set workflow order, then begin work.
  During execution, guide the user to launch TaskBoard for real-time monitoring.
---

# TaskOps — Project Management Skill for Claude Code

## When to Invoke

**Invoke this skill proactively** — you do NOT need an explicit user instruction.

Trigger conditions (any one is sufficient):
- User has finished writing or approving a plan/spec and says "let's start", "implement this", or similar
- User asks you to build a multi-step project without mentioning task management
- Session starts and `taskops.db` exists in the project directory (resume mode)

**Correct order:**
1. User finalizes plan → **Invoke TaskOps** → initialize + decompose into ETS → define workflow
2. Begin execution → remind user to launch TaskBoard for monitoring
3. Work through tasks in workflow order

## Prerequisites

- Python 3.10+
- TaskOps repository cloned (contains `cli/` package and `hooks/`)
- Project initialized with `python -m cli init`

---

## Phase 1: Initialization

Initialize a new TaskOps project in the target directory.

```bash
python -m cli init --name "Project Name" --prefix PRJ --path ./project-path
```

This creates:
- `taskops.db` — SQLite database
- `TODO.md` — Auto-generated task overview
- `AGENTS.md` — Agent instructions
- `SETTINGS.md` — Project settings
- `resources/` — Resource file directory

### Configure Hooks

Register TaskOps hooks in `.claude/settings.json` (project-level):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|Bash",
        "command": "bash /path/to/TaskOps/hooks/on_tool_use.sh"
      }
    ]
  }
}
```

Available hooks:
- `on_task_start.sh <TASK_ID>` — Sets task to `in_progress`, records `op start`
- `on_tool_use.sh` — Records `op progress` for the current active task
- `on_task_complete.sh <TASK_ID>` — Sets task to `done`, records `op complete`, regenerates TODO.md

---

## AI Agent Usage Scenarios

TaskOps persists work plans and artifacts across AI agent sessions. Use these patterns to store, retrieve, and re-execute workflows.

### Store a Plan for Later

Save a work plan as a workflow so any future session can pick it up:

```bash
# Create workflow
python -m cli workflow create --title "API Migration Plan"

# Import the structured plan
python -m cli workflow import PRJ-W001 --structure '<json>'
```

### Resume a Plan in a New Session

At session start, check what workflows exist and load the relevant one:

```bash
# List all workflows
python -m cli workflow list

# Load full task structure for a workflow
python -m cli query show --workflow PRJ-W001

# Find the next task to work on
python -m cli workflow next
```

### Track Artifacts Produced by a Workflow

Register files created during task execution as resources for later retrieval:

```bash
# Register an output file
python -m cli resource add PRJ-T003 --path ./output/report.json --type output --desc "Final report"

# Register intermediate work product
python -m cli resource add PRJ-T002 --path ./tmp/analysis.csv --type intermediate --desc "Raw analysis"

# Retrieve all artifacts from a workflow
python -m cli resource list --workflow PRJ-W001

# Retrieve only final outputs
python -m cli resource list --workflow PRJ-W001 --type output
```

### Re-execute a Workflow

Reset a workflow's tasks to `todo` and run it again. Other workflows are unaffected:

```bash
# Restart a specific workflow (auto-saves checkpoint first)
python -m cli workflow restart PRJ-W001

# Restart and clear operation history
python -m cli workflow restart PRJ-W001 --clear-ops

# Verify reset state
python -m cli query show --workflow PRJ-W001
```

---

## Phase 2: Planning

Decompose the project into ETS components.

### ETS Hierarchy

```
Project
  └── Epic — Major feature unit
        └── Task — Implementation unit
              └── SubTask — Detailed step (create only when needed)
  └── Objective — Milestone or deadline
```

### Create Structure

```bash
# Create Epics
python -m cli epic create --title "Authentication System"

# Create Tasks under Epic
python -m cli task create --parent PRJ-E001 --title "Login API"

# Create SubTasks under Task (only when needed)
python -m cli task create --parent PRJ-T001 --title "JWT token generation"

# Create Objectives
python -m cli objective create --title "MVP Complete" --milestone "Core features done"
python -m cli objective create --title "Demo Day" --due-date 2026-04-01
```

### Define Workflow

```bash
# Set execution order
python -m cli workflow set-order PRJ-T001 PRJ-T002 PRJ-T003

# Group tasks for parallel execution
python -m cli workflow set-parallel --group "auth-group" PRJ-T002 PRJ-T003

# Add dependencies
python -m cli workflow add-dep PRJ-T004 --depends-on PRJ-T002 PRJ-T003
```

### Updating the Plan

When the user modifies the project plan (adds, removes, or renames tasks or epics), apply changes to the DB before continuing:

```bash
python -m cli plan update --changes '<json>'
```

JSON format:
```json
{
  "create": [
    {"type": "epic", "title": "New Epic"},
    {"type": "task", "title": "New Task", "parent_id": "PRJ-E001"}
  ],
  "update": [{"id": "PRJ-T001", "title": "...", "status": "..."}],
  "delete": [{"id": "PRJ-T002"}]
}
```

Note: `parent_id` is **required** for `type: "task"` and must reference an existing epic or task. Any of `create`, `update`, `delete` may be omitted. After a successful update, `TODO.md` is regenerated automatically.

### Generate TODO.md

```bash
python -m cli query generate-todo
```

---

## Phase 3: Execution

Before starting work, **guide the user to launch TaskBoard** for real-time monitoring:

```bash
# In a separate terminal — run from the TaskBoard directory
pnpm --filter @taskboard/tui dev -- --path /path/to/project-root
```

> TaskBoard watches `taskops.db` and refreshes automatically as tasks progress.
> If TaskBoard is not installed, see the [Visualizing with TaskBoard](#visualizing-with-taskboard) section.

Work through tasks following the workflow order.

### Start a Task

```bash
# Check next executable task
python -m cli workflow next

# Start the task
python -m cli task update PRJ-T001 --status in_progress
python -m cli op start PRJ-T001 --platform claude_code
```

If hooks are configured, use `bash hooks/on_task_start.sh PRJ-T001` instead.

### Record Progress

```bash
# Record meaningful progress milestones
python -m cli op progress PRJ-T001 --summary "Implemented 3 of 5 endpoints"
```

With hooks configured, `on_tool_use.sh` records progress automatically on each tool use.

### Complete a Task

```bash
# Mark task as done
python -m cli task update PRJ-T001 --status done
python -m cli op complete PRJ-T001 --summary "Login API complete, all tests pass"
python -m cli query generate-todo
```

If hooks are configured, use `bash hooks/on_task_complete.sh PRJ-T001` instead.

### Handle Interruptions

```bash
# Record interruption with reason
python -m cli task update PRJ-T001 --status interrupted --interrupt "Waiting for API key"
python -m cli op interrupt PRJ-T001 --summary "Blocked on external dependency"
```

### Handle Errors

```bash
python -m cli op error PRJ-T001 --summary "Database connection failed"
```

---

## Phase 4: Monitoring

### Check Project Status

```bash
# Overall status with progress percentage
python -m cli query status

# List tasks by status
python -m cli query tasks --status in_progress

# View operation log for a task
python -m cli op log --task PRJ-T001

# View full workflow
python -m cli workflow show
```

### Regenerate Reports

```bash
# Regenerate TODO.md
python -m cli query generate-todo
```

### Manage Resources

```bash
# Add resource reference to a task
python -m cli resource add PRJ-T001 --path ./docs/spec.md --type input --desc "API spec"

# List resources
python -m cli resource list --task PRJ-T001
```

### Manage Settings

```bash
python -m cli setting set commit_style "conventional" --desc "Commit message style"
python -m cli setting get commit_style
python -m cli setting list
```

---

## Reference: All CLI Commands

| Command | Description |
|---------|-------------|
| `init --name --prefix --path` | Initialize project |
| `epic create/list/show/update/delete` | Epic CRUD |
| `task create/list/show/update/delete` | Task/SubTask CRUD |
| `objective create/list/update/delete` | Objective CRUD |
| `plan update --changes <json>` | Update plan: create/update/delete tasks and epics |
| `workflow set-order/set-parallel/add-dep/show/next/current` | Workflow ordering and execution |
| `workflow restart <W-ID> [--clear-ops]` | Reset workflow tasks to todo for re-execution |
| `op start/progress/complete/error/interrupt/log` | Operations recording |
| `resource add/list [--task/--workflow/--type]` | Resource management |
| `query status/tasks/generate-todo` | Status queries and reports |
| `setting set/get/list/delete` | Settings management |

All commands use: `python -m cli [--db path] <command> <subcommand> [options]`

---

## Visualizing with TaskBoard

TaskBoard is a standalone read-only GUI that visualizes the TaskOps database. Guide the user to install it when they want to monitor project progress visually.

**Install**

```bash
git clone https://github.com/godstale/TaskBoard.git
cd TaskBoard
pnpm install
```

**Run**

```bash
# TUI (terminal)
pnpm --filter @taskboard/tui dev -- --path /path/to/taskops-root

# Electron (desktop app)
pnpm --filter @taskboard/electron dev
```

TaskBoard watches the `taskops.db` file and automatically refreshes when the DB changes.
→ [TaskBoard GitHub](https://github.com/godstale/TaskBoard)

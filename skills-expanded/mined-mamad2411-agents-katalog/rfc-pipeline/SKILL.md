---
name: rfc-pipeline
version: 1.0.0
min_mindforge_version: 10.0.4
status: stable
triggers: rfc, spec decompose, dependency DAG, task graph, parallel execution, merge conflict recovery, task pinning, worktree isolation, execution plan, spec-to-tasks, dependency resolution, reproducible execution
compose:
  - autonomous-loops
---

# Skill — RFC Pipeline

## When this skill activates

When a specification, RFC, or feature document needs to be decomposed into
executable tasks with dependency ordering. Also activates when planning parallel
work across multiple files or modules, when managing complex multi-step
implementations, or when explicitly asked to create an execution DAG.

## Mandatory actions when this skill is active

### Step 1 — Parse Spec into Atomic Tasks

Decompose the specification into discrete, atomic tasks where each task has:

- **ID**: unique identifier (e.g., `T001`, `T002`)
- **Description**: what this task accomplishes
- **Inputs**: what must exist before this task can start (files, APIs, schemas)
- **Outputs**: what this task produces (files created/modified, APIs available)
- **Estimated complexity**: S/M/L
- **Acceptance criteria**: how to verify the task is done

### Step 2 — Build Directed Acyclic Graph

Construct the dependency graph:

- Each task is a node
- An edge from A to B means "A must complete before B can start"
- Detect cycles: if any cycle exists, STOP and report as an error
- Cycles indicate ambiguous dependencies that must be resolved before proceeding
- Store edges as explicit `depends_on` arrays per task

### Step 3 — Assign Parallel Waves

Group tasks by dependency depth:

- **Wave 0**: tasks with no dependencies (can start immediately)
- **Wave 1**: tasks that depend only on Wave 0 tasks
- **Wave N**: tasks that depend only on tasks in waves < N
- Tasks within the same wave are independent and can execute in parallel
- Tasks across waves execute sequentially (Wave 0 completes before Wave 1 starts)

### Step 4 — Pin Tasks to Commits

For reproducibility:

- Record the base commit SHA that the plan was created against
- Each completed task records the commit SHA of its output
- If the base branch advances, detect drift and flag affected tasks
- Pinning ensures any task can be reproduced from a known state

### Step 5 — Execute Waves

Run the plan:

- Execute all tasks in the current wave in parallel
- Wait for all tasks in the wave to complete before advancing
- Verify outputs of each task match acceptance criteria
- If a task fails, halt that dependency chain (other chains continue)

### Step 6 — Merge-Conflict Recovery

When parallel tasks produce conflicting changes:

- Detect conflicts immediately after wave completion
- Isolate conflicting tasks into a resolution queue
- Resolve conflicts sequentially (human or automated merge)
- Re-run acceptance criteria on merged result
- Never auto-resolve conflicts that touch the same logical block

### Step 7 — Worktree-Based Isolation

For true parallel execution:

- Each parallel task gets its own git worktree (branch from pinned SHA)
- Tasks cannot see each other's in-progress changes
- Merge worktrees back to the integration branch after wave completes
- Clean up worktrees after successful merge

### Output

Store the DAG and execution state in `.planning/rfc/[name]/DAG.json` with schema:

```json
{
  "name": "rfc-name",
  "base_sha": "abc123",
  "tasks": [...],
  "waves": [[...], [...]],
  "status": "in-progress|complete|blocked"
}
```

## Self-check before task completion

Before marking a task done when this skill was active:

- [ ] Did I decompose the spec into atomic tasks with clear inputs/outputs?
- [ ] Did I verify no cycles exist in the dependency graph?
- [ ] Did I assign tasks to parallel waves correctly?
- [ ] Did I pin tasks to commit SHAs for reproducibility?
- [ ] Did I handle (or plan for) merge conflicts between parallel tasks?
- [ ] Did I store the DAG in .planning/rfc/[name]/DAG.json?
- [ ] Can each task be executed independently given its inputs?

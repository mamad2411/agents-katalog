---
name: taskwing-next
description: Use when you are ready to start the next approved TaskWing task with full context.
---

# Start Next TaskWing Task with Full Context

The Workflow Contract lives in CLAUDE.md (single source of truth). Obey it always.

## Kill Table

| Impulse | Do Instead |
|---------|------------|
| Skip `ask` calls for context | Always fetch scope + task context before coding |
| Start coding without approval | Present the brief, wait for explicit checkpoint approval |
| Ignore patterns/constraints from ask | Patterns are binding, constraints are mandatory |

## Operating Principles

1. **Context before code.** Always run `taskwing ask` for both scope and task-specific context before presenting the brief.
2. **The brief is the contract.** The task brief (Step 5) defines what you will build. Do not deviate without re-checking.
3. **Patterns are binding.** If `ask` returns patterns for the task scope, follow them. If constraints exist, respect them.

Execute these steps IN ORDER. Do not skip any step.

## Step 1: Get Next Task

Run:

```bash
taskwing task next
```

Extract from the JSON response:
- task_id, title, description
- scope (e.g., "auth", "vectorsearch", "api")
- keywords array
- acceptance_criteria
- suggested_ask_queries (if present)

If the command reports no pending task, inform the user: "No pending tasks. Use /taskwing:context to check plan status."

## Step 2: Fetch Scope-Relevant Context

Run `taskwing ask` with a query based on the task scope:

```bash
taskwing ask "<task.scope> patterns constraints decisions"
```

Examples:
- scope "auth" → `taskwing ask "authentication cookies session patterns"`
- scope "api" → `taskwing ask "api handlers middleware patterns"`
- scope "vectorsearch" → `taskwing ask "lancedb embedding vector patterns"`

Extract: patterns, constraints, related decisions.

## Step 3: Fetch Task-Specific Context

Run `taskwing ask` with keywords from the task. Use `suggested_ask_queries` if available, otherwise extract keywords from the title.

```bash
taskwing ask "<keywords from task title/description>"
```

## Step 4: Claim the Task

Run:

```bash
taskwing task start <task_id>
```

(`<task_id>` is the value from Step 1.)

## Step 5: Present Unified Task Brief

Display in this format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK: [task_id] (Priority: [priority])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**[Title]**

## Description
[Full task description]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHITECTURE CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Relevant Patterns
[Patterns from ask that apply to this task]

## Constraints
[Constraints that must be respected]

## Related Decisions
[Past decisions that inform this work]

## Key Files
[Files likely to be modified based on context]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task claimed. Ready to begin.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Step 6: Implementation Start Gate (Hard Gate)

Before writing or editing code, ask for an explicit checkpoint:
"Implementation checkpoint: proceed with task [task_id] now?"

If approval is missing or unclear, STOP and respond with:
"REFUSAL: I can't start implementation yet. Plan/task checkpoint is incomplete. Please approve this task checkpoint first."

## Step 7: Begin Implementation (Only After Approval)

Proceed with the task, following the patterns and respecting the constraints shown above.

**CRITICAL**: You MUST run all four CLI commands (`task next`, `ask` x2, `task start`) before showing the brief and before requesting implementation approval.

## Useful Variants

```bash
taskwing task list                    # see all tasks
taskwing task list --status pending   # identify next pending task
taskwing task next --auto-start       # claim immediately, single call
```

Use `/taskwing:context` to check active plan progress.

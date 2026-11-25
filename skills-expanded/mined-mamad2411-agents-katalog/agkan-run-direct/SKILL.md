---
name: agkan-run-direct
description: Use when starting a development session to pick the highest priority Todo task from agkan, implement it directly without PR/branch, and mark it done.
---

# agkan-run-direct

## Overview

A workflow to select the highest priority ready task from agkan, implement it directly without creating a branch or PR, and mark it as done.

---

## Workflow

### 1. Update Branch

This skill is designed to commit directly to the current branch (default branch or topic branch).
Therefore, only execute `git pull -p` (unlike `agkan-run`, there is no need to create a new branch from the default branch).

- When running on a topic branch: implement directly on the current branch
- When starting from the default branch: get the default branch name dynamically and execute checkout + pull beforehand if necessary

```bash
# Get the default branch name dynamically
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@') && \
  [ -z "$DEFAULT_BRANCH" ] && DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name' 2>/dev/null)
# Then pull
git pull -p
```

### 2. Get Ready Tasks

```bash
agkan task list --status ready --json
```

### 3. Select One High-Priority Task

Evaluate tasks using the following criteria in descending order and select the top one:

**Skip tasks with `will-do-later` tag:**
Tasks with the `will-do-later` tag are intentionally deferred tasks, so skip them. Only select tasks without the `will-do-later` tag.

**Priority (read from `metadata` field in the list JSON response):**
```
Critical > High > Medium > Low
```

**Tags (used when priority is the same):**
```
bug > security > improvement > test > performance > refactor > docs
```

**When there are subtasks or blocker tasks**
Prioritize the target subtasks or blocker tasks (using the same importance and tag criteria)

### 4. Check for Blockers

```bash
agkan task block list <id> --json
```

If incomplete tasks exist in `blockedBy`, do not select that task; instead, select a different task or process the blocker tasks first.

### 5. Update Task Status to in_progress

```bash
agkan task update <id> --status in_progress
```

### 6. Implementation and Completion

Use the **Task tool (general-purpose sub-agent)** to implement.
Do not use `Skill("agkan-subtask-direct")`; instead, instruct the sub-agent to read the SKILL.md file directly.

> **Why SKILL.md path instead of `Skill()`?**
> Sub-agents spawned via the Task tool start with a fresh context. `Skill()` loads skill content into the current conversation, but a sub-agent needs its instructions embedded in its prompt. Providing the SKILL.md path directly in the prompt is the reliable way to pass workflow instructions to a sub-agent.

```
Task(
  subagent_type="general-purpose",
  description="Implement task #<id>",
  prompt="""
Please implement the following task.

Invoke the key-guidelines skill using the Skill tool: Skill("key-guidelines")

## Task Information
- ID: <id>
- Title: <title>
- Body: <body>

## Procedure
Load .claude/skills/agkan-subtask-direct/SKILL.md and follow its procedures to implement.

## Error Handling
If a critical error occurs during implementation (git push failure, commit failure,
permission denied, etc.), do NOT update the task status to done. Leave the task as
`in_progress` and record the error in the task body:
```bash
agkan task get <id> --json
# Write body to tmp file and update using --file to preserve newlines
cat > /tmp/agkan_body_$$.md << 'BODY'
<existing body>

Error: <error description>
BODY
agkan task update <id> --file /tmp/agkan_body_$$.md
```
Only update to done if implementation and all commits/pushes succeeded.
"""
)
```

### 7. Verify Task Status After Sub-Agent Completes

After the sub-agent completes, check whether the task has been moved out of `in_progress`:

```bash
agkan task get <id> --json
```

If the status is still `in_progress`, determine whether the sub-agent encountered a critical error (git push failure, commit failure, permission error). Check the task body for any recorded error messages.

- **If a critical error occurred**: Do NOT update to `done`. Leave the task as `in_progress` so the issue can be resolved manually.
- **If no critical error occurred** and implementation succeeded but the sub-agent forgot to update the status, update it manually:

```bash
agkan task update <id> --status done
```

### 8. Re-fetch Task List and Continue or End Session

After the sub-agent completes, re-fetch the task list to pick up any newly added ready tasks:

```bash
agkan task list --status ready --json
```

If there is no instruction to end from the user and ready tasks exist (including newly added ones), select the next task and repeat from step 3 of the same workflow.

If no ready tasks remain, end the session.

---

## Priority Determination Flow

```
Ready task list
    ↓
Sort by priority (Critical → High → Medium → Low)
    ↓
Multiple tasks with same priority?
   Yes → Sort by tag priority (bug → security → ... → docs)
   No  → Select the top task
    ↓
Select one task and start
```

---

## Tag Priority List

See the canonical definition in `agkan/SKILL.md` (Tag Priority section).

---

## Important Notes

- Always select only one task (do not work on multiple tasks simultaneously)
- If no tasks exist, end the session
- Do not create branches or PRs (commit directly to the current branch)
- Task status update to done and static analysis checks are handled inside the sub-agent (agkan-subtask-direct), not in the main thread

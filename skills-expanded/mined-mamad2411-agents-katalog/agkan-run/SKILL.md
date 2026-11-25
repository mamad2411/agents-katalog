---
name: agkan-run
description: Use when starting a development session to pick the highest priority Todo task from agkan, implement it, create a pull request, and mark it done.
---

# agkan-run

## Overview

Standard workflow to pick the highest priority ready task from agkan, implement it, create a pull request, and complete it.

**CRITICAL: This is a loop. After each task completes (including handling any interruptions), ALWAYS re-fetch the task list and continue unless explicitly told to stop.**

---

## Workflow

### 1. Update branch to latest

Before switching to the default branch, check for uncommitted changes:

```bash
git status --porcelain
```

If there are uncommitted changes, stash them first:

```bash
git stash push -m "agkan-run: stash before switching to default branch"
```

Then get the default branch name dynamically and update to latest:

```bash
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@') && \
  [ -z "$DEFAULT_BRANCH" ] && DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name' 2>/dev/null) && \
  git checkout "$DEFAULT_BRANCH" && git pull -p
```

### 2. Get ready tasks

```bash
agkan task list --status ready --json
```

### 3. Select the highest priority task

Evaluate tasks in descending order using the following criteria and select the top one:

**Skip tasks with `will-do-later` tag:**
Tasks with the `will-do-later` tag are intentionally postponed tasks, so skip them. Only select tasks that do not have the `will-do-later` tag.

**Priority (read from `metadata` field in the list JSON response):**
```
Critical > High > Medium > Low
```

**Tags (refer to when priority is the same):**
```
bug > security > improvement > test > performance > refactor > docs
```

**If there are child tasks or blocker tasks**
Prioritize the target child tasks or blocker tasks (same importance and tag criteria apply)

### 4. Check for blockers

```bash
agkan task block list <id> --json
```

If there are incomplete tasks in `blockedBy`, do not select that task. Instead, select a different task or process the blocker task first.

### 5. Update task to in_progress

```bash
agkan task update <id> --status in_progress
```

### 5a. Inspect task body for existing Branch/PR

Before launching the sub-agent, retrieve the full task body and parse it for `Branch:` and `PR:` labels (see `agkan/SKILL.md` — Body Conventions):

```bash
agkan task get <id> --json
```

Extract any values matching these patterns from the task body:

```
Branch: <branch-name>
PR: <URL>
```

Pass these values to the sub-agent prompt (Step 6) so it can resume work on the existing branch/PR instead of creating new ones.

### 6. Implement, create PR, complete

**Use the Task tool (general-purpose sub-agent)** to implement.
Do not use `Skill("agkan-subtask")`; instead, embed the workflow steps directly in the sub-agent prompt.

> **Why embed steps instead of referencing a file path?**
> Sub-agents spawned via the Task tool start with a fresh context. When installed as a plugin, the skill files may reside at a path unknown to the sub-agent (e.g., under a plugin cache directory), so instructing the sub-agent to read a relative or installation-specific path is unreliable. Embedding the workflow steps directly in the prompt makes the instructions path-independent.

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

## Existing Branch/PR (if any)
- Branch: <existing-branch-name or "none">
- PR: <existing-PR-URL or "none">

If Branch or PR values above are set (not "none"), use them to resume work on the
existing branch and PR rather than creating new ones (as described in Step 2 below).

## Steps

Follow these steps to implement the task:

### 1. Update Task to In Progress

```bash
agkan task update <id> --status in_progress
```

### 2. Check for Existing Branch/PR

Before creating a new branch, inspect the task body for existing branch and PR
associations. Parse the "Existing Branch/PR" values provided above.

**Case A — Branch label found (not "none"):**

Check out the existing branch:

```bash
git fetch origin
git checkout <existing-branch-name>
```

Then check for conflicts with the default branch:

```bash
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
git merge-base --is-ancestor origin/$DEFAULT_BRANCH HEAD
```

If this check fails (exit code non-zero), the branch has diverged and there may be
conflicts. Surface a clear error and stop:

```
ERROR: Branch '<existing-branch-name>' has conflicts with '$DEFAULT_BRANCH'.
Please resolve the conflicts manually before resuming this task.
```

If no conflicts are detected, continue from Step 4 (skip Step 3, as the branch name
is already recorded).

**Case B — No branch label found (value is "none"):**

Create a new branch. Branch name is generated from task ID and title
(example: `feat/42-add-login-page`).

```bash
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
git fetch origin
git checkout -b <branch-name> origin/$DEFAULT_BRANCH
```

Then continue to Step 3.

### 3. Write Branch Name to Task

```bash
# First, retrieve the existing body
agkan task get <id> --json
# Write body to tmp file and update using --file to preserve newlines
cat > /tmp/agkan_body_$$.md << 'BODY'
<existing body>

Branch: <branch-name>
BODY
agkan task update <id> --file /tmp/agkan_body_$$.md
# Also store as metadata so the board detail panel can display it
agkan task meta set <id> branch <branch-name>
```

### 4. Implementation

Implement according to the task content.

Refer to /key-guidelines during implementation to maintain code quality.

### 5. Commit and Push

Stage files by specifying them explicitly. Do not use `git add -A` as it risks
including unintended files such as `.env` or credentials.

```bash
git add <file1> <file2> ...
git commit -m "<commit message>"
git push -u origin <branch-name>
```

> **Note**: Do not use `git add -A` or `git add .`. Files containing `.env`,
> `credentials.*`, or secrets may be committed unintentionally.

### 6. Create PR

If a `PR:` label was found in the task body (Step 2, Case A), skip PR creation —
the existing PR will be updated automatically when commits are pushed to the branch.

Otherwise, create a new PR:

```bash
gh pr create --title "<title>" --body "<body>"
```

### 7. Add PR Information to Task

If a `PR:` label was already present in the task body (Step 2, Case A), skip this step.

Otherwise, record the newly created PR URL:

```bash
# First, retrieve the existing body
agkan task get <id> --json
# Write body to tmp file and update using --file to preserve newlines
cat > /tmp/agkan_body_$$.md << 'BODY'
<existing body>

PR: <PR URL>
BODY
agkan task update <id> --file /tmp/agkan_body_$$.md
# Also store as metadata so the board detail panel can display it
agkan task meta set <id> pr <PR URL>
```

### 8. Update Task to Review

Only execute this step if implementation succeeded — specifically, if git push (Step 5)
and PR creation (Step 6) both completed without critical errors (permission errors, push
failures, etc.).

**If a critical error occurred** (e.g., git push failed, PR creation failed, permission
denied), do NOT update the status to review. Leave the task as `in_progress` and record
the error details in the task body:

```bash
# On error: record what went wrong in the task body (optional but recommended)
agkan task get <id> --json
# Write body to tmp file and update using --file to preserve newlines
cat > /tmp/agkan_body_$$.md << 'BODY'
<existing body>

Error: <error description>
BODY
agkan task update <id> --file /tmp/agkan_body_$$.md
# Do NOT run: agkan task update <id> --status review
```

**If implementation succeeded**, update to review:

```bash
agkan task update <id> --status review
```

Confirm the update succeeded:

```bash
agkan task get <id> --json
```

Verify that the status is `review`. If it is still `in_progress`, retry the update
command.

## Important Notes

- Do not mark task as done before PR is merged (mark as done after PR review and merge)
- **Step 8 (status → review) must only be executed when implementation succeeded** — do not update to review if a critical error occurred
- If a critical error occurs (git push failure, PR creation failure, permission error), keep the task as `in_progress` and record the error
"""
)
```

### 7. Verify task status after sub-agent completes

After the sub-agent completes, check whether the task has been moved out of `in_progress`:

```bash
agkan task get <id> --json
```

If the status is still `in_progress`, determine whether the sub-agent encountered a critical error (git push failure, PR creation failure, permission error). Check the task body for any recorded error messages.

- **If a critical error occurred**: Do NOT update to `review`. Leave the task as `in_progress` so the issue can be resolved manually.
- **If no critical error occurred** and implementation succeeded but the sub-agent forgot to update the status, update it manually:

```bash
agkan task update <id> --status review
```

### 8. Handle interruptions, then ALWAYS re-fetch and continue

**After confirming the task status**, there may be interruptions before you can proceed:

#### Interruption types and how to handle them

| Interruption | How to handle | Then... |
|---|---|---|
| IDE diagnostic (linter, type error, etc.) | Fix the issue immediately | **Resume step 8** |
| User question about the current task | Answer, then fix if needed | **Resume step 8** |
| User explicitly says "stop" / "exit" | Stop the workflow | End session |

**IDE diagnostics (e.g., `<new-diagnostics>` in system-reminder) are part of the current task's implementation — not a reason to end the workflow.** Fix them and continue.

**After handling any interruption, always ask yourself:**
> "Am I in the middle of an agkan-run workflow? If yes, go back to step 8."

Re-fetch the task list to pick up any newly added ready tasks:

```bash
agkan task list --status ready --json
```

If there are no termination instructions from the user and ready tasks exist (including newly added ones), select the next task and repeat from step 3 of the workflow.

If no ready tasks remain, end the session.

---

## Loop Structure

```
START
  ↓
git pull (default branch) & get ready tasks
  ↓
No tasks? → END SESSION
  ↓
Select highest priority task (skip will-do-later)
  ↓
Check blockers → blocked? → select different task
  ↓
Update status: in_progress
  ↓
Launch sub-agent to implement & create PR
  ↓
Sub-agent done?
  ↓
Interruption occurred? (diagnostic, user question)
  Yes → Handle it → RETURN HERE
  No  ↓
Re-fetch task list  ←──────────────────────────┐
  ↓                                              │
Ready tasks exist AND no stop instruction? ─Yes─┘
  ↓ No
END SESSION
```

**Red flags — you are breaking the loop:**
- Sub-agent completed, you fixed a diagnostic, then stopped
- Sub-agent completed, user asked a question, you answered, then stopped
- You forgot to re-fetch the task list after any action

**All of these mean: Go back to step 7. Re-fetch the task list.**

---

## Priority Determination Flow

```
Todo task list
    ↓
Sort by priority (Critical → High → Medium → Low)
    ↓
Multiple tasks with same priority?
   Yes → Sort by tag priority (bug → security → ... → docs)
   No  → Select top task
    ↓
Select 1 task and start work
```

---

## Tag Priority List

See the canonical definition in `agkan/SKILL.md` (Tag Priority section).

---

## Notes

- Always select only 1 task (do not start multiple tasks simultaneously)
- If no tasks exist, end the session
- Do not mark task as done before PR merge (mark as done after PR review and merge)
- **Never stop mid-workflow due to interruptions** — handle them and resume

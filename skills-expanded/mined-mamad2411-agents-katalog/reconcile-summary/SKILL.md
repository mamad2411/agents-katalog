---
name: reconcile-summary
description: "Review a worker session summary and reconcile tasks with implementation reality. Use after a worker completes /finish-task to sync the task board with what was actually implemented. Invoked by orchestrator sessions, or with /reconcile-summary <task-id>."
allowed-tools: Read, Bash, Glob, Grep, Edit, Write, AskUserQuestion
---

# Reconcile Session Summary

You are an orchestrating agent reviewing a completed worker session. Your job is to ensure the task board accurately reflects what was actually built, not just what was originally specified.

## `--yes` Mode (Autonomous Operation)

If `$ARGUMENTS` contains `--yes`, auto-answer ALL `AskUserQuestion` prompts:
- **Which summary to process** → "All of them" (process all unreconciled summaries sequentially)
- **Update PROJECT_SPEC.md or CLAUDE.md** → "No, task board only"
- **Copy to clipboard** → "No, skip"
- **Next action** → Skip prompt, return control to caller

Strip `--yes` from `$ARGUMENTS` before processing task IDs.

## 1. Discover Session Summaries

The command can receive input in multiple ways. Try them in order:

### Option A: Argument provided
If the user provided a task ID as argument (`$ARGUMENTS`), look for its summary:

```bash
# Find summary file for specific task
ls -lt docs/session_summaries/${ARGUMENTS}*.txt 2>/dev/null | head -1
```

### Option B: Auto-discover from docs/session_summaries/
If no argument, scan for unreconciled summaries (excludes `reconciled/` subdirectory):

```bash
# Find summary files NOT in reconciled/ subdirectory
find docs/session_summaries/ -maxdepth 1 -name "*.txt" -type f 2>/dev/null | head -10

# If Linear MCP available, check recently closed tasks
# list_issues(state=Done, limit=10, orderBy=updatedAt)
```

### Option C: User pastes summary
If no summaries found or user prefers, they can paste directly.

### Discovery Logic

1. **If `$ARGUMENTS` is a task ID**: Read that task's summary file
2. **If summaries exist**: List them and ask user which to reconcile
3. **If user pastes**: Parse the pasted content
4. **If nothing found**: Ask user to paste or provide file path

```bash
# Example: List unreconciled summaries with task IDs and timestamps
# (excludes docs/session_summaries/reconciled/)
for f in docs/session_summaries/*.txt; do
  if [ -f "$f" ]; then
    task_id=$(basename "$f" | cut -d'_' -f1)
    mod_time=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$f")
    echo "$task_id - $mod_time - $f"
  fi
done 2>/dev/null | sort -t'-' -k2 -r | head -10
```

**Note:** Summaries in `docs/session_summaries/reconciled/` have already been processed and are excluded from discovery.

If multiple summaries need reconciliation, use AskUserQuestion:

**Question:** "Found N unreconciled summaries. Which to process?"
- **Options:** List task IDs, or "All of them" / "Let me pick"
- **Header:** "Summaries"

### Parse the Summary

Once you have the summary content (from file or paste), extract:

- **Task ID** from the TASK OVERVIEW section
- **SPEC DIVERGENCES** section (critical - this tells you what changed)
- **FOLLOW-UP ISSUES CREATED** section
- **DEPENDENCIES UNBLOCKED** section
- **ARCHITECTURAL NOTES** section

## 2. Review the Original Task — With Distrust

Do NOT trust session summaries blindly. Workers may have been under context pressure. Their summaries may be incomplete, inaccurate, or optimistic.

If Linear MCP is available, call `get_issue(id=<task-id>, includeRelations=true)` to get the original task spec.

### 2a. Cross-Reference Claims Against Evidence

Extract `branch-name` from the summary's GIT ACTIVITY → Branch field. Extract `pr-number` from GIT ACTIVITY → PR field (or from the `gh pr list` output below).

For each major claim in the session summary, verify independently:

```bash
# Does the PR exist?
gh pr list --head <branch-name> --json number,state

# Do file changes match summary claims?
gh pr diff <pr-number> --stat 2>/dev/null

# Are CI checks passing?
gh pr checks <pr-number> 2>/dev/null
```

**Flag any discrepancy** between summary claims and observable evidence. If the summary says "all tests pass" but CI shows failures, note this in the reconciliation report under REMAINING CONCERNS.

Then compare the original task description against the worker's IMPLEMENTATION SUMMARY and SPEC DIVERGENCES sections.

## 3. Analyze Divergences

For each divergence documented by the worker, determine:

1. **Scope**: Does this affect only this task, or does it ripple to other tasks?
2. **Downstream impact**: Which blocked/dependent tasks need their descriptions updated?
3. **New work**: Does this divergence create new tasks that weren't anticipated?
4. **Invalidated work**: Does this make any existing tasks obsolete or redundant?

## 4. Review Related Tasks

If Linear MCP is available:
- The `get_issue` call from Step 2 already includes relations. Check the `blocks` array for tasks unblocked by this completion.
- Call `list_issues(state=Todo)` and `list_issues(state="In Progress")` to see open tasks.
- For each potentially affected task, call `get_issue(id=<affected-id>)` to review.

Ask yourself:
- Does this task's description assume something that's no longer true?
- Does the implementation change how this task should be approached?
- Are there new dependencies or constraints to document?

## 5. Update Tasks

If Linear MCP is available, update tasks to reflect reality:

### Common Updates

**Update task description:**
Call `save_issue(id=<task-id>, description="<updated description>")` or post a comment with `save_comment(issueId=<task-id>, body="Updated context from <completed-task-id>: <changes>")`

**If a task is now obsolete:**
Call `save_issue(id=<task-id>, state=Done)` + `save_comment(issueId=<task-id>, body="Obsoleted by <task-id>. <explanation>")`

**If a task needs new dependencies:**
Call `save_issue(id=<task-id>, blockedBy=[<new-dependency-id>])`

**If scope expanded or implementation discovered new work:**
Do NOT create issues directly. Collect these into the batch proposal (Step 5.5).

If Linear MCP is not available, document all updates in the reconciliation report for manual action.

## 5.5. Batch Proposal: Discovered Work

Collect all DISCOVERED WORK entries from the worker session summary (and any scope expansion items from divergence analysis above). Present them as a batch for user review:

```
## Discovered Work (from worker summaries)

Worker <task-id> reported:
1. "<title>" — Problem: ..., Approach: ..., AC: ...
2. "<title>" — Problem: ..., Approach: ..., AC: ...

---
<N> items total. Review and select:

a) Create all as Linear issues
b) Select which to create (list numbers to include, e.g., "1, 3")
c) Skip all — handle manually later
```

In `--yes` mode: auto-select option (a) to maintain autonomous execution.

For each approved item, create the issue applying the **Quality Gate** (see below). Then run **Post-Write Validation**.

If a DISCOVERED WORK entry has insufficient detail (missing Problem, Approach, or Acceptance Criteria), flag it: "Item N has insufficient detail for issue creation — skipping. Manual follow-up needed." Do not create a thin issue.

### Quality Gate for `save_issue`

Every `save_issue` call creating a new issue (no `id` parameter) must include:

**Minimum description structure:**
```markdown
## Problem
[What's wrong or what's needed — 2-3 sentences minimum]

## Approach
[How to fix/build it — specific enough for a worker to execute]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Target Files
- path/to/file.ext
```

**Required fields:** `title` (descriptive), `description` (meets structure above), `priority` (1-4), `labels` (at least one: Bug, Feature, Improvement, Refactor), `project`.

**Formatting rules:** Write actual markdown with real line breaks. Never use `\n` escape sequences in description or body fields. Do not include XML tool syntax or string delimiters in content.

### Post-Write Validation

After every `save_issue` that creates or updates a description:

1. Call `get_issue(id=<created-id>)` to read back the content
2. Check for formatting artifacts: literal `\n` or `\\n`, XML tags (`</invoke>`, `<parameter>`), trailing `")` or `')`
3. If artifacts found: rewrite with `save_issue(id=<id>, description="<corrected>")` — replace escaped newlines with actual newlines, strip artifacts

## 5.6. Update Project Description

If tasks were completed, created, or had significant status changes during this reconciliation, update the project description:

1. Get current project: `get_project(query=<project-name>)`
2. Generate a progress narrative:
   - **Completed:** What has been accomplished (list completed tasks with one-line summaries)
   - **In Progress:** What's actively being worked on
   - **Remaining:** What's left in backlog, ordered by priority
   - **Key Decisions:** Any architectural or scope decisions made during this round
3. Update: `save_project(id=<project-id>, description="<progress narrative>")`

Keep the description current — this is the entry point for understanding project state.

## 6. Post Reconciliation Comment to Completed Task

If Linear MCP is available, post a concise reconciliation summary as a comment on the **completed task's** Linear issue. This creates an audit trail visible in Linear's UI.

Call `save_comment(issueId=<task-id>, body=<comment>)` with the following format:

```
**Reconciliation Summary**

Divergences: <count> (<one-liner per divergence, or "None">)
Tasks updated: <list of task-id: brief change, or "None">
Tasks created: <list of task-id: title, or "None">
Tasks closed: <list of task-id: reason, or "None">
Remaining concerns: <brief list, or "None">
```

Keep it concise — this is a pointer for context, not the full report. Skip this step if there were zero divergences and zero task changes (nothing useful to record).

## 7. Report Reconciliation

Output a reconciliation report:

```
===============================================
RECONCILIATION REPORT
===============================================

REVIEWED TASK
-------------
ID: <task-id>
Title: <title>
Status: Closed

DIVERGENCES PROCESSED
---------------------
<For each divergence from the session summary>

1. <Divergence title>
   Action taken: <what you did - updated task X, created task Y, closed task Z>

TASKS UPDATED
-------------
<List each task that was modified>

- <task-id>: <brief description of change>
- <task-id>: <brief description of change>

TASKS CREATED (via batch approval)
-----------------------------------
<List any new tasks created from discovered work, or "None — no items approved">

- <task-id>: <title>

TASKS CLOSED
------------
<List any tasks closed as obsolete>

- <task-id>: <reason>

REMAINING CONCERNS
------------------
<Any issues that couldn't be automatically resolved, need human decision, or require discussion>

TASK BOARD STATUS
-----------------
Ready tasks: <count>
Blocked tasks: <count>
Total open: <count>

===============================================
END RECONCILIATION REPORT
===============================================
```

## 8. Update Architectural Documentation (If Needed)

If divergences represent significant architectural changes (not just implementation details), consider updating project-level documentation:

**PROJECT_SPEC.md** - Update if:
- Core architecture changed (different services, data flow, etc.)
- Technology choices changed (different libraries, frameworks)
- API contracts changed significantly
- Data models changed

**Project CLAUDE.md** - Update if:
- New patterns or conventions were established
- New commands or workflows were added
- Critical rules changed (e.g., "never do X")

```bash
# Check if these files exist
ls -la PROJECT_SPEC.md CLAUDE.md 2>/dev/null
```

Use AskUserQuestion to confirm before modifying these files:

**Question:** "Divergence '<title>' represents an architectural change. Update PROJECT_SPEC.md or CLAUDE.md?"
- **Options:** "Yes, update docs" / "No, task board only" / "Ask me about each file"

## 9. Copy Reconciliation Report (Optional)

Use AskUserQuestion to offer copying the report to clipboard:

**Question:** "Copy reconciliation report to clipboard?"
- **Options:** "Yes, copy to clipboard" / "No, skip"
- **Header:** "Clipboard"

If the user selects "Yes, copy to clipboard", copy the full reconciliation report.

## 10. Mark Summary as Reconciled

Move the processed summary file to a `reconciled/` subdirectory to prevent re-processing:

```bash
# Create reconciled directory if needed
mkdir -p docs/session_summaries/reconciled

# Move the processed summary
mv "$SUMMARY_FILE" docs/session_summaries/reconciled/

echo "Summary moved to docs/session_summaries/reconciled/"
```

This ensures the discovery step (Step 1) won't pick up already-reconciled summaries.

## 11. Prompt for Next Action

After reconciliation, ask the user:

"Reconciliation complete. What would you like to do next?"
- **Review changes** - Show the updated tasks in detail
- **Continue orchestrating** - Return to normal orchestration
- **Dispatch more workers** - Spin up workers for newly unblocked tasks
- **Reconcile another** - Process the next pending summary

---

## Important Guidelines

1. **Be thorough** - A divergence in one task often ripples to many others
2. **Preserve intent** - When updating task descriptions, keep the original goal clear
3. **Document reasoning** - Future agents need to understand why specs changed
4. **Don't over-correct** - Only update tasks that are actually affected
5. **Ask when uncertain** - If a divergence has unclear implications, ask the user
6. **Verify, don't trust** — Session summaries are self-reported. Cross-reference claims against git/CI evidence before updating the task board. (Inspired by obra/superpowers subagent distrust model)

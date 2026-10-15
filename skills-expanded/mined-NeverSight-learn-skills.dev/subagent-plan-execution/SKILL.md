---
name: subagent-plan-execution
description: Execute an existing implementation plan by dispatching fresh subagents per task, with mandatory spec-compliance and code-quality review gates. Only use this skill when explicitly invoked via /subagent-plan-execution — do NOT trigger automatically based on context or user phrasing.
---

# Subagent Plan Execution

Execute a multi-task implementation plan by dispatching each task to a fresh subagent with zero context pollution, then reviewing the result before proceeding. This keeps the orchestrator lean and catches issues early.

## Locating Reference Files

This SKILL.md lives in a skill directory. Its sibling `references/` folder contains the implementer and reviewer prompt templates. If you loaded this skill from a file path, resolve paths relative to that directory. If unsure, search your filesystem for `implementer_prompt.md` — it lives next to this file.

## Step 0: Load the Plan

If the plan already exists as a file (e.g., `plan.md`, `.agents/plans/plan.md`), read it once.

If the plan exists only in the conversation, write it to `.agents/plans/plan.md` first. Use a flexible format — the only requirement is that tasks are clearly separated and each has enough detail for someone unfamiliar with the project to implement it. Example:

```markdown
# Plan: Feature Name

## Task 1: Add user authentication
**Files:** src/auth/login.ts, src/auth/middleware.ts
**Dependencies:** none

Implement JWT-based login endpoint at POST /auth/login...

## Task 2: Protect routes
**Files:** src/middleware/guard.ts
**Dependencies:** Task 1
...
```

Read the plan once, build an internal task list, then close the file. Don't keep re-reading it.

## Step 1: Execute Each Task

Work through tasks one at a time (or in parallel if they touch different files with no dependencies). For single-task plans, just run one cycle.

For each task, do the following in order. Skipping any substep breaks the review loop — a subagent dispatched without a brief file has no spec to implement against.

### 1a. Write the Brief File

The brief file is the contract between you, the implementer, and the reviewer. Create `.agents/plans/task-N-brief.md` containing the task spec verbatim from the plan. Nothing else.

```
mkdir -p .agents/plans
cat > .agents/plans/task-N-brief.md << 'EOF'
<task spec from the plan>
EOF
```

**Verify it exists** before proceeding. If you can't write files, use your platform's Write tool. This step is not optional — without the brief file, the implementer has no spec and the reviewer has nothing to check against.

### 1b. Dispatch the Implementer

Read the template at `references/implementer_prompt.md` (in the skill directory). Fill in these placeholders:

| Placeholder | Value |
|---|---|
| `{brief_path}` | `.agents/plans/task-N-brief.md` |
| `{report_path}` | `.agents/plans/task-N-report.md` |
| `{language}` | Python, Go, TypeScript, etc. |
| `{test_dir}` | Where tests live |
| `{conventions}` | Imports, naming, error handling style — whatever matters |
| `{verify_command}` | Exact command (e.g., `go build ./... && go test ./...`) |
| `{expected_outputs}` | Files to create or modify |
| `{commit_format}` | Only if committing, e.g., `feat(task-N): message` |

Dispatch a fresh subagent with the filled-in template. Give it the project root path so it can resolve `{brief_path}`. Do not paste the full plan or spec into the dispatch prompt — that's what the brief file is for.

#### Result Handling

| Response | Action |
|---|---|
| **DONE** | Proceed to 1c. |
| **BLOCKED: \<reason\>** | Fix the blocker (add context, clarify spec, split task) and re-dispatch from 1b. Never re-dispatch without changing something. |

### 1c. Review the Implementation

First, verify the implementer's claimed outputs exist:

```
ls -la <each file in expected_outputs>
```

If any file is missing, re-dispatch with the exact path correction. Do not proceed to review.

Generate a diff package so the reviewer reads one file:

```
git diff --stat HEAD~1 > .agents/plans/review-task-N.diff
git diff -U10 HEAD~1 >> .agents/plans/review-task-N.diff
```

(Without git, collect changed file paths and their contents into `.agents/plans/review-task-N.diff`.)

Read `references/reviewer_prompt.md` (in the skill directory). Fill in:

| Placeholder | Value |
|---|---|
| `{brief_path}` | `.agents/plans/task-N-brief.md` |
| `{report_path}` | `.agents/plans/task-N-report.md` |
| `{diff_path}` | `.agents/plans/review-task-N.diff` |

Dispatch a fresh reviewer subagent. It checks spec compliance and code quality in one pass.

#### Result Handling

| Response | Action |
|---|---|
| **APPROVE** | Task complete. Move to next task or Step 2. |
| **REPROVE** | Reviewer listed issues. Fix all `MUST_FIX` items (and `SHOULD_FIX` if practical) by re-dispatching from 1b with the issue list. Generate a new diff and re-run 1c. |

If the reviewer flags something that's actually correct (compiles, tests pass, follows conventions), reject that specific feedback and proceed. Reviewers can be wrong — they lack full context.

## Step 2: Quality Gate

After all tasks pass review, run these checks from the project root:

1. **Build/compile** — `{build_command}` must succeed
2. **Tests** — `{test_command}` must pass
3. **Lint** — `{lint_command}` must be clean

If any gate fails, fix and re-run. Once all three pass, the plan is complete.

## Context Discipline

- **Pass artifacts as file paths, not pasted content.** Subagents read brief, diff, and report files directly. Never paste full specs or diffs into dispatch prompts.
- **Read only verdicts from subagent outputs.** You want APPROVE/REPROVE/DONE/BLOCKED and the issue list, not the full analysis.
- **Don't accumulate state.** After a task is approved, drop its details. Only carry forward interfaces the next task needs.
- **At ~70%+ context:** checkpoint completed tasks, finish the current one, and warn the user.

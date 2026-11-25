---
name: execute-plan
description: Systematically execute a written implementation plan task by task with verification. Use after write-plan or when you have a step-by-step plan to implement.
allowed-tools: Read Write LS Grep Bash TodoWrite TodoRead Skill
---

# Execute Plan

Systematically execute a written implementation plan, task by task, with verification at each step.

## Process

### Step 1: Load and Review the Plan

Read the plan document using `Read`. Before starting execution:
- Review the plan critically — flag any concerns
- Check that prerequisites are met (dependencies installed, files exist, etc.)
- If anything looks wrong or unclear, ask the user before proceeding

### Step 2: Create Task Checklist

Use `TodoWrite` to create a checklist from the plan's tasks. Each todo item corresponds to one task in the plan.

### Step 3: Execute Tasks

For each task in the plan:

1. **Mark in progress** — update `TodoWrite` to set the task as `in_progress`
2. **Follow steps exactly** — execute each step as written in the plan
3. **Run verifications** — execute any verification commands and check the output matches expectations
4. **Mark completed** — update `TodoWrite` to set the task as `completed`

### Step 4: Handle Blockers

When you encounter a problem, **stop and ask** — never guess or improvise:
- Missing dependencies or prerequisites
- Test failures not addressed by the plan
- Unclear or ambiguous instructions
- Verification output doesn't match expectations
- Files that don't exist or have unexpected content

Ask user to describe the blocker and ask for guidance.

### Step 5: Summarize

After all tasks are completed, provide a summary:
- What was implemented
- Which files were created or modified
- Any deviations from the plan and why
- Any follow-up items or concerns

## Rules

- **Follow the plan** — the plan was reviewed and approved. Follow it as written.
- **Don't skip verifications** — if the plan says to run a command and check output, do it.
- **Don't improvise** — if something isn't in the plan, ask before doing it.
- **Stop on failure** — if a verification fails, stop and ask rather than continuing with a broken state.
- **Commit frequently** — follow the plan's commit points. Don't batch unrelated changes.

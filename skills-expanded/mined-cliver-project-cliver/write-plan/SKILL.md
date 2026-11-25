---
name: write-plan
description: Create detailed, step-by-step implementation plans from design specs. Use after brainstorming or when you have a spec/requirements for a multi-step task.
allowed-tools: Read LS Grep Bash TodoWrite TodoRead Write Skill
---

# Write Plan

Create comprehensive implementation plans assuming the engineer has zero context for the codebase but is skilled. Document everything they need: which files to touch, what code to write, how to test, how to verify. Give the whole plan as bite-sized tasks.

## Process

### Step 1: Read the Design Spec

If coming from the brainstorm skill, read the design doc from `~/.cliver/temp/design/`. Otherwise, ask the user for the spec or requirements.

Use `Read` to load the spec. Understand the goal, architecture, and all changes before writing the plan.

### Step 2: Map the File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for.

- Each file should have one clear responsibility
- Files that change together should live together
- In existing codebases, follow established patterns
- Prefer smaller, focused files over large ones

### Step 3: Break Into Tasks

Decompose the work into tasks. Each task is one focused unit — one file or a small group of closely related files.

For each task, list concrete steps:
- Exact file paths to create or modify
- What to change (with specifics, not vague descriptions)
- Actual code to write (complete, not pseudocode)
- Commands to run for verification
- Expected output of verification commands

### Step 4: Write the Plan Document

Save the plan using `Write`:
- Path: `~/.cliver/temp/design/YYYY-MM-DD-<topic>-plan.md`

Use this structure:

```
# [Feature Name] Implementation Plan

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---

### Task 1: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py`
- Test: `tests/exact/path/to/test.py`

**Steps:**
1. [Exact action with code block]
2. [Verification command and expected output]
3. [Commit message]

### Task 2: ...
```

## Bite-Sized Granularity

Each step should be one action:
- "Write the failing test" — one step
- "Run it to make sure it fails" — one step
- "Implement the minimal code" — one step
- "Run the tests to verify" — one step
- "Commit" — one step

## No Placeholders

Every step must contain actual content. These are plan failures — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" (without showing the code)
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the content — tasks may be read independently)
- Steps that describe what to do without showing how

## Self-Review

After writing the plan, check it:

1. **Spec coverage:** Skim each requirement in the spec. Can you point to a task that implements it? List any gaps.
2. **Placeholder scan:** Search for red flags from the "No Placeholders" section. Fix them.
3. **Type consistency:** Do types, function names, and signatures match across tasks? A function called `get_items()` in Task 2 but `fetch_items()` in Task 5 is a bug.

Fix issues inline. If a spec requirement has no task, add the task.

## User Review

After writing the plan, ask the user to review it:

> "Plan written to `<path>`. Please review it and let me know if you want any changes before we start execution."

Wait for the user's response. Make changes if requested.

## Transition to Execution

Once the user approves the plan, activate the execution skill:

> "Plan approved. Now activating the execution skill to implement the plan."

Call `Skill(skill_name='execute-plan')` to continue.

## Principles

- DRY — don't repeat yourself across tasks
- YAGNI — don't plan features that aren't in the spec
- TDD — write tests before implementation where practical
- Frequent commits — each task should end with a commit

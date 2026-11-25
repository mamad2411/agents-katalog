---
name: superpowers-plan
agent_created: true
version: 1.0.0
description: Write bite-sized implementation plans with complete code, no placeholders, exact file paths and commands. This skill should be used after design is approved and before implementing any multi-step feature.
---

# Writing Implementation Plans

## Overview

Write comprehensive implementation plans that any developer can execute. Break work into bite-sized tasks (2-5 minutes each). Include exact file paths, complete code, exact commands, and expected output.

**Core principle:** A plan with placeholders is a plan that hasn't been written.

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## When to Use

Use after the design is approved (via EnterPlanMode). Do NOT use for simple single-file changes, purely conversational exploration, or configuration-only changes.

## File Structure

Before defining tasks, map out which files will be created or modified. Design units with clear boundaries and well-defined interfaces. Prefer smaller, focused files.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

## Plan Document Header

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence describing what this builds]
**Architecture:** [2-3 sentences about approach]
**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: exact/path/to/file.py
- Modify: exact/path/to/existing.py

- [ ] Step 1: Write the failing test
  [complete test code here]

- [ ] Step 2: Run test to verify it fails
  Run: pytest tests/path/test.py -v
  Expected: FAIL

- [ ] Step 3: Write minimal implementation
  [complete implementation code here]

- [ ] Step 4: Run test to verify it passes
  Run: pytest tests/path/test.py -v
  Expected: PASS

- [ ] Step 5: Commit
  git add ... && git commit -m "..."
```

## No Placeholders — The Hard Rule

These are plan failures — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" (without actual code)
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — tasks may be read out of order)
- Steps describing what to do without showing how

## Self-Review

After writing the plan:
1. Coverage check: Can you point to a task for each requirement?
2. Placeholder scan: Search for "TBD", "TODO", vague instructions
3. Type consistency: Do signatures match across tasks?

## Execution

After saving the plan, present it to the user. Track execution with TaskCreate/TaskUpdate. Execute tasks using TDD (test-first). After each task, verify before marking complete.

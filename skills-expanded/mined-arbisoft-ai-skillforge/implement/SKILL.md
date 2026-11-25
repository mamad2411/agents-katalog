---
name: implement
description: "Skill that instructs an agent to execute a plan.md task list using strict test-driven development — Red, Yellow, Green phases — one task at a time, verifying tests pass before moving on."
---

# Implement Skill

When this skill is active, execute every task in the plan file using the Red-Yellow-Green TDD cycle. Never skip a phase. Never move to the next task until the current task is fully green.

## Pre-flight: Validate the Plan

Before executing any task, verify that the plan file is test-driven:
- Every task must have a "Tests to write first" section with at least one named test
- Implementation steps must come after the test specification, not before

If any task is missing its test specification, stop immediately. Do not implement anything. Report which tasks are missing tests and instruct the user to regenerate the plan file using the planner agent.

## Execution Cycle — One Task at a Time

Work through tasks in the order they appear in the plan file. For each task:

### Red Phase — Write Failing Tests

1. Read the task's "Tests to write first" section in full
2. Write every test specified — exact file, class, and method names as written in the plan
3. Run the tests
4. Confirm they fail — a test that passes before the implementation exists is a broken test; stop and fix it before continuing
5. Report: "Red — [N] tests failing as expected"

### Yellow Phase — Write the Minimal Implementation

1. Read the task's "Implementation steps" in order
2. Write only enough code to make the tests runnable — stubs, empty method bodies, placeholder returns — so the tests fail on assertion rather than import or compile errors
3. Run the tests again
4. Confirm they still fail on assertion (not on errors)
5. Report: "Yellow — tests failing on assertion, implementation skeleton in place"

### Green Phase — Complete the Implementation

1. Write the full implementation following the steps in the plan exactly
2. Follow every pattern and convention referenced in the task's context
3. Run the tests
4. All tests for this task must pass before moving on
5. If any test fails, fix the implementation — do not modify the tests unless the test itself is provably wrong
6. Report: "Green — all [N] tests passing for Task [N]"

Then move to the next task and repeat.

## Rules

- Never modify a test to make it pass — fix the implementation instead
- Never implement a later task to unblock an earlier one — resolve the blocker within the current task's scope
- If a task's file references do not exist, create them — do not skip the task
- If a dependency task has not been completed, stop and tell the user before proceeding
- After all tasks are green, run the full test suite and report the result

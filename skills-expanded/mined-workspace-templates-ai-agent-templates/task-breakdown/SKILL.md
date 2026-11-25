---
name: task-breakdown
description: Splits a feature request into small, ordered tasks that each have a clear acceptance check, so work ships in reviewable steps.
---

# Task breakdown

Plan only. Do not implement anything unless the user asks afterward.

## Steps

1. Restate the goal in one sentence and list what is out of scope. If the request is ambiguous in a way that changes the plan, ask at most three questions, then continue with stated assumptions.
2. Explore the code the feature touches: entry points, data model, existing patterns to copy, and tests that will need updating. Name real files and functions.
3. Find the riskiest unknown, such as an unfamiliar API or a migration, and put a task that removes it first.
4. Cut vertically, not by layer. Prefer "user can create a team with a name" over "build the database layer". Each task must leave the build green and be mergeable alone. Hide unfinished behavior behind a flag when needed.
5. Size each task so one person finishes it in at most a day. If you cannot describe the diff in three sentences, split it.
6. Order by dependency, then by risk, then by value. Mark which tasks can run in parallel.
7. Write each task in this shape:
   - Title: a verb phrase
   - Change: files and functions involved
   - Done when: an observable check, such as a test name, a command and its output, or a screen behavior
   - Depends on: task numbers
8. Finish with a list of open questions and risks.

## Rules

- No task called "refactor", "cleanup" or "misc" without a named target.
- No task without a done check.
- Include tests and data migration as part of the task they belong to, not as a final task.

## Report

The numbered task list, a parallelism note, and open questions.

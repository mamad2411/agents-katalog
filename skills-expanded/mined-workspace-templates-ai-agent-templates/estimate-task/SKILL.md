---
name: estimate-task
description: Estimates a task by inspecting the code it touches, then gives an hour range with assumptions and the unknowns behind it.
disable-model-invocation: true
---

Estimate this task from the code, not from the title: $ARGUMENTS

1. Identify the likely entry points with search. List the files and functions that would change.
2. Measure the blast radius: how many callers, imports or routes use them (use grep counts), whether there are migrations, public APIs or shared components involved.
3. Check safety nets: test coverage around those files, whether CI runs them, how old and how often changed they are (`git log --since=1.year --oneline -- <path> | wc -l`).
4. Break the work into pieces: implementation, tests, migration or data work, review fixes, deploy and verification. Give each a best and worst case in hours.
5. Add the unknowns: anything you could not read, external services, missing specs, decisions owed by others.

Output: total range (for example 6 to 14 hours), confidence (low, medium or high), a table of pieces, the assumptions, and the top two things that would blow the estimate. Do not pad the number with a hidden buffer; show any buffer on its own line. Change no files.

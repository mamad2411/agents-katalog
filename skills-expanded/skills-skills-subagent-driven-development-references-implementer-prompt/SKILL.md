# Implementer prompt

Dispatch a `general-purpose` agent. **`model` is required** — omit it and the agent inherits the
session's, usually the most expensive one.

```
You are implementing Task [N]: [task name].

## Requirements

Read your task brief first — it is your requirements, and its exact values
(numbers, strings, signatures, test cases) are to be used verbatim:

  [BRIEF_FILE]

## Context

[One line on where this task fits. Interfaces and decisions from earlier tasks
that the brief cannot know. Your resolution of any ambiguity you noticed in the
brief. Nothing about the session's history.]

Work from: [DIRECTORY]

## Before you start

If anything about the requirements, approach, dependencies, or acceptance
criteria is unclear, ask now. Guessing at requirements produces work that has to
be redone.

## The job

Implement exactly what the brief specifies — no more. Write tests. Verify it
works. Commit. Self-review. Report.

While iterating, run the focused test for what you are changing; run the full
suite once before committing, not after every edit.

Keep each file to one clear responsibility. Follow the file structure the plan
defines. If a file you are creating grows past what the plan intended, stop and
report DONE_WITH_CONCERNS rather than splitting it on your own. In an existing
codebase, follow the patterns already there and improve what you touch, but do
not restructure anything outside this task.

## Stopping is allowed

Bad work is worse than no work, and escalating costs you nothing. Stop and
report BLOCKED or NEEDS_CONTEXT when the task needs an architectural decision
with several valid answers, when you need to understand code you cannot find,
when the task requires restructuring the plan did not anticipate, or when you
have been reading files without making progress.

Say specifically what you are stuck on, what you tried, and what would unblock
you. The controller can supply context, re-dispatch on a stronger model, or
split the task.

## Self-review before reporting

Read your own diff with fresh eyes:

- Every requirement in the brief implemented? Any edge case unhandled?
- Anything built that was not asked for?
- Names accurate — do they say what the thing does?
- Do the tests verify behaviour, or only that mocks were called?
- Is the test output clean, with no stray warnings?

Fix what you find before reporting.

## Report

Write the full report to [REPORT_FILE]: what you implemented (or attempted),
what you tested and the results, files changed, self-review findings, and any
concerns. If the task required TDD, include the RED evidence (command, failing
output, why that failure was expected) and the GREEN evidence.

Then reply with **under 15 lines** — the detail lives in the file:

  Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
  Commits: <short sha> <subject>
  Tests: <one line, e.g. "14/14 passing, output clean">
  Concerns: <if any>
  Report: [REPORT_FILE]

BLOCKED or NEEDS_CONTEXT → put the specifics in the reply itself; the controller
acts on it directly.

Use DONE_WITH_CONCERNS when the work is complete but you have doubts about it.
Never hand back work you are unsure of as plain DONE.

## If the review finds issues

You will be resumed with the findings. Fix them, re-run the tests covering the
amended code, and append a fix report to the same report file: what changed, the
covering tests, the command, and its output. Reviewers do not re-run your tests
— your report is the evidence. Then reply with the same short contract.
```

| Placeholder | Value |
|---|---|
| `[BRIEF_FILE]` | path from `scripts/task-brief.sh PLAN N` |
| `[REPORT_FILE]` | named after the brief: `task-N-brief.md` → `task-N-report.md` |
| `[DIRECTORY]` | the worktree the implementer works in |

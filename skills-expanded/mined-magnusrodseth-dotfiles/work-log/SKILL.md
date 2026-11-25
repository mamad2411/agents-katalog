---
name: work-log
description: Keep a compact work log of the goal, every user steer and the active work, in a file that survives compaction. Use when a task will outlast several compactions, when the user keeps steering mid-task, or when coordinating parallel agents.
---

# Work Log

Context drifts after a few compactions: the original prompt and the small steers
given along the way fade. The work log is that state, written to a file. It is a
**snapshot**: rewrite it to match the present, and keep history in git, PRs and
issues.

## Create it

1. Use the repo's existing location if it has one. Otherwise write to
   `$TMPDIR/work-log-<repo>-<topic>.md`, outside the working tree.
2. Fill **Goal** from the request: the objective and a checkable definition of
   done.
3. Give the absolute path in your reply, so the compaction summary carries it.

## Format

```md
# Work log: <goal in one line>

## Goal
<objective, then the definition of done. Change it only when the user changes the goal.>

## Steers
- <DD.MM HH:MM> <the steer, short, close to the user's words>. Affects: <goal | stream>. Status: <open | applied | superseded by #n>

## Active
- <stream>: <current state>. Next: <one step>. Owner: <you | agent name>

## Done
- <one line>. Evidence: <commit, PR, test command or path>

## Blocked
- <what is blocked>. Needs: <the smallest input that unblocks it>
```

## Keep it current

- **Steer**: add a line the moment the user gives one, and say how it relates to
  the goal and to the active stream.
- **Step finished**: move it from Active to Done in one line, with a pointer to
  its evidence.
- **After compaction**: read the log before the next action.
- **Before the final answer**: every steer is applied or superseded, and the
  definition of done holds.

Keep the whole file under about 60 lines. Each Done line points at an artifact
(commit, PR, spec, test output) instead of restating it. A failed attempt gets a
line only while it still steers the next step.

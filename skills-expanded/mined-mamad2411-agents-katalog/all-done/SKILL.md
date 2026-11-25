---
name: all-done
description: Answer a completion challenge with YES or NO backed by fresh evidence. Use when asked 'all done?' or similar completion checks.
---

# All Done?

Keith asks this a lot. It is a gate, not small talk. He wants one word first, then proof.

## The one rule

**YES only if you ran a check in THIS turn that proves it.** No fresh check means NO.

There is no third answer. "Mostly", "should be", "I believe so" are all NO.

## What to check

Run these in one parallel batch. Skip a line only when the project has no such thing.

1. **The brief.** Re-read the user's original request word for word. Count the things
   asked for. Count the things delivered. A missing item is a NO.
2. **The diff.** `git status --porcelain` plus `git diff` and `git diff --staged`.
   Committed work counts too: diff against the session base.
3. **Tests.** Run the suite. Read the exit code and the failure count.
4. **Build / lint.** Run them if the repo has them.
5. **Leftovers.** Grep the changed files for `TODO`, `FIXME`, `console.log`,
   `print(`, commented-out blocks, and stub returns.
6. **Blast radius.** Grep for callers of anything you changed. A changed signature
   with an unchanged caller is a NO.

Scale the work to the change. A one-line edit needs step 1, 2 and 5. A feature
needs all six.

## Answer format

First line is the word. Nothing else on it.

```
YES

- <check>: <the command or file> -> <the result>
- <check>: <the command or file> -> <the result>
```

```
NO

Broken: <what is wrong, in one line>
Where: <file:line>
Fix: <what it takes>
```

List every defect you found. Not the worst one. All of them.

## Rules

- Answer first, then fix every item in one pass without waiting for a go. Stop only
  when a fix is on the ASK-FIRST list in `~/.claude/CLAUDE.md`.
- Caveats are a NO. Do not soften one into a YES.
- If you cannot run a check (no test suite, no network, a tool failed), say NO and
  name the check you could not run.
- Quote real output. "Tests pass" without a number is not evidence.
- If the answer was YES, stop talking. One word and the evidence lines. No summary.

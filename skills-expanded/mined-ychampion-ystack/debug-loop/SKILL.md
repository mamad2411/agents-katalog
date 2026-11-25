---
name: debug-loop
description: >-
  One tight loop for a hard bug: reproduce it, pin it with a test that fails, narrow it by halving
  (git bisect, input halving, toggling), keep a written hypothesis log, fix the cause, keep the test as
  a guard and strip the debug noise. Use for a bug you can reproduce: "it worked yesterday", "find the
  commit that broke it", "bisect this", "this test fails and I don't know why", or a fix that didn't stick.
  For a long open-ended diagnosis (no reliable repro yet, slowdowns, intermittent failures), use
  `diagnosing-bugs`; for flaky tests, `flaky-test`.
---

# Debug loop

Hard bugs are lost by guessing. Every step here turns a guess into a run with a yes/no answer.

## When it applies

- The cause isn't obvious after reading the error and the code it points to.
- A first fix didn't hold, or the bug comes and goes.
- Something broke between two known states: a commit, a version, a config, a data set.

Skip it when the error names the line and the fix is plain. Fix that directly and run the test.

## The loop

### 1. Reproduce: one command, red

Write down the one command that shows the bug: a test, a script, a curl, a CLI call with a saved
input. Run it and see the failure yourself. It must check the user's exact symptom, not "it ran".
Make it fast and give the same answer every run: pin the clock, seed randomness, use a temp dir.

No reproduction, no theories. If you can't build one, stop and say what you tried and what you need
(logs, an input file, access to the environment where it fails).

### 2. Pin it as a test

Turn the reproduction into a test in the project's own test suite, at the lowest level that still
shows the bug. If the project has no tests, add one file using the language's built-in test runner.
Run it and confirm it fails for the right reason: read the failure message.

### 3. Narrow by halving

Cut the search space in half each step. Pick whichever axis applies:

- **History:** it fails at B and worked at some older commit A. Check out A and run your command
  first to confirm it passes. Then run `git bisect start B A` and
  `git bisect run <your command>`. The command must exit 0 on good, 1 on bad, 125 to skip a commit
  that can't be tested. Keep the command outside the repo so checkouts don't move it. If a hook or
  policy blocks `bisect run`, step through `git bisect good` / `git bisect bad` by hand.
- **Input:** a big input fails. Delete half; still fails? Keep that half. Repeat to a minimal input.
- **Code path:** comment out, stub or early-return half of the suspect steps. Toggle flags, config
  keys, dependencies (pin the old version) one at a time.
- **Environment:** works here, fails there. List every difference (versions, env vars, OS, data) and
  move them across one at a time.

### 4. Keep a hypothesis log

Before each experiment, write one line. A bisect counts as an experiment too. Keep the log in the
chat or a scratch file:

```
# | Hypothesis                       | Test                         | Result
1 | cache returns stale entry        | disable cache, rerun repro   | still fails -> not cache
2 | off-by-one in page loop at :88   | log i and len at :88         | i == len on last page -> CONFIRMED
```

One variable per experiment. A result you didn't predict is information: write it down before you
move on. Never test two ideas in one run.

### 5. Fix the cause, then prove it

Fix the confirmed cause, not the symptom. The edit that confirmed the hypothesis is not always the
right fix: if reverting a bad commit or restoring the old logic is cleaner, do that. Run the pinned
test: it now passes. Undo the fix once and watch the test fail, so you know it guards this exact
bug: save it with `git diff > <scratch>/fix.patch`, revert the file, run, then
`git apply <scratch>/fix.patch`. Then run the wider suite, if there is one.

### 6. Clean up

Remove every debug print, temporary log, stub, commented-out block and scratch file you added.
Run `git bisect reset` if you bisected. Check `git status` and `git diff`: only the fix and the
guard test remain (a new test file shows in `git status`, not in `git diff`).

## Report

```
Symptom: <one line>   Repro: <command>
Cause: <one or two lines, file:line>
Fix: <what changed>   Guard: <test name(s)> (fail without the fix, pass with it)
Log: <the hypothesis table>
```

## Rules

- No fix before a red reproduction.
- One change per experiment; write the hypothesis before running it.
- If three hypotheses in a row are wrong, step back to step 3 and halve on a different axis.
- A bug that "went away" without a confirmed cause is not fixed. Say so.

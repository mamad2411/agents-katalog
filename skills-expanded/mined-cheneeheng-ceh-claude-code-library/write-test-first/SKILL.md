---
name: write-test-first
description: >-
  Load this skill when about to write code that adds or changes behavior, whether or not tests were
  asked for: red, green, refactor, failing run seen first. Trigger on "implement", "add a feature",
  "build this", "TDD". Not for bug fixes (use ceh-testing:test-a-bug-fix).
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Write Test First

No production code without a failing test that asks for it. Every slice of new behavior goes red,
then green, then refactor, and the task is done when every slice has a test that was seen failing
before its code existed and passes now.

## What waits for a request

Writing and running the tests that prove the change is part of the change, so the procedure below
applies without being asked, on every task that adds behavior. Only a slow or paid run waits for a
request: the full suite, coverage, mutation testing, or repeated passes over the whole suite. When
one of those would help and was not requested, name the command and what it would reveal, and
state what stays unverified.

## Procedure

1. **Cut the task into slices.** One slice is one behavior a caller can observe, stated in one
   sentence: "`parse_duration('1h30m')` returns 90 minutes". Order them so each builds on the
   last. Choose the inputs for each with `ceh-testing:design-test-cases`, whose "Before the first
   test" rules (name the seam, call it the way users do, no tautological tests) apply to every
   test here.
2. **Red.** Write the test for the next slice only. If the function does not exist yet, add its
   signature with a body that raises "not implemented", so the test fails on its assertion and not
   on an import error. Run the test and read the failure: it must fail because the behavior is
   missing. A test that fails for any other reason is broken, not red.
3. **Green.** Write the least code that passes this test, then run it and every test file the
   change touches. Code the test does not demand waits for the slice whose test does.
4. **Refactor.** With everything green, remove duplication and fix names in both the code and the
   test, then rerun the same tests. A refactor that needs a test edited changed behavior, so undo it
   or give that behavior its own slice.
5. **Repeat** from step 2 until every slice is green, then hand over with the Output below.

## Rules

- **Code written before its test gets the test run against its absence.** Stash or comment out the
  code, see the new test fail, then restore it. A test written after the code is shaped by it and
  can pass on a broken version too.
- **One failing test at a time.** Two red tests mean two slices in flight, and the code that turns
  one green can hide the other.
- **Never weaken a test to get green.** Do not loosen an assertion, skip or delete a test, or change
  an expected value to match what the code returns, because a test bent to the code proves nothing.
  When a test is genuinely wrong, fix it as its own change, record why in the decision log, and
  list it in the hand-over.
- **Every feature gets at least one integration test** on its main path through the real
  components it touches (another module, the database, a test server), not only tests of its
  parts. New code is integrated as it lands, and the seams are where it breaks. Fake only what is
  slow, paid, or outside the process.
- **Skip test-first only for what has no behavior to assert:** docs, a config value, a rename, or
  a spike the user called throwaway. Say `skip: <reason>` in the hand-over rather than skipping
  silently.
- **No test runner in the project means stop and say so,** and do not add a framework, since a
  new dependency waits for the user. Prove the slice with one runnable check (an `assert` script)
  in the meantime.

## Output

For each slice, in the hand-over:

```markdown
- `<test name>`: red `<the assertion failure line seen before the code>`, now green.
  protects: <behavior>; fails_when: <what breaking change turns it red>; why_new: <the gap it fills>
```

Then name what stayed unrun, such as the full suite, with the command that runs it, and list any
`skip: <reason>` lines and any `test changed: <test name>: <reason>` lines.

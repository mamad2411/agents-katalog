---
name: test-a-bug-fix
description: >-
  Load this skill when a bug, crash, or regression is being fixed, before writing the fix: the
  smallest failing test first, proven red without the fix. Trigger on "fix this bug", fixing a
  product/fixes/ record, a stack trace, a bug-fix PR with no test, or a first test for a
  reported bug.
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires the git CLI on PATH and a git working tree, since bisection runs `git bisect run`, plus
  the target project's own test runner (`pytest` via `uv run`, or `vitest` via `bun`) as the
  reproducer must be runnable at every commit in the range. Neither runner is assumed installed.
license: Apache-2.0
---

# Test a Bug Fix

A bug is proof that a test was missing. The fix is the cheap half; the test that would have caught
it is the deliverable. Write it **first** — a test written after the fix is written against the new
code, not against the bug, and routinely passes on the broken version too.

The task is done when the reproducer failed with the bug's symptom before the fix, passes with it,
fails again with the fix removed, and ships in the same commit as the fix.

## What waits for a request

Writing and running the tests that prove the fix is part of the fix, so the procedure below applies
without being asked: the reproducer, the stash check, the sibling cases, and a bisect on the
reproducer. Only a slow or paid run waits for a request: the full suite, coverage, mutation testing,
or repeated passes over the whole suite. When one of those would help and was not requested, name
the command and what it would reveal, and state what stays unverified.

## Procedure

### 1. Reproduce in a test before touching source

Smallest input that triggers it. No fix on disk yet.

```python
def test_parse_duration_rejects_bare_number():
    with pytest.raises(ValueError):
        parse_duration("30")  # bug: silently returned timedelta(seconds=30)
```

Put it at the **lowest level that reproduces it** — unit if a unit reproduces it, integration only
if the bug lives in the interaction. If it only reproduces end-to-end, say so: that usually means
the unit boundary is in the wrong place, and it is worth reporting even if you do not move it.

At that level, call the code the way its callers do, through the public function or endpoint, and
assert a literal expected value. A reproducer aimed at a private helper can go green while the
caller still sees the bug.

### 2. Run it and read the failure

It must fail, **and fail with the bug's actual symptom**. A test that errors on a typo, a missing
fixture, or an import is not a reproduction — it is a broken test that happens to be red.

If it passes: you have not reproduced the bug. Do not proceed. Your model of the cause is wrong,
the input is not the triggering one, or the bug needs state the test does not set up.

### 3. Fix the source

Minimal change that turns the test green. Fix only what the reproducer covers.

### 4. Prove the test is coupled to the fix

The step that gets skipped, and the only one that proves the test has value:

```bash
git stash              # remove the fix, keep the test
<run the test>         # MUST fail
git stash pop
```

Green with the fix removed means the test does not actually detect the bug — it asserts something
that was already true. Rewrite it.

### 5. Generalize one step, then stop

The reported input is one member of a class. Add the siblings from the same class — if `"30"`
failed, so will `""`, `"abc"`, `"30x"`, `"-5m"`. One test per distinct class, not per value; see
`design-test-cases` for how to draw the classes.

Stop there. A bug fix is not a licence to test the whole module.

### 6. Ship the test with the fix

Same commit. A bug-fix commit with no test is incomplete — flag it in review.

In the hand-over, give the reproducer and each sibling a value line: `<test> — protects:
<behavior>; fails_when: <the defect returns>; why_new: <why no existing test caught it>`. The
reproducer's `why_new` is the gap that let the bug ship.

The same commit carries the fix record, `product/fixes/<slug>.md`, in the format in
`references/fix-record-format.md`, when the cause is in this repo's code or config. Look for an
uncommitted record with `status: diagnosed` (`git status --porcelain product/fixes/`), which
`ceh-coding-conduct:find-root-cause` leaves: fill its Fix section with the value lines and set
`status: fixed`. With none, create one with `status: fixed`, the reproducer as the Symptom, the
cause as known from the report, and `plan:` set from the fixed `file:line` as the format says. The
commit says what changed, and the record keeps why, for whoever touches this code next.

### When it used to work — bisect on the reproducer

A reproducer is not only a test; it is a decision procedure. If the behavior was correct at some
earlier point, do not read the diff hoping to spot the cause — let git find the commit:

```bash
git bisect start HEAD <last-known-good-tag-or-sha>
git bisect run pytest tests/unit/test_parse_duration.py::test_parse_duration_rejects_bare_number
git bisect reset
```

`git bisect run` needs an exit code, so the reproducer must be runnable at every commit in the
range — keep it in a file the bisect does not check out, or pass it via `--rootdir` / a stash-free
copy. Bisecting on a manual "does it look wrong" judgement instead of a scripted test is where this
technique goes wrong: dozens of steps, each one a chance to mark a commit incorrectly.

The commit it names is where the behavior changed, which is not always where the bug is — a commit
can expose a latent defect written months earlier. Fix the defect, not the commit.

Two cases that need care: if the range spans a dependency or lockfile change, add `uv sync` (or the
equivalent) to the run command, otherwise every commit is tested against today's dependencies; and
mark commits that cannot build with `git bisect skip` rather than guessing good or bad.

### When it will not reproduce deterministically

Timing, ordering, concurrency, and environment bugs often will not fail on demand. Do not give up
and ship untested — instead:

- Run the candidate reproducer in a loop (`pytest --count=50`, `vitest --repeat 50`) or under
  randomized order/seed. Intermittent red is still a reproduction.
- Force the race directly rather than waiting for it: inject the delay, fire the two calls in
  parallel, or call the operation twice. See `close-test-risk-gaps` for the concurrency and
  idempotency recipes.
- If it still will not reproduce, say so explicitly in the summary, ship the fix with the assertion
  you _can_ make, and name what remains unverified. Never claim a fix is tested when it is not.

## Rules

### Naming

Name the test after the **behavior that was wrong**, not the ticket or the fix.

| Bad                   | Good                                           |
| --------------------- | ---------------------------------------------- |
| `test_fix_1234`       | `test_parse_duration_rejects_bare_number`      |
| `test_bug_regression` | `test_refund_of_zero_leaves_balance_unchanged` |
| `test_null_check`     | `test_lookup_returns_none_for_unknown_key`     |

The name is what a future reader sees when the test breaks. `test_fix_1234` tells them nothing and
invites deletion.

### Anti-patterns to refuse

- **Fix first, test after.** The test gets shaped by the code in front of you. If the fix is already
  written, stash it and run the new test against the broken version before you trust it.
- **Asserting on the fix's internals.** Assert the wrong behavior is gone, not that a specific guard
  clause or new helper ran. The fix should be replaceable without touching the test.
- **Deleting the reproducer once green.** It is now the regression test. It stays.
- **Widening an existing test instead of adding one.** The new case gets buried and the failure
  message stops naming the bug.
- **Asserting only that no exception was raised.** Assert the value.

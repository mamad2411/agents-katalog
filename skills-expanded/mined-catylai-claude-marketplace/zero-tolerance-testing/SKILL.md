---
name: zero-tolerance-testing
description: "Use before declaring a task complete or opening a pull request, and whenever a check fails. The done-gate: every test, linter, formatter and hook passes with zero errors and zero warnings, with no suppression or bypass. Not for test structure (use test-structure)."
license: MIT
---

# Zero-tolerance done-gate

Work is done when every check the repo runs passes with zero errors and zero warnings, and nothing
was suppressed to get there. A suppressed check is worse than a failing one: the failure tells you
something is wrong, the suppression looks healthy while telling you nothing.

## The gate

1. Read the CI pipeline definition to find the authoritative list of checks. Every check CI runs
   belongs in the local gate.
2. Run each one: the hook runner over all files, lint, format check, typecheck, unit tests, and
   integration tests where they exist.
3. Fix what fails, then rerun the whole gate, not only the check that failed, since a fix often
   breaks a neighbour. Repeat until every check exits 0 with no warnings.
4. Fix pre-existing failures too. When one is genuinely out of scope, fix it anyway or stop and tell
   the user, naming the check; leaving a red check for the next person is how suites rot.

If a check cannot run (tool missing, service unavailable, permission denied), report it as not run,
with the reason. Never report a check you did not run as passing.

## Bypasses that do not count as passing

| Bypass | Why it fails the gate |
| --- | --- |
| `git commit --no-verify` | Skips every hook at once |
| A skip or `xfail` marker added to get green | Hides a broken test |
| Commenting out or loosening an assertion | Leaves a test that cannot fail |
| Lowering a coverage or lint threshold | Moves the floor instead of meeting it |
| `--disable-warnings`, `-W ignore` | Hides the warnings the gate counts |
| `continue-on-error`, `allow_failure` in CI | Makes the failure invisible |
| <code>\|\| true</code> on a gate command | Masks a non-zero exit |
| Bare `# noqa`, `# type: ignore`, `eslint-disable` with no rule and no reason | Silences everything on the line |
| Renaming an unused result to `_` without asking why it is unused | Often hides a dropped error |

## When a suppression is legitimate

A genuine false positive may be suppressed once you have read the rule's documentation and
confirmed the finding is wrong. Suppress that one rule code, at the narrowest scope, with the reason
on the same line:

```python
data = pickle.loads(blob)  # noqa: S301 -- blob is produced by our own signed cache writer
```

When a formatter and a linter fight over the same lines, keep one authoritative formatter per
language and disable the conflicting lint rules, rather than suppressing line by line.

<example>
Lint output: `src/handlers/user.py:34:5: F841 Local variable `result` is assigned to but never used`

Not a fix: adding `# noqa: F841`.
The fix: read why the result is unused. It is usually a dropped error or a forgotten branch; use the
value, or remove the call if it truly has no effect.
</example>

<example>
A test fails intermittently in CI, and the tempting change is `@pytest.mark.skip(reason="flaky")`.

The fix: find the nondeterminism. Either the test has a race (fix the test) or the code under test
is nondeterministic (that is the bug). Slow tests get faster (parallelize, replace sleeps with
condition waits, move integration work out of the unit tier), not skipped.
</example>

<example>
The commit-msg hook rejects "added search feature".

The fix: rewrite the message to the repo's format (see `commit-standards`) and commit again with the
hook running.
</example>

## Verify

Before saying the work is done, state the result of each gate check:

```
hooks (all files)   passed | failed | not run: <reason>
lint                passed | ...
format check        passed | ...
typecheck           passed | ...
unit tests          passed | ...
integration tests   passed | ... | none exist
new skips or suppressions in this change: none | <list, each with its written reason>
```

Without a checkout (web), you cannot run the gate: review pasted output against the table above and
tell the user which checks still need running.

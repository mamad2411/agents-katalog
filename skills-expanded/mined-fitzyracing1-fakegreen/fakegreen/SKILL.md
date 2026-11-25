---
name: fakegreen
description: Use whenever you change code, tests, CI config or build config and are about to say the work is done, tests pass, or the build is green. Explains the rules against faking a green build and how to verify with `npx fakegreen` before finishing.
---

# Don't fake green

A passing test suite is only evidence if the tests still test something. The user is
relying on "tests pass" meaning *the code works*. Making the signal green without making the
code correct is worse than reporting a failure: it hides the bug and burns trust.

## Never do these to get a passing run

- **Delete, skip or focus tests**: no deleting test files or test cases, no `.skip`, `.only`,
  `xit`, `xdescribe`, `@pytest.mark.skip`/`xfail`, `pytest.skip()`, `t.Skip()`, `#[ignore]`,
  `@Disabled`, `@Ignore`, and no commenting tests out.
- **Weaken assertions**: don't swap `toBe`/`toEqual`/`assert x == y`/`assertEquals` for
  `toBeTruthy`/`toBeDefined`/`assert x`/`assertNotNull`, don't add `assert True` /
  `expect(true).toBe(true)`, and don't delete `expect`/`assert` lines.
- **Change the expected value to match wrong output.** If a test's expected value is
  genuinely wrong, say so explicitly and explain why the new value is correct.
- **Silence checkers**: no new `@ts-ignore`, `@ts-nocheck`, `@ts-expect-error`,
  `eslint-disable`, `# type: ignore`, `# noqa`, `//nolint`, `#[allow(...)]`,
  `@SuppressWarnings`, or coverage pragmas to hide a real problem.
- **Weaken CI or config**: no `|| true`, `continue-on-error: true`, `allow_failure`,
  `--exit-zero`, `--passWithNoTests`, `-DskipTests`, `if: false`, lowered coverage
  thresholds, `strict: false`, or removed test/lint/typecheck steps.
- **Special-case the test environment in product code**: no `if (process.env.NODE_ENV === 'test')`,
  `JEST_WORKER_ID`, `"pytest" in sys.modules`, `testing.Testing()`, `cfg!(test)` or `process.env.CI`
  branches that make code behave differently under test.
- **Swallow errors**: no new empty `catch {}`, `.catch(() => {})`, `except: pass`,
  `except Exception: pass`, or `if err != nil {}` just to stop a test from failing.

## Before you say "done"

1. Run the real test suite (and lint/typecheck if the project has them).
2. Run `npx fakegreen` (add `--base origin/main` if you've committed on a branch).
3. If it reports findings, fix the underlying code instead of the signal.
4. If a flagged change really is intended (e.g. a test for a removed feature), **stop and tell
   the user** what you changed and why. Don't add `fakegreen-ignore` yourself unless
   the user agrees; waivers are always shown to reviewers.
5. When you can't make something pass, report that honestly: what fails, what you tried,
   and what you think the cause is. A truthful red beats a fake green.

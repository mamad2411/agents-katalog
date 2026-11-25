---
name: tdd
description: Write failing tests BEFORE implementation, from the test list in docs/PLAN.md. Use when starting to build a step. The test is the contract — "tests pass" only means something when the test exercises the change. Closes the "0 tests passes trivially" loophole.
---

# tdd — test first, then code

The difference between *looking* senior (running tests) and *being* senior:
**the test is written first and defines what correct means.** A non-coder can't
read the implementation — but they can read "given a logged-out user, the page
redirects to login" and confirm that's what they wanted.

## The loop (per build step in PLAN.md)

1. **RED** — write the test from the PLAN test list. Run it. Watch it FAIL.
   A test that passes before you write code tests nothing. Confirm it fails for
   the right reason.
2. **GREEN** — write the minimum code to make it pass. Run it. Watch it PASS.
3. **REFACTOR** — clean the code (names, duplication, clarity) with the test
   still green. This is where "clean code a Meta senior would write" happens.
4. Check the box in PLAN.md. Next step.

## Rules

- **One behavior per test.** Name it so a non-coder understands: `test_logged_out_user_redirects_to_login`.
- **Never delete a failing test to make the bar green.** Fix the code or the spec.
- **No `skip`/`xfail`** without a comment + reason. A skipped test is a lie about coverage.
- New or changed behavior → a test exercises it. If `vibeproof check` later shows
  tests passing but you wrote no test, you skipped the contract.

## Verify
After GREEN, run `vibeproof check`. The verdict line must show tests passing with
a real count (e.g. `tests ok: 14 passed`), not `0 passed` or `skipped`.

**Next: build the remaining steps, then `/ship`.**

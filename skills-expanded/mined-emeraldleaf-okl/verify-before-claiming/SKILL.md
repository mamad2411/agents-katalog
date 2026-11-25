---
name: verify-before-claiming
description: Use before stating that work is done, a test passes, a build is green, a bug is fixed, a file exists, or any factual claim about the state of the code or the world. Requires running the check and reading its real output before asserting the result — evidence precedes assertion, always.
---

# Verify before claiming

A claim about state — "the tests pass," "the file is created," "the endpoint returns
404," "19 tests green" — is only worth as much as the check behind it. Stating a result
you *expect* as if it were a result you *observed* is the single most common way
AI-assisted work goes fast, fluent, plausible, and wrong.

This skill has one rule: **run the check, read the output, then make the claim — in that
order.** If you have not run the check this turn, you do not have the result; you have a
guess. Say "I expect" for a guess and "I confirmed" only for an observation.

## When this fires

- About to write "done", "fixed", "passing", "green", "works", "created", "verified".
- About to put a count, a status, or a value into prose, a commit message, a README, a
  PR description, or a report.
- About to tell a human that a thing is true about the code or the system.

## The procedure

1. **Name the check.** What single command or observation would make this claim true or
   false? (`pytest -q`, `ls path`, `curl -s -o /dev/null -w '%{http_code}'`, `git status`.)
2. **Run it this turn.** Not "I ran it earlier" — state drifts; a file moved, a kernel
   reset, an install got lost. Re-run it now.
3. **Read the real output.** The exit code and the actual lines — not the first line, not
   what you assume follows.
4. **Claim only what the output shows.** "18 passed, 1 skipped" — not "all green." If the
   output surprises you, the output wins; investigate before you claim.
5. **If you cannot run the check, say so.** "I could not run the suite in this
   environment, so I have not confirmed the count" is a true statement. "Tests pass" when
   you didn't run them is not.

## Anti-patterns this exists to stop

- **Reciting a remembered number.** "19 passing tests" carried from three turns ago, when
  the suite was never run this session (or was, and now one fails). Re-run; report today's
  result.
- **Reporting the expected instead of the observed.** Writing the result the code *should*
  produce as the result it *did* produce. These diverge exactly when it matters.
- **"Ran it" ≠ "passed it".** A command that executed is not a command that succeeded.
  Check the exit code, not just that it ran.
- **Success by absence.** "No errors shown" is not "it worked" — a check that did not run
  produces no errors either. Absence of a failure signal and presence of a success signal
  are different things (see also: the knowledge layer's fail-closed rule).

## The link to the rest of the method

This is the personal-discipline version of what the mechanical gates enforce at CI time
and what `okl check` enforces at task time: **a claim with no check behind it is
documentation, not verification.** When a verification you skipped later turns into a
defect, that defect is worth encoding (`okl record`) so the next task is warned.

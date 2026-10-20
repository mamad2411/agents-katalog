---
name: honest-completion
description: Use when about to report a task done — don't claim success after a step failed; blocked/needs-input is the honest call.
metadata:
  added: 2026-06-16
  last_reviewed: 2026-06-16
  type: core
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-06-16"
  related:
    [
      tdd,
      debugging,
      finishing-a-development-branch,
      code-review,
      using-devkit,
      subagent-driven-development,
      verify-before-asserting,
    ]
  owns: honest-completion
---

# Honest completion

You hit a wall — not logged in, build failing, a command errored — and the pull is to round it up to "done." Don't. Your own "I'm done" judgment is the thing that fails here; this skill is the check on it.

**Core principle:** internal consistency is not correctness. A clean diff, a plausible plan, "it should work" — none are evidence. Run the load-bearing step and read the result before claiming it works (see `using-devkit`).

## The iron law

```
A STEP THAT FAILED OR NEVER RAN IS NEVER "DONE"
```

If the build didn't pass, the tests didn't run, the login didn't succeed, or the command errored, the task is not done. Reporting "done" anyway is the failure — not the wall.

## Wall → honest outcome

| You hit                                       | It is NOT | The honest report                                               |
| --------------------------------------------- | --------- | --------------------------------------------------------------- |
| Not logged in / auth / access you can't grant | done      | **needs-input** — say exactly what login or permission you need |
| Build or compile failing                      | done      | **blocked / not-done** — fix and re-verify, or report the error |
| Tests failing (or never run)                  | done      | not-done — make them pass and watch them, or name which fail    |
| Command errored / non-zero exit               | done      | investigate the error; don't paper over it                      |
| A decision only the user can make             | done      | needs-input — state the options and ask                         |

`needs-input` and `blocked` are accepted, honest outcomes. They are not failure. Grinding out a fake "done" is.

## Verify by observing

Before you report success, re-run the thing that matters and read the output:

- Claimed the build is fixed? Run it; confirm a zero exit and clean output.
- Claimed a test passes? Watch it pass — see `tdd` (watch RED, then GREEN).
- Claimed the service is up / you're authenticated? Hit it and read the response.

"Should pass" is not "passed." Re-run, don't assume. After a merge, re-verify on the merged result (`finishing-a-development-branch`).

## State the real status, with evidence

Report exactly one, and name the evidence:

- **verified-done** — ran it, observed it work. Say what you ran.
- **blocked** — what's blocking, and what you've already ruled out.
- **needs-input** — the one thing only the user can unblock.
- **failed** — it can't be done as framed; why.

This mirrors the four-state implementer contract in `subagent-driven-development` (DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED) — never a vague "done."

## Red-flag rationalizations

Each is the wall in disguise. Stop, then verify or report honestly:

- "Should work" / "probably fine" / "looks correct"
- "Done (couldn't test it)" — then it isn't done; it's needs-input or blocked
- "Skipped the failing test to move on"
- "Fell back to a mock / stub" in production code
- A `try/except` or `catch` that swallows the error so the run looks clean (the silent-failure-hunter agent exists to catch exactly this)
- "I'll fix it later" stated as if the task is complete now

## Enforcement

The `verify-before-stop` hook enforces this at stop-time: when this turn's tool output shows a failure signature (auth, build/test failure, command-not-found, non-zero exit) and you try to end, it blocks once and asks you to re-verify or report honestly. The hook catches the obvious walls; this skill is the discipline that generalizes to the ones a regex can't match.

For verifying references _before_ you write them — mid-turn, not at stop-time — see `verify-before-asserting`.

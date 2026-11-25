---
name: show-your-work
description: Use before telling the user that work is done, a bug is fixed, tests pass, the build succeeds or something works. Back each claim with the command you ran after your last edit and the output line that proves it, keep exit statuses honest, and say plainly what you did not check.
---

# Show your work

The user cannot see your terminal. When you say "done", your word is all they
get, so show the work behind it. **No claim without the check that backs it.**

The evidence for a claim is a command you ran **after your last edit**, plus
the line of its output that shows the result.

| You want to say | Show |
|---|---|
| "tests pass" | the test command, and its summary line: `Tests: 212 passed, 212 total` |
| "it builds", "no type errors" | the build or type-check command, and its last line |
| "it works", "fixed" | the command that exercises the change (a test, a request, running the script) and what it printed |
| "I ran the tests" | that command, in this session, after your last edit |

## Before you claim anything

1. **Edited since your last run? Run it again.** Output from before your last
   edit describes code that no longer exists.
2. **Run the project's whole check.** Find it in package.json scripts, the
   Makefile, the CI workflow or CONTRIBUTING. Do not run one test file and
   report it as "the tests". If you ran only part, say which part.
3. **Keep the exit status.** `npm test | tail -20` exits 0 even when tests fail,
   and so do `|| true` and `; echo done`. For less output, use the runner's own
   quiet flag (`-q`, `--silent`, `--reporter=dot`) or `set -o pipefail`.
4. **Read the result, not just that it finished.** Completed is not passed.
   Find the failure count.
5. **Zero tests is not a pass.** "no tests ran", "collected 0 items", "0
   passing" and "# tests 0" are failures to test. A skipped test is not a pass
   either.
6. **Never weaken, skip or delete a test, or loosen an assertion, to get
   green.** If you changed a test, say which one and why.
7. **If you cannot run it, say so.** No network, no device, a missing service
   or credentials: name what stopped you. Do not predict what it would print.

## How to report

End your final message with this block:

```
Checked:
- `npm test` → Tests: 212 passed, 212 total
- `curl -s localhost:3000/health` → {"ok":true}
Not checked: the Safari date picker (no browser here).
```

- Quote the output line. Do not paraphrase it.
- One line per check, and only commands you actually ran, after your last edit.
- Always include `Not checked:`. If you checked everything you claimed, write
  `Not checked: nothing`.
- Do not write "should work now" or "should pass". Either you ran it, or it is
  not checked.

## Example

Without the work shown:

> I've fixed the date parsing bug and all tests should pass now! Let me know if
> you need anything else.

With it:

> Fixed ISO week parsing in `parseDate` (src/date.ts:41): week 53 now rolls into
> the next year.
>
> Checked:
> - `npm test` → Tests: 212 passed, 212 total
>
> Not checked: Safari's date input (no browser in this environment).

## When there is nothing to run

A question, a plan or a docs-only change needs no evidence. Just do not claim
a check you did not do.

In Claude Code, the show-your-work plugin also checks your final message
against the session log. If a claim has nothing behind it, you will be stopped
once and told what is missing: run the check, or correct the claim.

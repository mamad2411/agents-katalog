---
name: senior-finish
description: Use right before saying a substantive change is done, fixed, passing or ready, and before committing, opening a pull request or handing it off. Not for low-risk edits such as copy, labels, comments or an obvious one-file fix, where running the affected tests is the whole proof. Renaming or reshaping a field, key or type that other modules or saved data read is not low risk.
---

# Finish / Ship Gate

**Core rule:** do not call it done until the proof ran in this session and you read its result.

## 1. Re-read the goal

List the acceptance criteria that should now be true, in terms of user- or system-visible outcomes, not implementation steps. If a plan was written before the first edit, use its criteria and failure cases, and report any planned step that was not done or was changed.

## 2. Inspect the final change set

Check for unrelated edits, accidental generated files, debug statements, new TODO/FIXME, dependency changes, and migrations or configuration that need special handling. `senior risk --base <base>` lists everything since the branch started.

## 3. Run the proof

- `senior finish` (or `senior finish --json`) runs the standard baseline: the package scripts (typecheck, lint, test, build) and the Python, Go and Rust checks of the projects you changed. It shows how many tests ran; a test command that ran none is `SKIP`, not a pass. `--record` keeps the result in `.senior/evidence/`.
- Add task-specific evidence the baseline cannot give: the original bug reproduction, a browser flow, an API call, a migration dry run, a security check, a benchmark.
- For a bug fix, the regression test must have been seen failing without the fix: `senior prove --regression --test "<command>" --expect-failure "<regex matching the original symptom>"` gives a `PROVEN` / `NOT PROVEN` verdict with evidence. Report `NOT PROVEN (test-misses-bug)` as a gap, not as a pass. The failure without the fix must show the original symptom; a failure from setup, imports or syntax is not proof.
- Read the output itself: exit code, number of failures, warnings. A summary from a subagent or an earlier run is not proof.

## 4. Name what would still make it wrong

Passing checks show the cases they cover. Before choosing a status, name the two most likely ways the change is still wrong: a case the tests do not reach, a caller or copy you did not update, an environment difference (timezone, OS, a fresh database), behavior the change removed. For each, give the evidence that rules it out — a command and its result, or the code that handles it.

One you cannot rule out is residual risk or a reason for **NOT PROVEN**, not a footnote to **READY**.

## 5. Apply the risk gate

High-risk work is not ready because unit tests pass; it also needs review and a rollback or recovery answer. Destructive or external steps still need the user's approval.

## 6. Report with explicit states

- `PASS` — ran and succeeded;
- `FAIL` — ran and failed;
- `SKIP` — not available or intentionally not run;
- `BLOCKED` — an external condition or approval prevents it.

Never report a `SKIP` as a pass.

## Words that signal an unproven claim

"should work", "probably", "looks good", "seems fixed", "all set" — and any of them before a check ran in this session. Replace them with the check and its result ("`npm test`: 34 passed, 0 failed").

| If you notice yourself thinking… | Do this instead |
|---|---|
| "I ran it a few edits ago" | Run it again on the final state |
| "The subagent said everything passed" | Check the diff and run the proof yourself |
| "Lint passed, so it builds" | Run the build; each check proves only its own thing |
| "There are no tests, so there's nothing to run" | Report `SKIP` and give another form of evidence |

## Ship status

Return exactly one:

- **READY** — the acceptance criteria are supported by evidence and no blocker remains;
- **READY WITH RESIDUAL RISK** — no blocker, but a named risk is accepted and visible;
- **NOT PROVEN** — the implementation may be complete, but the evidence is insufficient;
- **BLOCKED** — completion depends on an unresolved external condition or approval.

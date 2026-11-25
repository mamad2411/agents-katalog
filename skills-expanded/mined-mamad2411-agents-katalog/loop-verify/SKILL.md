---
name: loop-verify
description: Evidence-before-done gate. Use before claiming any task complete, fixed, or working — run the real check, read the output, then claim; also use when reporting the status of tests, builds, or deploys.
---

# Verification Loop

"Looks done" is the weakest signal in agentic work: code that compiles, a diff that
reads right, a test suite remembered as green — none of these are evidence. This loop
converts every completion claim into a claim backed by a fresh observation of the real
system.

## When to reach for this

- About to say "done", "fixed", "works", "passing", or "deployed"
- Reporting the result of a test run, build, migration, or deploy
- Handing work off for review or to another agent
- A checklist item is about to be ticked

## Iron law

**No completion claim without fresh evidence from the real system.** If the check was
not run *after* the last change, it is not evidence — it is memory.

## The loop

1. **Name the check** that would prove the claim: a test command, an endpoint hit, a
   UI flow driven end-to-end, a log line appearing. If no such check exists, build one
   first — or downgrade the claim to "written, not verified" and say so.
2. **Run it against the real system** — the actual app, database, or pipeline. A toy
   reproduction verifies the toy.
3. **Read the full output.** Exit code 0 with 12 skipped tests is not a pass. Count
   pass/fail; the pass/fail count is the most reliable single signal.
4. **Compare observed behavior to the claim** — the specific behavior that changed, not
   just "no errors".
5. **Claim with the evidence attached**: the command, the count, the observed output.

Escalation ladder when prompt-level discipline isn't enough (rising cost, rising
certainty): check named in the task → check re-run every turn → a Stop hook that blocks
turn-end until the check passes → an adversarial fresh-context reviewer that sees only
the diff and the criteria (see `loop-review`).

## Rationalizations

| Excuse | Reality |
|---|---|
| "It compiles, so it works" | Compiling is the model's reward signal, not the user's — stubs compile |
| "The change is trivial" | Trivial changes break systems precisely because nobody verifies them |
| "Tests passed earlier" | Earlier was before the last change; evidence expires on every edit |
| "I'll verify after committing" | The claim is being made now; verify now |
| "The test is flaky, skip it" | A flaky gate is a bug to fix, never a gate to remove |

## Pitfalls

- Verifying against a mock or stub when the real dependency was the thing in question
- Weakening or deleting a failing test to make the gate pass — that is gaming the
  check, and it is never acceptable
- Quoting a stale run's output as if it were fresh
- Verifying the happy path only, when the change touched error handling

---
*Related: `loop-review` (adversarial verification of a whole diff), `loop-debug` (when
the check fails), `loop-long-horizon` (verification before flipping any state-file
entry) · output/ADR format: `playbook-conventions`*

---
name: adversarial-review-gate
description: Adversarial code review that tries to break a change instead of approving it, and only counts a finding when a failing test reproduces it, ending in a GATE PASS or GATE FAIL verdict. Use when reviewing a diff, pull request or freshly AI-generated code for race conditions, idempotency, partial-failure, boundary and security bugs, or when you need a review step that cannot rubber-stamp.
argument-hint: "[branch, PR, commit range or files to review]"
---

# Adversarial review gate

Your job is to break the code, not to praise it. Start from "there is a bug until I prove
otherwise". A finding without a reproducing test is a hypothesis, not a finding.

## Procedure

1. **Scope the change.** Use what the user names (PR, branch, commit range, files). Otherwise
   review the working-tree diff against the default branch. Read the spec, ticket or design notes
   if they exist: a violated requirement is the strongest finding.
2. **Build an attack list** from `references/attack-surfaces.md`, ranked by what the code does:
   money or shared state → concurrency, idempotency and atomicity first; parsers → boundaries and
   encoding; HTTP handlers → authorization, error mapping and input limits.
3. **Attack, one hypothesis at a time.** For each, write the smallest test that fails *if and only
   if* the bug exists, in the project's own test framework and folder, then run it.
   - The test **fails** → a finding. Record severity, `file:line`, the exact input or interleaving
     that triggers it, and the test name. Leave the test failing; it is the evidence.
   - The test **passes** → record the attack as "attempted, held". Keep the test as a regression
     guard if it is cheap and deterministic.
4. **Do not fix the code in this step.** The fix is a separate change by whoever owns the code;
   then this review runs again. A reviewer that fixes its own findings is grading its own work.
5. **Write the report** with `assets/REVIEW-template.md` to the place the user prefers (default
   `reviews/REVIEW-<NNN>.md`).

## Verdict

- `GATE: FAIL`: at least one finding is reproduced by a failing test.
- `GATE: PASS`: you list every attack you attempted, each with the adversarial test you wrote, and
  all of them pass.

An empty review, a "looks good", or findings without tests are not valid outcomes. If you could not
build a test for a suspicion (it needs infrastructure you do not have), list it under
"Unverified hypotheses" with what would be needed to test it. It does not count towards the
verdict either way.

## Techniques that find real bugs

- **Concurrency:** real threads or processes released together by a barrier, a file-backed or real
  database (never an in-memory stand-in that serialises for you), one connection per worker.
  Better still, **force the bad interleaving deterministically**: hold the lock on one connection
  and set a near-zero lock timeout on the other. A storm only finds the bug when it gets lucky.
- **Crash between two writes:** make the second write raise an exception type that escapes the
  code's cleanup handler (e.g. a `BaseException` subclass in Python), drop the connection, reopen,
  and assert the invariant still holds.
- **Replay:** send the same request twice, concurrently, and again after a restart.
- **Property-based tests** (Hypothesis, fast-check, jqwik, proptest) when the input space is large.

`references/case-study.md` shows a full red → fix → green cycle on a payments ledger.

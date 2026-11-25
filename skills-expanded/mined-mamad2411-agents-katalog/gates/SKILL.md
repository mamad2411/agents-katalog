---
name: gates
description: Use when about to claim work is complete/fixed/passing, when a task risks agent laziness (large, multi-step, previously half-done, or with acceptance criteria), or when running long-horizon/unattended work where quality must be verified before proceeding. Covers gates, gates ledgers, and autonomous gate semantics. Completion-claim discipline only; writing tests goes to testing or e2e-testing.
triggers: [user, model]
---

# Gates

**The Iron Law: NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.**

Violating the letter of this rule is violating the spirit. If you haven't run
the verification command in this message, you cannot claim it passes.

## The Gate Function (before ANY claim of status/success)

1. IDENTIFY: what command proves this claim?
2. RUN: execute it fresh and complete.
3. READ: full output, exit code, failure count.
4. VERIFY: output confirms the claim? NO → state actual status + evidence.
   YES → claim WITH evidence.
5. ONLY THEN make the claim. Skip any step = lying, not verifying.

| Claim | Requires | Not sufficient |
|---|---|---|
| Tests pass | Test output: 0 failures | Previous run, "should pass" |
| Lint clean | Linter output: 0 errors | Partial check |
| Build succeeds | Build exit 0 | Linter passing |
| Bug fixed | Original symptom test passes | Code changed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff verified | Agent said "success" |
| Requirements met | Line-by-line checklist | Tests passing |

Red flags — STOP: "should/probably/seems to", satisfaction before
verification ("Great!", "Done!"), committing without verification, trusting
agent reports, "just this once".

Security check before claiming done on API/DB/secrets/endpoints/infra work:
no secrets in diff, no new unauthenticated endpoints/public storage, no broad
IAM, no plaintext passwords. Any present → run `security` first.

## Gate types (autonomous/long-horizon)

A gate is a command that must exit 0 before the task can be declared complete.
Bounded (truncate output), idempotent, skippable only when nothing relevant
changed since last failure, multi-level.

| Gate | When | Example | On failure |
|---|---|---|---|
| Pre-task | Before starting | `git status --porcelain` | Stop, ask user |
| Step | After each step | `npm test -- --grep "<step>"` | Retry with output |
| Integration | After combining | `npm run build` | Roll back to green |
| Final | Before "done" | `npm run check` | Cannot declare done |
| Security | Before push | `python scripts/check-ai-signature.py` | Block, fix |

If a fixed gate still fails and the workspace is unchanged since last
failure → the gate may be wrong; stop and escalate.

## Verification Functions (VFs) — the dual gate

Before dispatching an implementer, distill the spec into checkable
assertions with commands:

```
VF1: API returns 200 for valid input → curl -s -o /dev/null -w "%{http_code}" localhost:3000/api -d '{"valid":"data"}'
VF3: Type checker passes → npx tsc --noEmit
```

Gate 1 (PRE): VFs go in the implementer's brief; it must run every VF and
show output before claiming DONE. Gate 2 (POST): controller re-runs VFs
independently; failure → re-enter fix loop. Can't write a VF → the
requirement is ambiguous — clarify first.

## Gates ledger (unlazy pattern)

For tasks at laziness risk — large, multi-step, previously half-done, or with
acceptance criteria — write the ledger BEFORE work. Path: `.devin/ledgers/<task>.md`
when tracked; otherwise the repo's tracked `ledgers/` convention (record the
path decision).

```markdown
# GATES: add OAuth2 login

- [ ] G1: valid fixture imports
  CHECK: python -m pytest tests/import/test_valid.py
  EXPECT: 1 passed
  EVIDENCE: pending

ABANDON: G3 migration owner unavailable; recorded in issue 123
```

Rules:
- Every runnable gate gets `CHECK:` + `EXPECT:`; run it, replace
  `EVIDENCE: pending` with the deciding snippet.
- Check fails → fix the work, not the check.
- Manual gates only when no command can decide.
- Impossible step → explicit `ABANDON: <id> <reason>`, never silent drop.
- A ticked gate with `EVIDENCE: pending` is worse than an empty gate.
- Re-run every runnable gate after claiming done; report met/unmet/abandoned.
- Don't create a ledger for a trivial edit (<20 lines, one tool call).

Anti-patterns: grading own gates without re-running; trusting "done" without
recorded evidence; skipping ABANDON; gates as the ONLY verification (manual
review still catches design issues); overly broad step gates (scope them).

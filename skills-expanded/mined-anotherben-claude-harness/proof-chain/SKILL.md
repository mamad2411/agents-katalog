---
name: proof-chain
description: >
  Use when someone wants to claim work is fixed, done, ready, green, merge-ready,
  shipped, proven, or deployed; when GitHub checks passed but live proof may be
  missing; or when proof must span patch-or-fix, prove-it, PR checks, review
  threads, merge, and dev/prod evidence. This skill composes existing proof
  skills and forbids completion claims from green CI or summaries alone.
---

# Proof Chain

## Overview

Turn completion claims into a proof-state verdict. This skill wraps `patch-or-fix`, `prove-it`, and PR/deploy closeout checks instead of duplicating their detailed workflows.

## Required Skill Reuse

- Run `patch-or-fix` when code, a fix, a PR diff, or a proposed repair exists and root-cause quality must be judged.
- Run `prove-it` before saying fixed, done, ready, safe, merge-ready, ship-ready, or deployed-proof complete.
- Run `blast-radius` because `prove-it` requires it for claimed fixes.
- Run PR/review closeout skills or repo wrappers when the claim involves a PR, review comments, or merge readiness.
- Run repo-local enterprise overlays when governed artifacts or route cards require them.

## Proof Ladder

Use the lowest honest status:

- `NOT_STARTED`: no implementation or proof.
- `IMPLEMENTED_UNREVIEWED`: code exists but patch/fix review has not run.
- `PATCH_OR_FIX_FAILED`: `patch-or-fix` found symptom patch, ownership/SRP/domain gap, or unproven root cause.
- `PATCH_OR_FIX_PASSED`: root-cause quality passed, but runtime proof has not.
- `PARTIALLY_PROVED`: some tests/proof ran, but live boundary, edge, side effect, review trap, or env proof is missing.
- `PROVED_LOCALLY`: `prove-it` passed against the correct local/live-safe boundary.
- `PR_READY`: local proof plus required PR body/wrapper/blast-radius requirements are satisfied.
- `REVIEW_SETTLED`: PR checks and review threads are clean for the current head.
- `MERGED`: merge completed on the intended base.
- `DEPLOYED_PROVED`: deployed dev/prod proof ran against the intended environment.
- `BLOCKED`: required env, route, issue, PR, or proof surface is unavailable.

GitHub green cannot raise the verdict above the available runtime proof. A stale SHA, wrong branch, wrong database, unresolved review thread, or skipped live proof lowers the verdict.

## Workflow

1. Name the claim being proved and split compound claims.
2. Resolve the current checkout, issue/PR, SHA, base, environment, and proof target.
3. Run or require `patch-or-fix` for root-cause quality when code changed.
4. Run or require `prove-it` for real-boundary runtime proof.
5. If PR-related, refresh checks, mergeability, review-thread state, and required wrapper evidence.
6. If merged/deployed proof is requested, verify the target branch/deployment and run the appropriate smoke/canary/deploy proof.
7. Emit the lowest honest proof status and the exact missing next proof action.

## Output

```markdown
**Proof status:** <proof ladder status>
**Can say fixed/done/ready?:** yes/no
**Current SHA/env:** <sha and target or missing>
**Patch-or-fix:** <PASS/FAIL/not run and why>
**Prove-it:** <PROVED/PARTIAL/UNPROVED/not run and why>
**PR/review state:** <not applicable or current evidence>
**Merge/deploy state:** <not applicable or current evidence>
**Blocking gaps:** <bullets>
**Next proof action:** <one exact action or command>
```

If either `patch-or-fix` or `prove-it` is required but unavailable, the proof status is no higher than `BLOCKED` or `PARTIALLY_PROVED`.

---
name: structural-verifying
description: Use when proving a fix, feature, migration, incident repair, performance claim, release candidate, or behavior change works in a running system.
---

# Structural Verifying

Verification is a running-system claim, not confidence in a diff.

Core rule:

> Watch the behavior fail where it lived, then pass where it will run. A green check that was never red proves nothing about the bug.

## Default output

```md
## Claim
- What must be proven:
- Where the bug/risk lived:

## Required proof
- Red before / green after:
- Acceptance criteria:
- Worst boundary input:
- Failure/degraded path:
- Replay/concurrency/interruption:
- Scale / performance bound:
- Prod-like signals:

## Evidence accepted
- Test/log/trace/provider/data evidence:
- Permanent regression:
- Unverified remainder:
```

## Verification checks

- Reproduce the original report before the fix and prove it gone after the fix.
- Verify against acceptance criteria and contract, not the diff.
- Drive the worst real boundary input: oversized, malformed, hostile, wrong auth, bad schema.
- Exercise failure and degraded paths: timeout, dependency down, breaker open, fallback visible.
- Run stateful operations twice, concurrently, and interrupted where those risks exist.
- Verify cost-bearing paths at reachable scale or assert stable query count/algorithmic bound.
- Confirm in staging/canary/prod-like config while watching the signals you shipped.
- Make the verification reproducible and keep escaped-bug regressions forever.

## Red flags

- “The unit test passes locally” as the whole verification.
- Test never seen red against the original defect.
- Only happy path exercised.
- Performance verified on toy data while caller can send large input.
- Manual terminal history with no pinned inputs, seed, or permanent check.

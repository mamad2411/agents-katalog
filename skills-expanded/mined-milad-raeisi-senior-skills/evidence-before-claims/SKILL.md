---
name: evidence-before-claims
description: Verification gate before any claim of success. Use right before saying anything is done, fixed, working, passing, faster, safe, or complete, before committing, pushing, or opening a PR, before moving to the next task, and before reporting a subagent's results. Requires fresh output from the command that proves each claim (tests, build, type-check, lint, reproduction of the original symptom, benchmark), and honest reporting of anything not verified.
license: MIT
metadata:
  category: craft
  version: "1.2.0"
---

# Evidence Before Claims

An agent's most expensive failure isn't a bug; it's a confident "done" that isn't. The user stops checking, builds on top of it, and finds out later at a much higher price. The fix is a simple gate: **no claim without fresh evidence from this session.**

## The gate

Before stating any status:

1. **Identify** the command or observation that would prove the claim.
2. **Run it** fresh, in full, now. Not an earlier run, and not a subset.
3. **Read** the whole output: exit code, failure counts, warnings, skipped tests.
4. **Decide**: if the evidence supports the claim, state it *with* the evidence. If it doesn't, state the actual status.

## What each claim requires

| Claim | Evidence | Not evidence |
|---|---|---|
| Tests pass | Test command output with 0 failures, run after the last change | An earlier run; "should pass" |
| Build works | Build command exits 0 | Lint passing; the editor showing no errors |
| Types are correct | Type-checker output clean | Tests passing (they may not cover it) |
| Bug fixed | The original reproduction no longer fails, plus a regression test that failed before the fix | The code "looks right" |
| Faster | Before and after measurements, same conditions, several runs | Reasoning about complexity |
| Feature complete | Each requirement checked off against the original request | The happy path working |
| Subagent's work is done | You inspected the diff and re-ran the checks | The subagent said so |
| Safe to deploy | The project's release checklist passed | Nothing obviously broke |

## Language that signals a missing check

"Should work", "probably", "seems to", "I believe this fixes", "this ought to", and celebrating ("Done!", "Perfect!") before running anything. When you notice yourself writing these, run the check instead, or rephrase as an honest unverified statement.

## Reporting partial verification

Sometimes you can't verify everything: no access to staging, no Windows machine, the suite takes hours, a test needs credentials. Then say precisely what was and wasn't checked:

```
Verified: unit tests (182 passed), type-check clean, build OK.
Not verified: the Stripe webhook path (needs live keys); please run `make e2e-payments` before merging.
```

That sentence is worth more than any confident summary, because it tells the reader exactly where the remaining risk is.

## Pre-existing failures

If something was already failing before your change, show it: run the same check on the base commit to prove the failure isn't yours, and report it separately. A separate checkout is safest (`git worktree add <scratch-dir> <base-ref>`); `git stash` skips untracked files unless you pass `-u`, and must be popped afterwards. Don't let pre-existing noise hide new breakage, and don't claim a clean suite when it isn't one.

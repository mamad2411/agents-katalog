---
name: adversarial-review
description: Review a diff as an adversary — assume the code is wrong, work from the diff alone, and try to construct concrete failures. The reviewer-role procedure for multi-agent workflows (one implements, N review), distilled from the Bun-in-Rust port.
---

# Adversarial review

Use when you are the *reviewer* in a generate-review-fix loop: another agent
(or person) wrote the change, and your job is to find what's wrong with it —
not to appreciate what's right.

The stance matters more than the checklist: the agent that wrote the code
wants it accepted; you want to find the failure. Those must be different
agents — never review your own diff adversarially and call it done.

## Ground rules

- **Assume the code is wrong.** Your null hypothesis is "this diff contains a
  bug"; your job is to locate it. Only after honestly failing to construct a
  failure do you approve.
- **Work from the diff.** Judge what's in front of you; read surrounding
  source only to verify a suspicion (call signatures, invariants, callers) —
  not to absorb the author's framing or comments as truth.
- **Concrete failures only.** Every finding names inputs/state → wrong
  outcome. "This looks risky" is not a finding; "empty list → index panic at
  line 42" is.
- **The paragraph rule:** if a workaround needs a paragraph-long comment to
  justify why it's OK, the code is wrong — reject and say what to fix.
  Suspiciously long justifications are where stubs and shortcuts hide.
- **No trust in green.** "Tests pass" is not evidence the change is right —
  check whether the tests were weakened, skipped, or never covered the
  changed behavior in the first place.

## Where to look first

1. **Edges:** empty/zero/max inputs, error paths, early returns, off-by-one.
2. **Deletions:** what did the diff remove, and who still depended on it?
3. **Renames & moves:** behavior changes hiding inside "mechanical" churn.
4. **Stubs:** `todo!()`, `unimplemented`, hardcoded returns, and their
   explanatory comments.
5. **Concurrency & resources:** lifetimes, locks, cleanup on the failure path.

## Output

Return findings ranked most-severe first, each as: **where** (file:line),
**what breaks** (the concrete scenario), **fix direction** (one sentence).
If nothing survived honest scrutiny, say so plainly — a forced nitpick is
noise, and an empty report from an adversary is a strong signal.

## In a workflow

Pair this with N ≥ 2 independent reviewers per diff when stakes warrant it —
different reviewers catch different failure modes. Feedback goes to a *fixer*
(the author role or a third agent), then re-review the fix: a fix is a new
diff and gets the same treatment.

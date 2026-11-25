---
name: legacy-code-changes
description: Making safe changes in unfamiliar, undertested, or legacy codebases — comprehension before modification, characterization tests, seams, and incremental replacement. Use when working in a codebase you didn't write, inheriting a project, touching code with no tests, planning a refactor of old code, or when the user says "legacy", "inherited this code", "old codebase", "nobody knows how this works", or "should we rewrite".
---

# Legacy Code Changes

Legacy code is code that makes money and scares you. It survived contact with reality — every weird `if` in it may be a bug fix for something that actually happened. The discipline: **comprehension before modification, safety before improvement, incremental over heroic.** This applies double to AI assistants, which have a strong rewrite bias: regenerating code they don't understand instead of minimally editing it.

## Gate 1: Understand before touching (timeboxed, active)

- **Trace one real flow end-to-end** — entry point → decision points → side effects → output — for the exact behavior you must change. Reading the whole codebase is procrastination; tracing one path is comprehension.
- Use archaeology, not just reading: `git log -p` on the file (why does this weird line exist? — the commit message knows), `git blame` on the scary part, existing tests as executable documentation, and running the thing with a debugger/print on the path in question.
- Write down the 3–5 facts you learned that surprised you. If nothing surprised you, you haven't understood it yet — legacy code always surprises.
- **Chesterton's Fence is the law**: never delete or "fix" code you can't explain. That check for a null tenant on Tuesdays is either dead code or a ₹10-lakh lesson — find out which (git history, asking, logging it in prod) before removing.

## Gate 2: Pin current behavior before changing it

- Where tests are missing, write **characterization tests first**: capture what the code *actually does now* (including behavior that looks wrong), so you can detect what your change breaks. You're not asserting correctness; you're building a tripwire. Feed the function its realistic inputs, snapshot the outputs, done — 30 minutes of pinning beats a week of "what else did I break".
- Can't test it because it's tangled in I/O and globals? Find or make the smallest **seam**: extract the decision logic from the side effects just enough to get it under test (code-quality's edges-and-core rule) — the minimal surgery, not a beautification pass.
- No time even for that? Then pin behavior operationally: run the golden path before and after, diff the outputs/DB state, and say honestly that this is the verification level (evidence rule).

## Gate 3: The smallest change that works — then stop

- Match the existing style, patterns, and idiom **even where you'd choose differently** — a codebase with two conventions is worse than one with one mediocre convention. Improvements to the pattern are a separate, explicit proposal.
- Never mix the behavior change with cleanup in one commit (change-hygiene). The reviewer must be able to verify one claim at a time.
- Resist the pull to fix everything you see. Keep a written list of what you *didn't* fix (the "later ledger") instead of expanding the blast radius now. Touch radius ∝ risk in undertested code.

## When "rewrite it" comes up — the honest calculus

Rewrites systematically lose because the old system's value is not its code but its **accumulated edge-case knowledge**, which the rewrite silently discards and then relearns from angry users. Default answer: no.

- The alternative that works: **strangler pattern** — put a boundary in front of the old code, route new functionality (or one migrated slice at a time) to new code behind the same interface, verify parity, expand slice by slice, delete the old path last. Every step shippable; reversal always possible.
- A rewrite is justified only when: the platform is dying under you (unsupported runtime, unbuildable), AND the scope is small enough to finish before requirements shift, AND you have the behavior pinned (tests/parity harness) so "done" is checkable. All three, in writing.
- Partial rewrites of the scary module follow the same rule in miniature: pin behavior → build replacement behind the seam → run both and diff (shadow mode) → cut over → delete.

## Failure modes to hunt (in yourself and AI output)

- The "while I was in there" diff — 400 changed lines for a 5-line fix. Reject and re-slice.
- Regenerated-not-edited: an AI rewriting a function wholesale, silently dropping the weird branches (that Tuesday null check) it didn't understand. Diff old vs new *branch by branch*, not by vibes.
- "The tests pass" in a codebase whose tests don't cover the changed path — check coverage of the specific diff, not the suite's green.
- Confidence from cleanliness: new tidy code *feels* more correct than old ugly code. Feeling is not evidence; parity runs are.

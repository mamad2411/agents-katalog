---
name: self-correction-loop
description: Use when a hook/tool returns a warning, lint/type/build error, or test failure after your edit. Iterate evidence-first; stop when verification passes.
---

# Self-Correction Loop

When your edit produces a warning/error signal, you're in a **correction loop**. This skill is the discipline that keeps the loop productive instead of thrashing.

## Trigger signals

You should engage this loop when ANY of these happen after your edit:

- `PostToolUse` hook injected `clang-tidy warnings:` / `lint warnings:` / similar
- A `Bash` command you ran returned non-zero exit
- A test runner reports failures
- A type-checker reports errors
- The user says "that broke X" / "it's failing now"

## The Loop (RED → diagnose → minimal-fix → GREEN)

This is **TDD's RED-GREEN-REFACTOR adapted for correction**:

```
1. CAPTURE the signal
   - What is the EXACT error message?
   - Which file / line?
   - What was my last change?

2. DIAGNOSE root cause (not symptom)
   - Read the error carefully — the answer is often in it
   - Check if my change broke an invariant elsewhere
   - Do NOT guess. If unclear, narrow with prints / smaller test cases

3. MINIMAL FIX
   - Smallest possible change that resolves THE specific issue
   - No "while I'm here" tangents (that's scope creep — see scope-jump)
   - Do NOT mask the error (e.g. catch-and-ignore) without explicit reason

4. RE-VERIFY
   - Run the same command that produced the signal
   - Observe the new output
   - Capture it as evidence
```

## Loop budget

This loop is for **surface signals** that a quick minimal fix resolves. If a minimal fix doesn't clear the signal within **1–2 iterations** — or the failure spans components / needs backward root-cause tracing — **switch to `superpowers:systematic-debugging`** (its 4-phase root-cause process). Don't keep thrashing minimal fixes here.

If you've iterated 3 times on the same signal without resolving it, **stop and escalate**:

- Switch to `superpowers:systematic-debugging` for structured root-cause investigation (its budget also caps at 3 fixes → then question the architecture; the two thresholds are intentionally aligned)
- Read more of the surrounding code than you have so far
- Invoke `docs-lookup` skill for the specific error class (Context7 → WebSearch fallback)
- Tell the user: *"I've tried 3 approaches to <issue>. Latest output: <...>. I need more context. Recommend either <option A> or <option B>?"*

Looping > 5 times is almost always a sign of:
- Wrong mental model of the bug → step out, re-read
- Missing tool/dependency → install it before continuing
- Genuinely ambiguous case → consult the user

### Two budgets: re-run vs. edit

The budget above is the **re-run budget** — re-running the *same failing command*. There's a second, sneakier loop: the **edit budget**.

- **Edit budget (doom-loop):** if you've made ~3–5 edits to the **same file** chasing the **same goal** without the signal clearing, you're micro-adjusting one approach. STOP. **Re-read the original spec / `done_criteria` — not your own diff** (the classic failure is re-reading your own code, deciding it "looks ok", and continuing). Then either switch to a structurally different approach or escalate to the user.
- Don't "fix" a failing test by **rewriting the test** to match your code — that silences the signal. Treat tests as a reserved space: change the implementation, or question the requirement, not the test.

This mirrors LoopDetection middleware ("reconsider the approach after N edits on one file") — break out *before* the 10th micro-adjustment, not after.

## What "fixed" looks like

- The original failing command now succeeds (exit 0 + expected output)
- You can articulate WHY it failed and WHY the fix resolves it
- No new failures introduced (re-run the broader test suite, not just the one test)

If you can't articulate WHY, your fix is suspicious — even if green. State this uncertainty per `anti-hallucination-gates`.

**Before moving on:** if the failure you just fixed is a *recurrence* (second+ time you've seen
the class), capture it as a golden rule **in this same turn** — a rough stub via
`capturing-golden-rules` — not as a mental note for session end. Deferred captures get distorted
or forgotten when context compacts.

## Anti-patterns

- **Silencing instead of fixing**: `// @ts-ignore`, `--no-verify`, deleting failing tests, broadening exception catches. These hide problems; sometimes they're warranted but require explicit user note.
- **Chasing different bug**: a lint warning on line 42 doesn't justify refactoring lines 100-200.
- **Optimistic re-run**: running the same failing test again "in case it was flaky" without changing anything. Flakiness is a separate issue to track, not a fix.

## How this interacts with hooks

`harness-anchor` hooks are **warn-only**. They inject `additionalContext` describing the problem; they don't block your action. That means:

- You *can* ignore a warning, but the warning is recorded in your context — the user can see you saw it. If you ignore, do so deliberately and say why.
- A test failure injected by PostToolUse should generally be addressed before moving on; if you choose to defer it (e.g., feature is mid-build and the test is for the next milestone), note it as a known-failing in `session-handoff.md`.

## When this skill is NOT applicable

- The signal is about a different feature than the one you're working on. Note it as `planned` in `feature_list.json` and continue current scope.
- The error is in third-party code you don't own. Document it; route to the right project.

## Triaging fresh-context sensor findings

A fresh-context sensor's report — `/verify` (`verification-runner`), `/test-plan` (`coverage-analyst`), `/gc` (`drift-analyst`) — is **reviewer feedback from a deliberately context-blind evaluator**: it cannot see your intent (that independence is the design). Triage it with `superpowers:receiving-code-review` rigor — verify each finding against the code, push back on false positives **with technical reasoning**, act one-at-a-time — rather than blind-applying. This matters most inside **`/verify --fix`**: the bounded loop should apply *verified* findings, not churn on every recommendation. This is not a licence to dismiss the sensor — `receiving-code-review` is rigorous; you verify, then act.

## Related

- `anti-hallucination-gates` — keep claims honest while looping
- `capturing-golden-rules` — a recurring failure you just fixed becomes a rule in the same turn
- `receiving-code-review` (superpowers) — the discipline for triaging a fresh-context sensor's findings (verify each, push back with reasoning, don't blind-apply)
- `systematic-debugging` (superpowers) — for deep debugging beyond surface signals
- `verification-runner` (agent) — for fresh-eyes evaluation of "is this really fixed?"

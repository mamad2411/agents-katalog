---
name: z-bugfix
description: Gated 4-phase diagnosis workflow for hard bugs, concurrency issues, and performance regressions. Use when something throws, fails, deadlocks, freezes, or behaves unexpectedly.
---

# Z-Bugfix Investigation Protocol

Enforces a rigorous 4-phase investigative gate. Never jump directly to guessing fixes in production code.

## Phase 1: Sensory Sweep (Observable Reality)
1. Read exact error messages, stack traces, and failure exit codes verbatim.
2. Locate the precise file and line numbers of the failure point.
3. Identify recent code diffs or environmental triggers that exposed the issue.

## Phase 2: Socratic Inquiry & Hypotheses
1. Formulate 2–3 competing hypotheses explaining the failure:
   - $H_1$: Logic/boundary condition error.
   - $H_2$: Concurrency / race condition / state mutation timing.
   - $H_3$: Environmental / configuration / type mismatch.
2. For each hypothesis, identify a testable distinction.

## Phase 3: Deterministic Reproduction Test (Red Gate)
1. Write a minimal automated reproduction test reproducing the exact failure.
2. Execute the test and verify it FAILS with the expected signature (Red).
3. If the test cannot reproduce the issue, do NOT touch production code; return to Phase 1.

## Phase 4: Targeted Fix & Zero-Regression Verification (Green Gate)
1. Apply the minimal necessary correction to eliminate the root cause.
2. Re-run the reproduction test and confirm it PASSES (Green).
3. Re-run the entire project test suite to verify zero regression across existing features.
4. Document the lesson in 3 parts: `<Problem> | <Root Cause> | <Fix>` for episodic memory harvesting.

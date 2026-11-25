---
name: formax-rework-convergence-workflow
description: Use when code has gone through repeated rework and may contain redundant logic, style drift, or tangled structure. Trigger when user asks for "返工收敛", "cleanup-pass", or requests a focused cleanup pass that reduces churn without changing behavior.
---

# Formax Rework Convergence Workflow

## Purpose

Use this workflow to clean up code after multiple back-and-forth edits.

Primary goal:
- Reduce redundancy
- Restore structure clarity
- Keep behavior unchanged unless user explicitly asks for behavior changes

## Trigger Phrases

Run this skill when the user says:
- `返工收敛` (recommended keyword)
- `cleanup-pass`
- "帮我收敛一下这波改动"
- "把返工后冗余代码清掉"

## Scope Rules

1. No feature expansion during convergence.
2. No broad redesign unless user explicitly asks.
3. Prefer local cleanup in touched files first.
4. Preserve existing runtime behavior and UI semantics.

## Workflow

1. Freeze Intent
- Restate the target in one sentence.
- Identify "must keep" behavior before editing.

2. Build Cleanup Map
- Inspect current diff and touched files.
- Group issues into:
  - duplicate logic
  - dead code / unreachable branches
  - conflicting style patterns
  - state ownership confusion
  - temporary patches that became permanent

3. Rank by Risk and Value
- High priority:
  - behavior-risky duplication
  - conflicting state sources
  - repeated conditional branches causing drift
- Medium priority:
  - naming inconsistencies
  - repeated style tokens/classes
- Low priority:
  - cosmetic micro-cleanups

4. Apply Minimal Convergence Edits
- Collapse duplicated branches into one shared path.
- Remove dead paths only when replacement path is verified.
- Keep interfaces stable.
- Keep patch size small and reviewable.

5. Validate
- Run targeted type-check/tests for changed scope.
- If UI is touched, do a quick manual visual sanity check path.
- If validation is blocked, report the exact blocker and impact.

6. Report Back in Convergence Format
- `what was removed`
- `what was unified`
- `what behavior stayed the same`
- `residual risks`

## Guardrails

- Do not hide uncertainty: explicitly call out assumptions.
- Do not ship "temporary fixes" silently.
- If a temporary mitigation is unavoidable, mark it and define removal conditions.
- Never mix unrelated cleanup in the same pass.

## Output Template

Use this structure in responses:

1. Convergence summary (2-4 lines)
2. Redundancy removed
3. Structure unified
4. Behavior parity check
5. Risks and next small pass (optional)


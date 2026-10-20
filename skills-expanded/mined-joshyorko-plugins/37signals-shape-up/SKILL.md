---
name: 37signals-shape-up
description: Use when shaping a raw product idea, request, spike, project, or bet into a bounded Shape Up pitch.
---
## Source Grounding

Community-maintained and 37signals-inspired, not official Basecamp guidance.
Read `../../references/caveats.md`; user constraints and current project truth
win.

# 37signals Shape Up

Shape before planning. The output is a small decision artifact that makes the
bet, appetite, boundaries, risks, and circuit breaker clear enough to decide.

## Workflow

1. State the raw idea in one sentence.
2. Name the appetite: tiny spike, one-day patch, one-week feature, or cycle.
3. Define the problem and user-visible progress that would count.
4. Sketch the solution at the interface/domain level, not task-by-task.
5. List rabbit holes that could consume the appetite.
6. List no-gos: what this intentionally will not solve.
7. Define the circuit breaker when the appetite is spent.
8. Decide: bet, reshape smaller, research first, or reject.

## Pitch Shape

Use `../../references/recipes/shape-up-pitch.md`. Use
`../../references/recipes/shape-up-cycle.md` when cycle, cool-down, betting, or
scope-progress language matters. A good pitch has problem, appetite, solution,
boundaries, rabbit holes, no-gos, and circuit breaker.

## AI Feature Checks

- Source data allowed and how the user inspects it.
- Deterministic fallback if generation quality misses the appetite.
- Human review before sending, publishing, deleting, or changing records.
- Permissions, tenant boundaries, retention, and cost controls before shipping.

## Do Not Use For

- Rails implementation after the pitch is accepted: use
  `$37signals-rails-implement`.
- Existing workflow refresh before it is a bet: use
  `$37signals-product-refresh`.
- Generic simplification without pitch structure: use
  `$37signals-scope-judgment`.

## Output

Return the pitch, recommendation, and next smallest validation step. Do not turn
a shaped pitch into an implementation plan unless the user asks.

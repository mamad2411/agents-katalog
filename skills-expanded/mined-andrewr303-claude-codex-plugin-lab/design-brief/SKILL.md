---
name: design-brief
description: Use before planning a new feature, architecture change, UI, workflow, product surface, or ML experiment where intent and constraints need shaping.
---

# Design Brief

Use this when the solution space is still blurry. The goal is a brief the user can approve or correct before implementation planning.

## Brief Fields

- Problem: what is failing or missing.
- Audience/user: who experiences the result.
- Outcome: what becomes possible after the work.
- Non-goals: what stays out of scope.
- Constraints: stack, design system, auth/data boundaries, runtime, deadline, compatibility.
- States: success, loading, empty, error, disabled, partial, retry, reduced motion, mobile/desktop if UI.
- Risks: quiet failures, costly reversals, late detection.
- Acceptance evidence: the concrete check that proves each important behavior.

## Method

1. Inspect the current system before proposing shape.
2. Generate 2-3 viable options only when meaningful.
3. Pick a recommended option and explain tradeoffs.
4. Keep the brief small enough to review.
5. Ask one blocking question only when a wrong assumption would be expensive.

## For ML Experiments

Add:

- Hypothesis.
- Independent/dependent/control variables.
- Fixed evaluation command or dataset.
- Baseline.
- Success threshold.
- Failure modes that distinguish implementation bugs from strategy failures.


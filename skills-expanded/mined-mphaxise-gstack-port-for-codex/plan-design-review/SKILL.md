---
name: plan-design-review
description: Pre-implementation design review for Codex. Use when a plan has user-facing UI or UX and should be critiqued before implementation starts.
---

# Plan Design Review

Use this skill when a plan includes user-facing experience and the right move is to improve the design before code is written.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Read only the materials needed to understand the planned experience.
2. Identify the primary user journey the plan is trying to create.
3. Review the plan across the main design dimensions:
   - clarity of purpose
   - visual hierarchy
   - interaction flow
   - information density
   - tone and taste
   - responsiveness and accessibility
4. Rate the weak points plainly and describe what a stronger version would look like.
5. Rewrite or refine the plan so the next implementation step is design-aware, not just technically valid.

## Guardrails

- Do not drift into implementation details unless they change the experience materially.
- Do not settle for generic "looks good" feedback; name the most important improvements.
- Preserve the product goal while challenging weak interaction or presentation choices.

## Outputs

Always include:

- user journey being reviewed
- strongest current design choice
- weakest current design choice
- revised design direction
- specific risks to avoid during implementation
- next 1-3 actions

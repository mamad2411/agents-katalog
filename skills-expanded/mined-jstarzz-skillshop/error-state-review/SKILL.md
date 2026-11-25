---
name: error-state-review
description: "Review how UI failure states explain what happened, preserve work and provide safe recovery without false success. Use when error state, API failure UI, retry UX."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "frontend"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Error State Review

Review how UI failure states explain what happened, preserve work and provide safe recovery without false success.

## Activate when

- error state
- API failure UI
- retry UX

## Focus

- Primary mission: Review how UI failure states explain what happened, preserve work and provide safe recovery without false success.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Identify the primary user, primary task, target devices, input methods, and supported environments.
2. Evaluate information hierarchy and interaction before cosmetic styling.
3. Exercise loading, empty, error, long-content, narrow-width, keyboard/touch, and permission-constrained states as relevant.
4. Prefer semantic platform controls, established design tokens/components, and clear labels over bespoke decoration.
5. Check responsiveness, accessibility, performance, and recovery behavior together rather than as separate afterthoughts.
6. Test on representative constrained conditions instead of trusting a desktop screenshot.
7. Return changes in terms of user-task improvement and reusable system fixes, not isolated pixel hacks.

## Deliverables

- User-task findings
- Reusable design/interaction fixes
- Device/accessibility/performance gaps
- A result that directly satisfies: Review how UI failure states explain what happened, preserve work and provide safe recovery without false success.

## Common failure modes

- Designing only for a single desktop screenshot
- Adding tooltips to compensate for bad information architecture
- Gratuitous cards, pills, gradients, huge radii, or icon noise
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.

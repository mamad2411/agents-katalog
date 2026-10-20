---
name: 37signals-product-design
description: Use when designing or reviewing product UI, flows, onboarding, settings, empty states, copy, or screens.
---
## Source Grounding

Community-maintained and 37signals-inspired, not official Basecamp guidance.
Read `../../references/caveats.md`; target users, product constraints, and the
existing design system win. Do not attribute this broad synthesis to DHH alone.

# 37signals Product Design

Design the product from the interface inward. Use real screens, real copy, and
the smallest useful workflow to expose product truth before adding architecture,
navigation, settings, or explanation.

## Workflow

1. Find the epicenter: the object, decision, or action that makes the product valuable.
2. Design that moment first with real user-facing language.
3. Add only the surrounding screens needed to complete the workflow.
4. Prefer depth over surface area: strengthen the core flow before adding modes.
5. Check context over consistency: reuse patterns when they clarify the moment.
6. Verify regular, blank, error, loading, no-permission, and mobile states.

## UI Defaults

- Prefer calm, dense, legible product screens over marketing composition.
- Use domain nouns and verbs, not generic SaaS abstractions.
- Treat copy as interface: labels, buttons, empty states, confirmations, errors.
- Keep navigation proportional to the product's real surface area.
- Avoid dashboards, settings, filters, roles, and customization until needed.
- Prefer Rails/Hotwire-friendly interactions when the target app supports them.

## Recipes

Use `../../references/recipes/product-empty-states.md` and
`../../references/recipes/product-copy.md` for state and language decisions.
Use `$37signals-product-refresh` when the user wants to improve an existing
screen or workflow. Use `$37signals-hotwire` when Rails interaction mechanics are
the main question.

## Review Lens

- What is the user trying to finish?
- Is the main object obvious without explanatory text?
- Does the screen get deeper or merely wider?
- Can the interface remove a decision, step, or setting?
- Are edge states designed, not left to framework defaults?

## Do Not Use For

- Full Rails feature implementation: use `$37signals-rails-implement`.
- Existing product refresh or modernization: use `$37signals-product-refresh`.
- Shape Up pitch work: use `$37signals-shape-up`.
- Generic scope cutting: use `$37signals-scope-judgment`.

Ask before rebranding, deleting committed workflows, introducing a new frontend
framework, or replacing a design system.

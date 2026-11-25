---
name: 37signals-product-refresh
description: Use when improving an existing product, screen, workflow, onboarding, settings, or stale feature.
---
## Source Grounding

Community-maintained and 37signals-inspired, not official Basecamp guidance.
Read `../../references/caveats.md`; current users, product constraints, and
existing code/design systems win. Do not attribute this broad synthesis to DHH.

# 37signals Product Refresh

Use this when the product already exists and needs to become clearer, calmer,
more useful, or more current without turning into a vague redesign or rewrite.
The job is to refresh one real workflow around one real pain.

## Workflow

1. Name the existing workflow and the user-visible pain.
2. Set the appetite: small polish, one-day patch, one-week refresh, or shaped bet.
3. Find the epicenter: the object, decision, or action that should feel better.
4. Keep what already works and name what must not change.
5. Cut or defer stale surface area, extra settings, dashboards, modes, and roles.
6. Redesign the core screen with real copy and regular, blank, loading, error,
   no-permission, no-results, and mobile states.
7. Identify Rails/Hotwire impact before proposing a heavier frontend or rewrite.
8. Decide: ship refresh, shape a bet, refactor first, or reject.

## Recipes

Use `../../references/recipes/product-refresh.md` first. Pull
`product-copy.md`, `product-empty-states.md`, `decision-memo.md`,
`hotwire-turbo.md`, `hotwire-stimulus.md`, and Rails recipes only when the
refresh touches those surfaces.

## Do Not Use For

- Raw new-product or new-feature shaping: use `$37signals-shape-up`.
- Pure scope cutting without UI/workflow refresh: use `$37signals-scope-judgment`.
- Rails implementation after the refresh is accepted: use
  `$37signals-rails-implement` or `$37signals-rails-refactor`.
- Rebrand, rewrite, SPA conversion, or "2.0 redesign" unless the user accepts
  a bounded pain, appetite, and no-go list.

## Output

Return a Refresh Brief: baseline, core pain, appetite, epicenter, what stays,
what gets cut/deferred, refreshed workflow, states/copy, Rails/Hotwire impact,
validation step, and build/shape/reject recommendation.

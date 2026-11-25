---
name: 37signals-rails-review
description: Use when reviewing Rails code, PRs, or architecture for conventions, Hotwire defaults, and correctness risks.
---
## Source Grounding

Community-maintained and 37signals-inspired, not official Basecamp guidance.
Read `../../references/caveats.md`; target repo conventions and demonstrated
bugs outrank style preference.

# 37signals Rails Review

Review for concrete fit, not vibes. Findings must separate proven bugs from
preferences and name the smallest Rails-native alternative when pushing back.

## Review Lens

- Does the change make the app easier for one capable Rails programmer to own?
- Is business logic in a coherent Rails place instead of a needless service maze?
- Are routes, controllers, models, jobs, mailers, and tests named around domain
  work instead of framework ceremony?
- Is Hotwire enough before a separate frontend architecture is introduced?
- Are tenancy, auth, state transitions, deploy impact, and async boundaries safe?
- Are source claims scoped correctly, especially DHH-specific claims?

## Recipe Routing

Load only the recipe cards that match touched code. Common cards:
`rails-crud.md`, `rails-models.md`, `rails-migrations.md`, `rails-tests.md`,
`hotwire-turbo.md`, `hotwire-stimulus.md`, `rails-tenancy.md`,
`activerecord-tenanted.md`, `rails-delegated-types.md`, and `rails-kamal.md`.

## Do Not Use For

- Implementing the fix directly: use `$37signals-rails-implement`.
- Product UI critique without Rails code: use `$37signals-product-design`.
- Explicit "what would DHH/Rails doctrine say" architecture calls: use
  `$dhh-rails-judgment`.

## Output

Lead with findings by severity and file/line when available. Include only
actionable issues, then note source-grounding limits, missing tests, and any
style tradeoff that is not a blocker.

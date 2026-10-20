---
name: dhh-rails-judgment
description: Use when evaluating Rails architecture through DHH or Rails Doctrine judgment.
---
## Source Grounding

Community-maintained and DHH/Rails-inspired, not an official DHH style guide.
Read `../../references/caveats.md`; only make DHH-specific claims from DHH or
Rails Doctrine source scope. Target repo constraints and production reality win.

# DHH Rails Judgment

Use this only when the user asks for DHH/Rails Doctrine style architecture
judgment. Prefer conceptual compression, integrated defaults, whole-product
ownership, and boring monolith-first delivery unless real pressure justifies
splitting the system.

## Decision Lens

- Can Rails already do this with a first-party or omakase-shaped primitive?
- Is the proposed split reducing complexity or moving it into network boundaries?
- Would one capable product programmer understand and operate the whole flow?
- Is the frontend stack adding state, build, deployment, or hiring cost?
- Is a dependency replacing a tiny domain object, controller, job, or model method?
- Does the design preserve programmer happiness through clear names and feedback?

## Defaults

- Start with a majestic monolith.
- Reach for Rails, Hotwire, Active Job, Solid Queue, Action Mailer, and Kamal
  before parallel stacks.
- Prefer no-build or low-build frontend paths when they satisfy the product.
- Keep domain logic close to Active Record models and cohesive domain objects.
- Split services only when scaling, ownership, reliability, or deployment needs
  are proven.

## Do Not Use For

- Product UI, copy, or onboarding critique: use `$37signals-product-design`.
- General scope cutting: use `$37signals-scope-judgment`.
- Rails implementation sequencing: use `$37signals-rails-implement`.
- Claims about Jason Fried, REWORK, or 37signals product philosophy unless a
  matching non-DHH source is cited.

## Output

Return the recommended Rails shape, complexity removed, complexity accepted, and
the condition that would make a heavier architecture worthwhile.

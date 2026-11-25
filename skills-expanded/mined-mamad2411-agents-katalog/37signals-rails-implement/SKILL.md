---
name: 37signals-rails-implement
description: Use when implementing or extending Rails features across models, REST, Hotwire, jobs, tenancy, and tests.
---
## Source Grounding

Community-maintained and 37signals-inspired, not official Basecamp guidance.
Read `../../references/caveats.md` and `../../references/source-index.yml`.
Target repo conventions, user constraints, and production reality win.

# 37signals Rails Implement

Use this as the Rails feature entrypoint. Start from the product workflow, then
load only the recipe cards needed for the implementation surface.

## Workflow

1. Identify the smallest user-visible workflow and the Rails resources it needs.
2. Choose recipes from `../../references/recipes/` for the touched layers.
3. Prefer Rails-native defaults before adding services, frontend stacks, queues,
   caches, or deployment complexity.
4. Keep business behavior close to models, cohesive domain objects, controllers,
   jobs, and mailers already understood by the app.
5. Re-check authorization, tenancy, state transitions, async boundaries, deploy
   impact, and tests before calling the feature done.

## Recipe Routing

- Models, concerns, state records, delegated types: `rails-models.md`,
  `rails-concerns.md`, `rails-state-records.md`, `rails-delegated-types.md`.
- Routes/controllers: `rails-crud.md`.
- Schema: `rails-migrations.md`.
- UI: `hotwire-turbo.md`, `hotwire-stimulus.md`.
- Async and notification: `rails-jobs.md`, `rails-mailers.md`,
  `rails-events.md`.
- Edges: `rails-auth.md`, `rails-apis.md`, `rails-caching.md`,
  `rails-tenancy.md`, `activerecord-tenanted.md`, `rails-kamal.md`,
  `rails-tests.md`.

## Do Not Use For

- Pure code review: use `$37signals-rails-review`.
- Pure refactoring without new behavior: use `$37signals-rails-refactor`.
- Raw product shaping before a build bet: use `$37signals-shape-up`.
- Live Basecamp/Fizzy data actions: use the relevant product CLI skill.

## Output

Return the Rails shape, recipe cards used, implementation order, tests, and any
accepted complexity or unresolved production risk.

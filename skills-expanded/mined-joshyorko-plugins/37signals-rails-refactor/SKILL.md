---
name: 37signals-rails-refactor
description: Use when simplifying Rails code without behavior change, especially indirection, verbs, or scattered domain logic.
---
## Source Grounding

Community-maintained and 37signals-inspired, not official Basecamp guidance.
Read `../../references/caveats.md`; preserve behavior and target app contracts.

# 37signals Rails Refactor

Use this to make existing Rails code smaller, clearer, and more idiomatic while
keeping the public behavior stable.

## Workflow

1. Identify the user-visible behavior that must not change.
2. Name the needless concept, layer, route, dependency, or UI machinery.
3. Choose the smallest recipe card needed for the refactor.
4. Move one coherent behavior at a time.
5. Run or specify tests that prove parity and edge behavior.

## Common Moves

- Move scattered business rules back to models or cohesive domain objects.
- Replace custom controller verbs with clearer resources when route shape improves.
- Collapse unnecessary service/interactor layers.
- Reduce JavaScript by returning useful server-rendered HTML.
- Replace boolean state piles with state records when history matters.
- Remove abstraction only when behavior and names get clearer.

## Do Not Use For

- New feature work: use `$37signals-rails-implement`.
- Review-only feedback: use `$37signals-rails-review`.
- Broad architecture philosophy without a target refactor: use
  `$dhh-rails-judgment`.

## Output

Return the behavior invariant, the refactor sequence, recipes used, tests to run,
and any risk that requires a smaller step.

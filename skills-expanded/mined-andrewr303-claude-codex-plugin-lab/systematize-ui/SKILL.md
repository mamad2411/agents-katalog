---
name: systematize-ui
description: Create, audit, extend, or refactor UI design systems, semantic tokens, theme layers, primitives, component APIs, variant/state models, icon rules, and shared frontend patterns. Use when repeated visual or interaction decisions drift across screens, a shared component is hard to change, a new brand/theme must be introduced, or a multi-consumer design-system migration is required.
---

# Systematize UI

Build the smallest shared decision system supported by real product usage. Do not turn a style inventory into speculative abstraction.

Use the bundled sources directly:

- [UI Design Deep Dive](../../references/UI_DESIGN_DEEP_DIVE.md) for bounded choices, semantic roles, component contracts, refactoring translations, and theme limits.
- [UI Design Implementation Playbook](../../references/UI_DESIGN_IMPLEMENTATION_PLAYBOOK.md) for the minimum viable system, state model, token recipe, migration loop, and proof gates.

Load [design-system-and-component-contracts.md](../../references/design-system-and-component-contracts.md) first. Load [refactoring-and-migrations.md](../../references/refactoring-and-migrations.md) for public APIs or multi-consumer work, and [responsive-accessibility-and-states.md](../../references/responsive-accessibility-and-states.md) for component state/input requirements.

## Inspect the current system

Map:

- token sources and raw/semantic layers;
- global styles, themes, utility configuration, and ownership;
- primitives, compounds, variants, slots, icon assets, and motion rules;
- semantic elements, accessible-name sources, state transitions, and input behavior;
- consumers, stories/tests, supported themes/locales/viewports, and published contracts;
- repeated literals, near-duplicate roles, scattered conditionals, prop clumps, opaque flags, and dead variants.

Do not add a second styling system or parallel token source without explicit product need.

## Name the concrete pressure

State which feature, bug, theme, repeated change, or comprehension problem the system work must make easier. Record:

- the current observable contract;
- the repeated decision or ownership problem;
- the smallest enabling seam;
- the first consumer;
- a check that can fail;
- compatibility and rollback needs.

Defer cleanup that has no relationship to current change cost or risk.

## Establish the minimum foundation

Use bounded foundation scales only where the product needs them:

- spacing and content-width relationships;
- type roles, weights, measures, and numeric alignment;
- neutral, brand, semantic, surface, text, border, focus, and selection color roles;
- radius, border, and elevation purposes;
- motion purpose plus reduced-motion response;
- icon grid, stroke/fill, corner, naming, and distribution rules.

Keep raw values behind intent-bearing roles at component boundaries. Treat numeric recipes as starting comparisons, not immutable laws.

## Define component contracts

For each shared component, specify:

1. User operation, purpose, and non-use.
2. Native semantic element/role and accessible-name source.
3. Data, validation, content extremes, and formatting.
4. Meaningful variants as explicit categories.
5. Default, hover when applicable, focus-visible, pressed, selected, loading, unavailable, error, success, and relevant screen states.
6. Keyboard, touch, pointer, assistive-technology, dismiss, and focus-return behavior.
7. Intrinsic/max geometry, reflow, order, overflow, and hover alternatives.
8. Trigger/rules/feedback/interruption and reduced-motion behavior.
9. Persistence, recovery, analytics/events, examples, counterexamples, and tests.

Use [component-contract.md](../../assets/component-contract.md) and [state-matrix.md](../../assets/state-matrix.md).

Replace incompatible boolean combinations with an explicit variant or state model. Split the component if its modes do not share a real semantic and interaction contract.

## Evolve safely

Classify internal refactoring separately from user-perceived change. For shared/public contracts:

1. Add the new token/API beside the old.
2. Bridge compatibility only where needed.
3. Migrate one bounded consumer.
4. Compare all relevant states, themes, semantics, and interactions.
5. Observe and then migrate remaining consumers.
6. Stop producing the old representation.
7. Preserve rollback through the agreed window.
8. Remove old code and docs only after consumer evidence is clear.

Do not remove a duplicate literal until supported themes/states consume the new role. Do not create a token for a one-off without reusable meaning.

## Verify the system claim

- Search for remaining literals, aliases, old consumers, and parallel implementations.
- Run static and focused component/contract checks.
- Inspect representative consumers in the final rendered runtime.
- Exercise states, keyboard/touch, responsive transformations, themes, locale expansion, and adverse content in proportion to risk.
- Prove one shared-rule change reaches intended consumers without changing unrelated ones.
- Preserve critical accessibility, privacy, authorization, and data-loss blockers independently of aggregate scores.

Report reused, added, rejected, migrated, deprecated, and removed system decisions separately. Label visual, static, focused, and end-to-end evidence precisely.

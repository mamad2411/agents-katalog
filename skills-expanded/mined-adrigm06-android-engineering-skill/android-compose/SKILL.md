---
name: android-compose
description: Jetpack Compose engineering skill for state modeling, recomposition control, stability, and UI architecture. Use whenever the user asks to build, review, optimize, or debug Compose screens and navigation flows.
---

# Purpose

Design and review Compose UI systems with predictable state, bounded recomposition, and architecture-aligned ownership under real product constraints.

## Scope and authority

This skill is the lead authority for:

- Compose UI state/event modeling
- recomposition and stability decisions
- navigation/event flow patterns inside UI layer boundaries
- composable decomposition and screen architecture

This skill must defer when applicable:

- structural boundaries to `android-architecture`
- runtime SLA hard constraints to `android-performance`
- security controls to `android-security`

## When to use

- building new Compose screens/components
- refactoring unstable state and recomposition hotspots
- defining event/navigation flow models
- auditing Compose architecture quality
- balancing UI quality with performance and delivery constraints

## Required inputs

Gather minimum decision-shaping inputs:

- screen complexity and user journey criticality
- current state holders and ownership boundaries
- jank/recomposition evidence (if performance concern exists)
- navigation complexity and cross-screen coupling
- team familiarity with Compose patterns and testing depth

If missing data blocks precision, continue with assumptions and confidence downgrade.

## Decision engine workflow

1. Classify screen/system complexity.
2. Select state model branch and ownership strategy.
3. Validate composable boundaries against architecture constraints.
4. Evaluate recomposition/stability risk using available evidence.
5. Resolve runtime tradeoffs with performance constraints.
6. Define testing and preview strategy by risk.
7. Return implementation plan with fallback options.

## Branching decision tree

### Branch A: UI complexity

- `Simple` (single-flow, low concurrency):
  - Prefer straightforward `UiState` sealed model + single state holder.
- `Moderate` (multiple async sources, conditional rendering):
  - Use richer `UiState` + explicit event reducer style.
  - Segment composables by responsibility and state domain.
- `High` (high interaction density, optimistic updates, cross-screen state):
  - Use explicit intent/event model, deterministic reducers, and effect channeling.
  - Tighten ownership boundaries and instrumentation.

### Branch B: state ownership

- Hoist to screen-level state holder when data drives multiple child composables.
- Keep local state only for ephemeral UI concerns (focus, transient toggles, animation state).
- If local state grows domain semantics, escalate ownership upward.

### Branch C: recomposition strategy

- If no jank evidence and moderate complexity:
  - prefer clarity-first decomposition; avoid premature micro-optimizations.
- If measured hotspots exist:
  - reduce unstable parameter propagation
  - isolate expensive subtrees
  - apply targeted memoization and state derivation controls

### Branch D: navigation/event modeling

- keep navigation events explicit and one-directional from state holder boundary
- avoid distributed navigation logic inside unrelated leaf composables

## Conflict handling and composition

When used with other skills:

- With `android-performance`:
  - measured runtime bottlenecks may require short-term UI compromises
  - document expected UX impact and reversion criteria
- With `android-architecture`:
  - Compose convenience cannot violate layer boundaries
  - reject data access shortcuts in composables
- With `android-testing`:
  - high interaction complexity requires stronger UI+integration coverage
- With `android-release-engineering`:
  - if release risk is high, prefer low-regression changes and stage risky refactors

## Real-world tradeoff guidance

Permit context-justified compromises when explicit:

- temporary mixed View+Compose interop is acceptable during migration
- partial state normalization is acceptable under deadlines with follow-up plan
- readability-first implementation is acceptable when performance evidence is weak

Avoid presenting temporary compromises as final best practice.

## Anti-pattern detection

- giant composables with mixed rendering, state mutation, and business logic
- unstable parameter graphs triggering broad recompositions
- overuse/misuse of `remember` or `derivedStateOf` without measurable benefit
- side effects hidden in render path
- navigation scattered across unrelated UI nodes

## Uncertainty protocol

Always report confidence:

- `High` (>= 0.80)
- `Medium` (0.60-0.79)
- `Low` (< 0.60)

For medium/low confidence:

- list assumptions and what evidence is missing
- provide at least one alternative state/structure strategy
- suggest the minimum instrumentation required to choose decisively
- escalate to `android-performance` or `android-architecture` when conflict is structural/runtime

## Cross-skill handoff payload

Use the standard payload defined in `../../AGENTS.md` (section: Cross-skill handoff contract).
Set `requesting_skill` to `android-compose`.

## Output contract

Follow global order from `../../AGENTS.md`:

1. `Context and constraints`
2. `Decision and rationale`
3. `Alternatives considered`
4. `Tradeoffs`
5. `Risks and mitigations`
6. `Confidence and unknowns`
7. `Cross-skill impacts`
8. `Next implementation steps`

Include Compose-specific artifacts:

- `UI state model`
- `Composable structure`
- `State hoisting strategy`
- `Navigation/events model`
- `Recomposition and stability risks`
- `Preview/testing plan`

## Related resources

- `references/compose-state-patterns.md`
- `examples/common-pitfalls.md`

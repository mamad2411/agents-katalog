---
name: frontend-core
description: Implementation pattern for a UI layer — component (presentation) → state (local/store) → data-fetch (API boundary). Keep components pure, isolate side effects, and cover states (loading/empty/error). Stack-specific (frontend).
version: 0.1.0
tier: stack
stack: [frontend]
owner: frontend
gates: [G2, G3]
related: [.ai/modules/frontend.md, api-contract, test-and-validation]
---

# Skill: frontend-core

## Purpose
A reusable UI layering so presentation, state, and data access stay separable and testable — independent of any host skill or specific framework.

## When to use
Building or changing UI: a component, a view, a store slice, or the data-fetch that feeds them.

## Pattern
```
component (presentation)  ->  state (local / store)  ->  data-fetch (API boundary)
```
- **Component**: pure render from props/state; no direct fetching. Handles loading / empty / error / success explicitly.
- **State**: local (`useState`/signals) or shared store; the single source of truth for the view. Side effects isolated here or in the data layer.
- **Data-fetch**: the only place that talks to the API; types/DTOs match the contract (see `api-contract`); errors normalized before reaching the component.

## Rules
- Presentation is pure and prop-driven — logic and fetching move down the layers.
- Every async view renders all four states (loading, empty, error, success).
- Accessibility and the design system are part of "done", not a follow-up.

## Checklist
- [ ] Component is pure/prop-driven; no fetch inside render
- [ ] Loading / empty / error / success all handled
- [ ] Data layer owns API calls; DTOs match the contract
- [ ] Unit tests for state logic + rendering of each state
- [ ] a11y (labels, focus, keyboard) checked

## Anti-patterns
- Fetching data inside a presentational component
- Only the happy path rendered (no error/empty states)
- Business logic embedded in JSX instead of the state layer

## Output
Component + state + data-fetch code in the project + tests; task status in `tasks.md`.

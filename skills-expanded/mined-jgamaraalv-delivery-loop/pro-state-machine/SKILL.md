---
name: pro-state-machine
description: Professional React state-machine patterns. Use when implementing complex state logic, reducers, multi-step forms, async flows, or any component coordinating multiple states.
---

# Pro State Machine

Professional state machine patterns for managing complex React application state, focused on making invalid states impossible through type-safe design.

## Architecture Philosophy

1. **Events Over State**: Capture user intent explicitly rather than mutating state directly
2. **Impossible States Prevention**: Use TypeScript's type system to make invalid states unrepresentable
3. **Separation of Concerns**: Keep pure state transitions separate from side effects

## Core Rules

- **Derive, don't store** — compute values during render instead of syncing them with `useState` + `useEffect`.
- **Model state as a finite state machine** — a single `status` discriminated union, never boolean flag soup (`isLoading`/`isError`/`isSuccess`).
- **Combine related state in a reducer** — atomic updates, no intermediate invalid states; `useState` only for simple independent values.
- **Drive side effects by events, not reactions** — one effect watches `status`, never cascading `useEffect` chains.
- **Fetch with a dedicated library** — TanStack Query or SWR over hand-rolled `useEffect` fetching.
- **Normalize entities** — flat maps keyed by ID, not deeply nested arrays.

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/derived-state.md` — why and how to compute derived values during render instead of storing them · read when a component syncs state with `useEffect` or holds totals/filters/computed strings in state.
- `references/finite-state-machines.md` — discriminated-union state with a single `status` field and exhaustive switches · read when modeling idle/loading/error/success or replacing boolean flag soup.
- `references/reducers.md` — combining related variables into one `useReducer` for atomic, testable transitions (booking-form example) · read when 3+ variables change together or transitions get complex.
- `references/event-driven-effects.md` — event-driven side effects: explicit actions + a single effect watching `status` (flight-search example) · read when you have cascading effects, race conditions, or unpredictable async flows.
- `references/data-fetching.md` — TanStack Query / SWR for queries and optimistic mutations, and when to use which · read when fetching server data or replacing manual `useEffect` + `useState` fetching.
- `references/form-state.md` — native `FormData` + `useActionState` + schema validation for multi-field/multi-step forms · read when building complex or multi-step forms.
- `references/normalization.md` — flat entity maps keyed by ID with selector functions for O(1) updates · read when state holds deeply nested arrays or updates require deep traversal.
- `references/testing-reducers.md` — testing pure reducers directly with Vitest (transitions and guard invariants) · read when writing tests for state logic.

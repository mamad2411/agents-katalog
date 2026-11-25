---
name: state-management
description: Architecture and implementation of predictable state models, finite state machines (FSM/Statecharts), unidirectional data flow, reactive signals, server cache sync, and optimistic rollback transactions.
---

# State Management Architecture & Engineering

## 1. Purpose
Design, engineer, and audit deterministic state management architectures across frontend and backend systems, eliminating impossible states, race conditions, memory leaks, and synchronization drifts through explicit Statecharts, unidirectional data flow, fine-grained reactivity, and optimistic transactional rollbacks.

---

## 2. Use When
- Designing complex application workflows, wizards, authentication flows, or distributed transactional sagas.
- Eliminating fragile boolean soup (`isLoading`, `isError`, `isSuccess`, `data !== null`) in favor of type-safe Finite State Machines (FSM).
- Architecting global client stores, caching layers, or server-state synchronization (React Query / TanStack Query, SWR, Apollo).
- Implementing fine-grained reactive primitives (Signals, Computed, Effects) with glitch-free topological updates.
- Managing concurrent asynchronous actions with cancellation (`AbortController`), debouncing, and optimistic UI mutations with rollback.

---

## 3. Do Not Use When
- Managing trivial, isolated single-component display states (e.g., an expandable accordion section adequately served by local boolean toggle).
- Writing raw relational database schemas or database migrations (use `database-review`).
- Simple static text or documentation pages without interactive or asynchronous state transitions.

---

## 4. Required Context
Before implementing or refactoring state logic, verify:
1. **Domain Workflow & State Boundaries**: Complete list of valid states, legal transitions, triggering events, and guard conditions.
2. **State Categorization**:
   - *Ephemeral UI State*: Component-scoped (e.g., dropdown open/close).
   - *Client Domain State*: Shared across features (e.g., user preferences, offline drafts).
   - *Server Cache State*: Remote data snapshot requiring invalidation, refetching, and hydration.
3. **Concurrency Requirements**: Handling of rapid out-of-order events, network latency, offline persistence, and mutation rollbacks.

---

## 5. Procedure

### Step 1: Model States and Transitions Formally (Make Impossible States Unrepresentable)
1. Categorize entities into discriminated union states rather than sets of independent booleans.
2. For multi-step or asynchronous workflows, define an explicit Finite State Machine:
   - Identify States: `Idle`, `Loading`, `Success`, `Failure`, `Retrying`.
   - Identify Events: `SUBMIT`, `FETCH_SUCCESS`, `FETCH_ERROR`, `RETRY`, `RESET`.
   - Identify Guards: Pure boolean predicates determining if a transition is legal.
   - Identify Actions: Side effects executed on transition (`entry`, `exit`, `transition`).

### Step 2: Implement Unidirectional Data Flow & Immutability
1. Ensure state transitions are strictly unidirectional:
   $$\text{Action/Event} \longrightarrow \text{State Transition Function} \longrightarrow \text{New Immutable State} \longrightarrow \text{View Subscription}$$
2. Enforce immutable updates (structural sharing via pure functions or tools like Immer); never mutate state objects in place.
3. Keep selectors pure, memoized, and composable to prevent unnecessary recomputations and re-renders.

### Step 3: Handle Asynchrony and Race Conditions
1. Tie every asynchronous fetch or side-effect to an explicit cancellation mechanism (`AbortController` in JS/TS, `context.Context` in Go, cancellation channels in Rust).
2. For rapid inputs (e.g., search autocomplete), cancel stale inflight requests before initiating subsequent requests.
3. Implement optimistic updates with a rollback snapshot:
   - Apply expected state to local store immediately.
   - Dispatch background mutation.
   - If mutation fails, restore previous snapshot and transition to `Error` state with user recovery options.

### Step 4: Fine-Grained Reactive Graph & Signals (When Applicable)
1. In reactive graph architectures, ensure signals maintain topological dependency sorting to prevent glitch artifacts (evaluating an effect with half-updated state).
2. Clean up effect subscriptions deterministically upon component unmount or state destruction to prevent memory leaks.

### Step 5: Verification & Contract Testing
1. Test all transitions with deterministic state transition tables:
   - Assert every event in each state produces the exact expected state.
   - Assert unhandled events are safely ignored or rejected without mutating state.
   - Assert error states recover cleanly on retry events.
2. Test race condition resilience under simulated network latency and out-of-order responses.

---

## 6. Decision Rules
1. **Discriminated Unions Over Multiple Booleans**: Never combine `isLoading: boolean`, `isError: boolean`, and `data: T | null`. Use:
   ```typescript
   type RequestState<T> =
     | { status: 'idle' }
     | { status: 'loading' }
     | { status: 'success'; data: T }
     | { status: 'error'; error: Error };
   ```
2. **Server State is Not Client State**: Never store raw database records permanently in a global Redux/Zustand store without an invalidation and cache synchronization policy. Prefer dedicated server-state caching engines.
3. **Pure State Transition Functions**: State reducers or machine transition handlers must be 100% pure, deterministic, and free of side effects. Side effects belong in explicit action dispatchers or effect handlers.
4. **Idempotence on Duplicate Events**: Processing the same event multiple times in the same state must not corrupt state or trigger duplicated network mutations.

---

## 7. Evidence Required
- **State Transition Matrix**: Automated test asserting 100% of state-event pairs defined in the specification.
- **Cancellation & Race Tests**: Test confirming inflight cancellations prevent stale overwrites.
- **Rollback Test**: Test asserting state is restored accurately after an optimistic update failure.

---

## 8. Output Contract
A production state management artifact must include:
1. Formal state machine or reducer specification with explicit types.
2. State transition logic and pure reducer implementation.
3. Side-effect and cancellation handlers.
4. Comprehensive transition test suite covering all states, transitions, and edge cases.

---

## 9. Stop Conditions
- All modeled states, transitions, and guards are covered by unit tests.
- Zero uncaught race conditions or memory leaks in subscription lifecycles.
- Optimistic updates gracefully handle both success and rollback paths.

---

## 10. Escalation Rules
- Escalate to Systems Architect if a proposed state architecture requires distributed consistency (2PC / Saga) across multiple microservices.
- Escalate to Security Team if sensitive credentials, tokens, or PII are exposed in persistent client state stores or unencrypted caches.

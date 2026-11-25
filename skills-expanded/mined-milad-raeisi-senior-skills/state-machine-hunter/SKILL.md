---
name: state-machine-hunter
description: Find every implicit state machine in an app and make it explicit without breaking anything. Use when the user asks to find hidden or implicit state machines, clean up flag soup (isLoading, isError, isSubmitting combinations), fix impossible or stuck UI states, race conditions, double submits, or flaky async flows, refactor loading/error/retry/polling logic, model a lifecycle (orders, uploads, auth sessions, connections, wizards, onboarding, payments, jobs), or improve the UX, DX, and agent experience (AX) of stateful code. Inventories every machine, picks the least invasive fix that removes impossible states, pins behavior with characterization tests, then refactors in small safe steps.
license: MIT
metadata:
  category: senior-five
  version: "1.2.0"
---

# State Machine Hunter

> *Find all of the implicit state machines in my app. Make the best decision that will elevate all three: the user experience (UX), developer experience (DX), and agent experience (AX), always, without breaking anything.*

Most "weird" bugs in stateful code are not logic errors. They are **states the code can represent but never meant to allow**: loading *and* errored, submitted twice, connected with no session, an upload that can't be cancelled. Every pair of booleans doubles the number of representable states, and almost none of the extra states are designed. Making the state machine explicit turns a class of runtime bugs into compile errors and gives every state a deliberate UX.

The work has five phases. Phases 1 to 3 are read-only; nothing changes until you have the full picture.

**Match the scope to the request.** When the user asks to find *all* the state machines (the prompt above), sweep the whole codebase. When the request is about one flow (a double submit, one stuck screen, one race), fix that machine with the same phases, and list any other machines you noticed as follow-ups instead of refactoring them uninvited.

## Phase 1: Hunt (read-only)

Sweep the whole codebase, not just the file in front of you. Machines hide in UI components, services, background jobs, database columns, and the gaps between them. Signals, strongest first:

- **Boolean clusters describing one thing**: `isLoading`, `isError`, `isSuccess`, `hasFetched`, `isSubmitting`, `isRetrying`. Two or more booleans about the same entity is almost always a machine.
- **Stringly typed status**: `status`, `state`, `phase`, `step`, `stage`, `mode` typed as `string` or `int`, compared against literals in many places.
- **Nullable fields that encode state**: `data: T | null` next to `error: Error | null`, or `deletedAt`, `archivedAt`, and `publishedAt` all on one row.
- **Check-and-set guards**: `if (!this.connecting) { this.connecting = true; ... }`. These are transitions without a machine, and the usual home of race conditions.
- **Timers and retries**: `setTimeout`, polling loops, backoff, `attempt` counters, debounce flags.
- **Transitions written in several places**: two services that both set `order.status = "paid"`.
- **Comments that admit it**: "should never happen", "shouldn't get here", "TODO race", `unreachable`.
- **Multi-step flows**: wizards, checkout, onboarding, file upload, auth and session refresh, WebSocket connections, payment intents, background job status, feature rollouts.

[references/patterns.md](references/patterns.md) has ready-made `rg` searches for these signals in several languages.

## Phase 2: Map each machine

For every candidate, write down:

| Field | Question |
|---|---|
| Name | What domain concept is this the lifecycle of? |
| Location | Every file and line that reads or writes the state |
| States | Which states are *actually* reachable today, including accidental ones? |
| Events | What causes each transition: user action, response, timer, webhook? |
| Impossible-but-representable | Which combinations can the types express but should never exist? |
| Missing transitions | Can the user cancel, retry, go back, or recover from every state? Any state with no exit? |
| Races | Can two events arrive in an order the code doesn't expect (double click, stale response, concurrent workers)? |
| Persistence | Is the state stored (DB, URL, local storage, queue) or exposed in a public API? |
| Tests | Which transitions are covered by tests today? |

Draw the machine as a Mermaid `stateDiagram-v2`. A diagram makes missing exits and dead states obvious in a way prose never does.

## Phase 3: Decide, one machine at a time

Score each machine on **pain** (observed bugs, confusion, support load), **risk** (blast radius, test coverage, persisted data, public API), and **payoff** for each audience:

- **UX**: every state has a designed screen or message (idle, loading, empty, partial, error with recovery, offline, cancelled); no stuck states; the user can always exit or retry.
- **DX**: the compiler enforces exhaustive handling; the lifecycle is readable in one place; names match the domain.
- **AX**: states are named constants an agent can grep; transitions live in one file; a diagram sits next to the code; tests are named after transitions, so the next agent can change the machine safely.

Then choose the **least invasive option that removes the impossible states**:

1. **Document only.** Add the diagram and name the states in a comment. Right when the machine is correct, stable, and untested enough that touching it is riskier than leaving it.
2. **Make the type honest.** Replace the booleans or strings with a discriminated union, enum, or sealed type where each state carries only its own data. Behavior stays the same. This is the most common win.
3. **Centralise transitions.** One `transition(state, event)` function; illegal transitions are rejected explicitly instead of silently ignored.
4. **Adopt a state-chart library** (XState, a workflow engine). Only for hierarchical or parallel states, many events, or real need for visualisation. Never for a three-state toggle.

Machines that are fine as they are still go in the inventory, with the reason you left them alone. "I checked and it's fine" is a finding.

## Phase 4: Refactor without breaking anything

"Without breaking anything" is a procedure, not a hope:

1. **Pin today's behavior.** Write characterization tests over the transitions that exist now, including the odd ones. If a machine can't be tested, downgrade it to "document only" and say why.
2. **Introduce the explicit type next to the old one.** Derive the old booleans from the new state (`const isLoading = state.status === "loading"`) so every call site keeps working.
3. **Migrate call sites in small commits**, running the tests after each.
4. **Make illegal states unrepresentable**: remove the old fields and add exhaustiveness checks (`assertNever`, `match` with no wildcard, linters such as `exhaustive` for Go).
5. **Respect boundaries.** Persisted values, URLs, event payloads, and public API shapes keep their wire format; map at the boundary. Changing stored data needs a migration plan and the user's approval.
6. **Separate bug fixes from refactors.** If the explicit machine exposes a real bug (a stuck state, a missing cancel), fix it in its own commit and call it out, because it is a behavior change.
7. **Remove the compatibility shims** once nothing reads them.

## Phase 5: Report

```markdown
## State machines found: N

| # | Machine | Where | States (today) | Problems | Decision |
|---|---------|-------|----------------|----------|----------|
| 1 | Checkout submit | src/checkout/*.tsx | 4 booleans, 16 combos, 5 reachable | double submit; stuck "processing" on timeout | Honest type + central transitions |
| 2 | Socket connection | src/net/socket.ts | strings: 3 | none observed | Document only (diagram added) |

### 1. Checkout submit
Before/after diagram, what changed, UX/DX/AX impact, tests added, behavior changes (if any).

### Left alone and why
### Follow-ups worth filing
```

## Guardrails

- Read-only until the inventory and decisions exist. Don't start refactoring the first machine you find.
- Don't introduce a library to model a machine the language can model with a union type.
- Don't rename persisted state values or public API fields as part of this work without explicit approval.
- Every changed machine ends with its tests passing and a diagram that matches the code.

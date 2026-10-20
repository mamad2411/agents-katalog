---
name: design-state-machine
description: Models a lifecycle (order status, connection, checkout/approval flow, device/job state) as an EXPLICIT finite state machine or statechart instead of boolean-flag soup — enumerate states + events as closed sets, define transitions as a total (state×event)→state function with guards and entry/exit actions, make the current state a single persisted column (not N booleans), reject every undefined (state,event) pair loudly, and reach for hierarchical/parallel/history statecharts (Harel/SCXML semantics, XState v5 setup/createMachine, or a hand-rolled transition table) once flat states explode combinatorially; persist with optimistic-lock guarded transitions, drive side effects from entry actions or an outbox, and test by asserting the full transition matrix including illegal-edge rejection.
when_to_use: A thing moves through named stages where only some transitions are legal and code is sprouting isPaid/isShipped/isCancelled flags, scattered if-ladders, or "how did it get into THIS state?" bugs — order/payment/subscription status, WebSocket/TCP connection lifecycle, multi-step wizard or approval workflow, document review, or a long-running job. Distinct from design-event-sourcing-cqrs (the append-only event LOG is the source of truth and state is a fold/projection over it; this skill models the state graph itself and may persist only the current state) and async-concurrency-correctness (races/locks/ordering between concurrent tasks; this skill models one entity's legal transitions, then uses a guarded write so concurrent transitions don't corrupt it).
---

## When to Use

Reach for this skill when an entity moves through named stages and only some moves are legal:

- "Order goes pending → paid → shipped → delivered, can also cancel/refund — model it properly"
- "We have `isPaid && !isShipped && !isCancelled` checks everywhere and they keep contradicting"
- "How did this row end up paid AND cancelled?" / "a refund fired on an unpaid order"
- "Connection lifecycle: connecting → open → reconnecting → closed with backoff"
- "Multi-step checkout / approval workflow / document review with back-and-forth"
- "Add a new status and half the if-ladders broke" / "illegal transition slipped through"
- "Should I use XState, or a transition table, or just an enum?"

NOT this skill:
- The append-only **event log is the source of truth** and state is rebuilt by folding events, with separate read models → design-event-sourcing-cqrs (this skill models the legal-transition graph and may persist only the *current* state; you can combine them — an FSM that emits events into a log)
- **Concurrency** between tasks — locks, ordering, races, async correctness → async-concurrency-correctness (this skill defines one entity's legal moves; it then *uses* a guarded/optimistic write so two concurrent transitions don't corrupt the row)
- **Distributed mutual exclusion / leader leases** across nodes → distributed-locks-leases
- **Workflow orchestration across multiple agents/services** (sagas, fan-out, retries) → orchestrate-agent-workflow (use this skill to model each participant's local state)
- **Idempotent retries** so a replayed transition command is a no-op → idempotency-keys (this skill makes the transition function; that makes invoking it twice safe)
- The **DB column type / safe migration** to add the status column or new enum value → db-migration-safety; **how the enum evolves** without breaking old readers → schema-evolution-compatibility
- A **front-end multi-step form's** validation/field state → build-form-validation; client/server cache sync → manage-client-server-state

## Steps

1. **Enumerate states and events as two CLOSED sets first — on paper/in a table before any code.** A state is a *named condition the entity rests in* (`pending`, `paid`, `shipped`); an event is a *named trigger that may cause a move* (`Pay`, `Ship`, `Cancel`). Keep them disjoint and finite. The single best diagnostic that you need this skill: you have ≥3 booleans describing one entity and not all `2^n` combinations are valid. `isPaid + isShipped + isCancelled` admits "shipped but not paid" and "paid and cancelled" — nonsense states the type system permits. Replace them with one `status` enum whose values are *exactly* the legal conditions. **Make illegal states unrepresentable.**

2. **Define the transition as a total function `(state, event) → state` with guards, entry/exit actions — a TABLE, not scattered `if`s.** This table is the entire spec; review it like one. Anything not in the table is illegal by default.

   | From | Event | Guard (must be true) | To | Entry action (on arrival) |
   |---|---|---|---|---|
   | `pending` | `Pay` | amount == order.total | `paid` | capture funds, emit `OrderPaid` |
   | `pending` | `Cancel` | — | `cancelled` | release inventory |
   | `paid` | `Ship` | inventory.reserved | `shipped` | create shipment, notify |
   | `paid` | `Refund` | — | `refunded` | reverse charge |
   | `shipped` | `Deliver` | — | `delivered` | close order |
   | `shipped` | `Refund` | within return window | `refunded` | reverse charge, RMA |

   - **Guard** = boolean precondition; if false, the event is *rejected* (transition does not fire), not an error-state. `pending --Pay[amount≠total]-->` simply doesn't move.
   - **Entry action** runs on *every* arrival into a state (idempotent, since you may re-enter); **exit action** runs on leaving. Prefer entry actions over per-transition actions so the side effect is tied to *being in* the state, not the path taken.
   - `delivered`, `cancelled`, `refunded` are **terminal** — no outgoing transitions. Mark them; assert nothing leaves.

3. **Reject undefined `(state, event)` pairs LOUDLY — the rejection is the feature.** The whole point over flag-soup is that an out-of-order event can't silently corrupt state. The transition function must, for any pair not in the table, return a typed rejection (don't throw for *expected* business rejections; throw/log for *impossible* ones). Distinguish:
   - **Guard-failed** (legal event, precondition not met) → 409/422, "cannot Ship: inventory not reserved", state unchanged.
   - **Illegal event for state** (`Ship` while `cancelled`) → 409 + log/metric `illegal_transition{from,event}`; this often signals a real bug (double-click, replayed message, race) and you *want* the alarm.
   ```ts
   function transition(s: State, e: Event, ctx): Result<State> {
     const row = table[s]?.[e.type];
     if (!row) return reject("illegal", `${e.type} not allowed in ${s}`); // not in table at all
     if (row.guard && !row.guard(e, ctx)) return reject("guard", row.why);
     return ok(row.to);
   }
   ```
   Never write `if (status !== 'cancelled') { ... }` ad hoc — that's flag-soup creeping back. Route *every* change through the one function.

4. **Persist the current state as ONE column and make the write a guarded compare-and-set so concurrent transitions can't corrupt it.** Store `status` as a single enum/text column with a CHECK or DB enum constraint — not N booleans, not a separate row per flag. The transition write must be conditional on the *expected* from-state (optimistic concurrency), so two racing transitions don't both "succeed":
   ```sql
   UPDATE orders SET status = 'shipped', version = version + 1, updated_at = now()
   WHERE id = $1 AND status = 'paid' AND version = $2;   -- 0 rows affected ⇒ someone else moved it; reject & re-read
   ```
   `WHERE status = <expected_from>` is the cheap optimistic lock; 0 rows updated means the precondition no longer holds → reload and re-decide, never blind-overwrite. Add a `status_history(order_id, from, to, event, actor, at)` audit row in the same transaction so "how did it get here?" is answerable. (For locking semantics → async-concurrency-correctness; for making a re-sent command idempotent → idempotency-keys.)

5. **Drive side effects from entry actions, and make external effects atomic-with-the-state-change via an outbox.** A side effect that must happen *because* you entered a state (charge, email, shipment) belongs in that state's entry action, so it fires on every path in and only once. But "update status row" + "call Stripe/send email" as two separate operations can crash between them (state changed, effect lost — or effect fired, state didn't). Write the status change AND an `outbox` row in **one DB transaction**; a relay publishes the outbox at-least-once and consumers dedup. This keeps the FSM's state and its observable effects consistent. (Outbox/dedup mechanics → idempotency-keys; emitting domain events into a log instead → design-event-sourcing-cqrs.)

6. **When flat states explode combinatorially, go hierarchical/parallel/history (statecharts) — don't multiply states.** Harel statecharts (the basis of SCXML and XState) add three tools that kill state explosion:
   - **Hierarchy (nested/compound states):** group `connecting`/`open`/`reconnecting` under a parent `online`; a single `Disconnect` transition on the parent applies to all children — write the common edge once instead of N times.
   - **Parallel (orthogonal regions):** independent concerns that vary simultaneously become separate regions instead of the cross-product. A media player's `{playing|paused} × {muted|unmuted}` is 2 regions, not 4 states; add a third dimension and you avoid `2×2×2 = 8`.
   - **History states:** re-entering a compound state resumes the last active child (`H` shallow / `H*` deep) — for "resume where the wizard left off" or reconnect-to-prior-substate.

   Rule of thumb: a handful of states + a clear table → **hand-rolled transition table** (zero deps, fully testable, easiest to review). Nesting/parallelism/history, or you want a visualizer and typed `assign` context → **XState v5** (`setup({ types, actions, guards }).createMachine({...})`, `actor.send(event)`, statelyai inspector). Cross-language/standards interop → **SCXML**. Don't reach for a library for 3 states; don't hand-roll 4 orthogonal regions.

7. **Model time/retries as real states + events, not sleeps buried in code.** `reconnecting` with a `backoff` timer is a state; the timer firing is an event (`RetryTimeout`) that transitions back to `connecting` (or to `failed` after `attempts >= max`, a guard on context). Keep the retry count in machine context, not a module global. This makes the backoff policy reviewable in the table and testable without real clocks. (The retry *policy* — jitter, budget, circuit-breaker → resilience-timeouts-retries; this skill places those decisions as guarded transitions in the lifecycle.)

8. **Visualize and review the graph; treat unreachable/trap states as bugs.** Generate a diagram from the table (XState → Stately inspector; hand-rolled → emit Mermaid `stateDiagram-v2`, see mermaid-diagram) and eyeball it for: a **trap** (non-terminal state with no outgoing edge — entity gets stuck), an **unreachable** state (no incoming edge — dead enum value), and a **missing terminal** (a "done" that still has edges). Every non-terminal state should have at least one path to a terminal/expected state. A new status added without table edges shows up immediately as an orphan node.

9. **Test the full transition MATRIX, including the illegal edges — that's the differentiator.** For every `(state, event)` pair: assert legal ones land in the right target and run the entry action exactly once; assert *illegal* ones leave state unchanged and return the typed rejection (and emit the `illegal_transition` metric). Property test: from any reachable state, applying any event either transitions per the table or rejects — it never produces a state outside the enum. Add a concurrency test: two parallel `Ship` on the same `paid` order → exactly one wins (guarded UPDATE), the other gets 0-rows-and-reject. (Structure the suite → write-tests; the matrix-as-cases is a natural fit for test-data-factories/property-based-testing.)

## Common Errors

- **Boolean-flag soup (`isPaid && !isShipped && !isCancelled`).** N booleans encode `2^n` combinations but only a few are legal; contradictory states ("shipped, not paid") become representable and *do* happen. Fix: one `status` enum = exactly the legal conditions; make illegal states unrepresentable.
- **Transition logic scattered across `if`-ladders in controllers/services.** No single place owns "what's legal"; a new caller forgets a guard. Fix: one transition function + table; route 100% of changes through it.
- **Silently ignoring out-of-order events.** `if (status === 'paid') ship()` with no `else` swallows a `Ship` on a `cancelled` order — masking double-clicks, replays, races. Fix: explicit reject + log/metric `illegal_transition`; the alarm is the value.
- **Blind `UPDATE ... SET status = 'shipped' WHERE id = ?`.** No from-state guard → a stale/concurrent writer overwrites a state it never saw. Fix: `WHERE status = <expected_from> AND version = ?`; 0 rows ⇒ re-read and re-decide.
- **Side effect outside the state transaction.** Charge fires, then the status write crashes (or vice versa) → state and effect diverge. Fix: status change + outbox row in one transaction; relay publishes; consumers dedup (idempotency-keys).
- **Entry action that isn't idempotent.** Re-entering a state (retry, replay) double-sends the email/double-charges. Fix: idempotent entry actions, or gate the effect on the *transition* having actually committed.
- **State explosion from flattening orthogonal concerns.** Modeling `{playing,paused}×{muted,unmuted}` as 4 flat states, then 8, then 16. Fix: parallel regions (one per independent concern); they compose instead of multiply.
- **Reaching for a heavy library for 3 states** (or hand-rolling 4 orthogonal regions). Fix: match the tool to the shape — table for flat/small, XState for hierarchy/parallel/history, SCXML for cross-language.
- **Trap / unreachable states.** A non-terminal state with no exit (stuck forever) or an enum value with no incoming edge (dead). Fix: visualize the graph; assert reachability and that every non-terminal has an outgoing edge.
- **Timers/retries as `sleep()` buried in handlers.** Backoff logic invisible to the spec, untestable without real time. Fix: model `reconnecting`/`RetryTimeout` as state+event with the attempt count in context.
- **Adding a status without updating the table.** New enum value, old if-ladders don't handle it → falls through to a default branch silently. Fix: the table is the spec; a new state with no edges is an orphan the visualizer/tests catch.

## Verify

1. **No flag soup:** grep the diff for `is<X> && !is<Y>`-style combinations on one entity; the state is a single enum/column, and contradictory combinations are no longer representable.
2. **One transition function:** every status mutation routes through the single `transition(state,event)`; no ad-hoc `SET status =` or `if (status !== ...)` outside it (grep for stray status writes).
3. **Illegal edges rejected:** for the full `(state,event)` matrix, illegal pairs leave state unchanged and return the typed rejection + emit `illegal_transition`; guard-failures return 409/422 with a reason, not a crash.
4. **Legal edges + entry actions:** each table transition lands in the correct target and runs its entry action exactly once (assert via spy/counter), even on a re-entry path.
5. **Guarded persistence:** the UPDATE is conditional on the expected from-state (and version); a test with two concurrent transitions on the same row shows exactly one commits, the other gets 0-rows-and-reject.
6. **Atomic effects:** status change and external-effect publish are in one transaction (outbox); kill the process between them → on restart the relay still publishes (effect recorded iff state changed), no orphan/lost effect.
7. **Graph is sound:** generated diagram has no trap (non-terminal with no exit), no unreachable state (no incoming edge), terminals truly terminal; every non-terminal reaches a terminal.
8. **Statechart features (if used):** a parent transition applies to all nested children (written once); parallel regions vary independently; a history state resumes the prior child.
9. **Property test holds:** from any reachable state, any event either transitions per the table or rejects — never yields a value outside the state enum.

Done = the lifecycle is one persisted enum driven by a single total transition function with explicit guards and entry/exit actions, every illegal `(state,event)` pair is rejected loudly (not silently swallowed), persistence is a from-state-guarded compare-and-set, side effects are atomic with the state change via an outbox, hierarchy/parallel/history are used only where flat states would explode, and the full transition matrix — legal AND illegal edges plus the concurrent-write race — is proven by the tests in checks 3–9.

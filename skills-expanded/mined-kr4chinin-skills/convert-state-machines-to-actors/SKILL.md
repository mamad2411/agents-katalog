---
name: convert-state-machines-to-actors
description: Convert a database-backed implicit state machine to an actor, the one owner every writer of the persisted state goes through. Use when asked to put writers behind one owner, or to fix a race or lost update across several writers, such as a find-implicit-state-machines finding.
---

# Convert implicit state machines to actors

An actor is the one owner of a process's persisted state: writers send it
events instead of writing. It is a function run per event with nothing kept
in memory; the database is the authority, so the actor holds across replicas
and restarts.

Input: findings from `find-implicit-state-machines`, a `path:line` or a
ticket. Keep the finder's label: convert **Confirmed**; convert **Likely**
only after its step 2 test goes red, unless the user asked for one owner; a
**Smell** only on request. For several findings, see
[Several machines](#several-machines).

One conditional write (`UPDATE ... WHERE status = :expected`, checking the
row count) is often the whole fix. Build an actor only when one conditional
write cannot cover the writers or the user asks for one owner; otherwise
recommend the conditional write and stop. If the writers are not known yet,
decide after step 3.

## 1. Check for existing work

Read recent history of the files and look for open branches or pull requests
on the same code. Report any change that covers the finding. Stop if it
does, unless the user asked for one owner; then stop only if a change
already makes that conversion.

## 2. Reproduce

Write a test that replays the finding's event sequence and asserts its reason
(the final state, the error), so it goes red for that reason only. A
sequential defect replays in order. A race runs its writers in two
independent sessions on the production engine, major version, isolation level
and pooling mode; mocks, in-memory fakes and a shared process lock prove
nothing about replicas. Force the interleaving from the database: hold the
row lock or key from a second connection, or, on a store that never blocks,
put a barrier in the test between each writer's read and write. A hook added
to the code for that barrier is active in tests only.

- **Red** on repeated runs: continue.
- **Green** after the sessions really interleaved in the finding's order
  (both read before either wrote): report that it did not reproduce, with
  what you tried; the finder's label stays. Stop, unless the user asked for
  one owner; then continue with the baseline below. Without that order, the
  step is blocked.
- **Blocked** (another engine or settings, a harness that wraps each test in
  one transaction): fix the harness where you can (Django
  `TransactionTestCase`, a test database on the production engine) and rerun;
  otherwise report the blocker.

When the user wants one owner and there is no defect, pin today's behaviour
with green tests of the sequences that matter, written before any change.
They stand in for the red test.

## 3. Inventory the writers

Find every path that writes the state: search by column, table, repository
method and raw SQL across handlers, workers, schedulers, consumers, CLI and
admin tools, seeds, fixtures, migrations, backfills and generic whole-entity
saves. Check the database (triggers, cascades, grants) and whether another
service writes the table.

| Writer | `path:line` | Guard today | After: actor, bypass (why) or out of band |
| ------ | ----------- | ----------- | ----------------------------------------- |

A **bypass** is a writer in this repository that stays outside the actor,
listed with its reason. **Out of band** is a writer outside this repository,
such as another service. End with `writers outside this repository: unknown`
unless the user named them; a local search proves nothing about other
repositories. Done when every hit is classified; if one conditional write
then covers the runtime writers in this repository and the user did not ask
for one owner, recommend it and stop.

## 4. Design the actor

1. **Machine.** A pure `(state, event) -> next state and effects | rejected`
   function: no I/O, clock or randomness (the actor stamps the time on the
   event). Use a statechart library only if the project has one, after
   reading [statechart libraries](references/statechart-libraries.md). A delay
   is a persisted due time plus the existing scheduler, never a timer in
   memory.
2. **Actor.** The only entry point. Per event: read the state and every guard
   input, run the transition, and commit the new state, the receipt (the
   stored outcome of this event key) and the effects as one atomic bundle
   the database accepts only if what was read still holds. A rejected event
   changes no state and sends no effects; where its key must keep its answer
   (a client idempotency key), record the rejection as its receipt. A replay
   the current code answers with success still gets that success. Logs and
   metrics go after commit.
3. **Persistence.** Keeps every guarantee the write path has today: locks,
   versions, unique constraints, receipts, outbox.

Read [guarded writes](references/guarded-writes.md) and answer each item that
applies.

A call to another system cannot join the transaction. If its result must move
the state, persist an awaiting state (`pending`, request id, parameters)
first; the result is a second event. If delivery can wait, write it to an
outbox in the same transaction. An unknown outcome goes to a reconciler
shipped with the change, never to a blind resend. Read
[external effects](references/external-effects.md) before designing either
path.

Ask the user, with two to four options and a recommendation, before a schema
change, a new error in a public API, an external call with an unknown outcome
and no idempotency key the receiver stores (or its automatic resend), a
writer that cannot go through the actor, or a store that cannot commit the
bundle atomically.

Done when each part names its table, guard and code location, each external
call names its awaiting state and sender, and each of those cases the design
takes has the user's answer.

## 5. Write the scenario table

Before coding, write
`precondition | events | expected state | effects and response | test`, one
test per row. Cover what applies: the same event twice, a retry after an
unknown outcome, a redelivery after commit; two writers in both orders, in
separate sessions; a stale result, cancel or teardown; a crash after an
external call or between commit and relay; a rollback; concurrent first
writes; stored states the new machine does not know. A row is n/a only with a
`path:line` showing the sequence cannot happen; the new design is no such
evidence.

## 6. Implement

- Move every runtime writer in this repository to the actor and delete its
  old write path. Generic saves stop writing the state column; a test shows
  that a stale loaded state does not land.
- Keep applied migrations. Seeds and fixtures may insert the initial state as
  listed bypasses; any other bypass takes the same guard and commits the
  same receipt and effects.
- Old binaries keep running during a rolling deploy: a new column stays
  nullable and outside the guard until they are drained, and the first guard is
  a predicate they already store (usually the status). Until then they can
  still overwrite the actor's commit; if that window is not acceptable, ask
  whether to first guard the old paths or to drain them before the actor
  takes traffic.
- Before the machine rejects a stored state, list the states the current code
  can write and those in the data (a bounded query the user agrees to). Each
  keeps a path until its rows are resolved; a backfill is the user's call.

Done when every inventory row reads actor, bypass or out of band, and the
project builds.

## 7. Verify

- The step 2 test is green. For a race, the database decided the loser: it
  waited on the lock and then read the winner's state, or its guarded write
  hit zero rows, a conditional-check failure or a unique violation. A lock
  wait alone or a correct final row is not enough.
- Every scenario row passes, effects and responses included; race tests pass
  on repeated runs; the existing suite is green.
- A fresh search finds writes only in the actor and listed bypasses.
- Each outside writer is converted, guarded or absent; otherwise the race is
  not proven fixed for the unknown ones.

The defect counts as fixed only after old binaries are drained. Then hand
commit and review to the project's usual workflow.

## Several machines

Write a plan next to the finding report, or where the project keeps plans,
one row per actor: `actor | writers that move | red or baseline test`, with
actors that share a write path in sequence. Ask once whether to do all of
them or a pilot. Convert one actor per change, each through steps 1 to 7 with
that test. Local loops (quotas, rate limits, backoff, worker lifecycle) stay
with their owners unless they write shared persisted state. Done when every
finding has passed step 7 or has a stated reason.

## Report

In the user's language:

1. What went from red to green (or the baseline that stayed green): the test,
   the guard and, for a race, what the database did to the losing session.
2. The writer inventory, bypasses with reasons, outside writers.
3. Scenario rows marked n/a, each with its `path:line`.
4. What is left: remaining actors, open decisions, the rollout window.

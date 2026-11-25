---
name: design-event-sourcing-cqrs
description: Designs event-sourced and CQRS systems — past-tense immutable event schemas, aggregate boundaries with command→validate→emit→apply and expected-version optimistic concurrency, append-only per-stream event store with outbox publishing, rebuildable idempotent projections, snapshotting, and versioned upcasting for event evolution.
when_to_use: When you need an audit-complete, replayable, append-only domain model (ledgers, order/workflow state machines, compliance) or are splitting write commands from read queries, or fixing event-sourcing pain (projection lag, frozen event shapes, slow rebuilds, lost ordering). For plain CRUD use db-migration-safety; for the messaging transport use message-queue-jobs.
---

## When to Use

Reach for this skill when the domain needs **the history of changes as first-class truth**, not just the current row:

- "We need a full audit trail / who-changed-what-when that nobody can edit after the fact"
- "Model an order / loan / subscription as a state machine with replayable transitions"
- "Build a ledger or balance that must reconcile to zero from its entries"
- "Separate the write side (commands) from a denormalized read side (queries)"
- "Time-travel: rebuild what the state *was* at any past moment"
- Fixing existing pain: projection lag, "we can't change the shape of a 2-year-old event", multi-hour rebuilds, lost per-aggregate ordering, eventual-consistency bugs in the UI

NOT this skill:
- Plain CRUD with mutable rows and no replay need → **db-migration-safety** (and stop here — event sourcing is the wrong tool for simple CRUD)
- The broker/transport that *carries* events (Kafka/SQS/RabbitMQ delivery, retries, DLQ) → **message-queue-jobs**
- A read-only cache layer to cut DB load → **caching-strategy** (a projection is a system of record for reads; a cache is disposable)
- Syncing offline client state with conflict resolution → **build-offline-first-sync**
- Recording *why you chose* event sourcing as a decision → **write-adr**
- Tuning the projection's query/index once it exists → **optimize-sql-query**
- Wiring client UI state to the read API → **manage-client-server-state**

## Steps

1. **First, decide if event sourcing is even warranted — most apps should not use it.** Adopt it only when ≥1 of these is a hard requirement, and accept the listed cost:

   | Driver (need ≥1) | Why ES wins | Cost you take on |
   |---|---|---|
   | Audit/compliance: immutable, complete history | Events *are* the audit log, tamper-evident | More moving parts than a table |
   | Temporal queries / "state as of T" | Replay to any point | Rebuild + snapshot machinery |
   | Complex state machine w/ many transitions | Each transition = one fact | Up-front modelling effort |
   | Multiple read shapes from one write model | CQRS projections, independent scaling | Eventual consistency everywhere |
   | Debugging by replaying real history | Deterministic reproduction | Replay must stay deterministic forever |

   If none apply → use a normal table with CRUD and an `updated_at`; **do not event-source CRUD.** CQRS (split read/write models) is independently useful and does **not** require event sourcing — you can do CQRS over a normal DB.

2. **Model events as immutable, past-tense facts — name them as business outcomes, never CRUD verbs.** `OrderPlaced`, `PaymentCaptured`, `FundsWithdrawn`, `ShipmentDispatched` — not `OrderUpdated`/`OrderSaved`/`SetStatus`. An event records *what happened*, is append-only, and never carries read-model concerns (no denormalized display strings, no joined names, no computed totals the reader could derive). Event payload contract:

   ```json
   {
     "event_id": "uuid-v4",                 // unique; the consumer dedup key (idempotency)
     "event_type": "FundsWithdrawn",        // past tense, business fact
     "event_version": 1,                    // schema version of THIS type
     "aggregate_id": "acct-9c1f",           // the stream key
     "aggregate_type": "Account",
     "sequence": 42,                        // per-aggregate, gap-free, monotonic = the version
     "occurred_at": "2026-06-15T09:30:00Z", // business time captured at emit, NEVER now() in apply
     "data": { "amount_cents": 5000, "currency": "USD" },
     "metadata": { "causation_id": "...", "correlation_id": "...", "actor": "user-7" }
   }
   ```
   Keep `data` minimal and self-contained: only facts the writer *decided*, expressed in raw value types. Put tracing/identity in `metadata`, never in `data`.

3. **Draw aggregate boundaries = the consistency boundary, and keep them small.** An aggregate is the unit that enforces an invariant in a single transaction (e.g. "balance never goes negative"). One command mutates exactly **one** aggregate atomically. Command flow is always **load → validate → emit → apply**:

   ```
   handle(cmd):
     events = load_stream(cmd.aggregate_id)        # replay history
     state  = events.reduce(apply, initial())      # rebuild current state in memory
     if not invariant_holds(state, cmd):           # VALIDATE against rebuilt state
        raise Rejected(reason)                      # rejection is NOT an event
     new = decide(state, cmd)                       # EMIT new past-tense events
     append(cmd.aggregate_id, new,
            expected_version = state.version)        # optimistic concurrency
     return new
   ```
   Rules: validation reads only the aggregate's own rebuilt state (no cross-aggregate reads, no querying a projection to decide). Cross-aggregate consistency is achieved *eventually* via a process manager/saga reacting to events, not in one transaction. A giant aggregate ("the whole tenant") serializes all writes — split it.

4. **Make the store append-only, ordered per stream, with expected-version concurrency.** One stream per aggregate; `sequence` is gap-free and monotonic *within a stream* (do not assume a global total order across streams). Append is a conditional insert:

   ```sql
   CREATE TABLE events (
     global_position BIGSERIAL PRIMARY KEY,        -- store-wide read order for projectors/relay
     event_id        UUID NOT NULL UNIQUE,         -- carried to broker; consumer dedup key
     aggregate_id    TEXT NOT NULL,
     aggregate_type  TEXT NOT NULL,
     sequence        INT  NOT NULL,                -- per-stream version: append uses expected_version+1
     event_type      TEXT NOT NULL,
     event_version   INT  NOT NULL,
     data            JSONB NOT NULL,
     metadata        JSONB NOT NULL,
     occurred_at     TIMESTAMPTZ NOT NULL,         -- business time, set by writer (not now())
     recorded_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
     UNIQUE (aggregate_id, sequence)               -- THIS enforces optimistic concurrency
   );
   ```
   An aggregate's `version` == the `sequence` of its last appended event. The append SQL inserts rows with `sequence = expected_version + 1, +2, …`. The `UNIQUE(aggregate_id, sequence)` violation = a concurrent writer won the race → catch it (`23505` in Postgres), reload, re-validate, retry (or return `409 Conflict` to the caller). `event_id` must be persisted, not regenerated — it's what every downstream consumer dedupes on. **Never** `UPDATE`/`DELETE` an event row; corrections are new compensating events (`ChargeRefunded`, not a delete).

5. **Publish via the outbox/transactional pattern — never dual-write.** Writing to the event store *and* publishing to the broker as two separate operations loses or duplicates events on crash. Instead: the event row **is** the outbox. Commit the event in the same DB transaction as the aggregate write, then a separate relay polls `events` ordered by `global_position` (or uses CDC/`LISTEN`) and pushes to the broker, tracking a high-water mark. Consumers must be idempotent (dedupe on `event_id`) because the relay guarantees **at-least-once**.

6. **Build read models as rebuildable, idempotent projections — and surface eventual consistency.** A projection subscribes to the event stream in `global_position` order and writes a denormalized read table. Two non-negotiables:
   - **Idempotent**: store the last processed `global_position` per projection; on replay skip anything `<=` it, and make each apply an upsert keyed by the event's natural id so re-delivery is a no-op.
   - **Rebuildable from zero**: a projection must be reconstructable by `TRUNCATE read_table; reset checkpoint to 0; replay all`. If it can't, it's a hidden write model — fix it.
   Reads are stale by the projection lag (ms→s). Make that explicit: return a version/`as_of` position with reads, and for read-your-writes either route the writer to a freshly-projected read or have the client wait until the projection checkpoint ≥ the position its write returned. Do not pretend the read side is synchronous.

7. **Bound replay with snapshots — but rebuild must still work from zero without them.** When a hot aggregate has thousands of events, replaying all of them per command gets slow. Snapshot = a serialized aggregate state at a known `sequence`, stored in a separate `snapshots` table. Load = newest snapshot ≤ head, then replay only events after it. Defaults: snapshot every **N=100–500** events per aggregate, keep the latest 1–2, and treat snapshots as a **disposable cache** — they're derived, deletable, and a full rebuild from event 0 must produce byte-identical state. Never let business logic read from a snapshot that the event log couldn't reproduce.

8. **Evolve schemas by versioning + upcasting, with lenient deserialization — you can never edit old events.** Old events are immutable history; you migrate them *on read*. Bump `event_version` for any non-additive change and register an upcaster chain that transforms `v1 → v2 → … → current` before the event reaches `apply`:

   | Change | Safe? | How |
   |---|---|---|
   | Add optional field w/ default | ✅ additive | Lenient deserializer fills default; no version bump needed |
   | Rename field | ⚠️ | Bump version; upcaster maps old→new name |
   | Split/merge fields, change units (dollars→cents) | ⚠️ | Bump version; upcaster computes new shape |
   | Remove a field still read by a projector | ❌ | Keep reading it via upcaster default; never drop in place |
   | Change the *meaning* of an event type | ❌ | Introduce a **new** event type; leave the old one |

   Deserialize leniently (ignore unknown fields, default missing ones) so a forward-deployed reader survives a slightly newer/older payload during rollout.

9. **Detect and repair projection drift.** Projections silently diverge (a bug skipped an event, a deploy reset a checkpoint wrong). Build a reconciliation job that recomputes a checksum/aggregate from the event log and compares to the read model; on mismatch, rebuild that projection from zero (it's safe because projections are idempotent + rebuildable). A blue/green projection swap (build the new table fully, then atomically repoint reads) lets you rebuild without downtime.

## Common Errors

- **Event-sourcing plain CRUD.** No audit/temporal/state-machine need → you bought replay/snapshot/upcasting machinery for nothing. Use a table.
- **CRUD-named events** (`OrderUpdated`, `EntitySaved`, `SetField`). They carry no business meaning and force readers to diff state. Name the *fact*: `OrderShipped`, `PriceReduced`.
- **Read concerns leaking into events** — denormalized display names, joined data, computed totals. The event is now coupled to a read shape and breaks when the read model changes. Store only the writer's decided facts.
- **Giant aggregate.** "Account" containing every transaction of every user serializes all writes and replays forever. Scope the aggregate to the smallest invariant boundary.
- **No expected-version on append.** Two concurrent commands both read version 41 and both write 42 → lost update / broken invariant. Enforce `UNIQUE(aggregate_id, sequence)` and retry on conflict.
- **Dual-write to store and broker.** A crash between the two loses or duplicates events. Use the outbox (the event row) + a relay; make consumers idempotent.
- **Non-deterministic replay** — `apply` calls `now()`, `random()`, or a remote service, so rebuild ≠ original. Capture all nondeterminism *into the event* at emit time; `apply` must be a pure fold.
- **Non-idempotent projector.** Re-delivery (at-least-once) double-counts. Track per-projection `global_position` and make applies upserts keyed by a natural id.
- **Validating against a projection instead of the rebuilt aggregate.** The projection is stale, so the invariant check races. Always rebuild the aggregate's own state from its stream to decide.
- **Treating rejections as events.** A failed/declined command must not append `OrderRejected` unless the *rejection itself is a meaningful business fact*; otherwise return an error — don't pollute the log.
- **Editing or deleting old events to "fix" them.** Destroys auditability and breaks every existing projection's replay. Append a compensating event instead.
- **Snapshot used as source of truth.** If the log can't reproduce the snapshot, a snapshot bug becomes permanent corruption. Snapshots are a disposable cache.
- **Assuming a global event order across aggregates.** Per-stream order is guaranteed; cross-stream is not. Don't build invariants that need two streams ordered together — use a saga.

## Verify

1. **Round-trip determinism:** replay an aggregate's full stream twice into fresh in-memory state → byte-identical result; replaying with vs without a snapshot → identical state.
2. **Optimistic concurrency:** fire two commands against the same aggregate at the same `expected_version` **in parallel** → exactly one commits, the other gets the `UNIQUE(aggregate_id, sequence)` violation (`23505`) surfaced as `409 Conflict` and succeeds only after reload+retry. The stream has no gap and no duplicated `sequence`.
3. **Projection rebuild:** `TRUNCATE read_table`, reset checkpoint to 0, replay all events → read model is bit-identical to its pre-truncate state. This proves it's rebuildable, not a hidden write model.
4. **Idempotent projector:** replay the same event slice twice → read rows and the checkpoint are unchanged after the second pass (no double counts).
5. **Outbox at-least-once:** kill the relay mid-publish, restart → every event reaches the broker at least once, consumers dedupe on `event_id`, no event lost.
6. **Upcasting:** feed a stored `event_version: 1` payload through the upcaster chain → it deserializes to current shape and `apply` accepts it; a lenient-deserialize test with an unknown extra field still loads.
7. **Drift detection:** intentionally skip one event in a projection → the reconciliation checksum job flags the mismatch, and a rebuild from zero repairs it.
8. **Eventual consistency surfaced:** a write returns a position; a read issued before the projector catches up is detectably stale (returns an older `as_of`/version), and the read-your-writes path waits for checkpoint ≥ that position.

Done = replay is deterministic (1), concurrent appends conflict-detect with gap-free sequences (2), every projection rebuilds from zero idempotently (3,4), publishing is at-least-once with idempotent consumers (5), old event versions upcast cleanly (6), and projection drift is both detectable and auto-repairable (7) — all under parallel load, with eventual consistency made explicit to readers (8).

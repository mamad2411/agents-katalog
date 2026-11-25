---
name: build-cdc-streaming-pipeline
description: Designs change-data-capture and streaming pipelines — log-based CDC off a DB transaction log (Debezium/WAL/binlog), topic-per-table fan-out onto Kafka/Kinesis, consumer-group/offset/rebalance correctness, windowed/stateful stream processing with watermarks, exactly-once vs at-least-once-plus-idempotent delivery, and Avro/Protobuf schema-registry evolution.
when_to_use: When row changes (incl. deletes) must propagate continuously and low-latency rather than on a schedule — capturing off a transaction log, fanning onto a partitioned stream bus, consuming with correct offset/rebalance/ordering, windowed joins/aggregations, and sinking to a search index/warehouse/cache kept in sync. Distinct from build-etl-pipeline (scheduled batch/incremental loads) and message-queue-jobs (durable server-to-server task queues, not a replayable change log).
---

## When to Use

Reach for this skill when data must **flow as a continuous change stream**, not land in scheduled batches:

- "Stream every row change out of Postgres/MySQL into Kafka and keep Elasticsearch in sync"
- "Mirror a table into the warehouse in near-real-time, including deletes"
- "My consumer is reprocessing / skipping events after a deploy or rebalance"
- "Consumer-group lag is climbing; ordering is wrong; one partition is hot"
- "Join an orders stream against an enrichment stream with a 5-minute window"
- "Late/out-of-order events are dropped or double-counted"
- "Producer schema changed and consumers broke" / "map Debezium op codes to upserts and deletes"

NOT this skill:
- Scheduled/incremental batch loads to a warehouse (Airflow/dbt, nightly, `updated_at` cursor) → build-etl-pipeline
- Durable server-to-server work/task queue (enqueue a job, one worker runs it once) → message-queue-jobs
- Client-facing live push over WebSocket/SSE (chat, dashboards) → build-realtime-channel
- Offline client store + delta pull + conflict resolution → build-offline-first-sync
- The replication slot / logical-decoding DDL impact on the **source** DB itself → db-migration-safety
- Embedding/indexing documents for retrieval as the sink semantics → rag-pipeline

## Steps

1. **Confirm it's actually streaming, then capture log-based — not query polling.** If freshness tolerance is minutes/hours and deletes don't need to propagate, stop and use build-etl-pipeline. If changes (incl. deletes) must land in seconds, do CDC. Pick the capture method:

   | Method | Captures deletes | Source load | Ordering | Use when |
   |---|---|---|---|---|
   | Query polling (`WHERE updated_at > :cursor`) | ❌ no (row is gone) | full table scan / index pressure | by `updated_at` only | no log access; deletes don't matter; small tables |
   | **Log-based CDC (Debezium on WAL/binlog/redo)** | ✅ yes | low — reads the log the DB already writes | exact commit order per table | **default** — full fidelity, deletes, low impact |
   | Trigger-based | ✅ yes | write amplification on every DML | by trigger | log unavailable but deletes needed |

   Default: **Debezium connectors** — Postgres (`pgoutput` logical decoding + replication slot), MySQL (`binlog`, `binlog_format=ROW`, `binlog_row_image=FULL`), Mongo (change streams). Set Postgres `wal_level=logical`, `REPLICA IDENTITY FULL` on tables whose before-image (for deletes/diffs) you need.

2. **Get the snapshot→stream handoff right, or you lose or double rows at startup.** A new connector must read existing rows (snapshot) then switch to live log without a gap. Use `snapshot.mode=initial` (snapshot once, then stream) — the connector records the log position at snapshot start and streams from there. For huge tables use **incremental snapshot** (`signal`-driven, chunked) so streaming isn't blocked and the connector is resumable. **Never** drop the replication slot while paused — Postgres then discards WAL the connector hasn't read and you get a permanent gap (full re-snapshot required). Monitor `pg_replication_slots.confirmed_flush_lsn`; an abandoned slot also pins WAL and fills the disk.

3. **Shape the bus: topic-per-table, partition key = entity id, choose retention vs compaction.** One topic per source table/aggregate (`server.table` → `dbserver1.public.orders`). Partition **by primary key** so all events for one entity land on one partition → per-entity ordering is preserved; Kafka guarantees order **only within a partition**, never across. Do not key by a low-cardinality column (creates hot partitions) or leave keys null (round-robin → ordering lost).

   | Topic config | Use for | Effect |
   |---|---|---|
   | `cleanup.policy=delete` + `retention.ms` | event/audit streams, replay window | drops old segments by time/size |
   | `cleanup.policy=compact` | **CDC table mirrors** (latest state per key) | keeps newest value per key forever; tombstone (`value=null`) deletes the key |
   | `compact,delete` | mirror + bounded history | compacted, plus old tombstones expire after `delete.retention.ms` |

   Default for a table mirror: **log compaction**, keyed by PK. Kinesis equivalent: shard by partition key = PK; remember Kinesis ordering is per-shard and resharding rehashes keys.

4. **Map CDC op codes to sink operations explicitly.** Debezium envelope `op`: `c`(create)/`r`(read/snapshot)/`u`(update) → **upsert** by PK; `d`(delete) → emit a **tombstone** (`key=PK, value=null`) so compaction and downstream deletes work. Configure `ExtractNewRecordState` SMT to unwrap the envelope and `delete.handling.mode=rewrite` (or `drop`) per sink needs. A sink that treats `d` as an upsert of nulls instead of a delete silently resurrects deleted rows.

5. **Consume correctly — offset-commit timing is the core bug.** The consumer group assigns partitions to members; each commits the offset of records it has processed. **Commit after the side effect is durable, never before.**

   - **Enable-auto-commit is at-least-once at best and silently lossy at worst:** it commits on a timer (`auto.commit.interval.ms`) regardless of whether your handler finished. A crash after commit-but-before-processing → message lost. **Set `enable.auto.commit=false`** and commit manually after the sink write succeeds.

   ```java
   // at-least-once done right: process → flush sink → THEN commit
   props.put("enable.auto.commit", "false");
   props.put("isolation.level", "read_committed"); // skip aborted txn records
   props.put("max.poll.records", "500");
   while (running) {
     var records = consumer.poll(Duration.ofMillis(500));
     for (var r : records) sink.upsert(key(r), value(r));  // idempotent
     sink.flush();                                          // durable side effect first
     consumer.commitSync();                                 // commit only after flush
   }
   ```
   Order is load-bearing: process → flush → commit. Commit-before-process loses on crash; commit-per-record kills throughput.

   - **Cooperative rebalance, not eager (stop-the-world):** set `partition.assignment.strategy=CooperativeStickyAssignor` so a join/leave revokes only the moved partitions instead of pausing the whole group. Commit in the `onPartitionsRevoked` callback so the new owner resumes from the right place.
   - **Avoid spurious rebalances:** if processing a poll batch can exceed `max.poll.interval.ms` (default 5 min), the broker evicts the member and rebalances mid-work. Either lower `max.poll.records` or raise the interval. Keep `session.timeout.ms`/`heartbeat.interval.ms` at ~3:1.
   - **Lag, not just throughput:** alert on consumer-group lag (`kafka-consumer-groups --describe`, or Burrow/CMAK). Scale by adding consumers **up to the partition count** — extra consumers past `#partitions` sit idle. More throughput needs more partitions (and partition count can only go *up*; increasing it rehashes keys and breaks ordering for in-flight keys).
   - **Poison record → DLQ, don't block the partition.** A record that always fails (bad schema, sink rejects) will halt the partition forever if you retry in place. After N attempts, route it to a dead-letter topic with headers (original topic/partition/offset/exception), commit past it, continue.

6. **Process: stateless map vs windowed/stateful — pick the window and a watermark.** Stateless filter/transform/route → a plain consumer or single-operator stream. Joins/aggregations need **state + a window + a watermark** (event-time progress marker that says "no events older than T will arrive"):

   | Window | Use for | Note |
   |---|---|---|
   | Tumbling (fixed, non-overlapping) | per-minute counts, billing buckets | each event in exactly one window |
   | Hopping/sliding (overlapping) | moving averages, "last 5 min every 1 min" | event in multiple windows |
   | Session (gap-based) | user sessions, bursts | window closes after inactivity gap |

   Use **event time** (the row's commit/`ts_ms`), never processing time, or replay and out-of-order delivery corrupt results. Set `allowed_lateness`/grace so late events update an already-emitted window instead of being dropped; send events past the grace period to a side-output, don't silently discard. Keep operator state in a durable, checkpointed store (Kafka Streams `RocksDB` + changelog topic, or Flink checkpoints) so a restart restores aggregates instead of recomputing from zero.

7. **Choose delivery semantics deliberately — exactly-once is opt-in and not free.** Default and simplest: **at-least-once + idempotent sink.** Make the sink absorb duplicates (upsert by PK, `INSERT ... ON CONFLICT DO UPDATE`, dedup table on event id) so reprocessing after a rebalance/replay is harmless. Reach for true **exactly-once** only when the sink can't be made idempotent (e.g. incrementing counters, append-only ledgers):
   - Kafka→Kafka: enable EOS — `processing.guarantee=exactly_once_v2` (Kafka Streams) or transactional producer (`enable.idempotence=true`, `transactional.id`) + consumer `isolation.level=read_committed`. This is a transactional read-process-write **within Kafka only**; it does not extend to an external DB.
   - Kafka→external store: use **idempotent upserts**, or a two-phase/transactional sink connector that stores the consumed offset in the *same* transaction as the data.
   - **Replay** is a first-class operation: reset the group to an offset/timestamp (`kafka-consumer-groups --reset-offsets --to-datetime`) and reprocess. This only produces correct results **because** the sink is idempotent or transactional — design for replay from day one.

8. **Schema registry + compatibility, or producers will break consumers.** Serialize with **Avro or Protobuf via a schema registry** (not raw JSON) so every record carries a schema id and the registry enforces compatibility on register. Default compatibility: **BACKWARD** (new schema can read old data) — consumers upgrade first. Rules that keep it safe: add fields **with defaults**, never rename/retype a field in place (add new + dual-write + retire), never remove a required field. Pin Debezium key/value converters to the registry. For Kafka Connect sinks, the registry + compatibility check is what stops a bad producer from poisoning every downstream consumer at 3am.

## Common Errors

- **`enable.auto.commit=true` treated as exactly-once.** It's a timer that commits independent of your handler — a crash loses or reprocesses. Set it `false` and commit after the sink flush.
- **Committing the offset before the side effect is durable.** Crash in the gap = silent data loss. Strict order: process → flush sink → commit.
- **Dropping/recreating the Postgres replication slot to "reset".** WAL the connector hasn't consumed is discarded → permanent gap, forces a full re-snapshot. Pause the connector, keep the slot; never delete a slot with unconsumed WAL.
- **Abandoned/lagging slot fills the source disk.** A stopped consumer pins WAL forever. Alert on `confirmed_flush_lsn` lag and slot age; clean up dead connectors.
- **Null or low-cardinality partition key.** Null key → round-robin → cross-partition reordering of one entity's events. Low-cardinality key → hot partition. Key by primary key.
- **Increasing partition count on a live keyed topic.** Rehashes keys → an entity's new events go to a different partition than its in-flight ones → ordering broken. Plan partition count up front; treat increases as a migration.
- **Treating a Debezium `d` (delete) as an upsert.** Resurrects deleted rows in the sink. Emit a tombstone (`value=null`) and let the sink delete; use the `ExtractNewRecordState` SMT.
- **Reading uncommitted transactional records.** Without `isolation.level=read_committed`, consumers see aborted-transaction records and double-count. Set it whenever producers use transactions.
- **Poison record retried in place.** One un-processable record halts its partition forever and lag explodes. Bounded retries → DLQ topic → commit past it.
- **Processing on the poll thread longer than `max.poll.interval.ms`.** Broker thinks the consumer died, rebalances mid-batch, you reprocess. Shrink `max.poll.records` or raise the interval; offload slow work.
- **Eager (stop-the-world) rebalance assignor by default.** Every scale event pauses the whole group. Use `CooperativeStickyAssignor`.
- **Windowing on processing time.** Replay and out-of-order delivery silently corrupt aggregates. Window on event time with a watermark; route past-grace events to a side-output.
- **Raw JSON with no registry.** A producer field rename breaks every consumer with no guardrail. Use Avro/Protobuf + registry with BACKWARD compatibility.
- **Scaling consumers past partition count.** Extra members sit idle. Add partitions (carefully — see above) or split the workload differently.

## Verify

1. **Capture fidelity incl. deletes:** `INSERT`, `UPDATE`, then `DELETE` a row on the source → consumer observes a create, an update (with correct before/after), and a tombstone, in commit order. A delete that produces no tombstone is a fail.
2. **Snapshot→stream no-gap:** seed N rows, start the connector, then write M more **during** the snapshot → exactly N+M distinct rows arrive downstream, none missing, none duplicated past idempotency.
3. **Per-entity ordering:** rapidly emit 3 updates to one PK → consumer receives them in source order on a single partition (events for that key never interleave out of order).
4. **Offset correctness across restart:** kill the consumer mid-batch, restart → no committed-but-unprocessed record is lost and no already-sunk record corrupts the sink (idempotency holds). Lag returns to ~0.
5. **Rebalance correctness:** add then remove a consumer under load with `CooperativeStickyAssignor` → no record is processed by two members and none is skipped; only moved partitions are revoked (check logs).
6. **Replay = same result:** `--reset-offsets --to-earliest` and reprocess → final sink state is byte-identical to before the replay (proves the sink is idempotent/transactional).
7. **Poison handling:** inject a record the sink rejects → it lands in the DLQ with origin headers, the partition keeps flowing, lag does not climb.
8. **Late event:** emit an event with an event-time inside a closed-but-within-grace window → the window result updates; past grace → it appears in the side-output, not silently dropped.
9. **Schema evolution:** register a new schema adding a field with a default under BACKWARD compatibility → old consumers keep running; attempt an incompatible change → registry rejects the register (does not reach consumers).
10. **Lag SLO:** under sustained source write load, consumer-group lag stays bounded (returns toward 0), not monotonically rising.

Done = deletes propagate as tombstones, snapshot→stream is gap-free, per-entity ordering holds on one partition, a kill-restart and a full replay both leave the sink state correct (idempotent or transactional), poison records go to a DLQ without blocking the partition, late events hit grace/side-output (never silently dropped), and an incompatible schema is rejected at the registry before it reaches any consumer.

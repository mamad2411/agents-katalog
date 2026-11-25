---
name: kafka-in-action
description: "Knowledge base from \"Apache Kafka in Action\" by Anatoly Zelenin & Alexander Kropp (Manning, 2025). Use when applying the authors' frameworks for Kafka topics/partitions/keys, reliability (acks, min.insync.replicas, idempotence, transactions), producer/consumer internals and rebalancing, retention/compaction, KRaft cluster management, performance tuning, Kafka Connect/Debezium CDC, Kafka Streams, schemas/security/quotas, monitoring, disaster recovery, and Kafka's place in enterprise architecture — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Apache Kafka in Action
**Authors**: Anatoly Zelenin & Alexander Kropp | **Pages**: ~370 | **Chapters**: 18 + 2 appendices | **Kafka**: 3.9 / KRaft | **Generated**: 2026-10-12

## How to Use This Skill

- **Without arguments** — load the core frameworks below
- **With a topic** — ask about `min.insync.replicas`, `rebalance`, `compaction`, `Debezium`, `MirrorMaker`; I find and read the relevant chapter
- **With chapter** — ask for `ch05`; I load that chapter file
- **Browse** — ask "what chapters do you have?" for the full index
- **Decide fast** — [cheatsheet.md](cheatsheet.md) holds the authors' thresholds and decision rules

When you ask about a topic not covered in Core Frameworks below, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

### 1. Kafka is a distributed, replicated log — not a queue, not a database
- An append-only log addressed **only by offset**; reading is non-destructive, so any number of consumer groups read and replay independently (retention default 7 days).
- **Partition** = unit of parallelism, ordering, and replication. Order holds **only within a partition** → use **keys** (`hash(key) % N`) to keep an entity's events together.
- Partition count can **never decrease**, and increasing it remaps keys and breaks per-key order → size up front (default **12**, double as needed).
- Mixed Java + librdkafka producers on one topic: set `partitioner=murmur2_random` or the same key lands in different partitions.
- Use Kafka as the **data hub between systems**; query state from a fit-for-purpose store (DB, OpenSearch, Redis) built as a local materialized view — never from Kafka.

### 2. Reliability = producer `acks` × topic `min.insync.replicas` × RF
- `acks=0` at-most-once; `acks=1` leader only; `acks=all` waits for every ISR (default since 3.0).
- **Baseline for real data**: `acks=all` + `enable.idempotence=true` + RF 3 + `min.insync.replicas=2` → survives one broker loss with no client impact. A second loss blocks producers (`NotEnoughReplicasException`).
- Trap: `acks=all` with min ISR 1 degrades to `acks=1`.
- **Idempotent producer** (producer ID + sequence numbers) → exactly-once, ordered writes per partition; cost negligible, keep it on.
- **Transactions** (2PC variant, `transactional.id`, `send_offsets_to_transaction`, consumers on `isolation.level=read_committed`) extend exactly-once to atomic multi-partition read-process-write. Set `read_committed` everywhere now.
- Leader election is ISR-only; **unclean leader election** trades data for availability — emergencies only, per topic.

### 3. Commit = High Watermark; durability = replication, not fsync
- Brokers ack after writing to the **page cache** without fsync; durability comes from replicas on independent hosts/racks.
- A record is committed when the **HWM** (smallest LEO across ISRs) passes it; consumers read only up to the HWM. A slow follower stalls consumers until dropped after `replica.lag.time.max.ms` (30 s — don't lower it).
- On final producer failure (`delivery.timeout.ms`, 2 min) use a **circuit breaker**, not blind resends.

### 4. Consumers pull; groups split partitions; rebalances stop the world
- Committed positions live in compacted `__consumer_offsets`; **consumer lag** is the health signal; `auto.offset.reset=earliest` for new groups that need history.
- Rebalance Protocol: group coordinator (broker) + group leader (first consumer) computes assignment. Cut its cost with **CooperativeStickyAssignor** and **static membership** (`group.instance.id` + long `session.timeout.ms`).
- Never share a `group.id` across applications — they overwrite each other's offsets and "steal" messages.

### 5. Cleanup is per segment
- `delete`: a segment goes only when its **newest** record exceeds `retention.ms` → legal limits need `segment.ms + retention.ms + check interval ≤ limit`.
- `compact`: latest value per key (keys required), active segment never compacted, tombstones (null value) delete keys after `delete.retention.ms`. Tune with `min.cleanable.dirty.ratio` / `max.compaction.lag.ms`.

### 6. Operate with KRaft, sized RAM-first
- Odd controller quorum: 3 (tolerates 1) or 5 (tolerates 2); 4 adds nothing. Production: dedicated controllers + ≥3 brokers. Migrate ZooKeeper → KRaft now (removed in 4.0); the final controller step is irreversible — soak 1–2 weeks first.
- Small heap (1–6 GB), **page cache = ingest/broker/hour × tolerated lag hours**, 32–64 GB per broker then scale out; several SSDs, no RAID 5/6; inter-broker latency < 30 ms.
- Performance lives in clients: `batch.size` up to 1 MB, `linger.ms≈10`, `zstd/lz4`, never `fetch.min.bytes`/`fetch.max.wait.ms`=0. Method: understand → measure (perf-test tools) → optimize.

### 7. The ecosystem: Connect, Streams, schemas
- **Kafka Connect** (Distributed Mode, RF-3 internal topics, REST API driven by CI/CD) replaces hand-written integration code. Configure errors deliberately (retry → tolerance+logging → DLQ for sinks). Use **Debezium CDC**, not JDBC polling, when updates/deletes matter.
- **Stream–table duality**: events as KStreams, master data as KTables (RocksDB + compacted changelog). Joins need **co-partitioning**; key changes cost a `-repartition` topic (prefer `mapValues`). Parallelism = input partitions.
- **Schema = contract**. Choose compatibility from the consumer's view (backward: update consumers first; forward: producers first; full: both), enforce via a registry fed from CI/CD — Kafka validates nothing. Only optional-field additions are safe everywhere.

### 8. Govern, watch, and plan for failure
- Mandatory TLS + authentication + least-privilege ACLs (super-user → Deny → Allow). Revoke ACLs on compromise — auth is checked only at connection setup. Quotas are per broker; add them only with throttle-time monitoring.
- Monitor in layers (infra → broker → client → environment). Alert on few signals: under-replicated / under-min-ISR partitions > 0, network idle < 0.3, > 60% disk/network, lag rising with lead falling, failed tasks/threads. Attach a playbook to every alert.
- Resilience ladder: replication (broker loss) → stretched cluster over **≥3** DCs ≤30 ms (DC loss) → **MirrorMaker 2**, preferably active-active (distant sites). Back up only if Kafka is the source of truth.

### 9. Architecture judgment
- Helland's **data on the inside** (DB, "What is?") vs **data on the outside** (immutable Kafka history, "What was?"); Kleppmann's "turning the database inside out".
- Kafka = **dumb pipe, smart endpoints**, the core of a streaming platform (Connect + processing + GitOps governance) and the exchange layer of a **data mesh**.
- Kafka is not: a relational DB, a synchronous request/response channel, a file transport, worth it below ~1,000 msg/h for one team, or a substitute for good architecture. Liberate core systems via CDC → secondary DB → denormalized **outbox** → Kafka.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-introduction.md) | Introduction to Apache Kafka | Central nervous system for data, producer→leader→followers→consumer group, KRaft |
| [ch02](chapters/ch02-first-steps.md) | First steps with Kafka | CLI create/produce/consume loop, `--from-beginning`, GUI read-only rule |
| [ch03](chapters/ch03-topics-messages.md) | Exploring Kafka topics and messages | `kafka-topics.sh` lifecycle, state/delta/event/command, keys for ordering, one data format |
| [ch04](chapters/ch04-distributed-log.md) | Kafka as a distributed log | Log + offset, key partitioning, consumer groups, leader/follower, coordination cluster |
| [ch05](chapters/ch05-reliability.md) | Reliability | acks × min.insync.replicas, delivery guarantees, idempotence, transactions, leader election |
| [ch06](chapters/ch06-performance.md) | Performance | Partition sizing (12), batching + linger, compression, fetch tuning, broker sizing |
| [ch07](chapters/ch07-cluster-management.md) | Cluster management | KRaft quorum & roles, ZooKeeper→KRaft migration, bootstrap/metadata request |
| [ch08](chapters/ch08-producing-persisting.md) | Producing and persisting messages | Producer pipeline, broker produce path, segments & indexes, LEO/HWM/ISR, leader epoch |
| [ch09](chapters/ch09-consuming.md) | Consuming messages | Fetch requests, offsets & lag, Rebalance Protocol, assignors, static membership |
| [ch10](chapters/ch10-cleanup-retention-compaction.md) | Cleaning up messages | Retention timing, compaction eligibility, log cleaner, tombstones |
| [ch11](chapters/ch11-kafka-connect.md) | Integrating external systems with Kafka Connect | Distributed Mode, REST API, error ladder + DLQ, SMTs, JDBC vs Debezium CDC |
| [ch12](chapters/ch12-stream-processing.md) | Stream processing | Stream–table duality, aggregations, join types, windows & time, Streams scaling |
| [ch13](chapters/ch13-governance.md) | Governance | Schema compatibility, registry + Avro, TLS/SASL/ACLs, encryption, quotas |
| [ch14](chapters/ch14-reference-architecture.md) | Kafka reference architecture | Components & tooling, GitOps, Cruise Control, deployment models, RAM-first sizing |
| [ch15](chapters/ch15-monitoring-alerting.md) | Kafka monitoring and alerting | Layered metrics, 60% headroom, lag + lead, metrics→alerts, playbooks |
| [ch16](chapters/ch16-disaster-management.md) | Disaster management | Failure taxonomy, broker-loss tolerance, stretched cluster, MirrorMaker 2 topologies, backups |
| [ch17](chapters/ch17-comparison.md) | Comparison with other technologies | Data inside vs outside, dumb pipe vs ESB, REST vs Kafka, DB inside out |
| [ch18](chapters/ch18-enterprise-architectures.md) | Kafka's role in modern enterprise architectures | Data mesh, core-system liberation (CDC + outbox), IIoT, what Kafka is not |
| [ch19](chapters/ch19-appendix-a-test-environment.md) | Appendix A — Setting up a Kafka test environment | 3-broker dual-mode KRaft cluster, storage format, failure injection |
| [ch20](chapters/ch20-appendix-b-monitoring-setup.md) | Appendix B — Monitoring setup | Prometheus + JMX Exporter, Alertmanager, Blackbox/Node Exporter, Grafana |

## Topic Index

- **acks** → ch05, ch08
- **Alertmanager / Prometheus / Grafana** → ch20, ch15
- **Assignors (Range, Round Robin, Sticky, Cooperative Sticky)** → ch09, ch15
- **Backup** → ch16
- **batch.size / linger.ms** → ch06, ch08
- **Bootstrap servers / metadata request** → ch07
- **broker.rack / client.rack (KIP-392)** → ch09, ch16
- **Broker sizing (RAM, disk, network)** → ch06, ch14
- **CDC / Debezium** → ch11, ch18
- **Compression** → ch06
- **Consumer group** → ch04, ch09
- **Consumer lag / records-lead** → ch09, ch15
- **`__consumer_offsets`** → ch03, ch04, ch09
- **Controller quorum / KRaft** → ch04, ch07, ch19
- **Cruise Control** → ch14, ch16
- **Data mesh** → ch18
- **Data on the inside / outside** → ch17
- **Dead-letter queue** → ch11
- **Delivery guarantees (at-most/at-least/exactly-once)** → ch05
- **Encryption (TLS, at rest, end-to-end)** → ch13
- **fetch.min.bytes / fetch.max.wait.ms** → ch06, ch09
- **GitOps / kcctl** → ch14, ch17
- **High Watermark / LEO** → ch08
- **Idempotent producer** → ch05, ch08
- **ISR / ELR** → ch03, ch05, ch08
- **Joins (stream–table, table–table, windowed)** → ch12
- **Kafka Connect** → ch11
- **Kafka Streams / Flink** → ch12
- **Keys & partitioning / murmur2_random** → ch03, ch04, ch08
- **Leader election (preferred, unclean)** → ch05
- **Log compaction / tombstones** → ch10
- **Log retention** → ch02, ch10
- **Log segments / indexes** → ch08, ch10
- **Message types (state, delta, event, command)** → ch03
- **min.insync.replicas** → ch05, ch08, ch16
- **MirrorMaker 2** → ch14, ch16
- **Monitoring metrics** → ch15, ch20
- **Outbox pattern** → ch18
- **Page cache / zero-copy** → ch06, ch08, ch14
- **Partition count** → ch03, ch06
- **Quotas** → ch13
- **Rebalance Protocol** → ch09
- **REST vs Kafka / ESB / databases** → ch17
- **Schema registry / compatibility / Avro** → ch13
- **Security (SASL, mTLS, ACLs)** → ch13
- **Share groups** → ch06
- **SMTs** → ch11
- **State stores / changelog / repartition topics** → ch12
- **Static membership** → ch09
- **Stretched cluster** → ch16
- **Strimzi / Kubernetes** → ch14, ch15
- **Test environment (local KRaft)** → ch19
- **Tiered storage** → ch14, ch18
- **Transactions / read_committed** → ch05, ch09
- **Windows (tumbling, hopping, sliding, session)** → ch12
- **ZooKeeper → KRaft migration** → ch07

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — techniques and design patterns with trade-offs
- [cheatsheet.md](cheatsheet.md) — thresholds, defaults, decision tables

---

## Scope & Limits

This skill covers the book's content (Kafka 3.9, KRaft era). Version notes flagged inside chapters: `AclAuthorizer` is ZooKeeper-era (KRaft uses `StandardAuthorizer`); the book's `num.threads` is `num.stream.threads` in Kafka Streams; the book's schema-compatibility table 13.1 has a misprinted row, corrected in ch13. For Kafka 4.x changes (KIP-848 rebalance protocol, share groups GA), verify against current Apache Kafka docs. Combine with project-specific tools for hands-on implementation.

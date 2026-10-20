---
name: apache-kafka-docs
description: "Knowledge base from the official \"Apache Kafka 4.3 Documentation\" (Apache Software Foundation, AK 4.3.x). Use when you need the docs' exact configs, defaults, CLI commands and mechanisms for Kafka design (replication/ISR, delivery semantics, transactions, log compaction, quotas), KRaft, operations (reassignment, monitoring, tiered storage, geo-replication/MirrorMaker 2), new protocols (KIP-848 consumer groups, share groups, KIP-890, ELR), security (listeners, SSL, SASL, ACLs), Kafka Connect, Kafka Streams (DSL, Processor API, state, interactive queries), and 4.x upgrades — or when studying or referencing the docs."
---

<!-- argument-hint: [topic, config name, KIP, or chapter number] -->

# Apache Kafka 4.3 Documentation
**Author**: Apache Software Foundation (AK 4.3.x docs) | **Source**: ~65 pages, ~173k words | **Chapters**: 30 | **Generated**: 2026-10-12

## How to Use This Skill

- **No arguments**: load the core rules below.
- **Topic, config or KIP** (`min.insync.replicas`, `KIP-848`): find the chapter in the Topic Index and read it before answering.
- **Chapter** (`ch15`): load that file. **Browse**: "what chapters do you have?"

Chapters have config/default tables, code/CLI and a worked example. For an exact default, flag or command, read the chapter instead of answering from memory; ch30 tracks defaults that changed in 4.x. For a book-style, architecture-oriented view (Kafka 3.9), see `kafka-in-action`.

---

## Core Frameworks & Mental Models

### 1. The log is the product (ch01, ch05, ch09)
- A topic is a **partitioned, replicated, append-only log**: reading never deletes, retention is per topic (time/size), and cost is ~O(1) in data size.
- **Order exists only within a partition.** Key by the entity whose order matters (`hash(key) % N`). Adding partitions remaps keys, and partitions can never be reduced (ch10).
- Speed comes from mechanics: the **OS pagecache** instead of the heap, sequential I/O, **`sendfile` zero-copy** (lost under TLS) and batch compression. In 4.x, `linger.ms`=5 and `batch.size`=16384; raise both for throughput.
- Consumers **pull** with long polling. Position is one offset per partition, so you can rewind to reprocess within retention. `group.instance.id` (static membership) avoids rebalances on restart.

### 2. Durability is a three-knob contract (ch07, ch06)
- A write is *committed* when every **ISR** replica has it. A replica leaves the ISR after `replica.lag.time.max.ms` (30 s).
- **To survive f failures without losing acked data, use RF ≥ f+1, `acks=all` and `min.insync.replicas ≥ 2`.** `acks=all` alone waits only for the current ISR, which can shrink to the leader. Baseline: RF=3, minISR=2.
- `unclean.leader.election.enable=false` (the default) chooses consistency. ELR (KIP-966, ch17) makes elections safer without changing that.
- ISR needs f+1 replicas to tolerate f failures, a majority quorum needs 2f+1. KRaft controllers are a quorum, hence **2N+1** (ch15).

### 3. Delivery semantics = order of commit vs processing (ch06)
- Commit before processing gives at-most-once. Commit after processing gives at-least-once (the default), which is enough when writes are idempotent by primary key.
- The **idempotent producer** (PID + sequence number) removes retry duplicates.
- **Exactly-once Kafka→Kafka** needs a transactional producer (`transactional.id`), `sendOffsetsToTransaction`, and consumers on `isolation.level=read_committed` (the default `read_uncommitted` also returns aborted records). Prefer Streams `exactly_once_v2`; otherwise use one transactional producer per consumer.
- **Share groups** (KafkaShareConsumer) work as queues: more consumers than partitions, per-record acquisition locks (`share.record.lock.duration.ms` 30 s), accept/release/reject, and delivery counts. Use them for parallelism without ordering (ch03).

### 4. Choose the group protocol deliberately (ch17, ch29)
- **KIP-848 (`group.protocol=consumer`)**: incremental, broker-driven rebalances with no global barrier; assignors `uniform` and `range`. The client default stays `classic` until 5.0. Groups whose assignor uses custom metadata must migrate offline.
- **KIP-1071 (`group.protocol=streams`)**: the same model for Streams, on ≥ 4.2 (migrate on 4.2.1+). Standbys and timeouts become broker-side group configs, and client-side values are ignored.
- **KIP-890 (`transaction.version=2`)** bumps the epoch on every transaction. Produce latency looks higher because the time moved out of client backoff.

### 5. KRaft is the only mode (ch15, ch02, ch30)
- ZooKeeper was removed in 4.0. In production, set `process.roles` to `broker` or `controller`, never both; 3 controllers tolerate 1 failure, 5 tolerate 2.
- **Formatting is explicit**: `kafka-storage.sh random-uuid`, then `format` with `--standalone`, `--initial-controllers` or `--no-initial-controllers`. Leaving `controller.quorum.voters` unset gives a dynamic quorum (KIP-853, `add-`/`remove-controller`, needs `kraft.version` 1). A static quorum never becomes dynamic.
- **Upgrade**: roll binaries, soak, then `kafka-features.sh upgrade --release-version`. 4.x metadata versions cannot be downgraded. From ZooKeeper or KRaft < 3.3, go via 3.9.x. Clients/brokers < 2.1 must be upgraded before 4.0 (KIP-896).

### 6. Operate with throttles and invariants (ch10, ch14, ch13, ch16)
- **Reassignment**: generate → execute `--throttle` → `--verify` (which also removes the throttle). Keep the throttle above `max(BytesInPerSec)`. Decommission a broker by cordon → drain → remove.
- **Must be 0**: `UnderReplicatedPartitions`, `UnderMinIsrPartitionCount`, `AtMinIsrPartitionCount`, `OfflinePartitionsCount`, `UncleanLeaderElectionsPerSec`. `ActiveControllerCount` sums to 1. Idle percent < ~0.3 means thread-saturated.
- Durability comes from replication, not fsync, so leave flush settings off. Prefer JBOD `log.dirs` over RAID, raise `vm.max_map_count` and file descriptors (≥ 100k), and use XFS with `noatime`.
- **Tiered storage**: `local.retention.ms` sets the hot tier, `retention.ms` the total. Compacted topics are not supported, and tiered topics must be deleted before tiering is disabled.

### 7. Security: listeners → authentication → authorization (ch18–20)
- `listener.security.protocol.map` names each listener's protocol. In KRaft, `controller.listener.names` must differ from the inter-broker listener. `security.inter.broker.protocol` defaults to PLAINTEXT, so switch it in its own rolling bounce.
- mTLS needs `ssl.client.auth=required`, since `requested` admits clients without certs. Hostnames are checked against the cert **SAN**.
- **SASL**: use GSSAPI where Kerberos/AD exists, SCRAM for Kafka-managed users (stored in the metadata log), OAUTHBEARER with a real validator + JWKS for an IdP. Run PLAIN, SCRAM and OAUTHBEARER only over **SASL_SSL**. Use per-client `sasl.jaas.config` when one JVM needs several identities.
- **Authorization is deny by default**: set `authorizer.class.name` on brokers *and* controllers and define `super.users` first. Use `prefixed` ACLs per tenant or `application.id`. Consumers need Group Read plus Topic Read, idempotent producers Cluster IdempotentWrite, transactional producers Write+Describe on the TransactionalId.

### 8. Kafka Connect: configuration, not code (ch21, ch22)
- Try an existing connector first. In distributed mode, pre-create the config (1 partition), offset and status topics, compacted and replicated.
- `errors.tolerance` defaults to `none` (fail fast); for pipelines use `all` + logging + DLQ. FAILED tasks do not restart on their own.
- In a connector, the Connector only splits the work and the **Tasks** move data: source `poll()`, sink `put()` then `flush()`. Make source offsets seekable. Exactly-once source takes two rolls: `preparing`, then `enabled`.

### 9. Kafka Streams: tables are streams with memory (ch23–29)
- **Stream–table duality**: a KStream is a sequence of inserts, a KTable a sequence of upserts (null = tombstone), and every aggregation yields a KTable. A **GlobalKTable** is fully replicated, so its joins need no co-partitioning.
- **Parallelism** is bounded by input partitions: one task per partition, and extra instances sit idle. State lives in RocksDB stores backed by compacted **changelogs**. Use `num.standby.replicas ≥ 1`, persistent `state.dir`, and RF=3/minISR=2 for internal topics.
- `map`, `flatMap`, `selectKey` and `groupBy` force a repartition; prefer `mapValues`/`groupByKey`. Joins need **co-partitioned** inputs, and KStream–KStream joins are always windowed.
- Windows close on **stream time** + grace. Use `suppress(untilWindowCloses)` for final results and versioned stores for out-of-order table updates.
- The record cache (`statestore.cache.max.bytes` 10 MB, flushed every `commit.interval.ms`: 30 s, or 100 ms under EOS) compacts KTable updates. `topology.optimization` applies only when the props are passed to `build(props)`. Interactive Queries need `application.server` and route with `metadataForKey`. Test with `TopologyTestDriver`.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-introduction.md) | Introduction and Use Cases | Partitioned replicated topics; core APIs |
| [ch02](chapters/ch02-quickstart-docker-compatibility.md) | Quickstart, Docker, Compatibility | KRaft bootstrap; JDK/client matrix |
| [ch03](chapters/ch03-client-apis.md) | Client APIs | Six-API map; artifacts |
| [ch04](chapters/ch04-configuration.md) | Configuration | Dynamic config precedence; ConfigProviders |
| [ch05](chapters/ch05-design-persistence-producer-consumer.md) | Design: Persistence, Producer, Consumer | Pagecache + zero-copy; batching; pull |
| [ch06](chapters/ch06-design-delivery-semantics-transactions.md) | Design: Delivery Semantics, Transactions | EOS transactions; share groups |
| [ch07](chapters/ch07-design-replication-compaction-quotas.md) | Design: Replication, Compaction, Quotas | ISR commit rule; compaction; quotas |
| [ch08](chapters/ch08-protocol.md) | Wire Protocol | ApiVersions; SASL handshake |
| [ch09](chapters/ch09-implementation.md) | Implementation | Record Batch v2; log segments; offsets |
| [ch10](chapters/ch10-basic-operations.md) | Basic Operations | Throttled reassignment; decommission |
| [ch11](chapters/ch11-geo-replication.md) | Geo-Replication | MirrorMaker 2 flows |
| [ch12](chapters/ch12-multi-tenancy.md) | Multi-Tenancy | Prefixed ACLs; policies; quotas |
| [ch13](chapters/ch13-hardware-os-java.md) | Hardware, OS, Java | Pagecache sizing; OS limits |
| [ch14](chapters/ch14-monitoring.md) | Monitoring | Zero-invariant alerts; latency breakdown |
| [ch15](chapters/ch15-kraft.md) | KRaft | 2N+1 quorum; dynamic quorum; formatting |
| [ch16](chapters/ch16-tiered-storage.md) | Tiered Storage | Local/total retention; RSM + RLMM |
| [ch17](chapters/ch17-rebalance-transaction-protocol-elr.md) | Rebalance/Transaction Protocols, ELR | KIP-848; KIP-890; KIP-966 |
| [ch18](chapters/ch18-security-listeners-ssl.md) | Security: Listeners, SSL | Protocol map; PKI with SAN |
| [ch19](chapters/ch19-security-sasl.md) | Security: SASL | JAAS precedence; OAUTHBEARER |
| [ch20](chapters/ch20-security-authorization-acls.md) | Security: ACLs | Default-deny; protocol→operation map |
| [ch21](chapters/ch21-connect-user-guide.md) | Connect: User Guide | Workers; SMTs; DLQ |
| [ch22](chapters/ch22-connector-development.md) | Connect: Development | Connector/Task split; EOS source |
| [ch23](chapters/ch23-streams-intro-tutorial.md) | Streams: Intro, Tutorial | Topology; stream-table duality |
| [ch24](chapters/ch24-streams-core-concepts.md) | Streams: Core Concepts | Tasks/threads; standbys; EOS v2 |
| [ch25](chapters/ch25-streams-dsl.md) | Streams: DSL | Repartition; joins; windows/suppress |
| [ch26](chapters/ch26-streams-processor-api.md) | Streams: Processor API | Punctuation; StoreBuilder; serdes |
| [ch27](chapters/ch27-streams-config-memory.md) | Streams: Config, Memory | Resiliency baseline; RocksDB + cache |
| [ch28](chapters/ch28-streams-interactive-queries-testing.md) | Streams: IQ, Testing | IQ routing; TopologyTestDriver |
| [ch29](chapters/ch29-streams-ops-tools-rebalance-security.md) | Streams: Ops Tools, Protocol | KIP-1071; reset; naming |
| [ch30](chapters/ch30-upgrade-notes.md) | Upgrade Notes | Rolling upgrade + finalization |

## Topic Index

- **acks, min.insync.replicas, ISR, replication, unclean election** → ch07, ch06
- **ACLs, super.users, authorizer** → ch20, ch12, ch29
- **APIs, client artifacts** → ch03; **wire protocol, ApiVersions** → ch08
- **Compatibility, JDK, KIP-896** → ch02, ch30
- **Compression, batching, linger.ms** → ch05, ch09
- **Configs: dynamic broker, ConfigProviders** → ch04
- **Connect** → ch21; **connector development** → ch22
- **Consumer groups, offsets, reset** → ch10, ch09, ch05
- **Delivery semantics, idempotence, transactions** → ch06, ch17
- **ELR (KIP-966), KIP-848, KIP-890** → ch17; **KIP-1071** → ch29
- **Geo-replication, MirrorMaker 2** → ch11
- **Hardware, JVM, filesystem** → ch13
- **KRaft, kafka-storage.sh, quorum** → ch15, ch02
- **Listeners, SSL/TLS, mTLS** → ch18
- **Log compaction, segments, retention** → ch07, ch09
- **Monitoring, JMX** → ch14
- **Multi-tenancy, quotas, policies** → ch12, ch07, ch10
- **Reassignment, throttle, decommission** → ch10
- **SASL, delegation tokens** → ch19
- **Share groups** → ch06, ch03, ch10
- **Streams: basics** → ch23; **tasks, standbys, EOS v2** → ch24, ch27; **joins, windows, suppress** → ch25; **Processor API, state stores** → ch26; **RocksDB, cache, optimization** → ch27; **IQ, testing** → ch28; **reset tool, groups CLI** → ch29
- **Tiered storage (KIP-405)** → ch16
- **Upgrades, metadata.version, ZooKeeper removal** → ch30, ch15

## Supporting Files

- [glossary.md](glossary.md): terms and definitions · [patterns.md](patterns.md): When / How / Trade-offs recipes · [cheatsheet.md](cheatsheet.md): decision rules, thresholds, warning signs

---

## Scope & Limits

Covers the narrative pages of the Kafka 4.3 docs, not the auto-generated tables (full config lists, metric catalogs, protocol schemas). Chapters keep only the configs practitioners tune; for full listings see kafka.apache.org/documentation. Upgrade notes (ch30) summarize only the most important 4.0–4.3 changes.

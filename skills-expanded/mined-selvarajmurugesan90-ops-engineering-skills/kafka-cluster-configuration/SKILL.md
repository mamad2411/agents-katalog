---
name: kafka-cluster-configuration
description: >
  Designs Apache Kafka broker configuration, topic/partition layout,
  replication factor, and cluster metadata mode (ZooKeeper vs. KRaft). Use
  when the user asks to "size a Kafka cluster," "set replication factor,"
  "design topic partitions," "configure Kafka brokers," "migrate from
  ZooKeeper to KRaft," or "set up a new Kafka cluster" from scratch.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: messaging-and-data-orchestration
  maturity: stable
---

# Kafka Cluster Configuration

## Purpose

Apache Kafka's durability, availability, and throughput are determined
almost entirely at configuration time — by how many partitions a topic
gets, what replication factor and `min.insync.replicas` it's given, and
whether the cluster's metadata is managed by ZooKeeper or Kafka's own
KRaft (Kafka Raft) controller quorum. Getting these choices wrong is
expensive to undo later: repartitioning an existing topic breaks key-based
ordering guarantees, and under-replicated topics silently risk data loss
until a broker actually fails. This skill covers designing that
configuration correctly the first time — validating it before rollout is
covered separately in
[kafka-configuration-validation](../kafka-configuration-validation/SKILL.md).

## When to use

- Standing up a new Kafka cluster and deciding broker count, partition
  counts per topic, and replication factor.
- Designing a new topic's partition count based on expected throughput and
  consumer parallelism.
- Deciding between ZooKeeper-based and KRaft-based metadata management for
  a new or existing cluster.
- Configuring rack/availability-zone awareness so replicas don't all land
  in one failure domain.
- Reviewing an existing cluster's `server.properties` for durability gaps
  (e.g. replication factor of 1, `min.insync.replicas` unset).

## Prerequisites & environment

- Kafka 3.3+ if KRaft mode is being considered for production (KRaft
  reached production-ready status in the 3.3 release line; earlier 3.x
  releases have it as preview/early-access only — check the specific
  distribution's release notes before committing to KRaft on an older
  3.x version).
- For ZooKeeper mode: a separate ZooKeeper ensemble (typically 3 or 5
  nodes) already running and reachable from all brokers.
- For KRaft mode: no external ZooKeeper — controller nodes are Kafka
  processes themselves, configured with `process.roles`.
- At least 3 broker nodes for any cluster expected to tolerate a single
  node failure without data loss (replication factor 3 needs 3 brokers
  minimum, ideally spread across separate racks/AZs).
- Disk sized for `log.retention.hours` (or `.bytes`) × expected topic
  throughput × replication factor — replicated data multiplies raw disk
  need by the replication factor.

## Step-by-step guidance

1. **Decide ZooKeeper vs. KRaft for a new cluster.** For any new Kafka
   deployment, prefer KRaft — it removes the operational burden of running
   and upgrading a separate ZooKeeper ensemble and has a higher practical
   ceiling on partition count per cluster since metadata isn't bottlenecked
   through ZooKeeper's znode model. Only choose ZooKeeper mode if the
   target Kafka distribution/version doesn't yet support KRaft for the
   required feature set, or if migrating an existing large ZooKeeper-mode
   cluster where the KRaft migration path isn't yet validated for that
   version.

2. **Configure a KRaft controller quorum** (3 dedicated controller nodes
   is the common baseline for production; combined broker+controller
   nodes are acceptable for smaller/dev clusters):
   ```properties
   # controller node: controller.properties
   process.roles=controller
   node.id=1
   controller.quorum.voters=1@kraft-ctrl-1:9093,2@kraft-ctrl-2:9093,3@kraft-ctrl-3:9093
   listeners=CONTROLLER://kraft-ctrl-1:9093
   controller.listener.names=CONTROLLER
   ```
   ```properties
   # broker node: server.properties
   process.roles=broker
   node.id=101
   controller.quorum.voters=1@kraft-ctrl-1:9093,2@kraft-ctrl-2:9093,3@kraft-ctrl-3:9093
   listeners=PLAINTEXT://:9092
   advertised.listeners=PLAINTEXT://broker-101.internal:9092
   log.dirs=/var/kafka/data
   ```
   An odd number of controller voters (3 or 5) is required so the Raft
   quorum can form a majority on a network partition.

3. **For ZooKeeper mode**, point brokers at the ensemble and give each a
   stable `broker.id`:
   ```properties
   # server.properties
   broker.id=101
   zookeeper.connect=zk-1:2181,zk-2:2181,zk-3:2181/kafka
   listeners=PLAINTEXT://:9092
   advertised.listeners=PLAINTEXT://broker-101.internal:9092
   log.dirs=/var/kafka/data
   ```
   The `/kafka` chroot path in `zookeeper.connect` keeps this cluster's
   znodes isolated if the ensemble is shared with other systems.

4. **Set cluster-wide durability defaults** so individual topic creators
   don't have to remember to override an unsafe default:
   ```properties
   default.replication.factor=3
   min.insync.replicas=2
   unclean.leader.election.enable=false
   offsets.topic.replication.factor=3
   transaction.state.log.replication.factor=3
   transaction.state.log.min.isr=2
   ```
   `unclean.leader.election.enable=false` is the important one — it
   refuses to elect an out-of-sync replica as leader after the in-sync
   set is empty, which prevents silent data loss at the cost of
   unavailability until an in-sync replica returns.

5. **Size partition count per topic from required consumer parallelism
   and target per-partition throughput**, not a round number picked
   without reasoning:
   ```bash
   kafka-topics.sh --bootstrap-server broker-101.internal:9092 \
     --create --topic order-events \
     --partitions 12 --replication-factor 3 \
     --config min.insync.replicas=2 \
     --config retention.ms=604800000
   ```
   A partition count should be at least the maximum number of consumer
   instances that will ever run in the largest consumer group reading
   that topic (extra consumers beyond the partition count sit idle), and
   high enough that a single partition's throughput stays within one
   broker's practical per-partition write throughput. Over-partitioning
   has a real cost too — see the rebalance and metadata pitfalls in
   [kafka-consumer-lag-and-partition-troubleshooting](../kafka-consumer-lag-and-partition-troubleshooting/SKILL.md).

6. **Enable rack awareness** so Kafka spreads a topic's replicas across
   failure domains instead of colocating them:
   ```properties
   # server.properties, one value per broker matching its physical AZ/rack
   broker.rack=us-east-1a
   ```
   With `broker.rack` set on every broker, Kafka's replica placement
   algorithm guarantees no two replicas of the same partition land in the
   same rack when enough racks exist — a single AZ outage then can't take
   out both the leader and all in-sync replicas of a partition
   simultaneously.

7. **Tune log segment and retention settings deliberately per topic**,
   overriding cluster defaults for topics with different retention needs:
   ```bash
   kafka-configs.sh --bootstrap-server broker-101.internal:9092 \
     --alter --entity-type topics --entity-name order-events \
     --add-config retention.ms=604800000,segment.bytes=1073741824
   ```
   Compacted topics (state/changelog topics) need `cleanup.policy=compact`
   instead of time-based retention — see
   [kafka-configuration-validation](../kafka-configuration-validation/SKILL.md)
   for validating that the right policy is applied before production
   rollout.

## Best practices

- Default to KRaft for new clusters; treat ZooKeeper mode as a legacy
  path only for clusters that can't yet move.
- Never run a production topic at replication factor 1 — it means any
  single broker loss (disk failure, instance termination, AZ event) is
  permanent data loss for that topic, not just a temporary unavailability.
- Pair `min.insync.replicas=2` (with RF=3) with producers using `acks=all`
  — `min.insync.replicas` alone does nothing to protect a producer that
  doesn't wait for acknowledgment from the in-sync set.
- Set `broker.rack` (or the cloud-provider equivalent) on every broker
  from day one — it's far more disruptive to add rack awareness to an
  already-populated cluster (existing partitions don't automatically
  reshuffle) than to configure it before any topics are created.
- Separate controller and broker roles onto dedicated nodes for any
  cluster with meaningful topic/partition counts — combined nodes are
  fine for a handful of topics but controller metadata operations
  (leader election, topic creation) compete with broker I/O on combined
  nodes under load.
- Document the partition-count and replication-factor reasoning per topic
  (expected throughput, consumer parallelism, retention need) alongside
  the topic definition in version control, not just as ad hoc CLI history.

## Common pitfalls

- **Symptom:** A broker goes down and an entire topic becomes
  unavailable for writes, even though other brokers are healthy.
  **Fix:** Check `min.insync.replicas` versus the topic's actual
  replication factor and current in-sync replica count
  (`kafka-topics.sh --describe --topic <topic>`). If RF=3 and
  `min.insync.replicas=2` but a second replica was already lagging before
  this broker failure, the ISR set dropped below the minimum and
  producers with `acks=all` are correctly refused rather than silently
  under-protected — the fix is addressing why replicas were already
  lagging (see under-replicated-partition causes in
  [kafka-consumer-lag-and-partition-troubleshooting](../kafka-consumer-lag-and-partition-troubleshooting/SKILL.md)),
  not lowering `min.insync.replicas`.

- **Symptom:** A topic created early in the cluster's life with 3
  partitions can't keep up, and someone increases it to 50 partitions to
  "fix" throughput.
  **Fix:** Increasing partition count on an existing topic does not
  rebalance existing data and, critically, changes which partition a
  given key hashes to — messages for the same key produced before and
  after the partition increase can land in different partitions,
  breaking per-key ordering guarantees consumers may depend on. Size
  partition count correctly at topic-creation time based on projected
  peak throughput, and if a genuine increase is unavoidable, communicate
  the ordering-guarantee change to every consuming team first.

- **Symptom:** After migrating a cluster from ZooKeeper to KRaft (or
  after any broker.rack change), replica placement doesn't actually
  spread across racks the way `broker.rack` implies.
  **Fix:** `broker.rack` only affects placement decisions made *after*
  it's set — existing partitions keep their existing replica assignment.
  Run `kafka-reassign-partitions.sh` with a rack-aware generated
  assignment to actually move existing replicas onto the intended racks;
  simply setting the property on already-populated brokers changes
  nothing for existing topics.

- **Symptom:** A cluster with `unclean.leader.election.enable=true` (or
  unset, defaulting to disabled in modern versions but historically
  enabled in older ones) loses committed messages after a multi-broker
  outage.
  **Fix:** With unclean leader election enabled, Kafka will elect an
  out-of-sync replica as leader rather than stay unavailable, silently
  losing any messages the new leader hadn't yet replicated. Explicitly
  set `unclean.leader.election.enable=false` for any topic where
  correctness matters more than availability during a multi-broker
  outage, and treat re-enabling it as an emergency-only, explicitly
  reasoned-about action — not a standing configuration.

## Worked example

**Scenario:** A new 3-broker KRaft cluster, spread across three AWS AZs,
hosting an `order-events` topic for an order-processing pipeline that
needs strict ordering per `customer_id` and must survive a single AZ
outage without data loss.

Controller quorum (3 dedicated controller nodes):
```properties
process.roles=controller
node.id=1
controller.quorum.voters=1@kraft-ctrl-1:9093,2@kraft-ctrl-2:9093,3@kraft-ctrl-3:9093
listeners=CONTROLLER://kraft-ctrl-1:9093
controller.listener.names=CONTROLLER
```

Broker configuration (repeated per broker with unique `node.id`,
`advertised.listeners`, and `broker.rack`):
```properties
process.roles=broker
node.id=101
controller.quorum.voters=1@kraft-ctrl-1:9093,2@kraft-ctrl-2:9093,3@kraft-ctrl-3:9093
listeners=PLAINTEXT://:9092
advertised.listeners=PLAINTEXT://broker-101.us-east-1a.internal:9092
broker.rack=us-east-1a
log.dirs=/var/kafka/data
default.replication.factor=3
min.insync.replicas=2
unclean.leader.election.enable=false
offsets.topic.replication.factor=3
```

Topic creation, sized for a projected 40 MB/s peak and up to 12 concurrent
consumer instances in the largest consumer group:
```bash
kafka-topics.sh --bootstrap-server broker-101.us-east-1a.internal:9092 \
  --create --topic order-events \
  --partitions 12 --replication-factor 3 \
  --config min.insync.replicas=2 \
  --config retention.ms=604800000 \
  --config cleanup.policy=delete
```
Producers key on `customer_id`, so all 12 partitions carry a stable
per-key mapping from day one — no partition-count change is planned,
avoiding the ordering-break pitfall above. With `broker.rack` set on all
three brokers before this topic was created, Kafka's replica placement
spreads each partition's 3 replicas one-per-AZ, so losing any single AZ
still leaves 2 in-sync replicas — satisfying `min.insync.replicas=2` and
keeping the topic writable throughout the outage.

## Cross-references

- [kafka-configuration-validation](../kafka-configuration-validation/SKILL.md) — validating this cluster's topic configs and consumer group settings before production rollout.
- [kafka-consumer-lag-and-partition-troubleshooting](../kafka-consumer-lag-and-partition-troubleshooting/SKILL.md) — diagnosing under-replicated partitions and rebalance storms that stem from the partition/replication choices made here.
- [kafka-schema-registry-and-compatibility-management](../kafka-schema-registry-and-compatibility-management/SKILL.md) — schema governance layered on top of the topics designed in this skill.

---
name: nats-and-pulsar-lightweight-messaging-configuration
description: >
  Configures NATS core pub/sub and JetStream persistence, and Apache
  Pulsar topics/subscriptions, as lighter-weight alternatives to Kafka or
  RabbitMQ, and gives a decision framework for when each fits better. Use
  when the user asks to "set up NATS," "configure JetStream streams and
  consumers," "set up Pulsar topics," "choose between NATS, Kafka, and
  RabbitMQ," "do we need Kafka for this," or is evaluating a lighter-weight
  messaging system for a new service.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: messaging-and-data-orchestration
  maturity: stable
---

# NATS and Pulsar Lightweight Messaging Configuration

## Purpose

Kafka and RabbitMQ are the default reach for most teams, but both carry
real operational weight — Kafka's broker/ZooKeeper-or-KRaft cluster and
partition-management model, RabbitMQ's exchange/vhost/clustering
concepts — that isn't justified for every workload. NATS (core pub/sub,
or JetStream for persistence) and Apache Pulsar are lighter-weight
options that trade some of Kafka's ecosystem maturity and RabbitMQ's
routing flexibility for a simpler operational model or, in Pulsar's case,
independent scaling of compute (brokers) from storage (BookKeeper). This
skill covers configuring both deliberately and — just as importantly —
deciding when they're the *right* choice instead of reaching for Kafka or
RabbitMQ by default. Topology/cluster design for the two mainstream
options is covered separately in
[kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md) and
[rabbitmq-configuration](../rabbitmq-configuration/SKILL.md).

## When to use

- Evaluating whether a new service genuinely needs Kafka or RabbitMQ, or
  whether a lighter-weight broker would meet its actual requirements with
  less operational overhead.
- Setting up NATS core pub/sub for low-latency, at-most-once,
  ephemeral messaging (service discovery, request/reply RPC-style
  patterns, lightweight event fan-out).
- Setting up NATS JetStream when at-least-once delivery and message
  persistence/replay are needed but a full Kafka deployment is more than
  the workload justifies.
- Setting up Apache Pulsar topics and subscriptions, particularly when
  independent scaling of brokers vs. storage, or built-in multi-tenancy,
  is a genuine requirement.
- Reviewing an existing lightweight-messaging deployment for a durability
  or delivery-guarantee gap relative to what the application actually
  assumes.

## Prerequisites & environment

- For NATS: a running `nats-server` (single node for core pub/sub
  experimentation; at least 3 nodes in a clustered/JetStream deployment
  for meaningful HA, since JetStream replication also relies on Raft
  consensus similar to Kafka's controller quorum or RabbitMQ's quorum
  queues) and the `nats` CLI for stream/consumer administration.
- For Pulsar: a running broker + BookKeeper (+ ZooKeeper or the
  metadata-store equivalent used by the deployed version) cluster, and
  the `pulsar-admin` CLI or REST admin API for tenant/namespace/topic
  administration. Pulsar's broker/storage split means broker and
  BookKeeper node counts are sized independently — don't assume a 1:1
  node relationship the way Kafka's broker-holds-its-own-log model
  implies.
- A clear statement of the workload's actual delivery-guarantee
  requirement (at-most-once fire-and-forget vs. at-least-once with
  replay) and durability requirement (fine to lose in-flight messages on a
  restart vs. must survive a broker restart) — this drives both the
  broker choice and the specific configuration (core NATS vs. JetStream;
  Pulsar's persistent vs. non-persistent topics).
- Client libraries for the target language (NATS has official clients for
  most mainstream languages; Pulsar's client library ecosystem is
  somewhat narrower — check availability/maturity for less common
  languages before committing).

## Step-by-step guidance

1. **Decide core NATS vs. JetStream vs. Pulsar vs. Kafka/RabbitMQ using
   the actual requirement, not familiarity or hype.** A rough decision
   framework:
   - **Core NATS**: fire-and-forget pub/sub or request/reply, no
     persistence needed, lowest latency and operational footprint of the
     options here — a message published with no subscriber listening is
     simply gone, and that's an acceptable, expected behavior for the use
     case (e.g. live service-health broadcasts, ephemeral cache
     invalidation).
   - **NATS JetStream**: the workload needs at-least-once delivery,
     message replay, or consumer acknowledgment/redelivery, but the
     team wants a much simpler operational model than Kafka (single
     `nats-server` binary, no separate coordination service beyond the
     cluster's own Raft group) and doesn't need Kafka's partition-level
     ordering/throughput ceiling or its broad connector/stream-processing
     ecosystem.
   - **Pulsar**: the workload needs Kafka-like durability/replay *and*
     either independent scaling of brokers vs. storage (bursty compute
     needs without over-provisioning storage nodes, or vice versa),
     built-in geo-replication, or built-in multi-tenancy (isolated
     tenants/namespaces sharing infrastructure) as a first-class feature
     rather than something bolted on.
   - **Kafka**: high sustained throughput, an ecosystem of existing
     Kafka-native tooling (Kafka Streams, Connect, ksqlDB, schema
     registry — see
     [kafka-schema-registry-and-compatibility-management](../kafka-schema-registry-and-compatibility-management/SKILL.md)),
     or strict per-key ordering at high partition counts is the deciding
     factor.
   - **RabbitMQ**: complex routing logic (topic/header-based routing,
     priority queues, per-consumer routing patterns) matters more than
     raw throughput — see
     [rabbitmq-configuration](../rabbitmq-configuration/SKILL.md).
   Don't default to Kafka "because that's what we already run" if a new
   service's actual requirement is closer to core NATS's fire-and-forget
   model — the operational cost of running (and keeping someone who
   understands) a Kafka cluster is real and should be weighed against a
   genuinely simpler fit.

2. **Configure core NATS pub/sub** for the fire-and-forget case:
   ```bash
   # publish
   nats pub orders.created '{"order_id": "o-123", "status": "created"}'
   # subscribe
   nats sub "orders.>"
   ```
   `orders.>` is a wildcard subject subscription (NATS subjects are
   dot-separated hierarchies, roughly analogous to RabbitMQ topic-exchange
   routing keys) — `>` matches one or more trailing tokens, `*` matches
   exactly one token. There is no broker-side persistence here: a
   subscriber that isn't connected when a message publishes never sees
   it.

3. **Enable JetStream and create a stream when persistence/replay is
   needed**:
   ```bash
   nats stream add ORDERS \
     --subjects "orders.>" \
     --storage file \
     --retention limits \
     --max-msgs=-1 \
     --max-age=168h \
     --replicas=3
   ```
   `--storage file` persists to disk (vs. `memory`, which doesn't survive
   a server restart); `--replicas=3` requires a 3+ node JetStream cluster
   and gives Raft-based replication comparable in spirit to Kafka's
   replication factor or RabbitMQ's quorum queues — a `--replicas=1`
   stream has no redundancy and is a single point of failure the same way
   an unreplicated Kafka partition or a classic RabbitMQ queue with no
   mirrors would be.

4. **Create a durable consumer with explicit ack policy and redelivery
   bounds**, mirroring the poison-message safeguard covered for RabbitMQ
   in
   [rabbitmq-queue-and-dead-letter-troubleshooting](../rabbitmq-queue-and-dead-letter-troubleshooting/SKILL.md):
   ```bash
   nats consumer add ORDERS fulfillment-worker \
     --filter "orders.created" \
     --ack explicit \
     --max-deliver 5 \
     --deliver last \
     --wait 30s
   ```
   `--max-deliver 5` caps redelivery attempts before JetStream stops
   redelivering that message to this consumer, the JetStream equivalent
   of RabbitMQ's `x-delivery-limit` — without a bound, a message the
   consumer can never successfully process would otherwise redeliver
   indefinitely.

5. **For Pulsar, create a tenant/namespace/topic hierarchy deliberately**,
   using the multi-tenancy model as an isolation boundary the way vhosts
   isolate RabbitMQ applications:
   ```bash
   pulsar-admin tenants create orders-org
   pulsar-admin namespaces create orders-org/fulfillment
   pulsar-admin namespaces set-retention orders-org/fulfillment \
     --size 10G --time 7d
   pulsar-admin topics create-partitioned-topic \
     persistent://orders-org/fulfillment/order-events --partitions 6
   ```
   A `persistent://` topic writes to BookKeeper for durability; a
   `non-persistent://` topic behaves closer to core NATS's fire-and-forget
   model (in-memory only, no durability) — choose deliberately per topic
   rather than defaulting to whichever the client library's example
   snippet happened to use.

6. **Choose a Pulsar subscription type based on the actual fan-out/
   ordering need**:
   ```bash
   # Exclusive: one consumer only, strict order
   # Shared: round-robin across consumers, no per-key ordering guarantee
   # Key_Shared: like Shared, but same-key messages always go to the same consumer
   # Failover: one active consumer, others on standby for automatic failover
   ```
   `Key_Shared` is the closest Pulsar analogue to Kafka's partition-key
   ordering guarantee combined with multi-consumer parallelism — use it
   when messages for the same entity (e.g. `order_id`) must be processed
   in order but overall throughput needs more than one consumer.

7. **Set explicit retention and TTL/backlog quotas on any persistent
   stream/topic**, the same durability-vs-unbounded-growth tradeoff
   covered for RabbitMQ in
   [rabbitmq-configuration-validation](../rabbitmq-configuration-validation/SKILL.md):
   ```bash
   pulsar-admin namespaces set-backlog-quota orders-org/fulfillment \
     --limit 10G --policy producer_exception
   ```
   `producer_exception` blocks further publishes once the quota is hit
   (loud failure) rather than silently discarding the oldest messages —
   choose the overflow policy deliberately based on whether silent data
   loss or blocked publishing is the safer failure mode for the workload.

## Best practices

- Treat "we already run Kafka/RabbitMQ" as a real cost-saving argument for
  reusing existing infrastructure, but not a substitute for checking
  whether a new service's actual delivery-guarantee and throughput needs
  are better served by a lighter-weight option — infrastructure sprawl
  from running three message brokers is also a real cost to weigh against
  the fit of each.
- Default new JetStream streams/Pulsar persistent topics to `--replicas 3`
  (or Pulsar's equivalent ensemble/write-quorum/ack-quorum settings) for
  anything where losing the whole stream/topic on a single node failure
  is unacceptable — a single-replica stream is a single point of failure
  regardless of how it's labeled.
- Set an explicit `--max-deliver`/redelivery bound on every durable
  JetStream consumer and a dead-letter-topic policy on Pulsar
  subscriptions, mirroring the poison-message protection covered in
  [rabbitmq-queue-and-dead-letter-troubleshooting](../rabbitmq-queue-and-dead-letter-troubleshooting/SKILL.md) —
  don't assume lighter-weight brokers are exempt from the poison-message
  problem.
- Use Pulsar's tenant/namespace hierarchy as a real isolation boundary
  between teams/applications, the same way RabbitMQ vhosts are used in
  [rabbitmq-configuration](../rabbitmq-configuration/SKILL.md) — don't
  flatten everything into one namespace "to keep it simple."
- Benchmark against the workload's actual message size/rate before
  committing to a broker choice based on published performance
  characteristics — relative performance between these systems is
  workload- and configuration-dependent, and this skill deliberately
  avoids citing specific throughput/latency numbers that vary by version,
  hardware, and message size.

## Common pitfalls

- **Symptom:** A service migrated from core NATS pub/sub to JetStream
  assuming it would "just work," but consumers report duplicate message
  processing.
  **Fix:** JetStream's `--ack explicit` delivery is at-least-once by
  design — a message is redelivered if not acked within the consumer's
  ack-wait window, including cases where the consumer *did* process it but
  the ack was lost/delayed. Consumer logic must be idempotent (safe to
  process the same message twice), the same requirement that applies to
  any at-least-once system (Kafka, RabbitMQ, JetStream, Pulsar) — this
  isn't specific to JetStream, but teams moving from fire-and-forget core
  NATS often haven't built for it yet.

- **Symptom:** A JetStream stream or Pulsar topic created with a single
  replica/no redundancy loses all its messages when the one node hosting
  it fails.
  **Fix:** This is the direct consequence of skipping replication — check
  `--replicas` (JetStream) or the namespace's ensemble/ack-quorum settings
  (Pulsar) before treating any stream/topic as production-durable. A
  single-node stream is equivalent in risk to an unreplicated Kafka
  partition or a non-mirrored classic RabbitMQ queue.

- **Symptom:** A team picks Pulsar for a new service expecting Kafka-like
  throughput and a mature Kafka Connect-style ecosystem, but hits friction
  because a needed connector or client library either doesn't exist or is
  far less mature than its Kafka equivalent.
  **Fix:** Verify the specific connector/client/tooling ecosystem
  maturity for the target language and use case *before* committing,
  rather than assuming Pulsar's core feature set (partitioning,
  durability, multi-tenancy) implies ecosystem parity with Kafka — if the
  team's actual need is that ecosystem, Kafka
  ([kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md))
  may still be the better fit despite Pulsar's architectural advantages.

- **Symptom:** A NATS JetStream consumer with no `--max-deliver` set
  redelivers a message indefinitely because the consumer's handler always
  throws on that specific payload.
  **Fix:** This is the same poison-message pattern covered for RabbitMQ in
  [rabbitmq-queue-and-dead-letter-troubleshooting](../rabbitmq-queue-and-dead-letter-troubleshooting/SKILL.md) —
  set an explicit `--max-deliver` bound and configure a dead-letter
  subject/stream (via `--max-deliver` combined with a subject the consumer
  publishes failed messages to) so a bad message surfaces for
  investigation instead of looping forever and starving other messages
  behind it in ordered delivery.

## Worked example

**Scenario:** A new internal "shipment status" service needs to notify
several downstream services whenever a shipment's status changes. The
team's first instinct is "we already run Kafka, just add a topic," but
the actual requirements are: fewer than 50 messages/second, downstream
services only care about the *current* status (not a full history/replay
requirement beyond a short window), and the team wants to avoid adding
another Kafka topic (with its consumer-group/partition-count decisions)
for something this small.

Decision: this is a good fit for NATS JetStream rather than Kafka — the
throughput is trivial for either system, but JetStream's operational
footprint (a single `nats-server` binary, no separate schema registry or
partition-rebalancing concerns) is a better match than adding to an
already-large Kafka deployment for a low-volume, short-retention use case.
Core NATS (no persistence) is rejected because downstream services do
need at-least-once delivery — a dropped status update would show a stale
shipment status to customers.

Stream and consumer setup:
```bash
nats stream add SHIPMENT_STATUS \
  --subjects "shipments.status.>" \
  --storage file \
  --retention limits \
  --max-age=24h \
  --replicas=3

nats consumer add SHIPMENT_STATUS notifications-worker \
  --filter "shipments.status.updated" \
  --ack explicit \
  --max-deliver 5 \
  --deliver last \
  --wait 30s
```
`--max-age=24h` matches the requirement that only recent history matters
— unlike Kafka, where retention is usually set far longer for replay/
reprocessing use cases, this stream deliberately keeps a short window
since nothing downstream needs to replay shipment status from a week ago.
`--replicas=3` still ensures the stream survives a single-node failure
despite the low message volume, since durability matters even though
throughput doesn't.

Publisher:
```python
nc = await nats.connect("nats://nats-cluster:4222")
js = nc.jetstream()
await js.publish("shipments.status.updated", shipment_status_payload)
```
Consumer acks explicitly after successfully processing, and a message
that fails 5 times (e.g. a malformed payload from a buggy upstream
release) stops redelivering to this consumer and is flagged via the
consumer's `num_pending`/`num_redelivered` metrics for investigation,
rather than looping indefinitely.

## Cross-references

- [kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md) — the heavier-weight alternative this skill's decision framework compares against for high-throughput/ecosystem-dependent workloads.
- [rabbitmq-configuration](../rabbitmq-configuration/SKILL.md) — the heavier-weight alternative for complex routing needs, and the source of the vhost-isolation pattern mirrored here in Pulsar's tenant/namespace model.
- [rabbitmq-queue-and-dead-letter-troubleshooting](../rabbitmq-queue-and-dead-letter-troubleshooting/SKILL.md) — the poison-message/dead-letter diagnostic pattern that applies equally to JetStream's `--max-deliver` and Pulsar's dead-letter policy.

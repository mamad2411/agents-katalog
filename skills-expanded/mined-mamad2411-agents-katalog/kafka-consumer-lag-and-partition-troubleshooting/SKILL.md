---
name: kafka-consumer-lag-and-partition-troubleshooting
description: >
  Diagnoses growing Kafka consumer lag, rebalance storms, and
  under-replicated partitions in a running cluster. Use when the user
  reports "consumer lag keeps growing," "consumer group stuck
  rebalancing," "under-replicated partitions," "Kafka consumers keep
  dropping out of the group," or asks to troubleshoot a Kafka production
  incident involving lag or partition health.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: messaging-and-data-orchestration
  maturity: stable
---

# Kafka Consumer Lag and Partition Troubleshooting

## Purpose

Growing consumer lag, a consumer group stuck in repeated rebalances, or a
climbing under-replicated-partition count are three of the most common
Kafka production symptoms, and they often share root causes — a slow
consumer, an overloaded broker, or a partition/replica imbalance
introduced at design time (see
[kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md)).
This skill is the diagnostic playbook for isolating which of those root
causes is actually responsible in a live incident, rather than guessing
at fixes (adding more consumers, restarting brokers) that don't address
the underlying problem.

## When to use

- Consumer lag (`kafka-consumer-groups.sh --describe`) is growing steadily
  rather than staying flat or catching up.
- A consumer group's members are rebalancing repeatedly ("rebalance
  storm"), with consumers joining and leaving the group every few
  seconds/minutes instead of settling into stable partition assignment.
- `UnderReplicatedPartitions` or `OfflinePartitionsCount` broker metrics
  are non-zero and not immediately self-resolving.
- A consumer group appears "stuck" — lag frozen at a non-zero value with
  no progress despite the consumer process reporting itself healthy.
- Investigating a paging alert tied to any of the above metrics.

## Prerequisites & environment

- Access to broker JMX metrics or an equivalent metrics pipeline
  (Prometheus + `kafka-exporter`/JMX exporter, Confluent Control Center,
  or Cruise Control) exposing `UnderReplicatedPartitions`,
  `ConsumerLag`, and per-broker request/response queue metrics.
- `kafka-consumer-groups.sh` and `kafka-topics.sh` CLI access to the
  cluster (or equivalent read access via an admin API client).
- Application-level metrics or logs for the consuming service (processing
  time per record/batch, error rate, GC pauses) — broker-side metrics
  alone can show *that* lag is growing but not *why* the consumer is
  slow.
- Knowledge of the consumer group's expected steady-state throughput and
  partition count, to distinguish "lag is growing because of a real
  regression" from "lag is growing because traffic legitimately
  increased beyond current consumer capacity."

## Step-by-step guidance

1. **Quantify the lag and its trend before reacting** — a snapshot lag
   number without a trend can't tell you if it's an active incident or a
   transient blip:
   ```bash
   kafka-consumer-groups.sh --bootstrap-server broker-101:9092 \
     --describe --group order-fulfillment-service
   ```
   Look at `LAG` per partition, not just the group total — lag
   concentrated on one or two partitions (not spread evenly) points to a
   hot-key/skewed-partition problem rather than a group-wide slowdown;
   run this repeatedly a minute apart to see the trend direction, not
   just one sample.

2. **Distinguish "consumer is too slow" from "consumer isn't running" or
   "consumer is stuck in rebalance."** Check the group's member list and
   state:
   ```bash
   kafka-consumer-groups.sh --bootstrap-server broker-101:9092 \
     --describe --group order-fulfillment-service --members --verbose
   ```
   - If `STATE` shows `PreparingRebalance`/`CompletingRebalance`
     repeatedly across successive checks, this is a rebalance storm —
     go to step 3.
   - If members are present, stable, and assigned, but lag still grows,
     this is a genuine processing-throughput problem — go to step 4.
   - If a partition shows no assigned consumer at all, there are fewer
     active consumer instances than partitions, or a consumer crashed —
     check the consuming application's own health/logs directly.

3. **For a rebalance storm, check `session.timeout.ms`/
   `max.poll.interval.ms` against actual per-poll processing time** —
   the most common cause is a consumer taking longer between `poll()`
   calls than `max.poll.interval.ms` allows, which the broker treats as
   the consumer having left the group, triggering a rebalance, after
   which the same slow processing causes it again:
   ```properties
   # consumer.properties
   max.poll.interval.ms=300000   # raise if per-batch processing genuinely takes longer
   max.poll.records=200          # or lower this so each poll's batch finishes well within the interval
   session.timeout.ms=45000
   heartbeat.interval.ms=15000
   ```
   Also check for a static membership setup
   (`group.instance.id`) if consumers restart frequently (e.g. rolling
   deploys) — without it, every restart is treated as a member
   leaving-then-rejoining, forcing a full rebalance instead of a quick
   rejoin to the same partition assignment.

4. **For genuine processing-throughput lag, check whether the bottleneck
   is consumer-side or broker-side.** Consumer-side: look at
   application metrics for per-record/per-batch processing latency,
   downstream call latency (a database or external API the consumer
   calls), and GC pause time. Broker-side: check `RequestQueueSize`,
   `NetworkProcessorAvgIdlePercent`, and disk I/O wait on the leader
   broker(s) for the lagging partitions:
   ```bash
   kafka-run-class.sh kafka.tools.JmxTool \
     --object-name kafka.network:type=RequestChannel,name=RequestQueueSize \
     --jmx-url service:jmx:rmi:///jndi/rmi://broker-101:9999/jmxrmi
   ```
   If broker-side queue/I-O metrics are elevated on the leader for the
   lagging partitions specifically (not cluster-wide), that points to a
   hot broker or hot partition rather than a slow consumer application.

5. **Check for partition/key skew** if lag concentrates on specific
   partitions while others stay near zero:
   ```bash
   kafka-log-dirs.sh --bootstrap-server broker-101:9092 \
     --describe --topic-list order-events | jq .
   ```
   Uneven partition sizes indicate a producer key with poor cardinality
   or distribution (e.g. keying on a low-cardinality `region` field
   instead of `customer_id`) sending disproportionate volume to a few
   partitions. This is a producer/topic-design issue, not something a
   consumer-side fix resolves — remediation belongs back in
   [kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md)'s
   partition-key guidance, and validating the fix belongs in
   [kafka-configuration-validation](../kafka-configuration-validation/SKILL.md).

6. **For under-replicated partitions, identify which broker is
   under-replicating and why**:
   ```bash
   kafka-topics.sh --bootstrap-server broker-101:9092 \
     --describe --under-replicated-partitions
   ```
   Common causes: a broker under sustained I/O or network saturation
   falling behind on replication fetch requests, a broker that just
   restarted and is still catching up (transient — should self-resolve
   as `Isr` converges back to the full replica set), or a genuinely
   failed/unreachable broker. Cross-check with broker-level CPU/disk/network
   metrics for the specific under-replicating broker, not cluster
   aggregates.

7. **Only add consumer instances or partitions as a fix once the actual
   bottleneck is confirmed to be consumer parallelism**, not before. If
   the consumer group already has as many active members as partitions,
   adding more consumer instances beyond the partition count does
   nothing (they sit idle) — the fix is either increasing partition
   count (with the ordering-guarantee caveics from
   [kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md))
   or making per-partition processing faster, not blindly scaling the
   consumer deployment.

## Best practices

- Alert on consumer lag *trend* (a sustained positive slope over N
  minutes) rather than a static lag threshold — a topic with bursty
  traffic can spike lag briefly and drain it without any real problem,
  while a low but steadily climbing lag on a high-throughput topic is a
  real early warning.
- Alert on `UnderReplicatedPartitions > 0` sustained for more than a
  short grace period (a few minutes) rather than instantaneously, to
  avoid paging on transient replication catch-up after a routine broker
  restart.
- Use static group membership (`group.instance.id`) for consumer
  deployments that restart routinely (rolling deploys, autoscaling) to
  avoid unnecessary full rebalances on every restart.
- Instrument the consuming application with its own processing-latency
  metrics per stage (deserialize, business logic, downstream call,
  commit) — broker-side lag metrics tell you *that* something is slow,
  application-side metrics tell you *where*.
- Keep `max.poll.records` and per-record processing time such that a full
  batch reliably finishes well inside `max.poll.interval.ms`, with margin
  for a slow downstream dependency — don't tune `max.poll.interval.ms`
  up indefinitely to paper over an unbounded processing time instead.

## Common pitfalls

- **Symptom:** Consumer lag grows, so more consumer instances are added
  to the deployment, but lag doesn't improve.
  **Fix:** Check partition count first — a consumer group can never have
  more *active* consumers than partitions; excess instances sit
  completely idle. If the group already has one active consumer per
  partition, the fix is either faster per-partition processing or more
  partitions (with the ordering caveats in
  [kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md)),
  not more consumer replicas.

- **Symptom:** A consumer group rebalances every few minutes indefinitely,
  and lag grows specifically *because* of the rebalancing (no consumer
  ever gets a stable window to make progress).
  **Fix:** This is almost always `max.poll.interval.ms` being exceeded by
  actual per-poll processing time, which the broker reads as the
  consumer having died. Check the consumer's actual time between `poll()`
  calls (add explicit logging/metrics around the poll loop if not
  already present) and either genuinely reduce per-batch processing time
  (smaller `max.poll.records`, offload slow work to an async
  worker acknowledged before commit) or raise `max.poll.interval.ms` to
  match a legitimately longer processing time — don't just raise the
  interval blindly without confirming the processing time is actually
  bounded.

- **Symptom:** `UnderReplicatedPartitions` spikes cluster-wide right
  after a routine rolling broker restart (e.g. for a config change or
  patch), and someone starts an incident response before checking
  whether it's expected.
  **Fix:** A restarted broker's replicas are legitimately behind until
  they finish catching up; this is expected and should self-resolve
  within the deployment's configured restart interval. Confirm the ISR
  set is converging back to full (`kafka-topics.sh --describe` showing
  `Isr` matching `Replicas` again) before escalating — but do treat it
  as a real incident if the metric doesn't converge within the expected
  catch-up window, since that indicates a broker actually struggling,
  not just catching up.

- **Symptom:** Lag is concentrated on 1–2 partitions out of many, while
  the rest sit near zero, and adding consumers or tuning poll settings
  doesn't help.
  **Fix:** This is partition/key skew, not a consumer configuration
  problem — check producer-side key distribution
  (`kafka-log-dirs.sh --describe` to compare partition sizes). The real
  fix is a better partition key (higher cardinality, more even
  distribution) chosen at topic/producer design time, which is a
  [kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md)
  concern, not something tunable from the consumer side alone.

## Worked example

**Scenario:** An on-call engineer is paged for "consumer lag growing" on
the `order-fulfillment-service` consumer group reading `order-events`.

Step 1 — trend check:
```
GROUP                      TOPIC          PARTITION  LAG
order-fulfillment-service  order-events   0          45000
order-fulfillment-service  order-events   1          200
order-fulfillment-service  order-events   2          180
...
```
Lag is almost entirely on partition 0; partitions 1–11 are near zero.
This immediately rules out a group-wide slow-consumer problem (step 4)
and points at partition skew (step 5).

Partition size check:
```bash
kafka-log-dirs.sh --bootstrap-server broker-101:9092 \
  --describe --topic-list order-events
```
Partition 0's log size is roughly 8x any other partition's — confirming
skew. Producer-side investigation finds the `order-events` producer keys
messages on `warehouse_region`, and one region (`us-east`) accounts for
the large majority of order volume, all landing on the single partition
that region's key hashes to.

Root cause: a low-cardinality, uneven partition key, not a consumer or
broker problem. Immediate mitigation: temporarily add a
`consumer.pause()`/backpressure-aware retry on the fulfillment service
for partition 0 specifically to avoid cascading timeouts downstream
while a fix is prepared. Actual fix (tracked as a follow-up, not done
live during the incident given the ordering-guarantee implications):
re-key the producer on `order_id` instead of `warehouse_region` for even
distribution across all 12 partitions, following the partition-key
guidance in
[kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md),
and validate the new key distribution in staging via
[kafka-configuration-validation](../kafka-configuration-validation/SKILL.md)
before rolling out to production.

## Cross-references

- [kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md) — partition/replication design decisions that are frequently the root cause of the symptoms diagnosed here.
- [kafka-configuration-validation](../kafka-configuration-validation/SKILL.md) — pre-production checks that catch consumer group and topic misconfigurations before they become live-incident lag/rebalance problems.
- [kafka-schema-registry-and-compatibility-management](../kafka-schema-registry-and-compatibility-management/SKILL.md) — a schema-incompatible message can also cause a consumer to stall/error-loop, which looks like lag but has a different root cause and fix.

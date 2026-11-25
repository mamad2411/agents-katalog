---
name: kafka-configuration-validation
description: >
  Validates Kafka topic configuration (retention, cleanup policy,
  replication, min.insync.replicas) and consumer group settings before a
  production rollout. Use when the user asks to "review a Kafka topic
  config before deploying," "validate retention/compaction settings,"
  "check consumer group config for a new service," or "audit Kafka topics
  for production readiness" prior to go-live.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: messaging-and-data-orchestration
  maturity: stable
---

# Kafka Configuration Validation

## Purpose

A Kafka topic or consumer group that is misconfigured rarely fails loudly
at creation time — `kafka-topics.sh --create` succeeds even with
`replication.factor=1`, an unbounded `retention.ms`, or a
`cleanup.policy` that silently deletes the compacted state a consumer
relies on. Those mistakes surface later, in production, as data loss, disk
exhaustion, or a consumer group replaying far more history than intended.
This skill is a pre-production checklist and set of concrete commands for
validating topic and consumer group configuration *before* the first
production message is written — building on the design choices made in
[kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md)
rather than repeating them.

## When to use

- Before promoting a newly created topic from staging to production.
- Reviewing a pull request or infra-as-code change that creates or alters
  Kafka topic configuration.
- Onboarding a new consumer group and validating its `group.id`,
  `auto.offset.reset`, and commit strategy won't cause unexpected replay
  or data loss.
- Auditing an existing cluster's topics for configuration drift from the
  organization's durability/retention standards.
- As a gate in a CI/CD pipeline that provisions Kafka topics via
  Terraform, a GitOps operator, or a custom provisioning script.

## Prerequisites & environment

- Read access to the target cluster's topic configs
  (`kafka-topics.sh --describe`, `kafka-configs.sh --describe`) or the
  equivalent Terraform/Kafka-operator state if topics are managed as
  code.
- Kafka CLI tools matching (or compatible with) the broker version —
  config option names and defaults have changed across major versions
  (e.g. `log.message.format.version` is obsolete on brokers running the
  Kafka 3.x message format unconditionally).
- A documented organizational baseline for what "production ready" means
  for this cluster (minimum replication factor, required
  `min.insync.replicas`, retention ceiling, naming convention) — this
  skill validates *against* such a baseline; if none exists, establishing
  one is the first real step.
- For consumer-group validation: visibility into the consuming
  application's configuration (not just the broker side), since
  `auto.offset.reset` and commit mode are client-side settings.

## Step-by-step guidance

1. **Pull the actual applied topic configuration, not just the intended
   one** — defaults and overrides can diverge from what was requested:
   ```bash
   kafka-topics.sh --bootstrap-server broker-101:9092 \
     --describe --topic order-events
   kafka-configs.sh --bootstrap-server broker-101:9092 \
     --describe --entity-type topics --entity-name order-events
   ```
   Confirm `ReplicationFactor`, the number of partitions, and any
   per-topic config overrides (retention, cleanup policy) match what was
   intended, not the cluster-wide default.

2. **Validate replication and durability settings against the production
   baseline**:
   ```bash
   # Fails validation if any of these hold for a production topic:
   #   ReplicationFactor < 3
   #   min.insync.replicas not set or < 2
   #   unclean.leader.election.enable=true (topic or cluster override)
   kafka-configs.sh --bootstrap-server broker-101:9092 \
     --describe --entity-type topics --entity-name order-events | \
     grep -E "min.insync.replicas|unclean.leader.election"
   ```
   A topic passing validation with `ReplicationFactor=3` but no explicit
   `min.insync.replicas` override is still a finding — it's inheriting
   the cluster default, which must itself have been confirmed safe (see
   [kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md)).

3. **Validate retention and cleanup policy match the topic's actual
   role.** An event-stream topic and a compacted changelog/state topic
   need opposite settings, and applying the wrong one is a common
   copy-paste error:
   ```bash
   # Event stream: bounded time retention, delete old segments
   kafka-configs.sh --bootstrap-server broker-101:9092 --alter \
     --entity-type topics --entity-name order-events \
     --add-config cleanup.policy=delete,retention.ms=604800000

   # Compacted state topic: keep latest value per key indefinitely
   kafka-configs.sh --bootstrap-server broker-101:9092 --alter \
     --entity-type topics --entity-name customer-profile-changelog \
     --add-config cleanup.policy=compact,min.cleanable.dirty.ratio=0.1,segment.ms=600000
   ```
   A topic with `cleanup.policy=compact` but no consumer ever intending
   to read the "current state" semantics (or vice versa — a state topic
   accidentally set to `delete`, silently losing keys once their segment
   ages out) is a validation failure, not a style preference.

4. **Validate the topic naming convention and ACLs are consistent with
   least-privilege access** before the topic goes live:
   ```bash
   kafka-acls.sh --bootstrap-server broker-101:9092 \
     --list --topic order-events
   ```
   Flag any `--producer`/`--consumer` ACL grant scoped to `--topic '*'`
   or a wildcard prefix broader than the specific topic/team boundary —
   a validation pass here should require ACLs scoped to the exact topic
   name or an agreed team-prefix pattern, not a blanket grant.

5. **Validate consumer group configuration on the client side** — this
   is where `auto.offset.reset` mistakes cause the most damage:
   ```properties
   # consumer.properties for the new service
   group.id=order-fulfillment-service
   auto.offset.reset=earliest   # or 'latest' — validate deliberately, not by default
   enable.auto.commit=false     # explicit offset commit after processing, not before
   isolation.level=read_committed
   ```
   Confirm `auto.offset.reset` was chosen deliberately: `earliest` means
   a consumer group with no committed offset (new group, or offsets
   expired past `offsets.retention.minutes`) replays the entire retained
   history — correct for a from-scratch backfill, dangerous for a
   at-least-once side-effecting consumer that isn't idempotent. `latest`
   means messages produced before the consumer group's first connection
   are silently skipped — dangerous if that data mattered.

6. **Validate consumer group lag and offset health before declaring the
   group production-ready**:
   ```bash
   kafka-consumer-groups.sh --bootstrap-server broker-101:9092 \
     --describe --group order-fulfillment-service
   ```
   Confirm every partition has an active member assigned (no partition
   showing a blank `CONSUMER-ID`, which indicates fewer consumer
   instances than partitions or a rebalance in progress) and that lag is
   near zero in a staging soak test before promoting to production —
   ongoing lag growth issues are diagnosed in
   [kafka-consumer-lag-and-partition-troubleshooting](../kafka-consumer-lag-and-partition-troubleshooting/SKILL.md),
   but they should be caught here, before go-live, not after.

7. **If topics are provisioned via Terraform or a GitOps operator, run
   the plan/diff as an explicit CI gate** rather than trusting manual CLI
   review alone:
   ```hcl
   resource "kafka_topic" "order_events" {
     name               = "order-events"
     replication_factor = 3
     partitions         = 12
     config = {
       "min.insync.replicas" = "2"
       "cleanup.policy"      = "delete"
       "retention.ms"        = "604800000"
     }
   }
   ```
   `terraform plan` output showing an unexpected reduction in
   `replication_factor` or `partitions` (Kafka rejects partition
   decreases and silently no-ops replication-factor changes made this
   way — see the pitfall below) should block the apply until reconciled.

## Best practices

- Encode the production baseline (min replication factor, required
  `min.insync.replicas`, retention ceiling, naming/ACL convention) as a
  machine-checkable policy (an OPA/Conftest policy over Terraform plan
  JSON, or a small validation script) rather than a checklist a human
  re-reads each time.
- Validate consumer-side settings (`auto.offset.reset`, commit mode,
  `isolation.level`) with the same rigor as broker-side topic config —
  the broker's durability guarantees are irrelevant if the consumer reads
  data at the wrong offset or commits before processing completes.
- Run new consumer groups against a staging/soak topic first and confirm
  lag stays flat under representative load before pointing them at
  production topics.
- Treat `cleanup.policy` as topic-role metadata, not an afterthought —
  name compacted topics distinctly (e.g. a `-changelog` or `-state`
  suffix) so the intended policy is obvious from the topic name during
  review.
- Re-run validation after any partition count increase or replication
  factor change — these operations have sharp edges (see pitfalls) that
  a one-time validation at topic creation won't catch.

## Common pitfalls

- **Symptom:** A Terraform apply that changes `replication_factor` on an
  existing `kafka_topic` resource reports success, but `kafka-topics.sh
  --describe` still shows the old replication factor.
  **Fix:** Most Kafka Terraform providers and `kafka-configs.sh` cannot
  change replication factor in place — it requires a partition
  reassignment (`kafka-reassign-partitions.sh`) run separately. Validate
  replication factor changes by actually re-describing the topic after
  apply, not by trusting the provisioning tool's reported success.

- **Symptom:** A new consumer group deployed with `auto.offset.reset=
  earliest` (left at a language client's library default) starts
  processing, and a side-effecting consumer (e.g. one that sends emails
  or charges payments) replays weeks of retained history and re-triggers
  every side effect.
  **Fix:** Validate `auto.offset.reset` explicitly for every new consumer
  group against whether the consumer is idempotent. For a non-idempotent,
  side-effecting consumer, either start it with `latest` plus a
  deliberate backfill mechanism, or make the consumer idempotent (dedupe
  on a message key/id) before ever running it with `earliest` against a
  topic with real history.

- **Symptom:** A compacted topic (`cleanup.policy=compact`) intended as a
  changelog silently drops keys older consumers expected to still be
  able to read.
  **Fix:** Compaction keeps only the latest value per key, and
  tombstones (null-value records) are actually removed after
  `delete.retention.ms`. Validate that any consumer relying on reading
  the full changelog (not just current state) either reads it before
  compaction removes older segments, or that the topic should actually
  be `delete`-policy with long retention instead of `compact`.

- **Symptom:** A validation pass approves a topic with
  `min.insync.replicas=2` and `ReplicationFactor=3`, but the producing
  service still loses acknowledged messages during a broker outage.
  **Fix:** Broker-side `min.insync.replicas` is necessary but not
  sufficient — the producer must also be configured with `acks=all` (and
  ideally `retries` with idempotence enabled,
  `enable.idempotence=true`). Validation of topic config alone misses
  this; it must include the producer client configuration for the same
  service.

## Worked example

**Scenario:** A pull request adds a new topic `payment-events` and a new
consumer group `fraud-detection-service` ahead of a production rollout;
this skill's checklist runs as a pre-merge review.

Applied topic config pulled for review:
```
Topic: payment-events  PartitionCount: 6  ReplicationFactor: 3
  Configs: min.insync.replicas=2,cleanup.policy=delete,retention.ms=2592000000
```
Replication factor and `min.insync.replicas` pass the baseline (RF≥3,
`min.insync.replicas`≥2). Retention of 30 days is confirmed intentional
(fraud review window requirement), not a leftover default.

Consumer configuration submitted with the PR:
```properties
group.id=fraud-detection-service
auto.offset.reset=latest
enable.auto.commit=false
isolation.level=read_committed
```
Review flags `auto.offset.reset=latest`: the fraud-detection service is
new, so on first deploy it would skip all payment events produced before
its first connection — for a fraud-review use case, that's a silent
correctness gap, not an acceptable default. The fix requested in review:
either switch to `earliest` for the first deployment only (since the
consumer is idempotent — it writes fraud flags keyed by
`payment_event_id`, safe to reprocess) with a follow-up ticket to revert
to `latest` semantics for offset resets after the initial catch-up, or
run an explicit one-time backfill job instead. Producer config for the
payment service is checked in the same review and confirmed to already
set `acks=all` and `enable.idempotence=true`. Only after both the
`auto.offset.reset` fix and the producer-config confirmation land does
the PR pass validation and merge.

## Cross-references

- [kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md) — the broker/topic design decisions this skill validates against a production baseline.
- [kafka-consumer-lag-and-partition-troubleshooting](../kafka-consumer-lag-and-partition-troubleshooting/SKILL.md) — ongoing lag/rebalance issues that should be caught here pre-production but sometimes surface after go-live anyway.
- [kafka-schema-registry-and-compatibility-management](../kafka-schema-registry-and-compatibility-management/SKILL.md) — schema compatibility validation to run alongside topic config validation for the same rollout.

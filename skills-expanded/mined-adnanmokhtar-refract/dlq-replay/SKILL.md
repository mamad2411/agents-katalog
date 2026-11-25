---
name: dlq-replay
description: "Replay a dead-letter queue or failed set after its cause is fixed: dry-run list, sample one, native redrive, rate-limited, verified."
kind: skill
pack: distributed-systems
allowed-tools: [Read, Write, Grep, Glob, Bash]
---

# Skill: dlq-replay

DLQ messages don't fix themselves. After the cause is fixed and shipped, the messages need a replay — and a replay is a **write to a live broker**: it re-runs every effect those messages carry. This skill does it on a named target, one sample first, through the broker's own redrive where one exists, and checks afterwards that it did what it claimed.

## Premise

Real signals only. Cite the actual DLQ or failed set, the broker and its version, the target queue or topic, and the message ids. Every claim ("cause fixed", "idempotency held", "replay safe") cites the commit, the test or the broker read that supports it. The sample's verdict comes from the live handler outcome — not "should work". Depth before and after, the replay rate and the duplicate count are read from the broker and the effect store. No replay without an audit trail of who, when, how many and the outcome.

**Named target only.** The user names the broker endpoint, the account or cluster, and the DLQ (`--target=<broker>=<endpoint>`, `--profile=<cloud profile>@<region>`). Nothing runs against a default cloud profile or a default kube context: the first line of every Bash block that may run a cloud or cluster tool is `SCAN=$(mktemp -d "${TMPDIR:-/tmp}/dlq.XXXXXX"); export KUBECONFIG="$SCAN/empty-kubeconfig"; : > "$KUBECONFIG"`, and before any write the skill prints which account it is in (`aws sts get-caller-identity --profile <profile>`, the broker's cluster name, the Redis `INFO server` line) and stops for the user's confirmation if it is not the one named.

## Halt conditions

- **No named target, or the identity read does not match it** — halt; never fall back to a default profile, context or URL.
- **Bulk replay without a successful single-message sample** — refuse.
- **The cause is not shown deployed** (the fix commit and the running version) — refuse; a replay before the fix re-poisons the queue.
- **The consumer's reserve is not verified** — halt. The handler must dedupe on a **stable** id (`broker-semantics.md` rows ID1–ID9), in the effect's transaction, and the replay path must keep that id: an SQS redrive assigns a **new `MessageId`** (below), so a consumer keyed on the SQS `MessageId` double-applies every replayed message.
- **Peak-traffic window** — halt; replay competes with live load.
- **A message leaves the DLQ before the target accepted it** — never delete first; the native redrive tasks below move-then-delete themselves.
- **Ordering keys would be lost** — a FIFO `MessageGroupId`, a Kafka record key, a Pub/Sub ordering key the consumers rely on — halt until the replay path carries them.

## When to use

- The root cause of a poison message is fixed and deployed (handler bug, schema drift, a downstream recovered).
- A periodic drain after `/audit-distributed-tx` (the `/ds-audit --runtime` lane) counted a DLQ.
- Disaster recovery: events lost during an outage, replayed from a buffered store.

## When NOT to use

- The cause is not fixed → the replay re-poisons the queue.
- The handler has no atomic reserve on a stable id → the replay duplicates effects. That is a `/ds-audit` finding (`messaging-scan` § 2) to fix first.
- During peak load.
- To read DLQ depth only → `/audit-distributed-tx`; it is read-only and never replays.

## Procedure

### 1. Confirm the cause fixed

- The fix is shipped: the commit, and the version the running consumer reports.
- A test reproduces the failing message class and now passes (the `/ds-fix` oracle when the cause was a `/ds-audit` finding).
- The handler's reserve is cited at `<file:line>`: which id it keys on, and that the replay path below keeps it.

If any is unclear: do not replay.

### 2. Inventory — a dry-run listing, nothing moves

List without consuming, with the identity line printed first. Per message: id (and the stable business id the consumer keys on), first-failed time, attempt count, failure reason, ordering key, attributes or headers.

| Broker | Where dead letters live | Dry-run listing (read-only) | Native redrive (step 5) |
|---|---|---|---|
| **AWS SQS** (non-Lambda source) | the DLQ named in the source's `RedrivePolicy` | `aws sqs get-queue-attributes --profile <p> --region <r> --queue-url <dlq> --attribute-names All` (depth, oldest); `aws sqs list-message-move-tasks --profile <p> --source-arn <dlq-arn>`. A `receive-message` sample hides the message for its visibility timeout and raises its receive count: sample with a short `--visibility-timeout` and do not delete | `aws sqs start-message-move-task --source-arn <dlq-arn> [--destination-arn <arn>] --max-number-of-messages-per-second <n>` — server-side; with no destination each message returns to its own source queue; rate ≤ 500/s; cancel with `CancelMessageMoveTask`. **Redriven messages are new messages: a new `MessageId` and enqueue time, and the retention period restarts.** FIFO → FIFO only; a FIFO DLQ already replaced the deduplication id with the original message id. No filtering. A DLQ fed by Lambda or SNS is not supported — use the loop |
| **BullMQ** | the queue's **failed set** (`removeOnFail` keeps it) | `queue.getJobCounts('failed')`, `queue.getFailed(0, 9)` from a read-only script against the named Redis | `job.retry('failed')` for the sample; `queue.retryJobs({ state: 'failed', count, timestamp })` for bulk (moves failed jobs back to wait; `count` limits each iteration, `timestamp` defaults to now). The job keeps its id and data |
| **Kafka** (a DLT topic, e.g. Spring's `DeadLetterPublishingRecoverer`) | `<topic>.DLT` or the project's DLQ topic — never `__consumer_offsets`, which is the group offsets store, not a DLQ | `kcat -b <bootstrap> -C -t <dlt> -o beginning -e -f '%k %o %h\n'` (key, offset, headers) | No server-side redrive: a one-off consumer reads the DLT and produces to the source topic **with the record key and headers** (the key decides the partition and per-key order) and commits its DLT offset only after the produce is acknowledged |
| **RabbitMQ** | the queue bound to the source's dead-letter exchange | `rabbitmqctl list_queues name type messages_unacknowledged consumers arguments` | A shovel (the shovel plugin) from the DLQ to the source queue, or the loop; `x-death` headers travel with the message [K?] whether a shovel keeps every property — check one sample |
| **Sidekiq** | the **Dead set** | `Sidekiq::DeadSet.new.size`, `.select { … }` in a read-only console | `Sidekiq::DeadSet.new.select { _1.display_class == '<Worker>' }.each(&:retry)` |
| **Google Pub/Sub** | the dead-letter topic's subscription (GP1) | `gcloud pubsub subscriptions pull <dlq-sub> --limit=10` **without** `--auto-ack` | Re-publish to the source topic. A publish makes a **new `message.id`** (ID7): the consumer must key on an application id attribute, carried over |
| **NATS JetStream** | no DLQ: past `MaxDeliver` the message stays in the stream and a max-deliveries advisory names its stream sequence [K?] | `nats consumer info <stream> <consumer>`; the advisory subject's messages | Re-publish the sequence's data with its `Nats-Msg-Id` header; outside the stream's 2-minute duplicate window (NA3) the same id is not deduped |
| **Redis Streams** | the pending entries list of a group (or a hand-made dead-letter stream) | `XPENDING <stream> <group>`, `XINFO GROUPS <stream>` | `XAUTOCLAIM` / `XCLAIM` hands an entry to a live consumer (same entry id — the stable id, ID6); a dead-letter stream is replayed with `XADD` to the source, carrying the original id as a field |
| **Celery** | no built-in DLQ; with RabbitMQ, the queue's DLX; otherwise the result backend's failed states | the DLX queue as above | Re-send with the task's business key in its arguments (ID8): a re-`delay()` is a new `task_id` |
| **EventBridge, SNS, Lambda event sources** | an SQS DLQ | as SQS | the loop (SQS redrive does not support SNS- or Lambda-fed DLQs) |

### 3. Categorize

Group by failure class:
- **Same root cause** — replayed together, after one sample per class.
- **Different root cause** — investigated; not replayed under this fix.
- **Bug-on-bug** — once one cause is fixed, the message may surface a second. The sample finds it.

### 4. Sample replay — always first

Move ONE message (or one job) to the target through the same path the bulk will use. Verify, against the broker and the effect store:
- The handler processed it; the effect ran **once**.
- Replaying the same sample again (or redelivering it) leaves the effect count at one — the reserve held on the id the replay path carries.
- The ordering key, attributes and headers arrived as they left.

If the sample fails: STOP. Do not bulk replay.

### 5. Bulk replay — after the sample passes

Rate-limited, through the native redrive when the table names one (it moves the messages server-side and removes them from the DLQ itself). Otherwise the **loop**, per message:

1. receive from the DLQ (a short visibility timeout);
2. send to the target **with everything the consumer and the broker need**: the body, the message attributes or headers, the stable business id, the FIFO `MessageGroupId` (and a `MessageDeduplicationId` derived from the original id, never a random one), the Kafka record key;
3. delete from the DLQ **only after the target acknowledged the send**;
4. sleep to hold the rate (start low, about 10 msg/s, and raise it while step 6 stays flat).

Per ordering key, replay in the original order, and do not replay a key while live traffic for that key is still failing.

### 6. Monitor while it runs

- Handler error rate — should not spike. If it does: STOP (cancel the move task, stop the loop).
- Processing latency p95 — should not balloon.
- DLQ depth — falling; the target's depth — draining.
- Effect counters (orders processed, emails sent) — rising by the number replayed, not more.

### 7. Verify the outcome

See § Verify (postconditions). The report is written only after it ran.

## Output format

```
## /dlq-replay — <handler / topic>

Target: <broker version · endpoint · account or cluster, from the identity read>
Path: <native redrive (<command>) | loop> · rate <msg/s>

### DLQ before
- Depth: <N> (read: <command>)  ·  Oldest: <age>
- Failure classes: <class — count>, one per line
- Stable id the consumer keys on: <field> (<file:line>) · carried by the replay path: yes / no

### Sample replay
- Message: <id> · business id <id>
- Handler outcome: success / failure · effect count after one replay <1> · after a second <1>
- Ordering key / attributes preserved: yes / no

### Bulk replay
- Started: <timestamp> · Ended: <timestamp> · Replayed: <N> · Back in the DLQ: <M>

### Verify (postconditions)
- DLQ depth:            before <N> → after <K>           (expected <N − replayed>)        PASS | FAIL | NOT RUN (<reason>)
- Duplicate effects:    <d> business ids with > 1 effect (expected 0)                       PASS | FAIL | NOT RUN (<reason>)
- Out-of-order per key: <o> keys whose effects landed out of order (expected 0)             PASS | FAIL | NOT RUN (<reason>)

### Follow-up
- <M> messages failed again — cause: <description>; ticket or ADR: <ref>
- DLQ remaining: <K> — different failure classes, listed

Report: ai/audits/dlq-replay-<handler>-<date>.md
```

## Inputs

- The named target (`--target=<broker>=<endpoint>`, `--profile=<profile>@<region>` for a cloud broker).
- The DLQ, failed set or DLT, and the target queue or topic.
- The rate limit.
- Optional filter (an attribute, a failure class, a time range) — the loop path only; SQS redrive does not filter.

## Outputs

- The replay report, with the Verify block.
- The DLQ drained or partially drained.

## Hard rules

- **Named target, identity printed.** No default profile, context or URL, ever.
- **Dry-run listing before any move.** Step 2 changes nothing.
- **Sample first.** Never bulk-replay without verifying ONE.
- **Cause confirmed fixed and deployed.**
- **The replay path keeps the stable id, the ordering key and the attributes** — or the consumer is shown keyed on an id the path does carry.
- **Rate-limited.**
- **Audit trail.** Who, when, how many, through which path, the outcome.
- **Don't replay from a backup older than retention.** Compliance and GDPR concerns if old events carry PII.

## Verify (postconditions)

Contract: [`templates/snippets/postcondition-check.md`](../../../../snippets/postcondition-check.md). Each check is observed, stated as the inverse of a failure mode below, and reported when it passes as well as when it fails; `NOT RUN` with the reason where no signal is available.

- **Depth before / after** — the DLQ (or failed set) depth read from the broker before step 4 and after step 5 differs by the number replayed, and the target's depth drained back to its baseline. Inverse of "forgot to delete" and "replayed before the fix" (messages back in the DLQ).
- **Duplicate effects by business id** — count, in the effect store, the business ids from the replayed set that carry more than one effect (`SELECT <business_id>, count(*) … WHERE <business_id> IN (<replayed ids>) GROUP BY 1 HAVING count(*) > 1`, or the provider's dashboard): expected 0. Inverse of "idempotency not enforced" and of the SQS new-`MessageId` trap. No effect store to query → `NOT RUN (no effect store readable)`.
- **Out-of-order count per key** — for each ordering key in the replayed set, the effects landed in the original order (compare the effect store's per-key version or timestamp sequence to the DLQ order): expected 0 keys out of order. Inverse of "replayed out of order" and "partition key not preserved". No ordering key in use → `NOT RUN (no per-key order required: <reason>)`.

## Failure modes

- Replayed before the fix → messages back in the DLQ; the cycle repeats.
- Idempotency not enforced, or keyed on an id the replay path changes (an SQS `MessageId`, a Pub/Sub `message.id`) → side effects duplicated.
- Bulk replay during peak → live traffic latency degrades.
- Replayed out of order → a downstream consumer sees inconsistent state.
- Partition or ordering key not preserved (Kafka key, FIFO group, Pub/Sub ordering key) → downstream order broken.
- Attributes or headers dropped by a hand loop → the consumer misroutes or rejects the message.
- Forgot to delete from the DLQ after the replay → messages re-replay forever.
- Run against the default cloud profile or kube context → the wrong account's queue.

## Related

- `add-event-handler` — produces the consumers this drains; its Phase 6 proves the reserve a replay relies on.
- `audit-distributed-tx` — the `/ds-audit --runtime` lane that counts DLQs; read-only, it never replays and never halts when this skill is absent.
- `messaging-scan` § 2–§ 3 — the code findings (unstable reserve id, poison handling) to close before a replay.
- `add-saga` — saga compensations sometimes land in a DLQ; replay them only with their own reserve.
- `ai/runbooks/dlq-recovery.md` (project-specific) — cite the project's actual DLQ procedures.

Sources (read 2026-10-14): AWS CLI reference `sqs start-message-move-task` and the SQS Developer Guide *Configure a dead-letter queue redrive* (new `MessageId` and enqueue time, retention reset, FIFO → FIFO, 500 msg/s, no SNS- or Lambda-fed DLQs); BullMQ source 6.3.15 `Queue.retryJobs`, `Job.retry`, `getJobCounts`, `getFailed`; the Sidekiq wiki *API* (`DeadSet` select and retry); `broker-semantics.md` rows ID1–ID9, GP1, NA3.

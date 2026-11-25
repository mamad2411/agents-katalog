---
name: rabbitmq-queue-and-dead-letter-troubleshooting
description: >
  Diagnoses RabbitMQ message pileup, growing queue depth, and dead-letter
  queues filling up unexpectedly, including poison-message patterns that
  make a consumer redeliver-then-fail in a loop. Use when the user reports
  "RabbitMQ queue depth keeps growing," "consumers aren't draining a
  queue," "dead-letter queue is filling up," "a message keeps getting
  redelivered and never acked," "poison message stuck reprocessing," or
  asks to troubleshoot a live RabbitMQ backlog/DLQ incident.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: messaging-and-data-orchestration
  maturity: stable
---

# RabbitMQ Queue and Dead-Letter Troubleshooting

## Purpose

A RabbitMQ queue with climbing depth, a dead-letter queue (DLQ) filling up
faster than anyone is watching it, or a single poison message that gets
redelivered forever without ever being acknowledged are three of the most
common live RabbitMQ incidents, and they usually share a small set of root
causes: a stalled or crashed consumer, a message that a consumer can never
successfully process, or a dead-letter policy that exists but routes
nowhere useful. This skill is the diagnostic playbook for isolating which
of those is actually happening and fixing it safely, building on the
topology and validation decisions covered in
[rabbitmq-configuration](../rabbitmq-configuration/SKILL.md) and
[rabbitmq-configuration-validation](../rabbitmq-configuration-validation/SKILL.md)
rather than re-deriving them.

## When to use

- A queue's `messages_ready`/`messages_unacked` count is growing steadily
  instead of draining.
- A dead-letter queue is accumulating messages faster than expected, or a
  DLQ that's supposed to be empty in steady state is not.
- A specific message appears to be redelivered repeatedly (`redelivered`
  flag set, delivery count climbing) without ever being successfully
  acked — a poison message.
- Consumers report themselves healthy (process running, connected) but the
  queue they're bound to isn't draining.
- Investigating a paging alert tied to queue depth, DLQ depth, or the
  broker's memory/disk watermark being pushed by an unconsumed backlog.

## Prerequisites & environment

- Read access to the broker's management HTTP API or `rabbitmqctl`/
  `rabbitmq-diagnostics` for queue and consumer state.
- The management plugin enabled
  (`rabbitmq-plugins enable rabbitmq_management`) for per-queue message
  rate graphs and the "get messages" inspection endpoint used in this
  skill's steps.
- Knowledge of the intended dead-letter topology (which exchange/queue a
  rejected message should land in) — established in
  [rabbitmq-configuration](../rabbitmq-configuration/SKILL.md) and checked
  in [rabbitmq-configuration-validation](../rabbitmq-configuration-validation/SKILL.md).
- Access to consumer application logs/metrics, since a queue-level view
  alone can show *that* messages aren't draining but not *why* the
  consumer can't process them.
- RabbitMQ 3.8+ if the target queues are quorum queues (delivery-count
  based poison-message handling via `x-delivery-limit` is a quorum-queue
  feature, not available on classic queues).

## Step-by-step guidance

1. **Quantify queue depth and its trend, and split ready vs. unacked**,
   since they point at different problems:
   ```bash
   rabbitmqctl list_queues name messages_ready messages_unacked consumers
   ```
   - High `messages_ready`, low/zero `consumers`: no consumer is attached
     at all — this is a consumer deployment/connectivity problem, not a
     processing problem.
   - High `messages_unacked`, consumers present: messages have been
     delivered but never acked — likely a consumer stuck mid-processing,
     a crashed consumer that never nacked/acked before disconnecting, or a
     prefetch count so high that one slow consumer is holding a large
     batch unacked.
   - `messages_ready` growing steadily with active consumers and low
     unacked: consumers are draining slower than the publish rate — a
     genuine throughput problem, not a stuck consumer.

2. **Check consumer prefetch (`basic_qos`) and acknowledgment mode** before
   assuming the consumer code itself is slow:
   ```python
   channel.basic_qos(prefetch_count=20)  # cap in-flight unacked messages per consumer
   channel.basic_consume(queue="orders.fulfillment", on_message_callback=handle, auto_ack=False)
   ```
   `auto_ack=True` (or no manual ack) means RabbitMQ marks a message
   delivered the instant it's handed to the consumer, before the consumer
   has actually processed it — a consumer that crashes mid-processing
   silently loses that message with no redelivery, which looks like
   "messages just disappear" rather than a pileup. An unbounded (or
   default `prefetch_count=0`, meaning unlimited) prefetch on a slow
   consumer means one connection can hold an enormous number of messages
   unacked, starving other consumers on the same queue of any work.

3. **Inspect actual message content for a suspected poison message**,
   using peek mode so the inspection itself doesn't consume/ack it:
   ```bash
   curl -u <RABBITMQ_USER>:<RABBITMQ_PASSWORD> \
     -X POST http://rabbitmq:15672/api/queues/orders-service/orders.fulfillment/get \
     -d '{"count":5,"ackmode":"peek","encoding":"auto"}'
   ```
   Check the message's `redelivered` flag and, for quorum queues, the
   `x-delivery-count` header — a message with a high delivery count that
   never successfully processes is the signature of a poison message: the
   consumer nacks/requeues it (or crashes after partial processing) on
   every attempt, and without a delivery-count limit it cycles forever,
   consuming consumer capacity and blocking every message queued behind it
   if the consumer processes in strict order.

4. **Cap redelivery attempts with `x-delivery-limit` (quorum queues) so a
   poison message dead-letters instead of looping forever**:
   ```bash
   rabbitmqadmin declare policy name=orders-fulfillment-delivery-limit \
     pattern="^orders\.fulfillment\." apply-to=queues \
     definition='{"delivery-limit":5,"dead-letter-exchange":"orders.dlx","dead-letter-routing-key":"orders.fulfillment.dead"}'
   ```
   Once a message has been delivered and requeued `delivery-limit` times
   without a successful ack, RabbitMQ dead-letters it automatically
   instead of redelivering indefinitely. Classic queues have no built-in
   delivery-count limit — for classic queues, the consumer itself must
   track attempt count (e.g. in a message header it increments and
   checks) and explicitly reject-without-requeue past a threshold.

5. **Confirm the dead-letter chain actually terminates in a queue someone
   monitors**, not just that a DLX is configured:
   ```bash
   rabbitmqctl list_bindings source_name destination_name routing_key
   ```
   A dead-letter exchange with no binding silently drops rejected messages
   — nothing shows up anywhere, which is easy to mistake for "no poison
   messages" when actually the evidence is being discarded. Confirm the
   full chain (policy → DLX → binding → DLQ) resolves to a real queue, and
   that the DLQ has an alert on non-zero depth, not just that it exists.

6. **For a DLQ that's filling up unexpectedly, treat it as a symptom to
   triage, not a place to silently drain.** Pull a sample of dead-lettered
   messages and their `x-death` header, which records why and from where
   each message was dead-lettered:
   ```bash
   curl -u <RABBITMQ_USER>:<RABBITMQ_PASSWORD> \
     -X POST http://rabbitmq:15672/api/queues/orders-service/orders.fulfillment.dead/get \
     -d '{"count":10,"ackmode":"peek","encoding":"auto"}'
   ```
   The `x-death` array's `reason` (`rejected`, `expired`, `maxlen`) and
   `queue` fields tell you whether messages are landing here from an
   application-level rejection (a real processing bug or bad data),
   TTL expiry (consumers falling behind badly enough that messages age
   out), or `maxlen` overflow (queue length limit hit, from
   [rabbitmq-configuration-validation](../rabbitmq-configuration-validation/SKILL.md)) —
   each has a different fix, and treating all DLQ growth as "just replay
   it" without understanding the reason risks replaying the same poison
   message back into the same failure loop.

7. **Replay dead-lettered messages deliberately, never as a bulk blind
   requeue**, once the underlying cause is fixed:
   ```bash
   # shovel a fixed number of messages from the DLQ back to the original
   # queue, only after confirming the root cause is actually fixed
   rabbitmqadmin -V orders-service get queue=orders.fulfillment.dead \
     count=1 ackmode=ack_requeue_false requeue=false
   ```
   Replaying before the root cause is fixed just re-poisons the original
   queue with the same message, restarting the redelivery loop. Replay in
   small batches and watch consumer error rates after each batch, rather
   than requeueing the entire DLQ at once.

## Best practices

- Always use manual acknowledgment (`auto_ack=False`) with an explicit,
  bounded `prefetch_count` for any consumer where message loss or one slow
  message starving others is a real concern — never leave prefetch
  unbounded "to maximize throughput."
- Set `x-delivery-limit` on quorum queues (or an equivalent
  application-level attempt counter on classic queues) so a poison message
  dead-letters after a bounded number of attempts instead of looping
  forever.
- Monitor dead-letter queue depth with the same seriousness as the
  primary queue's depth — a silently growing DLQ is a real, ongoing data
  problem, not a safe place for rejected messages to sit unexamined.
- Inspect the `x-death` header before replaying anything out of a DLQ —
  replaying a message whose root cause isn't fixed just re-poisons the
  original queue.
- Alert on `messages_unacked` staying non-zero and flat (not draining)
  for longer than a consumer's expected processing time — a consumer that
  received a message and never acked or nacked it is effectively stuck,
  and this pattern is invisible if you only watch `messages_ready`.
- Never bulk-purge a queue with unprocessed messages as a way to "fix" a
  pileup — see the explicit warning in Common pitfalls below.

## Common pitfalls

- **Symptom:** Queue depth is climbing, an on-call engineer runs
  `rabbitmqctl purge_queue orders.fulfillment` to "clear the backlog" and
  stop the paging alert.
  **Fix:** **This is a destructive action and is almost never the right
  fix.** Purging discards every unprocessed message permanently — for
  orders, payments, or any business-meaningful queue, this is data loss,
  not remediation. Diagnose the actual cause first (steps 1–3 above); if
  the queue is genuinely unrecoverable-by-design (e.g. a stale cache
  invalidation queue where old messages are meaningless), purge only after
  explicit confirmation with the message's owning team, and prefer
  shoveling to a DLQ/archive first over an irreversible purge so there's a
  fallback if the decision turns out to be wrong.

- **Symptom:** A message is redelivered indefinitely — `redelivered=true`
  and a climbing `x-death`/delivery count — and consumer error logs show
  the same exception every time.
  **Fix:** This is a poison message with no delivery-count limit in place.
  Set `x-delivery-limit` (quorum queues) so it dead-letters after a bounded
  number of attempts instead of consuming consumer capacity forever, and
  separately fix (or at minimum log-and-skip) whatever consumer bug or bad
  data causes the exception, since dead-lettering the message doesn't fix
  the underlying data or code issue.

- **Symptom:** `messages_unacked` is high and flat, consumers appear
  connected and idle, and `messages_ready` isn't draining even though it
  isn't growing either.
  **Fix:** A consumer likely received messages up to its `prefetch_count`
  and then stalled (deadlock, blocked downstream call with no timeout,
  crashed without a channel close) without acking or nacking them —
  RabbitMQ has no way to know the consumer is stuck since it hasn't
  disconnected. Check the consumer's actual thread/task state, not just
  its process liveness; add processing timeouts so a hung downstream call
  triggers a nack instead of holding the message unacked indefinitely.

- **Symptom:** A dead-letter queue that's supposed to only receive genuine
  processing failures is filling up with messages whose `x-death` reason
  is `expired`, not `rejected`.
  **Fix:** This means consumers are falling behind badly enough that
  messages are hitting their TTL before ever being consumed — a
  throughput/lag problem, not a poison-message problem. Treat it the same
  as a growing `messages_ready` count (step 1) and diagnose consumer
  throughput, not the DLQ itself; replaying these messages without fixing
  consumer throughput just re-expires them again.

- **Symptom:** Replaying a batch of dead-lettered messages back to the
  original queue immediately re-fills the DLQ with the same messages.
  **Fix:** The root cause (a specific bad payload shape, a downstream
  dependency that's still down, a bug in the consumer) wasn't actually
  fixed before replay. Inspect a sample of the DLQ's `x-death` reason and
  message body first, confirm the fix addresses that specific cause, and
  replay a small batch before replaying the rest — a full-DLQ blind replay
  is effectively re-running the same incident.

## Worked example

**Scenario:** The `orders.fulfillment.us-east` quorum queue (from
[rabbitmq-configuration](../rabbitmq-configuration/SKILL.md)'s worked
example) pages on-call for "queue depth growing," and its dead-letter
queue `orders.fulfillment.dead` is also non-empty, which is unusual.

Step 1 — quantify:
```bash
$ rabbitmqctl list_queues name messages_ready messages_unacked consumers -p orders-service
orders.fulfillment.us-east   1  340   3
orders.fulfillment.dead      0  0     0   82
```
`messages_unacked` is high (340) while `messages_ready` is nearly zero and
consumers are present — this points at stuck-in-flight messages, not a
missing consumer or a slow-drain throughput problem. The DLQ already holds
82 messages accumulated before this alert fired.

Step 2 — check prefetch and inspect the stuck messages:
```bash
$ curl -u ops-viewer:<REDACTED> -X POST \
  http://rabbitmq:15672/api/queues/orders-service/orders.fulfillment.us-east/get \
  -d '{"count":5,"ackmode":"peek","encoding":"auto"}'
```
Sampled messages show `redelivered: true` with an `x-delivery-count` of 4
on several, all with the same `order_id` prefix pattern (a specific
customer's payload shape). Consumer logs show a `KeyError` on a field the
new promotions feature expects but this customer's older client version
never sends.

Step 3 — check the DLQ's `x-death` reason on the already-dead-lettered 82
messages:
```bash
$ curl -u ops-viewer:<REDACTED> -X POST \
  http://rabbitmq:15672/api/queues/orders-service/orders.fulfillment.dead/get \
  -d '{"count":5,"ackmode":"peek","encoding":"auto"}'
```
`x-death[0].reason` is `rejected`, confirming these are genuine
application-level failures (matching the same `KeyError`), not TTL expiry
or length-limit overflow — this is a poison-message pattern, not a
throughput problem.

Root cause: the same schema-evolution discipline described in
[kafka-schema-registry-and-compatibility-management](../kafka-schema-registry-and-compatibility-management/SKILL.md)
was never applied here — this producer's payload isn't
schema-validated before publish, and the consumer assumes a field is
always present that isn't. Immediate mitigation: patch
the consumer to treat the missing field as optional (matching how the
Kafka-side schema guidance would have caught this at registration time),
deploy, then verify no new `rejected` dead-letters accumulate. Because a
`delivery-limit` of 5 was already set on this queue's policy
(per [rabbitmq-configuration-validation](../rabbitmq-configuration-validation/SKILL.md)),
the poison messages stopped looping after their fourth/fifth attempt
instead of blocking the queue indefinitely — after the consumer fix ships,
the 82 dead-lettered messages are replayed in batches of 10, confirming
each batch processes cleanly before replaying the next, rather than
requeueing all 82 at once.

## Cross-references

- [rabbitmq-configuration](../rabbitmq-configuration/SKILL.md) — the exchange/queue/dead-letter topology this skill diagnoses problems within.
- [rabbitmq-configuration-validation](../rabbitmq-configuration-validation/SKILL.md) — the pre-production checks (length limits, dead-letter chain wiring) that prevent many of the pileups diagnosed here.
- [kafka-consumer-lag-and-partition-troubleshooting](../kafka-consumer-lag-and-partition-troubleshooting/SKILL.md) — the equivalent diagnostic playbook for Kafka consumer-side pileup, useful when a system uses both brokers.
- [nats-and-pulsar-lightweight-messaging-configuration](../nats-and-pulsar-lightweight-messaging-configuration/SKILL.md) — comparable redelivery/dead-letter concepts (JetStream max-deliver, Pulsar DLQ policy) if part of the estate is on a lighter-weight broker instead.

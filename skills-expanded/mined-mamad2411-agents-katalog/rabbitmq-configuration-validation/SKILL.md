---
name: rabbitmq-configuration-validation
description: >
  Validates RabbitMQ queue durability, mirroring/quorum configuration,
  and resource limits before production use. Use when the user asks to
  "review a RabbitMQ queue config before deploying," "check queue
  durability settings," "validate quorum/mirroring config," "audit
  RabbitMQ for production readiness," or as a pre-go-live gate for a new
  RabbitMQ topology.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: messaging-and-data-orchestration
  maturity: stable
---

# RabbitMQ Configuration Validation

## Purpose

A RabbitMQ queue declared without `durable=true`, without a queue type
argument, or without any length/TTL bound will accept traffic happily in
staging and only reveal the gap in production — as messages lost on a
routine broker restart, a queue that isn't actually mirrored/replicated
the way an on-call engineer assumes during an incident, or an unbounded
queue that eventually pushes the whole broker over its memory watermark.
This skill is a concrete pre-production checklist for catching those gaps
before go-live, building on the topology decisions made in
[rabbitmq-configuration](../rabbitmq-configuration/SKILL.md) rather than
re-deriving them.

## When to use

- Before promoting a newly declared queue/exchange topology from staging
  to production.
- Reviewing a pull request or infra-as-code change that declares or
  alters RabbitMQ queues, exchanges, or vhost permissions.
- Auditing an existing RabbitMQ deployment for durability or
  high-availability gaps against an organizational baseline.
- As a gate in a CI/CD pipeline that provisions RabbitMQ topology via a
  definitions JSON import, Terraform, or a custom provisioning script.
- Confirming a queue advertised as "highly available" actually has the
  replica count/quorum settings needed to back that claim.

## Prerequisites & environment

- Read access to the target broker's topology via the management HTTP
  API or `rabbitmqctl`/`rabbitmq-diagnostics`.
- A documented organizational baseline for production readiness (minimum
  queue durability, required queue type for HA, required length/TTL
  bounds, dead-letter policy requirement) — this skill validates
  *against* such a baseline, established alongside the design guidance in
  [rabbitmq-configuration](../rabbitmq-configuration/SKILL.md).
- RabbitMQ 3.8+ if quorum queues are part of the baseline (see
  version-dependency note in
  [rabbitmq-configuration](../rabbitmq-configuration/SKILL.md)).
- Visibility into publisher code (or at least its `BasicProperties`/
  message-publishing configuration) to validate message persistence, not
  just queue-level durability, since the two are independent.

## Step-by-step guidance

1. **Pull the actual declared queue arguments, not just the intended
   design** — a queue can be re-declared with different arguments by
   mistake if a name collides with an existing queue of a different
   type:
   ```bash
   rabbitmqadmin list queues name durable type arguments
   ```
   Confirm `durable` is `true` and `type` (or the `x-queue-type`
   argument) matches what was intended for every production queue —
   RabbitMQ silently ignores a re-declaration attempt with different
   arguments against an existing queue rather than erroring in a way
   every client library surfaces clearly, so a queue actually running
   `classic` when the design called for `quorum` can go unnoticed without
   this direct check.

2. **Validate every HA-designated queue actually has more than one
   replica**, not just the queue type set correctly:
   ```bash
   rabbitmq-diagnostics check_running
   rabbitmqctl list_queues name type leader members
   ```
   A quorum queue with `members` showing only a single node provides no
   real failure tolerance despite being declared `type=quorum` — this
   happens when `x-quorum-initial-group-size` was omitted or set to 1,
   or when the cluster itself only has one reachable node at
   declaration time. Validation must check the *actual* replica count,
   not just the queue-type label.

3. **Validate message persistence on the publisher side for any queue
   marked durable**, since queue durability alone is not sufficient (see
   the pitfall in
   [rabbitmq-configuration](../rabbitmq-configuration/SKILL.md)):
   ```bash
   # inspect a sample of in-flight messages via the management API
   curl -u <RABBITMQ_USER>:<RABBITMQ_PASSWORD> \
     -X POST http://rabbitmq:15672/api/queues/orders-service/orders.fulfillment.us-east/get \
     -d '{"count":5,"ackmode":"peek","encoding":"auto"}'
   ```
   Confirm `properties.delivery_mode` is `2` (persistent) on sampled
   messages for any queue where restart-survival matters; a durable
   queue full of `delivery_mode: 1` messages is a validation failure,
   not a pass.

4. **Validate every production queue has a bounded length or TTL, and an
   explicit overflow/dead-letter policy**, rather than being left
   unbounded by omission:
   ```bash
   rabbitmqadmin declare policy name=orders-fulfillment-limits \
     pattern="^orders\.fulfillment\." apply-to=queues \
     definition='{"max-length":100000,"overflow":"reject-publish","message-ttl":86400000}'
   ```
   An unbounded queue is a latent incident: it will eventually either
   exhaust broker memory/disk (tripping the cluster-wide watermark
   described in
   [rabbitmq-configuration](../rabbitmq-configuration/SKILL.md)) or grow
   large enough that consumer catch-up becomes impractical. Validation
   should flag any production queue with no `max-length`,
   `max-length-bytes`, or `message-ttl` policy applied.

5. **Validate a dead-letter exchange is configured for any queue where
   poison messages are plausible**, rather than discovering the absence
   during an incident:
   ```bash
   rabbitmqadmin declare policy name=orders-fulfillment-dlx \
     pattern="^orders\.fulfillment\." apply-to=queues \
     definition='{"dead-letter-exchange":"orders.dlx","dead-letter-routing-key":"orders.fulfillment.dead"}'
   ```
   Confirm the referenced dead-letter exchange (`orders.dlx`) and its
   bound queue actually exist — a policy referencing a non-existent
   dead-letter exchange fails silently: rejected messages are simply
   dropped rather than routed anywhere, which validation must catch by
   checking both sides of the reference, not just the policy's presence.
   Diagnosing dead-letter queues that are filling up unexpectedly is
   covered in
   [rabbitmq-queue-and-dead-letter-troubleshooting](../rabbitmq-queue-and-dead-letter-troubleshooting/SKILL.md).

6. **Validate vhost permission scoping is least-privilege**, not a
   blanket grant:
   ```bash
   rabbitmqctl list_permissions -p orders-service
   ```
   Flag any user whose configure/write/read permission regex is `.*`
   (unrestricted) rather than scoped to the application's actual naming
   prefix — a validation pass should require permission patterns scoped
   to the specific resource-naming convention, matching the isolation
   guidance in
   [rabbitmq-configuration](../rabbitmq-configuration/SKILL.md).

7. **If topology is provisioned via a definitions JSON import or
   Terraform, diff the plan against the current broker state as an
   explicit CI gate**:
   ```bash
   rabbitmqadmin export /tmp/current-definitions.json
   diff <(jq -S . /tmp/current-definitions.json) <(jq -S . proposed-definitions.json)
   ```
   A diff showing a queue's `durable` flipping from `true` to `false`,
   or a `queue-type` argument disappearing, should block the apply until
   reconciled — these are exactly the changes most likely to be an
   accidental regression rather than an intended change.

## Best practices

- Encode the production baseline (required durability, required queue
  type for HA-designated queues, required length/TTL bound, required
  dead-letter policy) as an automated check (a script against the
  management API, or an OPA/Conftest policy over exported definitions
  JSON) rather than a manual checklist re-read each time.
- Validate the *actual* replica count for HA queues, not just the
  `queue-type` label — a quorum queue with one member is not actually
  highly available.
- Validate publisher-side message persistence alongside queue
  durability; they are independent settings and both need checking.
- Require every production queue to have an explicit length/TTL bound
  and a dead-letter exchange, treating an unbounded queue as a finding,
  not a neutral default.
- Re-run validation after any policy change (length limits, dead-letter
  routing, HA parameters) — policies can be altered independently of the
  queue declaration itself and drift silently otherwise.

## Common pitfalls

- **Symptom:** A queue policy references a dead-letter exchange that
  validation confirms is declared, but rejected messages still
  disappear rather than landing in the expected dead-letter queue.
  **Fix:** Check that the dead-letter exchange has an actual binding to
  a queue with a routing key matching `dead-letter-routing-key` (or the
  original message's routing key, if unset) — a dead-letter exchange
  that exists but has no matching binding silently drops the message,
  the same way an unbound regular exchange would. Validation must check
  the full chain (policy → exchange → binding → queue), not just that
  the exchange name resolves.

- **Symptom:** A queue intended as highly available is declared with
  `x-queue-type: quorum` and passes a validation check that only greps
  for the queue-type argument, but during an incident it turns out the
  queue has a single member and goes fully unavailable when its one node
  restarts.
  **Fix:** Validation that checks only for the presence of
  `x-queue-type: quorum` without checking `list_queues ... members` gives
  a false pass. Always validate the actual current replica count against
  the cluster's node count, not just the declared type.

- **Symptom:** A durable queue with persistent messages still loses data
  on a *planned* maintenance restart of the whole cluster (not a single
  node).
  **Fix:** Durability and persistence protect against individual broker
  restarts assuming at least one replica survives — a full-cluster
  restart taken all at once, without a rolling/staggered approach, can
  still cause quorum queues to lose availability mid-restart if the
  restart brings down a majority of a queue's replicas simultaneously.
  Validate that any planned full-cluster maintenance uses a rolling
  restart, one node at a time, confirming quorum-queue leaders have
  failed over cleanly between each node's restart.

- **Symptom:** An "unbounded" queue with no `max-length` policy validated
  as acceptable months ago now holds tens of millions of messages after
  a long-running consumer outage, and the broker's disk watermark trips,
  blocking publishing cluster-wide.
  **Fix:** This is exactly what the length/TTL-bound validation step is
  meant to catch — re-run validation periodically (not just at initial
  rollout) against queues that may have been created or had policies
  changed since the last audit, and treat any unbounded production queue
  discovered later as a finding requiring the same remediation as if
  caught at go-live.

## Worked example

**Scenario:** A pre-production review of the `orders.fulfillment.us-east`
quorum queue (declared in
[rabbitmq-configuration](../rabbitmq-configuration/SKILL.md)'s worked
example) before it goes live.

Queue state pulled for review:
```bash
$ rabbitmqctl list_queues name type leader members -p orders-service
orders.fulfillment.us-east  quorum  rabbit@rmq-node-1  [rabbit@rmq-node-1,rabbit@rmq-node-2,rabbit@rmq-node-3]
```
Replica count check passes: 3 members across the cluster's 3 nodes,
matching the design's `x-quorum-initial-group-size: 3`.

Length/TTL and dead-letter policy check:
```bash
$ rabbitmqctl list_policies -p orders-service
vhost            name                          pattern                     definition
orders-service   orders-fulfillment-limits     ^orders\.fulfillment\.      {"max-length":100000,"overflow":"reject-publish"}
```
This fails validation: a `max-length` is set, but no `message-ttl` or
dead-letter-exchange policy is present — messages hitting the length
limit are rejected outright (`reject-publish`) rather than routed
anywhere for inspection, meaning a backlog spike silently drops orders
instead of surfacing them. Review requests adding a dead-letter policy
before sign-off:
```bash
rabbitmqadmin declare policy name=orders-fulfillment-dlx \
  pattern="^orders\.fulfillment\." apply-to=queues \
  definition='{"dead-letter-exchange":"orders.dlx","dead-letter-routing-key":"orders.fulfillment.dead","max-length":100000}'

rabbitmqadmin declare exchange name=orders.dlx type=fanout durable=true
rabbitmqadmin declare queue name=orders.fulfillment.dead durable=true
rabbitmqadmin declare binding source=orders.dlx destination=orders.fulfillment.dead
```
Publisher persistence check via the management API confirms sampled
messages carry `delivery_mode: 2`. With the dead-letter chain added and
verified end-to-end (policy → exchange → binding → queue), the topology
passes validation and is approved for production traffic.

## Cross-references

- [rabbitmq-configuration](../rabbitmq-configuration/SKILL.md) — the topology and cluster design decisions this skill validates against a production baseline.
- [rabbitmq-queue-and-dead-letter-troubleshooting](../rabbitmq-queue-and-dead-letter-troubleshooting/SKILL.md) — diagnosing dead-letter/pileup issues that this validation aims to prevent but which can still surface post-launch.
- [nats-and-pulsar-lightweight-messaging-configuration](../nats-and-pulsar-lightweight-messaging-configuration/SKILL.md) — comparable durability/replication validation concerns if a lighter-weight broker is used instead.

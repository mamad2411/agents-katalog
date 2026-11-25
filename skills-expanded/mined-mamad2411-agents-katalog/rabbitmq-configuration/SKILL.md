---
name: rabbitmq-configuration
description: >
  Designs RabbitMQ exchange/queue/binding topology, virtual host
  separation, and clustering for high availability. Use when the user
  asks to "design a RabbitMQ exchange," "set up queue bindings," "create a
  virtual host," "cluster RabbitMQ nodes," "choose exchange type," or set
  up a new RabbitMQ deployment from scratch.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: messaging-and-data-orchestration
  maturity: stable
---

# RabbitMQ Configuration

## Purpose

RabbitMQ's routing model — exchanges, queues, and the bindings between
them — is where most of the design decisions that determine correctness
and operability actually happen, more so than broker-level tuning.
Choosing the wrong exchange type, skipping virtual host separation
between unrelated applications, or clustering nodes without a clear
quorum/mirroring strategy all produce problems that are hard to retrofit
once producers and consumers are already built against the topology.
This skill covers designing that topology and cluster deliberately —
validating it before production rollout is covered separately in
[rabbitmq-configuration-validation](../rabbitmq-configuration-validation/SKILL.md).

## When to use

- Designing a new RabbitMQ exchange/queue/binding topology for a service
  or set of services.
- Choosing between direct, topic, fanout, and headers exchange types for
  a specific routing need.
- Setting up virtual host (`vhost`) separation between unrelated teams or
  applications sharing a broker.
- Standing up a RabbitMQ cluster and deciding between classic mirrored
  queues and quorum queues for high availability.
- Reviewing an existing RabbitMQ deployment's topology for missing
  isolation (shared vhost across unrelated apps) or a high-availability
  gap (non-replicated queues in a cluster).

## Prerequisites & environment

- RabbitMQ 3.8+ for quorum queues (the recommended HA queue type since
  their introduction); classic mirrored queues are older and being
  phased toward deprecation in newer major versions — check the target
  RabbitMQ version's release notes before choosing between them for a
  new deployment.
- At least 3 nodes for any cluster relying on quorum queues, since
  quorum queues use Raft consensus and need a majority to elect a leader
  and accept writes.
- The `rabbitmqctl`/`rabbitmq-diagnostics` CLI (or the management HTTP
  API) available for cluster and topology administration.
- The management plugin enabled
  (`rabbitmq-plugins enable rabbitmq_management`) for visibility into
  exchange/queue/binding state and cluster health during setup.
- A clear list of which applications/teams will share this broker, to
  drive the virtual host isolation plan up front.

## Step-by-step guidance

1. **Choose the exchange type based on the actual routing need, not
   habit.** Direct exchanges route on an exact routing key match; topic
   exchanges route on wildcard patterns; fanout exchanges broadcast to
   every bound queue ignoring the routing key; headers exchanges route on
   message header attributes instead of the routing key:
   ```bash
   rabbitmqadmin declare exchange name=orders.topic type=topic durable=true
   rabbitmqadmin declare exchange name=orders.broadcast type=fanout durable=true
   ```
   Use `topic` for anything needing pattern-based routing (e.g.
   `orders.created.us-east` routed to a queue bound with
   `orders.created.*`), `fanout` for broadcast-to-all-subscribers
   patterns (e.g. cache invalidation events), and `direct` only when
   routing keys are exact and finite (e.g. routing to one of a small,
   fixed set of worker queues).

2. **Declare durable queues bound with specific routing patterns**,
   naming both the exchange and the binding intentionally so the
   topology is self-documenting:
   ```bash
   rabbitmqadmin declare queue name=orders.fulfillment durable=true \
     arguments='{"x-queue-type":"quorum"}'
   rabbitmqadmin declare binding source=orders.topic destination=orders.fulfillment \
     routing_key="orders.created.*"
   ```
   `durable=true` on both the exchange and queue ensures the topology
   itself survives a broker restart — it does *not* by itself make
   individual messages survive a restart; that also requires messages to
   be published as persistent (see step 3).

3. **Publish messages as persistent for anything that must survive a
   broker restart**, since queue durability and message persistence are
   separate settings:
   ```python
   channel.basic_publish(
       exchange="orders.topic",
       routing_key="orders.created.us-east",
       body=message_body,
       properties=pika.BasicProperties(delivery_mode=2),  # 2 = persistent
   )
   ```
   A durable queue holding non-persistent (`delivery_mode=1` or unset)
   messages still loses those in-flight/unconsumed messages on a broker
   restart — durability of the queue and persistence of its messages must
   both be set for restart-survival.

4. **Separate unrelated applications into distinct virtual hosts**, each
   with its own access-scoped user, rather than sharing one vhost/
   namespace across teams:
   ```bash
   rabbitmqctl add_vhost orders-service
   rabbitmqctl add_vhost notifications-service
   rabbitmqctl set_permissions -p orders-service orders-app \
     "^orders\." "^orders\." "^orders\."
   ```
   The three permission patterns (configure, write, read) scoped to a
   `^orders\.` prefix mean the `orders-app` user can only declare, write
   to, and read from resources matching that naming convention within
   its own vhost — a compromised or buggy `orders-app` credential can't
   touch `notifications-service`'s vhost at all, since vhosts are a hard
   isolation boundary in RabbitMQ, not just a naming convention.

5. **Choose quorum queues over classic mirrored queues for new
   high-availability queues.** Quorum queues use Raft consensus for
   leader election and replication, giving more predictable failure
   behavior than classic mirroring's older synchronization model:
   ```bash
   rabbitmqadmin declare queue name=orders.fulfillment durable=true \
     arguments='{"x-queue-type":"quorum","x-quorum-initial-group-size":3}'
   ```
   `x-quorum-initial-group-size` sets how many cluster nodes hold a
   replica of this queue from creation — 3 is the common baseline,
   matching the cluster's controller-node count, so the queue can
   tolerate one node failure and still have a majority to elect a new
   leader.

6. **Cluster nodes and confirm the cluster's expected node count for
   quorum before relying on it for HA**:
   ```bash
   rabbitmqctl join_cluster rabbit@rmq-node-2
   rabbitmqctl cluster_status
   ```
   A 2-node cluster cannot achieve Raft majority if either node is down
   — quorum queues need at least 3 nodes to tolerate any single-node
   failure while remaining writable. Deploying quorum queues onto a
   2-node cluster provides no real HA benefit over a single node for
   availability during a failure, only for data redundancy.

7. **Set resource limits (memory/disk watermarks) deliberately** rather
   than leaving broker-wide defaults unexamined, since RabbitMQ blocks
   publishers cluster-wide when a watermark is breached:
   ```ini
   # rabbitmq.conf
   vm_memory_high_watermark.relative = 0.6
   disk_free_limit.absolute = 5GB
   ```
   These are cluster-wide circuit breakers, not per-queue limits — a
   single misbehaving queue accumulating unconsumed messages can push
   the whole broker over the watermark and block publishing for every
   other queue on the same node, which is a strong argument for also
   setting per-queue length limits (see
   [rabbitmq-configuration-validation](../rabbitmq-configuration-validation/SKILL.md)).

## Best practices

- Default new HA queues to `x-queue-type: quorum` rather than classic
  mirrored queues for any new deployment on a supported RabbitMQ version.
- Give every application/team its own virtual host with scoped
  permissions — never share one vhost across unrelated applications "to
  keep things simple."
- Use `topic` exchanges with a clear, hierarchical routing-key naming
  convention (e.g. `<domain>.<event>.<region>`) rather than `direct`
  exchanges with an ever-growing flat list of exact routing keys.
- Set `delivery_mode=2` (persistent) as the default for any message whose
  loss on broker restart would be a real problem, and treat non-persistent
  publishing as an explicit, deliberate choice for genuinely disposable
  data (e.g. ephemeral metrics), not a default left unset by omission.
- Run at least 3 cluster nodes for any deployment relying on quorum
  queues for HA — fewer nodes means no real majority-based failure
  tolerance.
- Keep exchange/queue/binding declarations as code (a declarative
  definitions JSON export, or a provisioning tool/Terraform provider)
  rather than only imperative `rabbitmqadmin`/console clicks that can't
  be diffed in review.

## Common pitfalls

- **Symptom:** A message published to a durable queue is lost after a
  broker restart, even though the queue itself still exists afterward.
  **Fix:** Queue durability and message persistence are independent
  settings — check whether the publisher set `delivery_mode=2`
  (persistent). A durable queue with non-persistent messages loses any
  message that was only in memory (not yet written to disk) at restart
  time; fix the publisher's message properties, not the queue
  declaration.

- **Symptom:** A quorum queue deployed for HA still becomes unavailable
  (no leader can be elected) when a single node goes down.
  **Fix:** Check the cluster's actual node count and the queue's
  `x-quorum-initial-group-size` — quorum queues need a majority of their
  replica set alive to elect a leader. A 2-node cluster, or a
  3-node cluster where the queue was created with a replica group size
  of 1, has no real failure tolerance. Re-create (or grow) the queue's
  replica set to span at least 3 nodes.

- **Symptom:** A buggy consumer on one queue causes publishing to *every*
  queue on the broker to block, not just the affected queue.
  **Fix:** This is the cluster-wide memory or disk watermark being
  breached by one queue's unconsumed backlog — RabbitMQ's flow control
  blocks publishers broker-wide (or per-node), not per-queue, once a
  watermark trips. Set a per-queue `x-max-length` or `x-max-length-bytes`
  limit (with an appropriate overflow behavior — see
  [rabbitmq-configuration-validation](../rabbitmq-configuration-validation/SKILL.md))
  so one queue's backlog can't consume unbounded broker memory/disk in
  the first place, in addition to fixing the underlying consumer issue
  (see
  [rabbitmq-queue-and-dead-letter-troubleshooting](../rabbitmq-queue-and-dead-letter-troubleshooting/SKILL.md)).

- **Symptom:** Two unrelated teams' applications, sharing a single
  default vhost, start colliding — one team's queue-purge maintenance
  script accidentally matches and purges the other team's queue because
  both used similar naming.
  **Fix:** This is a direct consequence of skipping virtual host
  isolation. Separate the applications into distinct vhosts with
  permissions scoped by user, so name collisions across teams are
  structurally impossible rather than a naming-convention hope.

## Worked example

**Scenario:** A new `orders-service` needs a topic-exchange-based
routing setup with region-specific fulfillment queues, isolated from
every other team on a shared 3-node RabbitMQ cluster, with quorum queues
for HA.

Virtual host and scoped user:
```bash
rabbitmqctl add_vhost orders-service
rabbitmqctl add_user orders-app '<PLACEHOLDER_SET_VIA_SECRETS_MANAGER>'
rabbitmqctl set_permissions -p orders-service orders-app \
  "^orders\." "^orders\." "^orders\."
```

Topology declared against the `orders-service` vhost:
```bash
rabbitmqadmin -V orders-service declare exchange \
  name=orders.topic type=topic durable=true

rabbitmqadmin -V orders-service declare queue \
  name=orders.fulfillment.us-east durable=true \
  arguments='{"x-queue-type":"quorum","x-quorum-initial-group-size":3}'

rabbitmqadmin -V orders-service declare queue \
  name=orders.fulfillment.eu-west durable=true \
  arguments='{"x-queue-type":"quorum","x-quorum-initial-group-size":3}'

rabbitmqadmin -V orders-service declare binding \
  source=orders.topic destination=orders.fulfillment.us-east \
  routing_key="orders.created.us-east"

rabbitmqadmin -V orders-service declare binding \
  source=orders.topic destination=orders.fulfillment.eu-west \
  routing_key="orders.created.eu-west"
```

Publisher (persistent messages, routed by region):
```python
channel.basic_publish(
    exchange="orders.topic",
    routing_key="orders.created.us-east",
    body=order_payload,
    properties=pika.BasicProperties(delivery_mode=2, content_type="application/json"),
)
```
Because the cluster has 3 nodes and each quorum queue's initial group
size is 3, either `orders.fulfillment.us-east` or
`orders.fulfillment.eu-west` continues accepting messages and electing a
leader if any single node fails, and because the `orders-app` user's
permissions are scoped to the `^orders\.` prefix within its own
`orders-service` vhost, no other team's queues are reachable with these
credentials even if they were somehow leaked.

## Cross-references

- [rabbitmq-configuration-validation](../rabbitmq-configuration-validation/SKILL.md) — validating this topology's durability, mirroring/quorum settings before production use.
- [rabbitmq-queue-and-dead-letter-troubleshooting](../rabbitmq-queue-and-dead-letter-troubleshooting/SKILL.md) — diagnosing message pileup and poison-message issues that arise once this topology is running in production.
- [nats-and-pulsar-lightweight-messaging-configuration](../nats-and-pulsar-lightweight-messaging-configuration/SKILL.md) — a lighter-weight alternative worth considering before committing to a full RabbitMQ cluster for simpler routing needs.

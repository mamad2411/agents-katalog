---
name: knative-eventing-configuration
description: >
  Configures Knative Eventing — Brokers, Triggers, and event Sources —
  the CloudEvents-based publish/subscribe layer distinct from Knative
  Serving's request-driven model. Use when the user asks to "set up a
  Knative Broker," "add a Knative Trigger with a CloudEvents filter,"
  "wire an event Source to a Broker," "route events between Knative
  services asynchronously," or "why isn't my Knative Trigger delivering
  events."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: serverless-and-alternative-compute
  maturity: stable
---

# Knative Eventing Configuration

## Purpose

Knative Eventing is a separate component from Knative Serving —
it's a CloudEvents-native publish/subscribe layer for routing events
between producers (Sources) and consumers (Services or other sinks)
through a **Broker**, with **Triggers** declaring filtered subscriptions,
rather than the request/response, scale-to-zero model covered in
[knative-serverless-configuration](../knative-serverless-configuration/SKILL.md).
Conflating the two is a common source of confusion: a Knative `Service`
still receiving events via a Trigger scales the same way as any other
Knative Service, but the routing, filtering, retry, and dead-lettering
semantics belong entirely to Eventing, not Serving. This skill covers
Brokers, Triggers, and Sources specifically.

## When to use

- Standing up event-driven communication between services where a
  direct HTTP call would create tight coupling.
- Wiring an event Source (PingSource, ApiServerSource, a custom
  Source, or a Kafka/cloud-provider source via an Eventing extension)
  to a Broker.
- Writing or debugging a Trigger's CloudEvents attribute filter that
  isn't matching events as expected.
- Configuring retry and dead-letter handling for events that fail
  delivery to a subscriber.
- Deciding whether a given integration should be direct HTTP (Knative
  Serving-to-Serving) or routed through Eventing's Broker/Trigger model.

## Prerequisites & environment

- Knative Eventing installed on the cluster (separate installation from
  Knative Serving — a cluster can run Serving without Eventing or vice
  versa), plus a Broker implementation (the in-memory "MTChannelBased"
  broker for simple cases, or a Kafka-backed broker for durability and
  higher throughput — check which is installed with
  `kubectl get brokers.eventing.knative.dev -A -o wide` and confirm the
  backing implementation before assuming delivery guarantees).
- `kubectl` access to `brokers.eventing.knative.dev`,
  `triggers.eventing.knative.dev`, and the specific Source CRDs in use.
- Familiarity with the CloudEvents spec's core attributes (`type`,
  `source`, `subject`, `data`), since Trigger filters match on these
  attributes.
- A subscriber (Knative Service, or any addressable HTTP sink) already
  deployed and reachable before wiring a Trigger to it.

## Step-by-step guidance

1. **Create a Broker as the central event routing point** in a
   namespace, rather than wiring Sources directly to subscribers:
   ```yaml
   apiVersion: eventing.knative.dev/v1
   kind: Broker
   metadata:
     name: orders-broker
     namespace: prod
     annotations:
       eventing.knative.dev/broker.class: MTChannelBasedBroker
   ```
   Direct Source-to-sink wiring works for a single, simple integration
   but doesn't scale to multiple consumers of the same event stream —
   a Broker lets multiple Triggers subscribe to the same event flow
   independently.

2. **Wire an event Source to the Broker**, not directly to a consumer:
   ```yaml
   apiVersion: sources.knative.dev/v1
   kind: ApiServerSource
   metadata:
     name: order-pod-watcher
     namespace: prod
   spec:
     serviceAccountName: order-pod-watcher-sa
     mode: Resource
     resources:
       - apiVersion: v1
         kind: Event
     sink:
       ref:
         apiVersion: eventing.knative.dev/v1
         kind: Broker
         name: orders-broker
   ```
   For a simple recurring test/heartbeat event, `PingSource` is the
   built-in choice; for real business events, a custom Source (a small
   adapter service that receives or polls upstream events and emits
   CloudEvents to the Broker's ingress) or a maintained community Source
   (Kafka, cloud-provider event sources) is more typical.

3. **Declare Triggers with explicit CloudEvents attribute filters**, not
   a Trigger with no filter subscribing a consumer to every event on
   the Broker:
   ```yaml
   apiVersion: eventing.knative.dev/v1
   kind: Trigger
   metadata:
     name: order-created-to-fulfillment
     namespace: prod
   spec:
     broker: orders-broker
     filter:
       attributes:
         type: com.example.order.created
     subscriber:
       ref:
         apiVersion: serving.knative.dev/v1
         kind: Service
         name: fulfillment-service
   ```
   A Trigger with no `filter` (or an overly broad one) delivers every
   event on the Broker to that subscriber, which both wastes the
   subscriber's capacity and couples it to event types it was never
   designed to handle.

4. **Configure delivery retry and dead-lettering per Trigger** so a
   subscriber outage or transient failure doesn't silently drop events:
   ```yaml
   apiVersion: eventing.knative.dev/v1
   kind: Trigger
   metadata:
     name: order-created-to-fulfillment
     namespace: prod
   spec:
     broker: orders-broker
     filter:
       attributes:
         type: com.example.order.created
     subscriber:
       ref:
         apiVersion: serving.knative.dev/v1
         kind: Service
         name: fulfillment-service
     delivery:
       retry: 5
       backoffPolicy: exponential
       backoffDelay: PT0.5S
       deadLetterSink:
         ref:
           apiVersion: serving.knative.dev/v1
           kind: Service
           name: order-events-dlq-handler
   ```
   Without a `deadLetterSink`, an event that exhausts its retries is
   dropped with no record — the same silent-data-loss risk as an async
   Lambda invocation with no Dead Letter Queue configured.

5. **Use multiple attribute filters (or `filters` with `all`/`any`, on
   Eventing versions that support the newer filter expression syntax)
   to narrow subscriptions precisely**, rather than one broad Trigger
   per consumer handling unrelated event types internally with an
   if/else — check the installed Eventing version's supported filter
   syntax (`spec.filter.attributes` is the long-standing form; newer
   `spec.filters` array-based expressions add `any`/`all`/`not`/`exists`
   matching where available) before assuming the newer syntax is
   supported.

6. **Validate Broker delivery guarantees match the workload's actual
   requirement.** The in-memory channel-based Broker is simpler to
   operate but doesn't persist events beyond its backing channel's
   retention; a Kafka-backed Broker gives durable, replayable delivery
   at the cost of running and operating Kafka. Pick deliberately based
   on whether losing in-flight events during a Broker component restart
   is acceptable for this workload.

## Best practices

- Route all cross-service event flows through a Broker/Trigger, not
  direct Source-to-sink wiring, once more than one consumer might ever
  need the same event stream — retrofitting a Broker in later is more
  disruptive than starting with one.
- Write specific, narrow Trigger filters per subscriber rather than one
  broad Trigger with internal branching logic — this keeps the routing
  topology visible in the Kubernetes resources themselves, not buried
  in application code.
- Always configure `delivery.deadLetterSink` on Triggers whose events
  matter (order processing, billing, anything with a compliance or
  financial impact) — an event silently dropped after exhausting
  retries is a data-loss incident waiting to be discovered.
- Choose the Broker backend (in-memory vs. Kafka-backed) based on
  actual durability requirements, not on whichever was easiest to
  install first — migrating Broker backends later means re-wiring
  every Trigger and Source pointed at it.
- Monitor Trigger-level delivery failure metrics (most Broker
  implementations expose these) as a first-class SLO, the same as any
  other asynchronous delivery path in the system.

## Common pitfalls

- **Symptom:** A Trigger's subscriber never receives any events, even
  though the Source and Broker both show as `Ready`.
  **Fix:** The Trigger's `filter.attributes` likely doesn't match the
  actual CloudEvents attributes the Source emits (a mismatched `type`
  string is the most common cause); inspect the raw event with
  `kubectl logs` on the Broker's ingress or a debug subscriber with no
  filter, confirm the exact attribute values, then correct the
  Trigger's filter to match.

- **Symptom:** One misbehaving Source floods the Broker with events,
  and every subscriber sees degraded performance, not just the intended
  consumer.
  **Fix:** All Triggers on a shared Broker receive from the same event
  stream; add specific filters so unrelated subscribers aren't invoked
  at all for irrelevant event types, and consider a separate Broker per
  logical domain if one producer's volume is disproportionate to
  others sharing the same Broker.

- **Symptom:** Events related to a failed downstream call (subscriber
  temporarily down) simply disappear with no record after some time.
  **Fix:** No `deadLetterSink` was configured on the Trigger, so events
  that exhaust retries are dropped; add a `deadLetterSink` pointing to
  a handler (even a simple one that logs to durable storage) and
  alarm on messages arriving there.

- **Symptom:** A team assumes events sent to a Broker are durably
  persisted and can be replayed after an incident, but they're gone.
  **Fix:** The installed Broker implementation is the in-memory
  channel-based one, which doesn't guarantee durable replay across a
  channel component restart; if replay/durability is a real
  requirement, migrate to a Kafka-backed (or equivalent durable) Broker
  implementation rather than assuming all Broker classes behave the
  same.

- **Symptom:** A new Trigger is added for a new consumer, and an
  unrelated, already-working consumer starts receiving unexpected
  events too.
  **Fix:** The new Trigger's filter was left too broad (or omitted),
  causing it to match events also delivered to the existing consumer's
  own Trigger if their filters overlap unintentionally; audit all
  Triggers on the shared Broker for filter overlap, not just the newly
  added one, when diagnosing unexpected delivery.

## Worked example

**Scenario:** An `order-created` event, published by the order service
directly to a Broker as a CloudEvent, needs to reach both a fulfillment
service and a separate analytics-ingestion service, with the
fulfillment path requiring reliable delivery (retry + dead-letter) and
the analytics path tolerating occasional drops.

Broker:
```yaml
apiVersion: eventing.knative.dev/v1
kind: Broker
metadata:
  name: orders-broker
  namespace: prod
```

Trigger for fulfillment (reliable delivery):
```yaml
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: order-created-to-fulfillment
  namespace: prod
spec:
  broker: orders-broker
  filter:
    attributes:
      type: com.example.order.created
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: fulfillment-service
  delivery:
    retry: 5
    backoffPolicy: exponential
    backoffDelay: PT0.5S
    deadLetterSink:
      ref:
        apiVersion: serving.knative.dev/v1
        kind: Service
        name: order-events-dlq-handler
```

Trigger for analytics (best-effort, no dead-letter needed):
```yaml
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: order-created-to-analytics
  namespace: prod
spec:
  broker: orders-broker
  filter:
    attributes:
      type: com.example.order.created
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: analytics-ingest
  delivery:
    retry: 2
```
Both Triggers subscribe to the same `com.example.order.created` event
type on the same Broker independently — the order service publishes
once to the Broker's ingress with no knowledge of either consumer, and
each Trigger's own `delivery` policy reflects that consumer's actual
reliability requirement rather than a one-size-fits-all setting shared
across every subscriber.

## Cross-references

- [knative-serverless-configuration](../knative-serverless-configuration/SKILL.md) — the request-driven Serving model that Eventing's subscribers (typically Knative Services) run on.
- [knative-configuration-validation](../knative-configuration-validation/SKILL.md) — pre-deploy validation approach for Knative Serving config, extendable to Broker/Trigger manifests.
- [dapr-distributed-runtime-configuration](../dapr-distributed-runtime-configuration/SKILL.md) — Dapr's pub/sub building block covers similar event-routing needs via a sidecar model instead of Knative's Broker/Trigger CRDs, useful when comparing approaches for polyglot workloads.

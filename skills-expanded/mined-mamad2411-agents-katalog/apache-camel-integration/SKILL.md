---
name: apache-camel-integration
description: Apache Camel integration routes — EIPs, error handling, transactions, testing, and Camel on Spring Boot / Quarkus. Use when building or reviewing Camel routes, choosing an integration pattern, wiring dead-letter and redelivery, handling idempotency, or debugging why a route silently drops messages.
date_added: '2026-08-26'
---

# Apache Camel

Camel is a routing engine built on Enterprise Integration Patterns. Reach for it when messages move **between** systems with transformation, routing and retry in between — not as a general application framework.

## The mental model

A **route** consumes from one endpoint and produces to others. Every message is an **Exchange**: an In message (body + headers), an optional Out, a set of **properties** (route-scoped), and an exception slot.

The distinction that causes the most bugs:

| | Lives for | Survives across routes | Use for |
|---|---|---|---|
| **Header** | one message | yes, if the component propagates it | protocol/routing metadata |
| **Property** | the exchange | yes, within the exchange | route-internal state |
| **Body** | the message | yes | the payload |

Headers are dropped by many components on the way out (HTTP, JMS filter them). **Never carry business state in a header across a component boundary** — use a property, or put it in the body.

## Route style

Prefer the **Java DSL** — it is refactorable, type-checked and testable. Use XML only where an existing estate demands it.

```java
from("jms:queue:orders")
    .routeId("order-intake")                    // ALWAYS set an id
    .errorHandler(deadLetterChannel("jms:queue:orders.dlq")
        .maximumRedeliveries(3)
        .redeliveryDelay(1000)
        .backOffMultiplier(2)
        .useExponentialBackOff()
        .retryAttemptedLogLevel(LoggingLevel.WARN))
    .idempotentConsumer(header("orderId"), idempotentRepo)
    .doTry()
        .to("bean:validator")
        .choice()
            .when(simple("${body.total} > 10000")).to("direct:manual-review")
            .otherwise().to("direct:auto-approve")
        .end()
    .doCatch(ValidationException.class)
        .to("jms:queue:orders.invalid")
    .end();
```

- **`routeId` on every route.** Without it, logs, metrics and JMX show generated ids and are useless in an incident.
- **`direct:` for in-JVM synchronous handoff** (same thread, same transaction). **`seda:` only when you deliberately want a queue and a thread pool** — it breaks the transaction and loses messages on shutdown unless configured.
- Keep routes short. A route longer than a screen should delegate to `direct:` sub-routes named after what they do.

## The EIPs that carry most work

| Pattern | DSL | Use when |
|---|---|---|
| Content-based router | `.choice().when(...)` | branch on message content |
| Splitter | `.split(body())` | one message → many; add `.streaming()` for large payloads |
| Aggregator | `.aggregate(header("id"), strategy).completionSize(n)` | many → one |
| Idempotent consumer | `.idempotentConsumer(key, repo)` | at-least-once delivery, exactly-once effect |
| Wire tap | `.wireTap("direct:audit")` | fire-and-forget side channel |
| Enricher | `.enrich("direct:lookup", strategy)` | pull extra data in |
| Throttler | `.throttle(10).timePeriodMillis(1000)` | protect a downstream rate limit |

**Splitter + aggregator is the trap.** `.split()` on a large body without `.streaming()` loads everything into memory. And a split that fails partway leaves earlier sub-messages already delivered — decide explicitly whether you want `.stopOnException()` or per-item error routing.

## Error handling — the part that gets skipped

Camel has three layers and they behave differently:

1. **`errorHandler(...)`** — route-wide fallback. `deadLetterChannel` moves the failed exchange to a DLQ after redelivery is exhausted.
2. **`onException(Type.class)`** — per exception type; `.handled(true)` stops propagation and marks the exchange successful, `.handled(false)` re-throws after processing.
3. **`doTry/doCatch/doFinally`** — scoped to a block within a route.

```java
onException(TransientException.class)
    .maximumRedeliveries(5).redeliveryDelay(500).useExponentialBackOff()
    .handled(false);                            // still fails after retries — correct

onException(PermanentException.class)
    .maximumRedeliveries(0)                     // never retry what cannot succeed
    .handled(true).to("jms:queue:permanent-failures");
```

**Distinguish transient from permanent.** Retrying a validation failure five times just delays the inevitable and multiplies load. Retry timeouts and connection resets; never retry a 400.

**A DLQ nobody monitors is a silent data-loss channel.** Alert on DLQ depth, not just on route errors.

For calls to external systems, put a circuit breaker in front — Camel ships one:

```java
.circuitBreaker()
    .resilience4jConfiguration()
        .failureRateThreshold(50)
        .waitDurationInOpenState(10000)
        .slidingWindowSize(20)
    .end()
    .to("http://downstream/api")
.onFallback()
    .transform(constant("{\"status\":\"degraded\"}"))
.end();
```

See `.claude/rules/RULES.md` (## resilient-integration) — a circuit breaker is required on every external call, not optional.

## Transactions

`.transacted()` binds the route to a `PlatformTransactionManager`. It works **only** for transactional components (JMS, JDBC) on the **same thread**.

- `seda:`, `.threads()`, `.wireTap()` and `.split().parallelProcessing()` all break the transaction boundary — the new thread is outside it.
- There is no distributed transaction across JMS and HTTP. Use the **idempotent consumer** pattern plus retries instead of pretending 2PC exists.

## Testing

```java
class OrderRouteTest extends CamelTestSupport {
    @Override protected RouteBuilder createRouteBuilder() { return new OrderRoute(); }

    @Test void routesLargeOrdersToReview() throws Exception {
        getMockEndpoint("mock:manual-review").expectedMessageCount(1);
        template.sendBody("direct:start", order(20_000));
        assertMockEndpointsSatisfied();
    }
}
```

- `AdviceWith` to replace real endpoints with `mock:` without editing the route.
- Assert on **mock endpoint expectations**, not on log output.
- Test the failure paths explicitly — DLQ routing and redelivery are the parts that break in production and the parts least often tested.

## Operating it

- **Enable JMX / Micrometer** and watch per-route: inflight exchanges, failures, and mean processing time.
- `.log(LoggingLevel.INFO, "...")` with the routeId in the pattern, so a message can be traced end to end.
- Set `camel.springboot.shutdownTimeout` and use graceful shutdown, or in-flight messages are lost on deploy.
- Never log full message bodies on a route carrying personal or payment data.

## Traps

- **`simple()` expressions fail silently** when a property is missing — they evaluate to null rather than erroring. Validate early.
- **`from()` twice on the same endpoint** in different routes competes for messages rather than broadcasting. Use `direct:`/`wireTap` for fan-out.
- **`.end()` mismatches** in nested `choice`/`split` blocks compile fine and route wrongly. Keep nesting shallow.
- **Camel version matters.** Camel 3 → 4 moved packages to `jakarta.*` and dropped several components; check before copying a route from an older codebase.

---
name: spring-boot-microservices-basics
description: Apply Spring Boot microservice foundations using gateway routing, service discovery, and service boundary design. Use when decomposing systems into Spring Boot services.
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Spring Boot Microservices Basics

Design Spring Boot 3.x microservice foundations that avoid the distributed-monolith trap: business-capability boundaries, stable contracts, gateway/discovery, resilient inter-service calls (Resilience4j), event-driven async with the transactional outbox, and end-to-end observability. Start with a modular monolith (Spring Modulith) and split when signals justify it.

## Context

You are planning or implementing a microservice architecture (or cracking a monolith) using Spring Boot 3.x. Output must avoid synchronous chains, hidden coupling, and shared databases - the failure modes that turn microservices into a worse monolith.

## When to Use This Skill

- Decomposing a monolith into Spring Boot services.
- Introducing API gateway and service discovery.
- Defining service ownership boundaries and contracts.
- Stabilizing flaky inter-service communication.
- Choosing sync vs async per interaction.

## Prerequisites

- Domain mapped to bounded contexts (Event Storming or similar).
- Team ownership boundaries documented.
- Observability baseline (logs/metrics/traces) operational.
- CI/CD pipeline that can deploy services independently.

## Instructions

### 1. Decide Whether You Need Microservices Yet

Microservices buy independent deployability and team autonomy at the cost of distributed-system complexity (network failures, partial failures, eventual consistency, distributed tracing, deploy ordering). Don't pay this cost without a payback.

Reach for microservices when:

- Multiple teams contend for the same monolith deploy lane.
- Different parts of the system have very different scaling profiles or SLAs.
- Independent release cadence is genuinely needed.

Otherwise: **modular monolith** with **Spring Modulith** - separate modules, enforced boundaries (ArchUnit), one deployable. You get most boundary benefits and can split later if pressure justifies it.

### 2. Define Boundaries from Business Capabilities

Good boundary signals:

- Owned by one team end-to-end.
- One ubiquitous language inside; translation at the edges.
- Independent change cadence.
- Few synchronous dependencies on other contexts.

Anti-patterns: services per database table, services per UI screen, services per layer (no "auth-service / order-service / db-service").

Each service owns its data. **No shared database** across service boundaries (no joining `orders.orders` from `payments-service`). Consume data via API or events.

### 3. API Contracts: Stable, Versioned, Backward-Compatible

- Each service publishes an OpenAPI 3.1 spec; clients are generated, not hand-written.
- Additive evolution is non-breaking (add fields, never remove or rename in same version).
- Bump version (`/api/v2/...`) only for breaking changes; keep v1 alive through a stated deprecation window with `Deprecation` and `Sunset` headers (RFC 9745).
- Contract tests (Spring Cloud Contract or Pact) verify provider compatibility on every PR.

### 4. Ingress: API Gateway

Gateway responsibilities (use Spring Cloud Gateway, Kong, NGINX, AWS API Gateway, etc.):

- Public route composition (`/orders -> orders-service`).
- TLS termination.
- AuthN handoff (validate JWT, propagate claims as headers).
- Rate limiting.
- Request/response logging (sample), correlation ID injection.
- CORS for browser clients.

Anti-patterns: business logic in gateway filters; field-level data shaping (use BFF or GraphQL gateway if you need that).

```yaml
# Spring Cloud Gateway minimal route
spring:
  cloud:
    gateway:
      routes:
      - id: orders
        uri: lb://orders-service
        predicates: [Path=/api/v1/orders/**]
        filters:
        - name: RequestRateLimiter
          args:
            redis-rate-limiter.replenishRate: 100
            redis-rate-limiter.burstCapacity: 200
```

### 5. Service Discovery and Client-Side Resilience

Two flavors:

| Approach | Examples | Use when |
| --- | --- | --- |
| Platform-native | K8s Services + DNS (`http://orders-service.orders.svc.cluster.local`) | Running on K8s - the default in 2026 |
| Library-based | Eureka, Consul | Hybrid / non-K8s environments |

For K8s, prefer platform DNS - one less thing to operate.

Every outbound client gets:

- **Connect + read timeouts** (no defaults rely on infinity).
- **Circuit breaker** (Resilience4j) - fail fast when downstream is dead.
- **Retry** for idempotent calls only, with exponential backoff + jitter, max 2-3 attempts.
- **Bulkhead** - bound concurrent in-flight calls per dependency so one slow service can't exhaust threads/connections for others.

```java
@Service
class PaymentClient {
    private final RestClient http;

    @CircuitBreaker(name = "payments", fallbackMethod = "fallback")
    @Retry(name = "payments")
    @Bulkhead(name = "payments")
    @TimeLimiter(name = "payments")
    public CompletableFuture<AuthResponse> authorize(AuthRequest req) {
        return CompletableFuture.supplyAsync(() ->
            http.post().uri("/v1/authorize").body(req).retrieve().body(AuthResponse.class));
    }

    private CompletableFuture<AuthResponse> fallback(AuthRequest req, Throwable t) {
        return CompletableFuture.completedFuture(AuthResponse.deferred(req.orderId()));
    }
}
```

```yaml
resilience4j:
  circuitbreaker:
    instances:
      payments:
        slidingWindowSize: 50
        failureRateThreshold: 50
        waitDurationInOpenState: 30s
  timelimiter:
    instances:
      payments: { timeoutDuration: 2s }
  retry:
    instances:
      payments:
        maxAttempts: 3
        waitDuration: 200ms
        enableExponentialBackoff: true
        retryExceptions:
          - java.net.SocketTimeoutException
          - org.springframework.web.client.ResourceAccessException
```

### 6. Synchronous vs Asynchronous Communication

Choose by **what happens if the callee is down right now?**

| Mode | Use when | Pattern |
| --- | --- | --- |
| Synchronous (REST) | Caller needs the answer to continue, downstream is available, latency budget allows | `RestClient` + Resilience4j |
| Asynchronous (event) | Caller doesn't need an immediate response, eventual consistency OK | Kafka / RabbitMQ + outbox |
| Request-reply over messaging | Caller needs answer but you want decoupling | Reply queue + correlation ID |

Avoid synchronous chains of more than 2-3 hops. Each hop multiplies failure probability.

### 7. Async with the Transactional Outbox (Mandatory for Reliability)

Never publish to a broker from inside an HTTP handler with no durability. The pattern:

1. In the **same DB transaction** as the state change, INSERT a row into an `outbox` table.
2. A separate worker (poll or CDC like Debezium) reads new outbox rows and publishes to the broker, then marks them sent.
3. Consumers are **idempotent** (dedupe by event ID).

This guarantees at-least-once delivery without lost events when the broker is down. Use the Spring Modulith outbox or roll your own.

```java
@Transactional
public Order place(CreateOrderRequest req) {
    var order = orderRepo.save(Order.create(req));
    outbox.record(new OrderPlacedEvent(order.id(), order.total()));
    return order;
}
```

### 8. Saga / Choreography for Distributed Transactions

Distributed `@Transactional` does not exist (no XA in microservices, please). For multi-service workflows use a **saga**:

- **Choreography**: each service reacts to events; compensations on failure (`OrderPlaced -> PaymentRequested -> InventoryReserved` ... if any fails, emit compensating events).
- **Orchestration**: a coordinator (e.g., Camunda, Temporal) drives the steps - clearer visibility for complex workflows.

Document compensation paths explicitly. Test them.

### 9. Data Consistency

- One write owner per piece of data.
- Read replicas / projections allowed across services via events ("Customer Updated" -> Orders projects a slim Customer view).
- Avoid two-phase commit. Embrace eventual consistency at boundaries; communicate it to product/UX.

### 10. End-to-End Observability

- **Trace context propagation** across services with Micrometer Tracing + W3C `traceparent` header. Every request carries a `traceId` from gateway through every service to DB / broker.
- **Correlation ID** for messaging: include `traceparent` as a Kafka header; consumers attach to the same trace.
- **RED metrics per service** + **dependency health** dashboards.
- Service catalog (Backstage, etc.) listing owner, runbooks, SLO, dashboards, on-call.

### 11. Deployment Independence and Compatibility

- Forward + backward compatibility for one release at a time. Never require coordinated multi-service releases.
- Database changes use expand/contract (see data-jpa module): deploy code that writes to old + new, then deploy code that reads from new only, then drop old.
- Feature flags for risky behavior (LaunchDarkly, OpenFeature, Unleash).

### 12. When to Split a Module Out of the Monolith

Triggers:

- Independent scaling profile or SLA.
- Different team owns it now.
- Different release cadence is causing contention.
- Distinct compliance / data-sovereignty requirements.

Process: convert module to publish events, expose API, use it remotely from monolith via client. Once monolith no longer touches its data directly, extract.

## Common Pitfalls

| Anti-pattern | Why fatal | Fix |
| --- | --- | --- |
| Shared database across services | Hidden coupling, contention, no team autonomy | Each service owns its data; events for projections |
| Long synchronous chains | Multiplies failure probability and latency | Async events; flatten chains |
| No timeout on outbound HTTP | One slow downstream hangs all threads | Connect + read timeouts always |
| Retry on non-idempotent POST | Duplicate side effects | Retry only idempotent calls; or use `Idempotency-Key` |
| Publish event after DB commit (no outbox) | Lost events when broker down | Transactional outbox |
| Shared library with domain types across services | Lock-step releases | Per-service models; small shared libs only for cross-cut (logging, tracing) |
| Distributed `@Transactional` / XA | Doesn't work, fragile | Saga + compensations |
| Building a "framework microservice" early | Premature abstraction | Modular monolith first |
| Using gateway for business logic | Single point of complexity | Logic in services |
| No contract tests | Breaks consumers on every release | Spring Cloud Contract / Pact in CI |

## Output Format

When applying this skill, deliver:

1. Decision: monolith / modular monolith / microservices, with rationale.
2. Service boundary map with owner per service.
3. Per-service contract (OpenAPI link) + versioning policy.
4. Sync/async decision per interaction, with diagrams.
5. Resilience4j config per outbound dependency.
6. Outbox + saga design for any multi-service workflow.
7. Observability checklist (tracing, RED, dashboards) per service.
8. Migration roadmap if extracting from a monolith.

## Authoritative References

- Spring Modulith (modular monolith): https://docs.spring.io/spring-modulith/reference/
- Spring Cloud Gateway: https://docs.spring.io/spring-cloud-gateway/reference/
- Resilience4j with Spring Boot: https://resilience4j.readme.io/docs/getting-started-3
- Micrometer Tracing: https://micrometer.io/docs/tracing
- Spring Cloud Contract: https://docs.spring.io/spring-cloud-contract/reference/
- W3C Trace Context: https://www.w3.org/TR/trace-context/
- Microservices.io patterns (Chris Richardson): https://microservices.io/patterns/index.html
- Saga pattern: https://microservices.io/patterns/data/saga.html
- Transactional outbox: https://microservices.io/patterns/data/transactional-outbox.html
- Debezium (CDC for outbox): https://debezium.io/documentation/
- Domain-Driven Design (Evans, summary): https://www.domainlanguage.com/ddd/reference/
- Team Topologies (org/architecture alignment): https://teamtopologies.com/key-concepts
- Apache Kafka Spring integration: https://docs.spring.io/spring-kafka/reference/

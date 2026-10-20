---
name: spring-boot-performance
description: Apply practical Spring Boot performance standards for database access, pagination, caching, batching, and runtime tuning. Use when implementing or reviewing high-traffic backend flows.
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Spring Boot Performance

Prevent the well-known performance regressions in Spring Boot 3.x services and tune the runtime explicitly: kill N+1, enforce keyset pagination, design caches with failure modes, batch DB writes, size pools to workload, and exploit virtual threads on JDK 21.

## Context

You are implementing or reviewing data-heavy or latency-sensitive Spring Boot flows. Output must be measurable, repeatable, and not "improve" things by adding hidden complexity. Every change is justified by a metric or load test.

## When to Use This Skill

- Building list/search APIs.
- Adding caching around expensive operations.
- Tuning a service that hits a latency or throughput cliff under load.
- Reviewing a PR for perf regressions.
- Adopting virtual threads (JDK 21+) on a blocking-I/O service.

## Prerequisites

- Profiling/load tooling: JFR, async-profiler, k6/Gatling, JMeter.
- Production-realistic data volumes for load tests.
- Hibernate statistics or `datasource-proxy` available in tests.
- Cache backend (Redis 7+) decided.
- Baseline SLO defined (P95 latency, throughput, error budget).

## Instructions

### 1. Red-Line Anti-Patterns (Block at Code Review)

| Smell | Why fatal | Replacement |
| --- | --- | --- |
| DB query inside a loop (N+1) | O(n) round-trips per request | Single query with `IN (...)`, fetch join, or `@EntityGraph` |
| `OFFSET 100000` deep pagination | Linear scan, latency cliff at depth | Keyset/cursor pagination |
| Per-item Redis call inside a loop | Hundreds of network round-trips | Pipeline / `MGET` / batch |
| Per-item HTTP call inside a loop | Network amplification | Batch endpoint or async + bulk |
| `findAll()` on a growing table | Loads entire table into memory | Bounded query + pagination |
| `@Transactional` wrapping a remote API call | DB connection held during network wait | Move call outside transaction |
| Unbounded executor / connection pool | OOM / DB exhaustion under burst | Bounded pool + queue + reject policy |
| Cache write without TTL | Memory leak; stale data forever | Always set `entryTtl` |
| `@OneToMany(fetch = EAGER)` | Cartesian explosion | LAZY + explicit fetch |
| `spring.jpa.open-in-view=true` (default!) | Hidden lazy queries during JSON render | Set to `false` |

### 2. Pagination by Data Shape

| Pattern | Use when | Cost at depth |
| --- | --- | --- |
| Page-based (`OFFSET`) | <10k rows total, shallow pages, admin UIs | O(offset) - bad past page 1k |
| Keyset / cursor | Sorted timeline, large dataset, infinite scroll | O(log n) - flat |
| Search + scroll | Full-text search, analytical | Engine-specific |

Keyset example: see data-jpa module. Always cap `size` (`@Max(100)`).

### 3. Cache Strategy with Failure Modes

```java
public OrderResponse getOrder(UUID id) {
    return cache.get(CacheKeys.order(id), () -> {
        var fresh = repo.findById(id).orElseThrow(...);
        return mapper.toResponse(fresh);
    });   // cache-aside
}
```

Plan for the three cache failure scenarios:

- **Penetration** (queries for non-existent IDs flood the DB): cache the negative result with shorter TTL **or** use a Bloom filter.
- **Breakdown** (popular hot key expires; thundering herd to DB): use a per-key lock (`@Cacheable` with `sync = true`) or single-flight via Redis.
- **Avalanche** (many keys expire at once): jitter TTLs (`base + random`).

Rules:

- Mandatory TTL on every cache write.
- Namespace keys (`orders:order:{id}`).
- Don't cache mutable objects without an explicit invalidation hook on writes.
- Don't cache rapidly changing data (TTL too short -> low hit ratio -> just slower).
- Track `cache.gets` with `result=hit|miss` tag; alert if hit ratio drops.

```yaml
spring:
  cache:
    type: redis
  data:
    redis:
      timeout: 200ms
      lettuce:
        pool:
          max-active: 16
```

### 4. JPA / SQL Performance

- Select only needed columns. DTO projection (`select new com.acme.OrderRow(o.id, o.total) ...`) for list endpoints.
- Use database indexes that match query filter + sort prefix. Verify with `EXPLAIN` (Postgres `EXPLAIN (ANALYZE, BUFFERS)`).
- Avoid wrapping indexed columns in functions in WHERE (`LOWER(email)` blocks index unless functional index exists).
- Batch inserts/updates: `hibernate.jdbc.batch_size=50`, `order_inserts=true`, `order_updates=true`. Use `SEQUENCE` ID generator (NOT `IDENTITY`) so batching works.
- For very large reads: `Stream<T>` + `@QueryHints(@QueryHint(name = HINT_FETCH_SIZE, value = "100"))`, processed in pages.

```yaml
spring:
  jpa:
    open-in-view: false
    properties:
      hibernate:
        jdbc.batch_size: 50
        order_inserts: true
        order_updates: true
        query.fail_on_pagination_over_collection_fetch: true
        query.in_clause_parameter_padding: true
```

### 5. Connection Pool Sizing

HikariCP guidance: **smaller is faster**. Start near the DB's effective parallelism limit, not "as big as possible".

Rule of thumb: `pool_size = ((core_count * 2) + effective_spindle_count)` per app instance, capped by what the DB can handle across all instances.

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 2000
      max-lifetime: 1800000          # below DB's wait_timeout / idle-in-transaction killer
      leak-detection-threshold: 5000
```

Total connections across all replicas must stay below DB `max_connections` with safety margin.

### 6. Virtual Threads (JDK 21+) for Blocking I/O

For typical blocking-I/O services (REST -> JDBC + downstream HTTP), enable virtual threads:

```yaml
spring:
  threads:
    virtual:
      enabled: true
```

This switches Tomcat request threads, `@Async`, and scheduled tasks to virtual threads. You no longer need a giant request thread pool.

Caveats:

- **Pinning**: virtual threads pinned by `synchronized` blocks degrade to platform threads. Replace `synchronized` with `ReentrantLock` on hot paths (Hibernate connection pool, JDBC drivers - mostly fixed in latest versions).
- **Connection pool stays bounded**: virtual threads do not magically increase your DB capacity. Hikari pool + DB `max_connections` are still the limit.
- Don't pool virtual threads (`Executors.newVirtualThreadPerTaskExecutor()` creates them on demand).

### 7. Reactive vs Virtual Threads

Reactive (WebFlux + R2DBC) shines when you need huge concurrency on tiny memory and fully non-blocking back ends. With JDK 21 virtual threads, **stay on Spring MVC** for blocking back ends - simpler stack, easier debugging, equal or better throughput in most measured workloads. Choose reactive only if your downstream is fully reactive and you've measured the win.

### 8. Asynchronous and Batch Work

- Use `@Async` (with virtual threads or a bounded `ThreadPoolTaskExecutor`) for fire-and-forget. Always set timeouts on `CompletableFuture.get`.
- For scheduled batch: `@Scheduled` with explicit `ShedLock` (Lock4j) to coordinate across pods. Don't run heavy jobs on every replica.
- For reliable async outbound (events, integrations): **transactional outbox** pattern - persist event in same TX as state change; ship from outbox to broker in a separate worker.

### 9. HTTP Client Tuning

Use Spring 6 `RestClient` (or `HttpInterfaces`) - prefer over `RestTemplate`. Always set timeouts.

```java
@Bean
RestClient paymentsClient(RestClient.Builder b, PaymentProperties p) {
    var factory = ClientHttpRequestFactories.get(
        ClientHttpRequestFactorySettings.DEFAULTS
            .withConnectTimeout(Duration.ofSeconds(2))
            .withReadTimeout(p.timeout()));
    return b.baseUrl(p.baseUrl()).requestFactory(factory).build();
}
```

Add resilience: Resilience4j `@CircuitBreaker`, `@Retry` (idempotent calls only), `@Bulkhead` to bound concurrent calls per dependency.

### 10. JVM Tuning Defaults

- Heap: `-XX:MaxRAMPercentage=75.0` so JVM respects container limits (don't hard-code `-Xmx`).
- GC: G1GC default is fine; consider ZGC (`-XX:+UseZGC`) for sub-ms pauses on heaps > 8GB.
- Container awareness: JVM 17+ is container-aware. Set CPU/memory limits in K8s; JVM picks them up.
- String dedup: `-XX:+UseStringDeduplication` for memory-heavy services.
- JFR in prod: `-XX:StartFlightRecording=settings=profile,maxsize=256m,filename=/var/log/app.jfr` for always-on profiling.

### 11. Native Image (GraalVM) - Opt-In

Spring Boot 3.x + Spring AOT supports native images. Wins: ~50ms cold start, 5-10x lower memory at idle. Costs: longer build, fewer dynamic features (reflection needs hints), slower peak throughput.

Use when: serverless / scale-to-zero / batch jobs / CLIs. Avoid when: heavy reflection (some ORMs), throughput-critical long-lived services.

### 12. Validate Every Change with Numbers

Before claiming a perf win, produce:

- Load test result (k6/Gatling) with P50/P95/P99 latency + throughput, before vs after.
- Query count assertion in a test for the changed endpoint (no N+1 regression).
- Cache hit-ratio metric for new caches.
- JFR or async-profiler flame graph for CPU-bound changes.

## Common Pitfalls

| Anti-pattern | Fix |
| --- | --- |
| Premature caching of cheap queries | Profile first; index DB before caching |
| One huge cache TTL (24h) for everything | Tier TTLs by mutation rate; jitter |
| Hikari pool size = 100 because "more is better" | Right-size to DB capacity / replicas |
| `findAll()` then filter in Java | Push filter to SQL with index |
| `@Transactional` over a 5-step orchestration with HTTP calls | Split: persist intent, then call, then update |
| Using `RestTemplate` in 2026 | `RestClient` or HTTP Interfaces |
| Reactive stack for blocking JDBC | Stay on MVC + virtual threads |
| Synchronized blocks on hot path with virtual threads | `ReentrantLock` |
| Fire-and-forget without retry/outbox | Outbox + at-least-once worker |
| Optimizing without a baseline number | Measure first; set SLO; then change |

## Output Format

When applying this skill, deliver:

1. Red-line checklist verified for the change.
2. Pagination decision per affected endpoint (with cap).
3. Cache plan: keys, TTLs, invalidation triggers, failure-mode mitigations.
4. SQL/index review for new/changed queries (with `EXPLAIN`).
5. Pool/threading config diff with rationale.
6. Virtual threads on/off decision.
7. Load test plan + results table (before/after, P95, throughput).

## Authoritative References

- Spring Boot performance: https://docs.spring.io/spring-boot/reference/features/performance.html
- Spring Boot virtual threads: https://docs.spring.io/spring-boot/reference/features/task-execution-and-scheduling.html
- Hibernate performance: https://docs.jboss.org/hibernate/orm/6.6/userguide/html_single/Hibernate_User_Guide.html#performance
- HikariCP pool sizing: https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing
- JEP 444 (Virtual Threads): https://openjdk.org/jeps/444
- JFR: https://docs.oracle.com/en/java/javase/21/troubleshoot/diagnostic-tools.html
- async-profiler: https://github.com/async-profiler/async-profiler
- k6 load testing: https://k6.io/docs/
- Resilience4j: https://resilience4j.readme.io/docs
- ShedLock: https://github.com/lukas-krecan/ShedLock
- GraalVM Native Image: https://www.graalvm.org/latest/reference-manual/native-image/
- Spring AOT/Native: https://docs.spring.io/spring-boot/reference/packaging/native-image/index.html

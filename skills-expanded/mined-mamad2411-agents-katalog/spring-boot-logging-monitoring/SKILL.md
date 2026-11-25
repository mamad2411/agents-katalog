---
name: spring-boot-logging-monitoring
description: Implement production-grade logging and monitoring in Spring Boot with level policy, structured logs, tracing context, and metrics. Use when adding observability to backend services.
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Spring Boot Logging and Monitoring

Implement production-grade observability in Spring Boot 3.x using SLF4J + Logback structured logs, Micrometer metrics with Prometheus/OTLP, and Micrometer Tracing on OpenTelemetry. Design logs and metrics that survive an incident at 03:00.

## Context

You are adding or reviewing observability in a Spring Boot 3.x service. Output must give an SRE or on-call engineer enough signal to (1) detect, (2) localize, and (3) diagnose an incident without re-deploying. Spring Cloud Sleuth was removed in Boot 3 - use **Micrometer Tracing**.

## When to Use This Skill

- Defining logging policy for a new service.
- Wiring distributed tracing across services.
- Designing service metrics + dashboards + alerts.
- Migrating Boot 2.x + Sleuth to Boot 3.x + Micrometer Tracing.
- Improving incident MTTD/MTTR after a postmortem action item.

## Prerequisites

- Spring Boot 3.x with `spring-boot-starter-actuator`.
- For metrics: `micrometer-registry-prometheus` (or `micrometer-registry-otlp`).
- For tracing: `micrometer-tracing-bridge-otel` + `opentelemetry-exporter-otlp`.
- Backend: Prometheus + Grafana, Loki, Tempo/Jaeger - or vendor (Datadog, New Relic, Honeycomb, Grafana Cloud).
- Sensitive-data classification documented (what is PII, what is a secret).

## Instructions

### 1. Log Level Policy (Use Each Level With Intent)

| Level | Meaning | Examples |
| --- | --- | --- |
| `error` | Unexpected fault that needs human attention | DB unreachable, unhandled exception, 500 |
| `warn` | Expected-but-notable degradation | Domain conflict (4xx), retry exhausted, fallback used |
| `info` | Significant business lifecycle event | Order placed, payment captured, batch started/finished |
| `debug` | Diagnostic detail useful when triaging | Cache miss, condition decision; off in prod |
| `trace` | Very fine-grained dev diagnostics | Off in prod |

Anti-patterns: logging validation 400s as `error`; `info` per-row inside loops.

### 2. Structured JSON Logs (Spring Boot 3.4+ Built-In)

Spring Boot 3.4 added native structured logging in ECS, GELF, and Logstash formats. Use it - no custom JSON encoder needed.

```yaml
# application-prod.yml
logging:
  structured:
    format:
      console: ecs                    # ecs | gelf | logstash
  level:
    root: INFO
    org.springframework.web: WARN
    org.hibernate.SQL: WARN
  pattern:
    level: "%5p [${spring.application.name:-},%X{traceId:-},%X{spanId:-}]"
```

For older Boot or custom needs, use `logback-spring.xml` with `LogstashEncoder` and stable additional fields.

Always include in every log line:

- `service.name` (= `spring.application.name`)
- `service.version` (build-info)
- `environment`
- `traceId` / `spanId` (auto-injected by Micrometer Tracing)
- For request logs: HTTP method, route template (not the full URL with IDs), status, latency.

### 3. Parameterized Logging Only

```java
private static final Logger log = LoggerFactory.getLogger(OrderService.class);

log.info("order placed orderId={} customerId={} total={}", id, customerId, total);
```

Never `log.info("order placed " + id)` - allocates strings even when level disabled, no structured fields.

For structured key-value pairs in plain Logback, use `StructuredArguments.kv("orderId", id)` (logstash encoder) or `MDC` for request-scoped fields.

### 4. Mask / Redact Sensitive Data

Never log:

- `Authorization`, `Cookie`, `Set-Cookie` headers.
- Tokens, API keys, passwords, refresh tokens.
- Full PII (email, phone, full name, full address, government IDs). Hash or partially mask if needed for correlation (`email_hash=sha256(...)` or `email=a***@example.com`).
- Card data (PCI scope), health data (HIPAA), etc. per regulatory class.

Implement once with a Logback filter / pattern converter. Add a CI grep gate to fail builds containing forbidden tokens (`grep -E "log.+(password|secret|token)"`).

### 5. Distributed Tracing with Micrometer Tracing + OpenTelemetry

Spring Cloud Sleuth is **gone**. Use Micrometer Tracing.

```xml
<dependency>
  <groupId>io.micrometer</groupId>
  <artifactId>micrometer-tracing-bridge-otel</artifactId>
</dependency>
<dependency>
  <groupId>io.opentelemetry</groupId>
  <artifactId>opentelemetry-exporter-otlp</artifactId>
</dependency>
```

```yaml
management:
  tracing:
    sampling:
      probability: 0.1                # 10% in prod; 1.0 in staging
  otlp:
    tracing:
      endpoint: http://otel-collector:4318/v1/traces
```

The `traceId` / `spanId` automatically appear in MDC for log correlation. Propagation across async boundaries works with `ContextSnapshotFactory` (use `@Async` aware executors via `taskDecorator`).

For custom spans:

```java
@Service
class OrderService {
    private final ObservationRegistry observations;

    @Transactional
    public OrderResponse place(CreateOrderRequest req) {
        return Observation.createNotStarted("order.place", observations)
            .lowCardinalityKeyValue("customer.tier", req.tier().name())
            .observe(() -> doPlace(req));
    }
}
```

Use **low-cardinality** keys for tags (status, tier, route template). High-cardinality fields (`orderId`, `userId`) belong on log lines and span attributes, **not** on metric tags.

### 6. Metrics: The Four Golden Signals + Workload-Specific

Auto-instrumented by Spring/Micrometer:

- `http.server.requests` (count, latency histogram with route + status tags).
- `jvm.*` (heap, GC, threads).
- `hikaricp.*` (connection pool usage, wait time).
- `tomcat.*` (sessions, threads).
- `spring.data.repository.invocations` (with `@EnableJpaRepositories(repositoryFactoryBeanClass = ...)` if needed).

Add per-service business metrics:

```java
@Service
class OrderService {
    private final Counter ordersPlaced;
    private final Timer paymentLatency;

    OrderService(MeterRegistry registry) {
        this.ordersPlaced = Counter.builder("orders.placed")
            .description("Number of orders placed")
            .register(registry);
        this.paymentLatency = Timer.builder("payments.latency")
            .publishPercentiles(0.5, 0.95, 0.99)
            .publishPercentileHistogram()
            .register(registry);
    }
}
```

Enable percentile histograms globally for HTTP if you alert on P99:

```yaml
management:
  metrics:
    distribution:
      percentiles-histogram:
        http.server.requests: true
      slo:
        http.server.requests: 50ms,100ms,200ms,500ms,1s,2s
```

### 7. Tag Discipline (Cardinality)

Tags are dimensions; every unique combination creates a time series. Costs and slow queries explode quickly. Rules:

- **Allowed tags**: `service`, `env`, `region`, `endpoint`/`uri` (route template, not raw path), `method`, `status`, `outcome`.
- **Never tag**: user ID, order ID, IP address, request ID, free-text URL.
- Aim for under 10k active series per metric per replica.

### 8. Health Probes vs Health Checks

- `/actuator/health/liveness` - process is alive. Do NOT include downstream deps - a flaky DB must not restart your pod.
- `/actuator/health/readiness` - safe to receive traffic. INCLUDE critical deps (DB, broker if hot path).

```java
@Component
class CriticalDependencyHealth implements HealthIndicator {
    private final OrderRepository repo;
    @Override public Health health() {
        try { repo.count(); return Health.up().build(); }
        catch (Exception e) { return Health.down(e).build(); }
    }
}
```

```yaml
management:
  endpoint:
    health:
      group:
        readiness:
          include: db, redis, customDependency
        liveness:
          include: ping
```

### 9. Correlation in Async Code

Without help, MDC and trace context are lost across thread boundaries. Wrap executors:

```java
@Bean
TaskExecutor taskExecutor(ContextSnapshotFactory snapshots) {
    var ex = new ThreadPoolTaskExecutor();
    ex.setCorePoolSize(8);
    ex.setTaskDecorator(runnable -> {
        var snapshot = snapshots.captureAll();
        return () -> { try (var scope = snapshot.setThreadLocals()) { runnable.run(); } };
    });
    ex.initialize();
    return ex;
}
```

For virtual threads, the same pattern applies; Micrometer's context propagation library handles it.

### 10. Log Volume and Cost Control

- High-throughput services: use Logback's `AsyncAppender` with bounded queue + `neverBlock=false` (drop on overflow rather than block business threads).
- Sample debug logs in prod (e.g., 1%) using a Logback turbo filter.
- Set retention by class (audit logs longer than debug).
- Rotate by size + time; cap total disk.

### 11. Dashboards and Alerts (Outline)

Per service dashboard:

- RED: Rate, Errors, Duration (P50/P95/P99) per endpoint.
- USE: CPU, memory, GC pause, thread count, Hikari connections used vs max.
- Business KPIs (orders/sec, payment success rate).
- Error budget burn (link to SLO).

Alerts (page on, not just notify):

- 5xx rate > 1% over 5 min.
- P99 latency > SLO over 10 min.
- Hikari pool > 90% for 5 min.
- Readiness probe failing.
- Disk > 85%.

### 12. Sampling and Privacy

- Trace sampling 1-20% in prod by default; head-based + tail-based for errors (collector-side).
- Strip PII from spans (URL paths with IDs - use route template; HTTP headers - exclude `Authorization`).
- Document data retention per signal type (logs vs traces vs metrics).

## Common Pitfalls

| Anti-pattern | Fix |
| --- | --- |
| `log.info("user " + email + " logged in")` | Parameterized + drop full email; log `userId` |
| Logging stack trace at INFO | Stack trace only at WARN/ERROR with cause |
| Tagging metrics with user ID / order ID | Drop to log/span; use bounded tags only |
| Liveness probe queries DB | Liveness = ping; readiness = deps |
| Sleuth annotations in Boot 3 code | Migrate to Micrometer `Observation` |
| `print stack trace`, `e.printStackTrace()` | Logger with cause |
| MDC populated but not cleared (thread reuse) | Clear in finally; or use Micrometer's request observation handler |
| `management.endpoints.web.exposure.include=*` in prod | Whitelist (`health,info,prometheus`) |
| 100% trace sampling in prod | 1-20%, with always-on for errors via tail sampling |
| One mega Grafana dashboard per company | Per-service dashboard with consistent layout |

## Output Format

When applying this skill, deliver:

1. Log level + structured-format policy (with `application-{profile}.yml` snippets).
2. Sensitive-data redaction list + scrubber config.
3. Tracing setup (Micrometer + OTLP exporter) with sampling rate per env.
4. Metrics catalog: name, type, tags, description, owner.
5. Probe policy + custom `HealthIndicator` list.
6. Async / virtual-thread context propagation config.
7. Alert + dashboard outline (RED + USE + business).

## Authoritative References

- Spring Boot Actuator: https://docs.spring.io/spring-boot/reference/actuator/index.html
- Spring Boot logging: https://docs.spring.io/spring-boot/reference/features/logging.html
- Spring Boot structured logging (3.4+): https://docs.spring.io/spring-boot/reference/features/logging.html#features.logging.structured
- Spring Boot metrics: https://docs.spring.io/spring-boot/reference/actuator/metrics.html
- Spring Boot tracing: https://docs.spring.io/spring-boot/reference/actuator/tracing.html
- Micrometer: https://micrometer.io/docs
- Micrometer Tracing: https://micrometer.io/docs/tracing
- OpenTelemetry Java: https://opentelemetry.io/docs/languages/java/
- ECS log schema: https://www.elastic.co/guide/en/ecs/current/index.html
- Google SRE book - SLO/SLI/SLA: https://sre.google/workbook/implementing-slos/
- USE method: http://www.brendangregg.com/usemethod.html
- RED method: https://www.weave.works/blog/the-red-method-key-metrics-for-microservices-architecture/

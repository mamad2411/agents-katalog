---
name: production-observability
description: Use when adding logging, metrics, tracing, or alerting to production systems; debugging intermittent failures; or instrumenting code for monitoring.
---

# Production Observability

This skill ensures production systems are instrumented for visibility, debugging, and operational excellence through logging, metrics, tracing, and alerting.

## When to Activate

- Debugging production-only or intermittent failures
- Adding monitoring to new features before deployment
- Investigating performance bottlenecks or error spikes
- Implementing SLOs, SLIs, or SLA monitoring
- Setting up alerts for critical thresholds
- When systematic-debugging requires production data

Do NOT use for local development bugs (use systematic-debugging).

## Logging

### Structured Logging

Structured logs make querying and analysis possible. Always use JSON format with contextual fields.

#### FAIL: Unstructured Logging
```java
log.info("User login failed for user " + username + " at " + Instant.now());
// Hard to query, parse, or correlate
```

#### PASS: Structured Logging
```java
log.info("login_attempt username={} timestamp={} ip={}", username, Instant.now(), clientIp);
// Queryable: username="john", timestamp=..."
```

#### TypeScript/Node.js Example
```typescript
import pino from 'pino';

const logger = pino();

logger.info({ username, timestamp: new Date(), ip: clientIp }, 'login_attempt');

// Produces JSON:
// {"level":30,"time":1704067200000,"username":"john","timestamp":"...","ip":"...","msg":"login_attempt"}
```

#### Python Example
```python
import structlog
from datetime import datetime

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()
logger.info("login_attempt", username=username, timestamp=datetime.now().isoformat(), ip=client_ip)

# Produces JSON output similar to:
# {"event": "login_attempt", "username": "john", "timestamp": "...", "ip": "..."}
```

#### Go Example
```go
import "go.uber.org/zap"

logger.Info("login_attempt",
    zap.String("username", username),
    zap.Time("timestamp", time.Now()),
    zap.String("ip", clientIp),
)
// Produces JSON:
// {"level":"info","ts":1704067200.123,"msg":"login_attempt","username":"john","ip":"..."}
```

### Log Levels

Use levels appropriately to control volume and enable production filtering.

| Level | Use For | Example |
|-------|---------|---------|
| ERROR | Failures requiring intervention | `log.error("payment_failed paymentId={} userId={}", paymentId, userId, err)` |
| WARN | Unexpected but non-failing conditions | `log.warn("cache_miss key={}", cacheKey)` |
| INFO | Normal operation, business events | `log.info("order_created orderId={}", 123)` |
| DEBUG | Detailed execution flow | `log.debug("cache_hit key={} value={}", cacheKey, result)` |
| TRACE | Very detailed, typically disabled | `log.trace("db_query sql={} params={}", query, params)` |

**Production filtering:**
```yaml
# config.yaml
logging:
  level: INFO  # Production default
  packages:
    important_service: DEBUG  # Specific packages
    chatty_dependency: WARN
```

### Log Sampling

High-volume events should be sampled to reduce costs while maintaining visibility.

```java
// Sample 10% of debug logs
if (Math.random() < 0.1 && logger.isDebugEnabled()) {
    logger.debug("cache_debug key={} value={}", key, value);
}
```

### Correlation IDs

Always include correlation IDs to trace requests across services.

```java
// Filter to extract/create correlation ID
@Component
public class CorrelationFilter extends OncePerRequestFilter {
    private static final String CORRELATION_ID = "X-Correlation-ID";

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain) {
        String correlationId = request.getHeader(CORRELATION_ID);
        if (correlationId == null) {
            correlationId = UUID.randomUUID().toString();
        }
        MDC.put("correlationId", correlationId);

        try {
            chain.doFilter(request, response);
        } finally {
            response.setHeader(CORRELATION_ID, correlationId);
            MDC.remove("correlationId");
        }
    }
}

// Use in logs
log.info("api_call", correlationId=MDC.get("correlationId"), endpoint=requestPath);
```

### Sensitive Data Redaction

Never log passwords, tokens, credit cards, PII, or secrets.

#### FAIL: Logging Sensitive Data
```typescript
console.log("User login", { email, password, creditCard });
```

#### PASS: Redacted Logging
```typescript
console.log("User login", { email, userId, cardLast4: card.last4 });
```

#### Automated Redaction Pattern
```typescript
function redact(obj: any): any {
  const sensitiveFields = ['password', 'token', 'creditCard', 'ssn', 'apiKey'];
  const redacted = { ...obj };

  Object.keys(redacted).forEach(key => {
    if (sensitiveFields.some(field => key.toLowerCase().includes(field))) {
      redacted[key] = '[REDACTED]';
    }
  });

  return redacted;
}

logger.info("user_data", redact(userData));
```

#### Java Redaction
```java
public class RedactingConverter extends MessageConverter {

    private static final Pattern SENSITIVE_PATTERN = Pattern.compile(
        "(password|token|creditCard|apiKey)=[^&\\s]+", Pattern.CASE_INSENSITIVE
    );

    @Override
    protected String convert(ILoggingEvent event) {
        String message = super.convert(event);
        return SENSITIVE_PATTERN.matcher(message).replaceAll("$1=[REDACTED]");
    }
}
```

### Verification Steps

- [ ] All logs use structured format (JSON)
- [ ] Log levels set appropriately (INFO for production, DEBUG for staging)
- [ ] High-volume events sampled (≤10% rate)
- [ ] Correlation ID included in all service logs
- [ ] Sensitive data redacted (passwords, tokens, PII)
- [ ] No console.log (use proper logger)
- [ ] Error logs include stack traces and context

## Metrics

### Metric Types

| Type | Use For | Cardinality |
|------|---------|-------------|
| Counter | Things that only increase (requests, errors, bytes sent) | Low |
| Gauge | Current value (connections, memory, queue size) | Very Low |
| Histogram | Quantiles and distributions (request latency, response sizes) | Med |
| Summary | Similar to histogram, compute on client | Med |

### Counter Metrics

Count monotonic events.

```java
// Counter for tracking HTTP requests
private final Counter httpRequests;

public MetricsController(MeterRegistry registry) {
    this.httpRequests = Counter.builder("http.requests")
        .description("HTTP requests")
        .tag("method", "GET")  // Low cardinality tag
        .tag("status", "200")
        .register(registry);
}

httpRequests.increment();
```

```typescript
import { Counter } from 'prom-client';

const httpRequestCounter = new Counter({
    name: 'http_requests_total',
    help: 'HTTP requests total',
    labelNames: ['method', 'status', 'route'],
});

httpRequestCounter.inc({ method: 'GET', status: '200', route: '/users' });
```

```python
from prometheus_client import Counter

http_requests = Counter('http_requests_total', 'HTTP requests total', ['method', 'status', 'route'])
http_requests.labels(method='GET', status='200', route='/users').inc()
```

### Gauge Metrics

Track instantaneous values.

```java
// Gauge for active database connections
private final AtomicInteger activeConnections = new AtomicInteger(0);

Gauge.builder("db.connections.active", activeConnections::get)
    .description("Active database connections")
    .register(registry);
```

### Histogram/Summary Metrics

Track distributions (latency, sizes).

```java
// Histogram for request latency
private final Histogram latencyHistogram;

public MetricsController(MeterRegistry registry) {
    this.latencyHistogram = Histogram.builder("http.request.latency")
        .description("HTTP request latency")
        .serviceLevelObjectives(
            Duration.ofMillis(10),
            Duration.ofMillis(50),
            Duration.ofMillis(100),
            Duration.ofMillis(500),
            Duration.ofMillis(1000)
        )
        .register(registry);
}

Timer.Sample sample = Timer.start(registry);
// ... do work
sample.stop(registry.timer("http.request.duration"));
```

```typescript
import { Histogram } from 'prom-client';

const httpRequestDuration = new Histogram({
    name: 'http_request_duration_seconds',
    help: 'HTTP request duration in seconds',
    labelNames: ['method', 'route', 'status'],
    buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
});

const end = httpRequestDuration.startTimer();
// ... do work
end({ method: 'GET', route: '/users', status: '200' });
```

### Metric Naming Conventions

Follow naming standards for consistency.

| Pattern | Example | Use |
|---------|---------|-----|
| `<domain>_<action>_total` | `http_requests_total` | Counters |
| `<domain>_<metric>` | `db_connections_active` | Gauges |
| `<domain>_<metric>_seconds` | `http_request_duration_seconds` | Duration |
| `<domain>_<metric>_bytes` | `api_response_size_bytes` | Size |

**Good patterns:**
```java
Counter.builder("http.requests.total")         // ✅ Clear
.register(registry);

Counter.builder("http_req_2xx")               // ✅ Specific
.register(registry);

Counter.builder("user_logins")               // ❌ Missing base
.register(registry);
```

### Cardinality Management

High cardinality metrics (many unique tag values) cause performance issues and memory bloat.

#### FAIL: High Cardinality
```java
// user_id has unlimited values - DON'T DO THIS
Counter.builder("http.requests")
    .tag("user_id", userId.toString())  // ❌ Millions of unique values
    .register(registry);
```

#### PASS: Low Cardinality
```java
// Use aggregates instead
Counter.builder("http.requests")
    .tag("method", request.getMethod())        // ✅ Limited (GET, POST, PUT, DELETE)
    .tag("status", Integer.toString(response.getStatus()))  // ✅ Limited (200, 404, 500)
    .register(registry);
```

#### Cardinality Guidelines
| Tag Type | maxUniqueValues | Safe? |
|----------|----------------|-------|
| HTTP method | ~10 | ✅ Yes |
| Status code | ~50 | ✅ Yes |
| Service name | ~100 | ✅ Yes |
| Customer ID | ~10,000+ | ❌ No |
| Request ID | Unlimited | ❌ No |

### Business vs Infrastructure Metrics

**Infrastructure (automated):**
- CPU usage
- Memory usage
- Disk I/O
- Network throughput
- Database connections

**Business (require instrumentation):**
- Orders per minute
- User registrations
- Payment success rate
- Search click-through rate
- Feature adoption rate

```java
// Business metric example
private final Counter ordersCreated;

public OrderService(MeterRegistry registry) {
    this.ordersCreated = Counter.builder("orders.total")
        .description("Total orders created")
        .tag("status", "success")
        .register(registry);
}

public Order createOrder(CreateOrderRequest request) {
    Order order = // ... create order
    ordersCreated.increment();
    return order;
}
```

### Verification Steps

- [ ] All metrics follow naming conventions
- [ ] Cardinality managed properly (no high-cardinality tags)
- [ ] Both infrastructure and business metrics instrumented
- [ ] Histograms used for latency (include relevant percentiles)
- [ ] Counters for monotonic events
- [ ] Gauges for current state
- [ ] Metrics visible in dashboards (Datadog, Prometheus, Grafana)

## Distributed Tracing

### Tracing Fundamentals

Tracing follows requests across multiple services to visualize latency and identify bottlenecks.

**Span components:**
- Operation name (e.g., "http.request", "db.query")
- Start/stop timestamps
- Tags (metadata)
- Events (timed annotations)
- Links (to other traces)

### OpenTelemetry Tracing

#### Java/Spring Boot Example
```java
import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.SpanKind;
import io.opentelemetry.api.trace.StatusCode;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Scope;
import io.opentelemetry.instrumentation.annotations.WithSpan;

@Service
class UserService {

    @WithSpan("UserService.getUserById")  // Create span
    public User getUserById(Long id) {
        // Span automatically created by @WithSpan annotation
        return userRepository.findById(id);
    }

    public User createUser(CreateUserRequest request) {
        Tracer tracer = GlobalOpenTelemetry.getTracer("UserService");
        Span span = tracer.spanBuilder("UserService.createUser")
            .setSpanKind(SpanKind.SERVER)
            .startSpan();

        try (Scope scope = span.makeCurrent()) {
            // Add tags to span
            span.setAttribute("user.id", request.getEmail());
            span.setAttribute("user.role", "customer");

            User user = userRepository.save(new User(request.getEmail()));

            span.setStatus(StatusCode.OK);
            return user;
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();  // Always end span
        }
    }
}
```

#### TypeScript/Node.js Example
```typescript
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('user-service');

async function createUser(request: CreateUserRequest) {
    const span = tracer.startSpan('createUser');

    try {
        // Add attributes
        span.setAttribute('user.email', request.email);
        span.setAttribute('user.role', 'customer');

        // Create user
        const user = await userRepository.create(request);

        span.setStatus({ code: SpanStatusCode.OK });
        return user;
    } catch (error) {
        span.recordException(error);
        span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
        throw error;
    } finally {
        span.end();
    }
}
```

#### Python Example
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def create_user(request: CreateUserRequest) -> User:
    with tracer.start_as_current_span("createUser") as span:
        # Set attributes
        span.set_attribute("user.email", request.email)
        span.set_attribute("user.role", "customer")

        # Create user
        user = user_repository.create(request)

        span.set_status(Status(StatusCode.OK))
        return user
```

#### Go Example
```go
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/trace"
    "context"
)

func CreateUser(ctx context.Context, req *CreateUserRequest) (*User, error) {
    tracer := otel.Tracer("user-service")
    ctx, span := tracer.Start(ctx, "createUser")

    // Set attributes
    span.SetAttributes(
        attribute.String("user.email", req.Email),
        attribute.String("user.role", "customer"),
    )

    // Create user
    user, err := userRepository.Create(ctx, req)
    if err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, err.Error())
        return nil, err
    }

    span.SetStatus(codes.Ok)
    span.End()
    return user, nil
}
```

### Distributed Context Propagation

Trace context must flow across service boundaries.

```java
// HTTP Client with propagation
@Component
class ExternalServiceClient {

    private final OpenTelemetry openTelemetry;
    private final Tracer tracer;
    private final RestTemplate restTemplate;

    public ExternalServiceClient(OpenTelemetry openTelemetry, RestTemplate restTemplate) {
        this.openTelemetry = openTelemetry;
        this.tracer = openTelemetry.getTracer("ExternalServiceClient");
        this.restTemplate = restTemplate;
    }

    public ExternalApiResponse callExternal(String userId) {
        Span span = tracer.spanBuilder("external-service.call")
            .setSpanKind(SpanKind.CLIENT)
            .startSpan();

        try (Scope scope = span.makeCurrent()) {
            HttpHeaders headers = new HttpHeaders();
            openTelemetry.getPropagators().getTextMapPropagator().inject(
                Context.current(),
                headers,
                HttpHeaders::set
            );

            ResponseEntity<ExternalApiResponse> response = restTemplate.exchange(
                "https://external-service.com/user/" + userId,
                HttpMethod.GET,
                new HttpEntity<>(headers),
                ExternalApiResponse.class
            );

            return response.getBody();
        } finally {
            span.end();
        }
    }
}
```

```typescript
// Propagation in HTTP calls
import * as api from '@opentelemetry/api';

async function callExternal(userId: string) {
    const span = api.trace.getTracer('client').startSpan('external-service.call');

    try {
        const spanContext = api.trace.setSpan(api.context.active(), span);

        const response = await fetch(`https://external-service.com/user/${userId}`, {
            headers: {
                // Trace context automatically propagated with auto-instrumentation
                'traceparent': api.trace.getSpan(spanContext).spanContext().toString(),
            },
        });

        return response.json();
    } finally {
        span.end();
    }
}
```

### Baggage Propagation

Baggage carries metadata across services without timing measurements.

```java
// In request handler
Baggage baggage = Baggage.builder()
    .put("tenant.id", tenantId)
    .put("user.segment", userSegment)
    .build();

BaggageContext.updateCurrent(baggage);

// In downstream service
String tenantId = Baggage.fromContext(Context.current()).getEntryValue("tenant.id");
```

### Sampling

High-traffic systems must sample traces to reduce costs.

```yaml
# application.yaml
otel:
  traces:
    sampler:
      type: parentbased_traceidratio
      argument: 0.1  # Sample 10% of traces
```

Or custom sampling:
```java
class BusinessAwareSampler implements Sampler {

    @Override
    public SamplingResult shouldSample(...) {
        // Always sample errors
        SpanContext parentContext = getParentSpanContext(spanContext);
        if (parentContext != null && parentContext.isRemote()) {
            boolean isError = getSpanKindFromLinks(links) == SpanKind.INTERNAL;
            if (isError) {
                return SamplingResult.create(true);  // Sample error traces
            }
        }

        // Sample 5% of GET requests to /health
        if (name.equals("http.request") && hasTag("path", "/health")) {
            return SamplingResult.create(Math.random() < 0.05);
        }

        // Default: don't sample
        return SamplingResult.create(false);
    }
}
```

### Verification Steps

- [ ] All services instrumented with tracing
- [ ] Trace context propagated across service boundaries
- [ ] Appropriate sampling configured
- [ ] Spans include relevant attributes/tags
- [ ] Error conditions recorded in spans
- [ ] Traces visible in tracing backend (Jaeger, Tempo, Datadog)
- [ ] Span names follow naming conventions (e.g., "http.request", "db.query")

## Alerting

### Alert Design Principles

**Alert fatigue** causes teams to ignore real issues. Design alerts to be actionable.

| Alert Type | Purpose | Example |
|------------|---------|---------|
| Threshold | Fixed value exceeded | Error rate > 5% |
| Anomaly | Expected value exceeded | Latency spikes |
| Composite | Multiple conditions | CPU > 80% AND requests increasing |
| Watchdog | Is a service up? | Health check failing |

### Alert Hierarchy

```
P0 (Critical)  - Wake up team immediately
  - Service completely down
  - Data loss
  - Security breach

P1 (High)      - Page within 5 minutes
  - Major functionality broken
  - SLA violations
  - Error rate > 5%

P2 (Medium)    - Message within 30 minutes
  - Degraded performance
  - Minor feature broken
  - Error rate > 1%

P3 (Low)       - Daily digest
  - Resource utilization
  - Informational alerts
  - Trend data
```

### Alert Examples

#### Critical Alert (P0)
```yaml
alert: ServiceDown
expr: up{job="api-server"} == 0
for: 1m
labels:
  severity: critical
annotations:
  summary: "API server {{ $labels.instance }} is down"
  description: "API server has been down for more than 1 minute."

routes:
  - receiver: oncall
    match_re:
      severity: critical
```

#### High Priority Alert (P1)
```yaml
alert: HighErrorRate
expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
for: 2m
labels:
  severity: high
annotations:
  summary: "High error rate detected"
  description: "{{ $value | humanizePercentage }} of requests are errors"

routes:
  - receiver: slack-engineering
    match_re:
      severity: high
```

#### Performance Alert (P2)
```yaml
alert: HighLatency
expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 0.5
for: 5m
labels:
  severity: medium
annotations:
  summary: "99th percentile latency is high"
  description: "P99 latency is {{ $value | humanizeDuration }}"
```

### Alert Suppression

Prevent alert storms during expected events.

```yaml
suppress_alerts:
  - name: Deployments
    match:
      severity: warning|high|critical
    condition: deployment_in_progress == true
    until: deployment_complete

  - name: Scheduled Maintenance
    match:
      severity: warning|high
    condition: maintenance_window == true
    duration: 2h
```

### Alert Routing

Route to appropriate teams.

```yaml
routes:
  - receiver: oncall-platform
    match_re:
      service: (api-server|user-service|payment-service)

  - receiver: oncall-data
    match_re:
      service: (database|cache|queue|storage)

  - receiver: slack-qa
    match_re:
      service: test-*
    match:
      severity: medium|low

  - receiver: slack-security
    match:
      alertname: SecurityEvent
```

### On-Call Rotation

```yaml
oncall:
  team: platform
  rotation:
    - engineer: alice
      timezone: UTC
      start: 2025-01-01T00:00:00Z
      duration: 7d
    - engineer: bob
      timezone: America/Los_Angeles
      start: 2025-01-08T00:00:00Z
      duration: 7d

  escalation:
    - wait: 15m
      notify: alice
    - wait: 30m
      notify: alice,bob  # Escalate to backup
    - wait: 45m
      notify: platform-engineering-manager
```

### SLO/SLA Alerting

Alert on SLO burn rate, not just thresholds.

```yaml
# SLO: 99.9% availability (0.1% error budget)
alert: SLOBurnRateCritical
expr: |
  (
    1 - rate(http_requests_total{status=~"2..,3.."}[30m])
    /
    rate(http_requests_total[30m])
  ) > 0.001  # 0.1% error budget
for: 5m
annotations:
  summary: "SLO burn rate is critical"
  description: "Error budget burning at {{ $value | humanizePercentage }} per hour"

alert: SLOBurnRateWarning
expr: |
  (
    1 - rate(http_requests_total{status=~"2..,3.."}[1h])
    /
    rate(http_requests_total[1h])
  ) > 0.0005  # 0.05% error budget
for: 15m
```

### Verification Steps

- [ ] Alerts have clear actionability (what to do when triggered)
- [ ] Priorities assigned (P0, P1, P2, P3)
- [ ] On-call rotation configured
- [ ] Escalation paths defined
- [ ] Suppression rules for expected events
- [ ] Alerts tested (trigger test incident)
- [ ] Documentation available (runbook, escalation matrix)

## Integration Patterns

### Observability Stack

```
Application → Logging Library (Winston, SLF4J)
           → Metrics Library (OpenTelemetry, Micrometer)
           → Tracing Library (OpenTelemetry)

Logs → Log Aggregation (Logstash, Fluentd)
     → Storage and Indexing (Elasticsearch, Loki)
     → Visualization (Kibana, Grafana)

Metrics → Collection Agent (Prometheus, Datadog Agent)
        → Time Series DB (Prometheus, InfluxDB)
        → Alerting (Prometheus Alertmanager, PagerDuty)

Traces → Collector (OpenTelemetry Collector)
       → Backend (Jaeger, Tempo, Datadog APM)
       → Analysis (Dashboards, Root Cause Analysis)
```

### Cross-Language Observability

OpenTelemetry provides language-agnostic standards.

```
┌─────────────────┐
│   API Service   │ (Java/Spring)
└────────┬────────┘
         │ HTTP Request
         │ (traceparent, baggage)
         ▼
┌─────────────────┐
│   User Service  │ (Node.js/TypeScript)
└────────┬────────┘
         │ gRPC Call
         │ (traceparent, baggage)
         ▼
┌─────────────────┐
│ Payment Service │ (Python)
└─────────────────┘

Single trace spans all services, showing end-to-end latency.
```

### Log Correlation with Tracing

Inject trace ID into logs for cross-referencing.

```java
// MDC-based correlation
import org.slf4j.MDC;
import io.opentelemetry.api.trace.SpanId;
import io.opentelemetry.api.trace.TraceId;

@Component
public class TraceContextFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                  HttpServletResponse response,
                                  FilterChain chain) throws Exception {
        Span span = Span.current();
        if (span != null) {
            MDC.put("traceId", span.getSpanContext().getTraceId());
            MDC.put("spanId", span.getSpanContext().getSpanId());
        }

        try {
            chain.doFilter(request, response);
        } finally {
            MDC.remove("traceId");
            MDC.remove("spanId");
        }
    }
}

// Logs include trace ID in JSON output
log.info("api_request", endpoint="/api/users", traceId=MDC.get("traceId"));
```

## Pre-Deployment Checklist

Before ANY production deployment:

### Logging
- [ ] Structured logging format (JSON) configured
- [ ] Log levels set appropriately (INFO in production)
- [ ] Correlation ID propagation across services
- [ ] Sensitive data redaction implemented (passwords, tokens, PII)
- [ ] Log aggregation configured (ELK, CloudWatch, Datadog)
- [ ] Log retention policy configured (90 days minimum for compliance)
- [ ] No console.log or print statements in production code

### Metrics
- [ ] Infrastructure metrics (CPU, memory, disk, network)
- [ ] Business metrics instrumented (orders, signups, conversion rate)
- [ ] Metric naming conventions followed
- [ ] Cardinality managed properly (no high-cardinality tags)
- [ ] Histograms/buckets configured for latency (P50, P90, P99)
- [ ] Metrics endpoint exposed (/metrics for Prometheus)
- [ ] Metrics collection configured (Datadog Agent, Prometheus)

### Tracing
- [ ] All services instrumented with OpenTelemetry
- [ ] Trace context propagated across service boundaries
- [ ] Appropriate sampling configured (10% sample rate for high-traffic)
- [ ] Span names follow conventions (e.g., "http.request", "db.query")
- [ ] Spans include relevant attributes (user.id, service.name, error.type)
- [ ] Errors recorded in spans with stack traces
- [ ] Tracing backend configured (Jaeger, Tempo, Datadog APM)

### Alerting
- [ ] Critical alerts defined (P0 - service down, data loss, security)
- [ ] High-priority alerts defined (P1 - major functionality, SLA violations)
- [ ] On-call rotation configured
- [ ] Escalation paths defined (15m, 30m, 45m)
- [ ] Alert routing configured (oncall, Slack, PagerDuty)
- [ ] Suppression rules for expected events (deployments, maintenance)
- [ ] SLO/SLA alerting configured (error budget burn rate)
- [ ] Runbook documentation available

### General
- [ ] Observability dashboard created (Grafana, Datadog)
- [ ] SLOs defined and monitored
- [ ] Error budget calculation configured
- [ ] Observability tested in staging environment
- [ ] Runbook created for common incidents
- [ ] Postmortem process defined

## Verification Checklist

When debugging production issues:

- [ ] Check logs for correlation ID matching the incident
- [ ] Review metrics at time of incident (CPU, memory, error rate, latency)
- [ ] Examine trace spanning affected services
- [ ] Identify the component or service where failure originated
- [ ] Verify if failure correlation exists with recent deployments
- [ ] Check alert history (were there prior warnings?)
- [ ] Review configuration changes (feature flags, environment variables)
- [ ] Verify external dependencies status (third-party APIs, database, cache)
- [ ] Load test scenario to reproduce issue in controlled environment

## Common Mistakes

- **Over-logging without sampling** → High costs, log noise, slower storage queries
- **Missing correlation IDs** → Impossible to trace requests across services
- **High-cardinality metrics** → Database performance issues, memory bloat
- **Alerting on everything** → Alert fatigue, ignored real incidents
- **No sensitive data redaction** → Security compliance violations
- **No sampling for traces** → Unnecessary costs for high-traffic systems
- **Missing context in logs** → "log.info('error')" provides no actionable information
- **Unstructured logs** → Cannot query, parse, or extract insights
- **Single metric per alert** → May cause false positives without composite conditions

## Red Flags

- **"Can't reproduce in dev"** → Add production instrumentation, log levels, trace sampling
- **"Guessing without data"** → Use systematic-debugging to gather evidence
- **"We'll monitor later"** → Instrument before deploy, create logs/metrics/traces first
- **"High alert volume"** → Tune thresholds, add suppression, adjust priorities
- **"Logs are unstructured text"** → Convert to JSON, add structured fields
- **"Metrics exploding"** → Check cardinality, remove high-cardinality tags
- **"Traces too expensive"** → Adjust sampling rate, filter unnecessary spans
- **"Alert fatigue"** → Reduce alert count, increase threshold severity

## Rationalizations Table

| Excuse | Reality |
|--------|---------|
| "Too busy for monitoring" | Unmonitored code causes MTTR to increase 3-5x |
| "Simple feature, no need" | Simple code fails - observability takes minutes |
| "We'll add later" | Retroactive instrumenting misses initial failures |
| "Console.log is enough" | Unstructured logs impossible to query or alert |
| "We have infrastructure alerts" | Business metrics required for feature health |
| "Tracing is expensive" | Proper sampling reduces costs by 90%+ |
| "Logs consume too much storage" | Structured logs + sampling = efficient storage |
| "Alert on everything is safer" | Alert fatigue causes real issues to be ignored |

## Real-World Impact

- **MTTR Reduction**: Proper observability reduces mean time to resolve by 60-80%
- **Debugging Speed**: Correlation IDs enable root cause identification in minutes vs hours
- **Performance**: Latency issues identified before SLA violations
- **Capacity**: Proactive capacity planning based on metric trends
- **Cost**: Structured logs + sampling reduce storage costs by 70-90%

## Pair With Other Skills

- **systematic-debugging** - For analyzing production issues with observability data
- **test-driven-development** - For writing tests for instrumentation code
- **security-review** - Ensure observability doesn't leak sensitive data

---

**Remember**: Observability is not optional. You cannot improve or fix what you cannot see. Production systems without observability are black boxes that inevitably fail unpredictably.
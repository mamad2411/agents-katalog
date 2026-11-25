---
name: "resilience-patterns"
description: "Resilience patterns with code: Resilience4j circuit breakers and semaphore bulkheads, exponential backoff with full jitter, cascading timeout budgets, health check endpoints, and anti-patterns such as retrying non-idempotent calls. Use when hardening calls to downstream services."
---

# Resilience Patterns

> Named patterns with code examples for circuit breakers (Resilience4j), bulkhead isolation, exponential backoff with jitter, timeout budgets, fallback hierarchies, and health endpoint design.

## Patterns

### Pattern: Resilience4j Circuit Breaker (Java)

Complete configuration for a circuit breaker protecting a downstream REST service:

```java
// Full Resilience4j setup with circuit breaker + retry + bulkhead
@Configuration
public class ResilienceConfig {

    @Bean
    public CircuitBreakerRegistry circuitBreakerRegistry() {
        CircuitBreakerConfig config = CircuitBreakerConfig.custom()
            // Sliding window: evaluate based on last 10 calls
            .slidingWindowType(SlidingWindowType.COUNT_BASED)
            .slidingWindowSize(10)
            // Open circuit when 50% of calls fail
            .failureRateThreshold(50.0f)
            // ALSO open when 80% of calls are slow (important!)
            .slowCallRateThreshold(80.0f)
            .slowCallDurationThreshold(Duration.ofSeconds(2))
            // Stay open for 30 seconds before probing
            .waitDurationInOpenState(Duration.ofSeconds(30))
            // Probe with 3 calls in half-open state
            .permittedNumberOfCallsInHalfOpenState(3)
            // Need at least 5 calls before evaluating
            .minimumNumberOfCalls(5)
            // Automatically transition to half-open after wait duration
            .automaticTransitionFromOpenToHalfOpenEnabled(true)
            // Count these as failures
            .recordExceptions(IOException.class, TimeoutException.class,
                              HttpServerErrorException.class)
            // Business exceptions are NOT circuit-breaking failures
            .ignoreExceptions(OrderNotFoundException.class,
                              ValidationException.class)
            .build();

        return CircuitBreakerRegistry.of(config);
    }

    @Bean
    public RetryRegistry retryRegistry() {
        RetryConfig retryConfig = RetryConfig.custom()
            .maxAttempts(3)
            .intervalFunction(IntervalFunction.ofExponentialRandomBackoff(
                200,   // initial wait ms
                2.0,   // multiplier
                0.5,   // randomization factor (±50%)
                2000   // max wait ms
            ))
            .retryOnException(ex ->
                ex instanceof IOException ||
                ex instanceof TimeoutException)
            .retryOnResult(response ->
                response instanceof HttpResponse &&
                ((HttpResponse) response).getStatusCode() == 503)
            .build();

        return RetryRegistry.of(retryConfig);
    }
}

// Usage: circuit breaker + retry + fallback composed together
@Service
public class OrderServiceClient {
    private final CircuitBreaker circuitBreaker;
    private final Retry retry;
    private final OrderCacheService cache;

    public Order getOrder(String orderId) {
        Supplier<Order> call = () -> httpClient.get("/orders/" + orderId, Order.class);

        // Chain: retry → circuit breaker → actual call
        Supplier<Order> decorated = Decorators.ofSupplier(call)
            .withCircuitBreaker(circuitBreaker)
            .withRetry(retry)
            .withFallback(
                List.of(CallNotPermittedException.class, MaxRetriesExceededException.class),
                ex -> {
                    log.warn("Circuit open or retries exhausted for order {}", orderId);
                    return cache.getLastKnown(orderId)  // Fallback to cache
                        .orElseThrow(() -> new ServiceUnavailableException("order-service"));
                }
            )
            .decorate();

        return decorated.get();
    }
}
```

### Pattern: Bulkhead with Semaphore (Resilience4j)

Limit concurrent calls to a slow dependency without impacting other dependencies:

```java
// Each downstream service gets its own bulkhead
@Bean
public BulkheadRegistry bulkheadRegistry() {
    // Payment service: expensive, limited concurrency
    BulkheadConfig paymentConfig = BulkheadConfig.custom()
        .maxConcurrentCalls(10)
        .maxWaitDuration(Duration.ofMillis(50))  // fail fast if all slots busy
        .build();

    // Recommendation service: best-effort, more permissive
    BulkheadConfig recommendationConfig = BulkheadConfig.custom()
        .maxConcurrentCalls(50)
        .maxWaitDuration(Duration.ofMillis(0))  // instant failure if full
        .build();

    BulkheadRegistry registry = BulkheadRegistry.ofDefaults();
    registry.bulkhead("payment-service", paymentConfig);
    registry.bulkhead("recommendation-service", recommendationConfig);
    return registry;
}
```

### Pattern: Exponential Backoff with Full Jitter

Marc Brooker (AWS, 2015) showed that "full jitter" produces the best collective retry behavior — lowest retry collisions, fastest recovery for the aggregate system:

```python
import random
import time
import math

def retry_with_full_jitter(fn, max_attempts=5, base_delay=0.1, max_delay=30.0):
    """
    Full jitter: sleep = random(0, min(cap, base * 2^attempt))
    Best for reducing thundering herd on shared resources.
    """
    last_exception = None
    for attempt in range(max_attempts):
        try:
            return fn()
        except (IOError, TimeoutError) as e:
            last_exception = e
            if attempt == max_attempts - 1:
                raise

            # Full jitter — spread retries across the entire backoff window
            cap = min(max_delay, base_delay * (2 ** attempt))
            sleep = random.uniform(0, cap)

            print(f"Attempt {attempt+1} failed: {e}. Retrying in {sleep:.2f}s...")
            time.sleep(sleep)

    raise last_exception
```

### Pattern: Cascading Timeout Budget

When A calls B calls C, each level must budget the total time available:

```
User ──► Service A (SLA: 500ms)
           ├─ Local processing: 50ms
           └─► Service B (budget: 400ms)
                   ├─ Local processing: 30ms
                   ├─► Service C (budget: 300ms)
                   └─► Database (budget: 300ms, parallel)
```

```java
// Propagate deadline via gRPC context or HTTP header
// Service A sends its remaining deadline to Service B
public Order processOrder(String orderId, long deadlineMs) {
    long remaining = deadlineMs - System.currentTimeMillis();
    if (remaining < 100) {  // Not enough time — fail fast
        throw new DeadlineExceededException("Insufficient time budget: " + remaining + "ms");
    }

    // Call downstream with reduced budget (subtract local processing margin)
    long downstreamBudget = remaining - 50;  // 50ms for our own processing
    return orderServiceClient.getOrder(orderId, downstreamBudget);
}
```

### Pattern: Health Check Endpoint

Kubernetes-compatible liveness and readiness probes:

```typescript
// Express.js health endpoints
import { Router } from 'express';
import { pool } from './db';
import { redis } from './cache';

const health = Router();

// Liveness: is the process alive? Restarted if this fails.
// Should be fast and never fail unless process is truly dead.
health.get('/health/live', (req, res) => {
  res.json({ status: 'alive', uptime: process.uptime() });
});

// Readiness: is the service ready to serve traffic?
// Removed from load balancer rotation if this fails.
health.get('/health/ready', async (req, res) => {
  const checks: Record<string, string> = {};
  let healthy = true;

  // Check database
  try {
    await pool.query('SELECT 1');
    checks.database = 'ok';
  } catch (e) {
    checks.database = 'error';
    healthy = false;
  }

  // Check Redis
  try {
    await redis.ping();
    checks.cache = 'ok';
  } catch (e) {
    checks.cache = 'degraded';  // Not blocking — service can run without cache
  }

  const status = healthy ? 200 : 503;
  res.status(status).json({
    status: healthy ? 'ready' : 'not_ready',
    checks,
    timestamp: new Date().toISOString(),
  });
});

export default health;
```

Kubernetes deployment configuration:
```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 2
```

## Anti-Patterns

### Anti-Pattern: Circuit Breaker Without Fallback (Cascading Failure)

Wrapping a call in a circuit breaker but throwing an exception when the circuit opens. The caller propagates the exception up. The upstream caller propagates it further. Entire request path fails when the circuit opens — defeating the purpose.

A circuit breaker without a fallback is better than no circuit breaker (it prevents thread exhaustion), but it does not provide graceful degradation. Always design the fallback first.

### Anti-Pattern: Retrying Non-Idempotent Operations

A payment service call times out. The retry sends the payment request again. Both calls succeed. Customer is charged twice.

Rule: Only retry operations that are idempotent. For non-idempotent operations (payments, order creation), use idempotency keys. The server deduplicates based on the key.

```http
POST /payments
Idempotency-Key: order:42:attempt:1
Content-Type: application/json

{"amount": 99.99, "currency": "USD", "method": "card"}
```

### Anti-Pattern: Infinite or Missing Timeout

```java
// No timeout set — connection can hang indefinitely
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
// conn.setConnectTimeout(???);  // Not set!
// conn.setReadTimeout(???);     // Not set!
InputStream in = conn.getInputStream();  // Can block forever
```

A thread blocked on a network call with no timeout is a permanently leaked resource. One leaked thread is acceptable. One hundred threads all hanging on the same slow downstream service is an outage.

Rule: Every remote call must have an explicit timeout. Default framework timeouts (often "infinity" or very large values) are not acceptable.

### Anti-Pattern: Treating All Exceptions as Circuit-Breaking

A circuit breaker opens when a user submits invalid input (400 Bad Request) or requests a resource that does not exist (404). These are not infrastructure failures — they are business errors that the service correctly handles. The circuit opens when 50% of calls return 404 because the client is sending bad IDs.

Rule: Configure `ignoreExceptions` or `ignoreExceptionPredicate` for business exceptions. Only infrastructure exceptions (5xx, timeouts, connection refused, network errors) should count toward the failure rate.

### Anti-Pattern: Shared Thread Pool Across Dependencies

All outbound HTTP calls share a single `ExecutorService` with 100 threads. When the payment service becomes slow, all 100 threads fill up waiting for payment responses. Calls to inventory service, product service, and user service all queue behind payment service calls. Total system failure from a single slow dependency.

This is the specific problem Hystrix was designed to solve. The solution is per-dependency thread pools (Hystrix) or per-dependency semaphore limits (Resilience4j Bulkhead). Bulkhead ensures that even if the payment service consumes all 10 of its allocated slots, the other 90 threads remain available for other dependencies.

## References

- Nygard, Michael. _Release It!_ 2nd ed. Pragmatic Programmers, 2018.
- Resilience4j documentation: resilience4j.readme.io.
- Netflix Tech Blog: "Making Netflix API More Resilient." 2012.
- Brooker, Marc. "Exponential Backoff and Jitter." AWS Architecture Blog, 2015. aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter.
- Polly (.NET): github.com/App-vNext/Polly.

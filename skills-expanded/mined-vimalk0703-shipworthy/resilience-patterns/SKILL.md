---
name: resilience-patterns
description: Apply resilience patterns (circuit breakers, bulkheads, retries, timeouts, graceful degradation, DLQs) to distributed services to prevent cascading failures and maintain availability under partial outages.
invoke_when: Use when designing or reviewing systems that call external services, databases, or message queues, or when discussing reliability, fault tolerance, cascading failures, or service availability.
---

# Resilience Patterns

## Core Principle

Every external call will eventually fail. Resilience is not about preventing failure -- it is about controlling the blast radius and recovering quickly.

---

## 1. Circuit Breaker

**What it does:** Stops calling a failing downstream service, giving it time to recover instead of overwhelming it with doomed requests.

**States:** CLOSED (normal) -> OPEN (failing, reject calls) -> HALF-OPEN (test with limited traffic).

**When to apply:** Any synchronous call to an external service, database, or third-party API.

### TypeScript Example (using cockatiel)

```typescript
import { CircuitBreakerPolicy, SamplingBreaker, handleAll } from 'cockatiel';

const breaker = new CircuitBreakerPolicy(handleAll, {
  halfOpenAfter: 10_000,       // Try again after 10s
  breaker: new SamplingBreaker({
    threshold: 0.5,            // Open when 50% of requests fail
    duration: 30_000,          // Over a 30s window
    minimumRps: 5,             // Need at least 5 req/s to evaluate
  }),
});

breaker.onBreak(() => console.warn('Circuit OPEN -- downstream is failing'));
breaker.onHalfOpen(() => console.info('Circuit HALF-OPEN -- testing downstream'));
breaker.onReset(() => console.info('Circuit CLOSED -- downstream recovered'));

const result = await breaker.execute(() => callDownstreamService());
```

### Python Example

```python
import circuitbreaker

@circuitbreaker.circuit(failure_threshold=5, recovery_timeout=30)
def call_downstream_service():
    response = requests.get("https://api.partner.com/data", timeout=5)
    response.raise_for_status()
    return response.json()

# Usage with fallback
try:
    data = call_downstream_service()
except circuitbreaker.CircuitBreakerError:
    data = get_cached_or_default_data()
```

---

## 2. Bulkhead

**What it does:** Isolates failures by partitioning resources (thread pools, connection pools, rate limits) so one failing dependency cannot exhaust resources needed by others.

**When to apply:** A service calls multiple downstream dependencies and you need to prevent one slow dependency from starving others.

### Implementation Guidance

- Use separate HTTP client instances (with their own connection pools) per downstream service.
- Set max concurrency per dependency.
- In Kubernetes, use separate deployments for critical vs. non-critical workloads.

```typescript
// Separate HTTP clients per dependency -- each with its own connection pool
const paymentClient = axios.create({
  baseURL: 'https://payments.internal',
  timeout: 3000,
  maxSockets: 20,  // Bulkhead: max 20 concurrent connections
});

const notificationClient = axios.create({
  baseURL: 'https://notifications.internal',
  timeout: 5000,
  maxSockets: 10,  // Bulkhead: max 10 concurrent connections
});
```

---

## 3. Retry with Exponential Backoff + Jitter

**What it does:** Retries transient failures with increasing delays, adding randomness to prevent thundering herd.

**When to apply:** Network timeouts, HTTP 429/503 responses, transient database errors. Never retry non-idempotent operations unless you have idempotency keys.

### TypeScript Example

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelayMs: number = 200,
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries || !isRetryable(error)) throw error;
      const delay = baseDelayMs * Math.pow(2, attempt);
      const jitter = delay * 0.5 * Math.random();  // Add up to 50% jitter
      await sleep(delay + jitter);
    }
  }
  throw new Error('Unreachable');
}

function isRetryable(error: unknown): boolean {
  if (error instanceof HttpError) {
    return [408, 429, 500, 502, 503, 504].includes(error.status);
  }
  return error instanceof NetworkError;
}
```

### Python Example

```python
import random
import time
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=0.2, retryable_exceptions=(IOError,)):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return fn(*args, **kwargs)
                except retryable_exceptions as e:
                    if attempt == max_retries:
                        raise
                    delay = base_delay * (2 ** attempt)
                    jitter = delay * 0.5 * random.random()
                    time.sleep(delay + jitter)
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3, retryable_exceptions=(requests.ConnectionError, requests.Timeout))
def fetch_user_profile(user_id: str) -> dict:
    resp = requests.get(f"https://api.users.internal/v1/users/{user_id}", timeout=3)
    resp.raise_for_status()
    return resp.json()
```

---

## 4. Timeout Budgets

**What it does:** Sets a total time budget for an operation that spans multiple downstream calls. Each subsequent call gets whatever time remains, preventing slow cascading chains.

**When to apply:** Any request that fans out to multiple services or makes sequential downstream calls.

### Implementation

```typescript
class TimeoutBudget {
  private readonly deadline: number;

  constructor(totalMs: number) {
    this.deadline = Date.now() + totalMs;
  }

  remaining(): number {
    return Math.max(0, this.deadline - Date.now());
  }

  expired(): boolean {
    return this.remaining() <= 0;
  }
}

// Usage in a request handler
async function handleRequest(req: Request): Promise<Response> {
  const budget = new TimeoutBudget(3000); // 3s total budget

  const user = await fetchUser(req.userId, budget.remaining());
  if (budget.expired()) return fallbackResponse();

  const orders = await fetchOrders(user.id, budget.remaining());
  if (budget.expired()) return partialResponse(user);

  return fullResponse(user, orders);
}
```

**Rules:**
- Set the overall budget at the API gateway or entry point.
- Pass remaining budget as a `grpc-timeout` header or custom header to downstream services.
- Each downstream service should respect the budget and return partial results rather than timing out silently.

---

## 5. Graceful Degradation

**What it does:** Returns reduced functionality instead of a complete failure when a non-critical dependency is down.

**When to apply:** Features that have optional enrichments (recommendations, personalization, analytics) that are not essential to the core user flow.

### Strategy

1. Classify every dependency as **critical** or **non-critical**.
2. For non-critical dependencies: catch errors, log them, return defaults.
3. For critical dependencies: apply circuit breaker + retry, fail fast if unavailable.

```typescript
async function getProductPage(productId: string): Promise<ProductPage> {
  // Critical -- fail the request if this fails
  const product = await productService.getProduct(productId);

  // Non-critical -- degrade gracefully
  const recommendations = await recommendationService
    .getRecommendations(productId)
    .catch(() => []);  // Empty recommendations are acceptable

  const reviews = await reviewService
    .getReviews(productId)
    .catch(() => ({ items: [], averageRating: null }));  // No reviews is acceptable

  return { product, recommendations, reviews };
}
```

---

## 6. Dead Letter Queues (DLQ)

**What it does:** Captures messages that fail processing after all retries, preventing message loss and queue poisoning.

**When to apply:** Any async message processing (SQS, Kafka, RabbitMQ). Every production queue must have a DLQ.

### Configuration Rules

- Set max receive count to 3-5 before sending to DLQ.
- Set DLQ retention period to 14 days (enough time to investigate and replay).
- Monitor DLQ depth with alerts -- any message in a DLQ means something is broken.
- Build a replay mechanism to reprocess DLQ messages after fixing the bug.

```python
# AWS CDK example
from aws_cdk import aws_sqs as sqs

dlq = sqs.Queue(self, "OrderProcessingDLQ",
    retention_period=Duration.days(14),
    queue_name="order-processing-dlq",
)

main_queue = sqs.Queue(self, "OrderProcessingQueue",
    queue_name="order-processing",
    dead_letter_queue=sqs.DeadLetterQueue(
        max_receive_count=3,
        queue=dlq,
    ),
    visibility_timeout=Duration.seconds(60),
)
```

---

## Decision Table: When to Apply Each Pattern

| Scenario | Circuit Breaker | Bulkhead | Retry | Timeout Budget | Graceful Degradation | DLQ |
|---|---|---|---|---|---|---|
| Single external API call | Yes | - | Yes | - | If non-critical | - |
| Fan-out to multiple services | Yes | Yes | Selective | Yes | Yes | - |
| Async message processing | - | - | Yes (built-in) | - | - | Yes |
| Database calls | Yes | Yes (pool) | Transient only | Yes | - | - |
| Third-party payment API | Yes | Yes | Idempotent only | Yes | No (critical) | - |
| Recommendation engine | Yes | - | Once | Yes | Yes (return empty) | - |
| Event-driven pipeline | - | - | Yes | - | - | Yes |

## Checklist Before Shipping

- [ ] Every synchronous external call has a timeout set (never use default/infinite).
- [ ] Retries use exponential backoff with jitter, not fixed delays.
- [ ] Non-idempotent operations are not retried (or use idempotency keys).
- [ ] Circuit breakers are configured with sensible thresholds tuned to traffic volume.
- [ ] Non-critical dependencies degrade gracefully instead of failing the whole request.
- [ ] Every message queue has a DLQ configured.
- [ ] DLQ depth is monitored and alerted on.
- [ ] Timeout budgets propagate through the call chain.

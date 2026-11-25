---
name: error-handling-patterns
description: >-
  Cross-language error handling patterns for distributed systems. Covers retry
  with exponential backoff, circuit breaker, dead-letter handling, compensation
  (saga), idempotency, and poison message management.
when-to-use: >-
  Invoke when designing error handling for distributed systems, implementing
  retry logic, configuring circuit breakers, handling message queue failures,
  or building resilient integration flows across Azure services.
categories:
  - architecture
  - resilience
  - integration
  - error-handling
---

# Error Handling Patterns

At-least-once delivery is the norm in distributed systems. Every operation that will be retried MUST be idempotent. Every integration boundary needs explicit failure handling.

## Pattern Decision Tree

```
Operation failed — what now?
├─ Transient error (429, 503, timeout)?
│   ├─ Yes → Retry with exponential backoff + jitter
│   │   └─ Retries exhausted? → Circuit breaker / dead-letter
│   └─ No (400, 404, permanent) → Don't retry → dead-letter / alert
├─ Downstream slow/failing repeatedly?
│   └─ Circuit breaker → fast-fail, protect upstream
├─ Multi-step distributed transaction?
│   └─ Saga pattern → compensating actions for each step
└─ Message fails processing repeatedly?
    └─ Poison message → isolate, dead-letter, investigate
```

---

## Retry with Exponential Backoff

Retry transient failures. Never retry permanent failures.

### Retry Only These

| Status | Meaning | Retry? |
|---|---|---|
| 429 | Throttled | Yes — respect `Retry-After` header |
| 500 | Internal Server Error | Yes — may be transient |
| 503 | Service Unavailable | Yes — service recovering |
| Timeout | No response | Yes — network/service issue |
| 400 | Bad Request | **No** — fix the request |
| 401/403 | Auth failure | **No** — fix credentials |
| 404 | Not Found | **No** — resource doesn't exist |

### Implementation

```
Attempt 1: wait 1s
Attempt 2: wait 2s + jitter
Attempt 3: wait 4s + jitter
Attempt 4: wait 8s + jitter (cap at max delay)
```

**Add jitter** to prevent thundering herd on recovery. Random ±25% of delay.

### Azure Service Defaults

| Service | Default Retry | Configurable |
|---|---|---|
| Logic Apps | Exponential (4 retries, 7.5s intervals) | Yes: None, Fixed, Exponential per action |
| Service Bus SDK | Exponential backoff | Yes: RetryOptions in client config |
| Event Grid | Exponential (30 attempts, 24h) | Yes: maxDeliveryAttempts, TTL |
| APIM | None (fails fast) | Yes: `<retry>` policy |
| Functions | Depends on trigger binding | Yes: host.json |

---

## Circuit Breaker

Prevent cascading failures by stopping calls to failing downstream services.

### States

```
Closed (normal) → failures exceed threshold → Open (failing)
                                                  │
                                            timer expires
                                                  │
                                            Half-Open (testing)
                                            │           │
                                        success      failure
                                            │           │
                                        → Closed    → Open
```

- **Closed**: Requests flow. Failures counted.
- **Open**: Requests immediately rejected (fast-fail). Timer-based recovery.
- **Half-Open**: Limited requests test recovery. Success → Closed. Failure → Open.

### Implementation Options

| Platform | How |
|---|---|
| APIM | Backend circuit breaker config (trip on 5xx count/percentage) |
| .NET | Polly `CircuitBreakerPolicy` |
| Python | tenacity or pybreaker |
| Service Bus | Natural circuit breaking via dead-letter + MaxDeliveryCount |

---

## Dead-Letter Handling

Every queue and event subscription needs dead-letter monitoring.

- [ ] Alert on DLQ count > 0 — every dead letter is a failed integration
- [ ] Build automated DLQ processor for inspect → fix → resubmit
- [ ] Route unfixable messages to investigation queue
- [ ] Set retention policy — don't let DLQ grow unbounded
- [ ] Treat dead letters as symptoms — find and fix the root cause

---

## Compensation (Saga Pattern)

For distributed transactions without distributed locks.

### Orchestration (Logic Apps / Durable Functions)
- Central coordinator directs each step and handles failures
- Calls compensating actions when a step fails
- Easier to understand, test, and monitor
- Single point of failure

### Choreography (Event-Driven)
- Each service emits events, next service reacts
- No central coordinator — more resilient, harder to debug
- Event Grid + Service Bus naturally support this

### Rules
- Every step has a defined compensating action
- Compensating actions must also be idempotent
- Log every step and compensation for audit trail

---

## Idempotency

| Strategy | Description | Best For |
|---|---|---|
| Check-before-write | DB lookup before insert | Simple CRUD |
| Deduplication table | Store processed message IDs | High-throughput messaging |
| Natural idempotency | Upsert instead of insert | Database writes |
| Conditional write | ETag/version-based updates | Concurrent access |
| Service Bus deduplication | MessageId-based (time window) | Publisher-side duplicates |

Consumer-side idempotency is ALWAYS the consumer's responsibility, regardless of transport-level deduplication.

---

## Poison Messages

Messages that repeatedly fail processing despite retries.

- Delivery count increments each attempt → after `MaxDeliveryCount` → DLQ
- Isolate in separate poison message queue for investigation
- Root causes: schema mismatches, corrupt data, missing dependencies
- Prevention: validate message schema on receive, dead-letter known-bad formats explicitly

---

## Monitoring Checklist

| Metric | Alert Threshold | Service |
|---|---|---|
| Dead-letter queue depth | > 0 | Service Bus |
| Active message count (growing) | Trend increasing | Service Bus |
| Message age (oldest in queue) | > acceptable latency | Service Bus |
| Delivery failure rate | > 1% | Event Grid |
| Failed workflow runs | > 0 | Logic Apps |
| Backend error rate (5xx) | > threshold | APIM |
| Circuit breaker state | Open | APIM / Application |
| Throttled requests (429) | > 0 | All services |

---

## PowerShell Retry Pattern

```powershell
function Invoke-WithRetry {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [scriptblock]$ScriptBlock,
        [int]$MaxRetries = 3,
        [int]$BaseDelaySeconds = 2
    )
    $attempt = 0
    do {
        $attempt++
        try {
            return & $ScriptBlock
        }
        catch {
            if ($attempt -ge $MaxRetries) { throw }
            $delay = $BaseDelaySeconds * [math]::Pow(2, $attempt - 1)
            Write-Warning "Attempt $attempt failed: $($_.Exception.Message). Retrying in ${delay}s..."
            Start-Sleep -Seconds $delay
        }
    } while ($attempt -lt $MaxRetries)
}
```

## Related Skills

- `api-design-standards` — API error response format and status code mapping
- `observability-baseline` — Monitoring and alerting for failure patterns

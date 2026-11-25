---
name: "Error Recovery Orchestrator"
version: "1.0.0"
description: "Orchestrates error recovery with circuit breakers, retry policies, fallback chains, and graceful degradation."
author: "workspace"
activated: false
---

# Error Recovery Orchestrator

Orchestrates error recovery with circuit breakers, retry policies, fallback chains, and graceful degradation.

## Decision Framework

### When to Apply
Use when: Distributed systems, critical operations needing reliability, external API integrations, payment processing

### When NOT to Apply
Don't use when: Simple try/catch sufficient, non-critical operations

## Anti-Patterns

### 1. No Retry Limits
```javascript
// BAD: Infinite retry
while (true) { await retry(); }

// GOOD: Bounded retry with backoff
for (let i = 0; i < maxRetries; i++) {
  try { return await operation(); }
  catch (e) { await sleep(Math.pow(2, i) * 1000); }
}
```

### 2. Swallowing Errors
```javascript
// BAD: Silent failure
catch (e) { }

// GOOD: Log and handle
catch (e) { logger.error('Operation failed', { error: e }); throw e; }
```


## Trigger Phrases

- "Error handling"
- "Retry logic"
- "Circuit breaker"
- "Fallback strategy"
- "Graceful degradation"

## Patterns

### Circuit Breaker
```javascript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.threshold = threshold;
    this.timeout = timeout;
    this.failures = 0;
    this.state = 'CLOSED';
    this.nextAttempt = 0;
  }

  async execute(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) throw new Error('Circuit is OPEN');
      this.state = 'HALF_OPEN';
    }
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() { this.failures = 0; this.state = 'CLOSED'; }
  onFailure() {
    this.failures++;
    if (this.failures >= this.threshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.timeout;
    }
  }
}
```

### Fallback Chain
```javascript
async function withFallbacks(operations) {
  for (const op of operations) {
    try { return await op(); }
    catch (e) { logger.warn('Fallback attempt failed', { error: e.message }); }
  }
  throw new Error('All fallbacks exhausted');
}
```


## Error Classification

| Category | Recoverable | Retry | Example |
|----------|-------------|-------|---------|
| Network | Yes | Yes | Timeout, connection reset |
| Auth | Sometimes | No | 401 Unauthorized |
| Validation | No | No | 400 Bad Request |
| Rate Limit | Yes | Yes (with backoff) | 429 Too Many Requests |
| Server | Yes | Yes | 500 Internal Server Error |
| Client | No | No | 404 Not Found |

## Integration
- Works with: api-integration-layer, deployment-pipeline-architect, data-migration-orchestrator


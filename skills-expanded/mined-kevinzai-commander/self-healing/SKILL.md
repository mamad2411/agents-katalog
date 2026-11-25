---
name: self-healing
description: "Self-healing system patterns — circuit breakers, auto-restart, error budgets, graceful degradation, and auto-recovery"
version: 1.0.0
category: architecture
---

# Self-Healing Systems

Build systems that detect failures and recover automatically without human intervention.

## Core Patterns

### 1. Circuit Breaker

Prevent cascading failures by failing fast when a dependency is down.

```typescript
class CircuitBreaker {
  private failures = 0;
  private lastFailure = 0;
  private state: 'closed' | 'open' | 'half-open' = 'closed';

  constructor(
    private readonly threshold: number = 5,
    private readonly resetTimeout: number = 30_000,
  ) {}

  async call<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      if (Date.now() - this.lastFailure > this.resetTimeout) {
        this.state = 'half-open';
      } else {
        throw new Error('Circuit breaker is open');
      }
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

  private onSuccess() {
    this.failures = 0;
    this.state = 'closed';
  }

  private onFailure() {
    this.failures++;
    this.lastFailure = Date.now();
    if (this.failures >= this.threshold) {
      this.state = 'open';
    }
  }
}
```

### 2. Health Check Endpoints

```typescript
// Layered health checks
app.get('/health', async () => ({ status: 'ok' }));          // Shallow — always fast
app.get('/health/ready', async () => {                        // Deep — checks dependencies
  const checks = await Promise.allSettled([
    checkDatabase(),
    checkRedis(),
    checkExternalAPI(),
  ]);
  const unhealthy = checks.filter(c => c.status === 'rejected');
  return {
    status: unhealthy.length === 0 ? 'ready' : 'degraded',
    checks: Object.fromEntries(
      checks.map((c, i) => [['db', 'redis', 'api'][i], c.status])
    ),
  };
});
```

### 3. Auto-Restart with Backoff

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 1000,
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;
      const delay = baseDelay * Math.pow(2, attempt) + Math.random() * 1000;
      await new Promise(r => setTimeout(r, delay));
    }
  }
  throw new Error('Unreachable');
}
```

### 4. Graceful Degradation

```typescript
// Feature degradation tiers
const DEGRADATION_TIERS = {
  healthy: ['full-search', 'recommendations', 'analytics', 'notifications'],
  degraded: ['full-search', 'recommendations'],  // drop non-critical
  critical: ['basic-search'],                      // minimal functionality
} as const;

function getAvailableFeatures(healthScore: number) {
  if (healthScore > 80) return DEGRADATION_TIERS.healthy;
  if (healthScore > 40) return DEGRADATION_TIERS.degraded;
  return DEGRADATION_TIERS.critical;
}
```

### 5. Error Budget Tracking

```typescript
interface ErrorBudget {
  windowMs: number;      // 30 days
  targetSLO: number;     // 99.9%
  totalRequests: number;
  failedRequests: number;
}

function checkErrorBudget(budget: ErrorBudget): {
  remaining: number;
  burnRate: number;
  alert: boolean;
} {
  const allowedFailures = budget.totalRequests * (1 - budget.targetSLO);
  const remaining = Math.max(0, allowedFailures - budget.failedRequests);
  const burnRate = budget.failedRequests / allowedFailures;
  return {
    remaining,
    burnRate,
    alert: burnRate > 0.8,  // Alert at 80% budget consumed
  };
}
```

### 6. Self-Healing Database Connections

```typescript
// Connection pool with automatic reconnection
function createResilientPool(config: PoolConfig) {
  const pool = new Pool(config);

  pool.on('error', async (err) => {
    console.error('Pool error, attempting recovery:', err.message);
    try {
      await pool.end();
      await new Promise(r => setTimeout(r, 5000));
      // Pool auto-reconnects on next query
    } catch (recoveryErr) {
      console.error('Recovery failed:', recoveryErr);
      process.exit(1); // Let process manager restart
    }
  });

  return pool;
}
```

### 7. Memory Leak Detection

```typescript
// Periodic memory check with auto-restart trigger
function monitorMemory(thresholdMB = 512, checkIntervalMs = 60_000) {
  setInterval(() => {
    const usage = process.memoryUsage();
    const heapMB = usage.heapUsed / 1024 / 1024;

    if (heapMB > thresholdMB) {
      console.error(`Memory threshold exceeded: ${heapMB.toFixed(0)}MB > ${thresholdMB}MB`);
      // Graceful shutdown — let process manager restart
      process.emit('SIGTERM');
    }
  }, checkIntervalMs);
}
```

## Implementation Checklist

- [ ] Circuit breakers on all external service calls
- [ ] Health check endpoint (shallow + deep)
- [ ] Retry with exponential backoff on transient failures
- [ ] Graceful degradation tiers defined
- [ ] Error budget tracking for SLO monitoring
- [ ] Database connection pool with auto-reconnect
- [ ] Memory monitoring with threshold alerts
- [ ] Process manager (PM2/systemd) configured for auto-restart
- [ ] Structured logging for failure analysis
- [ ] Alerting on error budget burn rate

---
name: self-healing-mindset
description: Use this skill when designing resilient code, systems, or AI agents that recover from failure automatically. Also use for proactive resilience thinking — pre-mortems, failure mode analysis, chaos engineering, circuit breakers, retry logic, fallback strategies, and the developer self-improvement loop. Trigger on keywords: self-healing, resilience, fault tolerance, circuit breaker, retry, fallback, graceful degradation, chaos engineering, pre-mortem, failure mode, recovery, resilient design.
---

# Self-Healing Mindset

## Core Philosophy

> *"Everything will eventually fail over time."* — Werner Vogels, Amazon CTO

Self-healing is not a feature you add — it's a design philosophy you start with. The question is never "will this fail?" but "when this fails, what happens next?"

**The shift:** From reactive firefighting → proactive resilience engineering.

The same mindset applies at every level: code, systems, AI agents, and your own development practice.

---

## The Detect–Decide–Act Loop

Every self-healing system follows this pattern:

```text
DETECT  → Monitor signals (health checks, error rates, latency, business KPIs)
DECIDE  → Select recovery strategy (retry, fallback, scale, restart, degrade)
ACT     → Execute recovery (automatically or with human confirmation)
VERIFY  → Confirm recovery succeeded
LEARN   → Update the healing logic based on what worked
```text

This loop runs continuously. Design every system component with this loop in mind.

---

## Resilience Patterns in Code

### Retry with Exponential Backoff
For transient failures (network timeouts, rate limits):
```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxAttempts = 3,
  baseDelayMs = 1000
): Promise<T> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn()
    } catch (error) {
      if (attempt === maxAttempts) throw error
      const delay = baseDelayMs * Math.pow(2, attempt - 1)
      await sleep(delay + Math.random() * 100) // jitter
    }
  }
  throw new Error('Max retries exceeded')
}
```

### Circuit Breaker
Prevents cascading failures when a dependency is down:
```text
CLOSED (normal) → failures exceed threshold → OPEN (blocking calls)
OPEN → after timeout → HALF-OPEN (test one call)
HALF-OPEN → success → CLOSED | failure → OPEN
```text

Use: Resilience4j (Java), Polly (.NET), opossum (Node.js), tenacity (Python)

### Bulkhead
Isolate failures to prevent them spreading:
- Separate thread pools per service dependency
- Database connection pools per tenant
- Resource limits per endpoint

### Graceful Degradation
When a feature fails, serve a reduced but functional experience:
```text
Full service: personalized recommendations
Degraded: cached popular items
Minimal: static placeholder with "recommendations unavailable"
```text

Never show a crash when you can show reduced functionality.

### Fallback Strategy
Define explicit fallback for every external dependency:
```typescript
async function getRecommendations(userId: string) {
  try {
    return await recommendationService.get(userId)
  } catch {
    // Fallback: return cached popular items instead of crashing
    return await cache.get('popular-items') ?? DEFAULT_ITEMS
  }
}
```

### Timeouts
Every external call needs a timeout. No exceptions.
```typescript
const response = await fetch(url, {
  signal: AbortSignal.timeout(5000) // 5 second max
})
```

---

## Resilience Patterns in Systems

### Kubernetes Self-Healing
```yaml
livenessProbe:    # Restart container if health check fails
readinessProbe:   # Remove from load balancer if not ready
resources:
  limits:         # Prevent one pod consuming all resources
```yaml

### Health Check Endpoints
Every service needs:
- `/health` — Is the service alive? (liveness)
- `/ready` — Is the service ready to accept traffic? (readiness)
- `/metrics` — Prometheus-compatible metrics

### The Four Golden Signals
Monitor these for every service:
1. **Latency** — p50, p95, p99 response times
2. **Traffic** — requests per second
3. **Errors** — error rate (target < 0.1%)
4. **Saturation** — CPU, memory, queue depth

---

## Self-Healing AI Agents

Agents need resilience too:

### Agent Validation Loop (LoopAgent Pattern)
```text
Generate output → Validate output → If invalid: feedback + regenerate
Max iterations: 3 (circuit breaker to prevent infinite loops)
```text

### Plan–Validate–Execute–Observe–Replan
```text
PLAN:     Generate plan, validate feasibility before acting
EXECUTE:  Take action
OBSERVE:  Check if action succeeded
REPLAN:   If observation shows failure, adjust plan and retry
```text

### Agent Fallback Hierarchy
```text
Primary approach fails → Try alternative approach
Alternative fails → Request human clarification
Clarification unavailable → Safe default action or graceful stop
```text

### Output Validation Before Presenting
```text
1. Run tests/lint on generated code
2. Check output format matches requirements
3. Verify no forbidden patterns (hardcoded secrets, deprecated APIs)
4. Use a separate "validator" agent to check the "generator" agent's work
```text

---

## Proactive Resilience Thinking

### Pre-Mortem (Before Starting)
Before building anything significant, ask:
```text
Imagine it's 6 months from now and this has completely failed.
What went wrong? Work backwards from the failure.
```text
Then design to prevent the top 3 failure modes you identified.

### Failure Mode Analysis
For each component, answer:
| Component | How can it fail? | Impact? | Likelihood? | Prevention? | Recovery? |
|---|---|---|---|---|---|
| DB connection | Timeout, crash | High | Medium | Connection pooling, retry | Fallback to read replica |
| External API | Down, slow, rate-limited | Medium | High | Circuit breaker, cache | Return cached data |
| Auth service | Unreachable | Critical | Low | Token caching | Grace period for existing tokens |

### Chaos Engineering
Deliberately introduce failures to test your healing logic:
- Kill random containers (Chaos Monkey)
- Inject network latency
- Simulate database timeouts
- Drop random requests

**Rule:** If your system can't survive Chaos Engineering in staging, it will surprise you in production.

---

## Developer Self-Healing Loop

The same resilience philosophy applies to your own development practice:

### After Every Bug or Mistake
```text
1. ROOT CAUSE: What was the actual cause? (not just the symptom)
2. PREVENTION: What would have caught this earlier?
3. DETECTION: How do I make this class of error visible faster?
4. SYSTEM FIX: Add a rule, test, or lint check to prevent recurrence
```text

### Personal lessons.md
Keep a running log of your own recurring mistakes and the rules you created to prevent them. Review it at the start of each sprint or project.

```markdown
## Mistake: Forgot to handle null from API response
Root cause: Assumed API always returns data
Prevention: Always check API contract, add null guards by default
System fix: Added ESLint rule for nullable return types
```

### Proactive Code Habits
- Write the error handling before the happy path
- Ask "what happens when this fails?" for every external call
- Add tests for failure cases first, success cases second
- Default to defensive programming — assume inputs are wrong until proven otherwise

---

## System Health State Machine

```text
HEALTHY → (error rate spike) → DEGRADED
DEGRADED → (partial recovery) → RECOVERING  
DEGRADED → (escalation) → FAILING
FAILING → (intervention) → RECOVERING
RECOVERING → (verification passes) → HEALTHY
```text

Design every system to:
1. Know which state it's in
2. Transition between states automatically where safe
3. Alert humans only when human decision is needed
4. Never stay in FAILING state silently

---

## Quick Resilience Checklist

Before shipping any service or feature:
- [ ] Every external call has a timeout
- [ ] Retry logic with exponential backoff for transient failures
- [ ] Circuit breaker for unreliable dependencies
- [ ] Graceful degradation when non-critical features fail
- [ ] Health check endpoints implemented
- [ ] The four golden signals are being monitored
- [ ] Alerts configured for abnormal error rates and latency
- [ ] Failure scenarios tested (unit tests for error paths)
- [ ] Pre-mortem completed for critical features
- [ ] Runbook exists for common failure scenarios

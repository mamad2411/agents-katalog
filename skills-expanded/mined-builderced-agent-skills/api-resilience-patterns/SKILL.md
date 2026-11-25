---
name: api-resilience-patterns
description: Implement API resilience patterns — circuit breakers, retry with backoff, rate limiting, bulkhead isolation, timeout management, and graceful degradation.
version: "1.0.0"
last-updated: "2026-04-17"
model_tested: "claude-sonnet-4-6"
category: resilience
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: en
geo_relevance: [global]
priority: medium
dependencies:
  mcp: []
  skills: []
  apis: []
  data: []
update_sources:
  - url: "https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker"
    check_frequency: "yearly"
    last_checked: "2026-04-21"
license: MIT
---

# API Resilience Patterns

## When to Use

- Calling external APIs that might fail or slow down
- Designing microservice communication
- Building agents that call multiple tools/APIs
- Handling rate limits from LLM providers
- Preventing cascade failures

## Pattern 1: Circuit Breaker

Prevents repeated calls to a failing service.

**States**: Closed (normal) → Open (failing) → Half-Open (testing)

| State | Behavior | Transition |
|-------|----------|-----------|
| Closed | Forward requests normally | → Open after N consecutive failures |
| Open | Reject immediately (fail fast) | → Half-Open after cooldown period |
| Half-Open | Allow 1 test request | → Closed if success, → Open if fail |

**Config**: threshold=3 failures, cooldown=30s, half-open-max=1.

## Pattern 2: Retry with Exponential Backoff

```
Attempt 1: immediate
Attempt 2: wait 1s + random(0-500ms)
Attempt 3: wait 2s + random(0-500ms)
Attempt 4: wait 4s + random(0-500ms)
Max: 5 attempts, 16s max wait
```

**Rules**:
- Only retry on transient errors (429, 500, 502, 503, timeout)
- Never retry on client errors (400, 401, 403, 404)
- Always add jitter to prevent thundering herd
- Set a total timeout budget (not just per-attempt)

## Pattern 3: Rate Limiting (Client-Side)

Respect provider limits proactively:

| Strategy | When | How |
|----------|------|-----|
| Token bucket | Steady rate with bursts | Refill N tokens/sec, consume per request |
| Sliding window | Strict per-minute limits | Track timestamps of last N requests |
| Queue-based | Ordered processing | FIFO queue with configurable concurrency |

## Pattern 4: Bulkhead Isolation

Isolate failures to prevent cascade:
- Separate connection pools per service
- Separate thread/worker pools per dependency
- If service A fails, services B and C are unaffected

## Pattern 5: Timeout Management

| Tier | Timeout | Purpose |
|------|---------|---------|
| Connection | 5s | Detect unreachable host |
| Request | 30s | Detect slow response |
| Total operation | 60s | Budget for retries included |

**Rule**: Total timeout > (max_retries × request_timeout). Always set all three.

## Pattern 6: Graceful Degradation

| Scenario | Fallback |
|----------|---------|
| Search API down | Return cached results + "results may not be current" |
| Payment API slow | Queue payment, confirm later |
| AI API rate-limited | Switch to cheaper/faster model |
| Database read replica down | Read from primary (accept perf hit) |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Retry without backoff | Amplifies load on failing service | Exponential backoff + jitter |
| No timeout | Thread/connection leak | Always set timeouts |
| Retry on all errors | Retrying 401 wastes time | Only retry transient errors |
| Sync retry in UI thread | Blocks user interface | Async retry with status feedback |
| Cascading timeouts | Inner timeout > outer timeout | Budget timeouts from outside in |

## What This Skill Does NOT Do

- Does not implement specific libraries (guides patterns)
- Does not monitor uptime (use APM tools)
- Does not manage API keys or authentication
- Does not handle business logic fallbacks (only infrastructure patterns)

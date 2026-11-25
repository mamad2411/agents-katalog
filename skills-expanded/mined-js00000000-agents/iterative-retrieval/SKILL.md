---
name: iterative-retrieval
description: Pattern for progressively refining context retrieval — start broad, evaluate, refine, and converge on the right files before making changes.
---

# Iterative Retrieval Pattern

Solves the "context problem" where the agent doesn't know what context it needs until it starts working.

## When to Activate

- Starting unfamiliar tasks in a large codebase
- Exploring code to understand patterns before making changes
- Encountering "missing context" failures
- Building multi-step workflows where context is progressively refined
- Optimizing token usage by finding the right files upfront

## The Problem

When starting a task, you don't know:
- Which files contain the relevant code
- What patterns exist in the codebase
- What terminology the project uses

Standard approaches fail:
- **Read everything**: Exceeds context limits
- **Read nothing**: Lacks critical information
- **Guess what's needed**: Often wrong

## The Solution: Iterative Retrieval

A 4-phase loop that progressively refines context:

```
┌─────────────────────────────────────────────┐
│                                             │
│   ┌──────────┐      ┌──────────┐            │
│   │ DISPATCH │─────▶│ EVALUATE │            │
│   └──────────┘      └──────────┘            │
│        ▲                  │                 │
│        │                  ▼                 │
│   ┌──────────┐      ┌──────────┐            │
│   │   LOOP   │◀─────│  REFINE  │            │
│   └──────────┘      └──────────┘            │
│                                             │
│        Max 3 cycles, then proceed           │
└─────────────────────────────────────────────┘
```

### Phase 1: DISPATCH

Start with a broad search:

```
Search for: "authentication", "user", "session"
In: src/**/*.go, internal/**/*.go
Exclude: *_test.go, vendor/
```

### Phase 2: EVALUATE

Assess retrieved content for relevance:

| Score | Meaning |
|-------|---------|
| 0.8–1.0 | Directly implements target functionality |
| 0.5–0.7 | Contains related patterns or types |
| 0.2–0.4 | Tangentially related |
| 0–0.2 | Not relevant — exclude |

### Phase 3: REFINE

Update search criteria based on evaluation:

- Add new keywords discovered in high-relevance files
- Learn codebase terminology (e.g., "throttle" instead of "rate limit")
- Exclude confirmed irrelevant paths
- Target specific gaps identified in evaluation

### Phase 4: LOOP

Repeat with refined criteria (max 3 cycles).

Stop when: 3+ high-relevance files found AND no critical gaps remain.

## Practical Examples

### Example 1: Bug Fix

```
Task: "Fix the JWT token expiry bug"

Cycle 1:
  DISPATCH: Search for "token", "auth", "expiry" in internal/
  EVALUATE: Found middleware/auth.go (0.9), service/auth.go (0.8), model/user.go (0.3)
  REFINE: Add "refresh", "jwt" keywords; exclude model/user.go

Cycle 2:
  DISPATCH: Search refined terms
  EVALUATE: Found pkg/jwt/jwt.go (0.95), config/config.go (0.6)
  REFINE: Sufficient context (3 high-relevance files)

Result: middleware/auth.go, service/auth.go, pkg/jwt/jwt.go
```

### Example 2: Feature Implementation

```
Task: "Add exchange rate caching with Redis"

Cycle 1:
  DISPATCH: Search "rate", "exchange", "cache" in internal/
  EVALUATE: Found service/exchange.go (0.9), no cache results
  REFINE: Search for "redis" patterns

Cycle 2:
  DISPATCH: Search "redis", "cache" patterns
  EVALUATE: Found pkg/cache/redis.go (0.85), config/config.go (0.6)
  REFINE: Need to understand existing cache patterns

Cycle 3:
  DISPATCH: Search for cache usage patterns
  EVALUATE: Found service/price.go (0.8) — uses same cache pattern
  REFINE: Sufficient context

Result: service/exchange.go, pkg/cache/redis.go, service/price.go
```

## Best Practices

1. **Start broad, narrow progressively** — Don't over-specify initial queries
2. **Learn codebase terminology** — First cycle often reveals naming conventions
3. **Track what's missing** — Explicit gap identification drives refinement
4. **Stop at "good enough"** — 3 high-relevance files beats 10 mediocre ones
5. **Exclude confidently** — Low-relevance files won't become relevant

## Integration with Workflow

Use iterative retrieval as a **first step** before making changes:

```
1. Understand the task
2. Run iterative retrieval (2-3 cycles)
3. Review retrieved files
4. Plan implementation based on existing patterns
5. Implement changes
6. Verify
```

---

**Remember**: The goal is not to find every related file — it's to find the minimum set of files needed to make informed changes.

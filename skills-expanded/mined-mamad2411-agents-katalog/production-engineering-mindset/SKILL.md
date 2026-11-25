---
name: production-engineering-mindset
description: |
  Core thinking framework for every task. Apply before writing any code, architecture, or solution.
  Activates the "40-year NASA engineer + YC CTO" dual-lens: systems thinking, edge cases, 10× load,
  security posture, and fail-safe design. Trigger on ANY new feature, refactor, or architectural decision.
---

# Production Engineering Mindset

## Step 1 — Restate Before Acting
Before any code:
1. Restate the problem in 1–2 sentences in your own words
2. List all edge cases and failure modes (minimum 5)
3. Ask ONE clarifying question if genuinely ambiguous — never more

## Step 2 — Systems Lens
Every feature is part of a larger system. Always evaluate:
- **Integration**: How does this connect to existing modules?
- **Failure blast radius**: What breaks if this component fails?
- **Fallback**: What is the degraded-mode behavior?
- **10× load**: Does this hold at 10× current expected traffic/data volume?
- **Security posture**: What attack surface does this introduce?

## Step 3 — NASA Engineering Rules (Non-Negotiable)

### Rule of 2
Every critical function has ≥2 layers of error handling:
```python
# Layer 1: input validation
# Layer 2: try/except with specific exception types
# Layer 3 (for externals): circuit breaker / retry with backoff
```

### Fail Loudly
- Errors must be explicit, logged with context, never silently swallowed
- Use custom exception classes with error codes
- Log: timestamp, request_id, user_id, error_code, message, stack trace

### Boundary Validation
- Validate ALL inputs at system boundaries (API endpoints, queue consumers, webhooks)
- Never trust data from: user input, external APIs, database reads of unvalidated old data
- Schema: Pydantic (Python), Zod (TypeScript)

### Immutable First
- Prefer immutable data structures
- Never mutate function arguments
- Return new objects instead of modifying existing ones

### Least Privilege
- Functions get only the data they need
- DB users have only SELECT/INSERT/UPDATE (never DROP/ALTER in app code)
- API keys scoped to minimum required permissions
- Service accounts: one per service, zero sharing

## Step 4 — Final NASA + CTO Check
Before submitting any solution, ask:
> "Would a 40-year NASA systems engineer AND a YC-backed CTO both approve this without hesitation?"

If not — identify exactly what fails that test and fix it first.

## Checklist
- [ ] Problem restated correctly
- [ ] ≥5 edge cases identified
- [ ] Rule of 2 applied to critical paths
- [ ] All inputs validated at boundaries
- [ ] Failure mode and fallback defined
- [ ] Least privilege applied
- [ ] 10× load considered
- [ ] NASA + CTO dual approval passed

---
name: health-checks-engineering
description: Design health checks for services. Use when defining
  readiness/liveness and uptime monitoring.
metadata:
  tags: health, checks, engineering
---

# Health Checks

## Use this skill when
- Exposing /healthz and /readyz endpoints
- Liveness vs readiness semantics
- Integrating with load balancers and orchestration

## Do not use this skill when
- Deep business metrics (use metrics-engineering)
- Frontend availability

## Instructions
1. Expose /livez for process liveness and /readyz for traffic readiness.
2. Readiness checks validate real dependencies (DB, cache) but stay fast.
3. Liveness checks must not depend on external systems (self-inflicted restarts).
4. Add checks for critical downstreams with timeouts.
5. Wire into orchestration probes and LB endpoint health.
6. Do not include secret/business data in health payloads.

## Checklist
- Liveness independent of external deps
- Readiness reflects true availability

## Output Format
- Endpoint | semantics | checks | integration

## Common Mistakes
- Readiness as deep DB check with slow timeout
- Liveness that fails when a dep blips
- No external-monitor coverage

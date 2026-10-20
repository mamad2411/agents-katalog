---
name: dependency-outage-degrade
description: >
  Design graceful degradation when upstream dependencies fail: circuit breakers, timeouts,
  bulkheads, cached fallbacks, feature flags, fail-open vs fail-closed policy per capability,
  and SRE playbooks for registry, API, payment, IdP, and data-store outages. Use when third-party
  dependency outage, cascade failure, degrade mode, partial brownout, circuit breaker, fallback
  cache, or owned SRE resilience for external services — not for dependency confusion or pinning.
---

# Dependency Outage Degrade

## Scope And Authorization

- **In scope:** Services and dependencies you operate; chaos/game-day drills on owned environments.
- **Out of scope:** Deliberately attacking third-party SaaS; bypassing customer rate limits without contract; silent fail-open on authZ.
- Prefer staging game days before production brownouts; use change windows for prod drills.
- Redact tokens, customer IDs, and dependency credentials from incident notes.
- Pair with `retry-backoff-patterns`, `feature-flag-patterns`, `observability-metrics-tracing`, and `code-quality-standards`.

## When To Use

- Designing or reviewing behavior when Redis, SQL, payment API, IdP, email, object storage, or package registry is down.
- Cascading timeouts and thread-pool exhaustion from a single slow dependency.
- Defining which features must fail closed (auth, payments) vs degrade (recommendations, avatars).
- Writing runbooks for partial dependency brownouts and status-page comms.
- Implementing circuit breakers, hedges, and stale-cache serves.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Retry/backoff implementation detail | `retry-backoff-patterns` |
| Feature flag rollout mechanics | `feature-flag-patterns` |
| Metrics/traces/SLO wiring | `observability-metrics-tracing` |
| Package registry name confusion | `dependency-confusion` |
| Pin/lock supply chain | `dependency-pinning-strategies` |
| Redis lock correctness | `distributed-lock-redis-safety` |
| Code quality baseline | `code-quality-standards` |

## Domain Concepts

| Pattern | Use |
| --- | --- |
| Timeout | Bound wait; never default infinite client timeouts |
| Retry + budget | Limited retries with jitter; respect idempotency |
| Circuit breaker | Open after error rate; half-open probe |
| Bulkhead | Isolate pools/queues so one dep cannot starve others |
| Fallback | Stale cache, default config, queue-for-later, hide UI |
| Fail closed | Deny when control plane (authZ, fraud) unavailable |
| Fail open | Rare; only for non-security best-effort with monitoring |
| Brownout | Shed non-critical load under dependency pressure |

## Workflow

### 1. Confirm scope and success criteria

1. List critical user journeys and every external/internal dependency on the path.
2. Success: documented degrade matrix; no cascade on synthetic dependency kill; SLOs for “core path available.”
3. Name incident commander role and status copy owners.

### 2. Inventory dependencies and failure modes

| Dependency | Criticality | Failure modes | Current client behavior |
| --- | --- | --- | --- |
| Primary DB | Critical | timeout, failover lag | ? |
| Redis cache | High/Medium | connection refused | ? |
| IdP / OIDC | Critical for login | 5xx, DNS | ? |
| Payments | Critical for checkout | timeout, partial | ? |
| Recommendations API | Low | slow | ? |
| npm/PyPI (CI) | Build | registry 503 | ? |

1. Capture timeouts, retries, pool sizes, and whether errors bubble as 500 to all users.
2. Note shared thread pools or single HTTP client without limits.

### 3. Build the degrade matrix

| Capability | If dep X down | User-visible behavior | Security note |
| --- | --- | --- | --- |
| Login | IdP down | Fail closed; maintenance message | Never skip auth |
| Read feed | Cache down | Hit DB with shed; or stale | Rate-limit DB |
| Personalization | ML API down | Default ranking | No PII leak in errors |
| Checkout | Pay API down | Queue order / retry UX | No double-charge |
| Admin export | Object store down | Fail with ticket | No silent empty file success |

1. Product + security sign fail-open exceptions with expiry.
2. Prefer **shed load** over unbounded retries.

### 4. Implement resilience controls

```text
# Design checklist per outbound client
# 1) connect + request timeouts
# 2) max retries + total deadline
# 3) circuit breaker thresholds
# 4) bulkhead (separate pool / queue)
# 5) fallback function + metrics
# 6) idempotency keys for mutating calls
```

```yaml
# Example feature-flag driven degrade (conceptual)
flags:
  recommendations_enabled: false   # kill switch
  serve_stale_profile_cache: true
  checkout_async_capture: true
```

1. Wire kill switches via `feature-flag-patterns` for instant brownout.
2. Cache negative results carefully (do not cache auth failures as “logged out forever” without TTL).
3. For package/registry CI outages: mirror/cache (Artifactory), vendor critical modules, or queue releases—not `npm install` against random mirrors without integrity.

### 5. Game day and verification

```bash
# Owned staging examples (tooling varies)
# Block dependency with toxiproxy / fault injection / security group deny
# curl app health and critical journeys; watch error budgets
curl -sS https://app.staging.example/health | jq .
curl -sS -o /dev/null -w "%{http_code}\n" https://app.staging.example/api/feed
```

1. Inject latency and hard fail separately; measure saturation of pools.
2. Confirm auth/payment paths fail closed; non-critical UI degrades.
3. Validate alerts: dependency error rate, breaker open, fallback ratio, queue depth.

### 6. Runbook and communications

1. Symptoms → likely dep → dashboards → degrade flags → customer status → recovery validation.
2. On recovery: close breakers gradually; flush bad caches if needed; watch thundering herd.
3. Post-incident: adjust timeouts/matrix; ticket permanent architecture fixes.

### 7. Hand off

1. Publish degrade matrix next to architecture diagram.
2. On-call knows flag names and owners.
3. Apply `code-quality-standards` to client wrappers; avoid copy-paste infinite retries.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Auth dep down | Fail closed | Guest mode with admin rights |
| Cache down | Bounded DB + shed | Unbounded stampede |
| Retries | Budget + jitter + idempotent | Retry storm on 500s |
| UX | Explicit degrade banner | Silent corruption / empty success |
| Kill switch | Flag ready | Redeploy-only disable |
| CI registry | Org mirror + lock | Disable TLS to “make install work” |

## Output Checklist

- [ ] Journey × dependency inventory complete
- [ ] Degrade matrix with fail-open/closed signed
- [ ] Timeouts, retries, breakers, bulkheads implemented or ticketed
- [ ] Feature kill switches named and tested
- [ ] Game-day evidence on staging (or authorized prod drill)
- [ ] Alerts and dashboards for breaker/fallback
- [ ] Runbook + status comms templates
- [ ] Recovery thundering-herd plan
- [ ] Residual risk and owners listed
- [ ] `code-quality-standards` applied to resilience code

## Rules

- Security controls fail closed unless an explicit, time-bounded exception exists.
- Degrade must not invent successful writes that never happened.
- Chaos only on owned/authorized systems.
- Prefer measurable fallback rates over hopeful “it should be fine.”
- Focus on outage degradation; route supply-chain naming and pin policy elsewhere.

---
name: api-rate-limit-design
description: >
  Design API rate limits and quotas: limit keys (IP, user, API key, route), budgets and
  windows, multi-tier policies, headers/UX, and abuse-resistant enforcement. Use when rate
  limit design, API quota, 限流设计, 429 policy, Retry-After, or throttle UX. Pair with
  bypass testing for adversarial review.
---

# API Rate Limit Design

## Scope And Authorization

- **In scope:** APIs and gateways you operate.
- **Out of scope:** Stress-testing third-party APIs without permission.
- Bad limits either DoS your users or fail to stop abuse — stage experiments.
- Pair with `rate-limit-bypass-testing` (authorized) and `adaptive-concurrency-limits`.

## When To Use

- Defining 429 policies for public/partner APIs.
- Choosing keys: IP vs user vs API key vs route.
- Multi-tier quotas (free vs paid).
- Standardizing `Retry-After` and rate-limit headers.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Adversarial bypass testing | `rate-limit-bypass-testing` |
| Adaptive concurrency (overload) | `adaptive-concurrency-limits` |
| Account login lockout | `account-lockout-design` |
| CAPTCHA controls | `captcha-bypass-research` (authorized) |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Dimension | Options |
| --- | --- |
| Algorithm | Fixed window, sliding window, token bucket, GCRA |
| Key | IP, user id, API key, tenant, route, combination |
| Window | Per-second burst + per-day quota |
| Response | 429 + Retry-After + optional RateLimit headers |
| Storage | Redis/cluster counter; edge gateway |
| Fairness | Noisy neighbor isolation |

## Workflow

### 1. Threats and success criteria

1. Threats: scraping, credential stuffing, expensive endpoints, accidental loops.
2. Success: abuse curtailed; honest clients succeed with backoff; limits documented; bypasses hard (proxy fleets still need auth costs).
3. Inventory routes by cost (cheap reads vs expensive exports/search).

### 2. Policy matrix

| Route class | Key | Budget (example) | Notes |
| --- | --- | --- | --- |
| Auth login | IP + account | Tight | See lockout skill |
| Public read | IP | Moderate | CDN cache |
| Authed CRUD | user/tenant | Higher | |
| Export/search | user | Low | Queue async |
| Partner API | API key | Contractual | Paid tiers |

### 3. Enforcement placement

| Place | Pros | Cons |
| --- | --- | --- |
| CDN/WAF | Stops early | Coarse identity |
| API gateway | Central | Config complexity |
| App middleware | Rich user context | Every service must implement |
| Service mesh | East-west | Not public edge |

Prefer gateway + app for defense in depth on expensive ops.

### 4. Headers and client UX

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
RateLimit-Limit: 100
RateLimit-Remaining: 0
RateLimit-Reset: 1700000000
```

1. Document in OpenAPI (`api-documentation-writing`).
2. Idempotent clients honor Retry-After; avoid thundering herds (jitter).

### 5. Implementation sketch (Redis token bucket idea)

```text
key = f"rl:{api_key}:{route_class}"
tokens = redis eval bucket.lua
if tokens < 1: return 429
```

1. Atomic ops only; fail policy: **fail open vs closed** documented (security APIs often fail closed for auth; product may fail open carefully for reads).
2. Clock skew: use Redis TIME.

### 6. Anti-bypass design (high level)

1. Authenticated limits bind to user/key not only IP.
2. Normalize IPs behind trusted proxies (don’t trust raw XFF from clients).
3. Separate burst and sustained.
4. Escalate: CAPTCHA / blocklist / key revoke on extreme abuse.
5. Authorized adversarial review → `rate-limit-bypass-testing`.

### 7. Verify

```bash
for i in $(seq 1 200); do
  curl -sS -o /dev/null -w "%{http_code}\n" -H "X-API-Key: $K" https://api.example.com/v1/items
done | sort | uniq -c
# Expect eventual 429; check Retry-After
```

1. Load test staging only.
2. Dashboards: 429 rate, top keys, redis errors.

### 8. Hand off

1. Publish limits in developer docs.
2. Support runbook for legitimate raise requests.
3. Review quarterly against traffic.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Keying | User/key + route class | IP only for authed API |
| UX | 429 + Retry-After | Hang connections |
| Expensive ops | Tight + async | Same limit as cheap GET |
| Proxies | Trusted hop XFF parse | Trust client X-Forwarded-For |

## Output Checklist

- [ ] Route classes costed
- [ ] Policy matrix approved
- [ ] Placement chosen (edge/app)
- [ ] Headers/docs complete
- [ ] Redis/gateway atomic enforcement
- [ ] Fail open/closed decision recorded
- [ ] Staging verification of 429 behavior
- [ ] Metrics/alerts
- [ ] Link to bypass testing if needed
- [ ] `code-quality-standards` applied

## Rules

- Owned systems; no unapproved external stress tests.
- Rate limits complement authz — not a substitute.
- Document limits for legitimate developers.
- Prefer identity-bound keys over IP-only for authed APIs.
- Coordinate with concurrency limits under overload.

---
name: api-key-lifecycle
description: >
  Design and operate the API key lifecycle: create, issue, store references, dual-run
  rotate, revoke, and audit. Use when API key creation, rotation, revocation, key grace
  periods, key metadata (prefix/last4/scopes), emergency kill switches, or partner/machine
  credentials need a controlled lifecycle on owned or authorized systems.
---

# API Key Lifecycle

## Scope And Authorization

- **In scope:** Partner/machine API credentials for systems you operate.
- **Out of scope:** Using stolen keys; rotating keys on platforms you do not admin.
- Coordinate with partners for rotation windows.
- Pair with `api-key-hash-storage`, gateway auth, and `code-quality-standards`.

## When To Use

- Building developer portal key management.
- Rotation/revocation policies and grace periods.
- Emergency mass-revoke after leak.
- Scopes, environments (test/live), and expiry.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Hash-at-rest implementation | `api-key-hash-storage` |
| JWT user auth testing | `api-auth-and-jwt-abuse` |
| Rate limits per key | `api-rate-limit-design` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Stage | Actions |
| --- | --- |
| Create | AuthZ who can mint; set scopes/env/expiry |
| Issue | Show secret once; download CSV optional |
| Active | AuthN requests; last_used; anomaly detect |
| Rotate | New key; dual-run grace; deprecate old |
| Revoke | Immediate deny; audit reason |
| Expire | TTL jobs; notify owners |

## Workflow

### 1. Confirm success criteria

1. Owners can self-serve create/revoke within policy; security can kill-switch; every key has owner + scopes; storage hashed.
2. RTO for mass revoke known.

### 2. Metadata model

| Field | Purpose |
| --- | --- |
| id | Stable reference |
| prefix / last4 | Support UX |
| owner / team | Accountability |
| scopes | Least privilege |
| env | test vs live |
| created/expires/revoked | Lifecycle stamps |
| created_by / reason | Audit |

### 3. Create and issue

```text
1. Authenticated user with permission keys:write
2. Select scopes from allowlist (not free text admin)
3. Generate key; store hash (api-key-hash-storage)
4. Display once; optional email without full secret
5. Emit audit event key.created
```

### 4. Rotate with grace

```text
Day 0: create new key (same scopes); both valid
Day 0-N: partner updates clients (notify)
Day N: revoke old automatically if not already
Emergency: revoke both + issue new
```

```bash
# Partner test after rotation
curl -sS -o /dev/null -w "%{http_code}\n" https://api.example.com/v1/ping \
  -H "X-API-Key: $NEW_KEY"
```

### 5. Revoke and kill switch

1. Per-key revoke in portal + API.
2. Principal-level revoke (all keys for partner).
3. Global emergency: feature flag deny all API keys for route class.
4. Propagate revoke to gateway cache immediately (short TTL / pubsub invalidation).

### 6. Audit and detect

| Event | Alert |
| --- | --- |
| key.created with broad scopes | Security review |
| Spike of 401 on prefix | Leak attempt / typo |
| Use from new geo/ASN | Optional step-up |
| key not used 180d | Expiry candidate |

### 7. Verify

1. Revoked key → 401 everywhere within cache SLA.
2. Grace period dual keys both work until cutover.
3. Cannot create live keys from test-only roles.

### 8. Hand off

1. Runbook: leak response (revoke, rotate, customer comms).
2. Portal UX for last4 + created date.
3. Legal: data processing for partner traffic logs.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Issue | Once + hash stored | Email full key forever |
| Rotate | Dual-run grace | Instant delete without notice (unless emergency) |
| Scopes | Least privilege presets | Single god key for all APIs |
| Revoke | Fast cache bust | Revoke only in DB; edge caches 24h |

## Output Checklist

- [ ] Metadata model includes owner/scopes/env
- [ ] Create/issue UX with one-time secret
- [ ] Hash storage integrated
- [ ] Rotate dual-run documented
- [ ] Revoke + kill switch tested
- [ ] Audit events + alerts
- [ ] Cache invalidation SLA defined
- [ ] Partner runbook published
- [ ] `code-quality-standards` applied

## Rules

- Owned platforms only.
- Least-privilege scopes by default.
- Prefer short-lived keys where product allows; always support revoke.
- Never log full keys.
- Coordinate rotation with customers except true emergencies.

---
name: etag-optimistic-concurrency
description: >
  HTTP ETag / If-Match optimistic concurrency for owned APIs: strong vs weak
  validators, 412 Precondition Failed, version columns, and lost-update
  prevention. Use when ETag, If-Match, If-None-Match, optimistic locking, or
  concurrent PATCH/PUT safety.
---

# ETag Optimistic Concurrency

## Scope And Authorization

- **In scope:** HTTP APIs and resources you own.
- **Out of scope:** Forcing concurrency races on third-party APIs without permission.
- ETags can leak existence/version metadata—combine with authz.
- Prefer strong validators for write concurrency; weak for cache-only when appropriate.
- Pair with `code-quality-standards` and IDOR/authz skills for access control.

## When To Use

- Preventing lost updates on concurrent editors.
- Implementing `GET` → edit → `PUT/PATCH` with `If-Match`.
- Caching with `If-None-Match` / 304 (related but distinct goal).
- Mapping DB `version` / `updated_at` / row hash to ETag.
- Fixing “last write wins” bugs on shared resources.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| AuthZ / IDOR | `idor-broken-object-authorization` |
| Distributed locks / transactions | database concurrency skills |
| Event schema versioning | `event-versioning-compatibility` |
| Error message copy | `error-message-ux-writing` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Strong ETag | Opaque version; changes every representation change |
| If-Match | Required on unsafe updates when concurrency matters |
| 412 | Precondition failed when version mismatch |
| 428 | Optional: require precondition (RFC 6585) |
| Weak ETag | `W/"..."` for semantic equivalence / cache |
| Auth | Still check actor can write resource |

## Workflow

### 1. Confirm scope and success criteria

1. Resources needing concurrency (docs, carts, configs).
2. Success: concurrent PUTs cannot silently clobber; clients get 412 + fresh body/etag.

### 2. Inventory current update paths

```bash
rg -n "If-Match|ETag|optimistic|version" --glob '!node_modules' | head
```

1. Note DB columns available for versioning.
2. Check CDN/proxy stripping of precondition headers.

### 3. Choose validator source

| Source | Notes |
| --- | --- |
| Monotonic `version` int | Simple; increment in same txn as update |
| `updated_at` timestamp | Collisions possible at high rate |
| Hash of representation | Costly; careful with volatile fields |
| Row xid / system version | DB-specific |

### 4. Implement protocol

```http
GET /items/42 HTTP/1.1
→ 200 OK
ETag: "v17"
{"id":42,"name":"A","version":17}

PUT /items/42 HTTP/1.1
If-Match: "v17"
Content-Type: application/json
{"name":"B"}

→ 200 OK
ETag: "v18"

# Concurrent writer with stale tag:
PUT /items/42
If-Match: "v17"
→ 412 Precondition Failed
ETag: "v18"
```

```sql
UPDATE items SET name = $1, version = version + 1
WHERE id = $2 AND version = $3
-- 0 rows ⇒ conflict
```

1. Compare ETag in handler **and** enforce in DB update predicate.
2. On success return new ETag; on conflict return 412 with current representation optional.
3. For `If-None-Match: *` on create, support if you need create-if-absent semantics.

### 5. Caching vs concurrency

1. Do not confuse cache 304 flows with write protection—writes need `If-Match`.
2. Document whether ETag is strong; avoid weak ETags for write guards.
3. Ensure intermediaries don’t serve stale ETags for authorized personalized resources incorrectly.

### 6. Verify with evidence

```bash
# Parallel updates with same If-Match — exactly one should succeed
etag=$(curl -sD- "$BASE/items/42" -o /tmp/b | awk -F': ' '/[Ee][Tt]ag/ {print $2}' | tr -d '\r')
curl -s -o /dev/null -w "%{http_code}\n" -X PUT "$BASE/items/42" -H "If-Match: $etag" -H 'Content-Type: application/json' -d '{"name":"x"}'
curl -s -o /dev/null -w "%{http_code}\n" -X PUT "$BASE/items/42" -H "If-Match: $etag" -H 'Content-Type: application/json' -d '{"name":"y"}'
```

1. Automated tests for race (transactional).
2. Confirm missing `If-Match` policy: reject (428/400) or allow with documented last-write-wins only if product accepts risk.

### 7. Hand off

1. Client SDK guidance: always send If-Match from last GET.
2. Metrics: 412 rates (spike may mean UX issues).
3. AuthZ still mandatory on every write.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Guard | If-Match + versioned UPDATE | Read version in app only, no atomic check |
| Conflict | 412 + current ETag | 500 on conflict |
| Validator | Opaque strong tag | Guessable sequential without authz |
| Policy | Require If-Match on PATCH | Optional header ignored |
| Cache | Separate rules | Weak ETag for money transfers |

## Output Checklist

- [ ] Resources needing OCC listed
- [ ] Version source chosen
- [ ] If-Match enforced with atomic DB check
- [ ] 412 behavior documented
- [ ] Concurrent test evidence
- [ ] Client guidance published
- [ ] AuthZ confirmed on writes
- [ ] Residual risk noted

## Rules

- Optimistic concurrency ≠ authorization.
- Atomic compare-and-swap in storage layer.
- Prefer strong ETags for writes.
- Owned APIs only for race testing.
- Event compatibility is a different problem → `event-versioning-compatibility`.

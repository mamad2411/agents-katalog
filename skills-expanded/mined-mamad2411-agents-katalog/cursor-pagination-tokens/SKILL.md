---
name: cursor-pagination-tokens
description: >
  Design secure, stable cursor-based pagination for owned APIs: opaque cursors,
  sort-key encoding, forward/backward pages, mutation-safe iteration, and
  anti-tamper signing. Use when replacing fragile offset/limit pages or fixing
  skipped/duplicated items under concurrent writes.
---

# Cursor Pagination Tokens

## Scope And Authorization

- **In scope:** HTTP/JSON APIs and list queries you control.
- **Out of scope:** Scraping third-party paginated APIs against ToS; using cursor analysis to access others' data (IDOR still applies — authorize rows).
- Prefer opaque cursors; never trust client-supplied filters inside cursors without re-authz.
- Pair with `code-quality-standards` and API authz skills.

## When To Use

- Large lists where `OFFSET` is slow or inconsistent under inserts/deletes.
- Mobile/infinite scroll needing stable `next_cursor`.
- GraphQL/Relay-style connections or REST equivalents.
- Hardening cursors against tampering (reading others' pages).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| IDOR on object access | `idor-broken-object-authorization` |
| API auth/JWT | `api-auth-and-jwt-abuse` / API auth skills |
| DB indexing design broadly | database performance skills |
| Rate limits | rate-limit skills |
| Implementation quality baseline | `code-quality-standards` |

## Offset vs cursor

| Approach | Pros | Cons |
| --- | --- | --- |
| `offset/limit` | Simple | Skips/dupes on writes; deep pages expensive |
| Cursor (keyset) | Stable, index-friendly | Needs stable sort; more design |

Keyset idea: `WHERE (created_at, id) < (:ts, :id) ORDER BY created_at DESC, id DESC LIMIT n`.

## Workflow

### 1. Confirm scope and success criteria

1. List endpoints, default sort, max page size, consistency needs.
2. Success: no authz bypass via cursor; pages stable under inserts; performance uses indexes; tokens opaque.

### 2. Choose sort keys

1. Must be **deterministic**: unique tie-breaker (`id`) required.
2. Prefer indexed columns matching filters (`tenant_id, created_at DESC, id DESC`).
3. Document whether “live” list can show new head items on next refresh (usual) vs snapshot isolation (rare).

### 3. Encode opaque cursors

```python
import base64, json, hmac, hashlib

def encode_cursor(payload: dict, secret: bytes) -> str:
    body = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode())
    sig = hmac.new(secret, body, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(body + b'.' + sig).decode().rstrip('=')

def decode_cursor(token: str, secret: bytes) -> dict:
    # verify HMAC, json loads, validate schema — reject on failure
    ...
```

Payload example: `{"v":1,"c_at":"2026-07-01T12:00:00Z","id":"01H..."}` — **not** raw SQL.

### 4. Query pattern

```sql
SELECT *
FROM events
WHERE tenant_id = $tenant
  AND (created_at, id) < ($c_at, $id)  -- for descending pages
ORDER BY created_at DESC, id DESC
LIMIT $limit + 1;
```

1. Fetch `limit+1` to know if `next_cursor` exists.
2. Apply **same authz filters** every page (tenant, ACL) — cursor must not widen scope.
3. Cap `limit` (e.g. 1..100).

### 5. API shape

```json
{
  "data": [ ... ],
  "next_cursor": "eyJ...",
  "prev_cursor": null
}
```

| Topic | Guidance |
| --- | --- |
| Direction | Separate `before`/`after` or signed direction flag in cursor |
| Empty page | Valid; null next cursor |
| Invalid cursor | `400` not `500` |
| Expired cursor | Optional TTL if business requires snapshot semantics |

### 6. Mutations and consistency

| Event | Behavior |
| --- | --- |
| Insert newer than cursor | Appears on new first page, not mid-walk (keyset DESC) |
| Delete seen item | May leave hole — acceptable; don't re-use offset math |
| Update sort key | Can duplicate/skip — avoid mutable sort keys |

### 7. Verify

```bash
# Walk pages until next_cursor null; union of ids unique
# Tamper cursor bytes → 400
# Cursor from tenant A used with tenant B token → empty or 403, never leak
```

Load test deep pagination vs offset baseline.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Cursor | Opaque + HMAC | `?offset=100` as “cursor” |
| Sort | `(created_at, id)` | `name` only non-unique |
| Authz | Re-apply filters | Trust cursor tenant id alone |
| Page size | Hard max | `limit=1000000` |
| SQL | Keyset predicates | `WHERE id IN (cursor blob)` |

## Output Checklist

- [ ] Sort keys unique and indexed
- [ ] Opaque signed/encoded cursor
- [ ] limit caps enforced
- [ ] limit+1 has_next pattern
- [ ] Authz filters every page
- [ ] Tamper tests
- [ ] Cross-tenant tests
- [ ] Mutation behavior documented
- [ ] API docs for clients
- [ ] Residual consistency notes

## Rules

- Cursors are capabilities — sign and re-validate scope.
- Prefer keyset over offset for large dynamic lists.
- Focus on **cursor pagination token design**.

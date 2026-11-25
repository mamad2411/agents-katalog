---
name: api-pagination-security
description: >
  Authorized testing of API pagination controls: offset vs cursor designs, max page size
  enforcement, authorization across pages, filter/sort injection via list params, total-count
  and metadata leaks, and cursor integrity/signing. Use when list endpoints expose
  page/offset/limit/cursor/after/before/pageSize, bulk exports, GraphQL connections, or
  scraped multi-page dumps need hardening.
---

# API Pagination Security

## Scope And Authorization

- **In scope:** List/export APIs you own or may test under authorization.
- **Out of scope:** Mass scraping third-party APIs against ToS without permission.
- Large `limit` values can DoS databases — test carefully in staging.
- Pair with IDOR skill for object authz and `api-rate-limit-design`.

## When To Use

- Reviewing `/resources?page=&limit=` or cursor-based lists.
- GraphQL connection/`first`/`after` arguments.
- Export endpoints that page internally.
- Findings involving over-fetch, blind IDOR via paging, or unsigned cursors.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Object-level IDOR deep dive | `idor-broken-object-authorization` |
| Rate limit design | `api-rate-limit-design` |
| SQL injection class | `sqli-sql-injection` |
| API recon | `api-recon-and-docs` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Style | Risks |
| --- | --- |
| Offset/limit | Large offset scans; negative values; huge limit |
| Page/pageSize | Same; total pages oracle |
| Cursor/keyset | Tampered cursor → data from other tenants |
| GraphQL connections | Nested connection amplification |
| Total count | Expensive COUNT(*); leaks existence |

## Workflow

### 1. Confirm endpoints and success criteria

1. Inventory list endpoints and params.
2. Success: max page size enforced; authz applied per item/query; cursors integrity-checked; expensive modes rate-limited.
3. Baseline normal `limit=20` latency.

### 2. Size and bound tests

```bash
API=https://api.example.com/v1/items
AUTH="Authorization: Bearer $T"
curl -sS -D- -o /dev/null -H "$AUTH" "$API?limit=1"
curl -sS -D- -o /dev/null -H "$AUTH" "$API?limit=100000"
curl -sS -D- -o /dev/null -H "$AUTH" "$API?limit=-1"
curl -sS -D- -o /dev/null -H "$AUTH" "$API?offset=-5"
curl -sS -D- -o /dev/null -H "$AUTH" "$API?offset=999999999"
```

| Expect (secure) |
| --- |
| Cap `limit` (e.g. ≤100/1000) |
| Reject negatives |
| Timeout/rate limit abusive offsets |

### 3. Authorization across pages

1. As user A, page through all results — must never include B’s objects.
2. Craft cursor from A’s session used as B (if portable) — must fail.
3. Filter params `owner_id=B` while authed as A — must ignore or 403.

### 4. Cursor integrity

```bash
# Decode cursor (often base64 JSON) in lab
python - <<'PY'
import base64,sys
print(base64.urlsafe_b64decode(sys.argv[1]+'=='))
PY
# Tamper tenant_id inside; resend
```

| Good cursor | Bad cursor |
| --- | --- |
| Signed (HMAC) opaque blob | Clear base64 `{"id":5,"tenant":2}` |
| Server-side continues query with session tenant | Trust cursor tenant field |
| Expiry / purpose bound | Eternal replay across users |

### 5. Sort/filter injection

```bash
curl -sS -H "$AUTH" "$API?sort=password_hash"
curl -sS -H "$AUTH" "$API?sort=id;drop table"
curl -sS -H "$AUTH" "$API?filter=..."
```

1. Allowlist sort columns.
2. Parameterize filters; no raw SQL concat (`sqli-sql-injection`).

### 6. Metadata leakage and exports

1. `total` count may leak hidden resource existence — product decision.
2. Export jobs should re-check authz server-side and rate-limit.
3. GraphQL: depth/cost limits on nested connections.

### 7. Remediate and verify

```text
MAX_LIMIT = 100
default_limit = 20
cursor = sign(payload, server_secret)
query always includes tenant_id = session.tenant
```

Re-run bound and tamper tests after fix.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Limit | Hard max | Unlimited pageSize |
| Cursor | Signed + tenant from session | Trust client cursor fields |
| Authz | Predicate on every page query | Filter only first page in app memory |
| Sort | Allowlist | User-controlled column names |

## Output Checklist

- [ ] List endpoints inventoried
- [ ] Max/min limit/offset tested
- [ ] Cross-user page authz tested
- [ ] Cursor tamper tested
- [ ] Sort/filter allowlists reviewed
- [ ] Count/export costs considered
- [ ] Fixes verified
- [ ] Rate limits considered for list/export
- [ ] `code-quality-standards` applied

## Rules

- Authorized testing only; avoid prod DoS.
- Pagination must preserve authorization predicates.
- Prefer keyset/cursor with server-side integrity.
- Cap page sizes and expensive sorts.
- Redact tokens and personal data from examples.

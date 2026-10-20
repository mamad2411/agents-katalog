---
name: api-contracts
description: >
  REST API contracts for any stack: one field-casing convention on the wire, configured once in
  the serializer (default: snake_case), the standard envelope, prefix and versioning, mandatory
  pagination for list endpoints (offset vs cursor, when to use each, the canonical Page /
  PageMeta / CursorPage shapes, server-side filters, sort direction, active vs history split),
  DTOs as the contract (validation at the boundary, output shapes, no entity leakage), required
  HTTP security headers, and rate limiting (where, keys, 429 + Retry-After). Invoke
  automatically when creating or reviewing endpoints, input/output DTOs, pagination, filters, or
  API versioning, in any language or framework.
---

# API Contracts

> **How to read the examples.** Every example in this skill is framework-free TypeScript —
> plain interfaces and functions, no decorators, no framework, no validation, database or
> HTTP-client library. Read it as pseudo-code and translate it to the project's language and
> idioms. Stack-specific implementations (DTO classes and the validation library, the cursor
> queries against the project's database client, the security-headers plugin, the rate
> limiter, the client-side infinite-list hook) live in stack plugins — e.g.
> `dev-patterns:api-contracts` for NestJS/Fastify + Supabase — and in the project's own delta
> skill (`.claude/skills/<project>-api-contracts/`), when they exist. Load them together with
> this skill.

## Field naming on the wire — one casing convention for the whole API

**One casing convention for the whole API** — every field name in JSON request bodies, JSON
response objects and query parameters uses it, with no endpoint-by-endpoint exceptions.
**This plugin's default is snake_case** (the examples below use it); camelCase is an equally
valid choice if the project decides so — what is never acceptable is mixing both.

```
✅ (snake_case default)  access_token   resource_id   item_type   per_page   is_active   next_cursor
❌ (mixed in one API)    access_token   resourceId    item_type   perPage    is_active   nextCursor
```

Internal code (variables, function parameters, private fields) follows the language's own
convention. The mapping happens at the edge and is **configured once in the serializer**, not
hand-written per DTO — e.g. Jackson `PropertyNamingStrategies.SNAKE_CASE` (Java/Spring),
`System.Text.Json` `JsonNamingPolicy.SnakeCaseLower` (.NET), a Pydantic `alias_generator`
(Python/FastAPI), struct tags `json:"resource_id"` (Go), or explicit snake_case names in the
output DTO / mapper (TypeScript). The contract types that clients consume (shared types
package or OpenAPI schema) declare the same names.

Why this matters: most type systems do not check across the HTTP boundary. A field returned in
the wrong casing silently appears as `undefined`/`null` on a client whose contract type
declares the other casing — no compile error, no runtime warning. **A contract test that
rejects keys in the other casing** verifies the convention (`dev-core:test-patterns` →
contract tests).

**Verification rule:** before finishing a use case, confirm that every returned field name
matches exactly the field name declared in the API contract (shared type or OpenAPI schema)
for that response.

---

## Standard envelope

The error envelope (`{ error: { code, message, details } }`) is mandatory; the success envelope
(`{ data }`) is a per-project choice applied to every endpoint or to none. Both, and the
validation-error shape, are defined in `dev-core:error-handling` — do not redefine them per
endpoint. List endpoints add a `meta`
object (see pagination below).

Never a raw top-level array — a list is always an object with an `items` (or `data`) key, so
fields can be added later without breaking clients. This includes bounded, unpaginated lists
(`{ "items": [ ... ] }`, no `next_cursor`). Follow the project's success-envelope choice
(`dev-core:error-handling`, which also shows how each list shape appears in each mode). A
non-wrapping project that already returns bare arrays for bounded lists may keep doing so
consistently; new projects and new endpoints use `{ items }`.

## Prefix and versioning

```
All endpoints: /api/v1/<resource>
```

Breaking changes (removing or renaming a field, changing a type or a status code's meaning) →
new version `/api/v2/`. The old version remains active for 6 months. Additive changes (a new
optional field, a new endpoint) stay in the current version.

---

## Mandatory pagination for list endpoints

Every endpoint that returns a list that can grow is paginated. Two shapes — choose by how the
list is consumed.

| | Offset (`page` / `per_page`) | Cursor (`cursor` / `limit`) |
|---|---|---|
| Use for | Tabular/admin lists that need a total count or jump-to-page | Chronological/timeline lists the user scrolls through (activity feed, event log, history) and any list ordered by a timestamp |
| Cost | Grows with page depth (`OFFSET n` scans and discards n rows) | Constant regardless of depth |
| Concurrent inserts | Items shift — skipped or repeated | Stable — anchored to the last row seen |
| Total count | Yes | No |

### Offset pagination

```
GET /api/v1/resources?page=1&per_page=20&sort_by=created_at&sort_order=desc
```

Defaults: `page=1`, `per_page=20`, maximum `per_page=100`.

```json
{
  "data": [ ... ],
  "meta": { "page": 1, "per_page": 20, "total": 243, "total_pages": 13 }
}
```

The page types (`PageParams`, `PageMeta`, `Page<T>`) are canonical contract types, defined
once in the project's wire-contract source (shared types package, or the OpenAPI schema the
clients are generated from) — never redefined per module. Their shape:

```typescript
export interface PageParams {
  page: number;      // 1-based; default 1
  per_page: number;  // default 20, clamped server-side to max 100
}

export interface PageMeta {
  page: number;
  per_page: number;
  total: number;        // total matching rows (one COUNT query)
  total_pages: number;  // ceil(total / per_page); 0 when total is 0
}

export interface Page<T> {
  data: T[];
  meta: PageMeta;
}
```

### Cursor pagination

```
GET /api/v1/projects/:project_id/events?cursor=<opaque>&limit=20
```

```json
{ "items": [ ... ], "next_cursor": "MjAyNC0wNS0yOFQxNDozMjowMC4wMDBafGExYjI=" }
```

`next_cursor` is `null` on the last page. No total, no page count. Keep this shape identical
across every cursor endpoint of the API (how it relates to the success envelope follows the
project's envelope rule — `dev-core:error-handling`).

Rules:

- **Anchor on the last row actually seen:** `WHERE (sort_col, id) < (:cursor_sort, :cursor_id)`
  for newest-first (row-value comparison — PostgreSQL, MySQL, SQLite). On databases without
  row-value comparison (SQL Server, Oracle) use the expanded form:
  `WHERE sort_col < :cursor_sort OR (sort_col = :cursor_sort AND id < :cursor_id)`.
  Sort by `(sort_col, id)` — the `id` tie-breaker is required, timestamps aren't unique.
- **The cursor is opaque** to the client: an encoding of `sort_value|id` (e.g. base64). Decode
  defensively — an invalid cursor is treated as "no cursor", not a 500.
- **The cursor is untrusted input.** The client can send any bytes. Validate every decoded
  field before it reaches a query: `id` must be a UUID (or whatever the id type is), and
  `sort_value` must match the sort column's type — a timestamp pattern, or a safe-text pattern
  that excludes the query language's syntax characters. Prefer bound parameters; **never
  interpolate an unvalidated value into a filter string** (e.g. a PostgREST `or=(...)`, an
  OData `$filter`, a hand-built `WHERE`) — a crafted cursor would inject filter syntax.
  Choose the pattern so every value the column can legitimately hold passes; otherwise a real
  cursor is rejected and the client gets page one again.
- **Fetch `limit + 1` rows** to detect a next page without a `COUNT` query.
- **Clamp `limit` server-side** (default 20, max 50) — never trust the client value.

```typescript
// The canonical cursor page shape — defined once, next to Page<T>, in the wire-contract source.
export interface CursorPage<T> { items: T[]; next_cursor: string | null; }

export function encodeCursor(sortValue: string, id: string): string {
  return base64Encode(`${sortValue}|${id}`);
}

const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
// ISO-8601 timestamp as the database returns it, e.g. 2026-05-28T14:32:00.123456+00:00
const TIMESTAMP_RE = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?(Z|[+-]\d{2}:\d{2})$/;
// Letters, digits, space, '_' and '-' only — no , . ( ) " \ : or other filter syntax
const SAFE_TEXT_RE = /^[\p{L}\p{N} _-]{1,200}$/u;

export type CursorSortKind = 'timestamp' | 'text';

export function decodeCursor(
  cursor: string,
  sortKind: CursorSortKind = 'timestamp',
): { sortValue: string; id: string } | null {
  try {
    const decoded = base64Decode(cursor);
    const sep = decoded.lastIndexOf('|');
    if (sep <= 0) return null;
    const sortValue = decoded.slice(0, sep);
    const id = decoded.slice(sep + 1);
    if (!UUID_RE.test(id)) return null;
    const pattern = sortKind === 'timestamp' ? TIMESTAMP_RE : SAFE_TEXT_RE;
    return pattern.test(sortValue) ? { sortValue, id } : null;   // validated before any query
  } catch { return null; }
}

// Called with limit + 1 rows.
export function toCursorPage<T>(rows: T[], limit: number, cursorOf: (last: T) => string): CursorPage<T> {
  const hasMore = rows.length > limit;
  const items = hasMore ? rows.slice(0, limit) : rows;
  const last = items[items.length - 1];
  return { items, next_cursor: hasMore && last ? cursorOf(last) : null };
}

export const DEFAULT_PAGE_LIMIT = 20;
export const MAX_PAGE_LIMIT = 50;
export function parseLimit(raw: string | undefined): number {
  const n = raw ? parseInt(raw, 10) : DEFAULT_PAGE_LIMIT;
  return !Number.isFinite(n) || n < 1 ? DEFAULT_PAGE_LIMIT : Math.min(n, MAX_PAGE_LIMIT);
}
```

**Sort direction.** Newest-first uses `<`; an ascending list (e.g. alphabetical by `name`)
uses the mirror-image cursor — `ascending` on both sort columns and `>` instead of `<` ("resume
strictly *after* this row"). Everything else is identical; the comparison flips with sort
direction, not with the pagination mechanism.

**Filters are applied server-side, inside the same paginated query** — never client-side on
top of an already-paginated page. Filtering a page of `limit` items on the client can leave
fewer visible rows (or zero) even though more matching rows exist further down, because the
cursor already advanced past them. One endpoint, one `status` query param
(e.g. `active` / `resolved` / `all`), one repository method that filters and paginates
together. This also replaces pairs of separate non-paginated endpoints (e.g. `/projects` +
`/projects/archived`) with one paginated, filtered endpoint — prefer it when you find that
shape. On the client, the filter is part of the list's cache key so each tab paginates
independently.

**Split "active" from "history" when only one slice grows without bound.** A list mixing
open items (bounded — a parent has a handful open at once) with closed/terminal items
(accumulates forever) should not be paginated uniformly:

- `GET /projects/:project_id/<resource>` — open statuses only, unpaginated:
  `{ "items": [ ... ] }` (no `next_cursor`) — still an object, never a bare array.
- `GET /projects/:project_id/<resource>/history` — terminal statuses, cursor-paginated.

The client combines them per tab (`[...active.items, ...history]` for an "All" tab) and gates the
infinite-scroll wiring on the tabs that read history.

**Cursor sort column:** prefer a column that's always present and monotonic, even if it's not
the "ideal" business date — e.g. `created_at` (always set) rather than `completed_at` (null for
cancelled rows); the screen can still re-order each loaded page by the business date. When the
history holds a single terminal status whose business date is always set, that date can be the
cursor column. Sort direction is independent of the split.

---

## DTOs are the contract

- **Input DTOs** — one per endpoint, validated at the boundary (the interface adapter) before
  the use case runs: types, required fields, ranges, enums, array element types. Validation
  failures become `VALIDATION_ERROR` (`dev-core:error-handling`). Unknown fields are stripped
  or rejected, never passed through. The domain never validates DTOs.
- **Output shapes** — plain data types (no behavior, no framework annotations), in the API's
  casing convention, matching the contract type exactly. Dates and timestamps are ISO 8601 strings, not
  language date objects.
- **No entity leakage** — never serialize a domain entity, an ORM/database row or an aggregate
  directly. Map explicitly to the output shape in the use case or a mapper it owns — never in
  the entity (`dev-core:clean-architecture`) — so internal fields, renamed columns and secrets
  never reach the wire by accident.

```typescript
// Input — keys exactly as they arrive in the HTTP body (snake_case, this plugin's default)
export interface CreateOrderDto {
  name: string;           // required, non-empty
  quantity: number;       // >= 0
  order_type: OrderType;  // one of the enum values
  order_details: Record<string, unknown>;
}

// Output — plain shape, matches the shared contract type exactly
export interface OrderResponse {
  id: string;
  name: string;
  quantity: number;
  unit: string;
  order_type: OrderType;
  is_active: boolean;
  item_count: number;
  created_at: string;     // ISO 8601 string, not a Date (serialized over HTTP)
}
```

---

## HTTP security headers (required on every response)

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
```

| Header | Why |
|---|---|
| `Strict-Transport-Security` | Browsers only ever reach the API over HTTPS — no downgrade to plain HTTP |
| `X-Content-Type-Options: nosniff` | Browsers don't reinterpret a JSON/text response as script or HTML |
| `X-Frame-Options: DENY` | No page of the API can be framed (clickjacking) |
| `Content-Security-Policy` | Limits where scripts, styles and other resources may load from — the main XSS mitigation for any HTML the server returns |
| `Referrer-Policy` | Full URLs (which may carry tokens or IDs) aren't leaked to other origins |

Set them once, globally, at the edge — not per route.

---

## Rate limiting

Required on every API. Default limits:

```
Authentication endpoints:  stricter per-route limits — see dev-core:auth-security
Public endpoints:        100 req / 1min per IP
Authenticated endpoints: 300 req / 1min per user
Export/PDF endpoints:     10 req / 1h per user
```

- **Where:** a global safety-net limit for the whole API at the edge, plus tighter per-route
  limits on sensitive or expensive endpoints (auth, invites/spam-prone, exports, anything that
  sends email or costs money per call).
- **Keys:** per client IP for unauthenticated routes; per user ID for authenticated ones.
  Behind a reverse proxy/load balancer, trust the proxy's forwarded-for header, otherwise every
  request resolves to the proxy's IP and per-IP limiting becomes a no-op.
- **Shared counters:** in-memory counters are per instance. Once the API runs more than one
  replica, move the counters to a shared store (e.g. Redis) or the limits are per-instance
  instead of global.
- **Response:** `429 Too Many Requests` with the standard error envelope and a `Retry-After`
  header (seconds until the window resets), so clients can back off instead of retrying
  immediately.
- Keep the named limit profiles in one place so a policy change is a one-line edit.

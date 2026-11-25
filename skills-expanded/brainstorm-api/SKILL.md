---
name: brainstorm-api
description: "docs/plan/API.md: the contract between client and server before either is built: conventions (base path, auth, error shape, pagination, ids, dates, money), every route with its method, input, output and status codes, the shared types, and events or webhooks. The text briefs copy as the contract. Read when planning work where a client talks to a server."
---

# API.md: the contract parts build against

The frontend and backend parts run at the same time, so neither can wait
to see what the other made. The contract is what lets them meet: the same
route, the same field names, the same error codes. Written in a brief it
is lost after the run; written here it is read by every part, by `test`,
and by the next feature.

## 1. The template

````markdown
# API

Base: /api. JSON in and out, camelCase fields. Auth: session cookie; routes marked 🔒 need it.
Errors: { "code": "not_found", "message": "…" } with the status below. Codes are stable; messages are for people.
Pagination: ?cursor=&limit= (default 20, max 100) → { items, nextCursor } (null at the end).
Money: { amountMinor: 12500, currency: "IDR" }. Dates: ISO 8601 UTC. IDs: strings.

## Types
```ts
type Product = { id: string; slug: string; name: string; price: Money; imageUrl: string; categoryId: string };
type Money = { amountMinor: number; currency: string };
type Cart = { id: string; items: CartItem[]; total: Money };
type CartItem = { productId: string; name: string; qty: number; price: Money };
```
Lives in src/shared/types.ts (written in the foundation wave).

## Products
| Method | Path | Input | Output | Errors |
|---|---|---|---|---|
| GET | /products | ?cursor&limit&category | 200 { items: Product[], nextCursor } | 400 bad_filter |
| GET | /products/:slug | | 200 Product | 404 not_found |

## Cart 🔒
| Method | Path | Input | Output | Errors |
|---|---|---|---|---|
| POST | /cart/items | { productId, qty } (qty 1–99) | 201 Cart | 404 not_found, 409 out_of_stock, 422 invalid |
| PATCH | /cart/items/:productId | { qty } (0 removes) | 200 Cart | 404 not_found, 422 invalid |

## Events
- order.paid → POST to the email service with { orderId }; retried with backoff; idempotent by orderId.
````

## 2. Conventions first

Write the rules every route follows once, at the top: base path, format,
field case, auth, the error shape and its codes, pagination, how money,
dates and ids travel. Then each route only states what differs. Follow
`ARCHITECTURE.md`'s shared facts and `ERD.md`'s names (the API may shape
data differently from the table, but it names things the same way).

## 3. Routes

- Resources as nouns, grouped by resource. Methods by meaning: GET reads
  and never changes anything, POST creates or runs an action, PATCH
  changes part, PUT replaces, DELETE removes.
- For each: input (path, query, body, with limits: "qty 1–99"), output
  with its status, and every error a client must handle, by code.
- Status codes that mean what they say: 201 created, 204 nothing to
  return, 400 malformed, 401 not signed in, 403 not allowed, 404 not
  found (also for what exists but the caller may not know about), 409
  conflict with current state, 422 valid JSON with invalid values, 429 too
  many requests.
- Mark which routes need auth and which role, and which are public.
- Only the routes the Must requirements need. Each route traces to an
  `FR-n`.

## 4. Types

Shared types in one block, in the language the project uses (TypeScript
for a TypeScript project; otherwise JSON examples), and one file in the
codebase where they live, named in `ARCHITECTURE.md`. The briefs name
that file; nobody redefines the types.

## 5. Other interfaces

Server-sent events or websockets (event names and payloads), webhooks in
and out (who calls whom, signature checks, retries, idempotency keys),
jobs a request starts (what the client polls or is told). Same rigour as
routes.

## 6. Becoming the brief's contract

The contract section of each brief (`orchestration`, section 4) is the
lines of this document the part touches, copied exactly. When a part has
to change a route, it reports it; the orchestrator updates `API.md` first,
then tells the other side.

## Check it

- Every route traces to a requirement and every screen's data has a route.
- Every route lists its errors with status and code.
- Field names match `ERD.md` and the shared types; money, dates and ids
  follow the conventions.
- Auth is stated for every route.

## Avoid

Routes invented for completeness; verbs in paths (`/getProducts`);
200 with an error inside; errors without stable codes; types defined in
two places; a brief's contract that differs from this file.

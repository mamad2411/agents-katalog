---
name: rest-api-design
description: >
  The design rules for an HTTP/REST surface an agent can follow unattended — resource naming,
  status-code selection, one error envelope per API, bounded pagination, idempotency, and what
  counts as a breaking change. Use when adding or changing an HTTP endpoint, reviewing an
  OpenAPI or contract diff, deciding a status code or a URL shape, or judging whether an API
  change is safe to ship.
---

# REST API Design

An HTTP surface is a published contract: once a path, a status code or an error token reaches a
client, taking it back costs a version. An agent adding one endpoint sees only that endpoint,
which is how an API ends up with two error shapes, three pagination styles and a verb in a URL.

This skill is the *what the surface must look like*. Framework idioms, layering and the project's
verification commands live in its `.claude/rules/` files and its `api-endpoint` playbook.

## Discover before you design

The first action is never to invent. Read the neighbouring operation and the contract file, then
copy their decisions:

```bash
grep -rn 'HandleFunc\|@app.route\|router\.\(get\|post\)\|@RestController' <src>   # the route table
grep -rn 'error.*code.*message' <contract-dir>                                    # the error envelope
```

What those two greps return outranks every default below. A second convention standing next to an
existing one is the defect this skill exists to prevent — a finding even when the new convention
is the better one in isolation.

## Resource naming

| Rule | Correct | Wrong |
|---|---|---|
| Collections are plural nouns | `/v1/accounts` | `/v1/account`, `/v1/getAccounts` |
| No verb in a path — the method is the verb | `GET /v1/accounts/{id}` | `GET /v1/fetchAccount/{id}` |
| Nest only for true containment, never past `/collection/{id}/subcollection/{id}` | `/v1/accounts/{id}/transfers/{transferId}` | `/v1/regions/{r}/banks/{b}/accounts/{id}/transfers` |
| Multi-word segments are `kebab-case` | `/v1/payment-methods` | `/v1/paymentMethods`, `/v1/payment_methods` |
| Identity in the path, filters in the query string | `/v1/accounts/{id}`, `/v1/accounts?status=frozen` | `/v1/accounts?id=acc-1001` |
| A non-CRUD action is a sub-resource | `POST /v1/accounts/{id}/freeze` | `POST /v1/freezeAccount` |

## Status codes

| Outcome | Code |
|---|---|
| Created with a new identity | `201` + `Location` header |
| Accepted, work happens asynchronously | `202` |
| Succeeded, deliberately no body | `204` |
| Malformed syntax or failed validation | `400` |
| No credentials, or credentials not understood | `401` |
| Authenticated, not permitted | `403` |
| Identifier does not exist | `404` |
| State conflict, concurrent update, duplicate | `409` |
| Well-formed but semantically invalid | `422` *only if this API already uses 422* — otherwise `400` |
| Rate-limited | `429` |

Precedence is fixed: **authentication before authorization before existence.** An unauthenticated
caller gets `401` whether or not the resource exists. A caller who may not see a resource gets the
same answer for a real id and a fake one — never leak existence through a `404`/`403` difference.

## One error envelope

An API has exactly one error body shape. Reuse the one the repo already returns; if none exists,
define it once and record it in the contract.

- Never mix RFC 7807 `title`/`detail` into an API that already returns
  `{"error":{"code":"…","message":"…"}}`, or the reverse.
- `code` is a stable machine token. Once shipped it never changes meaning and is never renamed —
  clients branch on it.
- `message` is for a human reading a log. It may change in any release; nothing may parse it.
- Never return internal exception text, SQL, a file path or a stack trace. Log those; return the
  token.

## Collections

Every collection endpoint is paginated from its first commit — retrofitting pagination is a
breaking change.

- Bounded page size with a stated default and maximum: **default 20, maximum 100**, unless the
  project already uses other numbers.
- A `limit` above the maximum is a `400`. Never silently clamp: the caller then believes it has
  the whole page.
- Cursor pagination when rows can be inserted or reordered under the reader; offset only for
  stable admin-style listings. A cursor needs a deterministic total order — name the tie-breaker
  column (usually the primary key) and sort by it.
- An empty result is `200` with an empty array. Never `404`, never a null body.
- Filtering and sorting are query parameters against a closed allow-list of fields. Never a
  passthrough expression, a raw predicate, or a client-supplied column name.

## Idempotency and side effects

| Method | Safe | Idempotent |
|---|---|---|
| `GET`, `HEAD` | yes | yes |
| `PUT`, `DELETE` | no | yes |
| `POST`, `PATCH` | no | no |

A `GET` that mutates state is a defect, not an optimisation — caches, prefetchers and retries all
assume otherwise. A `POST` that moves money, provisions a resource or sends a message accepts an
`Idempotency-Key` header, stores the key with the result, and returns the original response on
replay instead of acting twice.

## Evolution

| Change | Breaking? |
|---|---|
| Adding an optional request field, or a new response field | no |
| Adding a required request field | yes |
| Removing or renaming a response field | yes |
| Narrowing a type, a range, or an enum | yes |
| Adding a value to a response enum | yes for closed clients — document the unknown-value behaviour |
| Changing the status code for an existing outcome | yes |
| Changing the meaning of an existing error `code` | yes |

A breaking change ships behind a new version path segment with a deprecation window. It is never
applied in place. Deprecation is announced in the same commit as the decision: a `Sunset` header
on the old operation and `deprecated: true` in the contract.

## Non-negotiable

1. **Never invent a second error envelope** in an API that already has one.
2. **Never return `200` with an error body** — the status code is the outcome.
3. **Never ship an unbounded collection** endpoint.
4. **Never remove, rename or retype a published field** in place.
5. **Never put a secret, a token or a credential in a query string** — it lands in access logs,
   proxies and browser history.

## Review checklist

- [ ] Path is a plural noun with no verb, `kebab-case`, nested at most one level
- [ ] Every outcome maps to the status code in the table; auth precedes existence
- [ ] The error body is the API's existing envelope, with a stable `code`
- [ ] Collection is paginated, bounded, `400` above the maximum, empty page is `200 []`
- [ ] Sort and filter fields come from a closed allow-list
- [ ] Mutating verb is not `GET`; a money-moving `POST` takes an `Idempotency-Key`
- [ ] No published field, path or error code was removed or retyped without a new version

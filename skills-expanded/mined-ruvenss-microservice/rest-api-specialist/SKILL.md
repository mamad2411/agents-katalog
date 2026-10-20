---
name: rest-api-specialist
description: REST API industry-standard design and review. Use when defining endpoints, choosing HTTP methods/status codes, designing error formats, versioning, pagination, auth, caching headers, or writing/validating OpenAPI specs.
---

# REST API Specialist

Apply industry standards (RFC 9110/9111 HTTP semantics, RFC 9457 Problem Details, OpenAPI 3.1) — not preference.

## Checklist for any endpoint
- **Resource & URI**: plural nouns, shallow nesting, no verbs in paths. Filter/sort/paginate via query params.
- **Method semantics**: GET (safe, cacheable), PUT/DELETE (idempotent), POST (not). PATCH for partial updates.
- **Status codes**: 200/201 (+`Location`)/204; 400 vs 401 vs 403 vs 404; 409 conflict; 422 validation; 428/412 optimistic concurrency; 429 rate limit.
- **Errors**: `application/problem+json` with stable machine `type`/`code` + human `title`/`detail` + field errors.
- **Pagination**: cursor/keyset for large or active data; offset only when acceptable. Return paging metadata + links.
- **Versioning**: pick one (`/v1` or media-type), apply consistently, additive-only within a version.
- **Concurrency/cache**: ETag + If-Match on updates; Cache-Control/Last-Modified; idempotency keys for critical retried writes.
- **Auth**: bearer/OAuth2/API key over TLS; never secrets in URIs; scope + rate-limit.

## Output
When designing: resource model → endpoint table (method, path, status codes, request/response schema, errors, auth). When reviewing: cite the violated rule and give the corrected version. Prefer contract-first OpenAPI with accurate schemas and examples.

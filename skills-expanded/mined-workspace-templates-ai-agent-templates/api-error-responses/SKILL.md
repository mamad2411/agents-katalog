---
name: api-error-responses
description: Defines one error format with stable machine codes and problem details, then applies it to every endpoint so clients can handle failures reliably.
---

# API error responses

One error shape, one place that produces it.

## Steps

1. Inventory first. Grep for every place that builds an error response (`res.status(4`, `raise HTTPException`, `ResponseEntity.badRequest`, exception handlers). List the distinct shapes you find.
2. Define the envelope, based on RFC 9457: `type` (a stable URL or slug), `title`, `status`, `detail`, `instance` (the request id), plus `code` (SCREAMING_SNAKE, stable forever) and, for validation, `errors: [{ field, code, message }]`.
3. Build one error class and one global handler. Domain code throws typed errors; only the handler touches status codes and serialization. Set `Content-Type: application/problem+json`.
4. Map consistently: 400 malformed input, 401 no identity, 403 identity but not allowed, 404 missing or hidden, 409 state conflict, 422 failed validation, 429 limited, 500 unexpected.
5. Migrate endpoint by endpoint. Add a contract test per status that asserts the full body shape.

## Rules

- Never return a stack trace, SQL text, file path or internal hostname. Log them with the request id instead.
- Never change a published `code`; add a new one and deprecate the old.
- Messages are for humans and may change; clients switch on `code` only.
- Unexpected errors return a generic 500 body with the request id and nothing else.
- Do not use 200 for failures.

## Report

The shapes found, the new envelope, the files changed, and endpoints you left on the old format with the reason.

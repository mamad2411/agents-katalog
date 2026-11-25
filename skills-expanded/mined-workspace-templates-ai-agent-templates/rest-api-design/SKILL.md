---
name: rest-api-design
description: "Designs or reviews HTTP APIs: resource names, methods, status codes, pagination, error format and versioning, with a short spec before any code."
---

# REST API design

Settle the contract before writing handlers.

## Steps

1. Read the existing API first: naming, casing, auth, error format, pagination. Match it unless asked to change it.
2. Model resources as plural nouns: `GET /orders`, `GET /orders/{id}`, `POST /orders`, `PATCH /orders/{id}`, `DELETE /orders/{id}`. Nest only one level (`/orders/{id}/items`). Actions that fit no resource get a sub-resource verb (`POST /orders/{id}/cancel`).
3. Use methods correctly: GET and DELETE are safe to retry, PUT replaces, PATCH changes fields, POST creates. Make POST retry-safe with an `Idempotency-Key` header for payments or anything with side effects.
4. Return precise status codes: 200, 201 with `Location`, 204, 400 malformed, 401 not logged in, 403 not allowed, 404, 409 conflict, 422 invalid fields, 429 with `Retry-After`. Never 200 with an error in the body.
5. Use one error shape everywhere: `{"error":{"code":"out_of_stock","message":"...","fields":[{"name":"qty","issue":"..."}]}}`. The code is stable and machine-readable.
6. Paginate every list: cursor-based (`?limit=50&cursor=...`) with a hard maximum and a `next` cursor. Filter and sort with named query params.
7. Version in the path (`/v1`) and only for breaking changes. Adding optional fields is not breaking; removing, renaming or changing a type is.
8. Write the spec (OpenAPI or a table) and get it confirmed before implementing.

## Report

The endpoint table, an example request and response for each, and a list of breaking changes with a migration path.

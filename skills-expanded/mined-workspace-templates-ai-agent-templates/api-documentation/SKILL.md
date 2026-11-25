---
name: api-documentation
description: Documents HTTP endpoints from the real handlers, with request and response examples, error cases and auth, so integrators succeed on the first call.
---

# API documentation

Document what the code does, not what the design doc hoped it would do.

## Steps

1. Find the surface: route definitions, controllers, OpenAPI or schema files, validators, middleware. List every endpoint with method and path before writing anything.
2. For each endpoint read the handler to learn the real parameters, which are required, defaults, size limits and the shape of the success body. Read the validator for exact constraints.
3. Collect error behavior: which status codes can come back, the error body format, and the trigger for each (missing field, bad token, not found, conflict, rate limit).
4. Write one shared section first: base URL, authentication (header name, token format, how to get a key, expiry), pagination style, rate limits, versioning, idempotency.
5. Write each endpoint as: purpose in one line; `curl` example with realistic values; request parameters as a table (name, type, required, notes); success response with a real JSON body; error table.
6. If a test or local server exists, run the curl examples and paste the real output.

## Rules

- Use dummy values like `YOUR_API_KEY`, never real secrets.
- Mark undocumented or deprecated behavior as such; do not hide it.
- Keep field names exactly as the code spells them.
- Do not invent endpoints, fields or status codes.

## Report

The docs file path, the endpoints covered, the examples you ran, and mismatches found between code and any existing spec.

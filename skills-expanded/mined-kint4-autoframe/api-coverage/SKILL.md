---
name: api-coverage
description: Map API endpoints against existing API tests to show what is tested and what is missing. Use when the user runs /api-coverage or asks which endpoints are covered.
---

# /api-coverage — Map API Test Coverage

**Type:** API
**Description:** Maps API endpoints against existing API tests, showing which endpoints and methods are tested and which are missing.

---

## Input Format

Optional:
- A list of endpoints (pasted, OpenAPI/Swagger spec, or via connector)
- A feature scope

With no input, map all existing API specs under `tests/api/`.

## Output Format

A coverage table:

| Endpoint | Method | Tested | Cases covered (success / auth / invalid / error) |
|---|---|---|---|

Plus a prioritized list of gaps with the suggested skill to close each.

## Step-by-Step Instructions

1. Enumerate every `*.api.spec.ts` under `tests/api/`.
2. Parse each test to extract the endpoint, method, and which case types it covers (success / 401 / 400 / error).
3. If an endpoint list or OpenAPI spec was provided, align tests to it; otherwise infer the endpoint set from existing tests.
4. Mark each endpoint+method as fully tested, partially tested (missing case types), or untested.
5. Render the coverage table.
6. List gaps in priority order and recommend `/new-api-spec` to close each.

## Rules

- A method isn't "covered" unless success, auth failure, and invalid input are all tested.
- Read specs, don't execute them.
- Be explicit about assumptions when no endpoint list is provided.

---
name: mcp-api-tester
description: "MCP API Test Tool — HTTP endpoint tests, smoke testing, contract verification, and integration tests. Use when testing MCP or HTTP API endpoints."
---

# MCP API Test Tool (MCP API Tester)

## Overview

MCP API Tester is a skill designed to test API endpoints over the MCP protocol. It provides the capabilities to construct HTTP requests, validate responses, execute contract tests against OpenAPI schemas, and run rapid smoke tests. It is designed to accelerate developer feedback loops and detect regressions early during the API development cycle.

**Core principle:** EVERY TEST MUST BE AUTOMATED AND REPEATABLE — MANUAL API TESTING IS UNRELIABLE.

## The Iron Law

```
NO API TEST IS COMPLETE WITHOUT RESPONSE VALIDATION. STATUS CODES, RESPONSE SCHEMAS, AND HEADERS MUST BE EXPLICITLY VALIDATED FOR EVERY REQUEST.
```

## When to Use

**Use this when:**
- You are developing a new API endpoint and need to verify it behaves correctly.
- You modified an existing API and need to ensure no regressions occurred.
- You need to confirm an API complies with its OpenAPI specification.
- You need to run smoke tests in a CI/CD pipeline.

**Use this ESPECIALLY when:**
- You consider "I'll just test this quickly with curl" — MCP API Tester is faster, structured, and repeatable.
- You say "it probably works already, no need to test it" — this is exactly why automated tests must be run.
- You are concerned that an API change might break downstream consumers.

**Don't skip when:**
- The API is still in the analysis or design phase (no code written yet).
- There is no endpoint available to test (implementation has not begun).
- You lack the credentials (auth tokens, API keys) required to access the API.

## Phase 1: Test Plan and Request Configuration

**BEFORE proceeding:**

1. **Define test scenarios** — identify endpoints, HTTP methods, and expected status codes.
2. **Configure request components** — headers, request bodies, query parameters, and path variables.
3. **Configure authentication** — Bearer tokens, API Keys, Basic Auth, or OAuth2 configurations.
4. **Define environment variables** — set up configurations for development, staging, or production target endpoints.

```
mcp-api-tester request build \
  --method POST \
  --url https://api.example.com/v1/users \
  --header "Content-Type: application/json" \
  --auth bearer --token "{{AUTH_TOKEN}}" \
  --body '{"name": "Test User", "email": "test@example.com"}'
```

## Phase 2: Request Execution and Raw Response Capture

**BEFORE proceeding:**

1. **Execute the request** — send the configured request via the MCP client.
2. **Capture raw responses** — log status codes, headers, response bodies, and execution times.
3. **Handle error states** — capture 4xx, 5xx, timeouts, and DNS resolution failures.

```
mcp-api-tester request send --request-id req-123
mcp-api-tester response raw --request-id req-123
```

## Phase 3: Response Validation

**BEFORE proceeding:**

1. **Verify status codes** — check that the returned HTTP status code matches the expected code.
2. **Verify response schemas** — confirm that the JSON payload structure conforms to the target schema.
3. **Verify headers** — check that headers like Content-Type, Cache-Control, or CORS are set correctly.
4. **Verify response latency** — check that response times are below the defined performance threshold.

```
mcp-api-tester validate status --request-id req-123 --expected 201
mcp-api-tester validate schema --request-id req-123 --schema '{"type": "object", "properties": {"id": {"type": "integer"}, "name": {"type": "string"}}}'
mcp-api-tester validate header --request-id req-123 --name Content-Type --expected "application/json"
mcp-api-tester validate timing --request-id req-123 --max-ms 500
```

## Phase 4: OpenAPI Contract Testing

**BEFORE proceeding:**

1. **Load the OpenAPI specification** — load the Swagger or OpenAPI document.
2. **Check endpoint coverage** — verify that the endpoint under test is declared in the specification document.
3. **Compare schema definitions** — validate actual request/response shapes against their specification models.
4. **Report schema deviations** — highlight missing endpoints or deviations in payload definitions.

```
mcp-api-tester contract load --spec openapi.yaml
mcp-api-tester contract validate --request-id req-123 --spec openapi.yaml
mcp-api-tester contract diff --spec openapi.yaml --live https://api.example.com/v1
```

## Phase 5: Executing Smoke Test Suites

**BEFORE proceeding:**

1. **Define smoke test scenarios** — include health checks, basic CRUD sequences, and authentication flows.
2. **Determine test sequence** — configure execution order if endpoints depend on prior steps.
3. **Execute the suite** — run the smoke tests sequentially or in parallel.
4. **Collect the summary report** — view passed/failed steps along with detailed error traces.

```
mcp-api-tester smoke create --name health-check --endpoint GET /health --expected 200
mcp-api-tester smoke create --name user-crud --steps "POST /users -> GET /users/:id -> PUT /users/:id -> DELETE /users/:id"
mcp-api-tester smoke run --suite smoke-suite
mcp-api-tester smoke report --suite smoke-suite
```

## Phase 6: Final Verification

Before marking complete:

- [ ] Have all requests been executed and their responses captured?
- [ ] Is the status code verified for every response?
- [ ] Is the response body structure and data types validated?
- [ ] Has OpenAPI contract validation been executed successfully?
- [ ] Did all tests in the smoke suite pass successfully?
- [ ] Have error reports been generated for any failing test cases?
- [ ] Are sensitive tokens or keys scrubbed from the final test logs?

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I will check the response manually; there's no need to write validation rules."
- "The status code is 200, so the response is correct; I don't need to check the body."
- "The OpenAPI spec is out of date anyway; I will skip contract testing."
- "Setting up a test suite takes too long; I'll run these individually."
- "This test failed, but it is probably just a temporary environment issue."

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "The API is up, but it is returning invalid property types." — You missed response body validations.
- "This endpoint is not documented in the specification." — You skipped OpenAPI contract testing.
- "The tests passed, but the service failed in production." — Your smoke test suite was incomplete or skipped.
- "Why are there so many unstructured test cases?" — You added tests without defining a clear plan.
- "The API key was written in the report." — You exposed credentials in the test output.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Manual inspection is faster than writing validation rules." | Manual verification misses issues; automation enforces the same standards on every run. |
| "A 200 status code guarantees success." | An endpoint can return 200 while containing empty bodies or error payloads. Validate the schema. |
| "The spec is outdated, so contract tests are useless." | Update the specification; discrepancies between docs and code lead to integration issues. |
| "Running one-off tests is sufficient." | One-off tests are not reproducible and cannot be easily run in automated pipelines. |
| "Failing tests are flaky environment issues." | Flaky tests hide actual bugs. Investigate and resolve all failures. |

## Related Skills

- **mcp-db-connector** — Verify database state changes during API testing.
- **mcp-server-hub** — Integrate security testing tools (e.g., Nmap, Nuclei) to verify endpoints.
- **spec-first-development** — Align tests directly with defined specifications.

## Self-Review

After completing this process:

1. **Coverage Check:** Are all critical API endpoints covered in the test suite?
2. **Validation Rigor:** Are status codes, schemas, and key headers verified for all responses?
3. **Contract Alignment:** Do all endpoint schemas align with the OpenAPI spec?
4. **Suite Stability:** Can the smoke test suite be executed repeatedly without failures?
5. **Credential Integrity:** Are passwords and tokens removed from all reports?

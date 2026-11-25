---
name: api-docs
description: >
  Generate or update API documentation from code — endpoints, request/response
  schemas, authentication, error codes, and usage examples.
  TRIGGER when: user says /api-docs, asks to document an API,
  needs endpoint documentation, or wants OpenAPI/Swagger specs.
argument-hint: "[API, service, or endpoint to document]"
user-invocable: true
---

# API Documentation Generator

You are a technical writer creating clear, accurate API documentation. Generate docs that developers can use without asking follow-up questions.

## Process

### Step 1: Discover the API

- Read route definitions, controllers, and handlers
- Identify all endpoints (method + path)
- Determine authentication requirements
- Extract request/response schemas from types, validators, or examples
- Note rate limits, pagination, and versioning

### Step 2: Document Each Endpoint

For each endpoint:

### `METHOD /path`

**Description:** What this endpoint does in one sentence.

**Authentication:** Required / Optional / None (specify type: Bearer, API key, etc.)

**Parameters:**

| Name | In | Type | Required | Description |
|------|-----|------|:---:|-------------|
| `param` | path/query/header/body | string/number/etc. | Yes/No | *description* |

**Request Body:**
```json
{
  "field": "value"
}
```

**Response:**

| Status | Description | Body |
|--------|-------------|------|
| 200 | Success | `{ "data": ... }` |
| 400 | Validation error | `{ "error": "message" }` |
| 401 | Unauthorized | `{ "error": "message" }` |
| 404 | Not found | `{ "error": "message" }` |

**Example:**
```bash
curl -X METHOD https://api.example.com/path \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'
```

### Step 3: Document Cross-Cutting Concerns

- **Base URL** and environment URLs
- **Authentication** — how to obtain and use credentials
- **Rate limiting** — limits, headers, retry behavior
- **Pagination** — cursor vs. offset, page size limits
- **Error format** — standard error response structure
- **Versioning** — how versions are specified, deprecation policy

### Step 4: Review for Completeness

- Every endpoint is documented
- All parameters and fields are described
- Error responses cover common failure modes
- Examples are copy-paste ready and correct
- Types match the actual implementation

## Output Format

Structured markdown suitable for a docs site or README. Group endpoints by resource or domain. Include a table of contents for larger APIs.

## Edge Cases

- For GraphQL: document queries, mutations, types, and common query patterns
- For WebSocket: document connection, message types, and event flows
- For gRPC: document service definitions, message types, and streaming patterns
- If types are loose (e.g., plain JS): infer schemas from usage and note uncertainty

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners

---
name: api-test-plan
description: >
  Design API test suites — endpoint coverage, contract testing, error scenarios,
  authentication flows, and response validation strategies.
  TRIGGER when: user says /api-test-plan, "test this API", "API test coverage",
  "endpoint testing", "contract tests", or "API validation".
argument-hint: "[API name, OpenAPI spec, or endpoint list]"
user-invocable: true
---

# API Test Plan

You are a QA engineer designing comprehensive API test coverage. Ensure correctness, reliability, security, and contract compliance across all endpoints.

## Process

### Step 1: Inventory Endpoints

| Endpoint | Method | Auth Required | Request Body | Response Codes | Priority |
|----------|--------|--------------|-------------|---------------|----------|
| /api/v1/resource | GET | Yes | N/A | 200, 401, 404 | High |
| /api/v1/resource | POST | Yes | JSON | 201, 400, 401, 409 | High |

### Step 2: Test Categories

| Category | What to Test | Example |
|----------|-------------|---------|
| **Happy path** | Valid requests return correct responses | GET /users/1 returns user object |
| **Input validation** | Invalid inputs rejected with proper errors | POST with missing required field returns 400 |
| **Authentication** | Unauthenticated requests rejected | Missing token returns 401 |
| **Authorization** | Users can only access permitted resources | User A can't access User B's data |
| **Error handling** | Errors return consistent format and codes | Non-existent resource returns 404 |
| **Edge cases** | Boundary values, empty collections, unicode | GET /users?page=0, empty search results |
| **Contract** | Response schema matches documented contract | All fields present with correct types |
| **Idempotency** | Repeated requests produce same result | Double POST doesn't create duplicates |
| **Rate limiting** | Throttling works as documented | Exceeding limit returns 429 |
| **Pagination** | Pagination parameters work correctly | page, limit, cursor, total count |

### Step 3: Test Case Design

For each endpoint, generate test cases:

| Test Case | Endpoint | Method | Input | Expected Status | Expected Body | Priority |
|-----------|----------|--------|-------|----------------|---------------|----------|
| [Name] | [Path] | [Verb] | [Request details] | [Status code] | [Key assertions] | High/Med/Low |

### Step 4: Contract Testing

| Aspect | Validation |
|--------|-----------|
| Response schema | All required fields present with correct types |
| Backward compatibility | New fields are additive; existing fields unchanged |
| Error format | Consistent error object structure across all endpoints |
| Headers | Content-Type, pagination headers, rate limit headers |
| Versioning | API version behavior matches documentation |

## Output Format

```markdown
## API Test Plan: [API Name]

### Endpoint Inventory
[Complete endpoint table]

### Test Cases
#### [Endpoint Group]
[Test case table per endpoint]

### Contract Tests
[Schema validation rules]

### Authentication Test Matrix
[Auth scenario coverage]

### Environment & Data Setup
[Test data requirements and environment config]

### Execution
[How to run, CI integration, reporting]
```

## Quality Checklist

- [ ] Every endpoint has happy path and error path coverage
- [ ] Authentication and authorization tested for all protected endpoints
- [ ] Input validation covers type, length, format, and required/optional
- [ ] Response schemas are validated against contract
- [ ] Edge cases include empty results, max values, and special characters
- [ ] Test data setup and cleanup are defined

## Edge Cases

- **GraphQL APIs**: Test query depth limits, field-level authorization, and N+1 detection
- **Webhook endpoints**: Test signature validation, retry behavior, and idempotency
- **File upload endpoints**: Test size limits, content-type validation, and malicious file handling
- **Streaming / SSE endpoints**: Test connection lifecycle, reconnection, and backpressure

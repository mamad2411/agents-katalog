---
name: api-and-interface-design
description: Design stable, evolvable APIs and interfaces using contract-first methodology, rigorous boundary validation, and versioning strategies that respect Hyrum's Law.
---

# API & Interface Design

## Overview

API and interface design is the practice of defining contracts between systems — whether REST endpoints, GraphQL schemas, gRPC services, library APIs, or module boundaries. Every interface is a contract that, once published, becomes a liability. This skill provides a systematic approach to designing interfaces that are correct, evolvable, and resilient.

The fundamental insight: APIs are forever (or at least longer than you expect). Hyrum's Law states: "With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody." Design for this reality.

## When to Use

- Designing new REST, GraphQL, or gRPC API endpoints
- Defining module boundaries in a codebase
- Creating library/framework public APIs
- Adding fields to existing API responses
- Modifying existing interface contracts
- Setting up API gateways or BFF (Backend for Frontend) layers
- Writing OpenAPI / GraphQL schema / protobuf definitions
- Conducting API reviews
- Designing event schemas for message queues
- Establishing error handling conventions

## Process

### Step 1: Contract-First Design

Never write implementation before the contract. The contract is the source of truth.

**1a. REST contracts (OpenAPI 3.1):**

```yaml
openapi: 3.1.0
info:
  title: Document Service API
  version: 1.0.0
paths:
  /documents/{id}:
    get:
      operationId: getDocument
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: The document
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Document'
        '404':
          $ref: '#/components/schemas/NotFoundError'
```

**1b. GraphQL contracts (SDL):**

```graphql
type Query {
  document(id: UUID!): Document
}

type Document {
  id: UUID!
  title: String!
  content: String!
  createdAt: DateTime!
  updatedAt: DateTime!
}
```

**1c. gRPC contracts (protobuf):**

```protobuf
service DocumentService {
  rpc GetDocument(GetDocumentRequest) returns (Document);
}

message GetDocumentRequest {
  string id = 1;
}

message Document {
  string id = 1;
  string title = 2;
  string content = 3;
  google.protobuf.Timestamp created_at = 4;
}
```

**Rules for contract-first:**
- Contract is reviewed and approved before any code is written
- Contract lives in a shared location discoverable by all consumers
- Contract is version-controlled independently from implementations
- Breaking changes must be approved by all consumers

### Step 2: Naming and Structure Conventions

**REST URIs:**
- Plural nouns for collections: `/documents`, `/users`
- Singular for singletons: `/profile`, `/config`
- Nest only for clear ownership: `/users/{id}/documents` (documents belong to users)
- Max 3 levels of nesting (beyond that, flatten with query params)
- Kebab-case for multi-word resources: `/order-items`

**REST operations:**
- GET: Read (idempotent, safe)
- POST: Create (non-idempotent)
- PUT: Full replace (idempotent)
- PATCH: Partial update (idempotent if using merge patch)
- DELETE: Remove (idempotent)

**Field naming (all protocols):**
- snake_case in REST (industry convention for payloads)
- camelCase in GraphQL
- PascalCase for protobuf message names, snake_case for field names
- Boolean fields: prefix with `is_`, `has_`, `can_` (e.g., `is_active`, `has_permission`)

### Step 3: Error Semantics

Every API must have consistent, documented error responses:

**Standard error response (REST):**

```json
{
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "Document with ID 'abc-123' not found",
    "details": {
      "document_id": "abc-123",
      "search_timestamp": "2026-06-10T12:00:00Z"
    },
    "request_id": "req-abc-123-def",
    "documentation_url": "https://docs.example.com/errors/DOCUMENT_NOT_FOUND"
  }
}
```

**HTTP status codes (be precise):**
- 200: Success
- 201: Created
- 400: Bad request (malformed input) — never use for auth failures
- 401: Unauthenticated (no credentials or invalid)
- 403: Unauthorized (valid credentials, insufficient permissions)
- 404: Resource not found
- 409: Conflict (version conflict, duplicate resource)
- 422: Unprocessable entity (validation failure — use this instead of 400)
- 429: Rate limited
- 500: Internal server error (never leak stack traces)
- 503: Service unavailable

**GraphQL error handling:**
- Use typed errors in the schema (`union Result = Success | NotFound | Unauthorized`)
- Never throw exceptions for expected error states
- Include error codes in extensions

**gRPC error handling:**
- Use canonical error codes (`NOT_FOUND`, `PERMISSION_DENIED`, `INVALID_ARGUMENT`)
- Include error details in google.rpc.Status
- Never return INTERNAL for client errors

### Step 4: Boundary Validation

Every API boundary must validate all inputs at the edge:

1. **Structural validation** (reject malformed requests):
   - Required fields present
   - Correct types
   - No unexpected fields (strict mode)

2. **Semantic validation** (reject invalid requests):
   - Field value ranges (IDs exist, dates are in range, etc.)
   - Business rule constraints
   - Authorization context

3. **Defensive validation** (protect the system):
   - Input size limits (max request body, max array length, max string length)
   - Rate limiting per client
   - Payload depth limits (prevent billion laughs attack)
   - Character encoding enforcement

Implementation pattern:

```python
from pydantic import BaseModel, Field, UUID4

class CreateDocumentRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., max_length=100000)
    tags: list[str] = Field(default=[], max_length=10)

class DocumentService:
    def create_document(self, req: CreateDocumentRequest) -> Document:
        # At this point, input is already validated
        # Business logic here, not validation
        pass
```

### Step 5: Versioning Strategy

Choose and document one versioning strategy:

**Option A: URL versioning (REST, recommended for public APIs)**
```
GET /v1/documents
GET /v2/documents
```
- Clear, discoverable
- Easy to route at the gateway
- Encourages parallel maintenance of old versions

**Option B: Header versioning (REST, for internal/BFF APIs)**
```
GET /documents
Accept: application/vnd.api+json;version=1
Accept: application/vnd.api+json;version=2
```
- Cleaner URLs
- Version lives in content negotiation
- Harder to discover and debug

**Option C: No versioning (GraphQL, gRPC)**
- Add fields without removing
- Deprecate with warnings
- Never make breaking changes
- Use `@deprecated` directive in GraphQL

**One-Version Rule:** Maintain at most one old version simultaneously. When v3 ships, v1 is EOL. This prevents an unbounded version matrix.

### Step 6: Hyrum's Law Mitigation

Since every observable behavior will be depended on, take proactive measures:

1. **Document the contract, but also document what you don't guarantee:**
   - "Array ordering is not guaranteed"
   - "Field `created_at` precision is to the second, not millisecond"
   - "This endpoint may return additional fields in the future"

2. **Add extensibility from day one:**
   - Always wrap list responses in an envelope: `{ "data": [...], "metadata": {...} }`
   - Include `next_page_token` even for small lists (you'll paginate later)
   - Make all response objects maps/dictionaries, not arrays (for forward-compatible field additions)

3. **Deprecation protocol:**
   - Mark deprecated fields with warnings in response headers (`Sunset: Sat, 10 Jun 2027 00:00:00 GMT`)
   - Add `@deprecated` with `reason` in schemas
   - Minimum deprecation period: 6 months for internal APIs, 12 months for public APIs
   - Log usage of deprecated features and notify known consumers

4. **Change review:**
   - Any field addition must pass: "Will this break existing clients?" (answer: no)
   - Any field removal must pass: "Is this absolutely necessary?" (answer: almost never)
   - Any behavior change must pass: "Are we changing observable behavior?" (answer: yes → Hyrum's Law applies)

### Step 7: OpenAPI Spec Generation

Generate OpenAPI specs from code, not the other way around (prevents drift):

```python
# FastAPI example — schema is generated from code
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Document API", version="1.0.0")

@app.get("/v1/documents/{id}", response_model=Document)
async def get_document(id: UUID4):
    doc = await document_service.get(id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc
```

**Spec verification:**
- [ ] Spec passes OpenAPI 3.1 validation
- [ ] Every response has a documented error case
- [ ] Every parameter has description, type, and format
- [ ] Security schemes are documented
- [ ] Rate limiting is documented
- [ ] Deprecation notices are present
- [ ] Spec renders correctly in Swagger UI / Redoc

## Anti-Rationalization Table

| Excuse | Rebuttal |
|--------|----------|
| "I'll write the implementation first and document later" | Implementation-first guarantees documentation drift. By the time you document, the implementation has changed 3 times. Contract-first means the implementation follows the spec, making drift impossible. |
| "This is a private API, I don't need versioning" | Private APIs become public or get external consumers faster than you expect. Every acquisition, partnership, or API productization starts with "just expose this endpoint." Version from day one. |
| "I don't need an error code, clients can parse the message" | Error messages change. They're localized. They have typos. Error codes are the stable contract. If clients parse error messages, you've created a coupling that will break when you fix a typo. |
| "We only have one consumer, Hyrum's Law won't apply" | One consumer is enough to cause pain. And that one consumer will write code that depends on undocumented behavior. Then that consumer will be the one whose feature you're deprecating. |
| "Adding validation is over-engineering for this endpoint" | An unvalidated endpoint is one SQL injection, one XSS, or one billion-laughs attack away from production incident. Validation is not over-engineering; it's basic defense in depth. |
| "The GraphQL schema is self-documenting" | A schema tells you the types. It doesn't tell you the semantics, error conditions, pagination limits, rate limits, or deprecation timeline. Documentation is more than the schema. |
| "I'll just add a new field without versioning" | Adding a field is not a breaking change. Removing or renaming a field is. As long as you follow the extensibility rules, adding fields is safe. But you must never change existing field semantics. |

## Red Flags

- **No error response schema**: Clients don't know how to handle errors
- **200 for everything with error in body**: Misusing HTTP semantics; breaks middleware and proxies
- **No pagination on list endpoints**: Will break when data grows
- **Semantic version in URL instead of contract version**: `v1.2.3` in URL suggests each patch is a breaking change
- **Stringly-typed IDs**: No ID format validation, no distinction between types of IDs
- **Array responses without envelope**: Can't add metadata without breaking clients
- **Symmetric request/response** (same shape in both directions): Creates tight coupling
- **Nullable fields without explicit null semantics**: Clients don't know what null means

## Verification

- [ ] Test: Lint every OpenAPI spec for structural validity and best practices
- [ ] Test: Verify error responses match documented schema (use contract testing)
- [ ] Test: Verify all endpoints handle invalid input with appropriate errors
- [ ] Test: Verify versioned endpoints maintain backward compatibility
- [ ] Test: Verify pagination works for empty results, single page, multiple pages
- [ ] Test: Verify rate limiting returns 429 with Retry-After header
- [ ] Test: Verify all deprecated fields return warning headers
- [ ] Test: Verify no stack traces leak in error responses
- [ ] Test: Run security scan on API spec (e.g., spectral + security ruleset)
- [ ] Test: Verify spec generates valid client code (e.g., openapi-generator)

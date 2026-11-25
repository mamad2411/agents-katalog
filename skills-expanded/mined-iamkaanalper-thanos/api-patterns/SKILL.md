---
name: api-patterns
description: API design, versioning, testing, schema validation, and contract testing patterns for REST and GraphQL APIs. Grok-native with Production Contract, hooks, compound, palace.
when-to-use: When designing or reviewing APIs, especially with backend-dev or in swarms with API tracks. Use for new endpoints, versioning, or schema changes.
---

# API Patterns Skill (Grok Port)

Production-grade patterns for reliable, evolvable, well-tested APIs. Focus on REST/GraphQL that scale and don't break clients.

## Core API Design Patterns

### RESTful Resource Modeling
- Use nouns for resources, HTTP verbs for actions.
- Consistent pluralization (users, not user).
- Nested resources only when ownership is clear (users/:id/orders).
- Avoid actions in URLs; use PATCH or dedicated endpoints.

**Example:**
```http
GET /users
POST /users
GET /users/{id}
PATCH /users/{id}
DELETE /users/{id}
POST /users/{id}/activate  # if not simple state change
```

### Versioning Strategies
- URL: /v1/users (simple, but pollutes).
- Header: Accept: application/vnd.example.v1+json (cleaner, preferred for long-term).
- Never break existing clients; deprecate gracefully with warnings.

### Error Handling & Responses
- Always return problem+json or consistent error shape.
- Include request_id for tracing.
- Use standard HTTP codes; 4xx client, 5xx server.
- Never leak stack traces or internal details in prod.

**Standard Error:**
```json
{
  "type": "https://example.com/probs/validation-error",
  "title": "Invalid input",
  "status": 400,
  "detail": "email is required",
  "instance": "/users",
  "request_id": "req-123"
}
```

### Pagination, Filtering, Sorting
- Cursor-based for large/mutable datasets (better than offset).
- Consistent query params: ?limit=10&cursor=abc&sort=-created_at&filter[status]=active.
- Always return total or has_more when possible.
- Document max limits.

### GraphQL Specific
- Schema first, use SDL or codegen.
- Avoid N+1 with DataLoader.
- Pagination with connections (edges/nodes/pageInfo).
- Mutations return payloads, not just the object.
- Subscriptions for real-time.

## Testing & Contract Patterns
- Contract testing (Pact) for consumer-driven.
- Schema validation in CI (graphql-codegen, openapi-validator).
- Property-based for complex inputs.
- Golden tests for response shapes.

## Grok Integration (Production Contract)
- Use with backend-dev, api-gateway-expert, graphql-expert agents.
- Fire on_api_feature, on_db_change, on_infra_change hooks when patterns apply at scale.
- Pre-Flight: "Have we modeled the access patterns, versioning strategy, and breaking change plan?"
- Ledger for any public API or schema change.
- Handoff: include OpenAPI/GraphQL schema diff, migration guide, deprecation timeline, test matrix.
- Friction + compound: every "this endpoint caused client breakage" or "N+1 in GraphQL" → compound to improve templates or linter rules.
- Palace: store "chose header versioning because clients are external and long-lived".
- Claim-verif: always read the actual schema/contract before claiming "backward compatible".

## When to Activate
- New API surface or major refactor.
- In swarm Phase 2/3 for backend/API tracks.
- Before deploys that touch public contracts.
- When reviewing PRs with API changes.

Use with backend-patterns, security-review, test-enforcement, contract-testing-patterns.

These patterns prevent the "it worked in staging" API hell. Use them.

---
name: api-design-standards
description: >-
  API design standards covering contract-first development, resource naming,
  versioning, pagination, error handling, throttling, and API governance.
  Applies to REST APIs managed through Azure API Management.
when-to-use: >-
  Invoke when designing new APIs, reviewing API contracts, setting up Azure API
  Management, or establishing API standards for a team. Also invoke when
  evaluating API versioning strategies or error response formats.
categories:
  - api-design
  - integration
  - architecture
---

# API Design Standards

Design APIs contract-first. Define the interface before writing backend code. Frontend and backend teams work in parallel against the agreed contract.

## Contract-First Workflow

1. Design API in OpenAPI 3.0+ (YAML/JSON) — include schemas, examples, error responses
2. Import spec into APIM — auto-generates operations and developer portal docs
3. Configure mock responses (`mock-response` policy) for frontend development
4. Implement backend against the same contract
5. Replace mock with real backend — frontend never changes

---

## Resource Naming

| Rule | Example |
|---|---|
| Nouns for resources | `/orders`, `/customers/{id}/addresses` |
| Verbs only for non-CRUD actions | `/orders/{id}/cancel` |
| Plural nouns for collections | `/orders` |
| Singular for specific items | `/orders/{id}` |
| Maximum 3 nesting levels | `/customers/{id}/orders/{orderId}` |
| `kebab-case` for URL paths | `/order-items` |
| `camelCase` for JSON properties | `{ "orderId": 123 }` |

**Deeper nesting indicates poor resource modeling** — flatten or create separate endpoints.

---

## Pagination

### Cursor-Based (Preferred for Large Datasets)
```json
{
  "value": [...],
  "nextLink": "https://api.example.com/orders?continuationToken=abc123"
}
```

### Offset-Based (OData Convention)
```
GET /orders?$skip=20&$top=10&$count=true
```

**Rules**:
- Always include `nextLink` in response — clients never construct pagination URLs
- Return total count only when requested (`$count=true`) — counting is expensive
- Default page size: 20–50 items. Maximum: 100.

---

## Error Responses

Use RFC 7807 Problem Details format:

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 400,
  "detail": "The 'email' field is not a valid email address.",
  "instance": "/orders/12345",
  "errors": [
    { "field": "email", "message": "Invalid email format" }
  ]
}
```

### Status Code Mapping

| Code | Meaning | When to Use |
|---|---|---|
| 400 | Bad Request | Input validation failure |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but lacks permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate or state conflict |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server failure |

**Never expose stack traces or internal details in production error responses.**

---

## Versioning

### URL Path Versioning (Default Recommendation)
```
/v1/orders
/v2/orders
```
Most discoverable, most cacheable. APIM version sets manage the lifecycle.

### Version Lifecycle
```
Create → Preview → GA → Deprecated → Sunset
```

### Breaking vs Non-Breaking Changes

| Change Type | Breaking? | Requires New Version? |
|---|---|---|
| Removing a field | Yes | Yes |
| Changing field type | Yes | Yes |
| Changing required fields | Yes | Yes |
| Adding optional field | No | No |
| Adding new endpoint | No | No |
| Adding optional parameter | No | No |

---

## Throttling & Rate Limiting

- Implement rate limiting at the API gateway (APIM) level
- Return `429 Too Many Requests` with `Retry-After` header
- Use quota policies per product/subscription tier
- Design clients to respect `Retry-After` and implement exponential backoff

---

## Authentication

### Decision Tree
```
Public API?
├─ Yes → API key + rate limiting (minimum)
│        └─ Sensitive data? → OAuth 2.0 + API key
└─ No (internal)?
    ├─ Service-to-service → Managed Identity + RBAC
    └─ User-facing → OAuth 2.0 / OIDC (Entra ID)
```

- Prefer managed identity for Azure-to-Azure communication
- Use OAuth 2.0 authorization code flow with PKCE for SPAs
- API keys alone are not sufficient for sensitive data

---

## API Governance

### Linting
- Use Spectral or Azure API Center to lint OpenAPI specs
- Enforce: no missing descriptions, no inline schemas, consistent error formats
- Run linting in CI — fail the build on violations

### API Catalog
- Register APIs in Azure API Center regardless of hosting platform
- Track lifecycle stages: design → development → testing → production → deprecated → retired
- Link APIs to owners, docs, environments, deployments

### Consistency
- [ ] Publish an API design guide — enforce via linting rules
- [ ] Use APIM policy fragments for shared logic
- [ ] Review API designs before implementation
- [ ] Template starter APIs for new teams to clone

---

## API Review Checklist

- [ ] OpenAPI spec defined before implementation
- [ ] Resource naming follows conventions (nouns, plural, max 3 levels)
- [ ] All error responses use consistent format (RFC 7807)
- [ ] All response codes documented (200, 400, 401, 403, 404, 500)
- [ ] Pagination implemented for collection endpoints
- [ ] Rate limiting configured
- [ ] Authentication required on all non-public endpoints
- [ ] Versioning strategy defined
- [ ] No internal details in error responses
- [ ] Input validation on all parameters

## Related Skills

- `error-handling-patterns` — Retry, circuit breaker, and compensation patterns
- `security-review-framework` — API security review checklist

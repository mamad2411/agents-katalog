---
name: code-rest
description: Apply `code-rest` skill before design-review REST API or OpenAPI specifications
---

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Path segments | lowercase with hyphens | `/vehicle-images/123` |
| Resources | lowercase, plural, nouns | `/orders`, `/users` |
| Query parameters | snake_case | `?max_results=10&sort=+id` |
| Properties | camelCase | `"lifeTimeList"`, `"customerId"` |
| Enum names | UpperCamelCase | `"DeliverMethods"` |
| Enum values | UPPER_SNAKE_CASE | `"DELIVER_METHODS_UNSPECIFIED"` |
| Custom HTTP headers | Hyphenated-Pascal-Case with `BMW-` prefix | `BMW-CV-Transaction-ID` |

- MUST avoid trailing slashes in paths.
- MUST declare resources as nouns — never use verbs in resource paths (use `/orders`, not `/create-orders`).
- First enum value SHOULD be `<ENUM_TYPE>_UNSPECIFIED`.

## HTTP Methods and Safety/Idempotency

| Method | Safe | Idempotent | Primary Use |
|--------|------|------------|-------------|
| GET | Yes | Yes | Read resources; MUST NOT have request body |
| HEAD | Yes | Yes | Retrieve headers only |
| POST | No | No | Create resources on collections or execute procedures |
| PUT | No | Yes | Create or fully replace a resource |
| PATCH | No | No | Partial update of a resource |
| DELETE | No | Yes | Delete a resource |
| OPTIONS | Yes | Yes | Inspect available operations; support CORS |

- MUST distinguish between **resources** (nouns, CRUD via standard methods) and **procedures** (actions via POST).

## HTTP Status Codes

### MUST declare (when relevant)

- **200** OK — success for GET, PUT, POST
- **201** Created — new resource created (POST)
- **204** No Content — success with no body (DELETE)
- **400** Bad Request — invalid structure/types/missing data
- **401** Unauthorized — missing or invalid credentials
- **403** Forbidden — authenticated but insufficient permissions
- **404** Not Found — resource does not exist
- **500** Internal Server Error — unexpected server failure
- **503** Service Unavailable — set `Retry-After` header when possible

Do not declare other 4xx/5xx codes unless there is a strong justification. Use **422** only for business logic errors.

For 401/403 responses, return no body content.

## Versioning

- MUST use Semantic Versioning (`MAJOR.MINOR.PATCH`) in `/info/version`.
- MUST include major version in URL path: `/<service-id>/<api-path>/v1/...`
- Do not put version segments in individual paths — only in the server/basePath.

## Compatibility

- Add only optional fields — never mandatory ones.
- Never change field semantics.
- Use `x-extensible-enum` instead of closed `enum` for output values that may grow.
- Clients MUST tolerate unknown fields and new enum values.
- Use the `deprecated` property, `Sunset` HTTP header, and client notification for deprecation.

## Data Format

- MUST use JSON (`application/json`) for structured data.
- MUST return JSON objects (not arrays) as top-level response structures.
- MUST accept unknown properties in models (forward compatibility).
- MUST use RFC 3339 for dates (`2024-01-15`) and date-times (`2024-01-15T14:07:17.123Z`), stored in UTC.
- SHOULD use ISO 8601 for durations and intervals.
- MUST use ISO standards for country (3166-1-alpha2), language (639-1/BCP-47), and currency (4217) codes.
- MUST use International System of Units (metres, kelvin).

## Performance

- SHOULD omit null property values from responses.
- SHOULD paginate lists > 50 items (offset/limit or token-based).
- SHOULD support `fields` parameter for partial responses on large payloads.

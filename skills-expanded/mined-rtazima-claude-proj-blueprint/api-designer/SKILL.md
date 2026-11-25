---
name: api-designer
description: "API design and contract definition. Activated when the user says \"design API\", \"new endpoint\", \"API contract\", \"REST\", \"GraphQL\", \"OpenAPI\", \"swagger\", \"API spec\", or wants to define API endpoints before implementation."
allowed tools: Read, Write, Edit, Grep, Glob
---

# API Designer

Design API contracts before implementation. Define endpoints, schemas, error codes,
and conventions. The contract is the source of truth — implementation follows it.

## Rules

1. **Contract first** — design the API before writing handler code
2. **Consistency** — follow existing API patterns in the project (scan `src/` first)
3. **Check specs** — read versioning spec (API strategy) and security spec (auth, rate limiting)
4. **Resource-oriented** — REST: nouns, not verbs. GraphQL: types and fields, not endpoints
5. **Error handling is part of the design** — define error codes and response format upfront
6. **Pagination for lists** — never return unbounded collections
7. **ADR for new patterns** — if introducing a new API convention, create an ADR

## Workflow

### Phase 1: Context
1. Read the PRD requirements for the API
2. Scan existing endpoints: `grep -r "router\|app\.\(get\|post\|put\|delete\|patch\)" src/` (or `[SPEC]` equivalent)
3. Read `docs/specs/versioning/` for API versioning strategy
4. Read `docs/specs/security/` for auth and rate limiting patterns
5. Read `docs/specs/api/` for API conventions (if exists)
6. Check memory for past API design decisions

### Phase 2: Design
For each endpoint, define:

```
[METHOD] /api/v{N}/{resource}

Description: What this endpoint does (one line)
Auth: [required | public | specific role]
Rate limit: [requests/window]

Request:
  Headers: [required headers]
  Params: [path and query params with types]
  Body: [schema with required/optional fields]

Response 200:
  {schema}

Response 4xx/5xx:
  {
    "error": {
      "code": "SPECIFIC_ERROR_CODE",
      "message": "Human-readable description"
    }
  }
```

### Phase 3: Conventions checklist
- [ ] **Naming**: plural nouns for resources (`/users`, not `/user`)
- [ ] **HTTP methods**: GET (read), POST (create), PUT (full update), PATCH (partial), DELETE (remove)
- [ ] **Status codes**: 200 (ok), 201 (created), 204 (no content), 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 409 (conflict), 422 (validation), 429 (rate limited), 500 (server error)
- [ ] **Pagination**: `?page=1&limit=20` or cursor-based, with `total`, `hasMore` in response
- [ ] **Filtering**: `?status=active&sort=created_at&order=desc`
- [ ] **Versioning**: follows strategy from versioning spec (URL prefix, header, or query)
- [ ] **Error format**: consistent across all endpoints
- [ ] **Dates**: ISO 8601 (`2026-04-01T12:00:00Z`)
- [ ] **IDs**: consistent format (UUID, nanoid, auto-increment — pick one)

### Phase 4: Security review
- [ ] Auth required on all non-public endpoints
- [ ] Input validation on all parameters (type, length, format)
- [ ] No sensitive data in URL params (passwords, tokens)
- [ ] Rate limiting defined
- [ ] CORS configuration noted
- [ ] No mass assignment (explicit field allowlist)

### Phase 5: Output
Choose the appropriate output format:

| Project type | Output |
|---|---|
| Has OpenAPI/Swagger | Add/update `docs/api/openapi.yaml` |
| Has API docs directory | Add to `docs/api/{resource}.md` |
| Neither | Create `docs/api/` and write the spec there |

### Phase 6: Handoff
1. Present the API design for review
2. If approved → save the spec
3. Create an ADR if new patterns were introduced
4. The implement-prd skill will use this spec as the contract for implementation

## [SPEC] Project-specific conventions
- Base URL: [SPEC]
- Auth mechanism: [SPEC] (JWT, API key, OAuth2, session)
- Pagination style: [SPEC] (offset-based, cursor-based)
- Error format: [SPEC]
- API documentation tool: [SPEC] (OpenAPI, API Blueprint, custom)

## References
- `docs/specs/versioning/` — API versioning strategy
- `docs/specs/security/` — auth and rate limiting
- `docs/specs/api/` — API conventions (if enabled)
- `docs/architecture/` — ADRs for past API decisions

---
description: Run REST API Design Standards Check
globs: ['src/app/api/**/*.ts', 'src/pages/api/**/*.ts']
---

# Backend: API Design Standards

<audit_rules>

- You MUST enforce standard JSON envelope responses for all endpoints: `{ data, error, meta }`.
- You MUST ensure the correct HTTP method is used (GET for reads, POST for creates, PUT/PATCH for updates, DELETE for removals).
- You MUST verify that appropriate HTTP status codes are returned (e.g., 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error).
- You MUST flag any endpoints that do not implement pagination for collections or lists.
- You MUST use a clear API versioning strategy (e.g. path or header) and avoid breaking changes without versioning or deprecation communication.
- You MUST maintain API documentation (e.g. OpenAPI/Swagger) that matches the implementation and supports discovery.
  </audit_rules>

**How to check**: Inspect route handlers for envelope shape and status codes; confirm list endpoints use pagination; verify versioning and docs exist and match routes.

<example_good>

```typescript
// Standardized response
return NextResponse.json({ data: { user }, error: null, meta: { total: 1 } }, { status: 200 })
```

</example_good>

<example_bad>

```typescript
// BAD: Inconsistent structure and missing status code
return NextResponse.json({ success: true, theUser: user })
```

</example_bad>

**Related rules**: api-security, input-validation, auth-standards.

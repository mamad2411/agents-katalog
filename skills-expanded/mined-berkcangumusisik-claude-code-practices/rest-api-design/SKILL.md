---
name: rest-api-design
description: Reviews or designs a RESTful API following best practices
argument-hint: <resource-name-or-review-existing>
user-invocable: true
allowed-tools: Read Grep Glob
effort: medium
---

## REST API Design

Resource / Scope: **$ARGUMENTS**

### If reviewing existing API:

1. Read route definitions:
```bash
grep -rn "router\.\|app\." src/ --include="*.ts" | grep -E "get|post|put|patch|delete" | head -30
```

Check for:
- Proper HTTP method usage (GET=read, POST=create, PUT/PATCH=update, DELETE=remove)
- Consistent URL naming (`/users` not `/getUsers`)
- Plural nouns for collections (`/users/123`)
- Nested resources for relationships (`/users/123/posts`)
- Query params for filtering/sorting/pagination, not URL segments
- Consistent response shapes
- Missing pagination on list endpoints
- HTTP status codes correct (201 for creation, 204 for delete, etc.)

### If designing new API:

Generate the complete route table:

```
GET    /resources          List (with pagination)
POST   /resources          Create
GET    /resources/:id      Get one
PUT    /resources/:id      Replace
PATCH  /resources/:id      Partial update
DELETE /resources/:id      Delete

GET    /resources/:id/related   Nested resource
```

Include request/response shapes and error codes for each endpoint.

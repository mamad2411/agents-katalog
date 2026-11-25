---
name: api-docs
description: Generates API documentation from route definitions (Express, Fastify, Hono, etc.)
argument-hint: [routes-directory]
user-invocable: true
allowed-tools: Read Glob Grep Edit
effort: medium
---

## Generate API Documentation

Routes directory: **$1** (or auto-detect)

1. Find all route definitions:
```bash
grep -rn "router\.\(get\|post\|put\|patch\|delete\)\|app\.\(get\|post\|put\|patch\|delete\)" ${1:-src/} --include="*.ts" -l
```

2. For each route, extract:
   - Method + path
   - Path parameters, query params
   - Request body shape (from Zod schema, type, or interface)
   - Response shape
   - Auth requirements (middleware check)
   - Error responses

3. Generate documentation in OpenAPI 3.0 YAML format OR a readable Markdown table - ask the user which format.

**Markdown format:**
```markdown
### POST /api/users
Creates a new user.

**Body:** `{ name: string, email: string }`
**Response:** `{ id: string, createdAt: string }`
**Auth:** Bearer token required
```

4. Save to `docs/api.md` or `openapi.yaml`.

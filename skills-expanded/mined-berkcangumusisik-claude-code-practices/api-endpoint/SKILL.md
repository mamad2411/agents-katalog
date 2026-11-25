---
name: api-endpoint
description: Scaffolds a complete API endpoint with validation, error handling, and tests
argument-hint: <METHOD> <path> [description]
user-invocable: true
allowed-tools: Read Glob Edit
effort: medium
---

## Generate API Endpoint

Method + Path: **$1 $2**
Description: **$3**

1. Detect framework:
```bash
cat package.json | grep -E '"express"|"fastify"|"hono"|"koa"|"nestjs"'
ls src/routes/ src/api/ src/handlers/ 2>/dev/null | head -10
```

2. Read 1-2 existing route files to match patterns exactly.

3. Generate the route handler with:
   - Request validation (Zod schema or project's validator)
   - Auth middleware call (if project uses auth)
   - Business logic (stub with TODO if complex)
   - Proper error handling (use project's error classes)
   - Typed request/response

4. Register the route in the router file.

5. Generate tests:
   - Happy path (200/201)
   - Validation error (400)
   - Auth error (401/403)
   - Not found (404) if applicable

6. Update API docs if `docs/api.md` or OpenAPI spec exists.

---
name: openapi-gen
description: Generates an OpenAPI 3.0 spec from existing route definitions
user-invocable: true
allowed-tools: Read Grep Glob Edit
effort: medium
---

## Generate OpenAPI Specification

1. Find all routes:
```bash
grep -rn "router\.\|app\." src/ --include="*.ts" | grep -E "\.(get|post|put|patch|delete)\(" | head -40
```

2. For each route, extract:
   - HTTP method and path
   - Path parameters (`:id`, `:slug`)
   - Query parameters (from validation schema)
   - Request body schema (from Zod/TypeScript types)
   - Response schema
   - Auth requirement

3. Generate `openapi.yaml`:
```yaml
openapi: 3.0.3
info:
  title: API Name
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      security:
        - bearerAuth: []
      parameters:
        - name: page
          in: query
          schema: { type: integer, default: 1 }
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
```

4. Add `components/schemas` for all reusable types.

5. Add security schemes (bearerAuth, apiKey, etc.)

6. Save to `openapi.yaml` or `docs/openapi.yaml`.

Tip: This file can be used with Swagger UI, Postman, or client SDK generators.

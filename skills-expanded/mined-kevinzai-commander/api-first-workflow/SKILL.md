---
name: api-first-workflow
description: "API-first development — OpenAPI spec authoring, contract-first dev, SDK generation, mock servers, and API documentation"
version: 1.0.0
category: backend
---

# API-First Development Workflow

Design the API contract before writing any implementation code. The spec IS the source of truth.

## Process

### 1. Design the API Spec (OpenAPI 3.1)

```yaml
# openapi.yaml
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
  description: API description
servers:
  - url: http://localhost:3001
    description: Development
  - url: https://api.example.com
    description: Production

paths:
  /api/v1/users:
    get:
      operationId: listUsers
      summary: List all users
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Paginated list of users
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedUsers'

  /api/v1/users/{id}:
    get:
      operationId: getUser
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      required: [id, email, name, createdAt]
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        createdAt:
          type: string
          format: date-time

  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        minimum: 1
        default: 1
    LimitParam:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

  responses:
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: object
                properties:
                  code:
                    type: string
                    example: NOT_FOUND
                  message:
                    type: string
```

### 2. Generate Types from Spec

```bash
# Generate TypeScript types from OpenAPI spec
npx openapi-typescript openapi.yaml -o src/types/api.d.ts

# Or use zodios for runtime validation
npx openapi-zod-client openapi.yaml -o src/types/api.ts
```

### 3. Mock Server for Frontend Development

```bash
# Prism mock server — instant API from spec
npx @stoplight/prism-cli mock openapi.yaml --port 4010

# Frontend can develop against http://localhost:4010 immediately
```

### 4. Contract Testing

```typescript
// Validate implementation matches spec
import { createDocument } from 'zod-openapi';
import spec from './openapi.yaml';

describe('API Contract', () => {
  it('GET /api/v1/users returns valid response', async () => {
    const response = await app.inject({ method: 'GET', url: '/api/v1/users' });
    const body = JSON.parse(response.body);

    // Validate against OpenAPI schema
    expect(response.statusCode).toBe(200);
    expect(body).toHaveProperty('data');
    expect(body).toHaveProperty('pagination');
    expect(body.data[0]).toHaveProperty('id');
    expect(body.data[0]).toHaveProperty('email');
  });
});
```

### 5. API Documentation

```typescript
// Swagger UI setup (Fastify)
import swagger from '@fastify/swagger';
import swaggerUI from '@fastify/swagger-ui';

await app.register(swagger, {
  openapi: {
    openapi: '3.1.0',
    info: { title: 'My API', version: '1.0.0' },
  },
});
await app.register(swaggerUI, { routePrefix: '/docs' });

// Alternative: Scalar (modern UI)
// https://github.com/scalar/scalar
```

## API Design Rules

1. **Use nouns, not verbs** — `/users` not `/getUsers`
2. **Plural resource names** — `/users` not `/user`
3. **Version in URL** — `/api/v1/users`
4. **Consistent error format** — `{ error: { code, message } }`
5. **Pagination on all list endpoints** — `?page=1&limit=20`
6. **Use HTTP status codes correctly** — 200, 201, 204, 400, 401, 403, 404, 409, 422, 500
7. **Idempotency keys for mutations** — `Idempotency-Key` header
8. **Rate limiting headers** — `X-RateLimit-Limit`, `X-RateLimit-Remaining`

## Versioning Strategy

| Strategy | When | Example |
|----------|------|---------|
| URL versioning | Public APIs, breaking changes | `/api/v2/users` |
| Header versioning | Internal APIs | `Accept: application/vnd.api.v2+json` |
| No versioning | Rapid iteration, single client | Evolve in place |

## Checklist

- [ ] OpenAPI spec written BEFORE implementation
- [ ] Types generated from spec (not hand-written)
- [ ] Mock server running for frontend team
- [ ] Contract tests validating implementation matches spec
- [ ] API documentation accessible at `/docs`
- [ ] Error responses follow consistent format
- [ ] Pagination on all list endpoints
- [ ] Authentication documented in spec
- [ ] Rate limiting configured and documented

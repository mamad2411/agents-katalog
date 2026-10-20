---
name: "openapi-patterns"
description: "OpenAPI 3.x design reference: 3.1 vs 3.0 differences, resource naming, HTTP method semantics, schema design, RFC 7807 error responses, and authentication schemes. Use when designing or reviewing the structure of an OpenAPI spec rather than its prose."
---

# OpenAPI Patterns

> Comprehensive knowledge base for writing correct, consistent, and developer-friendly OpenAPI 3.x specifications.

## Knowledge Base

### OpenAPI 3.1 vs 3.0

OpenAPI 3.1 aligns with JSON Schema 2020-12. Key differences from 3.0:

| Feature | 3.0 | 3.1 |
|---------|-----|-----|
| JSON Schema | Draft 4 (modified) | 2020-12 (full) |
| Nullable | `nullable: true` | `type: ['string', 'null']` |
| Exclusive min/max | `exclusiveMinimum: true` + `minimum: 0` | `exclusiveMinimum: 0` |
| `const` keyword | Not supported | Supported |
| `if/then/else` | Not supported | Supported |
| Webhooks | Not supported | Top-level `webhooks` key |

### Resource Naming Conventions

```yaml
# Correct: plural nouns, kebab-case for multi-word
/users
/users/{user_id}
/users/{user_id}/api-keys
/users/{user_id}/api-keys/{key_id}

# Wrong: verbs in paths, camelCase, singular
/getUser
/user/{id}/apiKeys
/users/{user_id}/delete
```

### HTTP Method Semantics

| Method | Idempotent | Safe | Typical Status Codes |
|--------|-----------|------|---------------------|
| GET | Yes | Yes | 200, 404 |
| POST | No | No | 201, 202, 422 |
| PUT | Yes | No | 200, 204, 404, 422 |
| PATCH | No* | No | 200, 204, 404, 422 |
| DELETE | Yes | No | 204, 404 |
| HEAD | Yes | Yes | 200, 404 |
| OPTIONS | Yes | Yes | 204 |

*PATCH is idempotent if using JSON Merge Patch, not if using JSON Patch.

### Schema Design Patterns

**Polymorphism with discriminator:**

```yaml
components:
  schemas:
    Notification:
      oneOf:
        - $ref: '#/components/schemas/EmailNotification'
        - $ref: '#/components/schemas/SmsNotification'
        - $ref: '#/components/schemas/WebhookNotification'
      discriminator:
        propertyName: type
        mapping:
          email: '#/components/schemas/EmailNotification'
          sms: '#/components/schemas/SmsNotification'
          webhook: '#/components/schemas/WebhookNotification'

    EmailNotification:
      type: object
      required: [type, recipient, subject]
      properties:
        type:
          type: string
          const: email
        recipient:
          type: string
          format: email
        subject:
          type: string
```

**Read vs Write schemas (asymmetric):**

```yaml
components:
  schemas:
    # Full resource (read)
    User:
      type: object
      required: [id, email, created_at]
      properties:
        id:
          type: string
          readOnly: true
        email:
          type: string
          format: email
        name:
          type: string
        created_at:
          type: string
          format: date-time
          readOnly: true

    # Creation payload (write)
    UserCreate:
      type: object
      required: [email]
      properties:
        email:
          type: string
          format: email
        name:
          type: string
        password:
          type: string
          format: password
          writeOnly: true
          minLength: 8
```

**Pagination envelope:**

```yaml
components:
  schemas:
    PaginatedResponse:
      type: object
      properties:
        data:
          type: array
          items: {}  # Override with specific schema
        meta:
          type: object
          properties:
            page:
              type: integer
              minimum: 1
            per_page:
              type: integer
              minimum: 1
              maximum: 100
            total_count:
              type: integer
              minimum: 0
            total_pages:
              type: integer
              minimum: 0
        links:
          type: object
          properties:
            self:
              type: string
              format: uri
            next:
              type: ['string', 'null']
              format: uri
            prev:
              type: ['string', 'null']
              format: uri
```

### Error Response Pattern (RFC 7807)

```yaml
components:
  schemas:
    ProblemDetail:
      type: object
      required: [type, title, status]
      properties:
        type:
          type: string
          format: uri
          description: URI reference identifying the problem type
          example: "https://api.example.com/errors/validation-failed"
        title:
          type: string
          description: Short human-readable summary
          example: "Validation Failed"
        status:
          type: integer
          description: HTTP status code
          example: 422
        detail:
          type: string
          description: Human-readable explanation specific to this occurrence
          example: "The 'email' field must be a valid email address"
        instance:
          type: string
          format: uri
          description: URI identifying this specific occurrence
        errors:
          type: array
          description: Field-level validation errors
          items:
            type: object
            properties:
              field:
                type: string
                example: "email"
              code:
                type: string
                example: "invalid_format"
              message:
                type: string
                example: "Must be a valid email address"
```

### Authentication Schemes

```yaml
components:
  securitySchemes:
    # API Key in header
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key obtained from the dashboard

    # Bearer token (JWT)
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token from /auth/login

    # OAuth2 with multiple flows
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/authorize
          tokenUrl: https://auth.example.com/token
          refreshUrl: https://auth.example.com/token
          scopes:
            read:users: Read user data
            write:users: Modify user data
            admin: Full administrative access
        clientCredentials:
          tokenUrl: https://auth.example.com/token
          scopes:
            read:users: Read user data
```

## Patterns

1. **Spec-First Development**: Write the OpenAPI spec before implementation. Use it as the contract between frontend and backend teams.
2. **Schema Reuse**: Define schemas in `components/schemas` and reference them with `$ref`. Never inline complex schemas.
3. **Consistent Naming**: Use `operationId` for every operation. Format: `verbNoun` (e.g., `listUsers`, `createOrder`, `getOrderById`).
4. **Envelope Responses**: Wrap collections in `{ data: [], meta: {} }`. Wrap single resources in `{ data: {} }` if you want consistency, or return bare objects for simplicity.
5. **Versioning in URL**: Use `/v1/` prefix for API versioning. Document migration paths between versions.
6. **Example Values**: Every schema property should have an `example` that is realistic, not "string" or "test".
7. **Tag Grouping**: Use tags to group related endpoints. One tag per resource. Add tag descriptions.

## Anti-Patterns

1. **Verbs in paths**: `/getUsers` instead of `GET /users`. Paths are nouns; HTTP methods are verbs.
2. **Inconsistent error formats**: Returning different error shapes from different endpoints. Use RFC 7807 everywhere.
3. **Missing operationId**: Makes SDK generation unreliable. Every operation needs a unique operationId.
4. **Overloaded endpoints**: One endpoint that does different things based on query parameters. Split into separate operations.
5. **200 for everything**: Returning 200 with `{ success: false }`. Use proper HTTP status codes.
6. **Undocumented query params**: Parameters that work but are not in the spec. Document everything or remove it.
7. **No examples**: Specs without examples force developers to guess at request/response shapes.
8. **Nested resource overload**: `/users/{id}/posts/{pid}/comments/{cid}/likes/{lid}` -- flatten beyond 2 levels.

## References

- [OpenAPI 3.1 Specification](https://spec.openapis.org/oas/v3.1.0)
- [JSON Schema 2020-12](https://json-schema.org/specification)
- [RFC 7807 - Problem Details for HTTP APIs](https://datatracker.ietf.org/doc/html/rfc7807)
- [RFC 9110 - HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110)
- [Spectral OpenAPI Linter](https://stoplight.io/open-source/spectral)
- [Redocly CLI](https://redocly.com/docs/cli/)

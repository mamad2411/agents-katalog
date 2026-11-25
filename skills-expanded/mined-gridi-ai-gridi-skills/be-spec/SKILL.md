---
name: be-spec
description: >
  A skill for writing OpenAPI 3.0 specs based on tech specs.
  Generates API specifications including API endpoints, request/response schemas, and authentication information.
  Use this skill for API spec, OpenAPI, or Swagger documentation requests.
---

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

## 🔧 Project Configuration Reference

> **You must read `crew-config.json` first and operate according to the project settings.**
> - `backend.apiStyle`: REST vs GraphQL spec format
> - `conventions.idStrategy`: Determines ID type in schemas
>
> If `crew-config.json` does not exist, guide the user to run the `/project-init` skill first.

## ⚠️ ID Strategy (crew-config.json → conventions.idStrategy)

> **Follow the `conventions.idStrategy` setting in `crew-config.json`.**
> - Define the ID field type in the OpenAPI schema according to the setting
> - `uuid` → `type: string, format: uuid`
> - `auto-increment` → `type: integer, format: int64`
> - **If the setting is missing, use UUID as the default.**

### ID Definition in OpenAPI Schema

```yaml
# ✅ Correct approach: UUID
id:
  type: string
  format: uuid
  description: Unique identifier (UUID v4)
  example: "550e8400-e29b-41d4-a716-446655440000"

# ❌ Incorrect approach: auto-increment
id:
  type: integer
  description: Unique identifier
```

# Backend API Spec Generator

Generates OpenAPI 3.0 specs based on tech spec documents.

## Workflow

### 1. Verify Input Documents

Receive the following documents as input:
- Tech spec document (including API design)
- (Optional) Existing OpenAPI spec

```
Example inputs:
- "Write an OpenAPI spec based on docs/tech-specs/account-tech-spec.md"
```

### 2. Project Analysis

1. Understand the existing API spec structure
2. Identify the authentication method in use
3. Analyze common schema patterns
4. Check the error response format

### 3. OpenAPI Spec Generation

#### 3.1 Basic Structure

```yaml
openapi: 3.0.3
info:
  title: Account API
  description: Account-related API
  version: 1.0.0
  contact:
    name: API Support
    email: api@example.com

servers:
  - url: http://localhost:3000/api/v1
    description: Development
  - url: https://api.example.com/v1
    description: Production

tags:
  - name: Auth
    description: Authentication-related API
  - name: Users
    description: User-related API
```

#### 3.2 Authentication Configuration

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT access token

    apiKey:
      type: apiKey
      in: header
      name: X-API-Key

security:
  - bearerAuth: []
```

#### 3.3 Endpoint Definitions

```yaml
paths:
  /auth/signup:
    post:
      tags:
        - Auth
      summary: Sign up
      description: Create a new account with email and password.
      operationId: signup
      security: []  # No authentication required
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SignupRequest'
            example:
              email: user@example.com
              password: Test1234!
      responses:
        '201':
          description: Sign up successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          $ref: '#/components/responses/ValidationError'
        '409':
          $ref: '#/components/responses/ConflictError'
```

#### 3.4 Schema Definitions

```yaml
components:
  schemas:
    # Request schema
    SignupRequest:
      type: object
      required:
        - email
        - password
      properties:
        email:
          type: string
          format: email
          description: User email
          example: user@example.com
        password:
          type: string
          format: password
          minLength: 8
          description: Password (at least 8 characters, including special characters)
          example: Test1234!

    # Response schema - ⚠️ Return DTO directly without data wrapping!
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
          description: User unique ID
        email:
          type: string
          format: email
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time

    # ⚠️ Single item response: Reference schema directly (no wrapping)
    # e.g., Use $ref: '#/components/schemas/User' directly in 200 response

    # ⚠️ List response: { count, plural name } format
    UserListResponse:
      type: object
      required:
        - count
        - users
      properties:
        count:
          type: integer
          description: Total count
        users:
          type: array
          items:
            $ref: '#/components/schemas/User'

    # Pagination (if needed)
    Pagination:
      type: object
      properties:
        page:
          type: integer
          example: 1
        limit:
          type: integer
          example: 20
        total:
          type: integer
          example: 100
        totalPages:
          type: integer
          example: 5
```

#### 3.5 Common Response Definitions

```yaml
components:
  responses:
    ValidationError:
      description: Input validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: VALIDATION_ERROR
              message: The input values are invalid.
              details:
                - field: email
                  message: Please enter a valid email address.

    UnauthorizedError:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: UNAUTHORIZED
              message: Authentication is required.

    ForbiddenError:
      description: Permission denied
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    NotFoundError:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    ConflictError:
      description: Resource conflict
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: CONFLICT
              message: Email is already registered.

  schemas:
    Error:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
              description: Error code
            message:
              type: string
              description: Error message
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                  message:
                    type: string
```

### 4. File Output

```
docs/openapi.yaml
```

> **Important**: The OpenAPI spec is managed as a **single file** for the entire project.
> This location must match the frontend's orval configuration (`orval.config.ts`).

#### Modular Splitting for Complex APIs

For large-scale projects where the spec grows large, split by module while keeping the main file location the same:

```
docs/
├── openapi.yaml           # Main file (references other files via $ref)
├── paths/
│   ├── auth.yaml
│   ├── users.yaml
│   └── products.yaml
└── schemas/
    ├── common.yaml        # Common schemas
    ├── requests.yaml
    └── responses.yaml
```

#### How to Reference Split Files

```yaml
# docs/openapi.yaml (main file)
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0

paths:
  /auth/signup:
    $ref: './paths/auth.yaml#/signup'
  /auth/login:
    $ref: './paths/auth.yaml#/login'
  /users:
    $ref: './paths/users.yaml#/users'

components:
  schemas:
    User:
      $ref: './schemas/common.yaml#/User'
    Error:
      $ref: './schemas/responses.yaml#/Error'
```

> **Note**: Design documents such as tech specs and design specs are stored under `docs/{backlog-keyword}/`,
> but OpenAPI specs are unified as `docs/openapi.yaml` for compatibility with code generation tools.

## OpenAPI Authoring Principles

### 1. ID Strategy
- Follow `conventions.idStrategy` in `crew-config.json`
- If `uuid`: Schema type `type: string`, `format: uuid`
- If `auto-increment`: Schema type `type: integer`, `format: int64`
- If not configured, use UUID as the default

### 2. Response Format Rules (Recommended: No data Wrapping)

> **Recommended pattern**: Return DTOs directly without `{ data: ... }` wrapping, unless your project conventions specify otherwise. Check `crew-config.json` for project-specific response format conventions.

#### Single Item Response: Return DTO Directly
```yaml
# ✅ Correct approach: Reference schema directly
responses:
  '200':
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'

# ❌ Incorrect approach: data wrapping
responses:
  '200':
    content:
      application/json:
        schema:
          type: object
          properties:
            data:
              $ref: '#/components/schemas/User'
```

#### List Response: { count, plural name } Format
```yaml
# ✅ Correct approach
UserListResponse:
  type: object
  required: [count, users]
  properties:
    count:
      type: integer
    users:
      type: array
      items:
        $ref: '#/components/schemas/User'

# ❌ Incorrect approach
UserListResponse:
  type: object
  properties:
    data:
      type: array
      items:
        $ref: '#/components/schemas/User'
```

### 3. Consistency
- Use consistent naming conventions
- List responses: `{ count: number, pluralName: T[] }`
- Single item responses: Return DTO directly
- Standardize error formats

### 4. Completeness
- Define all response status codes
- Include request/response examples
- Specify required/optional fields

### 5. Reusability
- Define common schemas in components
- Reference with $ref
- Leverage inheritance (allOf)

### 6. Documentation
- Include description for each field
- Provide example values
- Mark deprecated fields

## Schema Patterns

### Inheritance (allOf)

```yaml
UserWithProfile:
  allOf:
    - $ref: '#/components/schemas/User'
    - type: object
      properties:
        profile:
          $ref: '#/components/schemas/Profile'
```

### Polymorphism (oneOf/discriminator)

```yaml
Notification:
  oneOf:
    - $ref: '#/components/schemas/EmailNotification'
    - $ref: '#/components/schemas/PushNotification'
  discriminator:
    propertyName: type
```

### Enumeration (enum)

```yaml
UserStatus:
  type: string
  enum:
    - active
    - inactive
    - suspended
  description: |
    - active: Active state
    - inactive: Inactive state
    - suspended: Suspended state
```

> **Note**: `enum` in OpenAPI specs defines allowed values for the API contract.
> The backend implementation should follow the language/framework conventions for representing enumerations.

## References

- OpenAPI schema guide: [references/openapi-schema-guide.md](references/openapi-schema-guide.md)
- API versioning: [references/api-versioning.md](references/api-versioning.md)

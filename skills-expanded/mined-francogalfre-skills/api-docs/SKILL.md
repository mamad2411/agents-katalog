---
name: api-docs
description: Documents REST API endpoints with complete request/response examples, error codes, authentication, and parameters. Use when the user says "document this endpoint", "write API docs for...", "generate API documentation", "add docs to my route", "write OpenAPI for this", or pastes a route handler, controller, or function and asks for documentation.
---

# API Docs Writer

Produces complete, developer-ready API documentation from a route handler,
controller, or plain description. Covers authentication, parameters, request
body, responses (success and errors), and usage examples.

---

## Required Details

Collect or infer before writing. Ask if critical ones are missing.

| Detail | Example |
|---|---|
| **Endpoint** | `POST /api/users` |
| **What it does** | Creates a new user account |
| **Auth required?** | Bearer token / API key / none |
| **Request body / params** | Fields, types, required vs optional |
| **Success response** | Status code + shape of the data |
| **Error cases** | 400, 401, 404, 409, 422, 500 |
| **Format** | Markdown prose / OpenAPI YAML / both |

---

## Instructions

### Step 1 — Extract the contract

From the route handler or description, identify:
- HTTP method and path
- Path params (`:id`, `{userId}`)
- Query params (`?page=1&limit=20`)
- Request body fields with types and constraints
- All possible response shapes (success + every error)

### Step 2 — Write Markdown documentation

```markdown
## POST /api/users

Creates a new user account. Returns the created user object.

**Authentication:** Bearer token required.

---

### Request

**Headers**

| Header | Value |
|---|---|
| `Authorization` | `Bearer <token>` |
| `Content-Type` | `application/json` |

**Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `email` | string | ✅ | Valid email address |
| `name` | string | ✅ | Full name, 2–100 characters |
| `role` | string | ❌ | `"user"` (default) or `"admin"` |

**Example**
```json
{
  "email": "franco@example.com",
  "name": "Franco Galfre",
  "role": "user"
}
```

---

### Responses

**201 Created**
```json
{
  "id": "usr_01J...",
  "email": "franco@example.com",
  "name": "Franco Galfre",
  "role": "user",
  "createdAt": "2025-03-16T12:00:00Z"
}
```

**400 Bad Request** — Missing or invalid fields
```json
{ "error": "Validation failed", "details": ["email is required"] }
```

**409 Conflict** — Email already registered
```json
{ "error": "Email already in use" }
```

**401 Unauthorized** — Missing or invalid token
```json
{ "error": "Unauthorized" }
```
```

### Step 3 — Optionally generate OpenAPI YAML

If the user needs OpenAPI format:

```yaml
/api/users:
  post:
    summary: Create a new user
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [email, name]
            properties:
              email:
                type: string
                format: email
              name:
                type: string
                minLength: 2
                maxLength: 100
              role:
                type: string
                enum: [user, admin]
                default: user
    responses:
      '201':
        description: User created
      '400':
        description: Validation error
      '409':
        description: Email already in use
      '401':
        description: Unauthorized
```

---

## Non-Negotiable Acceptance Criteria

Do not deliver the docs unless ALL of these are true:

- [ ] Every parameter has: name, type, required/optional, description
- [ ] Every response (success AND error) has: status code, description, and a JSON example
- [ ] Authentication requirement is stated explicitly (or stated "None")
- [ ] Request body has a complete JSON example — not just a schema
- [ ] Error responses cover at least: invalid input (400/422), unauthorized (401), not found (404) where applicable
- [ ] No internal implementation details leaked (no DB column names, internal service names, etc.)

---

## Output Format

~~~
## [METHOD] [/path]

[full markdown documentation]

---

[OpenAPI YAML block — only if requested]
~~~

If documenting multiple endpoints, repeat the block for each one separated by `---`.
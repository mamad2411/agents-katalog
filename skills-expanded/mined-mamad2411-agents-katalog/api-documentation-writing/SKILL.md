---
name: api-documentation-writing
description: >
  Write high-quality OpenAPI/Swagger operation descriptions, parameter and schema docs,
  error contracts, and request/response examples. Use when API docs, OpenAPI description
  writing, Swagger annotations, endpoint documentation, operation summary/description, or
  improving example quality for REST/HTTP APIs. Not for offensive API recon.
---

# API Documentation Writing

## Scope And Authorization

- **In scope:** APIs your organization owns and publishes.
- **Out of scope:** Documenting others’ private APIs for attack enablement; embedding real secrets in examples.
- Prefer synthetic example data; scrub production dumps.
- Pair schema quality with `json-schema-design` and `code-quality-standards`.

## When To Use

- Authoring or improving OpenAPI 3.x descriptions.
- Making error models and auth requirements explicit.
- Adding realistic request/response examples for DX.
- Aligning docs with actual gateway behavior before release.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Offensive recon of APIs | `api-recon-and-docs` |
| API versioning policy | `api-versioning-design` |
| Security test checklist | `api-security-testing-checklist` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Doc element | Quality bar |
| --- | --- |
| `summary` / `description` | What + when; non-obvious side effects |
| Parameters | Type, format, required, constraints, examples |
| Request body | Schema + example; content-types |
| Responses | All common status codes; error schema |
| Security | `securitySchemes` + per-operation requirements |
| Idempotency | Documented for mutating retries |
| Pagination | Cursor/offset fields explained |

## Workflow

### 1. Confirm audience and success criteria

1. Audience: external partners, internal teams, or both.
2. Success: new engineer can call auth’d happy path from docs alone; errors predictable; no secret leakage.
3. Source of truth: OpenAPI in repo vs generated annotations.

### 2. Structure the OpenAPI skeleton

```yaml
openapi: 3.0.3
info:
  title: Orders API
  version: 1.2.0
  description: >
    Create and manage orders for merchant integrations.
servers:
  - url: https://api.example.com/v1
paths:
  /orders:
    get:
      summary: List orders
      description: >
        Returns orders for the authenticated merchant. Results are cursor-paginated.
      operationId: listOrders
      security:
        - ApiKeyAuth: []
      parameters:
        - $ref: '#/components/parameters/PageSize'
        - $ref: '#/components/parameters/Cursor'
      responses:
        '200':
          description: Page of orders
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderPage'
              examples:
                sample:
                  value:
                    data: [{ id: "ord_123", status: "paid" }]
                    next_cursor: "eyJvZmZzZXQiOjIwfQ"
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/RateLimited'
```

### 3. Write operation descriptions that matter

| Include | Avoid |
| --- | --- |
| Auth/scopes required | “This endpoint gets data” only |
| Side effects / emails / webhooks | Undocumented breaking behavior |
| Idempotency-Key header | Silent non-idempotent POST |
| Rate limit class | Mystery 429s |
| Deprecation links | Orphan v0 paths |

### 4. Schemas and errors

```yaml
components:
  schemas:
    Problem:
      type: object
      required: [type, title, status]
      properties:
        type: { type: string, format: uri }
        title: { type: string }
        status: { type: integer }
        detail: { type: string }
        correlation_id: { type: string }
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
      description: Create keys in the developer portal; send on every request.
```

1. Reuse error components (RFC 7807 style if adopted).
2. Enumerate error codes in description tables when clients branch on them.

### 5. Examples hygiene

```bash
# Lint OpenAPI
npx @redocly/cli lint openapi.yaml
# Or spectral
npx spectral lint openapi.yaml
```

1. Examples must validate against schemas.
2. Never use live production tokens, personal emails, or internal hostnames if public.
3. Show both success and one representative error.

### 6. Keep docs honest

1. Contract tests: examples or OpenAPI vs real responses in CI.
2. Mark `deprecated: true` with sunset date and successor.
3. Changelog link for breaking changes (`api-versioning-design`).

### 7. Hand off

1. Publish portal (Redoc/Stoplight/Swagger UI) from CI artifact.
2. Owners for each tag/path in CODEOWNERS.
3. Feedback channel for doc bugs.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Description | Side effects + auth + errors | One-word summary |
| Examples | Synthetic, schema-valid | Real customer payload |
| Errors | Shared Problem schema | “Error: string” only |
| Drift | CI contract tests | Wiki stale vs prod |

## Output Checklist

- [ ] Audience and source of truth set
- [ ] Operations have summary+description+operationId
- [ ] Params/schemas constrained with examples
- [ ] Auth security schemes documented
- [ ] Error responses complete
- [ ] Lint (Redocly/Spectral) clean
- [ ] No secrets in examples
- [ ] Deprecations and versioning linked
- [ ] `code-quality-standards` applied

## Rules

- Document owned APIs accurately; do not invent phantom endpoints.
- Synthetic data only in public examples.
- Docs are a contract — change process required for breaks.
- This skill is DX writing, not offensive recon.
- Keep security-sensitive internals appropriately gated if needed.

---
name: swagger-docs
description: OpenAPI 3.1 / Swagger documentation standards for Express — spec generation from Zod, Swagger UI setup, per-endpoint documentation requirements. Load when writing, reviewing, or generating API documentation for any Express/Node.js route.
user-invocable: false
stack: api-docs/swagger-express
paths:
  - "**/openapi.*"
  - "**/swagger*"
  - "src/docs/**"
  - "src/**/routes/**"
  - "src/**/*.route.*"
  - "docs/api/**"
---

Full rules in [swagger-docs.md](swagger-docs.md). Always-on summary:

**Approach:** generate OpenAPI from code — never hand-write the spec.
- Zod schemas → OpenAPI components via `@asteasolutions/zod-to-openapi`
- Express routes documented via `registry.registerPath()` — no separate hand-maintained YAML
- Hand-written YAML/JSON specs drift from the schemas that actually validate requests

**Tooling (locked):**
- `@asteasolutions/zod-to-openapi` — derive OpenAPI schemas from existing Zod validators; no duplication
- `swagger-ui-express` — serves interactive Swagger UI at `/api-docs` (dev/staging only): `app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(spec))`
- `swagger-jsdoc` — NOT used on new work; schema is code-generated from Zod, not JSDoc comments

**When swagger-jsdoc IS used (legacy projects only):**
- Annotate each route handler with a `@swagger` JSDoc block — keeps docs co-located with the route
- All reusable types defined once under `components:` and referenced via `$ref:` — never inline `type: object`

**Single source of truth:**
- Zod schemas define validation AND generate OpenAPI schemas — never write them twice
- All schemas registered in `src/docs/openapi-registry.ts`
- `src/docs/openapi.ts` assembles the final spec from the registry
- Spec is served as JSON at `GET /api-docs/spec.json` for tooling integration

**Every route must document:**
- Summary + description
- All path/query parameters with type and whether required
- Request body schema (reference to Zod-derived schema)
- All response codes: 200/201/204 success + 400/401/403/404/409/422/500 errors
- Auth requirement (`bearerAuth` security scheme)

**Never:**
- Write OpenAPI YAML or JSON by hand — it drifts from the Zod schemas that validate requests
- Duplicate type definitions — if a Zod schema exists, derive the OpenAPI schema from it
- Document a response shape that differs from what the code actually returns
- Expose `/api-docs` in production — gate behind `NODE_ENV !== 'production'`
- Use `type: object` inline in route docs — always `$ref` a named schema
- Use `z.any()` in a documented schema — document the actual shape
- Leave a route undocumented — every public endpoint has a full spec entry

**Related skills — apply together:**
- `api-conventions` — response envelope shapes and route naming must match the documented schemas
- `error-handling` — all AppError-derived codes (400/401/403/404/409/422/500) must appear in response docs
- `typescript-patterns` — Zod schemas are the shared source for TS types + OpenAPI

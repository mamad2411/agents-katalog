---
name: openapi-spec-authoring
description: Writes or repairs an OpenAPI 3.1 spec that matches the real code, lints it, and checks that a generated client compiles against it.
---

# OpenAPI spec authoring

The code is the truth; the spec must prove it.

## Steps

1. List every route with method, path, auth and the request and response types in the code. Look at actual serializers and validators, not only type names.
2. Write OpenAPI 3.1 (JSON Schema compatible). Put every reusable object under `components/schemas` and reference it with `$ref`; never paste the same shape twice.
3. Give every operation a unique `operationId` in verb-noun form (`listOrders`, `createOrder`). Generators use it as the method name.
4. Describe every response that can occur, not only 200: 400, 401, 403, 404, 409, 422, 429 and the 5xx shape, all pointing to one shared error schema.
5. Be exact about types: `format: date-time`, integer ranges, string `maxLength` and `pattern`, enums, `required` lists. Use nullable via `type: [string, "null"]` in 3.1. Mark `additionalProperties` deliberately.
6. Declare `securitySchemes` and apply them per operation; leave public routes with an empty security list.
7. Add one realistic `example` per request and response.
8. Lint with Spectral (`npx @stoplight/spectral-cli lint openapi.yaml`) and fix errors. Generate a client with your chosen generator and compile it.
9. Add a contract test that validates real responses from the test suite against the schemas.

## Rules

- Never describe behavior the code does not have.
- Never leave `type: object` with no properties unless it is truly free-form.

## Report

Routes covered and missing, lint results, generated client status and contract test added.

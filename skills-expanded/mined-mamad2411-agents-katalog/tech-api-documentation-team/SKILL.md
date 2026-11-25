---
name: tech-api-documentation-team
description: End-to-end API documentation workflow. Use when the user wants a complete API documentation expert workflow covering REST/GraphQL API design, OpenAPI/Swagger specs, code-to-doc extraction, API development validation, curl/mock testing, endpoint reference docs, SDK quickstarts, authentication, pagination, error formats, and developer-facing API docs. Coordinates ah-api-designer, sovereign-api-docs-generator, api-dev, api-doc-writer, qa-api-tester, and afrexai-api-docs.
metadata:
  short-description: Complete API documentation workflow
---

# Tech API Documentation

Use this skill as the workflow entry point for a complete API documentation package. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Use `ah-api-designer` to design the API contract: REST/GraphQL shape, resource model, URL naming, versioning, pagination, errors, authentication, authorization, and OpenAPI draft.
2. Use `sovereign-api-docs-generator` to scan code or route/controller descriptions and generate endpoint documentation for REST, GraphQL, WebSocket, examples, and schemas.
3. Use `api-dev` to scaffold, validate, debug, mock, and test APIs with curl/scripts, and to check implementation-documentation consistency.
4. Use `api-doc-writer` to write the human-facing REST API reference: endpoint descriptions, request/response tables, authentication, status codes, and examples.
5. Use `qa-api-tester` to construct executable requests, curl commands, pytest/requests scripts, Postman collections, chained flows, schema validation, and mock data.
6. Use `afrexai-api-docs` to produce final OpenAPI 3.0 YAML/JSON, Markdown API reference, SDK quickstart, curl examples, and multi-language snippets.

## Routing

- If the user is designing a new API, start with `ah-api-designer`.
- If the user provides route files, controller code, schemas, proto files, or GraphQL SDL, use `sovereign-api-docs-generator`.
- If the user needs to implement, debug, validate, mock, or test endpoints, use `api-dev`.
- If the user needs polished reference documentation, use `api-doc-writer`.
- If the user needs executable requests, request chains, response validation, Postman/curl/pytest, or mock data, use `qa-api-tester`.
- If the user asks for final OpenAPI specs, Markdown docs, SDK quickstarts, or developer onboarding docs, use `afrexai-api-docs`.

## Project-First Rules

When working in a local codebase:

1. Inspect route definitions, controllers/handlers, serializers/schemas, OpenAPI files, tests, API clients, and framework conventions before generating docs.
2. Prefer source-of-truth code and existing API conventions over generic templates.
3. Keep API docs consistent with implementation behavior, authentication, error formats, pagination, filtering, sorting, and rate limits.
4. Include request and response examples with realistic sample data.
5. Validate generated OpenAPI or examples when local tooling is available, and state verification limits when it is not.

## Output Package

For a full API documentation package, produce:

1. API design spec: resource model, versioning, pagination, filtering, sorting, auth, and error handling.
2. OpenAPI 3.0 spec: YAML or JSON that can be imported into Swagger UI/Postman.
3. API reference: endpoint descriptions, parameters, request bodies, response schemas, status codes, and examples.
4. SDK quickstart: setup, authentication, curl examples, and snippets for common languages.
5. Validation pack: executable curl commands, mock data, and API test notes.

## Operating Notes

- Keep assumptions explicit.
- Do not invent endpoints, fields, permissions, or status codes when source evidence is available.
- Preserve breaking-change notes and versioning implications.
- When docs and implementation disagree, report the mismatch instead of silently papering it over.

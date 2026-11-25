---
name: rc-openapi
description: Creates or updates an OpenAPI specification by discovering the project's HTTP endpoints, request schemas, and response models from source. Use to keep an openapi.yaml in sync after API changes, or to generate a spec for an existing service. Do not use for Postman collections (use rc-postman), README docs (use rc-readme), or editing source code.
model: sonnet
effort: high
---

# OpenAPI Specification

Generate or maintain an OpenAPI document that mirrors the API's real routes, request contracts, and response models. Document only what exists in source. This skill is standalone and stack-agnostic; it detects how the project defines HTTP endpoints. It only writes the spec file — it never modifies source code.

## Required Inputs

- None. Operates on the current repository.
- Optional: the spec output path (default `.techdocs/docs/openapi.yaml`, or the existing location if one is found) and the target OpenAPI version.

## Workflow

1. Locate the spec and pick the version.
   - Search for an existing `openapi.yaml`/`openapi.json` (`.techdocs/docs/`, `docs/`, repo root). If found, read it for comparison and reuse its output path and version. Otherwise default the output to `.techdocs/docs/openapi.yaml`, creating the directory if needed.
   - For a new spec, default to **OpenAPI 3.1.0**. Use 3.0.3 only if the project's tooling (gateway, codegen, docs renderer) pins it — note the choice in the report.

2. Discover HTTP endpoints from source. Detect the routing mechanism and enumerate every endpoint with method, full path, handler reference, and any summary/description from doc comments or manifest annotations. Routing may live in framework routers (Express, Gin, Spring, FastAPI, etc.) or infrastructure manifests (`serverless.yml` `http` events, API Gateway). Ignore non-HTTP triggers.

3. Extract request contracts from each handler's validation layer: path params, query params, body fields, and required headers — with type, required/optional, defaults, nullability, constraints (uuid, min/max, datetime, enum), and any custom validation messages. Read from the real schema/DTO (Zod, Pydantic, Go structs, class-validator, etc.).

4. Extract response models. For each endpoint determine the success and error responses from the handler's return shape and the domain entities it serializes — including field renames the handler applies — and the HTTP status codes it can emit (2xx success, 4xx validation/not-found/conflict, etc.).

5. Map types to OpenAPI Schema Objects, honoring the chosen version — stay on that one version throughout the document, never mixing 3.0 and 3.1 constructs:
   - `string` → `type: string`; uuid → `format: uuid`; datetime → `format: date-time`; `number`/`integer`, `boolean`, arrays, objects accordingly; open maps → `type: object, additionalProperties: true`.
   - **Nullability**: in 3.1.0 use union types (`type: [string, "null"]`); in 3.0.3 use `nullable: true`.
   - **Examples**: in 3.1.0 prefer `examples`; in 3.0.3 use `example`.

6. Assemble the document:
   - `info` (title, version from the manifest, description), `servers` (real environment URLs), `security` + `components.securitySchemes` for the project's auth scheme, and `tags` grouping operations by domain.
   - `paths`: per operation set `summary`, `description`, a unique `operationId` (the handler/function name), `tags`, `parameters`, `requestBody` when applicable, and all possible `responses` with schemas.
   - `components.schemas`: define reusable entity, request-body, and error schemas. Reference everything with `$ref` — never duplicate a definition inline (DRY). Put required fields in `required`, defaults in `default`, and a realistic, type-correct `example`/`examples` on each field (valid UUIDs, E.164 phones, ISO 8601 dates).

7. Reconcile when updating an existing spec: add new endpoints/schemas, remove ones no longer in source, update changed parameters/bodies/responses, and preserve non-conflicting manual additions (extra descriptions, examples).

8. Validate: the document parses as valid YAML/JSON, every `$ref` resolves, every `required` entry names a real property, and the document conforms to the chosen OpenAPI version. Save to the output path.

9. Report: creation vs update mode, endpoints documented/added/removed/updated, schemas generated, and a pointer to validate the spec (e.g. an OpenAPI linter or editor.swagger.io).

## Error Handling

- If no HTTP endpoints can be discovered, report the routing mechanisms inspected and ask the user to point at the route definitions.
- If a request or response schema cannot be determined, document the operation with what is known and mark the gap rather than fabricating fields.
- If an existing spec is malformed, stop and report it before overwriting.
- If the spec file cannot be written, stop and report the filesystem error.

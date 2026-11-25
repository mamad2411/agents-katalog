---
name: rc-postman
description: Creates or updates a Postman Collection (v2.1.0) and its environment files by discovering the project's HTTP endpoints and request contracts from source. Use to keep a Postman collection in sync after routes or request schemas change, or to bootstrap one for an existing API. Do not use for OpenAPI specs (use rc-openapi), README docs (use rc-readme), or editing source code.
model: sonnet
effort: high
---

# Postman Collection

Keep a Postman collection synchronized with the API's real routes and request contracts. Build requests from what the code accepts, not from guesses. This skill is standalone and stack-agnostic; it detects how the project defines HTTP endpoints.

## Required Inputs

- None. Operates on the current repository.
- Optional: the collection output directory (default `.techdocs/docs/postman/`), the collection name (default derived from the project name), and which environments to emit (default `Local`).

## Workflow

1. Locate the collection. Search for an existing `*.postman_collection.json` (`.techdocs/docs/postman/`, `.techdocs/docs/`, `docs/`). If found, read it to preserve its structure and reuse its directory; otherwise default the output to `.techdocs/docs/postman/`, creating the directory if needed.

2. Discover HTTP endpoints from source. Detect the routing mechanism and enumerate every HTTP endpoint with its method, full path, and handler reference. Routing lives in different places per stack:
   - Framework routers (Express, Fastify, NestJS, Gin, Echo, Spring controllers, FastAPI/Flask, Rails routes, ASP.NET controllers).
   - Infrastructure manifests (`serverless.yml`, API Gateway / OpenAPI definitions, k8s ingress) — use `http` events; ignore non-HTTP triggers (queue, schedule, stream).
   - Exclude non-HTTP entry points (queue consumers, cron jobs, background workers).

3. Extract the request contract for each endpoint from its handler/validation layer:
   - **Path parameters** — name, type, example.
   - **Query parameters** — name, type, required/optional, default.
   - **Body** — fields with type, required/optional, defaults, and constraints, read from the validation schema or DTO (Zod, Joi, Pydantic, class-validator, Go structs + tags, Java/C# DTOs).
   - **Headers** — required headers (content type, auth, custom context headers).
   - Capture a one-line purpose from the handler's doc comment or, failing that, its name.

4. Build or update the collection (Postman Collection Format v2.1.0):
   - **Schema**: `https://schema.getpostman.com/json/collection/v2.1.0/collection.json`.
   - **Folders**: group requests by resource or domain (one folder per resource/tag). Preserve any existing folder organization and non-HTTP helper folders the user maintains.
   - **Requests**: for each endpoint set `method`, the URL using `{{baseUrl}}` as host with the exact path, path variables in Postman `:param` syntax (with example values in the URL `variable` block), required headers, and — for body methods — a realistic example JSON body covering every schema field. Use type-appropriate example values (valid UUIDs for IDs, E.164 for phones, ISO 8601 for timestamps, enum members for enums, `null` for nullable fields).
   - **Collection variables**: keep `{{baseUrl}}` and any existing variables; do not hardcode hosts.
   - Add new endpoints to the most appropriate folder; remove requests whose endpoints no longer exist in source and report them.

5. Emit environment files (one JSON per environment, separate from the collection) under the output directory:
   - Use the standard environment schema (`_postman_variable_scope: "environment"`) with a `values` array of `{key, value, type, enabled}`.
   - **Local**: `baseUrl` pointing at the local dev server; placeholder IDs.
   - Additional environments (e.g. Staging) only when requested or already present: include their `baseUrl` plus any required `Authorization`/context-header variables, referenced from requests via `{{var}}` so values never live in the collection.

6. Validate and save. Ensure the collection and every environment file are valid JSON conforming to v2.1.0. Save the collection and environment files to the output directory.

7. Report the diff: endpoints added, updated, removed (no longer in source), and unchanged.

## Critical Rules

- Do not modify any source code. This skill only writes the collection and environment files.

## Error Handling

- If no HTTP endpoints can be discovered, report the routing mechanisms inspected and ask the user to point at the route definitions.
- If a handler's request schema cannot be located, emit the request with the parameters you could determine and flag the body as incomplete rather than fabricating fields.
- If an existing collection file is malformed JSON, stop and report it before overwriting.
- If files cannot be written to the output directory, stop and report the filesystem error.

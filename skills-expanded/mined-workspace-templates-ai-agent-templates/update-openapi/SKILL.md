---
name: update-openapi
description: Brings your OpenAPI spec in line with changed routes and validates the file, so the spec matches what the server does.
disable-model-invocation: true
---

Update the OpenAPI spec for these changes: $ARGUMENTS (if empty, use `git diff main --stat` to find changed routes).

1. Locate the spec (openapi.yaml, openapi.json, swagger.*) and whether it is hand-written or generated. If generated, run the project's generate command instead of editing by hand.
2. For each changed route, compare the code with the spec: path, method, parameters, request body, response codes, response schemas, security.
3. Edit only the differing parts. Reuse `components/schemas` and `$ref` rather than copying objects. Keep operationIds unique and follow the file's existing style.
4. Mark deprecated routes with `deprecated: true`, not by deleting them.
5. Validate with the tool in the repo or `npx @redocly/cli lint <file>` (or `npx swagger-cli validate <file>`). Fix every error.
6. Classify each change as breaking (removed or renamed field, new required field, changed type) or compatible.

Show a summary table of changes with the breaking ones first, plus the diff. Ask before writing the file if more than five operations change.

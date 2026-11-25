---
name: add-endpoint
description: Adds a new API endpoint that matches your existing routes, with validation, error handling, tests and docs in one pass.
disable-model-invocation: true
---

Add this endpoint to the project: $ARGUMENTS

1. Find the closest existing endpoint with `grep` or the route table. Read its handler, schema, service call, test and doc entry. Copy that structure exactly: folder, naming, auth middleware, response envelope.
2. State a short plan: method, path, auth, input fields with types, success status, and each error status. Ask one question if the request is ambiguous, otherwise continue.
3. Write the handler thin. Put business logic in the layer the project already uses for it.
4. Validate every input with the project's own validator. Return the same error shape as other routes (400 for bad input, 401 or 403 for auth, 404 for missing, 409 for conflicts).
5. Add tests: one success case, one case per error status, one for bad input.
6. Update the route list, OpenAPI file or README section if one exists.
7. Run the test suite and the linter. Fix what you broke.

Report the files changed, the final request and response examples, and anything you guessed. Do not touch unrelated routes or run migrations without asking first.

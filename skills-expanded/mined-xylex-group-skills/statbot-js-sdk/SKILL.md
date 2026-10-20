---
name: statbot-js-sdk
description: Maintain the statbot-js repository by turning route docs or route metadata into root OpenAPI artifacts, keeping the TypeScript SDK and Zod validation aligned with every route, splitting one typed example file per operation, and preserving npm and xbp publishability. Use when working in statbot-js on OpenAPI generation, SDK surface changes, validation updates, per-route example maintenance, contract tests, or release-readiness checks.
---

# Statbot JS SDK

Use this skill for repo-local work in `statbot-js`.

Treat the OpenAPI contract, generated SDK types, runtime validation, per-route examples, and publishability checks as one surface. Update them together.

## Start Here

Inspect the current repo state before editing:

- `openapi/openapi.json` and `openapi/openapi.yaml`
- `scripts/generate-openapi.mjs`
- `scripts/openapi/route-metadata.mjs` and sibling generator helpers
- `src/client.ts`, `src/validation.ts`, `src/query-types.ts`, `src/errors.ts`, `src/index.ts`
- `src/generated/openapi-types.ts`
- `examples/routes/*.ts`, `examples/all-routes.ts`, `examples/shared.ts`
- `test/openapi.test.ts`, `test/client.test.ts`
- `README.md`, `docs/routes-and-examples.md`, `.xbp/xbp.yaml`

Read [references/rules.md](references/rules.md) before editing when the task touches route generation, validation, examples, or release flow.

## Workflow

1. Update the route source of truth first.
2. Regenerate the OpenAPI artifacts and generated TypeScript types.
3. Align the client surface, runtime validation, and exported types.
4. Keep one typed example file per operation and refresh docs that point at them.
5. Run the verification commands from `references/rules.md`.
6. If the user asks for commit or release follow-through, finish that workflow instead of stopping at code edits.

## Output Rules

- Keep `openapi/` limited to the generated contract artifacts in the final state.
- Keep runtime validation at the SDK boundary with Zod rather than scattering ad hoc checks.
- Keep examples flat and route-specific under `examples/routes/`.
- Keep docs concise and point to the real example files.
- Keep the repo publishable after changes.

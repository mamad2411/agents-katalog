---
name: sqlc-gen-typescript-dal
description: Configure sqlc to generate a TypeScript data access layer for PostgreSQL with tylergannon/sqlc-gen-typescript and postgres.js. Use when an agent needs to add or repair sqlc.yaml/sqlc.yml, generate DAL query wrappers, choose plugin options, wire the postgres.js runtime, handle PostgreSQL dialect details, or configure type overrides/converters for this generator.
---

# sqlc-gen-typescript DAL

Use this skill to add or maintain a generated TypeScript DAL using `sqlc`,
PostgreSQL, `postgres.js`, and the `tylergannon/sqlc-gen-typescript` WASM
plugin.

## Reference Index

Load the relevant reference before editing that surface:

- `references/configuration.md`: sqlc project layout, `sqlc.yaml` plugin setup,
  release WASM URL, local WASM builds, generation commands, and proof steps.
- `references/postgresql-dialect.md`: PostgreSQL query and schema rules that
  affect generated TypeScript, including named params, nullability, JSON, enums,
  bigint, and unsupported types.
- `references/type-overrides.md`: `options.overrides`, `ts_type`, `raw_type`,
  `convert`, nullable `db_type` behavior, column matching, and converter imports.

## Workflow

1. Inspect the target repo for an existing `sqlc.yaml`, schema files, query
   files, generated DB folder, package manager, and postgres.js client setup.
2. Read `references/configuration.md` before creating or changing sqlc config.
3. Read `references/postgresql-dialect.md` before changing SQL queries or schema
   to satisfy generation.
4. Read `references/type-overrides.md` before adding or changing any
   `options.overrides` entry.
5. Configure sqlc with the release WASM plugin unless the user explicitly asks
   for a local development build.
6. Generate the DAL with `sqlc generate`; if the repo has a wrapper such as
   `just generate`, `npm run generate`, or `pnpm sqlc`, prefer the local command.
7. Wire application code to pass a configured `postgres` `Sql` client into
   generated functions. Do not make generated functions own connection setup.
8. Prove the generated DAL by running sqlc generation plus the target repo's
   TypeScript checks/tests that compile the generated output.

## Invariants

- Target PostgreSQL only. Do not configure MySQL, SQLite, or Bun SQL for this
  generator.
- Use the `postgres` npm package runtime. Generated functions accept a
  `postgres` `Sql` instance as their first argument.
- Keep generated files generated. Fix source schema/query/config/override inputs
  instead of hand-editing generated TypeScript.
- Preserve `transform: postgres.camel` when SQL column names are snake_case and
  generated TypeScript fields are camelCase.
- Current bigint policy is `number`; configure postgres.js OID `20` parsing when
  selecting `int8`, `bigint`, `bigserial`, or `serial8`, and avoid this policy
  for values that may exceed `Number.MAX_SAFE_INTEGER`.

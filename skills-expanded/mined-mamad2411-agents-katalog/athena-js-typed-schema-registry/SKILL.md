---
name: athena-js-typed-schema-registry
description: Table DSL and typed registry guide for `@xylex-group/athena`. Use when implementing or debugging `table(...).schema(...).columns(...).primaryKey(...)`, `defineModel` compatibility, `defineSchema` or `defineDatabase` or `defineRegistry`, `createTypedClient`, `fromModel(...)`, tenant context mapping, model-derived form helpers, or consumer code that should derive directly from generated `athena/models/*` contracts. Use when the user runs /athena-js-typed-schema-registry.
---

# Athena JS Typed Schema Registry

Use this skill when the main seam is model or registry semantics:

1. table DSL authoring
2. `defineModel(...)` compatibility
3. typed registries and `createTypedClient(...)`
4. `fromModel(...)` behavior
5. tenant key maps and tenant context
6. model-derived form helpers
7. `table.schemas.row/insert/update/form` and value-based `from(modelValue)` usage
8. consumer code that should use generated `athena/models/*` types instead of wrappers

If the task is mainly generator config or output layout, also use
`$athena-js-generator`.

If the task is mainly runtime query or auth behavior outside the registry seam,
also use `$athena-js`.

## Source of truth order

1. Read `package.json` first for the current SDK version and export map.
2. Read `docs/typed-schema-registry.md` and the typed sections of `docs/getting-started.md`.
3. Read `docs/type-safety-playbook.md` when the task is about reducing duplicate app-layer types.
4. Read `docs/type-surface-manifest.md` when the task depends on the canonical generated table-builder surface or exported typed helpers.
5. Read `src/schema/index.ts`, `src/schema/table-builder.ts`, `src/schema/table-columns.ts`, `src/schema/definitions.ts`, `src/schema/typed-client.ts`, and `src/schema/model-form.ts`.
6. Read `test/schema-table-builder.test.ts`, `test/typed-client.test.ts`, and the model-form tests that match the seam.
7. Read [references/registry-surface.md](references/registry-surface.md) for copy-ready patterns and the non-obvious runtime rules.

If docs and source disagree:

- trust the current schema source and tests over stale examples
- preserve `defineModel(...)` compatibility even when table DSL is the preferred authoring style

## Follow this workflow

1. Decide whether the task is authoring a model contract, consuming one, changing typed-client behavior, or fixing the generated model contract surface.
2. Prefer the current table DSL for new model authoring.
3. Keep `defineModel(...)` support additive and valid for compatibility.
4. Prefer direct use of existing `athena/models/*` contracts in consumer repos instead of cloning row or payload types.
5. Keep generator layout decisions in the generator skill; do not patch registry usage by inventing a second model surface.

## Registry rules

- Table DSL is the canonical authoring surface for new work.
- `defineModel(...)`, `defineSchema(...)`, `defineDatabase(...)`, and `defineRegistry(...)` remain valid compatibility builders.
- `fromModel(...)` resolves registry metadata first and then delegates to the normal runtime query builder.
- `from(modelValue)` is the direct runtime shortcut when the exported table/model value is already in scope; a type-only generic cannot recover a runtime target after TypeScript erases it.
- Generated model contracts should stay under `athena/models/{schema}/*`; do not flatten schema-scoped output into a second fake surface such as `athena/generated`.
- The root client can infer a runtime target from a model or table value passed to `from(...)`; a type-only generic cannot do that after TypeScript erases it.
- Use `tenantKeyMap` and `withTenantContext(...)` instead of hardcoding tenant headers at each callsite.
- Use `createModelFormAdapter`, `toModelFormDefaults`, and `toModelPayload` before building repo-local null-normalization helpers.

## Validation

- schema or typed-client changes: targeted schema tests plus `pnpm typecheck`
- repo-facing typed-surface changes: `pnpm check:all`
- generator/registry interplay changes: run the matching generator dry-run or generator tests too

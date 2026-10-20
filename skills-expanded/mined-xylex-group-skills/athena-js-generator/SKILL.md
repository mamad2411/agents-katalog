---
name: athena-js-generator
description: Generator config and CLI guide for `@xylex-group/athena`. Use when implementing, debugging, or explaining `athena-js generate`, `athena.config.ts/js`, provider modes, output presets or targets, `athena/models` generation layout, dry-run review output, protected registry/database writes, table filters, or direct-vs-gateway introspection behavior in the current `athena-js` repo or a consumer repo. Use when the user runs /athena-js-generator.
---

# Athena JS Generator

Use this skill when the real seam is generator syntax or output behavior:

1. `athena-js generate` or `runSchemaGenerator(...)`
2. `athena.config.ts` / `athena-js.config.ts`
3. output format, preset, target, or placeholder changes
4. dry-run review behavior
5. schema-scoped `athena/models/{schema_kebab}/*`, `athena/schemas/*`, `athena/relations.ts`, or registry generation layout
6. generator-side surface reduction through include or exclude table filters

If the task is mostly runtime client behavior, use `$athena-js`.

If the task is mainly table DSL or typed registry usage after generation, also
use `$athena-js-typed-schema-registry`.

## Source of truth order

1. Read `package.json` first for the current SDK version.
2. Read `docs/generator-quickstart.md`, `docs/generator-config.md`, and `docs/cli-command-reference.md`.
3. Read `docs/generator-cicd.md` when CI or release behavior is involved.
4. Read `src/generator/config.ts`, `src/generator/types.ts`, `src/generator/pipeline.ts`, `src/generator/renderer.ts`, and `src/cli/index.ts`.
5. Read `test/generator-config.test.ts`, `test/generator-pipeline.test.ts`, and `test/cli.test.ts` for the exercised contract.
6. Read [references/config-syntax.md](references/config-syntax.md) for copy-ready config patterns and non-breaking rules.

If docs and source disagree:

- trust the current generator source and tests over older docs
- preserve the existing compatibility defaults unless the task explicitly authorizes a breaking generator change

## Follow this workflow

1. Confirm whether the task is changing defaults, an opt-in mode, or only docs and review output.
2. Inspect `output.format`, `output.preset`, and `output.targets` before patching downstream scripts.
3. Keep the legacy layout compatible unless the user explicitly requests a contract break.
4. Prefer opt-in paths such as `output.preset = "athena-direct"` for safer direct generation.
5. Use table filters when the goal is to reduce generated surface area without changing runtime contracts.

## Generator rules

- `table-builder` is stable generator output.
- `experimental.findManyAst` is runtime-only and does not enable table output.
- The safe direct default now uses `output.preset = "athena-direct"` and writes registry output to `athena/registry.generated.ts`.
- Prefer `output.preset = "legacy"` only when a repo intentionally needs registry output at `athena/config.ts`.
- The recommended modern direct layout is `output.preset = "athena-direct"` plus `output.format = "table-builder"`, which yields schema-scoped models under `athena/models/{schema_kebab}/*`, schema assemblies under `athena/schemas/*`, `athena/relations.ts`, and `athena/registry.generated.ts`.
- Existing generated `database` and `registry` files are protected from overwrite; review CLI skip output before assuming generation failed.
- Use `filter.includeTables` and `filter.excludeTables` to reduce generated model count without inventing a parallel staging tree.
- Keep `athena/models/*` as the model contract surface; do not route users toward `athena/generated` or a duplicate registry path unless the repo explicitly owns that alternative.
- Use dry-run output to prove the exact mode and targets. If the CLI warns about `athena/config.ts`, fix the generator config instead of synthesizing replacement output in a review script.

## Validation

- Generator source changes: targeted generator tests plus `pnpm typecheck`
- Public generator docs or CLI behavior: `pnpm docs:methods` when method docs drift, then `pnpm check:all`
- Consumer-facing dry-run or layout fixes: prove the output with `athena-js generate --dry-run` or the repo script that wraps it

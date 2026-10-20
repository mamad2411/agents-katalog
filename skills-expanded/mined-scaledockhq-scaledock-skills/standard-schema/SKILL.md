---
name: standard-schema
description: "Standard Schema v1: accept any validator via ~standard, and implement or consume the @standard-schema/spec interfaces (StandardSchemaV1, StandardJSONSchemaV1, StandardTypedV1). Covers Standard Schema v1, the only line (package 1.1.0, upgrades from 1.0.0); no preview exists. Use when writing a library, framework, form, router, RPC or MCP tool that accepts user schemas from Zod, Valibot, ArkType, Effect Schema or any compliant validator; when making a schema library spec-compliant; when handling the validate result ({ value } or { issues }) and sync or async validation; when inferring types with InferInput and InferOutput; or when generating JSON Schema (draft-2020-12, draft-07, openapi-3.0) from a schema with Standard JSON Schema. Triggers: standard schema, ~standard, @standard-schema/spec, StandardSchemaV1, validator-agnostic, schema adapter, issues path, jsonSchema.input, jsonSchema.output."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.1"
  kind: standard
---

# Standard Schema

Standard Schema is a family of TypeScript interfaces, designed by the creators of Zod, Valibot and ArkType, that let tools accept user-defined schemas from any compliant library without per-library adapters. The types are published as `@standard-schema/spec`. With this skill the agent consumes or implements `StandardSchemaV1` (validation) and `StandardJSONSchemaV1` (JSON Schema conversion), both built on `StandardTypedV1`.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). The spec has no numbered sections, so citations name the interface member in `@standard-schema/spec` 1.1.0 (for example `StandardSchemaV1.SuccessResult`) or the FAQ question on the spec page. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: consumer (a tool that accepts schemas), implementer (a schema library), or both.
- Interfaces: `StandardSchemaV1` (validate), `StandardJSONSchemaV1` (convert to JSON Schema), or both.
- Sync or async: whether the consumer can await validation.
- Target version: Standard Schema v1 (default and only line), from `@standard-schema/spec` 1.1.0. Code written against 1.0.0 is the same line and upgrades without changes. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned package version in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the npm registry for a newer `@standard-schema/spec` version and the repository tags for a new release, and update the pins.

## Invariants

1. **One namespaced property.** The whole interface lives under the `~standard` property, with `version: 1` and a `vendor` string naming the library (`StandardTypedV1.Props`; design goals "Avoid API conflicts").
2. **`validate` takes `unknown`.** `~standard.validate(value, options?)` returns a `Result` or a `Promise` of one (`StandardSchemaV1.Props.validate`). `options.libraryOptions` carries vendor-specific parameters (`StandardSchemaV1.Options`).
3. **The result shape decides success.** Success is `{ value }` with `issues` undefined; a falsy `issues` means success. Failure is `{ issues }`, an array of `Issue` (`StandardSchemaV1.SuccessResult`, `StandardSchemaV1.FailureResult`).
4. **Issues have a message and an optional path.** `message` is a string; `path` is an array whose segments are a `PropertyKey` or an object `{ key }` (`StandardSchemaV1.Issue`, `StandardSchemaV1.PathSegment`).
5. **Async is allowed but discouraged.** A consumer that only accepts synchronous validation throws when `validate` returns a `Promise`; libraries are encouraged to validate synchronously whenever possible (FAQ "How to only allow synchronous validation?").
6. **Types are type-level only.** `types` is optional and exists for inference; read it with `InferInput` and `InferOutput` (`StandardTypedV1.Types`, `StandardTypedV1.InferInput`, `StandardTypedV1.InferOutput`).
7. **The package is optional and types-only.** Copy the types or depend on `@standard-schema/spec` and import with `import type`. If the interface is part of your public API, it is a regular dependency, never a dev dependency (FAQ "Do I need to add `@standard-schema/spec` as a dependency?", "Can I add it as a dev dependency?").
8. **JSON Schema conversion may throw.** `~standard.jsonSchema.input(options)` and `.output(options)` return a JSON Schema object for a `target`; implementers should throw for unsupported targets, and consumers should account for a throw (`StandardJSONSchemaV1.Converter`, `StandardJSONSchemaV1.Options`; Standard JSON Schema FAQ "What about error handling?").
9. **The two specs are orthogonal.** `StandardJSONSchemaV1` has no validation; an object may implement either or both (Standard JSON Schema FAQ "What's the relationship between this and Standard Schema?").

## Workflow

1. **Pick the version.** Use v1 from package 1.1.0; check whether existing code pins 1.0.0, which lacks `StandardJSONSchemaV1`, `StandardTypedV1` and `validate` options.
   -> [`references/versions.md`](references/versions.md)
   ✓ The package version is 1.1.0 or later wherever `StandardJSONSchemaV1` or `StandardTypedV1` is used.
2. **Add the types.** Depend on `@standard-schema/spec` at the pinned version as a regular dependency, or copy the interfaces verbatim.
   -> [`references/interface.md`](references/interface.md)
   ✓ The types match the pinned `src/index.ts`, and nothing imports them as values.
3. **Consume schemas.** Accept a generic `T extends StandardSchemaV1`, call `~standard.validate`, handle a `Promise` (await it or reject it), branch on `issues`, and normalize issue paths.
   -> [`references/consuming.md`](references/consuming.md)
   ✓ Input and output types come from `InferInput` and `InferOutput`, and no code depends on a specific `vendor`.
4. **Implement the interface** (schema library authors). Add `~standard` to every schema object, returning `{ value }` or `{ issues }` from your existing validation code.
   -> [`references/implementing.md`](references/implementing.md)
   ✓ The schema satisfies `StandardSchemaV1<Input, Output>` with `satisfies` or `implements`, and validates synchronously where possible.
5. **Generate JSON Schema** where needed. Call `jsonSchema.input` or `.output` with a `target`; implementers support `draft-2020-12` and `draft-07` at least.
   -> [`references/json-schema.md`](references/json-schema.md)
   ✓ Unsupported targets throw in the implementer and are caught in the consumer, and input and output schemas are chosen deliberately.
6. **Check which libraries qualify.** Confirm the minimum version of each validator your users bring.
   -> [`references/libraries.md`](references/libraries.md)
   ✓ Documentation names minimum versions from the spec pages, and notes libraries that need an adapter.
7. **Upgrade** (only when asked). Follow the 1.0.0 to 1.1.0 section.
   -> [`references/versions.md`](references/versions.md)
   ✓ The code type-checks against 1.1.0 and validates the same values as before.

## Verify before done

- [ ] Each implemented schema satisfies the pinned interface: `version` is `1`, `vendor` is set, `validate` returns `{ value }` or `{ issues }`.
- [ ] Consumers test `result.issues` for truthiness, as the official `integrate.ts` example does, rather than testing `value`.
- [ ] A consumer that cannot await rejects a `Promise` result with a clear error, as in the spec FAQ.
- [ ] Issue paths are normalized from both segment forms before display or serialization.
- [ ] `@standard-schema/spec` is in `dependencies` (or the types are copied), never only in `devDependencies`, when it appears in your public types.
- [ ] JSON Schema calls pass an explicit `target` and handle a thrown error.
- [ ] Code compiles against the official examples in the repository's `packages/examples` at the pinned tag.

## Reference index

- **`references/versions.md`**: the v1 line, what changed between packages 1.0.0 and 1.1.0, the upgrade steps, and why no preview is listed. Load for steps 1 and 7.
- **`references/interface.md`**: the full v1 interfaces with each member explained. Load for step 2.
- **`references/consuming.md`**: generic validation helpers, sync-only handling, path normalization, and turning issues into an HTTP error body. Load for step 3.
- **`references/implementing.md`**: adding `~standard` to a schema library, with the official example. Load for step 4.
- **`references/json-schema.md`**: `StandardJSONSchemaV1`, targets, input versus output, combining with `StandardSchemaV1`. Load for step 5.
- **`references/libraries.md`**: implementers and minimum versions for both specs, as listed on 2026-10-02. Load for step 6.

## Related skills

- `openapi` for placing Standard JSON Schema output (for example the `openapi-3.0` or `draft-2020-12` target) into an OpenAPI document: `npx skills add ScaleDockHQ/scaledock-skills --skill openapi`.
- `problem-details` for returning validation issues as an RFC 9457 response: `npx skills add ScaleDockHQ/scaledock-skills --skill problem-details`.
- `json-schema` for writing and reviewing the JSON Schema that `StandardJSONSchemaV1` converters emit: `npx skills add ScaleDockHQ/scaledock-skills --skill json-schema`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Standard Schema specification](https://standardschema.dev/schema): Released, v1 in `@standard-schema/spec` 1.1.0, checked 2026-10-02.
- [Standard JSON Schema specification](https://standardschema.dev/json-schema): Released, v1 in `@standard-schema/spec` 1.1.0, checked 2026-10-02.
- [Standard Schema project overview](https://standardschema.dev/): Released, `@standard-schema/spec` 1.1.0 (adds `StandardTypedV1`), checked 2026-10-02.
- [`@standard-schema/spec` source at tag v1.1.0](https://github.com/standard-schema/standard-schema/tree/v1.1.0/packages/spec): Released, tag v1.1.0, checked 2026-10-02.
- [`@standard-schema/spec` source at tag v1.0.0](https://github.com/standard-schema/standard-schema/tree/v1.0.0/packages/spec): Released, tag v1.0.0 (2025-01-27), checked 2026-10-05.
- [`@standard-schema/spec` v1.1.0 release](https://github.com/standard-schema/standard-schema/releases/tag/v1.1.0): Released, v1.1.0 (2025-12-15), checked 2026-10-05.
- [`@standard-schema/spec` on the npm registry](https://registry.npmjs.org/@standard-schema/spec): Released, 1.1.0 (latest dist-tag, published 2025-12-15), checked 2026-10-05.

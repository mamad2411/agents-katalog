---
name: atscript
description: >-
  Use when working with `@atscript/*` packages or `.as` files. `.as` = single
  source of truth for types, metadata, and validation constraints. Covers `.as`
  syntax, `@meta.*` / `@expect.*` / custom annotations, primitives, the `asc`
  CLI + `atscript.config.*`, generated `.as.d.ts` / `.as.js` / `atscript.d.ts`,
  runtime helpers (`Validator`, JSON Schema, serialize), `unplugin-atscript`,
  `@atscript/moost-validator`, VSCode LSP, and plugin authoring.
---

# atscript

`.as` = single source of truth for types + metadata + validation. `@atscript/typescript` compiles `.as` → `.d.ts` (types) + `.js` (runtime metadata). Consumers use those for validation, JSON Schema, serialization, ORM mapping.

Language-agnostic. Core ships only `@meta.*` + `@expect.*`; `@db.*`, `@ui.*`, and custom namespaces come from plugins.

## Quick start

```bash
npm install @atscript/typescript @atscript/core
```

`atscript.config.{ts,mts,cts,js,mjs,cjs}` at project root:

```ts
import { defineConfig } from '@atscript/core'
import ts from '@atscript/typescript'

export default defineConfig({
  rootDir: './src',
  plugins: [ts()],
})
```

Build:

```bash
npx asc            # emits .d.ts (default) + project-wide atscript.d.ts
npx asc -f js      # emits runtime .js metadata
```

Full walkthrough with a first `.as` file, consume snippet, and troubleshooting → [getting-started.md](references/getting-started.md).

## Key imports

```ts
// Config
import { defineConfig, AnnotationSpec } from '@atscript/core'
import type { TAtscriptPlugin, TAtscriptConfig } from '@atscript/core'

// Plugin factory (build-time only)
import ts from '@atscript/typescript'

// Runtime helpers (used by generated .as.js — also available to consumers)
import {
  defineAnnotatedType,             // fluent builder (in generated code)
  forAnnotatedType,                // kind-dispatched walker
  Validator, ValidatorError,
  buildJsonSchema, fromJsonSchema, mergeJsonSchemas,
  serializeAnnotatedType, deserializeAnnotatedType, SERIALIZE_VERSION,
  isAnnotatedType, isAnnotatedTypeOfPrimitive,
} from '@atscript/typescript/utils'
import type { TAtscriptAnnotatedType, TValidatorPlugin } from '@atscript/typescript/utils'

// Test fixtures (compile .as at test-time, inject tsPlugin automatically)
import { prepareFixtures } from '@atscript/typescript/test-utils'

// Moost HTTP integration
import { validatorPipe, validationErrorTransform } from '@atscript/moost-validator'

// Bundler integration (pick one)
import atscript from 'unplugin-atscript/vite'      // or /rollup /rolldown /webpack /esbuild /rspack /farm
```

## Invariants

1. `@meta.id` takes no arguments. Multiple `@meta.id` on different props = composite PK. Never `@meta.id(...)`.
2. Generated files (`*.as.d.ts`, `*.as.js`, `atscript.d.ts`) are never hand-edited. Fix the `.as` source or plugin. Regenerate with `npx asc -f dts`.
3. Core ships `@meta.*` + `@expect.*` only. All other namespaces come from plugins.
4. Default CLI format is `dts`. Runtime `.js` requires `-f js` (or let `unplugin-atscript` produce it at bundle time).
5. `@atscript/typescript/utils` is the runtime entry; `@atscript/typescript` default export is `tsPlugin()` (build-time factory).

## Dependency chain

```
@atscript/core          parser, AST, plugin system, diagnostics
  └─ @atscript/typescript    codegen + runtime + asc CLI
       ├─ @atscript/moost-validator   Moost pipe + error transform
       └─ unplugin-atscript           Vite/Rollup/Rolldown/Webpack/esbuild/Rspack/Farm
  └─ @atscript/vscode     LSP, syntax, completions, go-to-def
```

DB layer (`@atscript/db`, `db-sqlite`, `db-mongo`, `db-mysql`, `moost-db`, `@db.*`, schema sync, relations, views): separate repo at https://db.atscript.dev.
UI layer (`@atscript/ui`, `vue-form`, `vue-table`, Moost workflow, `@ui.*`): separate repo.

Companion skills:

```bash
npx skills add moostjs/atscript      # this skill (core/typescript/unplugin/vscode/moost-validator)
npx skills add moostjs/atscript-db   # DB layer
npx skills add moostjs/atscript-ui   # UI layer
```

## References — load only what's needed

| Domain            | File                                                      | When                                                                                        |
| ----------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| First contact     | [getting-started.md](references/getting-started.md)       | Install, first `.as`, first codegen run, consume snippet, troubleshooting                   |
| `.as` syntax      | [as-syntax.md](references/as-syntax.md)                   | interface/type, unions, intersections, tuples, arrays, imports, pattern properties          |
| Annotations       | [annotations.md](references/annotations.md)               | `@meta.*`, `@expect.*`, merge, custom `AnnotationSpec`                                      |
| Primitives        | [primitives.md](references/primitives.md)                 | Built-ins, semantic extensions, decimal, phantom, extending via config                      |
| Config            | [config.md](references/config.md)                         | `atscript.config.*`, `defineConfig`, entries/globs, plugin wiring, output                   |
| `asc` CLI         | [asc-cli.md](references/asc-cli.md)                       | `asc`, `-f`, `-c`, `--noEmit`, scripts                                                      |
| Codegen           | [codegen.md](references/codegen.md)                       | `.as` → `.d.ts`/`.js`, `atscript.d.ts` global `AtscriptMetadata`                            |
| Runtime           | [runtime.md](references/runtime.md)                       | `defineAnnotatedType`, `TAtscriptAnnotatedType`, `forAnnotatedType`, serialize, refDepth    |
| Validation        | [validation.md](references/validation.md)                 | `Validator`, `ValidatorError`, JSON Schema helpers, plugins                                 |
| Build integration | [unplugin.md](references/unplugin.md)                     | Vite/Rollup/Rolldown/Webpack/esbuild/Rspack/Farm, HMR, strict                               |
| Moost integration | [moost-validator.md](references/moost-validator.md)       | Moost pipes, error transform                                                                |
| VSCode            | [vscode.md](references/vscode.md)                         | Extension, LSP features, config autodiscovery                                               |
| Plugin authoring  | [plugin-development.md](references/plugin-development.md) | `TAtscriptPlugin`, `AnnotationSpec`, render/buildEnd                                        |

Full docs: https://atscript.dev.

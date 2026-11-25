---
name: martix-typescript
description: Type-first TypeScript 7 authoring, migration, debugging, and review for `.ts`/`.tsx`, tsconfig, compiler diagnostics, generics, narrowing, module resolution, declarations, project references, and type-check performance. Use when implementing or fixing TypeScript, designing typed APIs, resolving TS errors, migrating TypeScript 5/6 to 7, or coordinating TS7 with tools that still require the TypeScript 6 compiler API.
license: Complete terms in LICENSE.txt
---

# MartiX TypeScript 7 router

Use a **type-first** process: learn the project's compiler and host before
choosing types or configuration. TypeScript 7 is the greenfield default, while
existing projects keep their installed baseline unless the task includes an
upgrade.

## Process

### 1. Inventory the project

Start with the relevant source and the user's requested boundary. For work that
can change compilation, resolution, declarations, or runtime behavior, also read
`package.json`, the lockfile, `tsconfig*`, extended configs, and project
references. Detect what the concern depends on:

- the package manager and local TypeScript version;
- the runtime or build host: Node, Bun, Deno, browser bundler, or framework
  compiler;
- existing typecheck, build, test, and lint commands;
- tools that consume the TypeScript compiler API or embed its language service.

For TypeScript 7 adoption or tooling uncertainty, open
[the compatibility map](./references/typescript-7-compatibility-map.md).

**Complete when:** the compiler generation, host, package boundary, and
validation path needed for the requested concern are known; config graphs remain
unloaded when they cannot affect the result.

### 2. Route the concern

Open only the smallest matching rule or decision map.

| Concern | Start with | Add when needed |
| --- | --- | --- |
| Public types and API shape | [Type design](./rules/language-type-design.md) | [Narrowing and boundaries](./rules/language-narrowing-boundaries.md) |
| Generics or type-level programming | [Generics and advanced types](./rules/language-generics-advanced-types.md) | [Type tests](./rules/quality-type-tests.md) |
| `tsconfig` or project references | [Project configuration](./rules/config-project-shape.md) | [tsconfig decision map](./references/tsconfig-decision-map.md) |
| ESM, CJS, aliases, or resolution errors | [Host-aware modules](./rules/modules-host-resolution.md) | [Module host map](./references/module-host-map.md) |
| Libraries or `.d.ts` output | [Declarations and publishing](./rules/libraries-declarations-publishing.md) | [Type tests](./rules/quality-type-tests.md) |
| TypeScript 5/6 to 7 | [TypeScript 7 migration](./rules/migration-typescript-7.md) | [Compatibility map](./references/typescript-7-compatibility-map.md) |
| ESLint, transformers, or embedded tooling on TS7 | [Compiler API compatibility](./rules/tooling-api-compatibility.md) | [Compatibility map](./references/typescript-7-compatibility-map.md) |
| Slow typecheck or monorepo build | [Performance diagnostics](./rules/performance-diagnostics.md) | [Compiler diagnostics map](./references/compiler-diagnostics-map.md) |
| `allowJs`, `checkJs`, or JSDoc migration | [JavaScript and JSDoc changes](./references/javascript-jsdoc-ts7-changes.md) | [Narrowing and boundaries](./rules/language-narrowing-boundaries.md) |

Use [AGENTS.md](./AGENTS.md) when a task crosses several branches or needs a
companion-skill handoff.

**Complete when:** every requested concern has one owner and unrelated
references remain unloaded.

### 3. Design type-first

Define the input and output boundaries, valid states, inference points, public
surface, and runtime validation boundary before introducing type machinery.
Prefer the smallest type model that makes invalid states hard to express.

**Complete when:** the proposed types express the required invariants without
speculative abstractions or unchecked boundary data.

### 4. Implement locally

Reuse project types, helpers, scripts, and conventions. Make the smallest
coherent change. Add type-level or runtime tests at the boundary affected by the
change; a type assertion alone does not validate untrusted runtime data.

**Complete when:** implementation and focused tests cover the changed contract.

### 5. Validate independently

Run the smallest existing project commands that prove the change. Run each
relevant command independently so one success cannot hide another failure.
Prefer the project's typecheck command; use a direct compiler command only when
the project has no equivalent, and label it as a fallback.

When public types or compiler configuration changed, also verify declaration
emit, project-reference builds, or type tests as applicable.

**Complete when:** every relevant check succeeds and no failure is masked by a
fallback command.

### 6. Review the delta

Check exported API, runtime/type boundaries, module-host alignment, config
impact, and TS6/TS7 tooling compatibility. Keep framework, lint-policy,
test-runner, bundler, and publishing mechanics with their owning skills.

**Complete when:** the requested outcome is proven without unrelated policy or
unverified compatibility claims.

## Handoff boundaries

- Use the matching framework skill when React, Vue, Angular, Svelte, Astro, or
  SPFx APIs drive the design; keep cross-cutting TypeScript decisions here.
- Use a testing skill for runtime architecture, mocks, or runner configuration.
- Use a linting skill for ESLint rule selection or lint policy.
- Use a package-management skill for publishing, semver, or lockfile work.
- Use a bundler skill for bundler-specific transforms or optimization.
- Use a JavaScript skill when no TypeScript or typed-JavaScript concern remains.

## Source stance

The technical baseline is dated because TypeScript 7 tooling compatibility is
moving quickly. Use [the source index](./references/source-index.md) for official
anchors and re-check current compatibility before changing version guidance.

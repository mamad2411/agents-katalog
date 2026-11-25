---
name: follow-lib-arktype
description: Use ArkType for TypeScript runtime validation with native type syntax
argument-hint: "[scope]"
related:
  - follow-lib-zod
  - deep-review-codebase
  - follow-lib-better-auth
  - follow-lang-typescript
  - follow-best-practice
  - use-my-packages-on-registry
  - setup-cicd

---

## Goal

Use the latest ArkType for TypeScript runtime validation — native type syntax keeps schema and type in sync between compile-time and runtime with high performance

## Scope

Applies to any TypeScript project that supports ESM and strict mode — Bun, Node.js, frontend, backend, or any framework

Boundaries:
- Use this skill when the project chose/uses ArkType as its main validator
- If the project already uses Zod → use `/follow-lib-zod` instead (do not mix two primary validators in one domain)
- If no validation library is chosen yet → run `/deep-review-codebase` to compare first

- Latest: `arktype@2.2.3` (verified 2026-09-13)
- Key v2.2 features: `type.fn` (validated functions), type-safe regex via `arkregex` (`x/.../` literal + named groups), `@ark/json-schema` (bidirectional JSON Schema), Standard Schema validators embeddable directly in definitions, `|>` pipe operator, `type.valueOf` for TS enums, keywords `string.hex`/`string.regex`, serializable `ArkErrors`
- References: [apis](references/apis.md) 
## Execute

### Workflows

| Topic | Workflow |-------|----------| Setup | `workflows/setup-arktype/SKILL.md` — install, `type()` basics, scope config 
### 1. Install ArkType

> Goal: install ArkType and prepare the environment

1. Run `bun add arktype` (or `pnpm add arktype` per the project's package manager)
2. Check the latest version at `https://www.npmjs.com/package/arktype` (currently v2.2.3, verified 2026-09-13)
3. Confirm `arktype` is in `dependencies` in `package.json`
4. Confirm `package.json` has `"type": "module"` or the runtime supports ESM imports

### 2. Configure TypeScript

> Goal: set up `tsconfig.json` and the editor for ArkType syntax

1. Enable `strict: true` or `strictNullChecks: true` (required)
2. Enable `exactOptionalPropertyTypes: true` (recommended)
3. Enable `skipLibCheck: true` (strongly recommended)
4. Use TypeScript `>= 5.1`
5. Add VSCode settings in `.vscode/settings.json`:

```json
{
  "editor.quickSuggestions": { "strings": "on" },
  "typescript.preferences.autoImportSpecifierExcludeRegexes": [
    "^(node:)?os$"
  ]
}
```

6. See additional details in 

### 3. Define Schemas

> Goal: create schemas with native type syntax

1. Use `type()` from `arktype`
2. Define primitives such as `type("string")`, `type("number")`, `type("boolean")`
3. Define objects such as `type({ name: "string", "age?": "number" })`
4. Use optional fields with the `"field?"` syntax
5. Use unions and intersections with `"|"` and `"&"` or `.or()` and `.and()`
6. See additional details in 

### 4. Validate Data

> Goal: pick the right validation method

1. Call `Schema(data)` directly to get output or `ArkErrors`
2. Use `Schema.assert(data)` when you want a `TraversalError` thrown
3. Use `Schema.allows(data)` for a boolean type guard (does not apply morphs)
4. Check `instanceof type.errors` or `instanceof ArkErrors` for error handling
5. See additional details in 

### 5. Pattern Matching

> Goal: use `match()` for type-safe branching

1. Use `match()` from `arktype` for pattern matching
2. Define cases with the Case Record API (`match({ "string | Array": v => v.length, ... })`)
3. Use the Fluent API with `.case()` and `.default()` for non-string definitions
4. Use `.in<T>()` and `.at("key")` for narrowing and property matching
5. `default` values: `"assert"` (throw), `"reject"` (return ArkErrors), `"never"` (throw), or a handler function

### 6. Configure Validation

> Goal: customize validation behavior and error messages

1. Use `configure()` from `arktype/config` for global configuration
2. Define custom error messages with `.configure({ actual: () => "..." })` or `.describe(...)`
3. Use keyword configuration for built-in types (e.g. `numberAllowsNaN`, `jitless`)
4. See additional details in 

### 7. Type Inference And Scope

> Goal: use type inference and scopes for reusable types

1. Use `typeof Schema.t` or `typeof Schema.infer` for type inference
2. Use `scope()` from `arktype` for grouped type definitions that reference each other
3. Avoid unnecessary type assertions — rely on ArkType inference
4. See additional details in 

### 8. Performance And Integration

> Goal: use ArkType in performance-critical scenarios and integrate with frameworks

1. Use ArkType for performance-critical validation (benchmarks many times faster than Zod)
2. The runtime caches repeated validations — use it
3. Use Standard Schema integration (`~standard`) when needed — v2.2 embeds Standard Schema validators (Zod, Valibot, etc.) directly in definitions
4. Use `type.fn(args, ":", returnType)` for runtime-validated functions and `arkregex` (`type("x/^...$/")`) for type-safe regex with inferred capture groups
5. Use `@ark/json-schema` for bidirectional JSON Schema conversion (`toJsonSchema()` supports fallbacks and draft-07/2020-12)
6. See official resources in 

## Rules

### 1. Installation

- Use `bun add arktype` (runtime dependency) or the project's package manager
- Confirm `package.json` has `type: "module"` or the environment supports ESM

### 2. TypeScript Configuration

- Always enable `strict: true` or `strictNullChecks: true`
- Enable `exactOptionalPropertyTypes: true` and `skipLibCheck: true`
- Set VSCode `quickSuggestions.strings: on`

### 3. Schema Definitions

- Use `type()` for schema definitions
- Use `match()` for pattern matching
- Use double quotes or backticks for type expressions in examples
- Use code blocks for schema examples

### 4. Validation

- Use direct invocation `Schema(data)` for result or errors
- Use `.assert()` to throw
- Use `.allows()` for a boolean type guard

### 5. Type Safety

- Always use type inference from ArkType (`typeof Schema.t` or `typeof Schema.infer`)
- Avoid unnecessary type assertions

### 6. Performance

- Use ArkType for performance-critical validation
- Avoid redundant validations

### 7. Integration

- Use Standard Schema (`~standard`) when needed
- Use `/follow-lib-zod` if the project uses Zod as its primary validator
- Use `/deep-review-codebase` when a validation library still needs choosing/comparing
- Use /follow-lib-better-auth if needed
- Use /follow-lang-typescript if needed
- Use /follow-best-practice if needed
- Use /use-my-packages-on-registry if needed
- Use /setup-cicd if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Fast, accurate schema validation
- Type-safe code at both compile-time and runtime
- Maintainable, consistent code
- Optimized performance

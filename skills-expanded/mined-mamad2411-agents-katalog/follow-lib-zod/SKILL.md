---
name: follow-lib-zod
description: Use Zod v4 for TypeScript schema validation with static type inference
argument-hint: "[scope]"
related:
  - follow-lib-arktype
  - follow-lib-better-auth
  - follow-lang-typescript
  - follow-best-practice
  - use-my-packages-on-registry
  - setup-cicd

---

## Goal

Use Zod v4 to build schema validation that is type-safe at both compile-time and runtime with the current API

## Scope

Use with all kinds of TypeScript projects including frontend, backend, full-stack, and libraries that need runtime validation with static type inference

- Use this skill for the Zod v4 API (`z.object`, `.safeParse`, `z.infer`, `zod/mini`, `zod/v4` subpaths)
- Migrate v3 → v4 → workflow `workflows/migrate-zod-v4/SKILL.md`
- If the project uses ArkType or needs to compare schema libraries → `/follow-lib-arktype`; Zod v4 supports Standard Schema and works with form/validation libs

## Execute

### Workflows

| Topic | Workflow |
|-------|----------|
| Setup/install/version detect | `workflows/setup-zod/SKILL.md` — v3 vs v4 detect, install, tsconfig |
| Schema design | `workflows/define-schemas/SKILL.md` — objects/unions/refinements/transforms/`z.infer` |
| Boundary validation | `workflows/validate-data/SKILL.md` — `parse`/`safeParse`, API/env/file boundaries |
| Error handling | `workflows/handle-errors/SKILL.md` — `ZodError`, issues, `treeifyError`, custom messages, locales |
| Integration | `workflows/integrate-forms/SKILL.md` — Standard Schema, RHF/TanStack Form, JSON Schema/OpenAPI |
| Migrate v3→v4 | `workflows/migrate-zod-v4/SKILL.md` — breaking changes, import path, API renames | 
### 1. Install Zod

> Goal: install the latest Zod version

1. Run `bun add zod@latest` (or `pnpm add zod@latest` per the project's package manager)
2. Check the latest version at `https://www.npmjs.com/package/zod` (currently v4.6.4, verified 2026-09-13)
3. Confirm `package.json` has `zod` in `dependencies`
4. Use `import * as z from "zod"` for the classic API
5. For a smaller bundle, use `import * as z from "zod/mini"`

### 2. Enable Strict TypeScript Mode

> Goal: configure `tsconfig.json` to support strict mode for Zod type inference

1. Enable `strict: true` in `tsconfig.json`
2. Enable `noUncheckedIndexedAccess: true` for extra type safety (if the project allows)
3. Keep the other compiler options consistent with the project

### 3. Define Schemas

> Goal: create reusable schemas for primitive and complex types

1. Use factory functions from the `z` namespace (`z.string()`, `z.number()`, `z.boolean()`)
2. Define schemas for complex structures (`z.object({})`, `z.array()`, `z.union()`, `z.intersection()`)
3. Use `z.coerce` for type coercion, knowing the input type is `unknown` unless a generic is given
4. Use `z.custom()` or `.refine()` for custom validation
5. Structure schemas to be reusable by domain or feature

### 4. Validate Data

> Goal: pick the validation method fitting the use case

1. Use `.parse()` for validation that should throw `ZodError`
2. Use `.safeParse()` for validation that should return a result object
3. Use `.parseAsync()` or `.safeParseAsync()` for async validation
4. Note that the `safeParse()` error in Zod 4 no longer extends `Error` — check via `result.success`

### 5. Handle Errors

> Goal: handle validation errors clearly and user-friendly

1. Use `try-catch` with `.parse()`
2. Check `error instanceof z.ZodError`
3. Access `error.issues` for error details (`.errors` was removed in v4)
4. Use the `error` parameter in schemas instead of the deprecated `message`
5. Use `z.config({ customError: ... })` or `z.config(z.locales.en())` for global error messages
6. Use `z.treeifyError()` instead of the deprecated `.format()` or `.flatten()`

### 6. TypeScript Integration

> Goal: keep type safety at both runtime and compile-time

1. Use `z.infer<typeof schema>` for type inference
2. Use `z.input<typeof schema>` for the input type
3. Use `z.output<typeof schema>` for the output type
4. Watch out for internal APIs (`._zod`, `ZodEffects` removed) — prefer the public API
5. Keep type safety at both runtime and compile-time

### 7. Schema Composition

> Goal: compose schemas to stay maintainable and cut TypeScript compilation time

1. Use spread syntax or `A.extend(B.shape)` instead of the deprecated `.merge()`
2. Use `.safeExtend()` when extending schemas that have refinements
3. Use `.pick()` and `.omit()` for partial schemas
4. Use `.partial()` for optional fields
5. Use `.required()` for required fields
6. Use `z.strictObject()` or `z.looseObject()` instead of the deprecated `.strict()` and `.passthrough()`
7. Organize schemas by domain or feature

### 8. Advanced Patterns

> Goal: use advanced validation and transformation patterns for special cases

1. Use `.refine()` for custom validation logic with the `error` option
2. Use `.transform()` for data transformation after validation
3. Use `.pipe()` for chaining transformations
4. Use `.preprocess()` for data normalization before validation
5. Use `z.discriminatedUnion()` or `z.union()` for tagged unions
6. Use `.brand()` for branded types
7. Use `.readonly()` for immutable data
8. Use `.default()` for default values (output side)
9. Use `.prefault()` for prefault values (input side)
10. Use top-level string formats like `z.email()`, `z.uuid()`, `z.iso.date()` instead of the deprecated `z.string().email()`
11. Consider `z.core` or `z.compile()` for AOT compilation when needed

## Rules

### 1. TypeScript Configuration

- Always enable `strict: true` in `tsconfig.json`
- Enable `noUncheckedIndexedAccess: true` for extra type safety

### 2. Validation Methods

- Use `.safeParse()` for user input validation and performance-sensitive code
- Use `.parse()` for critical validation that should throw
- Use `.parseAsync()` or `.safeParseAsync()` for async schemas

### 3. Error Handling

- Custom error messages should be clear and in language the user understands
- Use the `error` parameter instead of the deprecated `message` or `errorMap`
- Use `z.config()` for global error messages

### 4. Schema Design

- Schemas should be reusable and maintainable
- Organize schemas by domain or feature
- Use type inference instead of manual type definitions
- Use `z.coerce` when type conversion is needed

### 5. Schema Composition

- Use spread syntax or `A.extend(B.shape)` instead of the deprecated `.merge()`
- Use `.safeExtend()` for schemas with refinements

### 6. Advanced Patterns

- Use `.preprocess()` for data normalization before validation
- Use `.transform()` for data transformation after validation
- Use `z.lazy()` for recursive schemas with an explicit type hint

### 7. Performance

- Consider `zod/mini` for bundle size constraints
- Use `z.compile()` when AOT compilation is desired

### 8. Testing

- Test schemas comprehensively across valid, invalid, and edge cases
- Use `.safeParse()` in tests

### 9. Cross-Skill References

- Use `/follow-lib-arktype` if needed
- Use `/follow-lib-better-auth` if needed
- Use `/follow-lang-typescript` if needed
- Use `/follow-best-practice` if needed
- Use `/use-my-packages-on-registry` if needed
- Use `/setup-cicd` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Zod installed and configured correctly
- Well-structured, reusable schemas
- Type-safe validation logic
- Clear, user-friendly error handling
- Types synchronized with runtime validation
- Test coverage for the validation logic
- A maintainable and scalable codebase

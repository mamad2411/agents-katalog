---
name: follow-tool-data-validation
description: Use a validator in the project for data, forms, API payloads, and schemas
argument-hint: "[scope]"
related:
  - follow-tool-linter
  - follow-lib-zod
  - update-tests
  - run-test
---

## Goal

Use a validator in the project to check data, forms, API payloads, and schemas in a type-safe, consistent way

## Scope

Use for projects that must validate both external input (API, forms, CLI args) and internal input (function arguments, config) — supports TypeScript, Rust, Python, Go

- Boundary: this skill covers runtime/schema validation only — code style/syntax uses `/follow-tool-linter`; the zod deep-dive uses `/follow-lib-zod`

## Execute

### 1. Select Validator

> Goal: pick the validator per tech stack

1. Check the project's tech stack
2. Choose a validator as appropriate:
   - TypeScript/JavaScript: zod (`^4.x` — latest `4.6.4`, verified 2026-09-13), valibot, arktype, yup, joi, class-validator
   - Rust: validator crate, garde, serde_json schema
   - Python: pydantic, marshmallow, cerberus
   - Go: go-playground/validator, govalidator
3. If existing schemas are present → keep using them; if not → pick the ecosystem-recommended one

### 2. Define Schemas

> Goal: define validation schemas for every input

1. Create a schema per domain model / DTO / form
2. Use type inference from the validator when available (e.g. `z.infer<typeof Schema>`)
3. Define custom error messages that read well (zod 4 uses the `error` param instead of `message`/`invalid_type_error`)
4. Split schema files by domain/feature — do not put everything in one file
5. If a schema is reused often → create a shared schema and compose

### 3. Validate In Code

> Goal: call the validator at the right points

1. Validate at the boundary: API handler, controller, CLI input, form submit
2. Do not re-validate inside business logic
3. Convert validation errors into domain errors the caller understands
4. Use `parse`/`safeParse` or the library's equivalent
5. On validation failure → throw or return a structured error naming the field

### 4. Handle Errors

> Goal: handle validation errors consistently

1. Create a standard error format: `{ field, message, code }`
2. Use the library's `flatten` or `formatError` when available
3. For an API → return 400 with field-level errors
4. For a CLI → show a readable message and exit non-zero
5. For a form → bind the error back to the field

### 5. Test Validation

> Goal: test the schemas and error cases

1. Run `/update-tests` for the happy path, invalid types, missing fields, and edge cases
2. Test the custom error messages
3. Test schema composition/refinement
4. Run `/run-test` to verify

## Rules

### 1. Type Safety

- Use type inference from the validator whenever possible
- Never use `any` for validated data
- Separate domain types from schema types when needed

### 2. Single Source Of Truth

- Never duplicate schema logic in several places
- Use schema composition instead of copy-paste
- Shared schemas live in `shared/schemas/` or `domain/schemas/`

### 3. Error Clarity

- An error message must state the field, the expected value, and the actual value when available
- Use error codes so callers can handle them
- Do not expose internal details that may change

### 4. No Validation In Business Logic

- Business logic receives already-validated input
- If business logic must validate → the rule should move to the schema layer
- Never use manual `if (!x) throw` in place of schema validation

- Use /follow-tool-linter if needed
- Use /follow-lib-zod if needed
- Use /update-tests if needed
- Use /run-test if needed

## References

- [CLI reference](references/cli.md)


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The validator selected and installed correctly for the tech stack
- Schemas cover every boundary input
- Validation errors are consistent and readable
- Tests cover the happy path and invalid cases
- Business logic carries no redundant validation


# Gemini CLI TypeScript Rules

## Role
- You are a Gemini CLI coding agent operating in TypeScript repositories.
- Optimize for strict typing, safe refactors, and clear module boundaries.

## Type Safety
- Enforce strict TypeScript compiler settings.
- Never introduce `any`.
- Prefer `unknown` plus explicit narrowing for external data.
- Annotate exported function return types.
- Prefer discriminated unions over stringly typed state.

## Module Conventions
- Prefer named exports in all source modules.
- Avoid default exports unless framework-required.
- Keep files cohesive and focused.
- Avoid oversized barrel files.
- Use explicit imports from concrete paths.

## Error Handling
- Throw `Error` subclasses for domain and app failures.
- Include stable error codes for machine handling.
- Normalize unknown errors at I/O boundaries.
- Avoid swallowing exceptions silently.
- Return user-safe messages from CLI/API edges.

## Testing
- Use `vitest` for unit and integration tests.
- `*.test.ts` for unit tests.
- `*.integration.test.ts` for integration tests.
- Cover happy path, invalid input, and failure states.
- Mock network, filesystem, and external services only.

## Code Style
- Use 2-space indentation and semicolons.
- Prefer single quotes.
- Keep functions short and predictable.
- Favor early returns over nested branches.
- Avoid hidden mutation across module boundaries.

## Async Patterns
- Prefer `async`/`await`.
- Add timeout and cancellation handling for network operations.
- Surface retryable errors with clear classification.
- Keep side effects isolated from pure business logic.

## Completion Criteria
- Strict typecheck passes.
- Vitest suite passes for changed behavior.
- New code follows named export convention.
- Error handling is explicit and tested.
- Style rules are consistent across touched files.

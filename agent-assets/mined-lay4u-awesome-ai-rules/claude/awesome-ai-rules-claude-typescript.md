# TypeScript Project Rules

## Scope
- Applies to all TypeScript packages and services in this repository.
- Prioritize maintainability, explicit typing, and predictable runtime behavior.

## Compiler Baseline
- TypeScript must run in strict mode for every project.
- Required `tsconfig` options:
  - `"strict": true`
  - `"noImplicitOverride": true`
  - `"noUncheckedIndexedAccess": true`
  - `"exactOptionalPropertyTypes": true`
  - `"noFallthroughCasesInSwitch": true`
  - `"useUnknownInCatchVariables": true`
- `skipLibCheck` may be `true` only to speed CI, never to hide app type errors.

## Module and Export Conventions
- Prefer named exports in all modules.
- Default exports are disallowed except framework-required entry files.
- Barrel files (`index.ts` that re-export many modules) are discouraged.
- Import directly from concrete module paths to keep dependency boundaries clear.

## File and Naming Conventions
- Use `kebab-case` for filenames: `user-service.ts`.
- Use `PascalCase` for classes and types/interfaces.
- Use `camelCase` for functions, variables, and object keys.
- One primary responsibility per file.

## Error Handling
- Do not throw raw strings or generic `Error` for domain failures.
- Use custom error classes with stable `code` fields.
- Custom errors must:
  - extend `Error`
  - set `name`
  - include contextual metadata where helpful
- Convert unknown errors at boundaries (HTTP handlers, queues, CLI entrypoints).

## Testing Standards
- Test runner: Vitest only.
- Use `describe` and `it` blocks; keep test names behavior-focused.
- File naming:
  - unit: `*.test.ts`
  - integration: `*.integration.test.ts`
- Co-locate tests with source or place under `tests/` with mirrored structure.
- Mock external I/O only; keep core business logic tests real and deterministic.

## Build and Runtime
- Development runtime must use `tsx` (`tsx watch src/index.ts`).
- Production builds must use `tsc` to emit JavaScript.
- Do not use `ts-node` in production or CI build pipelines.
- CI should run: typecheck, test, lint, then build.

## Code Style
- Indentation: 2 spaces.
- Strings: single quotes.
- Semicolons: required.
- Keep functions small and side effects explicit.
- Prefer early returns over nested conditionals.

## Dependency and API Design
- Prefer small utility modules over large shared helpers.
- Keep public APIs explicit; avoid exposing internal types by accident.
- Avoid circular dependencies; refactor shared logic into dedicated modules.

## Definition of Done
- `pnpm typecheck` (or equivalent) passes with strict mode enabled.
- Vitest suite passes for changed behavior.
- New or changed error paths include custom error handling.
- Exports follow named-export rule and avoid new barrels.

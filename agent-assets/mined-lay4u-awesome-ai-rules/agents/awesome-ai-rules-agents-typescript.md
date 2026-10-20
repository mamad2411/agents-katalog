# Codex TypeScript Rules

## Role
- You are an OpenAI Codex coding agent for strict TypeScript projects.
- Optimize for correctness, maintainability, and low-surprise behavior.

## Type System
- TypeScript must run with `strict: true` in every package.
- Never use `any`, including implicit `any`.
- Use `unknown` for external input, then narrow with guards.
- Prefer explicit return types on exported functions.
- Use discriminated unions for variant domain states.
- Avoid non-null assertions (`!`) unless a prior check guarantees safety.

## Exports and Modules
- Prefer named exports for all modules.
- Avoid default exports unless framework conventions require them.
- Keep modules focused; one primary responsibility per file.
- Avoid broad barrel exports that hide dependency boundaries.
- Import from concrete module paths.

## Error Handling
- Do not throw strings.
- Throw `Error` subclasses with stable `code` fields.
- Include contextual metadata in custom error constructors.
- At boundaries, map internal exceptions to user-safe errors.
- In `catch` blocks, treat caught values as `unknown` and narrow safely.
- Log structured context before rethrowing or returning failures.

## Testing
- Use `vitest` for all tests.
- Unit tests use `*.test.ts` naming.
- Integration tests use `*.integration.test.ts` naming.
- Write behavior-focused test names.
- Mock external I/O only; keep domain logic tests real.
- Cover success, failure, and edge conditions for changed code.

## Code Style
- Use 2-space indentation.
- End statements with semicolons.
- Prefer single quotes unless escaping is noisy.
- Favor early returns over deep nesting.
- Keep functions short and side effects explicit.
- Avoid boolean flag arguments; prefer explicit options objects.

## Async and APIs
- Use `async`/`await` over raw promise chains.
- Validate API inputs at the boundary, not deep in services.
- Keep DTO types separate from internal domain models.
- Do not leak infrastructure errors through public APIs.

## Definition of Done
- `tsc --noEmit` passes with strict settings.
- `vitest` passes for affected areas.
- No `any` introduced.
- New exports are named exports unless justified.
- Error paths are typed, tested, and user-safe.

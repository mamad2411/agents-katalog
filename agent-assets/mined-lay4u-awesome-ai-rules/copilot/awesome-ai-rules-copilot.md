# GitHub Copilot Instructions: Go

## Inline Completion Priorities
- Suggest idiomatic Go first, clever abstractions second.
- Default to explicit error checks with immediate returns.
- Prefer readable control flow over compressed one-liners.
- Keep generated snippets aligned with existing package style.

## Go API Conventions
- Package names: short, lowercase, no underscores.
- Export only what callers need; keep helpers unexported.
- Favor composition via struct fields over inheritance-style hierarchies.
- Avoid `init()` unless a framework requires automatic registration.

## Interfaces
- Prefer small interfaces focused on behavior.
- Accept interfaces in inputs where mocking/substitution is needed.
- Return concrete structs from constructors and factories.
- Avoid generating broad "god interfaces".

## Error Patterns
- Use `if err != nil { return ... }` consistently.
- Wrap with `fmt.Errorf("context: %w", err)` when propagating.
- Use `errors.Is` / `errors.As` for branching logic.
- Do not ignore returned errors from I/O, close, or encode/decode calls.

## Concurrency
- Include `context.Context` as first argument for cancellable work.
- Suggest goroutines only with clear synchronization (`WaitGroup`, channels, `errgroup`).
- Avoid channel misuse: sender closes, receiver ranges.
- Prefer race-safe patterns and recommend `go test -race` when relevant.

## Testing
- Generate table-driven tests for function matrices.
- Use subtests for each table row with descriptive names.
- Prefer `testify/require` for setup-critical assertions.
- Keep fixtures lightweight and deterministic.

## Tooling Awareness
- Assume `gofmt`/`goimports` will run; produce format-stable code.
- Keep code compatible with `golangci-lint` defaults.
- Favor stdlib dependencies unless a third-party package is clearly justified.
- Keep module imports tidy and consistent with `go.mod`.

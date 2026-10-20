# Cursor Go Rules

## IDE-First Defaults
- Always format on save with `gofmt` (or `goimports` when available).
- Never accept code that is unformatted; formatting is non-negotiable.
- Organize imports automatically; avoid manual import micromanagement.
- Keep editor diagnostics on for `go vet` and `golangci-lint`.

## Go Code Style
- Prefer small packages with focused responsibilities.
- Package names must be short, lowercase, and without underscores.
- Prefer composition over inheritance-style embedding chains.
- Avoid `init()`; use explicit constructors and setup functions.
- Keep exported APIs minimal and stable.

## Error Handling
- Use explicit error returns; Go has no exceptions for normal control flow.
- Return early on errors and keep happy-path unindented.
- Wrap errors with `%w` when adding context.
- Compare with `errors.Is`/`errors.As` instead of string matching.
- Do not swallow errors; either handle, wrap, or return them.

## Interfaces and API Design
- Prefer small interfaces (1-3 methods) near the consuming package.
- Accept interfaces in function parameters when behavior is needed.
- Return concrete structs from constructors for better discoverability.
- Avoid exporting interfaces prematurely.

## Concurrency and Context
- Pass `context.Context` as the first parameter for request-scoped work.
- Never store `context.Context` inside structs.
- Use goroutines only with a clear lifecycle and cancellation path.
- Prefer channels for coordination, not as a replacement for all state.
- Close channels only from the sender side.
- Guard shared mutable state with `sync.Mutex`/`sync.RWMutex`.

## Testing in the Editor Loop
- Use table-driven tests for branch-heavy logic.
- Run `go test ./...` before finalizing changes.
- Use `testify/require` for must-stop assertions and `assert` for continued checks.
- Keep tests deterministic; avoid sleeps when synchronization primitives are possible.
- Add race checks (`go test -race ./...`) when touching concurrency.

## Modules and Dependencies
- Use Go modules and keep `go.mod`/`go.sum` in sync.
- Prefer standard library packages before adding new dependencies.
- Add dependencies deliberately; remove unused ones promptly.

# Gemini CLI Go Rules

## CLI-First Workflow
- Operate from terminal with reproducible command sequences.
- Prefer explicit command output over assumptions.
- Keep a tight loop: edit -> format -> build -> test -> lint.

## Standard Command Set
- `goimports -w .` (or `gofmt -w` when goimports is unavailable)
- `go build ./...`
- `go test ./...`
- `go vet ./...`
- `golangci-lint run`
- `go test -race ./...` for concurrency-sensitive changes.

## Go Code Conventions
- Package names: lowercase, short, no underscores.
- Prefer composition via structs and injected collaborators.
- Avoid inheritance-style deep embedding trees.
- Avoid `init()` unless required for unavoidable registration behavior.

## Error Handling
- Handle every returned `error` explicitly.
- Keep error paths clear with early returns.
- Wrap propagated errors using `%w`.
- Use `errors.Is` and `errors.As` for robust error checks.
- Use panic only for unrecoverable programmer/setup faults.

## Interfaces and Boundaries
- Keep interfaces narrow and purpose-built.
- Accept interfaces at boundaries where substitution is needed.
- Return concrete structs from constructors.
- Place interfaces in consuming packages to avoid leakage.

## Concurrency
- Pass `context.Context` first for cancellable operations.
- Use goroutines with explicit ownership and shutdown.
- Prefer `errgroup` for coordinated concurrent work.
- Use channels for signaling/work distribution with clear close semantics.

## Testing
- Use table-driven tests for behavior matrices.
- Use subtests for readable case output.
- Use `testify` when assertions become noisy.
- Ensure tests are deterministic and CI-friendly.

## Modules and Dependencies
- Manage dependencies via `go.mod`/`go.sum` only.
- Prefer standard library before adding third-party modules.
- Keep dependency graph lean and intentional.
- Re-run full command set after dependency updates.

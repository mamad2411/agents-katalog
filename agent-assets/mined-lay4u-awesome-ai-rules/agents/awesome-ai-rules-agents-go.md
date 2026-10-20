# Codex Go Rules

## Mission
- Deliver production-safe Go changes with autonomous verification.

## Execution Protocol
- Before edits: inspect module layout and existing lint/test commands.
- During edits: keep diffs small and behavior-focused.
- After edits: run required verification commands and report concrete results.

## Required Verification Commands
- `go fmt ./...` or `gofmt`/`goimports` on changed files.
- `go build ./...`
- `go test ./...`
- `go vet ./...`
- `golangci-lint run`
- `go test -race ./...` when concurrency paths are touched.

## Go Design Rules
- Use short, lowercase, underscore-free package names.
- Prefer composition over inheritance-style architecture.
- Keep constructors explicit (`NewX(...)`) and dependency-injected.
- Do not introduce `init()` except for unavoidable registration side effects.

## Error Handling
- Go uses explicit error returns: check and propagate every error.
- Return early on failure to keep control flow shallow.
- Wrap with `%w` to preserve error chains.
- Use `errors.Is`/`errors.As` for semantic matching.
- Never ignore cleanup errors (`Close`, `Flush`, `Sync`) without intent.

## Interfaces
- Define minimal interfaces where consumed.
- Accept interfaces when callers need substitution.
- Return structs for richer capabilities and easier evolution.
- Avoid exporting interfaces without multiple real implementations.

## Concurrency and Context
- Pass `context.Context` as first argument to cancellable operations.
- Never store context in structs.
- For fan-out tasks, prefer `errgroup.WithContext`.
- Ensure every goroutine has a bounded lifecycle and cancellation path.
- Use channels deliberately; close only by senders.

## Testing Standards
- Prefer table-driven tests with descriptive case names.
- Use `t.Run` subtests for scenario isolation.
- Use `testify` (`require`/`assert`) where it improves clarity.
- Keep tests deterministic and avoid timing flakiness.

## Module and Dependency Management
- Keep `go.mod` authoritative and `go.sum` synchronized.
- Prefer stdlib before external dependencies.
- Pin/upgrade dependencies intentionally and verify downstream impact.
- Remove unused dependencies and dead abstractions.

## Completion Criteria
- All required commands pass on touched scope.
- Formatting and lint are clean.
- New behavior has tests (including error paths).

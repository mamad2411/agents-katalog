# Go Rules for Claude Code

## Terminal Workflow
- Use the shell loop: edit -> `go build` -> `go test` -> `go vet`.
- Run commands from module root unless the repo defines another entrypoint.
- Keep changes small enough to validate quickly from terminal feedback.

## Required Verification Commands
- `go build ./...`
- `go test ./...`
- `go vet ./...`
- `golangci-lint run`
- `go test -race ./...` when concurrency code changed.

## Formatting and Imports
- `gofmt`/`goimports` is mandatory; do not hand-format.
- Reject diffs containing formatting drift.
- Keep imports grouped and unused imports removed.

## Project and Module Hygiene
- Use one module per deployable boundary unless explicitly multi-module.
- Keep `go.mod` minimal and intentional.
- Commit `go.sum` updates with dependency changes.
- Avoid hidden toolchain assumptions; pin Go version in `go.mod`.

## Error Handling
- Return `error` explicitly; never emulate exceptions with panic.
- Reserve `panic` for unrecoverable programmer errors at startup boundaries.
- Wrap lower-level failures with `%w` and actionable context.
- Use sentinel errors sparingly; prefer typed errors when callers branch on behavior.

## Interface Design
- Keep interfaces small and behavior-oriented.
- Accept interfaces, return structs.
- Define interfaces where consumed, not where implemented.
- Do not add interfaces "just in case".

## Concurrency Discipline
- Thread `context.Context` through I/O and goroutine boundaries.
- Always define goroutine shutdown behavior.
- Prefer `errgroup` for fan-out/fan-in with cancellation.
- Use buffered channels only when capacity is justified.

## Testing Standards
- Prefer table-driven tests for permutations.
- Use subtests (`t.Run`) with clear case names.
- Use `testify` to improve assertion readability where useful.
- Keep integration tests explicit about external requirements.

## Construction and Initialization
- Avoid `init()` unless required for runtime registration hooks.
- Prefer explicit constructors like `NewService(...)`.
- Inject dependencies through constructors to keep tests isolated.
- Prefer composition over inheritance-like patterns.

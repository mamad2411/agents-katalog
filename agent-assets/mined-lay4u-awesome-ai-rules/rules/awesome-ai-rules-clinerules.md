# Cline Go Rules

## Role
- You are Cline, a Go coding assistant embedded in VS Code.
- Optimize for readability, idiomatic Go patterns, and operational reliability.
- Prefer incremental refactors with compile/test checks between steps.

## Coding Standards
- Follow effective Go naming and package conventions.
- Keep interfaces small and defined by consumers, not producers.
- Return errors as values; avoid panics outside truly unrecoverable states.
- Wrap errors with context using `%w` and preserve root cause.
- Prefer composition over inheritance-like patterns.
- Keep functions short and avoid deep nesting.
- Use `context.Context` for request-scoped cancellation and deadlines.
- Avoid shared mutable state; protect with synchronization when required.
- Run `gofmt` and `go vet` for all changed Go files.

## File Structure
- Recommended layout: `cmd/`, `internal/`, `pkg/`, `api/`, `testdata/`.
- Place executables in `cmd/<app>/main.go`.
- Keep non-public internals in `internal/`.
- Use `pkg/` only for stable reusable libraries.
- Co-locate tests with source as `*_test.go`.

## Testing Requirements
- Use table-driven tests for input/output-heavy logic.
- Add subtests with clear case names.
- Test files must cover success, failure, and edge conditions.
- Prefer integration tests for DB/network workflows behind build tags if needed.
- Keep unit tests fast; avoid live external dependencies.
- Run `go test ./...` after any behavior change.

## Cline IDE Workflow
- Read package neighbors before editing to keep API boundaries consistent.
- Use small inline edits and keep imports tidy.
- Run `go test`, `go vet`, and `golangci-lint` (if configured) in terminal tasks.
- Let Cline scaffold tests, then tighten assertions manually.
- Use command execution to validate generated mocks and codegen outputs.
- Use MCP integrations to inspect API specs and generate typed clients safely.
- Summarize package-level impact and migration notes when signatures change.

## Done Criteria
- `gofmt` applied and no lint/vet regressions.
- `go test ./...` passes for affected packages.
- Error handling includes useful context.
- Public APIs remain minimal and documented by usage.


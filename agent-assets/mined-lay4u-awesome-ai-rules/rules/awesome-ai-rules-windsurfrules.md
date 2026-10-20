# Windsurf Go Rules

## Flow-State Development
- Keep edits incremental and compile after each logical chunk.
- Prefer fast feedback loops over large speculative rewrites.
- When uncertain, add a small test first, then implement.

## Non-Negotiables
- Always run `gofmt`/`goimports` before considering work complete.
- Maintain `golangci-lint` cleanliness on touched code.
- Avoid `init()` unless absolutely required by external registration patterns.

## Idiomatic Go Design
- Package names should be lowercase, concise, and underscore-free.
- Keep packages cohesive; split by responsibility, not by technical layer alone.
- Prefer composition: embed or inject collaborators instead of inheritance mimicry.
- Keep public APIs small and intention-revealing.

## Error Handling
- Return explicit errors and check them immediately.
- Add context during propagation with `%w` wrapping.
- Avoid panic-based control flow.
- Model expected domain failures with typed or sentinel errors where necessary.

## Interfaces and Boundaries
- Define tiny interfaces at call sites.
- Accept interfaces where behavior varies.
- Return structs so concrete capabilities remain visible.
- Delay interface extraction until there is at least one real alternate implementation.

## Concurrency
- Use `context.Context` for cancellation/timeouts in I/O paths.
- Launch goroutines only when ownership and shutdown are defined.
- Prefer `errgroup.WithContext` for coordinated worker sets.
- Use channels for ownership transfer/signaling, not hidden shared-state mutation.

## Testing Loop
- Use `go test ./...` frequently during edits.
- Write table-driven tests for branch-heavy functions.
- Use `testify` where assertion clarity improves signal.
- Run `go test -race ./...` after concurrency changes.

## Module and Dependency Hygiene
- Keep `go.mod`/`go.sum` committed and current.
- Prefer standard library solutions first.
- Add third-party dependencies only with clear payoff.
- Remove stale dependencies promptly.

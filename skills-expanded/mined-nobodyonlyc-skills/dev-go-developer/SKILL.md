---
name: dev-go-developer
description: Guides the agent in writing idiomatic, production-quality Go code — concurrency, interfaces, error handling, testing, and module layout.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **Senior Go Engineer**. Adopt their exact mindset, priorities, and vocabulary. Do NOT spawn a subagent for this.

Develop Go feature for: $ARGUMENTS

Follow these guidelines to design, implement, and verify Go code at a production level.

> **Apply the shared [engineering principles](../../resources/engineering-principles.md) throughout:** trace code to the requirement (§1), set the architecture/boundary before coding (§2), choose design patterns deliberately (§3), design for extension (§4), keep it clean (§5).

## Step 1: Module & Package Design
Before writing code, establish the module shape:
1. **Package layout**: Group by domain concern, not by type. Prefer `internal/` for unexported packages. Keep `main` packages thin.
2. **Dependency direction**: Domain packages must NOT import infrastructure packages. Use interfaces at the boundary.
3. **Naming**: Follow the Go convention file — snake_case files, lowercase single-word packages, `er`-suffix interfaces.
4. Read [`go.md`](../../resources/conventions/go.md) before writing a single line.
5. **Package graph (MANDATORY — confirm before coding)**: Output a package diagram and present it via ask-user. Do NOT write implementation code until the user approves.
   ```
   cmd/server          ← main (thin, wires everything)
     internal/order
       handler.go      ← HTTP adapter (imports domain interface)
       service.go      ← domain logic (no infra imports)
       repo.go         ← implements Storer interface
     internal/payment
       client.go       ← external adapter (new)
     pkg/db
       postgres.go     ← shared DB pool (reuse existing)
   ```
   Show import direction with `→`. Flag any proposed import that violates the domain→infra boundary as `⚠ boundary violation`.

## Step 2: Idiomatic Go Patterns
Write Go the Go way — do not import patterns from other languages:

- **Interfaces**: Keep them small (1–3 methods). Accept interfaces, return structs. Define interfaces where they are used (consumer side), not where types are defined.
- **Error handling**: Return `error` explicitly; never swallow errors. Wrap with context using `fmt.Errorf("doing X: %w", err)`. Use `errors.Is` / `errors.As` for checks.
- **Zero values**: Design structs so the zero value is useful. Avoid constructors unless invariants require them.
- **Embedding over inheritance**: Compose behavior via struct embedding and interface promotion.
- **Named return values**: Use only when the function is long and the names add clarity. Never as a shortcut for early `return`.

## Step 3: Concurrency
Go concurrency must be intentional and documented:
1. **Goroutines**: Never leak a goroutine. Every goroutine must have a clear exit path (context cancellation, done channel, or WaitGroup).
2. **Channels vs Mutexes**: Use channels to communicate ownership; use `sync.Mutex` to protect shared state accessed from multiple goroutines. Do not mix the two for the same data.
3. **Context propagation**: Every function that does I/O or can block MUST accept `context.Context` as the first argument. Respect cancellation.
4. **Race detector**: Run `go test -race ./...` before marking any concurrent code as done.
5. **sync primitives**: Prefer `sync.WaitGroup`, `sync.Once`, `sync.Pool` over ad-hoc solutions.

## Step 4: Error Handling & Sentinel Errors
1. **Sentinel errors**: Define at the package level for expected failure modes that callers need to distinguish (`var ErrNotFound = errors.New("not found")`).
2. **Custom error types**: Use only when structured metadata (HTTP status, code, field) is needed.
3. **Panic**: Never use `panic` for normal error paths. Reserve for programmer errors (impossible state) and recover only at top-level HTTP/server boundaries.
4. **Logging**: Log errors at the point of handling, not at every propagation level (avoids duplicate log lines).

## Step 5: Testing
Go testing is first-class — follow the standard toolchain:
1. **Table-driven tests**: Default pattern for functions with multiple input/output cases.
2. **Subtests**: Use `t.Run("name", ...)` to group and isolate cases; name them clearly.
3. **Test files**: `*_test.go` in the same package (white-box) or `package foo_test` (black-box, tests the public API).
4. **Mocking**: Use interfaces to inject test doubles. Prefer hand-rolled fakes over mocking frameworks for clarity.
5. **Coverage**: Run `go test -cover ./...`. Aim for >80% on business-logic packages.
6. **Benchmarks**: Add `Benchmark*` functions when performance is a stated requirement.

## Step 6: Performance Guardrails
- Avoid unnecessary allocations in hot paths — reuse buffers with `sync.Pool`, preallocate slices with `make([]T, 0, cap)`.
- Profile before optimizing: `pprof` over intuition.
- Use `strings.Builder` for string concatenation in loops; never `+=` inside a loop.
- Avoid reflection in production code paths; use generics (Go 1.18+) where type parameterization is needed.

## Step 7: Verification (Definition of Done)
Code is NOT done until:
1. `go build ./...` — no compile errors.
2. `go vet ./...` — no vet warnings.
3. `golangci-lint run` (if configured) — no lint errors.
4. `go test -race ./...` — all tests pass, no race conditions.
5. All acceptance criteria from the US are covered by a test.
6. New packages have a `README.md` or `doc.go` per the Go convention.

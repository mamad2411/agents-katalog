---
name: go-patterns
description: Go stack conventions agentic-forge applies when the detected stack is Go — the toolchain (go test -race / go vet / gofmt / golangci-lint), error-handling and concurrency idioms, testing discipline, layout, and the high-value Go pitfalls. Loaded on demand by develop / code-review and the software-engineer / qa-engineer roles after stack detection; kept off the always-on listing.
disable-model-invocation: true
---

# Go patterns

The Go stack pack: loaded by the `software-engineer` / `qa-engineer` roles (and the
`code-review` lint aspect) when `stacks.detect` reports Go. It carries only what is
**Go-specific** on top of [`engineering-standards`](../engineering-standards/SKILL.md) — Claude
already knows general Go; this encodes the conventions and gates agentic-forge holds Go work to.
(Mechanism: ADR 0015, by-stack detection + reference packs.)

## Toolchain

**Prefer the repo's own commands** — read the `Makefile` / CI workflow and run *those*; Go's
toolchain is otherwise standard. Defaults (the same commands `stack-detect` reports as fallbacks):

| Job | Conventional command | Gate |
| --- | --- | --- |
| test | `go test -race ./...` | green; new behaviour covered; race-clean |
| build/types | `go build ./...` | compiles (the compiler is the type check) |
| vet | `go vet ./...` (the profile's lint when no golangci config exists) | clean |
| lint | `golangci-lint run` when `.golangci.{yml,yaml,toml,json}` sits beside `go.mod` | clean (no new `//nolint`) |
| format | `gofmt -w .` (or `goimports -w .`) | applied (canonical; non-negotiable) |

Run `go vet` and the formatter on the change before declaring done; keep `go.mod`/`go.sum` tidy
(`go mod tidy`). Never silence a checker to pass — fix the cause.

## Idioms

- **Errors are values.** Return `error` as the last result; wrap with
  `fmt.Errorf("doing x: %w", err)`; branch with `errors.Is` / `errors.As`. Don't `panic` for
  ordinary failures, and don't discard errors (`_ =`).
- **Accept interfaces, return concrete types**; keep interfaces small and defined at the
  consumer. Zero values should be useful; prefer composition (embedding) over inheritance.
- **`defer`** for cleanup (close/unlock); **`context.Context` as the first parameter** for
  cancellation/deadlines; propagate it, don't store it.
- Concurrency: goroutines + channels or `sync`; ensure every goroutine can exit (no leaks);
  exported identifiers get a doc comment starting with the name.

## Testing

- Standard `testing` package, **table-driven tests with `t.Run` subtests** (the Go idiom).
  Cover the happy path plus a boundary and an error case. Use `t.Helper()`, `t.TempDir()`.
- **`go test -race ./...`** for anything concurrent. Tests must be deterministic — no real
  network/clock; don't depend on map iteration order. Never weaken or delete a test to go green.
- **A goroutine a test starts must stop before the test ends.** Cancel its context and wait for
  it (a done channel, or `errgroup.Wait`) in a `t.Cleanup` registered **after** `t.TempDir()`:
  cleanups run last-in-first-out, so the goroutine stops before the directory it writes into is
  removed. Bound the wait with a timeout (`select` on the done channel and `time.After`, then
  `t.Error`) so a hung goroutine fails that test instead of hanging the suite. `-race` does not
  catch this: the symptom is a flaky `TempDir RemoveAll cleanup: ... directory not empty`.

## Pitfalls (Go-specific, high-value)

- **Unchecked errors** and ignored returns; **nil interface vs nil pointer** (a non-nil
  interface holding a nil pointer is `!= nil`).
- **Goroutine leaks**; **send on a closed channel** (panics); data races (catch with `-race`).
- **`defer` inside a loop** (resources pile up until the function returns — scope to a helper).
- **Loop-variable capture** in closures/goroutines — Go 1.22+ scopes it per iteration, but be
  explicit when targeting older Go or for clarity.
- **Unchecked type assertions** (use `v, ok := x.(T)`); slice aliasing via `append`; relying on
  random **map iteration order**.

## Definition of done (Go)

`go build ./...` and `go vet ./...` clean (plus `golangci-lint` if configured), `gofmt` applied,
`go test -race ./...` green with table-driven boundary/error cases, errors wrapped not swallowed,
exported symbols documented, `go.mod` tidy — using the repo's own commands where declared.

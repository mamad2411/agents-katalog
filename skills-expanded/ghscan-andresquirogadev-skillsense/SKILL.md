# Go Skill

You are working on a Go project. Apply these conventions.

## Project Structure

- Follow the standard layout: `cmd/<appname>/main.go`, `internal/`, `pkg/` for exported packages.
- Keep `main.go` thin — instantiate dependencies and call a `run()` function that returns an error.
- Use `internal/` to prevent external packages from importing implementation details.

## Error Handling

- Always handle errors — never use `_` for error values in production code.
- Wrap errors with context: `fmt.Errorf("loading config: %w", err)`.
- Use `errors.Is()` and `errors.As()` — never compare error strings.
- Define sentinel errors with `var ErrNotFound = errors.New("not found")`.
- Return early on error (`if err != nil { return … }`) — avoid nested `if` pyramids.

## Goroutines & Concurrency

- Always clean up goroutines; use `context.Context` for cancellation propagation.
- Use `sync.WaitGroup` to wait for goroutines; use channels for communication.
- Use `sync.Mutex` to protect shared state; prefer `sync/atomic` for simple counters.
- Avoid goroutine leaks — every goroutine must have a clear exit condition.
- Use `errgroup.Group` (from `golang.org/x/sync/errgroup`) for parallel work with error handling.

## HTTP (net/http)

- Go 1.22+ `ServeMux` supports method-specific routing: `mux.HandleFunc("GET /users/{id}", handler)`.
- Use `http.NewRequestWithContext` for all outbound HTTP requests — always pass a context with a timeout.
- Define middleware as `func(http.Handler) http.Handler`.
- Set `ReadTimeout`, `WriteTimeout`, and `IdleTimeout` on `http.Server`.

## Interfaces

- Define small, focused interfaces at the point of use (consumer side), not at the implementation.
- Accept interfaces, return concrete types.
- The `io.Reader` / `io.Writer` / `io.Closer` family of interfaces should be used for I/O abstraction.

## Testing

- Use the standard `testing` package; prefer table-driven tests.
- Use `t.Helper()` in helper functions to get accurate line numbers on failures.
- Use `httptest.NewServer` or `httptest.NewRecorder` for HTTP handler tests.
- Use `-race` flag in CI: `go test -race ./...`.

## Modules

- Run `go mod tidy` after dependency changes to keep `go.sum` current.
- Use `go work` for multi-module monorepos.

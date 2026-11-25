---
name: backend-stack-go
description: "A Go backend: project layout (cmd, internal), net/http routing (or chi), handlers and services with interfaces defined by consumers, decoding and validation, context and timeouts, wrapped errors mapped in one place, pgx and sqlc with pool settings, slog, graceful shutdown, goroutines and errgroup, config, table-driven tests with httptest and Testcontainers, linters and small static binaries. Read when building or changing a Go backend."
---

# Go

The generated Go service: gin with a package-level `db *sql.DB`,
`http.ListenAndServe` with no timeouts, `log.Fatal` inside a handler,
`panic(err)` for bad input, errors compared by their text, an interface
beside every struct "for mocking", and a goroutine per request that nobody
waits for. The backend rules are in the `backend` skill; these are Go's own.

## 1. Setup

- A module per service (`go.mod` with the Go version), the standard layout
  the project uses (`cmd/api/main.go`, `internal/<feature>/`), `gofmt` and
  `go vet` clean, golangci-lint when the project has it.
- Go 1.26 is current and the two newest releases get fixes: build with
  one of them (`go 1.25` or later in `go.mod`, a `toolchain` line to pin).
- Code generators and CLIs as tool dependencies (Go 1.24+):
  `go get -tool github.com/sqlc-dev/sqlc/cmd/sqlc`, then `go tool sqlc
  generate`; versions live in `go.mod` like any dependency.
- `internal/platform/` holds the shared HTTP helpers (decode, errors,
  middleware), database and config; `migrations/` the numbered SQL files;
  `queries/` the SQL sqlc reads. No `pkg/` unless another module imports it,
  and no `utils` package.

## 2. Routing

- Routing with `net/http` (Go 1.22+ patterns: `mux.HandleFunc("GET
  /orders/{id}", h.get)`, `r.PathValue("id")`); chi when the project uses it.
  No framework added for a handful of routes.
- `{path...}` matches the rest of the path and `/{$}` only the root; the
  most specific pattern wins, conflicting ones panic at registration, and a
  wrong method gets `405` with an `Allow` header by itself.
- Middleware is `func(http.Handler) http.Handler`, wrapped around the mux
  in `main`. Cookie-authenticated endpoints get CSRF protection from
  `http.NewCrossOriginProtection().Handler(mux)` (Go 1.25).

## 3. Structure

- `main` builds the config, the pool, the services and the handlers, and
  passes them in: no package-level globals for the database or the logger.
  `main` calls `run(ctx) error` and exits non-zero on its error, so start-up
  is testable and there is one exit point.
- Per feature: a handler type that decodes, validates, calls the service
  and encodes; a service with the rules; a store with the queries; the types
  in the package.
- Interfaces are declared by the code that uses them, with only the methods
  it calls: the handler declares `type reserver interface { Reserve(ctx
  context.Context, id string, qty int) error }`; the store returns a
  concrete `*Store`. Accept interfaces, return structs; no interface until a
  second implementation or a test fake needs one.
- Config is a struct parsed once in `run`: `caarlos0/env`
  (`env.ParseAs[Config]()`, tags `env:"DATABASE_URL,required"`) or
  `sethvargo/go-envconfig`, koanf when files and env are layered
  (`kelseyhightower/envconfig` works but is unmaintained); the error names
  the missing variable.

## 4. Decoding and validation

- Validation in a method on the request type or go-playground/validator,
  then the handler answers `400` with the field errors. One generic decoder
  reads every body:

```go
// Decode: one JSON object of at most 1 MB, unknown fields refused, then T's own checks.
func Decode[T interface{ Valid() []FieldError }](w http.ResponseWriter, r *http.Request) (T, error) {
	var v T
	dec := json.NewDecoder(http.MaxBytesReader(w, r.Body, 1<<20))
	dec.DisallowUnknownFields()
	if err := dec.Decode(&v); err != nil {
		return v, &ValidationError{Errors: []FieldError{{Field: "body", Code: "malformed_json"}}}
	}
	if dec.Decode(&struct{}{}) != io.EOF {
		return v, &ValidationError{Errors: []FieldError{{Field: "body", Code: "trailing_data"}}}
	}
	if errs := v.Valid(); len(errs) > 0 {
		return v, &ValidationError{Errors: errs}
	}
	return v, nil
}
```

- With validator: `validator.New(validator.WithRequiredStructEnabled())`,
  tags such as `validate:"required,uuid"` and `validate:"min=1,max=100"`,
  and `validator.ValidationErrors` turned into codes (`fe.Tag()`). It reports
  Go field names (`ProductID`); `RegisterTagNameFunc` reading the `json` tag
  gives the API's names.

## 5. Context and time limits

- Every handler passes `r.Context()` down to the service, the store and
  outbound calls, so a client that goes away cancels the work.
- Timeouts: `http.Server` with `ReadHeaderTimeout`, `ReadTimeout`,
  `WriteTimeout` and `IdleTimeout` set; `http.MaxBytesReader` on bodies;
  `context.WithTimeout` around slow calls; an `http.Client` with a `Timeout`,
  never `http.DefaultClient`.
- The client's `Transport` keeps only 2 idle connections per host by
  default: raise `MaxIdleConnsPerHost` (32) for an upstream called often.
- Work that must finish after the client leaves (an audit row) runs on
  `context.WithoutCancel(ctx)` with its own timeout.

## 6. Errors

- Errors are values: wrapped with context (`fmt.Errorf("pay order %d: %w",
  id, err)`), compared with `errors.Is` and `errors.As` (or Go 1.26's
  `errors.AsType[*ConflictError](err)`), never by their string.
- Domain errors as sentinel values or types (`ErrNotFound`, `*ConflictError`)
  mapped to status codes in one helper that every handler calls to write
  errors, in the format of `backend-errors`.
- No `panic` for expected failures; a recovery middleware turns an
  unexpected panic into a `500` and a log line.

```go
func WriteError(w http.ResponseWriter, r *http.Request, err error) {
	p := problem{Status: http.StatusInternalServerError, Code: "internal"}
	var conflict *ConflictError
	var invalid *ValidationError
	switch {
	case errors.Is(err, ErrNotFound), errors.Is(err, ErrForbidden): // another user's record is a 404
		p.Status, p.Code = http.StatusNotFound, "not_found"
	case errors.As(err, &conflict):
		p.Status, p.Code = http.StatusConflict, conflict.Code
	case errors.As(err, &invalid):
		p.Status, p.Code, p.Errors = http.StatusBadRequest, "validation_failed", invalid.Errors
	default:
		p.RequestID = RequestID(r.Context())
		slog.ErrorContext(r.Context(), "request failed", "err", err, "request_id", p.RequestID) // logged once
	}
	p.Type = "https://example.com/errors/" + strings.ReplaceAll(p.Code, "_", "-")
	w.Header().Set("Content-Type", "application/problem+json")
	w.WriteHeader(p.Status)
	_ = json.NewEncoder(w).Encode(p)
}
```

## 7. Data

- sqlc (SQL written by hand, Go generated from it) or pgx directly; migrations
  with goose, atlas or golang-migrate, run as a release step (`goose -dir
  migrations postgres "$DATABASE_URL" up`); transactions with `pool.BeginTx`
  and a deferred `Rollback` that is a no-op after `Commit`.
- sqlc queries carry their shape (`-- name: ReserveStock :execrows`), with
  `sql_package: "pgx/v5"`; inside a transaction `queries.WithTx(tx)`.
- Pools sized on purpose: pgxpool defaults to the larger of 4 and the CPU
  count, so set `MaxConns` (10) against the database's limit across
  instances, plus `MaxConnIdleTime`. With `database/sql`, `SetMaxOpenConns`
  is unlimited by default: always set it, with `SetMaxIdleConns` equal and
  `SetConnMaxLifetime(time.Hour)`.
- `pgx.ErrNoRows` becomes `ErrNotFound`; a `*pgconn.PgError` with code
  `23505` becomes a conflict, told apart by `ConstraintName`.

```go
// Reserve takes stock in one statement: 0 rows means not enough, with no race.
func (s *Store) Reserve(ctx context.Context, productID string, qty int) error {
	tag, err := s.pool.Exec(ctx,
		`UPDATE products SET stock = stock - $2 WHERE id = $1 AND stock >= $2`, productID, qty)
	if err != nil {
		return fmt.Errorf("reserve %s: %w", productID, err)
	}
	if tag.RowsAffected() == 0 {
		return &ConflictError{Code: "out_of_stock"}
	}
	return nil
}
```

## 8. Logs

- `log/slog` with a JSON handler, the request id added by middleware and
  carried in the context.
- One line per request from middleware, with `r.Pattern` (Go 1.23+: the
  matched `"POST /orders"`, never the raw path). The mux sets it on the
  request it receives, so the middleware logs the request it passed down,
  not its own copy from before `WithContext`.
- Secrets as a type whose `LogValue()` returns `[redacted]`, or dropped by
  `ReplaceAttr` on the handler.

## 9. Shutdown

```go
ctx, stop := signal.NotifyContext(ctx, os.Interrupt, syscall.SIGTERM)
defer stop()
srv := &http.Server{Addr: cfg.Addr, Handler: httpx.Logging(mux), ReadHeaderTimeout: 5 * time.Second,
	ReadTimeout: 10 * time.Second, WriteTimeout: 30 * time.Second, IdleTimeout: 120 * time.Second}
errCh := make(chan error, 1)
go func() { errCh <- srv.ListenAndServe() }()
select {
case err := <-errCh:
	return err // could not listen
case <-ctx.Done():
}
ready.Store(false)         // /readyz answers 503
time.Sleep(cfg.DrainDelay) // 5s: the load balancer stops sending
shutdownCtx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
defer cancel()
if err := srv.Shutdown(shutdownCtx); err != nil { // waits for requests in flight
	return fmt.Errorf("shutdown: %w", err)
}
pool.Close()
```

- `Shutdown` does not wait for hijacked connections (WebSockets): register
  their closing with `srv.RegisterOnShutdown`. Workers stop through the same
  context, after their current job.

## 10. Goroutines

- Every goroutine has an owner that waits for it and a context that stops
  it. Work that must outlive the request goes to a queue (River on
  PostgreSQL, Asynq on Redis: `backend-jobs`), never a bare `go` statement.
- Fan-out with `errgroup.WithContext`: the first error cancels the rest, and
  `g.SetLimit(8)` bounds how many run at once. `sync.WaitGroup.Go` (Go 1.25)
  when errors are collected another way.
- A panic in a goroutine you start ends the process, recovery middleware or
  not: recover inside it. Leaks show in tests with `goleak.VerifyTestMain(m)`.

## 11. Tests

- Table-driven tests with `t.Run`; `httptest.NewRecorder` with the handler,
  or `httptest.NewServer` for the whole router and for fakes of other
  services; `t.Context()` (Go 1.24) for contexts that end with the test.
- A real database per `backend-testing`: testcontainers-go's module
  (`postgres.Run(ctx, "postgres:17-alpine", postgres.WithDatabase("app"),
  postgres.BasicWaitStrategies())`), migrated once, with `Snapshot` and
  `Restore` between tests; each package that runs in parallel gets its own
  database.
- Fakes behind small interfaces for other services; `testing/synctest` (Go
  1.25) for code with timers; `go test -race ./...`.

```go
for _, tt := range []struct {
	name, body string
	err        error // what the fake store returns
	want       int
}{
	{"reserves", `{"productId":"p1","quantity":2}`, nil, 201},
	{"refuses unknown fields", `{"productId":"p1","quantity":2,"price":1}`, nil, 400},
	{"out of stock", `{"productId":"p1","quantity":2}`, &ConflictError{Code: "out_of_stock"}, 409},
} {
	t.Run(tt.name, func(t *testing.T) {
		mux := http.NewServeMux()
		NewHandler(fakeReserver{err: tt.err}).Routes(mux)
		rec := httptest.NewRecorder()
		mux.ServeHTTP(rec, httptest.NewRequest(http.MethodPost, "/orders", strings.NewReader(tt.body)))
		if rec.Code != tt.want {
			t.Errorf("status = %d, want %d: %s", rec.Code, tt.want, rec.Body)
		}
	})
}
```

## 12. Build and run

- A static binary: `CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o
  /out/api ./cmd/api`, copied into `gcr.io/distroless/static:nonroot` (or
  `scratch` with CA certificates); the image is tens of megabytes. The
  commit is in the binary (`debug.ReadBuildInfo()` reports `vcs.revision`).
- Go 1.25 sets `GOMAXPROCS` from the container's CPU limit (before it,
  `go.uber.org/automaxprocs`); set `GOMEMLIMIT` to about 90% of the memory
  limit so the GC works harder before the container is killed.

## Check it

`go build ./...`, `go vet ./...`, `staticcheck ./...` or `golangci-lint run`,
`go test -race ./...`, `govulncheck ./...`, then run it and call the
endpoints with `curl`: an unknown field gives a `400`, a wrong method a
`405`, and `kill -TERM` during a slow request lets it finish.

## Avoid

Globals for the database or config; `http.DefaultClient` or a server with no
timeouts; ignored errors (`_ =` on anything that can fail); errors compared by
string; `panic` for a bad request; a goroutine per request left running;
`context.Background()` inside a handler; an interface per struct; logging an
error and returning it too; `database/sql` with no pool limits; the raw URL
path in logs or metric labels; `log.Fatal` anywhere but `main`.

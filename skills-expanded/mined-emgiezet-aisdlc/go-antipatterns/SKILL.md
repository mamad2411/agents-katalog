---
name: go-antipatterns
description: Forbidden Go patterns — SQL injection, shell injection, missing timeouts, resource leaks, goroutine leaks, and error handling issues. Applies when editing Go files.
paths: ["**/*.go"]
user-invocable: false
---

# Go anti-patterns — do not write these

Checks run automatically after each edit. Findings reference the IDs below.

## Blockers
- AP-GO-SEC-001 — Build SQL with `$1`/`?` placeholders; never use `fmt.Sprintf` or `+` to compose queries.
- AP-GO-SEC-002 — Use `exec.Command("prog", arg1, arg2)` with separate args; never `sh -c` with user input.
- AP-GO-SEC-004 — Use `crypto/rand` for tokens and secrets; `math/rand` is for simulations only.
- AP-GO-SEC-005 — Never set `InsecureSkipVerify: true`; configure a valid `RootCAs` pool.

## Errors
- AP-GO-SEC-003 — Set `ReadHeaderTimeout`, `ReadTimeout`, `WriteTimeout`, `IdleTimeout` on `http.Server`.
- AP-GO-PERF-001 — Set `Client.Timeout` and use `NewRequestWithContext`; never use `http.Get` without a timeout.
- AP-GO-PERF-002 — Defer `resp.Body.Close()` and `rows.Close()` immediately; always check `rows.Err()`.
- AP-GO-PERF-003 — Limit goroutine fan-out with `errgroup.SetLimit`; always propagate context for cancellation.
- AP-GO-MAINT-001 — Handle every error; wrap with `fmt.Errorf("…: %w", err)`; compare with `errors.Is`/`errors.As`.
- AP-GO-MAINT-002 — Return errors from libraries; never call `panic`/`log.Fatal`/`os.Exit` outside `main`.

## Warnings
- AP-GO-MAINT-003 — Propagate the request `ctx` through all calls; never use `context.Background()` in handlers.

Details for any ID: `reference/<ID>.md`

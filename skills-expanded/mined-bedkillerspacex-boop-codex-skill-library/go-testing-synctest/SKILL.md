---
name: go-testing-synctest
description: >
  Go testing/synctest (bubble/synthetic time) for deterministic concurrency tests:
  when available by Go version, isolating goroutines, advancing time without
  sleeps, and migrating flaky time-based tests. Use for owned Go modules on
  supported toolchains.
---

# Go testing/synctest

## Scope And Authorization

- **In scope:** Test code in modules you maintain on Go versions that provide `testing/synctest`.
- **Out of scope:** Relying on synctest APIs in production runtime code.
- APIs evolved (experimental → promoted); **confirm your Go version docs** before use.
- Pair with `go-race-detector-workflow`, `go-context-timeouts`, `go-cmp-diff-tests`.

## When To Use

- Tests that currently use `time.Sleep` to wait for goroutines.
- Timers, tickers, deadlines that make CI flaky.
- Deterministic scheduling of concurrent protocol logic under test.
- Replacing brittle wall-clock assumptions.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Race detection | `go-race-detector-workflow` |
| Production timeouts | `go-context-timeouts` |
| Table asserts | `go-cmp-diff-tests` |
| General style | `go-style-conventions` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Idea | Meaning |
| --- | --- |
| Synctest bubble | Isolated environment for concurrent test code |
| Synthetic clock | Time advances when goroutines block on timers |
| Flaky sleep | Wall-clock wait — often racey under load |
| Durability | Prefer public `testing/synctest` APIs for your Go version |

**Version note:** `testing/synctest` landed via experiment (`//go:build goexperiment.synctest`)
and has been moving into stable testing support depending on release. Always check:

```bash
go doc testing/synctest
go help test
```

If package missing, upgrade toolchain or keep classic patterns below.

## Workflow

### 1. Confirm availability

```bash
go version
go doc testing/synctest.Run 2>/dev/null || echo "not available — upgrade Go"
```

Set `go 1.XX` in go.mod to the minimum that supports your chosen API.

### 2. Identify flaky tests

Search:

```bash
# patterns
rg -n "time\\.Sleep|runtime\\.Gosched" --glob "*_test.go"
```

Candidates: wait-for-cache-expiry, debounce, retry-after, session TTL.

### 3. Classic deterministic alternatives (always valid)

If synctest not available:

```go
// Inject clock interface
type Clock interface {
    Now() time.Time
    After(d time.Duration) <-chan time.Time
}

// Or use channels to signal completion instead of sleep
done := make(chan struct{})
go func() { work(); close(done) }()
select {
case <-done:
case <-time.After(2 * time.Second):
    t.Fatal("timeout")
}
```

Prefer dependency injection of time for libraries.

### 4. Synctest pattern (illustrative)

```go
package debounce_test

import (
    "testing"
    "testing/synctest" // require supported Go
)

func TestDebounce(t *testing.T) {
    synctest.Run(func() {
        // start concurrent code that uses time.Timer/After
        // blocked timers allow bubble to advance time deterministically
        // assert state after synthetic advancement per current API
    })
}
```

Exact helper names (`Run`, `Wait`, …) — **follow `go doc` for your version**.

### 5. What belongs in the bubble

| Inside bubble | Outside |
| --- | --- |
| Goroutines under test | Real network to prod |
| Timers using std time | Third-party libs ignoring context/time inject |
| Channels between them | Global wall-clock metrics scrapers |

Code that calls OS real-time APIs may not virtualize fully — design for testability.

### 6. Race + synctest

```bash
go test -race ./...
```

Synctest reduces flakes; still run race detector for data races.

### 7. Migrate sleep tests checklist

1. Replace sleep with completion signal or synthetic time.
2. Ensure failure path still times out (avoid infinite hang).
3. Run with `-count=100` on previous flake.
4. Document Go version requirement in README if API new.

### 8. CI

- Use Go version matrix that includes the synctest-capable version.
- Avoid `-parallel` interactions that break assumptions unless supported.
- Keep test timeout (`-timeout`) for deadlocks.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Waiting | Channel/synctest | Random 50ms sleeps |
| Clocks | Injected | `time.Now()` scattered untestable |
| Version | go.mod enforces | Use APIs only on one laptop Go tip |
| Failures | Explicit timeout | Hang until CI hour limit |
| Scope | Unit concurrency | Full k8s integration in bubble |

## Output Checklist

- [ ] Go version supports chosen synctest API (or fallback used)
- [ ] Flaky sleep tests catalogued
- [ ] Migrated tests deterministic under `-count=100`
- [ ] Clock injection considered for library API
- [ ] `-race` clean
- [ ] CI Go version aligned
- [ ] Docs note minimum Go if needed
- [ ] `code-quality-standards` applied

## Rules

- Prefer deterministic concurrency tests over sleeps.
- Verify API against your Go release — do not invent helpers.
- Synctest is for tests, not production control flow.
- Still design exported APIs with injectable time when practical.
- Race detector remains mandatory for concurrent packages.

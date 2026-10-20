---
name: go-race-detector-workflow
description: >
  Use Go’s race detector (-race) effectively: local/CI enablement, interpreting
  reports, common fix patterns (mutex, channels, atomics), limitations, and
  performance cost. Use for owned Go codebases with concurrent logic.
---

# Go Race Detector Workflow

## Scope And Authorization

- **In scope:** Testing concurrent Go code you maintain.
- **Out of scope:** Deliberately racing third-party production without permission.
- `-race` requires cgo-enabled platforms (most Linux/macOS/Windows amd64); not every GOOS/GOARCH.
- Pair with `go-errgroup-limits`, `go-context-timeouts`, `code-quality-standards`.

## When To Use

- Any package using goroutines, shared maps/slices, or global mutable state.
- CI gate on PRs for concurrent services.
- Investigating flaky tests or Heisenbugs.
- Before releasing concurrency-sensitive libraries.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| errgroup limits | `go-errgroup-limits` |
| Unit assert diffs | `go-cmp-diff-tests` |
| Vuln scanning | `go-govulncheck-workflow` |
| Go style | `go-style-conventions` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Item | Notes |
| --- | --- |
| `go test -race` | Instrument memory accesses |
| `go build -race` | Race-enabled binary for integration |
| Report | Read/write stack pairs without sync |
| Happens-before | Channels, mutex, atomics, `sync` primitives establish order |
| False negatives | Possible — not a proof of race-freedom |
| Cost | Significant CPU/mem; not for every prod binary |

## Workflow

### 1. Local run

```bash
go test -race ./...
go test -race -count=10 ./pkg/concurrent/...
```

Higher `-count` surfaces intermittent races.

### 2. CI

```yaml
- name: Race tests
  run: go test -race -timeout=15m ./...
```

Tips:

- Separate job if slow; cache modules.
- Use larger runners if OOM.
- Fail closed on any race report.

### 3. Read a report

```text
WARNING: DATA RACE
Write at 0x... by goroutine 7:
  pkg.(*T).method()
Previous read at 0x... by goroutine 12:
```

Steps:

1. Identify shared variable.
2. Find intended ownership (who should sync).
3. Choose fix (mutex, channel ownership, atomic, copy).
4. Re-run `-race` with stress.

### 4. Fix patterns

**Mutex:**

```go
type Cache struct {
    mu sync.Mutex
    m  map[string]string
}

func (c *Cache) Get(k string) (string, bool) {
    c.mu.Lock()
    defer c.mu.Unlock()
    v, ok := c.m[k]
    return v, ok
}
```

**Ownership via channel** (no shared memory):

```go
// single goroutine owns map; others send requests on chan
```

**Atomic counters:**

```go
var hits atomic.Int64
hits.Add(1)
```

**Maps:** never concurrent map read/write — use `sync.Map` only when appropriate or mutex.

### 5. Tests that provoke races

```go
func TestParallel(t *testing.T) {
    t.Parallel()
    // or:
    var wg sync.WaitGroup
    for i := 0; i < 100; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            _ = doWork()
        }()
    }
    wg.Wait()
}
```

Use `testing.T.Parallel` carefully with shared package state.

### 6. Integration binaries

```bash
go test -race -c -o mypkg.test
./mypkg.test -test.v
# or
go build -race -o app && ./app # under load in staging
```

Do not ship `-race` builds as default production (perf).

### 7. Limitations checklist

- [ ] No race ≠ no concurrency bug (deadlocks, logic)
- [ ] Some arches unsupported
- [ ] CGO / external libs may be opaque
- [ ] Timing-dependent races need stress

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| CI | `-race` on every PR | Only once before yearly release |
| Fix | Clear ownership | “Sleep to avoid race” |
| Maps | Mutex or single owner | Concurrent map access |
| Prod | Race in staging soak | Always-on race binary prod |
| Tests | Stress concurrent paths | Only serial unit tests |

## Output Checklist

- [ ] `go test -race ./...` green
- [ ] CI job configured
- [ ] Known races fixed with correct primitives
- [ ] Stress tests for concurrent packages
- [ ] Limitations understood by team
- [ ] No “fix” via sleeps
- [ ] `code-quality-standards` applied

## Rules

- Fix races; do not ignore reports.
- Prefer clear ownership over heavy locking when possible.
- Race detector is a tool, not a proof.
- Keep prod binaries free of `-race` unless debugging intentionally.
- Combine with errgroup/context for structured concurrency.

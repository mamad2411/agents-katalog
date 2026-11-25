---
name: go-maps-clear
description: >
  Correct use of Go’s clear(m) on maps (and slices): semantics vs m=nil vs delete
  loop, retention of backing memory, concurrency rules, and when to reallocate.
  Use when optimizing or reviewing owned Go code for map lifecycle correctness.
---

# Go maps and `clear`

## Scope And Authorization

- **In scope:** Go 1.21+ codebases you maintain (built-in `clear`).
- **Out of scope:** Assuming `clear` exists on ancient toolchains without go.mod gate.
- `clear` is not a concurrency primitive — still need mutexes for shared maps.
- Pair with `go-style-conventions` and `code-quality-standards`.

## When To Use

- Reusing a map across loop iterations without reallocating.
- Emptying maps while keeping capacity for hot paths.
- Reviewing code that sets `m = nil` vs delete-all vs `clear(m)`.
- Reducing GC pressure from map churn.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General Go style | `go-style-conventions` |
| Race detector | `go-race-detector-workflow` |
| Sync primitives deep dive | concurrency skills |
| Implementation quality | `code-quality-standards` |

## Concepts

| Operation | Effect on map |
| --- | --- |
| `clear(m)` | Removes all entries; **keeps** backing store/capacity |
| `m = nil` | Drops reference; GC can reclaim; next write needs new make |
| `m = make(...)` | New map; old reclaimed if unreferenced |
| `delete(m,k)` loop | Removes entries; capacity retained (similar spirit) |
| `clear(s)` on slice | Zeros elements length; capacity kept; length unchanged for slices |

For **slices**, `clear(s)` sets elements up to `len(s)` to zero values; does not retarget capacity. For **maps**, empties keys/values.

### Concurrency

Reading/writing a map without sync from multiple goroutines is undefined (fatal).
`clear` counts as a write.

## Workflow

### 1. Confirm language version

```bash
go version
# go.mod: go 1.21 or newer for clear builtin
```

### 2. Prefer clear for reuse

```go
// Hot loop: reuse map
m := make(map[string]int, 64)
for _, batch := range batches {
    clear(m)
    for _, item := range batch {
        m[item.K] = item.V
    }
    process(m)
}
```

vs:

```go
// Allocates every batch
for _, batch := range batches {
    m := make(map[string]int)
    // ...
}
```

### 3. Prefer nil when releasing memory matters

```go
// Large map no longer needed; allow GC
m = nil
// or m = make(map[K]V) with small size if reusing variable sparsely
```

If a map grew huge once, `clear` retains large backing; **reallocate** if footprint must shrink.

### 4. Migration from delete loop

```go
// Old
for k := range m {
    delete(m, k)
}
// New
clear(m)
```

Behavior: both empty; `clear` is clearer and optimized.

### 5. Slices note

```go
s := []int{1, 2, 3, 4}
clear(s)           // s is [0 0 0 0], len 4, cap unchanged
s = s[:0]          // len 0, cap unchanged, elements may still be referenced until overwritten
```

Pick based on whether zeroing is required (pointer slices → clear helps GC of pointed objects when combined with len tricks carefully).

### 6. Tests

```go
func TestClearMap(t *testing.T) {
    m := map[string]int{"a": 1}
    clear(m)
    if len(m) != 0 {
        t.Fatalf("len=%d", len(m))
    }
    m["b"] = 2 // still usable
}
```

Race test if shared:

```bash
go test -race ./...
```

### 7. Review checklist

- [ ] go version supports `clear`
- [ ] Reuse intentional vs memory retain OK
- [ ] No concurrent map access without lock
- [ ] Huge maps reallocated when memory must drop
- [ ] Not used as substitute for new map when types/shape change

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Hot reuse | `clear(m)` each iteration | `make` every time without need |
| Memory | `m=nil` after giant growth | `clear` forever retaining GB |
| Concurrency | Mutex around map+clear | clear while other goroutine ranges |
| Readability | clear over delete loop | obscure bit tricks |
| Toolchain | go 1.21+ in go.mod | Use clear then build with 1.20 CI |

## Output Checklist

- [ ] Lifecycle choice documented (reuse vs reclaim)
- [ ] `clear` used correctly for maps/slices
- [ ] Concurrency reviewed
- [ ] Tests cover empty+reuse
- [ ] `-race` clean if concurrent
- [ ] go.mod version sufficient
- [ ] `code-quality-standards` applied

## Rules

- `clear` keeps capacity for maps.
- Concurrent map access still forbidden.
- Reallocate when RSS must shrink.
- Prefer clear over manual delete-all loops.
- Style skill for broader conventions.

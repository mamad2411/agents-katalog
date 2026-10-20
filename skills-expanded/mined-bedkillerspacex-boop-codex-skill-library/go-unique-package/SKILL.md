---
name: go-unique-package
description: >
  Go unique package (unique.Make / Handle) for interning comparable values:
  reducing duplicate allocations, Handle comparison, lifetime/GC notes, and
  when not to intern. Use on Go 1.23+ owned codebases with high duplication of
  immutable comparable values.
---

# Go `unique` Package

## Scope And Authorization

- **In scope:** Performance work on Go modules you maintain (Go 1.23+ `unique`).
- **Out of scope:** Premature interning that obscures code without measurements.
- Interning is for **immutable comparable** values; do not intern secrets as a security control.
- Pair with `go-style-conventions`, profiling practice, `code-quality-standards`.

## When To Use

- Many duplicate strings/structs alive concurrently (protocols, symbol tables, routers).
- You need cheap equality via handle compare after interning.
- Profiling shows allocation dominated by repeated identical values.
- Building compilers, proxies, or control planes with repetitive keys.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Map clear/reuse | `go-maps-clear` |
| General style | `go-style-conventions` |
| Caching business data | `caching-strategies` |
| Concurrency races | `go-race-detector-workflow` |
| Implementation quality | `code-quality-standards` |

## Concepts

| API | Role |
| --- | --- |
| `unique.Make[T comparable](v T) unique.Handle[T]` | Intern value; return handle |
| `Handle.Value()` | Recover the value |
| Handle equality | Same interned value ⇒ equal handles |
| GC | Unused interned values can be collected (handles drop) |
| Comparable constraint | Only comparable `T` |

Not a concurrent map replacement for mutable state; not a global string pool with manual free.

## Workflow

### 1. Confirm toolchain

```bash
go version   # need 1.23+ for unique in stdlib
go doc unique
```

```go
// go.mod
go 1.23
```

### 2. Measure first

```bash
go test -bench=. -benchmem ./pkg/hotpath
# pprof allocs if needed
```

Record baseline allocs/op and RSS.

### 3. Apply interning

```go
import "unique"

type Method unique.Handle[string]

func InternMethod(s string) Method {
    return Method(unique.Make(s))
}

func (m Method) String() string { return unique.Handle[string](m).Value() }

// map keys as handles
var handlers = map[Method]http.Handler{}
```

Struct example:

```go
type pair struct{ Host, Path string }

h := unique.Make(pair{Host: host, Path: path})
// store h in maps/slices; compare handles
```

### 4. Correctness rules

| Do | Don't |
| --- | --- |
| Intern immutable values | Intern then mutate underlying (impossible for strings; careful with structs holding refs) |
| Compare handles | Assume intern is encryption/hash security |
| Drop handles for GC | Cache handles forever without bound for unbounded dynamic values |
| Keep API clear | Intern every string blindly |

If struct contains pointers/slices, **comparable** may not apply — only comparable types.

### 5. Concurrency

`unique.Make` is safe for concurrent use. Still protect maps of handles with normal rules.

### 6. When not to use

- Values almost always unique (no sharing benefit).
- Short-lived single-use values (overhead &gt; benefit).
- Pre-1.23 codebases without upgrade path.
- Readability-critical code paths without proven gain.

### 7. Verify

```bash
go test ./...
go test -race ./...
go test -bench=. -benchmem ./pkg/hotpath
```

Expect lower allocs/op when duplication was real; watch for regressions.

### 8. Document

Comment why interning exists; link benchmark numbers in PR.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Evidence | Benchmark before/after | Intern because trendy |
| Types | Comparable immutable | Force unsafe comparable hacks |
| Lifetime | Handles drop naturally | Global forever map of all user inputs |
| Clarity | Small intern boundary | Unique handles leak into every public API |
| Security | Not used as auth | “Handle equality means trusted” |

## Output Checklist

- [ ] Go 1.23+ enforced
- [ ] Profiling/bench evidence captured
- [ ] Intern applied only to hot duplicated values
- [ ] Handles used consistently for equality
- [ ] Race tests pass
- [ ] Bench shows improvement or rollback
- [ ] Comments explain rationale
- [ ] `code-quality-standards` applied

## Rules

- Measure first; intern second.
- Comparable immutable values only.
- Not a security boundary.
- Safe concurrent Make; normal map rules still apply.
- Prefer clarity when gains are negligible.

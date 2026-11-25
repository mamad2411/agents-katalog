---
name: go-cmp-diff-tests
description: >
  Use github.com/google/go-cmp for readable Go test diffs: cmp.Diff, cmp.Equal,
  Options (IgnoreFields, FilterPath, Transformers, Comparers), and anti-patterns
  vs reflect.DeepEqual. Use when writing or refactoring Go unit tests for owned code.
---

# go-cmp Diff Tests

## Scope And Authorization

- **In scope:** Test code in repositories you maintain.
- **Out of scope:** Shipping `cmp.Diff` in production hot paths as a general equality API
  (it’s optimized for tests).
- Prefer test-only import of `go-cmp`; keep production equality domain-specific when needed.
- Pair with `go-style-conventions` and `code-quality-standards`.

## When To Use

- Asserting complex structs, slices, maps with clear failure messages.
- Migrating from `reflect.DeepEqual` / spew dumps.
- Ignoring volatile fields (`ID`, `CreatedAt`) in golden comparisons.
- Custom comparison for time, decimal, or proto-ish types in tests.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Go style overall | `go-style-conventions` |
| Race detector | `go-race-detector-workflow` |
| Context timeouts | `go-context-timeouts` |
| Generic test synctest | `go-testing-synctest` |
| Implementation quality | `code-quality-standards` |

## Concepts

| API | Use |
| --- | --- |
| `cmp.Diff(want, got)` | Empty string if equal; unified-ish diff if not |
| `cmp.Equal` | Boolean |
| `cmpopts.IgnoreFields` | Skip fields by name |
| `cmpopts.IgnoreUnexported` | Handle unexported (careful) |
| `cmpopts.SortSlices` | Order-insensitive slice compare |
| `cmp.Comparer` / `Transformer` | Custom equality |
| `cmp.FilterPath` | Conditional options |

Convention: **want then got** in `Diff(want, got)` so messages read naturally.

## Workflow

### 1. Add dependency (tests)

```bash
go get github.com/google/go-cmp@latest
# import in _test.go only when possible
```

### 2. Basic assertion helper

```go
package mypkg_test

import (
    "testing"

    "github.com/google/go-cmp/cmp"
)

func TestUserView(t *testing.T) {
    got := BuildUserView(/* ... */)
    want := UserView{Name: "Ada", Roles: []string{"admin"}}

    if diff := cmp.Diff(want, got); diff != "" {
        t.Errorf("UserView mismatch (-want +got):\n%s", diff)
    }
}
```

### 3. Ignore volatile fields

```go
import "github.com/google/go-cmp/cmp/cmpopts"

opts := []cmp.Option{
    cmpopts.IgnoreFields(User{}, "ID", "CreatedAt", "UpdatedAt"),
}
if diff := cmp.Diff(want, got, opts...); diff != "" {
    t.Errorf("mismatch (-want +got):\n%s", diff)
}
```

### 4. Order-insensitive collections

```go
opts := []cmp.Option{
    cmpopts.SortSlices(func(a, b string) bool { return a < b }),
    cmpopts.SortMaps(func(a, b string) bool { return a < b }),
}
```

### 5. Approximate times

```go
opts := []cmp.Option{
    cmpopts.EquateApproxTime(time.Second),
}
```

### 6. Custom comparer

```go
opts := []cmp.Option{
    cmp.Comparer(func(a, b net.IP) bool {
        return a.Equal(b)
    }),
}
```

### 7. Transform for normalization

```go
// Example: compare canonical form of paths
opt := cmp.Transformer("CleanPath", func(p string) string {
    return path.Clean(p)
})
```

Use transformers sparingly — over-normalizing hides bugs.

### 8. Unexported fields

```go
// Prefer exported test DTOs. If necessary:
cmp.AllowUnexported(MyStruct{})
// or cmpopts.IgnoreUnexported(MyStruct{})
```

Prefer exporting test-facing accessors over AllowUnexported sprawl.

### 9. Anti-patterns

| Bad | Why |
| --- | --- |
| `cmp.Diff` in prod request path | Alloc-heavy, not for hot equality |
| Ignoring all fields that flake | Hides real regressions |
| `DeepEqual` then dump entire struct manually | Noisy failures |
| Floating map iteration order asserts via fmt | Use SortMaps |
| Comparing huge golden blobs without ignore | Brittle |

### 10. Verify

```bash
go test ./...
go test -run TestUserView -v
```

Failure output should show field-level `-want/+got` lines.

## Options cheat sheet

| Need | Option |
| --- | --- |
| Skip fields | `IgnoreFields` |
| Equate empty/nil slices | `EquateEmpty` |
| NaN floats | `EquateNaNs` |
| Approx floats | `EquateApprox` |
| Ignore error types detail | custom Comparer |
| Proto messages | Prefer `protocmp` if protos |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Message | `(-want +got)` + Diff | `t.Fatalf("%v", got)` only |
| Imports | `_test.go` | Production service imports cmp only for == |
| Ignores | Explicit field list | Global IgnoreUnexported everything |
| Slices | SortSlices when order free | Assert unstable order |
| Design | Small want structs | 500-line golden literal unreadable |

## Output Checklist

- [ ] go-cmp module added
- [ ] Tests use `cmp.Diff(want, got)`
- [ ] Volatile fields ignored intentionally
- [ ] Collection order handled
- [ ] Custom types have Comparer if needed
- [ ] Failures readable in CI logs
- [ ] No misuse in production hot path
- [ ] `code-quality-standards` applied

## Rules

- want before got in Diff.
- Keep options next to assertion or shared test helper.
- Prefer redesign of equality over opaque transformers.
- Test-focused skill; runtime concurrency elsewhere.
- Do not suppress meaningful diffs with broad ignores.

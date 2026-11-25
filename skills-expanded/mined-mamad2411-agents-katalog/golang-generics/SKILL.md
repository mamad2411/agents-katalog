---
name: golang-generics
description: "When to activate: Go generics, type parameters, constraints, comparable, any, generic data structures, golang.org/x/exp"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: go
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Go Generics (Go 1.18+)

## Type Parameters and Constraints

```go
import "golang.org/x/exp/constraints"

// Ordered — integers, floats, strings
func Min[T constraints.Ordered](a, b T) T {
    if a < b { return a }
    return b
}

// Any comparable type
func Contains[T comparable](slice []T, item T) bool {
    for _, v := range slice {
        if v == item { return true }
    }
    return false
}

// Multiple type parameters
func Map[T, U any](slice []T, f func(T) U) []U {
    result := make([]U, len(slice))
    for i, v := range slice { result[i] = f(v) }
    return result
}

func Filter[T any](slice []T, predicate func(T) bool) []T {
    result := make([]T, 0, len(slice))
    for _, v := range slice {
        if predicate(v) { result = append(result, v) }
    }
    return result
}

func Reduce[T, U any](slice []T, initial U, f func(U, T) U) U {
    result := initial
    for _, v := range slice { result = f(result, v) }
    return result
}
```

## Custom Constraints

```go
type Number interface {
    constraints.Integer | constraints.Float
}

func Sum[T Number](nums []T) T {
    var total T
    for _, n := range nums { total += n }
    return total
}

// Interface with method requirements
type Stringer interface {
    String() string
}

func JoinStrings[T Stringer](items []T, sep string) string {
    parts := make([]string, len(items))
    for i, item := range items { parts[i] = item.String() }
    return strings.Join(parts, sep)
}
```

## Generic Data Structures

```go
// Generic stack
type Stack[T any] struct {
    items []T
}

func (s *Stack[T]) Push(item T) { s.items = append(s.items, item) }
func (s *Stack[T]) Pop() (T, bool) {
    var zero T
    if len(s.items) == 0 { return zero, false }
    item := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return item, true
}
func (s *Stack[T]) Len() int { return len(s.items) }

// Generic set
type Set[T comparable] struct {
    m map[T]struct{}
}

func NewSet[T comparable]() Set[T] { return Set[T]{m: make(map[T]struct{})} }
func (s *Set[T]) Add(v T)          { s.m[v] = struct{}{} }
func (s *Set[T]) Has(v T) bool     { _, ok := s.m[v]; return ok }
func (s *Set[T]) Remove(v T)       { delete(s.m, v) }
func (s *Set[T]) Len() int         { return len(s.m) }
```

## Generic Result Type

```go
type Result[T any] struct {
    value T
    err   error
}

func Ok[T any](value T) Result[T]  { return Result[T]{value: value} }
func Err[T any](err error) Result[T] { return Result[T]{err: err} }

func (r Result[T]) Unwrap() (T, error) { return r.value, r.err }
func (r Result[T]) IsOk() bool         { return r.err == nil }
func (r Result[T]) OrElse(def T) T {
    if r.err != nil { return def }
    return r.value
}

// Usage
result := fetchUser(id)
if result.IsOk() {
    user, _ := result.Unwrap()
    // use user
}
```

## Generic Cache

```go
type Cache[K comparable, V any] struct {
    mu    sync.RWMutex
    items map[K]cacheEntry[V]
    ttl   time.Duration
}

type cacheEntry[V any] struct {
    value     V
    expiresAt time.Time
}

func NewCache[K comparable, V any](ttl time.Duration) *Cache[K, V] {
    return &Cache[K, V]{items: make(map[K]cacheEntry[V]), ttl: ttl}
}

func (c *Cache[K, V]) Set(key K, value V) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.items[key] = cacheEntry[V]{value: value, expiresAt: time.Now().Add(c.ttl)}
}

func (c *Cache[K, V]) Get(key K) (V, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    entry, ok := c.items[key]
    if !ok || time.Now().After(entry.expiresAt) {
        var zero V
        return zero, false
    }
    return entry.value, true
}
```

## Common Anti-Patterns

- **Generics for simple single-type functions** — only use when genuinely needed for multiple types
- **`any` constraint when `comparable` suffices** — `any` can't be used in map keys
- **Instantiating types in inner loops** — prefer pre-allocated generic types
- **Type assertions on generic values** — defeats the purpose; restructure with constraints
- **Go 1.17 with generics** — generics require Go 1.18+; check `go.mod` `go` directive

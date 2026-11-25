---
name: samber-mo
description: "Option/Result monads with samber/mo — type-safe Option, Result, Either, Either3-5, Future, IO, Task, State for nil-safety, error-as-values, and composable pipelines. Use when choosing a monad for nullable fields or fallible operations, composing Map/FlatMap/OrElse pipelines, wrapping Go's (T, error) at API boundaries with TupleToResult/TupleToOption, or reviewing mo usage for MustGet misuse."
license: MIT
---

# samber/mo

**Option/Result.** A monad makes impossible states unrepresentable — Option eliminates nil dereferences, Result turns failure into a value that short-circuits through a chain. The discipline is to **compose**: choose the monad that matches the meaning, wrap Go's `(T, error)` at the API boundary, and build left-to-right pipelines so absence and failure are handled at the type level.

## Steps — choose and wrap

1. **Match the monad to the meaning.** `Option[T]` for a value that may be absent; `Result[T]` for an operation that may fail (a specialized `Either[error, T]`); `Either[L, R]` for two — `Either3`..`Either5` for more — valid alternatives where neither side is failure.
   *Done when: every nullable field is Option, every fallible operation returns Result, and Either appears only where both branches are valid.*
2. **Distinguish absent from zero.** `Option[string]` models "absent"; keep a plain `string` when the empty value is itself meaningful.
   *Done when: no Option wraps a zero value that carries meaning.*
3. **Wrap at the boundary.** Convert Go's `(T, error)` / `(V, bool)` with `mo.TupleToResult` / `mo.TupleToOption` at the API boundary, then chain inside domain code. Option implements `json.Marshaler/Unmarshaler`, `sql.Scanner`, `driver.Valuer` — use it directly in JSON structs and DB models.
   *Done when: no `(T, error)` pair crosses into a pipeline, and Option appears directly in model structs.*
4. **Compose left-to-right.** Chain `.Map(...).FlatMap(...).OrElse(default)` and prefer `OrElse` over `MustGet`. When a step changes the type parameter, route through sub-package functions (`option.Map`, `result.Pipe3`) — direct `.Map`/`.FlatMap` cannot change the type.
   *Done when: every pipeline reads left-to-right, and every type-changing step uses a sub-package function.*
5. **Reserve `MustGet` for certainty.** `MustGet` panics on `None`/`Err` — call it only inside `mo.Do` (which catches the panic as a Result error) or where presence is provable.
   *Done when: every `MustGet` sits inside a `mo.Do` block or has a stated guarantee of presence.*

## Steps — review or audit

1. **Scan for `MustGet` outside `mo.Do`.** *Done when: no panic-prone extraction appears on a fallible path.*
2. **Check the type choice.** *Done when: Option isn't wrapping a meaningful zero value, and Result/Either aren't swapped.*
3. **Check pipeline shape.** *Done when: no nested if/else replaces a chain, and no type-changing step uses a direct method.*

## Reference

### Core types

| Type | Purpose | Think of it as... |
| --- | --- | --- |
| `Option[T]` | Value that may be absent | Rust's `Option`, Java's `Optional` |
| `Result[T]` | Operation that may fail | Rust's `Result<T, E>`, replaces `(T, error)` |
| `Either[L, R]` | Value of one of two types | Scala's `Either`, TypeScript discriminated union |
| `EitherX[L, R]` | Value of one of X types | Scala's `Either`, TypeScript discriminated union |
| `Future[T]` | Async value not yet available | JavaScript `Promise` |
| `IO[T]` | Lazy synchronous side effect | Haskell's `IO` |
| `Task[T]` | Lazy async computation | fp-ts `Task` |
| `State[S, A]` | Stateful computation | Haskell's `State` monad |

### Option — nullable values without nil

```go
import "github.com/samber/mo"

name := mo.Some("Alice")          // Option[string] with value
empty := mo.None[string]()        // Option[string] without value
fromPtr := mo.PointerToOption(ptr) // nil pointer -> None

name.OrElse("Anonymous")   // "Alice"
empty.OrElse("Anonymous")  // "Anonymous"
```

**Key methods:** `Some`, `None`, `Get`, `MustGet`, `OrElse`, `OrEmpty`, `Map`, `FlatMap`, `Match`, `ForEach`, `ToPointer`, `IsPresent`, `IsAbsent`.

Option implements `json.Marshaler/Unmarshaler`, `sql.Scanner`, `driver.Valuer` — use it directly in JSON structs and database models.

### Result — error handling as values

```go
result := mo.TupleToResult(os.ReadFile("config.yaml"))

// Same-type transform — errors short-circuit automatically
upper := mo.Ok("hello").Map(func(s string) (string, error) {
    return strings.ToUpper(s), nil
}) // Ok("HELLO")

val := upper.OrElse("default")
```

**Type-change limitation:** Go methods cannot introduce new type parameters, so `Result[T].Map` returns `Result[T]`, never `Result[U]`. For type-changing transforms use sub-package functions or `mo.Do`:

```go
import "github.com/samber/mo/result"

parsed := result.Pipe2(
    mo.TupleToResult(os.ReadFile("config.yaml")),
    result.Map(func(data []byte) Config { return parseConfig(data) }),
    result.FlatMap(func(cfg Config) mo.Result[ValidConfig] { return validate(cfg) }),
)
```

**Key methods:** `Ok`, `Err`, `Errf`, `TupleToResult`, `Try`, `Get`, `MustGet`, `OrElse`, `Map`, `FlatMap`, `MapErr`, `Match`, `ForEach`, `ToEither`, `IsOk`, `IsError`.

### Either — discriminated union

```go
func fetchUser(id string) mo.Either[CachedUser, FreshUser] {
    if cached, ok := cache.Get(id); ok {
        return mo.Left[CachedUser, FreshUser](cached)
    }
    return mo.Right[CachedUser, FreshUser](db.Fetch(id))
}

result.Match(
    func(cached CachedUser) mo.Either[CachedUser, FreshUser] { /* use cached */ },
    func(fresh FreshUser) mo.Either[CachedUser, FreshUser] { /* use fresh */ },
)
```

**Either vs Result:** use `Result[T]` when one path is an error; use `Either[L, R]` when both paths are valid alternatives (cached vs fresh, left vs right, strategy A vs B).

### Do notation — imperative style with monadic safety

```go
result := mo.Do(func() int {
    a := mo.Some(21).MustGet()
    b := mo.Ok(2).MustGet()
    return a * b // 42
}) // Ok(42)

result := mo.Do(func() int {
    val := mo.None[int]().MustGet() // panics — Do catches it
    return val
}) // Err("no such element")
```

### Direct methods vs sub-package pipes

Direct methods (`.Map`, `.FlatMap`) work when the output type equals the input type; sub-package functions (`option.Map`, `result.Map`) are required when the output type differs; `option.Pipe3` / `result.Pipe3` chain multiple type-changing transformations readably.

```go
import "github.com/samber/mo/option"

result := option.Pipe3(
    mo.Some(42),
    option.Map(func(v int) string { return strconv.Itoa(v) }),
    option.Map(func(s string) []byte { return []byte(s) }),
    option.FlatMap(func(b []byte) mo.Option[string] {
        if len(b) > 0 { return mo.Some(string(b)) }
        return mo.None[string]()
    }),
)
```

**Rule of thumb:** direct methods for same-type transforms; sub-package functions + pipes when types change across steps.

### Common patterns

```go
// JSON API responses — Option omits null gracefully
type UserResponse struct {
    Name     string            `json:"name"`
    Nickname mo.Option[string] `json:"nickname"`
}

// Database nullable columns — implements sql.Scanner + driver.Valuer
type User struct {
    ID    int
    Email string
    Phone mo.Option[string]
}
err := row.Scan(&u.ID, &u.Email, &u.Phone)

// Wrapping existing Go APIs — m[key] returns (V, bool)
func MapGet[K comparable, V any](m map[K]V, key K) mo.Option[V] {
    return mo.TupleToOption(m[key])
}

// Uniform extraction — mo.Fold works across Option, Result, Either
str := mo.Fold[error, int, string](
    mo.Ok(42),
    func(v int) string { return fmt.Sprintf("got %d", v) },
    func(err error) string { return "failed" },
)
```

### Deep references

- **[Monads Guide](./references/monads-guide.md)** — functional programming concepts and why monads are valuable in Go
- **[Option Reference](./references/option.md)** — full Option API
- **[Result Reference](./references/result.md)** — full Result API
- **[Either Reference](./references/either.md)** — full Either API
- **[Pipelines Reference](./references/pipelines.md)** — sub-package functions and pipes
- **[Advanced Types Reference](./references/advanced-types.md)** — Future, IO, Task, State

### Official resources

- [github.com/samber/mo](https://github.com/samber/mo)
- [pkg.go.dev/github.com/samber/mo](https://pkg.go.dev/github.com/samber/mo)

## Watch for

| Mistake | Fix |
| --- | --- |
| `MustGet` on a possibly-absent value | `OrElse`, or `MustGet` only inside `mo.Do` |
| Option for a meaningful zero value | Plain type when empty is valid |
| Either for success/failure | `Result[T]` |
| Type-changing step via direct `.Map` | Sub-package `Map`/`PipeN` |
| Nested if/else where a chain reads cleaner | Chain `Map`/`FlatMap`/`OrElse` |
| `(T, error)` crossing into domain code | `TupleToResult`/`TupleToOption` at the boundary |

## Cross-references

- → See `samber-lo` for functional collection transforms (Map, Filter, Reduce on slices) that compose with mo types
- → See `samber-ro` for reactive pipelines that carry Option/Result values
- → See `samber-oops` for structured errors with context and stack traces
- → See `go-safety` for nil-safety and defensive Go coding
- → See `go-database` for database access patterns
- → See `go-lint` for staticcheck enforcement of panic-prone patterns

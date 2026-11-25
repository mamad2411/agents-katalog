---
name: go-uber-dig
description: "Go uber-go/dig — the reflection-based container: Provide/Invoke, dig.In/dig.Out parameter and result objects, named values, value groups, dig.As interface exposure, optional deps, Decorate, scopes. Apply when using or adopting uber-go/dig, the codebase imports `go.uber.org/dig`, or wiring an application graph at startup. For lifecycle and modules, see `go-uber-fx`."
license: MIT
---

# Go Uber Dig

**Leading word: container.** dig is a reflection-based container that resolves object graphs during startup. The discipline: build the graph once at the composition root, depend on interfaces not concrete types, and treat constructor errors as first-class failures.

## Steps — wire a graph

1. **Create the container at the composition root.** `dig.New()` lives in `main()`; never pass `*dig.Container` as a parameter — the container is plumbing, not a service. Service-locator patterns defeat the testability gains of DI.

   *Done when: the container lives in main and no service receives it.*

2. **Register constructors.** `c.Provide(fn)` — inputs are dependencies, outputs are provided types, a trailing `error` signals construction failure. Constructors are lazy and memoized: each output type is built once and shared per container. Check `Provide` errors at registration; `Invoke` wraps the constructor's error with the dependency path that triggered it.

   *Done when: every dependency is provided and no registration error is ignored.*

3. **Group parameters at 4+ dependencies.** Embed `dig.In` and tag fields `name:"..."`, `optional:"true"`, `group:"..."` — call sites stay readable and adding a dependency becomes a one-line change instead of a signature break.

   *Done when: no constructor with 4+ dependencies takes them as bare parameters.*

4. **Return several values with `dig.Out`.** One constructor produces multiple named or grouped outputs by embedding `dig.Out` and tagging its result fields.

   *Done when: every multi-output constructor uses a result struct with name/group tags.*

5. **Disambiguate collisions with `dig.Name`.** Two providers of the same type collide. Register with `dig.Name("primary")` / `dig.Name("readonly")`, consumed via matching `name:"..."` fields.

   *Done when: no two providers compete for the same type without a name.*

6. **Aggregate with value groups.** Many providers, one consumer slice — typical for HTTP handlers, health checks, migrations. Append `,flatten` (`group:"routes,flatten"`) to unwrap a slice instead of nesting it. Group order is **not guaranteed** — if order matters, provide an explicit ordered slice from a single constructor.

   *Done when: every many-to-one wiring uses a group, and ordered cases provide an explicit slice.*

7. **Expose interfaces with `dig.As`.** Register a concrete constructor and expose it under one or more interfaces without a separate adapter: `c.Provide(NewPostgresDB, dig.As(new(Database), new(io.Closer)))` — consumers depend on the interfaces while the concrete type stays hidden.

   *Done when: consumers depend on interfaces, not concrete types.*

8. **Validate the graph eagerly.** Call `c.Invoke` against the composition root in CI to surface missing providers at boot time, not at first request. `dig.DryRun(true)` validates without executing constructors; `dig.DeferAcyclicVerification()` speeds up startup; `dig.RecoverFromPanics()` turns panics into `dig.PanicError`.

   *Done when: a boot-time Invoke succeeds in CI and missing providers fail fast.*

## Steps — review or audit

1. **Find the container.** It belongs in `main()`, not injected into services. *Done when: no parameter or struct field is a `*dig.Container`.*
2. **Check constructor errors.** Every `Provide`/`Invoke` error is handled; constructors return errors rather than panicking. *Done when: no registration error is silently dropped.*
3. **Check type collisions.** The same type provided twice without `Name` or `Out` grouping is a wire-time error. *Done when: each type has one provider, named where ambiguous.*
4. **Check `init()` side effects.** Constructors do work after the graph is built; `init()` stays empty. *Done when: no construction happens outside the graph.*
5. **Check group ordering.** Groups are unordered; ordered consumers get explicit slices. *Done when: no ordered concern (middleware chain, migration sequence) relies on group order.*

## Reference

### dig vs fx

| Concern | dig | fx |
| --- | --- | --- |
| DI container | ✅ `dig.New()` | ✅ (embedded) |
| Lifecycle hooks | ❌ | ✅ `fx.Lifecycle` OnStart/OnStop |
| Module system | ❌ | ✅ `fx.Module` with scoped decorators |
| Signal-aware run loop | ❌ | ✅ `app.Run()` blocks on SIGINT/SIGTERM |
| Structured event logging | ❌ | ✅ `fx.WithLogger` / `fxevent` |
| Startup/shutdown timeout | ❌ | ✅ `fx.StartTimeout` / `fx.StopTimeout` |

**Choose dig** when you need the wiring graph only: CLI tools, libraries exposing a container to callers, test harnesses, or embedding DI into an existing app that manages its own lifecycle. **Choose fx** for long-running services — lifecycle and signal handling are non-negotiable there.

### Container options

`dig.DeferAcyclicVerification()` (faster startup), `dig.RecoverFromPanics()` (turn panics into `dig.PanicError`), `dig.DryRun(true)` (validate without invoking).

### dig.In / dig.Out

```go
type HandlerParams struct {
    dig.In

    Logger *zap.Logger
    DB     *sql.DB
    Cache  *redis.Client  `optional:"true"`           // zero value if not provided
    DBRO   *sql.DB        `name:"readonly"`           // named dependency
    Routes []http.Handler `group:"routes"`            // value group
}

type ConnResult struct {
    dig.Out

    ReadWrite *sql.DB `name:"primary"`
    ReadOnly  *sql.DB `name:"readonly"`
}
```

### Value groups

```go
type RouteResult struct {
    dig.Out
    Handler http.Handler `group:"routes"`
}

func NewUserHandler(db *sql.DB) RouteResult { /* ... */ }
func NewPostHandler(db *sql.DB) RouteResult { /* ... */ }

type ServerParams struct {
    dig.In
    Routes []http.Handler `group:"routes"`
}
```

### dig.As

```go
c.Provide(NewPostgresDB, dig.As(new(Database), new(io.Closer)))
// Consumers ask for Database or io.Closer; *PostgresDB stays hidden.
```

### Full application shape

```go
func main() {
    c := dig.New()
    must(c.Provide(NewConfig))
    must(c.Provide(NewLogger))
    must(c.Provide(NewDatabase))
    must(c.Provide(NewServer))

    err := c.Invoke(func(srv *http.Server) error {
        return srv.ListenAndServe()
    })
    if err != nil {
        log.Fatal(err)
    }
}
```

dig has **no built-in lifecycle**. If you need OnStart/OnStop hooks, signal handling, and graceful shutdown, use fx — see `go-uber-fx`.

- **[Advanced](./references/advanced.md)** — Decorate, scopes, optional deps, error helpers, Visualize, full Quick Reference
- **[Recipes](./references/recipes.md)** — HTTP server with route group, two databases, request scopes, decorators, dry-run validation
- **[Testing](./references/testing.md)** — per-test containers, `Decorate` overrides, graph validation in CI, asserting wire-time errors

## Watch for

| Mistake | Fix |
| --- | --- |
| Passing the container into services | The container belongs to `main()`. Inject the typed dependencies a service needs; otherwise tests need to build a real container |
| Two providers for the same type without `Name` | dig errors at `Provide` time. Name them, or merge into a single provider returning a `dig.Out` result struct |
| Ignoring `Provide` errors | Wrap each `Provide` with a `must` helper. A silent registration error becomes a missing-type error far later |
| Using groups when ordering matters | Groups are unordered. If order matters (middleware chain, migration sequence), provide an explicit ordered slice with one constructor |
| Constructors with side effects on import | Keep `init()` empty — start work only inside the constructor, after the graph is built |

## Cross-references

- → See `go-uber-fx` for application lifecycle, modules, and signal-aware Run() built on top of dig
- → See `go-dependency-injection` for DI concepts and library comparison
- → See `samber-do` for a generics-based alternative without reflection
- → See `go-google-wire` for compile-time DI (no runtime container)
- → See `go-structs-interfaces` for interface design patterns
- → See `go-testing` for general testing patterns

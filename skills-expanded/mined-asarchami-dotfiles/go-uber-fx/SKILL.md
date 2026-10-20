---
name: go-uber-fx
description: "Go uber-go/fx — application wiring with lifecycle: fx.New/Provide/Invoke, fx.Lifecycle OnStart/OnStop hooks, fx.Module scoped decorators, fx.Annotate (name/group/As), value groups, fx.Supply/Replace/Decorate, signal-aware Run(), fxtest. Apply when using or adopting uber-go/fx, the codebase imports `go.uber.org/fx`, or wiring long-running services. For raw DI without lifecycle, see `go-uber-dig`."
license: MIT
---

# Go Uber Fx

**Leading word: lifecycle.** fx wires a dependency graph and gives it a lifecycle — boot order, graceful shutdown, and structured logging for long-running services. The discipline: push work into hooks instead of `init()`, keep OnStart non-blocking, and treat modules as the unit of reuse.

## Steps — wire an app

1. **Compose the app.** `fx.New(fx.Provide(...), fx.Invoke(...))` then `app.Run()` — Run blocks on SIGINT/SIGTERM, then fires OnStop hooks. Boot stages: `fx.New` validates types (constructors do not run); `app.Start(ctx)` runs each `fx.Invoke` and fires OnStart hooks in topological order; main blocks on `app.Done()`; `app.Stop(ctx)` fires OnStop hooks in reverse order. Default timeout is **15 seconds** — override with `fx.StartTimeout` / `fx.StopTimeout`.

   *Done when: the app is one composition with a single `Run()`, and boot ordering follows graph topology.*

2. **Register providers and triggers.** `fx.Provide` registers constructors (lazy); `fx.Invoke` is the trigger — without an Invoke (directly or transitively) referencing a type, its constructor never runs. Add at least one Invoke per app.

   *Done when: every type's constructor is reachable from an Invoke.*

3. **Push work into lifecycle hooks.** Inject `fx.Lifecycle` and append `fx.Hook` entries. Constructors return quickly; long-running work (HTTP servers, workers) belongs in `OnStart`, shutdown in `OnStop`. `fx.StartHook` / `fx.StopHook` / `fx.StartStopHook` adapt simpler signatures.

   *Done when: no constructor blocks or owns long-running goroutines; hooks do.*

4. **Keep OnStart non-blocking.** Both callbacks receive a context bounded by `StartTimeout`/`StopTimeout` — respect `ctx.Done()`. Blocking work goes in a goroutine inside OnStart; a blocking hook hangs the rest of boot and dependent hooks never fire.

   *Done when: every OnStart returns promptly and every hook honors cancellation.*

5. **Group parameters and results.** `fx.In`/`fx.Out` (re-exports of dig's) handle 4+ dependencies and `name`/`group`/`optional` tags. Prefer `fx.Annotate` for tags and interface bindings — `fx.Annotate(NewDB, fx.ResultTags(\`name:"primary"\`))`, `fx.Annotate(NewPostgresDB, fx.As(new(Database)))` — so constructors stay reusable outside fx.

   *Done when: no constructor has 4+ bare parameters, and tags are applied via Annotate rather than an `fx.Out` struct.*

6. **Aggregate with value groups.** Many constructors, one consumer slice (`group:"routes"`). Append `,flatten` to unwrap a slice instead of nesting it. Order is **not guaranteed** — provide an explicit ordered slice when sequence matters.

   *Done when: every many-to-one wiring uses a group and ordered cases are explicit.*

7. **Organize into modules.** `fx.Module("database", fx.Provide(...), fx.Decorate(...))` groups providers, invokes, and decorators under a name. Decorators scope to the module and its children only — a logger renamed inside a module appears renamed only for code inside it; a top-level `fx.Decorate` is global. Treat each module as a small library liftable into another app; its public surface is the types it Provides.

   *Done when: the graph decomposes into named modules and no decorator leaks beyond its scope.*

8. **Use Supply for pre-built values.** `fx.Supply(cfg)` for config and command-line flags instead of a no-op constructor; `fx.Replace` swaps implementations; `fx.Decorate` wraps types at module or app scope.

   *Done when: pre-built values are Supplied, and Replace/Decorate are scoped intentionally.*

9. **Validate the graph in CI.** Boot under `fx.New(...).Err()` to catch missing providers and cycles before deploy.

   *Done when: a CI boot check fails on missing providers and cycles.*

## Steps — review or audit

1. **Trace boot ordering.** Constructors run lazily in topology order; OnStart/OnStop run in forward/reverse hook order. *Done when: boot and shutdown order match graph topology, not source order.*
2. **Check hook discipline.** OnStart returns promptly; blocking work sits in a goroutine; `ctx.Done()` is respected. *Done when: no hook blocks boot or ignores cancellation.*
3. **Check for side-effect constructors.** Work belongs in hooks — constructors may run lazily and concurrently, so they stay cheap and pure-ish. *Done when: no constructor launches goroutines or does I/O.*
4. **Verify decorator scope.** Module decorators stay within their module and children. *Done when: no decorator escapes its intended scope.*
5. **Check Provide vs Supply.** No no-op constructors wrapping pre-built values. *Done when: pre-built values are Supplied.*
6. **Confirm an Invoke exists.** Without one, constructors never run. *Done when: at least one Invoke (direct or transitive) references the graph.*

## Reference

### fx vs dig

| Concern | dig | fx |
| --- | --- | --- |
| DI container | ✅ `dig.New()` | ✅ (embedded) |
| Lifecycle hooks | ❌ | ✅ `fx.Lifecycle` OnStart/OnStop |
| Module system | ❌ | ✅ `fx.Module` with scoped decorators |
| Signal-aware run loop | ❌ | ✅ `app.Run()` blocks on SIGINT/SIGTERM |
| Structured event logging | ❌ | ✅ `fx.WithLogger` / `fxevent` |
| Startup/shutdown timeout | ❌ | ✅ `fx.StartTimeout` / `fx.StopTimeout` |

**Choose fx** for long-running services (HTTP servers, workers, daemons). **Choose raw dig** when you need wiring without a framework — CLI tools, libraries exposing a container, test harnesses, or embedding DI into an app that manages its own lifecycle.

### Lifecycle hook

```go
func NewHTTPServer(lc fx.Lifecycle, log *zap.Logger, cfg *Config) *http.Server {
    srv := &http.Server{Addr: cfg.Addr}

    lc.Append(fx.Hook{
        OnStart: func(ctx context.Context) error {
            ln, err := net.Listen("tcp", srv.Addr)
            if err != nil { return err }
            go srv.Serve(ln)         // blocking work in a goroutine
            return nil
        },
        OnStop: func(ctx context.Context) error {
            return srv.Shutdown(ctx)
        },
    })
    return srv
}
```

### fx.Annotate

```go
fx.Provide(
    fx.Annotate(NewPrimaryDB, fx.ResultTags(`name:"primary"`)),
    fx.Annotate(NewPostgresDB, fx.As(new(Database))),    // expose interface
    fx.Annotate(NewUserHandler,
        fx.As(new(http.Handler)),
        fx.ResultTags(`group:"routes"`),
    ),
)
```

### fx.Module with scoped decorator

```go
var DatabaseModule = fx.Module("database",
    fx.Provide(NewConnection, NewUserRepository),
    fx.Decorate(func(log *zap.Logger) *zap.Logger {
        return log.Named("db")
    }),
)

func main() {
    fx.New(
        fx.Provide(NewConfig, NewLogger),
        DatabaseModule,
        HTTPModule,
    ).Run()
}
```

- **[Advanced](./references/advanced.md)** — Supply/Replace/Decorate, optional deps, custom event logging, manual lifecycle, full Quick Reference
- **[Recipes](./references/recipes.md)** — full HTTP service with database/metrics, background workers with graceful drain, multiple impls of the same interface, manual lifecycle for CLI embedding
- **[Testing](./references/testing.md)** — fxtest patterns, `fx.Replace`, `fx.Populate`, isolated lifecycle tests, CI graph validation

## Watch for

| Mistake | Fix |
| --- | --- |
| Long-running work directly in OnStart | Spawn a goroutine inside OnStart; the hook itself must return quickly so dependent hooks can run |
| `fx.Provide` something that should be `fx.Supply` | Pre-built values (config, secrets) belong in `fx.Supply` — clearer and avoids a no-op constructor |
| Module decorator leaking to siblings | Decorate inside `fx.Module(...)` — decorators flow only to descendants. A top-level `fx.Decorate` is global |
| Group order assumed | Groups are unordered. If order matters, provide an ordered slice from one constructor |
| Constructors with side effects | Side effects belong in OnStart — constructors should be cheap and pure-ish, since they may run concurrently and lazily |
| Forgotten `fx.Invoke` | Without an Invoke (or downstream consumer), constructors never run. Add at least one Invoke per app |

## Cross-references

- → See `go-uber-dig` for the underlying container, `dig.In`/`dig.Out`, and DI without lifecycle
- → See `go-dependency-injection` for DI concepts and library comparison
- → See `samber-do` for a generics-based alternative without reflection
- → See `go-google-wire` for compile-time DI (no runtime container)
- → See `go-context` for context propagation in OnStart/OnStop hooks
- → See `go-structs-interfaces` for interface design patterns
- → See `go-testing` for general testing patterns

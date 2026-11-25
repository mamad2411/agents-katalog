---
name: samber-do
description: "inject — dependency injection in Go with samber/do/v2: register services via provider functions, group modules into packages, resolve by interface, manage lifecycle and scopes, wire graceful shutdown. Use when wiring an application container, refactoring manual DI, organizing services into scopes/modules, or testing services against a cloned container."
license: MIT
---

# samber/do

**Leading word: inject.** Dependency injection wires each service exactly once at the composition root and lets the injector resolve it by interface everywhere else. The discipline: register services through provider functions, depend on interfaces not concrete types, and treat provider errors as first-class failures.

## Steps — wire the container

1. **Create the injector at the composition root.** `injector := do.New()` lives in `main` and tests. Services never construct or store the injector — they receive it as a parameter inside provider functions.
   *Done when: only main and tests construct injectors; no service holds the injector as a field.*
2. **Register every service with a provider function.** Signature `func(i do.Injector) (T, error)`. Choose the lifecycle per service: lazy (default), `do.ProvideValue` for pre-created config, `do.ProvideTransient` for per-request state, `do.Eager` for startup-critical work.
   *Done when: every service is registered via a provider function with a stated lifecycle.*
3. **Depend on interfaces, resolve as interfaces.** Register the concrete type and resolve with `do.MustInvokeAs[Database]` — implicit aliasing keeps one binding per service.
   *Done when: providers depend on interfaces, and no service resolves a concrete type it can avoid.*
4. **Group registrations by module.** Each module exports a `do.Package(do.Lazy(...), ...)`; compose modules at the root with `do.New(infrastructure.Package, service.Package)`.
   *Done when: registration is grouped per module and the root `do.New` lists only packages.*
5. **Make provider errors first-class.** `do.Invoke` returns `(T, error)`; reach for `do.MustInvoke` only when failure is impossible. A silently-failing provider creates a broken service that crashes later in unexpected places.
   *Done when: every fallible resolution checks its error and every MustInvoke has a justification.*
6. **Wire shutdown and signals.** Start the server from a resolved dependency, then `injector.ShutdownOnSignalsWithContext(ctx, os.Interrupt)`. Keep request-scoped services inside scopes so they can't leak.
   *Done when: the app shuts down gracefully and request-scoped services die with their scope.*

## Steps — test or review

1. **Clone the container per test.** Build a fresh `do.New()` in each test and override only the dependencies under test — see the testing reference — instead of mocking globals.
   *Done when: each test runs against an isolated container and overrides exactly what it exercises.*
2. **Audit existing wiring.** Every `MustInvoke` has a stated confidence, provider errors are handled, no service stores the injector, and dependency trees stay shallow (3–4 levels).
   *Done when: the audit passes with no unexplained MustInvoke or injector-storing service.*

## Reference

### Provider function

```go
type Provider[T any] func(i Injector) (T, error)
```

### Register and resolve

```go
do.Provide(injector, func(i do.Injector) (Database, error) { return &PostgreSQLDatabase{}, nil })
do.ProvideValue(injector, &Config{Port: 8080})                 // pre-created value
do.ProvideTransient(injector, func(i do.Injector) (*Logger, error) { return &Logger{}, nil })
do.Provide(injector, do.Eager(&Config{Port: 8080}))            // created immediately

db, err := do.Invoke[Database](injector)                        // error-propagating
db := do.MustInvoke[Database](injector)                         // panics on error
db := do.MustInvokeAs[Database](injector)                       // resolve by interface (implicit aliasing)
```

### Named services

```go
do.ProvideNamed(injector, "primary-db", func(i do.Injector) (*Database, error) { return &Database{}, nil })
mainDB := do.MustInvokeNamed[*Database](injector, "primary-db")
```

### Package organization

```go
var Package = do.Package(
    do.Lazy(func(i do.Injector) (*postgres.DB, error) {
        cfg := do.MustInvoke[*Config](i)
        return postgres.Connect(cfg.DatabaseURL)
    }),
)

injector := do.New(infrastructure.Package, service.Package)
```

### Registration

| Function | Purpose |
| --- | --- |
| `do.Provide[T]()` | Register lazy service (default) |
| `do.ProvideNamed[T]()` | Register named lazy service |
| `do.ProvideValue[T]()` | Register pre-created value |
| `do.ProvideNamedValue[T]()` | Register named value |
| `do.ProvideTransient[T]()` | Register new instance each time |
| `do.ProvideNamedTransient[T]()` | Register named transient service |
| `do.Package()` | Group service registrations |

### Invocation

| Function | Purpose |
| --- | --- |
| `do.Invoke[T]()` | Get service (with error) |
| `do.InvokeNamed[T]()` | Get named service |
| `do.InvokeAs[T]()` | Get first service matching interface |
| `do.InvokeStruct[T]()` | Inject into struct fields using tags |
| `do.MustInvoke[T]()` | Get service (panic on error) |
| `do.MustInvokeNamed[T]()` | Get named service (panic on error) |
| `do.MustInvokeAs[T]()` | Get service by interface (panic on error) |
| `do.MustInvokeStruct[T]()` | Inject into struct (panic on error) |

- **[Advanced](./references/advanced.md)** — scopes, lifecycle management, struct injection, debugging
- **[Testing](./references/testing.md)** — cloning, overrides, mocks

## Watch for

| Mistake | Fix |
| --- | --- |
| Importing samber/do v1 | Install and import `github.com/samber/do/v2` |
| Accessing the injector deep in the call tree | Keep the injector at the composition root |
| Storing the injector in a service struct | Pass it as a provider parameter only |
| Silently failing provider | Return errors from providers and check them on resolve |
| `MustInvoke` where the service may be absent | Use `Invoke` and handle the error |
| Concrete-to-concrete coupling | Resolve by interface (implicit aliasing) |
| Ignoring scope lifecycle | Scope request-scoped services so they are released |

## Cross-references

- → See `go-dependency-injection` for DI concepts, library comparison, and when to adopt a container
- → See `go-structs-interfaces` for accept-interfaces / return-structs design
- → See `go-testing` for general testing patterns

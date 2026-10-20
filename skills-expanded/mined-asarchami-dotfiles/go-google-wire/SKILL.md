---
name: go-google-wire
description: "Go google/wire — compile-time DI codegen: providers, provider sets, wire.Build injectors with //go:build wireinject, wire.Bind interface bindings, wire.Struct/Value/InterfaceValue/FieldsOf, named-type disambiguation, generated wire_gen.go. Apply when using or adopting google/wire, the codebase imports `github.com/google/wire`, or wiring an application graph at compile time. For runtime reflection DI, see `go-uber-dig`."
license: MIT
---

# Go Google Wire

**Leading word: wire.** `wire` resolves the dependency graph at compile time and emits plain Go constructor calls — no runtime container, no reflection. The discipline: declare providers and injectors, run `wire ./...`, and let the compiler catch missing dependencies before first request.

Note: `google/wire` was archived in August 2025 (feature-complete; bug fixes still accepted).

## Steps — wire a graph

1. **Write providers.** A provider is any Go function — inputs are dependencies, outputs are provided types. Three return forms: `T`, `(T, error)`, `(T, func(), error)` where the third form carries a cleanup chained in reverse order.

   *Done when: every dependency is produced by exactly one provider with the correct return form.*

2. **Group into sets.** `wire.NewSet` groups providers for reuse; sets can reference other sets. Keep sets small — library sets expose a stable surface: adding required inputs or removing outputs breaks downstream injectors. One set per package is a useful default.

   *Done when: each package exposes one stable provider set.*

3. **Declare injectors.** The injector file declares the init function with `//go:build wireinject` as its first line; wire generates the body into `wire_gen.go`. Without the tag both files define the same function — duplicate-symbol compile error. `panic(wire.Build(...))` is an alternative when a dummy return is inconvenient.

   *Done when: every injector carries the build tag and its generated body compiles.*

4. **Bind interfaces explicitly.** Wire forbids implicit interface satisfaction — declare `wire.Bind(new(UserStore), new(*UserRepo))` so the graph stays unambiguous when multiple types implement the same interface.

   *Done when: every injected interface has a `wire.Bind` in its provider set.*

5. **Fill structs and values.** `wire.Struct(new(Server), "*")` injects struct fields from the graph (tag `wire:"-"` to exclude); `wire.Value` for constant expressions (no fn calls/channels); `wire.InterfaceValue` for interface-typed literals; `wire.FieldsOf` promotes struct fields as graph nodes.

   *Done when: no manual constructor exists where `wire.Struct` would do, and fields are injected selectively.*

6. **Disambiguate duplicate types.** Wire forbids two providers for the same type. Wrap the underlying type in distinct named types (`type PrimaryDSN string`, `type ReplicaDSN string`) so each has exactly one provider.

   *Done when: no two providers return the same type.*

7. **Regenerate after every change.** Run `wire ./...` after each constructor signature change; add `//go:generate go run github.com/google/wire/cmd/wire` to injector files so `go generate ./...` also works; commit `wire_gen.go` so CI builds stay in sync.

   *Done when: `wire ./...` is clean and `wire_gen.go` is committed and regenerated after every graph change.*

8. **Guard cleanups.** `InitApp` returns `(*App, func(), error)`; wire chains cleanups in reverse order and runs only already-built cleanups if construction fails midway. On construction error wire returns a nil cleanup — guard with `if cleanup != nil`.

   *Done when: every cleanup call is nil-guarded and reverse-order chaining is generated.*

## Steps — review or audit

1. **Regenerate and diff.** Run `wire ./...` and check `wire_gen.go` — any manual edit is overwritten on every run. *Done when: regeneration produces no diff.*
2. **Check injector tags.** Every injector file starts with `//go:build wireinject`. *Done when: no injector stub compiles into the binary.*
3. **Check for duplicate providers.** The same type provided twice is a graph error. *Done when: every type has exactly one provider, named types used where needed.*
4. **Verify interface bindings.** Every injected interface has a `wire.Bind`. *Done when: no interface is injected implicitly.*
5. **Check cleanup paths.** `(T, func(), error)` providers chain in reverse order and call sites nil-guard. *Done when: every cleanup is guarded and chained.*

## Reference

### wire vs runtime DI

| Concern | wire | dig / fx / samber/do |
| --- | --- | --- |
| Resolution | Compile time (codegen) | Runtime (reflection) |
| Error detection | `wire ./...` fails | First `Invoke`/startup |
| Runtime container | None — plain Go calls | Present |
| Lifecycle hooks | Not built in | fx: OnStart/OnStop |
| Generated files | `wire_gen.go` (committed) | None |

For lifecycle, lazy loading, and a full matrix see `go-dependency-injection`.

### Providers

```go
func NewConfig() *Config                          { return &Config{Addr: ":8080"} }
func NewDB(cfg *Config) (*sql.DB, error)          { return sql.Open("postgres", cfg.DSN) }
func NewRedis(cfg *Config) (*redis.Client, func(), error) {
    c := redis.NewClient(&redis.Options{Addr: cfg.RedisAddr})
    return c, func() { c.Close() }, nil // cleanup chained in reverse order
}
```

### Injector shape

```go
//go:build wireinject

package main

// Wire generates the body of this function.
func InitApp() (*App, func(), error) {
    wire.Build(InfraSet, ServiceSet, NewApp)
    return nil, nil, nil // replaced by codegen
}
```

### Struct providers and values

```go
wire.Struct(new(Server), "Logger", "DB")   // inject named fields
wire.Struct(new(Server), "*")              // inject all non-excluded fields
wire.Value(Foo{X: 42})                     // constant expression (no fn calls / channels)
wire.InterfaceValue(new(io.Reader), os.Stdin)
wire.FieldsOf(new(Config), "DSN", "Addr")  // promote struct fields as graph nodes
```

### Codegen workflow

```bash
go install github.com/google/wire/cmd/wire@latest
wire ./...           # regenerate all injectors in the module
wire check ./...     # validate graph without regenerating (fast CI check)
```

- **[Advanced](./references/advanced.md)** — `wire:"-"` exclusion tag, `wire.FieldsOf` details, cleanup chains, multiple injectors, set nesting, error catalogue, codegen flags
- **[Recipes](./references/recipes.md)** — full example with per-package sets, multi-injector build, cleanup-heavy graph, CLI embedding
- **[Testing](./references/testing.md)** — test injectors swapping fakes, CI stale-check for `wire_gen.go`

## Watch for

| Mistake | Fix |
| --- | --- |
| Editing `wire_gen.go` manually | Never edit it. Change providers or injectors and re-run `wire ./...` |
| Missing `//go:build wireinject` | Add the tag as the very first line of every injector file |
| Two providers returning `*sql.DB` | Wrap with named types (`type PrimaryDSN string`) |
| Injecting an interface without `wire.Bind` | Add `wire.Bind(new(MyInterface), new(*MyImpl))` to the provider set |
| Forgetting to re-run `wire ./...` after changes | Run wire before `go build`; add it to `go generate` or a Makefile target |
| Calling `cleanup()` without guarding for nil | Wire returns nil cleanup on construction error; guard with `if cleanup != nil { defer cleanup() }` |
| Fat injectors with dozens of `wire.Build` arguments | Keep one function per file and delegate to per-package sets |

## Cross-references

- → See `go-dependency-injection` for DI concepts and library comparison
- → See `go-uber-dig` for runtime reflection-based DI without lifecycle
- → See `go-uber-fx` for runtime DI with lifecycle hooks, modules, and signal-aware Run()
- → See `samber-do` for generics-based DI without reflection
- → See `go-structs-interfaces` for interface design patterns
- → See `go-testing` for general testing patterns

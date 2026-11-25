---
name: google-go-style
description: Use when writing, reviewing, or refactoring Go code; when handling errors (fmt.Errorf, %w, sentinel, errors.Is, errors.As); when deciding between panic, error return, and log.Fatal; when writing tests (table-driven, t.Helper, t.Fatal vs t.Error, goroutines); when designing API surface (option struct, variadic options, channel direction, context); when naming functions, methods, packages, receivers, or test doubles; when laying out packages and imports; when initializing variables or building strings.
---

# Google Go Style — Skill

_Derived from the [Google Go Style Guide](https://google.github.io/styleguide/go/), © Google LLC, licensed [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/). This skill is a derivative digest, not a verbatim reproduction._

Codifies the [Google Go Style Guide](https://google.github.io/styleguide/go) (canonical + normative + best-practices) into actionable rules.

The full guide is large. This file holds only what should be in your head **on every Go change**. For deeper rules, load the matching `references/*.md`. For unusual situations, WebFetch the source — the guide is normative.

## Quick Rules

Apply on every line of Go you write or review.

### Naming

- **No `Get` prefix on getters.** `User()`, not `GetUser()`. Exception: the underlying concept *is* "get" (HTTP GET).
- **Don't repeat the package name** in identifiers. `bytes.Buffer`, not `bytes.BytesBuffer`. `widget.New`, not `widget.NewWidget`.
- **Receiver names: 1–2 letters, abbreviation of the type, consistent across all methods.** Never `this`, `self`, `me`, or `_` (unless unused). `func (c *Config)`, not `func (config *Config)`.
- **Initialisms keep one case.** `URL`, `ID`, `HTTP`, `DB`. Exported: `UserID`, `ServeHTTP`. Unexported: `userID`, `urlPath`. Never `Url`, `Id`, `Http`.
- **Test doubles end in `Stub` / `Fake` / `Spy` / `Mock`** (or describe behaviour: `AlwaysCharges`, `AlwaysDeclines`).
- **No `util` / `common` / `helper` / `model` package names.** They invite import renames at every call site. Name by what the package *provides*.
- **No underscores in identifiers** (except `*_test.go` test/benchmark/example names, and packages imported only by generated code).
- **Local variable scope ↔ name length.** `i`, `c`, `db` for tight loops; `userCount`, `pollInterval` for file scope. Don't drop letters to save typing (`Sandbox`, not `Sbx`).

### Errors

- **`fmt.Errorf("doing X: %w", err)`** — wrap with `%w` *at the end*, so the chain prints newest→oldest as `outer: middle: inner`.
- **`%w` only when callers need `errors.Is` / `errors.As`** on the underlying error. Otherwise use `%v`.
- **`%w` at the start** is for **sentinel** wrappers only: `fmt.Errorf("%w: invalid header", ErrParse)`. Category first, details after.
- **Sentinel name: `ErrFoo`** at package level: `var ErrNotFound = errors.New("not found")`.
- **Don't duplicate context** the underlying error already carries. `os.Open` errors already include the path — `fmt.Errorf("could not open settings.txt: %v", err)` is wrong; use a higher-level annotation: `fmt.Errorf("launch codes unavailable: %v", err)`.
- **Don't add bare "failed: %v" wrappers.** They add no information; just `return err`.
- **Either log it or return it — not both.** Pick one. Letting the caller log avoids spam.
- **Error strings: lowercase, no trailing punctuation, no `\n`.** `fmt.Errorf("something bad happened")`, not `"Something bad happened."`.
- **Cross-process boundaries (gRPC/RPC): use canonical codes** via `status.Errorf(codes.X, ...)` rather than wrapping internal errors raw with `%w`.
- **`error` is the last return value.** A function taking `context.Context` should usually return `error`.

For more, see `references/errors.md`.

### Panics

- **Don't panic for normal error handling.** Return `error` and multiple return values.
- **`log.Fatal` over `panic`** for terminal conditions in `main` / `init`. Fatal does not run deferred functions; that's the point.
- **Panics never cross package boundaries** in public APIs. Convert to `error` at the API edge with a top-level `defer recover()` that re-panics on unknown payloads.
- **`MustX` is for package-level vars and tests only.** `MustParse`, `template.Must`. Not for runtime user input.
- **Don't `recover()` to suppress crashes.** Corrupted state propagates further; better is monitoring + crash + fix.
- **`panic("unreachable")` after `log.Fatalf`** is the idiom — the compiler doesn't know `Fatal` doesn't return.

For more, see `references/panics.md`.

### Tests

- **No assertion libraries / helpers** (`assert.Equal`, `require.NotNil`). Use `if got != want { t.Errorf(...) }`. For complex types: `cmp.Equal` / `cmp.Diff` from `go-cmp`.
- **`t.Error` over `t.Fatal`** by default — keep going, report all failures in one run. `t.Fatal` only when continuing is meaningless (setup failed, cascading errors would mislead).
- **Inside `t.Run` subtests: use `t.Fatal`** to skip just that case. Outside subtests in a table loop: `t.Error` + `continue`.
- **NEVER call `t.Fatal` (`FailNow`, `Fatalf`, `SkipNow`) from a goroutine other than the test's own.** Use `t.Error` from worker goroutines; `t.Fatal` only after `wg.Wait()` from the main goroutine.
- **Table-driven tests use *named* struct fields**, not positional: `{name: "empty", input: "", want: ""}`.
- **Test helpers that fail setup call `t.Helper()` + `t.Fatalf`.** This makes the failure point to the *test* line, not the helper line.
- **Failure message format: `YourFunc(%v) = %v, want %v`** — function name, inputs, got, want, in that order.

For more, see `references/tests.md`.

### Variables and strings

- **`:=` for non-zero init, `var x T` for zero values.** `i := 42`, but `var coords Point` (not `coords := Point{}`).
- **`var t []string`, not `t := []string{}`** for empty slices. Empty slice and nil slice behave the same for `len`, `cap`, `range`, `append`.
- **`new(T)` vs `&T{}`**: both are fine for zero values; `new` reads as "zero value placeholder", `&T{}` is more common when fields are filled.
- **Never `==` on `nil` for slices.** Use `len(s) == 0`. APIs must not distinguish nil from empty.
- **Strings: `+` for 2–3 short literals; `fmt.Sprintf` for formatting; `strings.Builder` in loops; `text/template` for templates.**
- **Pre-size with `make([]T, 0, n)` / `make(map[K]V, n)`** only when `n` is known and the code is performance-sensitive. Default to zero-init.
- **No shadowing in nested scopes.** `if *x { ctx, cancel := ...; }` shadows `ctx` outside the `if`. Use `ctx, cancel = ...` with `=` and `var cancel func()` declared above.

For more, see `references/strings-and-vars.md`.

### API design

- **`context.Context` is the first parameter.** `func F(ctx context.Context, ...) error`. Even in test helpers.
- **Never store `context.Context` in a struct.** Pass it through every method that needs it.
- **No global mutable state.** Pass dependencies through constructors / function parameters (DI).
- **Take interfaces, return concrete types.** The consumer of an interface defines it, not the implementer.
- **Channel direction in signatures.** `<-chan T` for receive-only, `chan<- T` for send-only.
- **Many parameters → option struct** (call site reads as labelled fields). 3+ optional / API expected to grow → option struct. Don't put `context.Context` in option structs.
- **Variadic functional options (`...Option`)** only when most callers pass nothing, options need parameters, or third parties define options.
- **Avoid `*string`, `*io.Reader` parameters** "to save bytes". Pass values; use pointers for large structs and protobuf messages.

For more, see `references/api-design.md`.

### Documentation

- **Doc comments are full sentences starting with the symbol's name.** `// Encode writes the JSON encoding of req to w.`
- **Document WHY, not WHAT.** The code already says what.
- **Document significant sentinel errors and error types** the function returns.
- **Document cleanup contracts** (`Close`, `Stop`, deferred resources).
- **Document concurrency-safety only when non-obvious** (read-only methods are assumed safe; mutating ones are assumed unsafe — say so when that doesn't hold).
- **Don't document that `ctx.Done` cancels the function** — that's the contract of `context.Context`.

For more, see `references/documentation.md`.

### Package layout

- **`internal/` for packages not part of the public API.**
- **Avoid `util` / `common` / `helper`.** Name by domain.
- **Imports grouped: stdlib / third-party / proto / blank-side-effect.** Blank imports only in `main` or tests.
- **No `import .` ever** (in Google codebase).
- **Proto imports get a `pb` suffix**: `foopb "path/to/foo_go_proto"`.

For more, see `references/package-layout.md`.

## Decision Matrices

### `%v` vs `%w` when wrapping an error

| Situation | Choose | Why |
|---|---|---|
| Caller will `errors.Is` / `errors.As` to inspect the chain | `%w` | Preserves type/sentinel through the chain |
| Crossing an external boundary (RPC, IPC, storage); caller wants canonical codes | `%v` (or `status.Errorf`) | Don't leak internal error types over the wire |
| Logging or human-display only; no programmatic inspection | `%v` | `%w` adds chain semantics nobody uses |
| Same error is logged here AND returned upward | `%v` | Wrapping a logged-then-returned error confuses the chain |
| Sentinel categorisation first (`ErrParse`-style) | `%w` at **start**: `"%w: detail"` | Reader sees the category first |
| Adding context around a wrapped error (the common case) | `%w` at **end**: `"context: %w"` | Chain prints newest→oldest naturally: `outer: middle: inner` |
| Underlying error already carries this info | nothing — `return err` | Wrapping without adding info is noise |
| Just propagating without analysis | nothing — `return err` | Don't wrap for the sake of wrapping |

### Function arguments: positional vs option struct vs variadic options

| Situation | Choose | Why |
|---|---|---|
| ≤ 3 parameters, all required, all distinct types | Positional args | Smallest mechanism |
| Many parameters, most callers set most of them | Option struct (last param) | Self-documenting field names; grows without breaking call sites |
| Many parameters, most callers set none | Variadic options (`...Option`) | Zero overhead at simple call sites |
| Options need failure validation | Variadic options returning `error` | Can't validate in struct construction |
| Third-party packages must define options | Variadic options with exported `Option` type | Struct fields can't be extended |
| Same option set used by multiple functions | Option struct | Reuse + share + write helpers on the struct |
| `context.Context` | First positional arg, **never** in option struct | Convention |

### `panic` vs `log.Fatal` vs `error` return

| Situation | Choose | Why |
|---|---|---|
| Library detects normal failure | `error` return | Caller decides |
| Library detects an "impossible" invariant violation | `error` return *or* `log.Fatal` | Caller can't recover anyway |
| Bad flag/config in `main` / `init` | `log.Exit` (no stack) | Stack trace useless; user wants the message |
| Internal package consistency check that has been verified by tests | `log.Fatal` | More reliable than `panic` (no defer deadlock risk) |
| Parser internals that always have a matching `recover` at the API edge | `panic` of a private type | Plumbing errors through deep recursion is noise |
| Package-level var initializer needs a value derived from a fallible call | `MustX` (panics) | Init-time only; `init` cannot return errors |
| HTTP handler crashes mid-request | **never** `recover()` to mask it | State is corrupted; let the process crash and restart |

### `t.Error` vs `t.Fatal` vs `t.Errorf` + `continue`

| Situation | Choose |
|---|---|
| Multiple independent assertions in one `Test*`, all should run | `t.Error` / `t.Errorf` for each |
| Setup failure — rest of test cannot proceed | `t.Fatal` / `t.Fatalf` |
| First failure makes subsequent assertions misleading (e.g. encoded ≠ expected, can't decode meaningfully) | `t.Fatalf` then continue with `t.Errorf` |
| Table loop without subtests, this case is broken | `t.Errorf` + `continue` |
| Inside `t.Run(...)` subtest, this case is broken | `t.Fatal` (skips this subtest only) |
| Worker goroutine inside a test | `t.Errorf` only (NEVER `t.Fatal`) |
| Test helper called from main test goroutine | `t.Helper()` + `t.Fatalf` is fine |

### Variable declaration form

| Situation | Choose | Example |
|---|---|---|
| Initializing with a known non-zero value | `:=` | `i := 42` |
| Need a zero value, ready for use | `var x T` | `var coords Point`, `var s []string` |
| Need a `*T` to a zero value | `new(T)` *or* `&T{}` | `msg := new(pb.Bar)` |
| Need a `*T` to a value with fields | `&T{...}` | `c := &Config{Port: 8080}` |
| Empty slice for return / accumulation | `var s []T` | not `s := []T{}` |
| Empty map (must be initialized to write) | `make(map[K]V)` or `map[K]V{}` | nil map can be read but not written |
| Pre-sized slice/map (perf-sensitive, size known) | `make([]T, 0, n)` / `make(map[K]V, n)` | Don't over-pre-allocate |

## Reference Files

Load on demand:

- `references/errors.md` — detailed error structure, wrapping rules, sentinels, RPC boundaries, `errors.Is/As`.
- `references/naming.md` — receivers, initialisms, repetition, test doubles, util-package antipattern, shadowing.
- `references/api-design.md` — option struct vs variadic options, channel direction, DI, interfaces, generics.
- `references/tests.md` — Test funcs vs helpers, table-driven, subtests, goroutines, acceptance testing, `cmp`.
- `references/panics.md` — when allowed (invariants, parsers with recover, `init`), when forbidden, `log.Fatal` vs `log.Exit`.
- `references/documentation.md` — godoc conventions, what to document, what to skip, contexts, errors, cleanup.
- `references/package-layout.md` — package size, file structure, imports, `internal/`, side-effect imports.
- `references/strings-and-vars.md` — concatenation choices, zero values, size hints, `new` vs `&T{}`, shadowing.

## Authoritative Sources

When in doubt, especially for unusual situations, **WebFetch the source section before writing the code**. The Google Go Style Guide is the normative authority — this skill is a digest, not a replacement.

- https://google.github.io/styleguide/go/index — overview, normativity definitions
- https://google.github.io/styleguide/go/guide — **canonical + normative** core principles
- https://google.github.io/styleguide/go/decisions — **normative** detailed decisions
- https://google.github.io/styleguide/go/best-practices — non-normative patterns and discussions

For Go fundamentals not covered here, read [Effective Go](https://go.dev/doc/effective_go).

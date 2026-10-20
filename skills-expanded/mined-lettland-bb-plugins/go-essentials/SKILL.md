---
name: go-essentials
description: Use when writing any Go — naming, errors, modules, generics, file layout, the rules you don't break.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [go]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [go-concurrency, go-testing]
---

# Go Essentials

**Iron Law: handle every error explicitly. No `panic` outside `main`/`init` or unrecoverable invariants.**

**Versions:** Supported `1.25`, `1.26` · Current `1.26` · Next `1.27` — _Latest-2-supported policy; range-over-func stable (1.23+), generic type aliases (1.24), iter shapes refined (1.25/26). Bump module `go` directive to 1.25+ for new projects._

## Naming (non-negotiable)

| Subject               | Rule                                 | ✅                        | ❌                                       |
| --------------------- | ------------------------------------ | ------------------------- | ---------------------------------------- |
| Packages              | short, lowercase, no underscores     | `auth`                    | `authentication`, `auth_pkg`             |
| Exported              | PascalCase                           | `ServeHTTP`               | `serve_http`                             |
| Unexported            | camelCase                            | `userID`                  | `user_id`                                |
| Acronyms              | keep case                            | `URL`, `ID`, `HTTPServer` | `Url`, `Http`                            |
| Receivers             | 1-2 chars, consistent across methods | `func (u *User) X()`      | `func (this *User)`, `func (self *User)` |
| Interfaces (1 method) | `<verb>er`                           | `Reader`, `Stringer`      | `IReadable`, `IDataSource`               |

**Stutter is forbidden.** Package qualifies; `auth.AuthService` → `auth.Service`. `user.UserRepo` → `user.Repo`.

## Errors (you wrap, you don't swallow)

```go
file, err := os.Open(path)
if err != nil {
    return fmt.Errorf("open %s: %w", path, err)   // %w preserves the chain
}
defer file.Close()
```

| Need                    | Use                                                                        |
| ----------------------- | -------------------------------------------------------------------------- |
| Wrap upstream error     | `fmt.Errorf("verb noun: %w", err)` — lowercase, no period                  |
| Known failure type      | sentinel: `var ErrXxx = errors.New("...")`                                 |
| Carry data on the error | custom type with `Error() string`                                          |
| Inspect later           | `errors.Is(err, sentinel)` / `errors.As(err, &target)`                     |
| Combine N errors        | `errors.Join(errs...)` (1.20+)                                             |
| Recovery boundary       | HTTP middleware / goroutine top: `defer func() { if r := recover(); … }()` |

## File layout

```
yourapp/
├── cmd/<binary>/main.go         # thin entry; calls a startup function in internal/
├── internal/
│   ├── <domain>/                # auth, orders, db, cache, obs
│   └── <subdomain>/             # nested when a domain grows
├── pkg/                         # ONLY if you publish a library — most apps don't need this
└── go.mod
```

**`internal/` for everything that isn't a deliberate public API.** Compiler enforces — modules outside this tree cannot import.
**File ≤500 lines.** Past that, split by responsibility.
**No `init()` functions** unless you can defend them in code review. They run before `main`, hide global state, surprise readers. Load state explicitly.

## Receivers: pointer vs value

```go
func (u *User) SetName(n string) { u.Name = n }   // mutates → pointer
func (u User)  String() string  { return u.Name } // doesn't mutate, value type small → value
```

**Be consistent within a type.** Mixing is a smell. When in doubt: pointer.

## Modules

```
yourapp/
├── go.mod                # module declaration + deps + go version
├── go.sum                # cryptographic hashes — COMMIT IT
```

- `go mod tidy` before every commit. Removes unused, adds missing.
- v2+ has versioned import path: `github.com/you/lib/v2`. Skipping this breaks consumers.
- `replace` directives don't ship to release branches.
- Workspaces (`go.work`) for cross-module dev — **don't commit** `go.work`.

## Generics

Use when:

- Container types (typed queue/set/cache)
- Algorithms over `comparable` / `Ordered` (sort, dedup, min/max)
- Std lib's `slices`, `maps`, `cmp` (1.21+) already cover most cases — **check there first**

Don't use when:

- One concrete type — write the function
- Interface with methods would do — interface is clearer
- "Just in case" — YAGNI

## Anti-patterns

- `if err != nil { return err }` without wrapping context — wrap with `%w`
- Logging AND returning the error — caller logs it again
- `panic` for normal error paths
- `_ = f()` silently ignoring errors (use `// reason: ...` if truly needed)
- `interface{}` in public APIs — use generics or be specific
- Goroutines started without a stop mechanism (see `Skill(go-concurrency)`)
- Global mutable state, even in `internal/`
- Empty `pkg/` directory just because some blog said to
- `log.Println` for structured needs — use `log/slog`

## Red flags

| Thought                                     | Reality                                                                           |
| ------------------------------------------- | --------------------------------------------------------------------------------- |
| "I'll handle it later" (re: error)          | Later = never. Wrap or document the ignore now.                                   |
| "This needs reflection"                     | 95% of the time you need generics or an interface. Reflection is the last resort. |
| "Just one global"                           | Two months later there are forty. Pass it explicitly.                             |
| "Test the implementation, not the behavior" | Test the behavior. Implementation can change.                                     |
| "It's faster with `interface{}`"            | Measure first. Reflection beats type-asserting hot paths only sometimes.          |

## Hand-off

For concurrency (goroutines, channels, context, errgroup): `Skill(go-concurrency)`. For tests (table-driven, `t.Parallel`, testcontainers): `Skill(go-testing)`. For HTTP routing with chi: `Skill(go-chi)`. For database access: `Skill(go-pgx)` + `Skill(go-sqlc)`. For structured logging: `Skill(go-slog)`. For MCP servers: `Skill(go-mcp)`.

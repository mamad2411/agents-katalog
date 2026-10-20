---
name: go-code-style
description: "Golang code style, naming, struct/interface design, and idiomatic patterns. Covers formatting and conventions, naming (packages, constructors, structs, interfaces, constants, enums, errors, booleans, receivers, getters/setters, functional options, acronyms, test names), struct/interface design (composition, embedding, type assertions, type switches, interface segregation, pointer vs value receivers, struct field tags), and design patterns/idioms (functional options, constructors, error flow, resource management and lifecycle, graceful shutdown, resilience, architecture styles, data handling, streaming). Use when writing Go code, reviewing style, choosing between naming alternatives, designing types or interfaces, embedding structs, writing type assertions, adding struct field tags, choosing pointer vs value receivers, implementing functional options or builders, setting up graceful shutdown, applying resilience patterns, or asking which idiomatic Go pattern fits a problem. Also trigger for MixedCaps vs snake_case, ALL_CAPS constants, Get-prefix getters, error string casing, 'accept interfaces return structs', or compile-time interface checks."
user-invocable: true
license: MIT
compatibility: Designed for Claude Code or similar AI coding agents, and for projects using Golang.
metadata:
  author: samber
  version: "1.2.0"
  openclaw:
    emoji: "🎨"
    homepage: https://github.com/samber/cc-skills-golang
    requires:
      bins:
        - go
    install: []
---

**Persona:** You are a Go architect who favors small, composable interfaces, concrete return types, and patterns applied only when they solve a real problem — not to demonstrate sophistication. You push back on premature abstraction.

**Modes:**

- **Design mode** — creating new APIs, packages, or application structure: ask about architecture preference before proposing patterns; favor the smallest pattern that satisfies the requirement.
- **Review mode** — auditing existing code: scan for `init()` abuse, unbounded resources, missing timeouts, implicit global state, naming stutter, premature interfaces, and large interfaces; report findings before suggesting refactors. Use up to 5 parallel sub-agents for large codebases, each on an independent concern (control flow, naming, interface design, resource management, architecture).

> **Community default.** A company skill that explicitly supersedes `go-code-style` skill takes precedence.

# Go Code Style, Naming & Design Patterns

Style, naming, type design, and idiomatic patterns that require human judgment — linters handle raw formatting, this skill handles clarity and structure.

> "Clear is better than clever." — Go Proverbs
>
> "Design the architecture, name the components, document the details." — Go Proverbs

When ignoring a rule, add a comment to the code explaining why.

## Best Practices Summary

1. Constructors SHOULD use **functional options** — they scale better as APIs evolve (one function per option, no breaking changes)
2. Functional options MUST **return an error** if validation can fail — catch bad config at construction, not at runtime
3. **Avoid `init()`** — runs implicitly, cannot return errors, makes testing unpredictable. Use explicit constructors
4. Enums SHOULD **start at 1** (or an `Unknown` sentinel at 0) — Go's zero value silently passes as the first enum member otherwise
5. Error cases MUST be **handled first** with early return — keep the happy path flat
6. **Panic is for bugs, not expected errors** — callers can handle returned errors; panics crash the process
7. **`defer Close()` immediately after opening** — later code changes can accidentally skip cleanup
8. Every external call SHOULD **have a timeout** — a slow upstream hangs your goroutine indefinitely
9. **Limit everything** (pool sizes, queue depths, buffers) — unbounded resources grow until they crash
10. All identifiers MUST use **MixedCaps**, never underscores — this is load-bearing for Go's export mechanism and tooling
11. Names MUST NOT **stutter** with their package (`http.Client`, not `http.HTTPClient`)
12. Interfaces SHOULD have **1-3 methods**, defined where consumed, not where implemented
13. Functions SHOULD **accept interfaces, return concrete structs** — never return interfaces from constructors
14. NEVER create interfaces prematurely — wait for 2+ implementations or a real testability need
15. **Design for testability** — accept interfaces, inject dependencies, keep functions pure

## Line Length & Breaking

No rigid line limit, but lines beyond ~120 characters MUST be broken. Break at **semantic boundaries**, not arbitrary column counts. Function calls with 4+ arguments MUST use one argument per line — even when the prompt asks for single-line code:

```go
// Good — each argument on its own line, closing paren separate
mux.HandleFunc("/api/users", func(w http.ResponseWriter, r *http.Request) {
    handleUsers(
        w,
        r,
        serviceName,
        cfg,
        logger,
        authMiddleware,
    )
})
```

When a function signature is too long, the real fix is often **fewer parameters** (use an options struct, see Design Patterns below) rather than better line wrapping. For multi-line signatures, put each parameter on its own line.

## Variable Declarations

SHOULD use `:=` for non-zero values, `var` for zero-value initialization. The form signals intent: `var` means "this starts at zero."

```go
var count int              // zero value, set later
name := "default"          // non-zero, := is appropriate
var buf bytes.Buffer       // zero value is ready to use
```

### Slice & Map Initialization

Slices and maps MUST be initialized explicitly, never nil. Nil maps panic on write; nil slices serialize to `null` in JSON (vs `[]` for empty slices), surprising API consumers.

```go
users := []User{}                       // always initialized
m := map[string]int{}                   // always initialized
users := make([]User, 0, len(ids))      // preallocate when capacity is known
m := make(map[string]int, len(items))   // preallocate when size is known
```

Do not preallocate speculatively — `make([]T, 0, 1000)` wastes memory when the common case is 10 items.

### Composite Literals

Composite literals MUST use field names — positional fields break when the type adds or reorders fields:

```go
srv := &http.Server{
    Addr:         ":8080",
    ReadTimeout:  5 * time.Second,
    WriteTimeout: 10 * time.Second,
}
```

## Control Flow

### Reduce Nesting

Errors and edge cases MUST be handled first (early return). Keep the happy path at minimal indentation:

```go
func process(data []byte) (*Result, error) {
    if len(data) == 0 {
        return nil, errors.New("empty data")
    }

    parsed, err := parse(data)
    if err != nil {
        return nil, fmt.Errorf("parsing: %w", err)
    }

    return transform(parsed), nil
}
```

### Eliminate Unnecessary `else`

When the `if` body ends with `return`/`break`/`continue`, the `else` MUST be dropped. Use default-then-override for simple assignments — assign a default, then override with independent conditions or a `switch`:

```go
// Good — default-then-override with switch (cleanest for mutually exclusive overrides)
level := slog.LevelInfo
switch {
case debug:
    level = slog.LevelDebug
case verbose:
    level = slog.LevelWarn
}

// Bad — else-if chain hides that there's a default
if debug {
    level = slog.LevelDebug
} else if verbose {
    level = slog.LevelWarn
} else {
    level = slog.LevelInfo
}
```

### Complex Conditions & Init Scope

When an `if` condition has 3+ operands, MUST extract into named booleans — a wall of `||` is unreadable and hides business logic. Keep expensive checks inline for short-circuit benefit. [Details](references/details.md)

```go
// Good — named booleans make intent clear
isAdmin := user.Role == RoleAdmin
isOwner := resource.OwnerID == user.ID
isPublicVerified := resource.IsPublic && user.IsVerified
if isAdmin || isOwner || isPublicVerified || permissions.Contains(PermOverride) {
    allow()
}
```

Scope variables to `if` blocks when only needed for the check:

```go
if err := validate(input); err != nil {
    return err
}
```

### Switch Over If-Else Chains

When comparing the same variable multiple times, prefer `switch`:

```go
switch status {
case StatusActive:
    activate()
case StatusInactive:
    deactivate()
default:
    panic(fmt.Sprintf("unexpected status: %d", status))
}
```

## Function Design

- Functions SHOULD be **short and focused** — one function, one job.
- Functions SHOULD have **≤4 parameters**. Beyond that, use an options struct (see Design Patterns below).
- **Parameter order**: `context.Context` first, then inputs, then output destinations.
- Naked returns help in very short functions (1-3 lines) where return values are obvious, but become confusing when readers must scroll to find what's returned — name returns explicitly in longer functions.

```go
func FetchUser(ctx context.Context, id string) (*User, error)
func SendEmail(ctx context.Context, msg EmailMessage) error  // grouped into struct
```

### Prefer `range` for Iteration

SHOULD use `range` over index-based loops. Use `range n` (Go 1.22+) for simple counting.

```go
for _, user := range users {
    process(user)
}
```

## Value vs Pointer Arguments

Pass small types (`string`, `int`, `bool`, `time.Time`) by value. Use pointers when mutating, for large structs (~128+ bytes), or when nil is meaningful. This covers **function parameters**, not method receivers — see [Pointer vs Value Receivers](#pointer-vs-value-receivers) below. [Details](references/details.md)

## Code Organization Within Files

- **Group related declarations**: type, constructor, methods together
- **Order**: package doc, imports, constants, types, constructors, methods, helpers
- **One primary type per file** when it has significant methods
- **Blank imports** (`_ "pkg"`) register side effects (init functions). Restricting them to `main` and test packages makes side effects visible at the application root, not hidden in library code
- **Dot imports** pollute the namespace and make it impossible to tell where a name comes from — never use in library code
- **Unexport aggressively** — you can always export later; unexporting is a breaking change

## String Handling

Use `strconv` for simple conversions (faster), `fmt.Sprintf` for complex formatting. Use `%q` in error messages to make string boundaries visible. Use `strings.Builder` for loops, `+` for simple concatenation.

## Type Conversions

Prefer explicit, narrow conversions. Use generics over `any` when a concrete type will do:

```go
func Contains[T comparable](slice []T, target T) bool  // not []any
```

---

## Naming Conventions

Go favors short, readable names. Capitalization controls visibility — uppercase is exported, lowercase is unexported. All identifiers MUST use MixedCaps, NEVER underscores (the only exceptions are test subcases like `TestFoo_InvalidInput`, generated code, and OS/cgo interop) — this is load-bearing, not cosmetic, since Go's export mechanism and tooling assume MixedCaps throughout.

### Quick Reference

| Element | Convention | Example |
| --- | --- | --- |
| Package | lowercase, single word, \_test suffix OK for test files | `json`, `http`, `tabwriter`, `http_test` |
| File | lowercase, underscores OK | `user_handler.go` |
| Exported name | UpperCamelCase | `ReadAll`, `HTTPClient` |
| Unexported | lowerCamelCase | `parseToken`, `userCount` |
| Interface | method name + `-er` | `Reader`, `Closer`, `Stringer` |
| Struct | MixedCaps noun | `Request`, `FileHeader` |
| Constant | MixedCaps (not ALL_CAPS) | `MaxRetries`, `defaultTimeout` |
| Receiver | 1-2 letter abbreviation | `func (s *Server)`, `func (b *Buffer)` |
| Error variable | `Err` prefix | `ErrNotFound`, `ErrTimeout` |
| Error type | `Error` suffix | `PathError`, `SyntaxError` |
| Constructor | `New` (single type) or `NewTypeName` (multi-type) | `ring.New`, `http.NewRequest` |
| Boolean field | `is`, `has`, `can` prefix on **fields** and methods | `isReady`, `IsConnected()` |
| Test function | `Test` + function name | `TestParseToken` |
| Acronym | all caps or all lower | `URL`, `HTTPServer`, `xmlParser` |
| Variant: context | `WithContext` suffix | `FetchWithContext`, `QueryContext` |
| Variant: in-place | `In` suffix | `SortIn()`, `ReverseIn()` |
| Variant: error | `Must` prefix | `MustParse()`, `MustLoadConfig()` |
| Option func | `With` + field name | `WithPort()`, `WithLogger()` |
| Enum (iota) | type name prefix, zero-value = unknown | `StatusUnknown` at 0, `StatusReady` |
| Named return | descriptive, for docs only | `(n int, err error)` |
| Error string | lowercase (incl. acronyms), no punctuation | `"image: unknown format"`, `"invalid id"` |
| Import alias | short, only on collision | `mrand "math/rand"`, `pb "app/proto"` |
| Format func | `f` suffix | `Errorf`, `Wrapf`, `Logf` |
| Test table fields | `got`/`expected` prefixes | `input string`, `expected int` |

### Avoid Stuttering

Go call sites always include the package name, so repeating it in the identifier wastes the reader's time — `http.HTTPClient` forces parsing "HTTP" twice. A name MUST NOT repeat information already present in the package name, type name, or surrounding context.

```go
// Good — clean at the call site
http.Client       // not http.HTTPClient
json.Decoder      // not json.JSONDecoder
user.New()        // not user.NewUser()
config.Parse()    // not config.ParseConfig()

// In package sqldb:
type Connection struct{}  // not DBConnection — "db" is already in the package name

// Anti-stutter applies to ALL exported types, not just the primary struct:
// In package dbpool:
type Pool struct{}        // not DBPool
type Status struct{}      // not PoolStatus — callers write dbpool.Status
type Option func(*Pool)   // not PoolOption
```

### Frequently Missed Conventions

These conventions are correct but non-obvious — they are the most common source of naming mistakes:

**Constructor naming:** When a package exports a single primary type, the constructor is `New()`, not `NewTypeName()`. This avoids stuttering — callers write `apiclient.New()` not `apiclient.NewClient()`. Use `NewTypeName()` only when a package has multiple constructible types (like `http.NewRequest`, `http.NewServeMux`).

**Boolean struct fields:** Unexported boolean fields MUST use `is`/`has`/`can` prefix — `isConnected`, `hasPermission`, not bare `connected` or `permission`. The exported getter keeps the prefix: `IsConnected() bool`. This reads naturally as a question and distinguishes booleans from other types.

**Error strings are fully lowercase — including acronyms.** Write `"invalid message id"` not `"invalid message ID"`, because error strings are often concatenated with other context (`fmt.Errorf("parsing token: %w", err)`) and mixed case looks wrong mid-sentence. Sentinel errors should include the package name as prefix: `errors.New("apiclient: not found")`.

**Enum zero values:** Always place an explicit `Unknown`/`Invalid` sentinel at iota position 0. A `var s Status` silently becomes 0 — if that maps to a real state like `StatusReady`, code can behave as if a status was deliberately chosen when it wasn't.

**Subtest names:** Table-driven test case names in `t.Run()` should be fully lowercase descriptive phrases: `"valid id"`, `"empty input"` — not `"valid ID"` or `"Valid Input"`.

### Detailed Categories

For complete rules, examples, and rationale, see:

- **[Packages, Files & Import Aliasing](references/naming-packages-files.md)** — Package naming (single word, lowercase, no plurals), file naming conventions, import alias patterns (only use on collision to avoid cognitive load), and directory structure.

- **[Variables, Booleans, Receivers & Acronyms](references/naming-identifiers.md)** — Scope-based naming (length matches scope: `i` for 3-line loops, longer names for package-level), single-letter receiver conventions (`s` for Server), acronym casing (URL not Url, HTTPServer not HttpServer), and boolean naming patterns (isReady, hasPrefix).

- **[Functions, Methods & Options](references/naming-functions-methods.md)** — Getter/setter patterns (Go omits `Get` so `user.Name()` reads naturally), constructor conventions (`New` or `NewTypeName`), named returns (for documentation only), format function suffixes (`Errorf`, `Wrapf`), and functional options (`WithPort`, `WithLogger`).

- **[Types, Constants & Errors](references/naming-types-errors.md)** — Interface naming (`Reader`, `Closer` suffix with `-er`), struct naming (nouns, MixedCaps), constants (MixedCaps, not ALL_CAPS), enums (type name prefix like `StatusReady`), sentinel errors (`ErrNotFound` variables), error types (`PathError` suffix), and error message conventions (lowercase, no punctuation).

- **[Test Naming](references/naming-testing.md)** — Test function naming (`TestFunctionName`), table-driven test field conventions (`input`, `expected`), test helper naming, and subcase naming patterns.

### Naming Common Mistakes

| Mistake | Fix |
| --- | --- |
| `ALL_CAPS` constants | Go reserves casing for visibility, not emphasis — use `MixedCaps` (`MaxRetries`) |
| `GetName()` getter | Go omits `Get` because `user.Name()` reads naturally at call sites. But `Is`/`Has`/`Can` prefixes are kept for boolean predicates: `IsHealthy() bool` not `Healthy() bool` |
| `Url`, `Http`, `Json` acronyms | Mixed-case acronyms create ambiguity (`HttpsUrl` — is it `Https+Url`?). Use all caps or all lower |
| `this` or `self` receiver | Go methods are called frequently — use 1-2 letter abbreviation (`s` for `Server`) to reduce visual noise |
| `util`, `helper` packages | These names say nothing about content — use specific names that describe the abstraction |
| `http.HTTPClient` stuttering | Package name is always present at call site — `http.Client` avoids reading "HTTP" twice |
| `user.NewUser()` constructor | Single primary type uses `New()` — `user.New()` avoids repeating the type name |
| `connected bool` field | Bare adjective is ambiguous — use `isConnected` so the field reads as a true/false question |
| `"invalid message ID"` error | Error strings must be fully lowercase including acronyms — `"invalid message id"` |
| `StatusReady` at iota 0 | Zero value should be a sentinel — `StatusUnknown` at 0 catches uninitialized values |
| `"not found"` error string | Sentinel errors should include the package name — `"mypackage: not found"` identifies the origin |
| `userSlice` type-in-name | Types encode implementation detail — `users` describes what it holds, not how |
| Inconsistent receiver names | Switching names across methods of the same type confuses readers — use one name consistently |
| `snake_case` identifiers | Underscores conflict with Go's MixedCaps convention and tooling expectations — use `mixedCaps` |
| Long names for short scopes | Name length should match scope — `i` is fine for a 3-line loop, `userIndex` is noise |
| Naming constants by value | Values change, roles don't — `DefaultPort` survives a port change, `Port8080` doesn't |
| `FetchCtx()` context variant | `WithContext` is the standard Go suffix — `FetchWithContext()` is instantly recognizable |
| `sort()` in-place but no `In` | Readers assume functions return new values. `SortIn()` signals mutation |
| `parse()` panicking on error | `MustParse()` warns callers that failure panics — surprises belong in the name |
| Mixing `With*`, `Set*`, `Use*` | Consistency across the codebase — `With*` is the Go convention for functional options |
| Plural package names | Go convention is singular (`net/url` not `net/urls`) — keeps import paths consistent |
| `Wrapf` without `f` suffix | The `f` suffix signals format-string semantics — `Wrapf`, `Errorf` tell callers to pass format args |
| Unnecessary import aliases | Aliases add cognitive load. Only alias on collision — `mrand "math/rand"` |
| Inconsistent concept names | Using `user`/`account`/`person` for the same concept forces readers to track synonyms — pick one name |

---

## Structs & Interfaces

### Keep Interfaces Small

> "The bigger the interface, the weaker the abstraction." — Go Proverbs

Interfaces SHOULD have 1-3 methods, named after their method with an `-er` suffix (see Naming Conventions above). Small interfaces are easier to implement, mock, and compose. If you need a larger contract, compose it from small interfaces:

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// Composed from small interfaces
type ReadWriter interface {
    Reader
    Writer
}
```

### Define Interfaces Where They're Consumed

Interfaces belong to consumers. Interfaces MUST be defined where consumed, not where implemented — this keeps the consumer in control of the contract and avoids importing a package just for its interface.

```go
// package notification — defines only what it needs
type Sender interface {
    Send(to, body string) error
}

type Service struct {
    sender Sender
}
```

The `email` package exports a concrete `Client` struct — it doesn't need to know about `Sender`.

### Accept Interfaces, Return Structs

Functions SHOULD accept interface parameters for flexibility and return concrete types for clarity. Callers get full access to the returned type's fields and methods; consumers upstream can still assign the result to an interface variable if needed.

```go
// Good — accepts interface, returns concrete
func NewService(store UserStore) *Service { ... }

// BAD — NEVER return interfaces from constructors
func NewService(store UserStore) ServiceInterface { ... }
```

### Don't Create Interfaces Prematurely

> "Don't design with interfaces, discover them."

NEVER create interfaces prematurely — wait for 2+ implementations or a testability requirement. Premature interfaces add indirection without value. Start with concrete types; extract an interface when a second consumer or a test mock demands it.

```go
// Bad — premature interface with a single implementation
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*User, error)
}
type userRepository struct { db *sql.DB }

// Good — start concrete, extract an interface later when needed
type UserRepository struct { db *sql.DB }
```

### Make the Zero Value Useful

Design structs so they work without explicit initialization. A well-designed zero value reduces constructor boilerplate and prevents nil-related bugs:

```go
// Good — zero value is ready to use
var buf bytes.Buffer
buf.WriteString("hello")

var mu sync.Mutex
mu.Lock()

// Bad — zero value is broken, requires constructor
type Registry struct {
    items map[string]Item // nil map, panics on write
}

// Good — lazy initialization guards the zero value
func (r *Registry) Register(name string, item Item) {
    if r.items == nil {
        r.items = make(map[string]Item)
    }
    r.items[name] = item
}
```

### Avoid `any` / `interface{}` When a Specific Type Will Do

Since Go 1.18+, MUST prefer generics over `any` for type-safe operations. Use `any` only at true boundaries where the type is genuinely unknown (e.g., JSON decoding, reflection):

```go
// Bad — loses type safety
func Contains(slice []any, target any) bool { ... }

// Good — generic, type-safe
func Contains[T comparable](slice []T, target T) bool { ... }
```

### Key Standard Library Interfaces

| Interface     | Package         | Method                                |
| ------------- | --------------- | -------------------------------------- |
| `Reader`      | `io`            | `Read(p []byte) (n int, err error)`   |
| `Writer`      | `io`            | `Write(p []byte) (n int, err error)`  |
| `Closer`      | `io`            | `Close() error`                       |
| `Stringer`    | `fmt`           | `String() string`                     |
| `error`       | builtin         | `Error() string`                      |
| `Handler`     | `net/http`      | `ServeHTTP(ResponseWriter, *Request)` |
| `Marshaler`   | `encoding/json` | `MarshalJSON() ([]byte, error)`       |
| `Unmarshaler` | `encoding/json` | `UnmarshalJSON([]byte) error`         |

Canonical method signatures MUST be honored — if your type has a `String()` method, it must match `fmt.Stringer`. Don't invent `ToString()` or `ReadData()`.

### Compile-Time Interface Check

Verify a type implements an interface at compile time with a blank identifier assignment. Place it near the type definition:

```go
var _ io.ReadWriter = (*MyBuffer)(nil)
```

This costs nothing at runtime. If `MyBuffer` ever stops satisfying `io.ReadWriter`, the build fails immediately.

### Dependency Injection via Interfaces

Accept dependencies as interfaces in constructors. This decouples components and makes testing straightforward:

```go
type UserStore interface {
    FindByID(ctx context.Context, id string) (*User, error)
}

type UserService struct {
    store UserStore
}

func NewUserService(store UserStore) *UserService {
    return &UserService{store: store}
}
```

In tests, pass a mock or stub that satisfies `UserStore` — no real database needed. → See the `go-dependency-injection` skill for library-based DI (samber/do, wire, dig, fx).

### Pointer vs Value Receivers

| Use pointer `(s *Server)` | Use value `(s Server)` |
| --- | --- |
| Method modifies the receiver | Receiver is small and immutable |
| Receiver contains `sync.Mutex` or similar | Receiver is a basic type (int, string) |
| Receiver is a large struct | Method is a read-only accessor |
| Consistency: if any method uses a pointer, all should | Map and function values (already reference types) |

Receiver type MUST be consistent across all methods of a type — if one method uses a pointer receiver, all methods should.

For type assertions, type switches, embedding depth, struct field tags, and the `noCopy` pattern, see [Structs & Interfaces — Depth](references/structs-interfaces.md).

### Structs & Interfaces Common Mistakes

| Mistake | Fix |
| --- | --- |
| Large interfaces (5+ methods) | Split into focused 1-3 method interfaces, compose if needed |
| Defining interfaces in the implementor package | Define where consumed |
| Returning interfaces from constructors | Return concrete types |
| Bare type assertions without comma-ok | Always use `v, ok := x.(T)` |
| Embedding when you only need a few methods | Use a named field and delegate explicitly |
| Missing field tags on serialized structs | Tag all exported fields in marshaled types |
| Mixing pointer and value receivers on a type | Pick one and be consistent |
| Forgetting compile-time interface check | Add `var _ Interface = (*Type)(nil)` |
| Using `ToString()` instead of `String()` | Honor canonical method names |
| Premature interface with a single implementation | Start concrete, extract interface when needed |
| Nil map/slice in zero value struct | Use lazy initialization in methods |
| Using `any` for type-safe operations | Use generics (`[T comparable]`) instead |

---

## Design Patterns & Idioms

Idiomatic Go patterns for production-ready code. For error handling details see the `go-error-handling` skill; for context propagation and goroutine lifecycle see the `go-concurrency` skill.

### Constructor Patterns: Functional Options vs Builder

```go
type Server struct {
    addr         string
    readTimeout  time.Duration
    writeTimeout time.Duration
    maxConns     int
}

type Option func(*Server)

func WithReadTimeout(d time.Duration) Option {
    return func(s *Server) { s.readTimeout = d }
}

func WithWriteTimeout(d time.Duration) Option {
    return func(s *Server) { s.writeTimeout = d }
}

func WithMaxConns(n int) Option {
    return func(s *Server) { s.maxConns = n }
}

func NewServer(addr string, opts ...Option) *Server {
    s := &Server{ // defaults
        addr:         addr,
        readTimeout:  5 * time.Second,
        writeTimeout: 10 * time.Second,
        maxConns:     100,
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// Usage
srv := NewServer(":8080",
    WithReadTimeout(30*time.Second),
    WithMaxConns(500),
)
```

Constructors SHOULD use **functional options** — they scale better with API evolution and require less code than a builder. Use the builder pattern only if you need complex validation between configuration steps.

### Avoid `init()` and Mutable Globals

`init()` runs implicitly, makes testing harder, and creates hidden dependencies:

- Multiple `init()` functions run in declaration order, across files in **filename alphabetical order** — fragile
- Cannot return errors — failures must panic or `log.Fatal`
- Runs before `main()` and tests — side effects make tests unpredictable

```go
// Bad — hidden global state
var db *sql.DB

func init() {
    var err error
    db, err = sql.Open("postgres", os.Getenv("DATABASE_URL"))
    if err != nil {
        log.Fatal(err)
    }
}

// Good — explicit initialization, injectable
func NewUserRepository(db *sql.DB) *UserRepository {
    return &UserRepository{db: db}
}
```

### Enums: Start at 1

Zero values should represent invalid/unset state (see Naming Conventions above for the `StatusUnknown` naming pattern):

```go
type Status int

const (
    StatusUnknown Status = iota // 0 = invalid/unset
    StatusActive                // 1
    StatusInactive              // 2
    StatusSuspended             // 3
)
```

### Compile Regexp Once

```go
// Good — compiled once at package level
var emailRegex = regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)

func ValidateEmail(email string) bool {
    return emailRegex.MatchString(email)
}
```

### Use `//go:embed` for Static Assets

```go
import "embed"

//go:embed templates/*
var templateFS embed.FS

//go:embed version.txt
var version string
```

### Error Flow Patterns

Error cases MUST be handled first with early return — keep the happy path at minimal indentation (see Control Flow above for the full pattern and examples).

**When to panic vs return error:**

- **Return error**: network failures, file not found, invalid input — anything a caller can handle
- **Panic**: nil pointer in a place that should be impossible, violated invariant, `Must*` constructors used at init time
- **`.Close()` errors**: acceptable to not check — `defer f.Close()` is fine without error handling

### Data Handling

| Type     | Default for | Use when                                            |
| -------- | ----------- | ---------------------------------------------------- |
| `string` | Everything  | Immutable, safe, UTF-8                              |
| `[]byte` | I/O         | Writing to `io.Writer`, building strings, mutations |
| `[]rune` | Unicode ops | `len()` must mean characters, not bytes             |

Avoid repeated conversions — each one allocates. Stay in one type until you need the other.

Use iterators (Go 1.23+) and streaming patterns to process large datasets without loading everything into memory. For large transfers between services (e.g., 1M rows DB to HTTP), stream to prevent OOM.

For code examples, see [Data Handling Patterns](references/patterns-data-handling.md).

### Resource Management

`defer Close()` immediately after opening — don't wait, don't forget:

```go
f, err := os.Open(path)
if err != nil {
    return err
}
defer f.Close() // right here, not 50 lines later

rows, err := db.QueryContext(ctx, query)
if err != nil {
    return err
}
defer rows.Close()
```

Prefer `runtime.AddCleanup` over `runtime.SetFinalizer` — finalizers are unpredictable and can resurrect objects.

For graceful shutdown, resource pools, and `runtime.AddCleanup`, see [Resource Management](references/patterns-resource-management.md).

### Resilience & Limits

**Timeout every external call:**

```go
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()

resp, err := httpClient.Do(req.WithContext(ctx))
```

**Retry & context checks:** Retry logic MUST check `ctx.Err()` between attempts and use exponential/linear backoff via `select` on `ctx.Done()`. Long loops MUST check `ctx.Err()` periodically. → See the `go-concurrency` skill.

### Database Patterns

→ See the `go-database` skill for sqlx/pgx, transactions, nullable columns, connection pools, repository interfaces, testing.

### Architecture

Ask the developer which architecture they prefer: clean architecture, hexagonal, DDD, or flat layout. Don't impose complex architecture on a small project.

Core principles regardless of architecture:

- **Keep domain pure** — no framework dependencies in the domain layer
- **Fail fast** — validate at boundaries, trust internal code
- **Make illegal states unrepresentable** — use types to enforce invariants
- **Respect 12-factor app** principles — → see the `go-project-layout` skill

| Guide | Scope |
| --- | --- |
| [Architecture Patterns](references/patterns-architecture.md) | High-level principles, when each architecture fits |
| [Clean Architecture](references/patterns-clean-architecture.md) | Use cases, dependency rule, layered adapters |
| [Hexagonal Architecture](references/patterns-hexagonal-architecture.md) | Ports and adapters, domain core isolation |
| [Domain-Driven Design](references/patterns-ddd.md) | Aggregates, value objects, bounded contexts |

### Code Philosophy

- **A little copying is better than a little dependency** — a little recode > a big dependency; each dep adds attack surface and maintenance burden
- **Use `slices` and `maps` standard packages**; for filter/group-by/chunk, use `github.com/samber/lo`
- **"Reflection is never clear"** — avoid `reflect` unless necessary
- **Don't abstract prematurely** — extract when the pattern is stable
- **Minimize public surface** — every exported name is a commitment
- **Design for testability** — accept interfaces, inject dependencies, keep functions pure

## Enforce with Linters

Many rules across this skill are enforced automatically: `gofmt`, `gofumpt`, `goimports`, `gocritic`, `revive`, `wsl_v5` (style); `revive`, `predeclared`, `misspell`, `errname` (naming). → See the `go-lint` skill.

## Cross-References

- → See the `go-lint` skill for automated formatting and naming enforcement
- → See the `go-dependency-injection` skill for library-based DI (samber/do, wire, dig, fx) built on the interface patterns above
- → See the `go-error-handling` skill for error wrapping, sentinel errors, and the single handling rule
- → See the `go-data-structures` skill for data structure selection, internals, and container/ packages
- → See the `go-concurrency` skill for goroutine lifecycle, graceful shutdown, and context propagation
- → See the `go-project-layout` skill for architecture and directory structure
- → See the `go-database` skill for repository patterns, transactions, and connection pools
- → See `go-continuous-integration` skill for automated AI-driven code review in CI using these guidelines

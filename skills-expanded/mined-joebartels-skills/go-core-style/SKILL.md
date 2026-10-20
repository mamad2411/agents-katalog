---
name: go-core-style
description: Comprehensive agent skill for enforcing idiomatic Go philosophy, style standards (Google/Uber Go Style Guides), line-of-sight error handling, and consumer-side interface abstractions. Use when writing, reviewing, refactoring, or linting Go code.
version: 1.1.0
author: go-agentic-workbench
license: MIT
---

# Go Core Philosophy & Style Skill

This skill guides AI agents in writing, reviewing, and refactoring **idiomatic Go code** in strict alignment with Go's founding philosophy, modern engineering specifications, and established industry guidelines.

---

## 1. Core Philosophy ("The Go Way")

### 1.1 Clarity & Simplicity Over Cleverness
* **Clear is better than clever**: Avoid complex abstractions, reflection hacks, or unhelpful design patterns. Code is written primarily to be read and maintained by engineers, not just executed by machines [385, 396].
* **Simplicity is prerequisite for reliability**: Keep functions focused and eliminate unnecessary indirection [364]. Shorter, simpler functions compile faster, inline better, and reduce cognitive overhead [314, 375].

### 1.2 Line of Sight Coding & Early Guard Clauses
* **Align the happy path to the left**: Functions MUST use guard clauses to handle edge cases and errors immediately, returning early [55-56, 374, 399-401].
* **Avoid deep nesting**: Never nest business logic inside deep `if/else` structures. Handle preconditions first so the primary execution path flows straight down the left margin [56, 374, 401].

### 1.3 Errors as Values
* **Errors are normal values, not exceptional control flows**: Handle errors explicitly at the point of occurrence using `if err != nil` [370-372].
* **Plan for failure first**: Address error cases before writing the happy path logic [371].
* **Contextual error wrapping**: Use `fmt.Errorf("...: %w", err)` to wrap errors with actionable context while preserving the underlying error chain for `errors.Is` and `errors.As` checks [40, 56].

### 1.4 Consumer-Side Interfaces & Duck Typing
* **Accept interfaces, return structs**: Functions and constructors should return concrete struct pointers (`*T`), but accept narrow, focused interfaces (`I`) [50-51, 334].
* **Small, consumer-side definitions**: Define interfaces in the package where they are *consumed*, not where they are implemented [1, 6, 50]. Leverage Go's implicit structural duck typing [6, 50].
* **Avoid preemptive interfaces**: Do NOT create interfaces for types with only a single implementation unless required for mocking/testing [51, 332].
* **Interface naming**: Single-method interfaces should use agent nouns ending in `-er` (e.g., `Reader`, `Writer`, `Fetcher`) [105].

### 1.5 State & Goroutine Discipline
* **Avoid package-level state**: Do NOT use global package variables for state or counters. Encapsulate dependencies and state within struct fields to support concurrency and parallel unit testing [365-370].
* **Goroutine lifecycle ownership**: Never launch a goroutine (`go func()`) without knowing exactly how, when, and under what conditions it will terminate [14, 53, 308, 377].
* **Graceful shutdown**: Microservices must manage OS signal cancellation (`SIGTERM`, `SIGINT`) using `signal.NotifyContext` (Go 1.16+) and enforce bounded context timeouts for teardown [18, 237, 320-321].

### 1.6 Parsing, Ownership & Determinism
* **Parse, don't validate**: Turn raw input (config strings, request fields) into its typed value once, at the boundary, and pass the typed value on. A raw string that is kept and checked again elsewhere has two interpreters, and they drift apart. When a type already exists (`time.Duration`, `slog.Level`, `netip.Prefix`), make it the field's type: decoders call `encoding.TextUnmarshaler`.
* **Checks live on the path that produces the value**: A constructor, or the `Parse` that returns the value a caller needs, checks what it is given and returns an error. Don't export a separate `Assert` or `Validate` that every caller must remember to call, and don't rely on callers' checks: `time.NewTicker` panics on a zero interval, so a type that ticks checks its own interval.
* **One struct per key**: Values that share a key live in one struct in one map (`map[string]*Tenant`), not in parallel maps keyed by the same id, which need two lookups and can disagree.
* **Deterministic at the source**: When output order matters, iterate map keys in sorted order (`slices.Sorted(maps.Keys(m))`) where the values are produced, instead of sorting rendered strings afterwards.
* **Strict decoding**: Don't switch on a lenient mode (such as mapstructure's `WeaklyTypedInput`) and then patch its silent conversions with hooks. Decode strictly, and convert explicitly only what needs it, such as environment-variable strings.

---

## 2. Style Standards & Conventions

### 2.1 Standard References
* **Canonical Guides**: Primary guidance follows the **Google Go Style Guide** and **Uber Go Style Guide** [41, 240, 241].
* **Formatting**: Formatting is 100% machine-enforced by `gofmt` (using tabs for indentation) [99, 100, 192].
* **Historical Note**: *Effective Go* (2009) was officially designated as unmaintained in 2022. Modern language capabilities (Go modules, generics, `%w` error wrapping, `net/http.ServeMux` wildcards) supersede older patterns [40, 90, 97].

### 2.2 Naming Rules
* **Package Names**: Short, lowercase, single-word nouns (e.g., `user`, `order`, `http`) [103, 360]. Avoid generic catch-all names like `util`, `common`, `base`, or `helpers` [361].
* **Exported vs Unexported**: `MixedCaps` for exported identifiers, `mixedCaps` for unexported identifiers [104, 106].
* **Getters**: Do NOT prefix getters with `Get`. A getter for field `owner` should be named `Owner()` [104].
* **Receiver Names**: Use 1–2 letter abbreviations matching the struct type (e.g., `func (s *Server) Start()`), never `this` or `self`.

### 2.3 Microservice & Standard Library Best Practices
* **Standard Library First**: Prefer `net/http.ServeMux` (Go 1.22+) for HTTP method matching and path parameters (`GET /users/{id}`) over third-party router frameworks when appropriate [42, 58].
* **Structured Logging**: Use structured, zero-allocation loggers (e.g., `zerolog` or `zap`) returning JSON output for production observability [12-13, 58].

---

## 3. Code Quality Examples

### 3.1 Line of Sight & Error Handling

#### ❌ Bad (Nested Conditionals & Unwrapped Errors)
```go
func ProcessUser(u *User) error {
    if u != nil {
        err := u.Validate()
        if err == nil {
            err = u.Save()
            if err == nil {
                return nil
            } else {
                return err
            }
        } else {
            return err
        }
    } else {
        return errors.New("user is nil")
    }
}
```

#### ✅ Good (Idiomatic Left-Aligned Happy Path)
```go
func ProcessUser(u *User) error {
    if u == nil {
        return errors.New("user is nil")
    }
    if err := u.Validate(); err != nil {
        return fmt.Errorf("user validation failed: %w", err)
    }
    if err := u.Save(); err != nil {
        return fmt.Errorf("saving user failed: %w", err)
    }
    return nil
}
```

---

### 3.2 Interface Abstraction ("Accept Interfaces, Return Structs")

#### ❌ Bad (Package-Level Concrete Interface Export & Prefixes)
```go
// Tightly couples implementation to interface in the producer package
package store

type UserServiceInterface interface { // Anti-pattern: Interface suffix/prefix
    GetUser(id string) (*User, error)
}

type UserServiceImpl struct{} // Anti-pattern: Impl suffix
```

#### ✅ Good (Consumer-Side Narrow Interface)
```go
// Producer Package: Returns concrete struct pointer
package store

type UserStore struct{}

func NewUserStore() *UserStore {
    return &UserStore{}
}

func (s *UserStore) GetUser(id string) (*User, error) {
    return &User{ID: id}, nil
}

// Consumer Package: Defines narrow interface at point of consumption
package service

type UserFetcher interface {
    GetUser(id string) (*store.User, error)
}

type Service struct {
    fetcher UserFetcher
}

func NewService(f UserFetcher) *Service {
    return &Service{fetcher: f}
}
```

---

## 4. Verification & Quality Gates

When generating or reviewing Go code, run the following verification steps:

1. **Formatting Check**: Verify code passes `gofmt -s -w .`
2. **Static Analysis**: Run `go vet ./...` and `staticcheck ./...` [226, 234].
3. **Unit Tests**: Execute `go test -v -race ./...` to verify functionality and detect data races.

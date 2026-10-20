---
name: go-structs-interfaces
description: "Compose Go structs and interfaces — small interfaces, embedding, type assertions and switches, field tags, pointer vs value receivers. Use when designing new Go types, reviewing or auditing existing type design, defining or implementing interfaces, embedding structs or interfaces, writing type assertions or type switches, adding serialization tags, or choosing between pointer and value receivers."
license: MIT
---

# Go Structs & Interfaces

**Leading word: compose.** Design by composition, not abstraction for its own sake — build small 1–3 method interfaces and larger contracts by composing them, and promote APIs by embedding rather than inheriting. Start concrete, and discover interfaces when a second implementation or a testability requirement actually demands one.

## Steps — design new types

1. **Start concrete.** Extract an interface only when a second implementation or a testability requirement appears; a single-implementation interface is premature indirection.

   *Done when: every interface in the design has two or more implementations, or a concrete testability reason.*

2. **Keep interfaces small.** Interfaces have 1–3 methods; compose larger contracts from small ones. Interfaces belong to consumers — define them where consumed, not in the implementor's package.

   *Done when: each interface is at most 3 methods and lives in the package that consumes it.*

3. **Accept interfaces, return structs.** Constructors take interface dependencies where flexibility matters and return concrete types, so callers get full access to the returned type's fields and methods.

   *Done when: every constructor parameter is an interface at its boundary and every constructor returns a concrete type.*

4. **Compose with embedding, hold dependencies as named fields.** Embed when the outer type wants to promote the inner type's full API ("is a"); use a named field when the inner type is internal ("has a"). The outer type overrides a promoted method by defining its own; promoted-method receivers are the inner type.

   *Done when: every embedded type's full API is wanted, and every internal dependency is a named field.*

5. **Make the zero value useful.** A struct works without explicit initialization — guard nil maps/slices with lazy initialization inside methods rather than requiring a constructor.

   *Done when: every type works correctly at its zero value, or explicitly documents why it cannot.*

6. **Assert dynamic types defensively.** Use the comma-ok form `v, ok := x.(T)`, type switches to dispatch on dynamic type, and optional-behavior checks such as `if f, ok := w.(Flusher); ok`.

   *Done when: no bare type assertion exists; capability checks never panic when unsupported.*

7. **Pick one receiver style per type.** Pointer receivers for mutation, mutexes, and large structs; value receivers for small immutable types. Consistency wins — if one method uses a pointer, all should. Honor canonical method names (`String()`, `Read`, `Write`).

   *Done when: receiver style is uniform per type and every interface-satisfying method matches its canonical signature.*

## Steps — review or audit existing types

1. **Audit interface shape.** No interface exceeds 3 methods or sits in the implementor's package; no constructor returns an interface. *Done when: each interface is small, consumer-side, and constructors return concrete types.*
2. **Check composition.** Embeddings promote a full API intentionally; named fields hold dependencies. *Done when: no embedding exists where a named field suffices.*
3. **Check safety.** Zero values are usable, type assertions use comma-ok, and structs holding mutexes/channels/internal pointers embed `noCopy`. *Done when: `go vet` is clean and no nil-map panic is reachable.*
4. **Check serialization.** Exported fields in marshaled structs carry tags; `json:"-"` excludes internals. *Done when: every exported field in a serialized struct is tagged.*
5. **Check typing.** `any` appears only at true boundaries (JSON decoding, reflection); generics carry type-safe operations. *Done when: no type-safe operation uses `any`.*

## Reference

### Key standard library interfaces

| Interface | Package | Method |
| --- | --- | --- |
| `Reader` | `io` | `Read(p []byte) (n int, err error)` |
| `Writer` | `io` | `Write(p []byte) (n int, err error)` |
| `Closer` | `io` | `Close() error` |
| `Stringer` | `fmt` | `String() string` |
| `error` | builtin | `Error() string` |
| `Handler` | `net/http` | `ServeHTTP(ResponseWriter, *Request)` |
| `Marshaler` | `encoding/json` | `MarshalJSON() ([]byte, error)` |
| `Unmarshaler` | `encoding/json` | `UnmarshalJSON([]byte) error` |

Honor canonical method signatures — `String()`, not `ToString()`.

### Compile-time interface check

```go
var _ io.ReadWriter = (*MyBuffer)(nil)
```

Place it near the type definition; the build fails the moment the type stops satisfying the interface. Costs nothing at runtime.

### Embedding vs named field

| Use | When |
| --- | --- |
| **Embed** | Promote the full API of the inner type — the outer type "is a" enhanced version |
| **Named field** | The inner type is internal — the outer type "has a" dependency |

### Composition examples

```go
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type ReadWriter interface {
    Reader
    Writer
}

type Logger struct { *slog.Logger } // embedded — promotes Info, Warn, ...

type Server struct {
    Logger
    store *DataStore // named field — dependency held internally
}
```

### Field tag directives

```go
type Order struct {
    ID        string    `json:"id"         db:"id"`
    UserID    string    `json:"user_id"    db:"user_id"`
    Total     float64   `json:"total"      db:"total"`
    Items     []Item    `json:"items"      db:"-"`
    CreatedAt time.Time `json:"created_at" db:"created_at"`
    DeletedAt time.Time `json:"-"          db:"deleted_at"`
    Internal  string    `json:"-"          db:"-"`
}
```

| Directive | Meaning |
| --- | --- |
| `json:"name"` | Field name in JSON output |
| `json:"name,omitempty"` | Omit field if zero value |
| `json:"-"` | Always exclude from JSON |
| `json:",string"` | Encode number/bool as JSON string |
| `db:"column"` | Database column mapping (sqlx, etc.) |
| `yaml:"name"` | YAML field name |
| `xml:"name,attr"` | XML attribute |
| `validate:"required"` | Struct validation (go-playground/validator) |

### Pointer vs value receivers

| Pointer `(s *Server)` | Value `(s Server)` |
| --- | --- |
| Method modifies the receiver | Receiver is small and immutable |
| Receiver contains `sync.Mutex` or similar | Receiver is a basic type (int, string) |
| Receiver is a large struct | Method is a read-only accessor |
| Consistency: if any method uses a pointer, all should | Map and function values (already reference types) |

### Dependency injection via interfaces

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

Tests pass a mock or stub satisfying `UserStore` — no real database needed.

### Zero value and generics

```go
func (r *Registry) Register(name string, item Item) {
    if r.items == nil {
        r.items = make(map[string]Item)
    }
    r.items[name] = item
}

// Generics over any for type-safe operations
func Contains[T comparable](slice []T, target T) bool { ... }
```

`any`/`interface{}` is reserved for true boundaries where the type is genuinely unknown (e.g., JSON decoding, reflection).

### `noCopy` for non-copyable structs

```go
// noCopy may be added to structs which must not be copied after first use.
type noCopy struct{}
func (*noCopy) Lock()   {}
func (*noCopy) Unlock() {}

type ConnPool struct {
    noCopy noCopy
    mu     sync.Mutex
    conns  []*Conn
}
```

`go vet` flags any copy of `ConnPool` (passed by value, assigned). This is the same technique the standard library uses for `sync.WaitGroup`, `sync.Mutex`, and `strings.Builder`. Always pass these by pointer.

## Watch for

| Mistake | Fix |
| --- | --- |
| Large interfaces (5+ methods) | Split into focused 1–3 method interfaces, compose if needed |
| Interfaces defined in the implementor package | Define where consumed |
| Returning interfaces from constructors | Return concrete types |
| Bare type assertions without comma-ok | Always use `v, ok := x.(T)` |
| Embedding when you only need a few methods | Named field and delegate explicitly |
| Missing field tags on serialized structs | Tag all exported fields in marshaled types |
| Mixing pointer and value receivers | Pick one and be consistent |
| Forgetting the compile-time check | Add `var _ Interface = (*Type)(nil)` |
| `ToString()` instead of `String()` | Honor canonical method names |
| Premature interface with one implementation | Start concrete, extract when needed |
| Nil map/slice in zero value struct | Lazy initialization in methods |
| `any` for type-safe operations | Generics (`[T comparable]`) instead |

## Cross-references

- → See `go-style` for interface naming conventions (Reader, Closer, Stringer)
- → See `go-patterns` for functional options, constructors, and builder patterns
- → See `go-dependency-injection` for DI patterns using interfaces
- → See `go-style` for value vs pointer function parameters (distinct from receivers)
- → See `go-data-structures` for generics vs `any` and struct composition choices

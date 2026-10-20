---
name: dev-design-patterns
description: Guides the agent in applying GoF design patterns, SOLID principles, and architectural patterns — choosing the right pattern for the right problem, never over-engineering.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **Senior Software Architect**. Your primary job is to choose the *right* pattern for the *actual* problem, then implement it cleanly. Never apply a pattern just to look sophisticated. Do NOT spawn a subagent for this.

Apply design patterns to: $ARGUMENTS

> **Apply the shared [engineering principles](../../resources/engineering-principles.md) throughout**, especially §3 (design patterns) and §4 (design for extension). The anti-pattern guard in §3 is mandatory — name the axis of change a pattern buys you before writing a single line.

---

## Step 0: Pattern Selection Gate
Before writing any code, answer these three questions in a brief note:
1. **What is the axis of change?** (What will vary independently?)
2. **Which pattern addresses that axis?** (See catalogue below.)
3. **What is the alternative without the pattern?** If the alternative is not clearly worse, use the simpler approach.

---

## Creational Patterns

### Factory Method
**Use when**: the type of object to create is determined at runtime, and the caller should not depend on the concrete type.
```typescript
// Good: new payment provider can be added without touching callers
interface PaymentProcessor { charge(amount: number): Promise<void> }
function createProcessor(type: 'stripe' | 'paypal'): PaymentProcessor { ... }
```
**Anti-pattern**: a factory with only one concrete product that never changes.

### Abstract Factory
**Use when**: you need to create *families* of related objects that must stay consistent (e.g., UI widget sets per theme/OS).
**Avoid when**: you have only one product family — Factory Method is enough.

### Builder
**Use when**: constructing a complex object requires many steps or optional parameters and the construction order matters.
```go
// Good: SQL query builder, HTTP request builder, test fixture builder
query := NewQueryBuilder().
    Select("id", "name").
    From("users").
    Where("active = true").
    Limit(10).
    Build()
```
**Avoid when**: the object has ≤4 fields — use named parameters / option structs instead.

### Singleton
**Use when**: exactly one instance is required and shared (DB connection pool, logger, config registry).
**Rules**: make it thread-safe (sync.Once in Go, module-level in Node.js/Python). Never use Singleton to avoid passing dependencies — use dependency injection instead.
**Anti-pattern**: Singleton as global mutable state. Every test that touches it becomes order-dependent.

### Prototype
**Use when**: creating a new object is expensive and a clone is cheaper (e.g., deep-copying a template object).

---

## Structural Patterns

### Adapter
**Use when**: you need to integrate a third-party interface that doesn't match your domain's interface. The adapter wraps the third-party code; your domain code sees only your interface.
```typescript
// Your domain
interface EmailSender { send(to: string, body: string): Promise<void> }
// Adapts SendGrid SDK to your interface
class SendGridAdapter implements EmailSender { ... }
```

### Decorator
**Use when**: you need to layer cross-cutting concerns (auth, logging, caching, rate-limiting) without modifying core logic.
```go
// Each layer wraps the next, adding one concern
func WithCache(next Handler) Handler { ... }
func WithAuth(next Handler) Handler { ... }
router.Handle("/", WithAuth(WithCache(businessHandler)))
```
**Avoid when**: you have only one concern — just put the logic in the function.

### Facade
**Use when**: a subsystem has many moving parts and callers only need a simplified view. The facade provides a single entry point.
**Avoid**: a facade that exposes every method of every subsystem — that is just an extra layer with no simplification.

### Proxy
**Use when**: you need controlled access to an object — lazy initialization, access control, remote stub, or caching. The proxy implements the same interface as the real subject.

### Composite
**Use when**: you have a tree structure where leaf nodes and composite nodes should be treated uniformly (file system, UI component trees, rule engines).

### Bridge
**Use when**: you have two independent axes of variation (e.g., shape + rendering engine) and want to extend each independently without a class explosion.

---

## Behavioral Patterns

### Strategy
**Use when**: one algorithm has several interchangeable implementations selected at runtime (pricing, sorting, export format, auth method).
```typescript
interface SortStrategy<T> { sort(items: T[]): T[] }
class ReportService {
  constructor(private sort: SortStrategy<Row>) {}
  generate(rows: Row[]) { return this.sort.sort(rows) }
}
```
**Anti-pattern**: a Strategy with only one implementation that never changes — use a plain function.

### Observer / Event Emitter
**Use when**: one change must trigger reactions in multiple decoupled components (domain events, webhooks, UI state updates).
```go
bus.Subscribe("order.placed", sendConfirmationEmail)
bus.Subscribe("order.placed", updateInventory)
bus.Publish("order.placed", order)
```
**Rules**: always define who owns the subscription lifecycle and how to unsubscribe (memory leaks in long-running processes).

### Command
**Use when**: you need to encapsulate a request as an object — for undo/redo, queuing, logging, or transactions.

### Template Method
**Use when**: several algorithms share the same skeleton but differ in specific steps. The base class defines the skeleton; subclasses override steps.
**Prefer over**: copy-pasted code with slight variations. But see below.
**Prefer Strategy instead when**: the variant parts need to be chosen at runtime or tested in isolation.

### Chain of Responsibility
**Use when**: a request should pass through a chain of handlers and each handler decides to process it or pass it on (middleware pipelines, validation chains, approval workflows).
```typescript
// Express middleware is a canonical Chain of Responsibility
app.use(authMiddleware)
app.use(validationMiddleware)
app.use(businessHandler)
```

### State
**Use when**: an object's behavior changes based on its internal state and the set of states is finite and well-defined (order lifecycle, connection state, document workflow).
**Avoid when**: the number of states is ≤2 and a boolean is readable — State adds real overhead.

### Iterator
**Use when**: you need to traverse a collection without exposing its structure. In modern languages, prefer built-in iterators / generators / `Iterable` protocols.

---

## Architectural Patterns (Cross-cutting)

### Repository
Isolate persistence behind an interface. Business logic calls `UserRepository.findById()` — it does not know about SQL, Redis, or REST. Enables unit testing without a DB.

### CQRS (Command Query Responsibility Segregation)
Separate write paths (commands that change state) from read paths (queries that return data). Justified when reads and writes have fundamentally different load, model, or consistency requirements. Overkill for simple CRUD.

### Event Sourcing
Store state as a sequence of immutable events; rebuild state by replaying them. Use only when audit trail, temporal queries, or event replay are a stated requirement — it adds significant complexity.

### Saga
Manage distributed transactions across services via a sequence of local transactions and compensating actions. Required in microservices where a 2-phase commit is not possible.

---

## SOLID Quick Reference
| Principle | Rule | Common Violation |
|---|---|---|
| **S**ingle Responsibility | One reason to change per class/module | Service that validates + persists + sends email |
| **O**pen/Closed | Add behavior by adding code, not editing existing | Giant `if type == X` switches |
| **L**iskov Substitution | Subtypes must be substitutable for their base | Override that throws where base didn't |
| **I**nterface Segregation | Small, focused interfaces | One interface with 15 methods; callers only need 2 |
| **D**ependency Inversion | Depend on abstractions, not concretions | Business logic that imports a DB package directly |

---

## Step 8: Verification (Definition of Done)
1. Named the axis of change (Step 0 gate passed).
2. The pattern is the simplest one that addresses the axis — no over-engineering.
3. Unit tests cover the pattern's behavior variation (each strategy, each state transition, each decorator combination).
4. No pattern is applied where a plain function/struct would do.

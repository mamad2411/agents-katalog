---
name: lyra-clean-code
description: Clean, testable code rules for TS, Python, PHP, Go, Rust, Java, C#, and Ruby. Use when writing, reviewing, or refactoring.
compatibility: No tools required. Language-agnostic examples.
---

# lyra-clean-code

## What it does

Twenty rules for code that is cheap to change and easy to test. Each rule ships a bad/good pair in a real language and ties back to testability — if a function resists a test, a rule is being broken somewhere. Use it while writing, reviewing, or refactoring. Cite the rule number in review, not your taste.
The rules cover naming, functions, SOLID, component cohesion, error handling, testability, and state.

## The rules

### 1. Reveal intent in every name

A name answers _what_, not _how_. If you need a comment to explain the name, the name failed.

```typescript
// bad:  const d = 3; // days since login
// good: const daysSinceLogin = 3;
```

### 2. Don't disinform with names

`accountList` that holds a `Map` lies about type. Vague beats misleading.

```typescript
// bad:  const accountList: Map<Id, Account> = new Map();
// good: const accounts: Map<Id, Account> = new Map();
```

### 3. Drop noise suffixes

`Data`, `Info`, `Helper`, `Manager`, `Processor` add zero information. Name what the thing actually does.

```typescript
// bad:  class UserDataManager { /* ... */ }
// good: class UserSerializer { /* ... */ }
```

### 4. Do one thing

If you can extract another function at a different level of abstraction, do it. Extract until you can't.

```python
# bad:  def process_order(o): total=...; email_if_vip(o,total); db.save(o); db.save(Invoice(total))
# good: def process_order(o): total=compute_total(o); persist(o, total)
```

### 5. Cap arguments at two

Three or more arguments signal a hidden object. Group them into a struct.

```typescript
// bad:  makeRect(x, y, w, h, color, border)
// good: makeRect(origin: Point, size: Size, style: Style)
```

### 6. Kill flag arguments

A boolean parameter means the function does two things. Split it into two named functions.

```typescript
// bad:  render(page, useCache: boolean)
// good: render(page); renderCached(page)
```

### 7. No hidden side effects

A function named `get*` or `is*` must not mutate state, write to disk, or fire HTTP. Side effects belong in verbs named for the effect.

```typescript
// bad:  function getUser(id) { const u = db.find(id); u.lastSeen = Date.now(); db.save(u); return u; }
// good: function getUser(id) { return db.find(id); }   // touchUserLastSeen(id) handles the write
```

### 8. One responsibility per class

A class has one reason to change. If two unrelated teams would edit it for unrelated reasons, split it.

```typescript
// bad:  class Report { calculate(); format(); email(); save(); }
// good: class Report { calculate(); } ; class ReportMailer { email(); }
```

### 9. Open for extension, closed for modification

Add behavior by adding a new type, not by editing a switch. New discount = new class, not new `case`.

```typescript
// bad:  function price(i) { switch (i.type) { case "book": return i.base*0.9; case "luxury": return i.base*1.2; } }
// good: class BookItem { price() { return this.base*0.9; } } ; class LuxuryItem { price() { return this.base*1.2; } }
```

### 10. Honor Liskov substitution

Subtypes must be usable wherever the base type is, with no surprises.

```typescript
// bad:  class Square extends Rectangle { setWidth(w) { super.setWidth(w); super.setHeight(w); } }
// good: class Square { setSide(s); area(); }   // doesn't pretend to be a Rectangle
```

### 11. Segregate fat interfaces

Clients depend only on the methods they call. Fat interfaces force clients to implement methods they don't use.

```typescript
// bad:  interface Worker { work(); eat(); }   // Robot must implement eat()
// good: interface Worker { work(); } ; interface Eater { eat(); }
```

### 12. Depend on abstractions, not concretions

High-level policy depends on interfaces. `new ConcreteRepo()` inside a domain service couples you to a detail.

```python
# bad:  def place(self, o): self._repo = PostgresOrderRepo(); self._repo.save(o)
# good: def place(self, o): self._repo.save(o)   # OrderRepo injected via __init__
```

### 13. Co-locate what changes together

Classes that change together live in the same package. Classes that change for unrelated reasons live apart.

```text
// bad:  billing/Invoice + shipping/InvoiceValidator   (both change on invoice rules)
// good: billing/Invoice + billing/InvoiceValidator
```

### 14. Break dependency cycles

If `A → B → C → A`, no module can be understood or released on its own. Break the cycle with an interface and inversion.

```text
// bad:  Orders → Invoices → Inventory → Orders
// good: Orders → Invoices → Inventory ; Inventory --(IInventoryEvents)--> Orders
```

### 15. Return results, not error codes

Error codes are silently ignorable. Use a Result, Option, or Exception type the caller is forced to handle.

```go
// bad:  func DeleteUser(id string) int { /* 0=ok, 1=not_found */ }
// good: func DeleteUser(id string) error { /* ... */ }
```

### 16. Never return null

Return an empty collection, `Option<T>`, `Result<T, E>`, or a Null Object. Null turns every caller into a defensive minefield.

```typescript
// bad:  function findUser(id: string): User | null
// good: function findUser(id: string): Option<User>
```

### 17. Never pass null

If a parameter can be null, you have two functions. Make the optional case explicit with overloads, option types, or sentinels.

```typescript
// bad:  setDiscount(code: string | null)
// good: setDiscount(code: string) ; clearDiscount()
```

### 18. If you can't test it first, the design is wrong

Before writing a function, write its test. If the test needs 5+ mocks, a real database, or a `sleep`, the design violates Rule 12 or Rule 4.

```typescript
// bad:  test("checkout", () => { new CheckoutService(); /* pulls db, stripe, mailgun */ });
// good: test("checkout", () => { new CheckoutService(fakeRepo, fakePay, fakeMail); });
```

### 19. Inject every dependency

No `new`, no `os.environ`, no `DateTime.now()`, no `Math.random()` inside business logic. Pure logic is testable logic.

```typescript
// bad:  function discountFor(u: User) { return new Date().getMonth() === 11 ? 0.2 : 0; }
// good: function discountFor(u: User, now: Date) { return now.getMonth() === 11 ? 0.2 : 0; }
```

### 20. Prefer immutability

Mutable shared state is the largest source of concurrency bugs. Make records immutable; copy-on-change.

```typescript
// bad:  let total = 0; items.forEach(i => { total += i.price; });
// good: const total = items.reduce((sum, i) => sum + i.price, 0);
```

---

_Part of the [skill collection](../README.md)._
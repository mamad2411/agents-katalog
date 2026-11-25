---
name: clean-code-principles
description: Write clean, readable, maintainable code following Robert Martin's principles. Use when writing any function, naming any variable, structuring any class, or reviewing code quality. This is the baseline for how code should look and feel — not just whether it works.
---

# Clean Code Principles

Drawn from: *Clean Code* (Robert C. Martin), *Software Engineering: A Practitioner's Approach* (Roger Pressman).

## Naming: The Most Important Thing

Names should reveal intent. If a name requires a comment to explain it, the name is wrong.

```typescript
// ❌ Bad — what is d? what is elapsed? elapsed what?
const d = 7;
function getThem(list: number[][]): number[][] {
  return list.filter(x => x[0] === 4);
}

// ✅ Good — reveals intent without a single comment
const DAYS_IN_WEEK = 7;
function getFlaggedCells(gameBoard: Cell[][]): Cell[][] {
  return gameBoard.filter(cell => cell.isFlagged());
}
```

**Rules:**
- Use names that reveal purpose: `elapsedTimeInDays`, not `d`
- Avoid disinformation: `accountList` should only be used if it IS a list
- Make names pronounceable and searchable — avoid single-letter variables except loop counters
- Classes: noun or noun phrase (`Customer`, `OrderProcessor`)
- Methods: verb or verb phrase (`sendEmail`, `deletePage`, `save`)
- Boolean names: `isLoaded`, `hasPermission`, `canDelete` — never `flag`, `status`, `ok`
- Don't encode types in names: `nameString` → `name`, `customerList` → `customers`

## Functions: Small, Focused, One Level of Abstraction

```typescript
// ❌ Bad — does too many things, mixes levels of abstraction
async function processOrder(orderId: string) {
  const order = await db.query(`SELECT * FROM orders WHERE id = '${orderId}'`);
  if (!order) return;
  const tax = order.total * 0.15;
  const grandTotal = order.total + tax;
  await db.execute(`UPDATE orders SET tax=${tax}, grand_total=${grandTotal} WHERE id='${orderId}'`);
  await fetch('/api/email', { method: 'POST', body: JSON.stringify({ to: order.email }) });
  console.log('done');
}

// ✅ Good — each function does one thing at one level of abstraction
async function processOrder(orderId: OrderId): Promise<void> {
  const order = await orderRepository.findById(orderId);
  if (!order) throw new NotFoundError('Order', orderId);
  await applyTax(order);
  await notifyCustomer(order);
}

async function applyTax(order: Order): Promise<void> {
  const tax = calculateTax(order.total);
  await orderRepository.updateTotals(order.id, tax);
}

function calculateTax(subtotal: Money): Money {
  return subtotal.multiply(TAX_RATE);
}
```

**Rules:**
- Functions should do **one thing** — if you can extract a meaningful sub-function, the function does more than one thing
- Maximum 3 arguments; prefer 0–2. If you need more, group into an object
- No boolean flag arguments — they signal the function does two things (`render(true)` → `renderForSuite()` + `renderForSingleTest()`)
- No side effects — a function named `checkPassword` should not also initialise a session
- Command-query separation: a function either *does something* (command) or *answers something* (query) — never both
- Functions should read top-to-bottom: callers above callees

## Comments: Only When the Code Cannot Speak

```typescript
// ❌ Bad — comment repeats what the code already says
// Increment i by 1
i++;

// ❌ Bad — commented-out code (delete it — that's what git is for)
// const oldResult = computeOld(x);
const result = computeNew(x);

// ✅ Good — explains WHY, not what; the code cannot say this itself
// We use 17 here because the legacy payment provider rejects values divisible by 5
// when processing international transactions. Remove when provider is upgraded.
const PAYMENT_CHUNK_SIZE = 17;

// ✅ Good — warns of non-obvious consequence
// This regex took 45 minutes to tune — do not simplify without running the full test suite
const VALID_EMAIL = /^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$/;
```

**Rules:**
- The best comment is a well-named function or variable
- Never explain *what* the code does — that's the code's job
- Always explain *why* if the reason is non-obvious
- Delete commented-out code — git remembers it
- No journal/author/date comments — that's git's job

## Error Handling as First-Class Concern

```typescript
// ❌ Bad — returns null, forces caller to remember to check
function findUser(id: string): User | null {
  return db.users.find(u => u.id === id) ?? null;
}
// Caller often forgets: const user = findUser(id); user.name // 💥

// ✅ Good — throw a typed error; caller handles explicitly or lets it propagate
function findUser(id: UserId): User {
  const user = db.users.find(u => u.id === id.value);
  if (!user) throw new NotFoundError('User', id.value);
  return user;
}

// ❌ Bad — error handling obscures business logic
try {
  const order = getOrder(id);
  try {
    const tax = computeTax(order);
    try {
      save(order, tax);
    } catch (e) { log(e); }
  } catch (e) { log(e); }
} catch (e) { log(e); }

// ✅ Good — separate error handling from business logic
async function processOrder(id: OrderId): Promise<void> {
  const order = await getOrder(id);
  const tax = computeTax(order);
  await save(order, tax);
}
// Error handling at the boundary (middleware, top-level handler)
```

**Rules:**
- Prefer exceptions over returning null or error codes
- Each exception type should be meaningful: `NotFoundError`, `ValidationError`, not generic `Error`
- Don't return null — throw or return a typed result
- Don't pass null as an argument — it forces defensive null checks everywhere
- Handle errors at the boundary (API middleware), not scattered throughout business logic

## Code Formatting: Vertical Density and Horizontal Clarity

```typescript
// ✅ Related concepts together, blank lines between unrelated groups
class OrderService {
  constructor(
    private readonly orders: OrderRepository,
    private readonly mailer: Mailer,
  ) {}

  async place(data: PlaceOrderData): Promise<Order> {
    const order = Order.create(data);
    await this.orders.save(order);
    await this.mailer.sendConfirmation(order);
    return order;
  }

  async cancel(id: OrderId): Promise<void> {
    const order = await this.orders.findById(id);
    order.cancel();
    await this.orders.save(order);
  }
}
```

**Rules:**
- Concepts that are closely related belong vertically close
- Caller functions above callee functions (top-down reading)
- Keep lines short enough to read without scrolling
- Consistent indentation and brace style (enforce via formatter — don't debate it)

## Testing: Tests Are Specification

From Pressman + Martin — tests are not an afterthought; they define what the code should do.

**F.I.R.S.T. principles:**
- **Fast** — tests run in milliseconds; slow tests don't get run
- **Independent** — no test depends on another; any test can run first
- **Repeatable** — same result every run, in any environment
- **Self-validating** — pass/fail, no manual inspection of output
- **Timely** — written before or alongside the code they test

```typescript
// ✅ One concept per test, clear name, clear assertion
describe('Order.cancel()', () => {
  it('should set status to cancelled', () => {
    const order = Order.create(validOrderData());
    order.cancel();
    expect(order.status).toBe(OrderStatus.Cancelled);
  });

  it('should throw if order is already shipped', () => {
    const order = shippedOrder();
    expect(() => order.cancel()).toThrow(InvalidOperationError);
  });
});
```

## Pressman's Software Engineering Checklist

From *Software Engineering: A Practitioner's Approach* — before shipping:

- [ ] Requirements are testable — each requirement has at least one acceptance test
- [ ] Design follows separation of concerns — layers don't bleed into each other
- [ ] Code has been reviewed (not just by the author)
- [ ] Tests cover the changed behaviour (not just legacy paths)
- [ ] Error handling is explicit at system boundaries
- [ ] Performance has been considered for the expected data volume
- [ ] The change is documented in the commit message with *why*, not just *what*

## The Clean Code Decision Filter

Before submitting any code, ask:

1. Does every name reveal its intent without needing a comment?
2. Does every function do exactly one thing?
3. Are errors handled explicitly, not swallowed or deferred with null?
4. Could a reader unfamiliar with this codebase understand this in under 2 minutes?
5. Is there a test that would catch a regression in this logic?

If any answer is no — fix it before the PR.

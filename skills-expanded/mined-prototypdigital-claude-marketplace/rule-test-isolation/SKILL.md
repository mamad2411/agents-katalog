---
name: test-isolation
description: Each test must set up and tear down its own state; never rely on execution order or shared mutable state
---

# Test Isolation

A test suite is only as reliable as its worst isolation failure. When tests share mutable state, the pass/fail of any test depends on which tests ran before it and in what order. Parallel runners, re-runs, and watch mode all break the implicit ordering — and with it, the signal.

## Rules

- **Each test creates its own fixtures.** Don't rely on `beforeAll` to seed data that tests modify. Use `beforeEach` or inline setup inside the test body so every run starts clean.
- **Reset all shared mutable state after each test.** Module-level variables, in-memory stores, and singletons that survive across tests are the most common source of order-dependent failures. Clear them in `afterEach` or use factory functions that return fresh instances.
- **Never assert the side-effects of a previous test.** If a test passes because an earlier test created a row in the database or set a flag, the tests have a hidden dependency. Each test must establish its own precondition.
- **Restore mocks and spies in `afterEach`.** A mock left on a module affects every subsequent test in the file. Configure `restoreMocks: true` globally or call `vi.restoreAllMocks()` / `jest.restoreAllMocks()` in `afterEach`.
- **Use test-scoped database transactions where possible.** For integration tests that hit a real database, wrap each test in a transaction and roll it back in `afterEach` — faster and cleaner than truncating tables.

## Examples

```ts
// BAD — tests share a module-level cart; order determines outcome
const cart = new Cart()

it('adds items to the cart', () => {
  cart.add({ id: 1, qty: 2 })
  expect(cart.items).toHaveLength(1)
})

it('calculates the total', () => {
  // Passes only if the previous test ran first
  expect(cart.total()).toBe(20)
})

// GOOD — each test builds its own cart
it('adds items to the cart', () => {
  const cart = new Cart()
  cart.add({ id: 1, qty: 2 })
  expect(cart.items).toHaveLength(1)
})

it('calculates the total', () => {
  const cart = new Cart()
  cart.add({ id: 1, qty: 2, price: 10 })
  expect(cart.total()).toBe(20)
})

// GOOD — integration test with transaction rollback
beforeEach(async () => {
  await db.beginTransaction()
})

afterEach(async () => {
  await db.rollbackTransaction()
})

it('persists the order', async () => {
  await orderService.create({ userId: 42, total: 100 })
  const order = await db.orders.findFirst({ where: { userId: 42 } })
  expect(order).toBeDefined()
})
```

## Enforcement

Isolation is a mechanical invariant — pin it in config so a forgotten `afterEach` cannot silently leak state: set `restoreMocks: true` (and `clearMocks: true`) globally, and run the suite with a randomized test order (`--sequence.shuffle` in Vitest, `--randomize` in Jest) in CI so order-dependent failures surface immediately instead of hiding behind a stable local order.

---
name: test-data-builders
description: Use factory or builder functions for test fixtures; never scatter inline object literals across the test suite
---

# Test Data Builders

Inline object literals duplicated across tests create a maintenance trap: when the shape of a domain object changes, every test that builds one manually breaks. A factory function is a single source of truth for a valid fixture. It accepts the fields the test cares about and fills in sensible defaults for everything else, so tests read as a list of what matters, not a wall of required fields.

## Rules

- **Use factory functions instead of inline literals.** A `createUser({ role: 'admin' })` call communicates intent. A 15-field object literal hides it. Build factories for every domain entity that appears in more than one test.
- **Factories provide valid defaults for every field.** The caller specifies only the fields relevant to the test. A test that has to supply `id`, `createdAt`, `updatedAt`, `email`, `name`, and `role` just to test one behavior is telling you the factory is missing.
- **Use the builder pattern for complex or stateful objects.** When the object has many optional variants or must be built in stages, a `new OrderBuilder().withLineItems([...]).withShipping('express').build()` is more readable than a factory with 12 optional parameters.
- **Never hardcode IDs or dates in literals across multiple tests.** Collisions between tests that use the same hardcoded `id: 1` cause order-dependent failures. Factories should generate unique IDs (incremental counter or sequential stub).
- **Keep factories in a shared `__fixtures__` or `test/factories` directory.** Co-locating factory files makes them discoverable and prevents duplication between test files in different directories.

## Examples

```ts
// BAD — inline literal repeated across tests
it('sends a confirmation email to admins', async () => {
  const user = {
    id: 1,
    name: 'Alice',
    email: 'alice@example.com',
    role: 'admin',
    createdAt: new Date('2024-01-01'),
    updatedAt: new Date('2024-01-01'),
    verified: true,
  }
  await notifyService.sendConfirmation(user)
  expect(emailClient.sent[0].to).toBe('alice@example.com')
})

// BAD — shape change breaks every test that duplicated the literal

// GOOD — factory with defaults; test specifies only what it cares about
// test/factories/user.ts
let nextId = 1
export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: nextId++,
    name: 'Test User',
    email: `user${nextId}@example.com`,
    role: 'member',
    createdAt: new Date('2024-01-15T12:00:00Z'),
    updatedAt: new Date('2024-01-15T12:00:00Z'),
    verified: true,
    ...overrides,
  }
}

// Test — only the relevant field is specified
it('sends a confirmation email to admins', async () => {
  const user = createUser({ role: 'admin', email: 'alice@example.com' })
  await notifyService.sendConfirmation(user)
  expect(emailClient.sent[0].to).toBe('alice@example.com')
})

// GOOD — builder for complex objects
const order = new OrderBuilder()
  .withLineItems([createLineItem({ productId: 'p1', qty: 2 })])
  .withShipping('express')
  .build()
```

---
name: coverage-meaningful-not-vanity
description: Assert observable behavior and edge cases; never write tests that execute code without asserting anything
---

# Coverage: Meaningful, Not Vanity

A line-coverage number tells you which lines were touched, not whether the software works. Tests that execute code without asserting outcomes inflate coverage metrics while providing no safety net — they are worse than no tests because they create false confidence. Coverage is a byproduct of writing good tests, not a target to hit.

## Rules

- **Every test must assert at least one observable outcome.** A test that calls a function and expects no errors is not a test — it is a proof that the code doesn't crash on the happy path. Assert return values, state changes, emitted events, or thrown errors.
- **Test behavior, not implementation.** Assertions on private methods, internal counters, or intermediate variables couple tests to the implementation. When you refactor, the tests break even though the behavior is unchanged.
- **Cover the edge cases that matter, not every line.** Focus assertions on boundary conditions, error paths, and invariants the caller depends on. A single well-chosen edge-case test delivers more signal than five happy-path tests.
- **Do not set line-coverage thresholds as a quality gate** unless you pair them with mutation testing or explicit edge-case review. A 90% coverage gate with no assertion quality standard is a vanity gate.
- **Delete tests that assert nothing.** A `it('runs without throwing')` test that exists to bump coverage is noise. Either add real assertions or remove the test.

## Examples

```ts
// BAD — executes code, asserts nothing meaningful
it('processes the payment', async () => {
  await processPayment({ amount: 100, card: validCard })
  // no assertions — just checks it doesn't throw
})

// BAD — asserts implementation detail, not behavior
it('calls the repository save method', async () => {
  const saveSpy = vi.spyOn(repo, 'save')
  await createUser({ name: 'Alice' })
  expect(saveSpy).toHaveBeenCalledTimes(1) // how, not what
})

// GOOD — asserts the observable outcome for the caller
it('returns the created user with an assigned id', async () => {
  const user = await createUser({ name: 'Alice' })
  expect(user.id).toBeDefined()
  expect(user.name).toBe('Alice')
})

// GOOD — covers an edge case that matters
it('throws InvalidCardError when the card is expired', async () => {
  await expect(
    processPayment({ amount: 100, card: expiredCard })
  ).rejects.toThrow(InvalidCardError)
})
```

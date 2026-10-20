---
name: test-naming
description: Name tests as "it does X when Y" — describe the behavior under a condition, not the implementation
---

# Test Naming

A failing test name is the first thing you read when CI breaks. If the name says `test_getUserById` you learn nothing until you open the file. If it says `returns 404 when the user does not exist` you know immediately what broke, what the expected behavior is, and where to look. Test names are documentation that updates itself — make them worth reading.

## Rules

- **Describe behavior, not method names.** The test name should complete the sentence "it ___". Avoid names that restate the function being called (`test_processPayment`, `should call save`).
- **Include the condition.** "returns an error" is ambiguous — "returns an error when the input is empty" pins the scenario. Use `when`, `if`, `given`, or `for` to introduce the condition.
- **Use plain language.** Abbreviations, internal names, and jargon obscure meaning. A new team member should understand the test name without reading the test body.
- **Group related cases with `describe` blocks.** Nest `describe('when the user is unauthenticated')` around the relevant `it` blocks rather than repeating the condition in every name.
- **Avoid `should`.** `it('should return 404')` is hedging. `it('returns 404')` is a fact. Write the fact.

## Examples

```ts
// BAD — restates the function name, no condition
describe('getUserById', () => {
  it('test_getUserById', async () => { ... })
  it('getUserById error case', async () => { ... })
})

// BAD — vague, no condition
it('should handle the payment', async () => { ... })
it('works correctly', () => { ... })

// GOOD — behavior + condition
describe('getUserById', () => {
  it('returns the user when the id exists', async () => { ... })
  it('returns null when the user does not exist', async () => { ... })
  it('throws AuthError when the caller is unauthenticated', async () => { ... })
})

// GOOD — grouped conditions
describe('processPayment', () => {
  describe('when the card is valid', () => {
    it('returns a success receipt with a transaction id', async () => { ... })
    it('deducts the amount from the card balance', async () => { ... })
  })

  describe('when the card is expired', () => {
    it('throws InvalidCardError', async () => { ... })
    it('does not deduct any amount', async () => { ... })
  })
})
```

## Enforcement

Naming conventions are best enforced by lint, not review memory: enable `eslint-plugin-jest`/`vitest` rules `valid-title` and `no-restricted-syntax` to reject titles starting with `should`, `test_`, or that merely restate the function name. A lint gate catches drift the moment it lands; a prose rule does not.

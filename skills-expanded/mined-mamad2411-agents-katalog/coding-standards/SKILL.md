---
name: coding-standards
description: Keep functions and components small, readable, and easy to reason about.
---

# Coding standards

**Why:** Deeply nested, multi-purpose functions hide bugs and make changes risky; small flat units are testable and reviewable in isolation.

## Function complexity

- Prefer small, single-purpose functions.
- Keep control flow shallow; avoid deep nesting.
- Use early returns and guard clauses to reduce `else` blocks.
- Extract complex logic into well-named helpers.

## Readability

- Favor descriptive names for functions, variables, and components.
- Avoid magic numbers/strings; use constants where appropriate.
- Keep conditionals straightforward; prefer `if (!condition) return` patterns.

## Examples

```ts
// BAD — deeply nested, hard to follow
function processOrder(order: Order) {
  if (order) {
    if (order.items.length > 0) {
      if (order.status === 'pending') {
        charge(order)
      } else {
        throw new Error('Not pending')
      }
    } else {
      throw new Error('No items')
    }
  } else {
    throw new Error('No order')
  }
}

// GOOD — early returns flatten the control flow
function processOrder(order: Order) {
  if (!order) throw new Error('No order')
  if (order.items.length === 0) throw new Error('No items')
  if (order.status !== 'pending') throw new Error('Not pending')
  charge(order)
}
```

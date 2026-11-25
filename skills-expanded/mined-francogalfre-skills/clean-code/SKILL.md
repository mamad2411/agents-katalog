---
name: clean-code
description: Refactors code to be cleaner, more readable, and easier to maintain — without changing behavior. Use when the user says "clean up this code", "refactor this", "this is messy", "improve readability", "simplify this function", "too many nested ifs", "make this more maintainable", or pastes code that works but is hard to read or understand.
---

# Clean Code

Refactors working code to be cleaner and more maintainable. Applies one
principle at a time — naming, function size, early returns, duplication,
magic values — and always preserves the original behavior exactly.

---

## Required Details

| Detail | Example |
|---|---|
| **Code to refactor** | Paste the code |
| **Language** | TypeScript / JavaScript / other |
| **Context** | What does this code do? |
| **Constraints** | Public API that can't change? Tests that must pass? |

---

## Instructions

### Step 1 — Identify the smells

| Smell | Signal |
|---|---|
| **Long function** | More than 20-30 lines, does multiple things |
| **Deep nesting** | More than 2-3 levels of if/for |
| **Magic values** | `if (status === 3)`, `timeout(5000)` |
| **Poor names** | `data`, `temp`, `x`, `handleThing` |
| **Duplication** | Same logic copy-pasted in 2+ places |
| **Boolean parameters** | `render(true)` — what does `true` mean? |
| **Long parameter list** | More than 3-4 params — use an options object |
| **Comments explaining what** | If you need a comment to explain *what*, rename instead |

### Step 2 — Apply targeted fixes

**Naming — the highest ROI refactor**
```ts
// ❌
const d = new Date();
const u = users.filter(x => x.a === true);
function calc(n: number) { ... }

// ✅
const today = new Date();
const activeUsers = users.filter(user => user.isActive);
function calculateMonthlyRevenue(amount: number) { ... }
```

**Early returns — remove nesting**
```ts
// ❌ Arrow anti-pattern — 4 levels deep
function processOrder(order) {
  if (order) {
    if (order.items.length > 0) {
      if (order.user.isVerified) {
        return charge(order);
      }
    }
  }
}

// ✅ Guard clauses — flat
function processOrder(order) {
  if (!order) return null;
  if (order.items.length === 0) return null;
  if (!order.user.isVerified) return null;
  return charge(order);
}
```

**Magic values — named constants**
```ts
// ❌
if (user.role === 2) { ... }
setTimeout(sync, 86400000);

// ✅
const ROLE_ADMIN = 2;
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

if (user.role === ROLE_ADMIN) { ... }
setTimeout(sync, ONE_DAY_MS);
```

**Long functions — extract until it reads like a sentence**
```ts
// ❌ One function doing three things
function submitOrder(cart) {
  // validate
  if (!cart.items.length) throw new Error('Empty cart');
  if (!cart.user.address) throw new Error('No address');
  // calculate
  const subtotal = cart.items.reduce((sum, i) => sum + i.price, 0);
  const tax = subtotal * 0.1;
  const total = subtotal + tax;
  // save
  db.orders.insert({ userId: cart.user.id, total });
}

// ✅ Each function does one thing
function submitOrder(cart) {
  validateCart(cart);
  const total = calculateOrderTotal(cart.items);
  saveOrder(cart.user.id, total);
}
```

**Options object — replace long param lists**
```ts
// ❌
function createUser(name, email, role, isActive, sendEmail) { ... }
createUser('Franco', 'f@x.com', 'admin', true, false);

// ✅
function createUser({ name, email, role, isActive, sendEmail }: CreateUserOptions) { ... }
createUser({ name: 'Franco', email: 'f@x.com', role: 'admin', isActive: true, sendEmail: false });
```

---

## Non-Negotiable Acceptance Criteria

- [ ] Behavior is identical before and after — no logic changes
- [ ] Every renamed variable/function is more descriptive than the original
- [ ] No new abstractions introduced unless they remove real duplication
- [ ] Refactored code has no deeper nesting than the original
- [ ] Each change is explained — "extracted X because it does one distinct thing"

---

## Output Format

~~~
## Refactored Code

```[language]
[clean version]
```

## Changes Made
- [change 1 and why]
- [change 2 and why]
- [...]

## What was NOT changed
[mention anything intentionally left as-is and why]
~~~
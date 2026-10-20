---
name: simplify
description: Reduce complexity without changing behavior — code simplification
---

# /simplify — Code Simplification

> "Complexity is the enemy of execution."

## Purpose

Simplify code for clarity and maintainability. Reduce complexity **without changing behavior**.

## When to Use

- After `/review` identifies complexity issues
- When code is hard to understand
- Before adding new features to tangled code
- During tech debt cleanup sprints

## Principles

### Chesterton's Fence

> Before removing something, understand why it exists.

Don't delete code just because it looks unnecessary. Investigate:
- Git history: `git log -p -- path/to/file`
- Related tests
- Comments or documentation
- Ask team members if unsure

### Rule of 500

If a function, file, or class exceeds ~500 lines, it likely needs splitting.

---

## Workflow

### Step 1: Identify Target

```bash
# Recently modified complex code
git diff --stat HEAD~10

# Or specify scope
# "Simplify the OrderService class"
```

### Step 2: Understand Before Changing

1. **Read the code** — What does it do?
2. **Check tests** — What behaviors are verified?
3. **Trace callers** — Who uses this code?
4. **Note edge cases** — Any special handling?

### Step 3: Identify Opportunities

| Pattern | Simplification |
|---------|---------------|
| Deep nesting (> 3 levels) | Guard clauses, extract helpers |
| Long functions (> 30 lines) | Split by responsibility |
| Nested ternaries | `if/else` or `switch` |
| Unclear names | Rename for clarity |
| Duplicated code | Extract shared function |
| Dead code | Remove entirely |
| Complex conditionals | Extract to named function |
| Magic numbers | Named constants |

### Step 4: Apply Incrementally

**One change at a time:**

```javascript
// Before: Deep nesting
function processOrder(order) {
  if (order) {
    if (order.items.length > 0) {
      if (order.status === 'pending') {
        // ... actual logic buried here
      }
    }
  }
}

// After: Guard clauses
function processOrder(order) {
  if (!order) return;
  if (order.items.length === 0) return;
  if (order.status !== 'pending') return;

  // ... actual logic at top level
}
```

**Run tests after each change.**

### Step 5: Validate

```bash
# All tests pass
npm test

# Build succeeds
npm run build

# Behavior unchanged (manual check if needed)
```

### Step 6: If Tests Fail

**Revert immediately.** Don't debug while mid-simplification.

```bash
git checkout -- .
```

Then:
1. Reassess the change
2. Make a smaller change
3. Or add missing tests first

---

## Common Simplifications

### Extract Guard Clauses

```javascript
// Before
function getDiscount(user) {
  if (user) {
    if (user.membership === 'premium') {
      return 0.2;
    } else {
      return 0.1;
    }
  }
  return 0;
}

// After
function getDiscount(user) {
  if (!user) return 0;
  if (user.membership === 'premium') return 0.2;
  return 0.1;
}
```

### Extract Named Functions

```javascript
// Before
const eligibleUsers = users.filter(u => 
  u.age >= 18 && u.verified && !u.banned && u.subscription !== 'free'
);

// After
const isEligible = (user) =>
  user.age >= 18 && 
  user.verified && 
  !user.banned && 
  user.subscription !== 'free';

const eligibleUsers = users.filter(isEligible);
```

### Replace Nested Ternary

```javascript
// Before
const status = isPaid ? (isShipped ? 'complete' : 'processing') : 'pending';

// After
function getOrderStatus(isPaid, isShipped) {
  if (!isPaid) return 'pending';
  if (!isShipped) return 'processing';
  return 'complete';
}
```

### Remove Dead Code

```javascript
// Before
function calculate(a, b) {
  // const oldResult = legacyCalculate(a, b);  // Commented out
  const result = a + b;
  // console.log('Debug:', result);  // Debug log
  return result;
}

// After
function calculate(a, b) {
  return a + b;
}
```

---

## Red Flags

Stop if you find yourself:

- Changing behavior while "simplifying"
- Unable to explain why code exists
- Simplifying without tests
- Making changes across unrelated files
- Creating new abstractions

---

## Output

- Simpler, clearer code
- All tests still passing
- Atomic commits with clear messages

## Next Step

Run `/review` to verify improvements.

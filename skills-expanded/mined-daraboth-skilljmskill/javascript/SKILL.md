---
name: javascript
description: Standards and patterns for writing clean, modern JavaScript — const/let (no var), async/await over .then chains, template literals, destructuring, and core fundamentals (closures, promises, scope). Use when the user writes or reviews JavaScript, asks to explain JS concepts (hoisting, event loop, this binding, prototypes), or builds browser/Node features in JS. Do not use for TypeScript-specific questions.
---

# Skill: JavaScript

> **Purpose**: Write clean, modern JavaScript. Master the fundamentals that matter.

## When to Use
- Writing or reviewing JavaScript code
- Explaining JS concepts (closures, async, promises)
- Building features or fixing JS bugs

---

## Core Fundamentals

### Variables
```javascript
const API_URL = 'https://api.example.com'; // Default — never changes
let retryCount = 0;                         // Only when reassignment needed
// Never use var — it's function-scoped and causes subtle bugs
```

### Closures
A function that remembers variables from its creation scope.
```javascript
function createCounter(start = 0) {
  let count = start;
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count,
  };
}
const counter = createCounter(10);
counter.increment(); // 11
counter.increment(); // 12
counter.getCount();  // 12
```
**When to use**: Private state, factory functions, event handlers with state.

### Promises & Async/Await
```javascript
// ❌ Callback hell
getUser(id, (user) => {
  getOrders(user.id, (orders) => {
    getDetails(orders[0].id, (details) => { /* nested mess */ });
  });
});

// ❌ .then() chains — better but still messy
getUser(id).then(user => getOrders(user.id)).then(orders => getDetails(orders[0].id));

// ✅ async/await — clean and readable
async function getUserOrderDetails(userId) {
  const user = await getUser(userId);
  const orders = await getOrders(user.id);
  const details = await getDetails(orders[0].id);
  return details;
}
```

### Destructuring
```javascript
// Objects
const { name, email, role = 'user' } = userData;

// Arrays
const [first, second, ...rest] = items;

// Function parameters
function createUser({ name, email, role = 'user' }) {
  return { id: generateId(), name, email, role };
}
```

---

## Clean Function Design

### Rules
1. **One job per function** — if you use "and" to describe it, split it
2. **Max 20 lines** — extract helpers if longer
3. **Descriptive names** — `calculateTotalPrice` not `calc`
4. **Return early** — avoid deep nesting

```javascript
// ❌ Deep nesting
function processOrder(order) {
  if (order) {
    if (order.items.length > 0) {
      if (order.status === 'pending') {
        // actual logic buried here
      }
    }
  }
}

// ✅ Early returns
function processOrder(order) {
  if (!order) throw new Error('Order is required');
  if (order.items.length === 0) throw new Error('Order has no items');
  if (order.status !== 'pending') return; // Nothing to process
  
  // Clean, flat logic here
  const total = calculateTotal(order.items);
  return submitOrder(order.id, total);
}
```

---

## Error Handling

```javascript
// Custom error for domain-specific failures
class ValidationError extends Error {
  constructor(field, message) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
  }
}

// Use it
function validateEmail(email) {
  if (!email) throw new ValidationError('email', 'Email is required');
  if (!email.includes('@')) throw new ValidationError('email', 'Invalid email format');
  return true;
}

// Catch specific errors
try {
  validateEmail(input);
} catch (error) {
  if (error instanceof ValidationError) {
    showFieldError(error.field, error.message);
  } else {
    console.error('Unexpected error:', error);
    throw error;
  }
}
```

---

## Example: Feature Implementation

**Task**: Build a simple task manager module.

```javascript
// taskManager.js
function createTaskManager() {
  const tasks = [];
  let nextId = 1;

  function addTask(title) {
    if (!title || title.trim() === '') {
      throw new Error('Task title cannot be empty');
    }
    const task = {
      id: nextId++,
      title: title.trim(),
      completed: false,
      createdAt: new Date().toISOString(),
    };
    tasks.push(task);
    return task;
  }

  function completeTask(id) {
    const task = tasks.find(t => t.id === id);
    if (!task) throw new Error(`Task ${id} not found`);
    task.completed = true;
    return task;
  }

  function getPending() {
    return tasks.filter(t => !t.completed);
  }

  function getSummary() {
    const total = tasks.length;
    const done = tasks.filter(t => t.completed).length;
    return { total, done, pending: total - done };
  }

  return { addTask, completeTask, getPending, getSummary };
}

// Usage
const manager = createTaskManager();
manager.addTask('Fix login bug');
manager.addTask('Write unit tests');
manager.completeTask(1);
console.log(manager.getSummary()); // { total: 2, done: 1, pending: 1 }
```

---

## Best Practices
1. **Use `const` by default** — switch to `let` only when needed
2. **Always handle errors** — never empty catch blocks
3. **Use array methods** — `map`, `filter`, `find`, `reduce` for data transforms
4. **Use template literals** — `` `Hello ${name}` `` not `"Hello " + name`
5. **Avoid mutation** — return new objects/arrays when possible

## Common Mistakes
| Mistake | Fix |
|---------|-----|
| Using `==` instead of `===` | Always use strict equality |
| Forgetting `await` | Missing await = working with Promise object, not value |
| Mutating function arguments | Clone first: `const copy = [...arr]` |
| Not handling Promise rejections | Always `.catch()` or try/catch with await |
| Using `this` in arrow functions | Arrow functions inherit `this` — use regular functions in classes |

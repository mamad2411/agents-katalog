---
name: javascript-patterns
description: Write idiomatic, reliable JavaScript following patterns from the Good Parts, functional composition, and module design. Use when writing JavaScript (not TypeScript-specific), reviewing JS code, or when the user asks about JS patterns, prototypes, closures, modules, or functional programming in JS.
---

# JavaScript Patterns

Drawn from: *JavaScript: The Good Parts* (Douglas Crockford), *Professional JavaScript for Web Developers* (Nicholas Zakas), *Programming JavaScript Applications* (Eric Elliott).

## The Good Parts: What to Use and What to Avoid

Crockford's core insight: JavaScript has brilliant parts and terrible parts. Use only the good parts.

### Avoid These (The Bad Parts)

```javascript
// ❌ == (type coercion) — always use ===
0 == ''       // true  (confusing)
0 == '0'      // true  (confusing)
'' == '0'     // false (inconsistent)
null == undefined  // true

// ✅ Always ===
0 === '' // false — correct

// ❌ with statement — banned in strict mode for good reason
with (obj) { x = 1; } // ambiguous scope

// ❌ eval — security risk, disables optimisations
eval('const x = ' + userInput); // ❌ never

// ❌ var — function-scoped, hoisted, leaks into outer scope
var x = 1;
// ✅ const by default, let when you need to rebind
const x = 1;
let counter = 0;

// ❌ Implicit globals
function bad() { x = 1; } // x leaks to global scope without var/let/const
// ✅ Always declare
function good() { const x = 1; }

// ❌ typeof null === 'object' — historical bug, work around it
if (typeof x === 'object') { ... } // passes for null too
// ✅
if (x !== null && typeof x === 'object') { ... }
```

## Closures: The Core Power of JS

A closure is a function that retains access to its outer scope after the outer function has returned.

```javascript
// ✅ Module pattern using closure — private state, public interface
function makeCounter(initial = 0) {
  let count = initial; // private — not accessible from outside

  return {
    increment() { count++; },
    decrement() { count--; },
    value() { return count; },
  };
}

const counter = makeCounter(10);
counter.increment();
counter.value(); // 11
// count is not accessible — it's private

// ✅ Closure for memoization
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}
```

## Module Pattern (ES Modules)

Elliott's principle: modules are the unit of reuse. Design around clean module interfaces.

```javascript
// ✅ ES module — explicit imports and exports, static analysis
// orderService.js
import { OrderRepository } from './orderRepository.js';
import { calculateTax } from './tax.js';

export async function placeOrder(data) {
  const order = createOrder(data);
  const tax = calculateTax(order.subtotal);
  await OrderRepository.save({ ...order, tax });
  return order;
}

// ❌ Avoid default exports for utilities — named exports are easier to refactor
export default function process() { ... } // hard to rename across codebase
export function processOrder() { ... }    // ✅ named — explicit and renameable
```

**Module design rules (Elliott):**
- One responsibility per module
- Export only the public interface — keep implementation private
- Prefer many small modules over one large file
- Avoid circular dependencies — they signal a design problem

## Functional Patterns

Elliott's *Programming JavaScript Applications* is built on functional composition.

### Pure Functions

```javascript
// ❌ Impure — depends on and mutates external state
let total = 0;
function addToTotal(amount) {
  total += amount; // side effect
  return total;
}

// ✅ Pure — same input always produces same output, no side effects
function add(a, b) { return a + b; }
```

### Composition

```javascript
// ✅ Compose small functions into larger behaviour
const compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x);
const pipe    = (...fns) => x => fns.reduce((v, f) => f(v), x);

const processUser = pipe(
  validateUser,
  normaliseEmail,
  hashPassword,
  saveUser,
);

// ✅ Partial application
function multiply(a) {
  return function(b) { return a * b; }
}
const double = multiply(2);
const triple = multiply(3);
double(5); // 10
triple(5); // 15
```

### Immutability

```javascript
// ❌ Mutating arrays and objects — causes hard-to-trace bugs
function addItem(cart, item) {
  cart.push(item); // mutates the original
  return cart;
}

// ✅ Return new values — original is unchanged
function addItem(cart, item) {
  return [...cart, item];
}

function updateUser(user, changes) {
  return { ...user, ...changes }; // new object, original unchanged
}
```

## Prototypal Inheritance — Crockford's Way

Prefer object composition over class hierarchies.

```javascript
// ❌ Deep class inheritance — brittle, hard to change base class
class Animal { speak() { ... } }
class Dog extends Animal { fetch() { ... } }
class GuideDog extends Dog { guide() { ... } }

// ✅ Compose behaviour from mixins
const canSpeak  = (state) => ({ speak:  () => `${state.name} speaks` });
const canFetch  = (state) => ({ fetch:  () => `${state.name} fetches` });
const canGuide  = (state) => ({ guide:  () => `${state.name} guides` });

function createGuideDog(name) {
  const state = { name };
  return Object.assign({}, canSpeak(state), canFetch(state), canGuide(state));
}

const rex = createGuideDog('Rex');
rex.speak();  // Rex speaks
rex.guide();  // Rex guides
```

## Event Handling (Zakas)

```javascript
// ✅ Delegate events to a common ancestor — avoid attaching to every child
document.querySelector('#list').addEventListener('click', (event) => {
  const item = event.target.closest('[data-id]');
  if (!item) return;
  handleItemClick(item.dataset.id);
});

// ✅ Clean up event listeners to prevent memory leaks
const handler = () => doSomething();
element.addEventListener('click', handler);
// later:
element.removeEventListener('click', handler); // same reference required
```

## Async Patterns (ES2017+)

```javascript
// ✅ async/await over promise chains for readability
async function loadUser(id) {
  try {
    const user = await userApi.get(id);
    const orders = await orderApi.getByUser(user.id);
    return { user, orders };
  } catch (error) {
    logger.error('Failed to load user', { id, error });
    throw error; // re-throw — don't swallow
  }
}

// ✅ Parallel where there's no dependency
async function loadDashboard(userId) {
  const [user, orders, notifications] = await Promise.all([
    userApi.get(userId),
    orderApi.getByUser(userId),
    notificationApi.getByUser(userId),
  ]);
  return { user, orders, notifications };
}

// ❌ Sequential when parallel is possible
const user = await userApi.get(userId);          // waits
const orders = await orderApi.getByUser(userId); // then waits again
```

## Type Coercion — Know What JS Does

```javascript
// Truthy / falsy values
// Falsy: false, 0, '', null, undefined, NaN
// Everything else: truthy (including '0', [], {})

// ✅ Explicit boolean conversion
if (value !== null && value !== undefined) { ... }
if (Boolean(value)) { ... }

// ❌ Implicit coercion surprises
if (value) { ... } // passes for '0', [], {} — may be wrong

// ✅ String conversion
String(123)     // '123'
(123).toString() // '123'

// ❌ Accidental string concatenation
'5' + 3  // '53' — not 8
// ✅ Explicit
Number('5') + 3 // 8
parseInt('5', 10) + 3 // 8
```

## JS Code Quality Checklist

- [ ] `===` everywhere — no `==`
- [ ] `const` by default, `let` only when rebinding, never `var`
- [ ] No `eval`, no `with`
- [ ] Functions are pure where possible — no hidden side effects
- [ ] Mutations return new values (spread/Object.assign) rather than mutating in place
- [ ] Async paths use `try/catch` — errors are never silently swallowed
- [ ] Event listeners are removed when components/elements are destroyed
- [ ] Modules have a single clear responsibility and a small public interface
- [ ] No implicit globals — strict mode enabled (`'use strict'` or ES modules)

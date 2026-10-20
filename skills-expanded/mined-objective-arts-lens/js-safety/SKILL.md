---
name: js-safety
description: "JS Good Parts"
---

# Douglas Crockford JavaScript Philosophy

Applying Douglas Crockford's defensive JavaScript philosophy from "JavaScript: The Good Parts" and JSLint. The language has good parts and bad parts—use only the good parts.

---

## Core Philosophy

### The Good Parts Exist

JavaScript has more bad parts than good parts. Professional JavaScript means knowing which parts to avoid entirely.

> "JavaScript is the only language people feel they don't need to learn before using."

### Subset Is Sufficient

You don't need all of JavaScript. A disciplined subset produces better programs than the full language.

---

## The Bad Parts (Avoid Entirely)

### Global Variables

```javascript
// BAD: Implicit global
function bad() {
  x = 5;  // Creates global!
}

// GOOD: Explicit scope
function good() {
  const x = 5;
}
```

### == vs ===

```javascript
// BAD: Type coercion chaos
'' == '0'           // false
0 == ''             // true
0 == '0'            // true
false == 'false'    // false
false == '0'        // true

// GOOD: Always use ===
if (value === expected) { ... }
```

### with Statement

```javascript
// NEVER use with - ambiguous scope
with (obj) {
  a = b;  // Is this obj.a = obj.b? obj.a = b? a = obj.b?
}
```

### eval

```javascript
// NEVER use eval - security and performance disaster
eval(userInput);  // Code injection vulnerability

// Also avoid: new Function(), setTimeout with strings
setTimeout("doThing()", 100);  // BAD
setTimeout(doThing, 100);       // GOOD
```

### Bitwise Operators

```javascript
// Avoid in most cases - rarely needed, often confused with logical
if (a & b) { }   // Bitwise AND - probably meant &&
if (a | b) { }   // Bitwise OR - probably meant ||
```

---

## The Good Parts (Use These)

### Functions as First-Class Objects

```javascript
// Functions are values
const double = x => x * 2;
const numbers = [1, 2, 3].map(double);

// Closures for encapsulation
function counter() {
  let count = 0;
  return {
    increment: () => ++count,
    get: () => count
  };
}
```

### Object Literals

```javascript
// Simple, readable object creation
const point = {
  x: 10,
  y: 20,
  distance(other) {
    return Math.sqrt(
      Math.pow(this.x - other.x, 2) +
      Math.pow(this.y - other.y, 2)
    );
  }
};
```

### Array Methods

```javascript
// Functional iteration - no manual loops
const adults = people
  .filter(p => p.age >= 18)
  .map(p => p.name)
  .sort();
```

### Module Pattern

```javascript
// Encapsulation through closures
const myModule = (function() {
  // Private
  let privateVar = 0;
  function privateMethod() { }

  // Public API
  return {
    publicMethod() {
      privateMethod();
      return privateVar;
    }
  };
})();
```

---

## Defensive Patterns

### Fail Fast

```javascript
function divide(a, b) {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new TypeError('Arguments must be numbers');
  }
  if (b === 0) {
    throw new RangeError('Cannot divide by zero');
  }
  return a / b;
}
```

### Default Parameters

```javascript
// Guard against undefined
function greet(name = 'Guest') {
  return `Hello, ${name}`;
}
```

### Object.freeze for Constants

```javascript
const CONFIG = Object.freeze({
  API_URL: 'https://api.example.com',
  TIMEOUT: 5000
});
// CONFIG.API_URL = 'x';  // Throws in strict mode
```

---

## JSLint Rules (Apply These)

1. **Declare variables at top of function**
2. **One var/let/const per declaration**
3. **Always use braces for blocks**
4. **No fallthrough in switch**
5. **Strict equality only (===, !==)**
6. **No bitwise unless intentional**
7. **No eval, with, or implied globals**

---

## When to Apply

| Scenario | Apply Crockford |
|----------|-----------------|
| Legacy JS codebase | Yes - identify bad parts |
| Code review | Yes - flag dangerous patterns |
| New utility library | Yes - defensive style |
| Modern React/Vue | Partially - frameworks have own conventions |
| TypeScript | Less critical - types catch many issues |

---

## Source Material

- "JavaScript: The Good Parts" (2008)
- JSLint and its documentation
- Crockford on JavaScript (video series)
- JSON specification (Crockford invented JSON)

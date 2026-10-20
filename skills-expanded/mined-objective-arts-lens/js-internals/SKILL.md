---
name: js-internals
description: Deep JavaScript language mechanics from "You Don't Know JS" philosophy. Use for debugging closures, this binding, prototype chains, coercion bugs, or async execution mysteries. Triggers on complex JS runtime behavior, scope issues, "why does JavaScript do this?", unexpected this binding.
---

# Kyle Simpson (YDKJS) JavaScript Philosophy

Deep JavaScript language mechanics expertise based on Kyle Simpson's "You Don't Know JS" philosophy. Understanding what JavaScript actually does under the hood - closures, scope, this binding, prototypes, coercion, and async patterns at the engine level.

Applying Kyle Simpson's deep JavaScript philosophy when debugging complex runtime behavior, understanding scope chain resolution, diagnosing `this` binding issues, explaining prototype delegation, or when abstraction leaks cause unexpected behavior. Use this when surface-level JavaScript knowledge is insufficient and true language mechanics understanding is required.

**Triggers:**
- Complex closure debugging or memory leak investigation
- Unexpected `this` binding behavior
- Prototype chain confusion or inheritance issues
- Coercion bugs or type conversion surprises
- Async execution order mysteries
- "Why does JavaScript do this?" questions
- Debugging transpiled/bundled code behavior differences

**Anti-triggers:**
- Simple syntax questions (use MDN)
- Framework-specific patterns (use framework docs)
- Build tooling configuration
- CSS/HTML questions

---

## Philosophy

### Core Principles (YDKJS)

1. **Know the language, not just the patterns** - Understand WHY code works, not just that it works
2. **Embrace JavaScript as it is** - Don't fight the language; understand its design decisions
3. **Abstraction leaks are bugs in understanding** - When abstractions fail, language knowledge saves you
4. **Mental models must match engine behavior** - Your understanding should predict what JavaScript will do

### The Three Pillars

**Scope & Closures**
- Lexical scope is determined at author time, not runtime
- Closures are functions that remember their lexical scope
- The scope chain is a one-way lookup (inner → outer)
- Block scope (let/const) vs function scope (var)

**this & Object Prototypes**
- `this` is determined by call-site, not definition site
- Four rules in order: new > explicit > implicit > default
- Prototype is delegation, not inheritance (objects link to other objects)
- `[[Prototype]]` chain lookup happens on property access

**Types & Coercion**
- JavaScript has types; variables don't have types, values do
- Coercion is not evil; implicit coercion can be readable when understood
- `==` uses coercion, `===` doesn't - know when each is appropriate
- Falsy values: `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN`

---

## Diagnostic Framework

### Debugging `this` Binding

```javascript
// Ask these questions in order:
// 1. Was the function called with `new`? → this = newly constructed object
// 2. Was it called with call/apply/bind? → this = specified object
// 3. Was it called with a context object? → this = that object
// 4. None of the above? → this = undefined (strict) or globalThis (sloppy)

// Arrow functions: lexical this (inherits from enclosing scope)
```

### Debugging Closures

```javascript
// Closure = function + its lexical environment
// Common gotcha: loop variable capture

// Bug:
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100); // prints 3, 3, 3
}

// Fix 1: let creates new binding per iteration
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100); // prints 0, 1, 2
}

// Fix 2: IIFE creates new scope
for (var i = 0; i < 3; i++) {
  ((j) => setTimeout(() => console.log(j), 100))(i);
}
```

### Debugging Prototype Chain

```javascript
// Object.create(proto) - creates object with [[Prototype]] = proto
// obj.hasOwnProperty(prop) - checks own properties only
// prop in obj - checks entire prototype chain
// Object.getPrototypeOf(obj) - gets [[Prototype]]

// Shadowing: own property hides prototype property
// Delegation: property lookup walks up [[Prototype]] chain
```

### Debugging Coercion

```javascript
// ToString: null→"null", undefined→"undefined", true→"true"
// ToNumber: ""→0, "  "→0, null→0, undefined→NaN, true→1
// ToBoolean: falsy values→false, everything else→true

// Abstract equality (==) coercion rules:
// string == number → ToNumber(string) == number
// boolean == anything → ToNumber(boolean) == anything
// null == undefined → true (special case)
// object == primitive → ToPrimitive(object) == primitive
```

---

## Deep Dive Patterns

### Scope Resolution

```
Global Scope
  └─ Outer Function Scope
      └─ Inner Function Scope
          └─ Block Scope (let/const)

Lookup: Inner → Outer → Global → ReferenceError
```

### Event Loop Mental Model

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Call Stack  │ ←── │ Event Loop  │ ←── │ Task Queue  │
└─────────────┘     └─────────────┘     └─────────────┘
                          ↑
                    ┌─────────────┐
                    │ Microtask   │ (Promises, queueMicrotask)
                    │ Queue       │ (drained between tasks)
                    └─────────────┘

Order: Sync code → All microtasks → One macrotask → Repeat
```

### `this` Binding Decision Tree

```
Was `new` used?
├─ Yes → this = new object
└─ No → Was call/apply/bind used?
    ├─ Yes → this = specified object (unless null/undefined in strict)
    └─ No → Is there a context object (obj.fn())?
        ├─ Yes → this = context object
        └─ No → Is it strict mode?
            ├─ Yes → this = undefined
            └─ No → this = globalThis

Arrow function? → Inherits this from enclosing scope (lexical)
```

---

## Anti-Patterns to Recognize

### Misunderstanding Hoisting

```javascript
// Mental model: declarations move to top, assignments stay
// Reality: functions fully hoisted, var declarations hoisted (value undefined)

console.log(foo); // undefined (var hoisted)
console.log(bar); // ReferenceError (let TDZ)
var foo = 1;
let bar = 2;
```

### Confusing Prototype with Class Inheritance

```javascript
// JavaScript has delegation, not classical inheritance
// Objects delegate to other objects via [[Prototype]]
// Class syntax is syntactic sugar over prototype delegation

// This is NOT copying properties:
class Child extends Parent {}
// This is linking Child.prototype.[[Prototype]] = Parent.prototype
```

### Relying on Implicit Globals

```javascript
// In sloppy mode, undeclared assignment creates global
function leak() {
  oops = "I'm global now"; // No var/let/const = global property
}
// Always use strict mode: "use strict";
```

---

## Debugging Checklist

When JavaScript behaves unexpectedly:

1. [ ] What is `this` at the call-site? (Not definition site)
2. [ ] Is there a closure capturing a variable? What's its current value?
3. [ ] Is coercion happening? What types are actually involved?
4. [ ] Is the prototype chain being traversed? Check `hasOwnProperty`
5. [ ] Is this sync or async? What's the event loop state?
6. [ ] Am I in strict mode? Behavior differs significantly
7. [ ] Is TDZ (Temporal Dead Zone) involved with let/const?
8. [ ] Could hoisting be affecting execution order?

---

## Resources

- YDKJS Book Series: https://github.com/getify/You-Dont-Know-JS
- Kyle's talks on Frontend Masters
- ECMAScript specification for authoritative behavior

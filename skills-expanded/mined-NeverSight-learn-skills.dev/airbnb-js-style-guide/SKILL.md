---
name: airbnb-js-style-guide
description: Enforces Airbnb JavaScript Style Guide when writing JS, JSX, or TypeScript code. This skill should be used whenever writing, reviewing, or generating JavaScript, JSX, or TypeScript code to ensure it follows Airbnb's coding standards for variables, functions, classes, modules, naming, formatting, and React/JSX patterns.
---

# Airbnb JavaScript Style Guide

This skill enforces the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript) for all JS, JSX, and TypeScript code. Apply every rule below without exception unless the user explicitly overrides a specific rule.

## When to Apply

Apply these rules whenever you:

- Write new JavaScript, TypeScript, or JSX/TSX files
- Modify existing JS/TS/JSX code
- Review code for correctness and style
- Refactor or clean up existing code
- Generate code snippets or examples

## Quick Rule Reference

### References

```js
// Bad
var count = 1;
if (true) { var name = 'bad'; }

// Good
const count = 1;
let name;
if (true) { name = 'good'; }
```

- **Always use `const`** by default. Use `let` only when reassignment is needed. **Never use `var`.**

### Objects

```js
// Bad
const item = new Object();
const obj = { a: a, b: b };
const copy = Object.assign({}, original);

// Good
const item = {};
const obj = { a, b };
const copy = { ...original };
```

- Literal syntax `{}`, property shorthand, spread over `Object.assign`.

### Arrays

```js
// Bad
const arr = new Array();
arr[arr.length] = 'x';
const copy = arr.slice();

// Good
const arr = [];
arr.push('x');
const copy = [...arr];
```

### Destructuring

```js
// Bad
const first = arr[0];
const name = user.name;
const age = user.age;

// Good
const [first] = arr;
const { name, age } = user;

// Multiple return values → object destructuring
function getRange() { return { min: 0, max: 100 }; }
const { min, max } = getRange();
```

### Strings

```js
// Bad
const name = "Bob";
const greeting = 'Hello, ' + name + '!';

// Good
const name = 'Bob';
const greeting = `Hello, ${name}!`;
```

- **Single quotes** for strings. **Template literals** for interpolation/multiline.

### Functions

```js
// Bad
function foo() { ... }          // declaration — use expression instead
const f = function() { ... };   // anonymous — name it
function bar(opts) { opts = opts || {}; }  // mutating params

// Good
const foo = function foo() { ... };
const bar = (opts = {}) => { ... };
```

- Named function expressions over declarations. Default parameters, not mutation. Never use `arguments` — use rest `...args`.

### Arrow Functions

```js
// Bad
[1, 2, 3].map(function(x) { return x * x; });
[1, 2, 3].map((x) => { return x * x; });  // unnecessary block body

// Good
[1, 2, 3].map((x) => x * x);
[1, 2, 3].map((x) => ({ key: x }));       // returning object: wrap in ()
```

- Always include parentheses around parameters: `(x) => x`, not `x => x`.

### Classes

```js
// Bad
function Queue() { this.items = []; }
Queue.prototype.push = function(item) { this.items.push(item); };

// Good
class Queue {
  constructor() { this.items = []; }
  push(item) { this.items.push(item); }
}
class PriorityQueue extends Queue { ... }
```

- Use `class` and `extends`. Avoid empty constructors. No duplicate class members.

### Modules

```js
// Bad
const styleGuide = require('./styleGuide');
module.exports = styleGuide.default;

import * as all from './all';          // no wildcard
export { foo as default } from './foo'; // no re-export from import

// Good
import styleGuide from './styleGuide';
export default styleGuide;
import { named } from './module';
```

- ES `import`/`export` only. No wildcard imports. One import per path. Imports above all other statements.

### Iterators

```js
// Bad
for (let i = 0; i < arr.length; i++) { ... }
for (const key in obj) { ... }

// Good
arr.forEach((item) => { ... });
arr.map((item) => item.name);
arr.filter((item) => item.active);
arr.reduce((acc, item) => acc + item, 0);
Object.keys(obj).forEach((key) => { ... });
```

- Prefer higher-order functions over `for`/`for-in`/`for-of` loops.

### Variables

```js
// Bad
let a = 1, b = 2;
let a; const b = 1;   // mixed, group them
const foo = a = b = 1; // chained assignment

// Good
const b = 1;
const c = 2;
let a;
let d;
```

- One declaration per variable. Group `const` then `let`. No chained assignment. No `++`/`--`.

### Comparison

```js
// Bad
if (name == 'test') { ... }
if (isValid == true) { ... }
if (collection.length > 0) { ... }

// Good
if (name === 'test') { ... }
if (isValid) { ... }
if (collection.length) { ... }
```

- **Always `===` and `!==`**. Shorthand for booleans; explicit for strings/numbers.

### Blocks

```js
// Bad
if (test) return false;
if (test) {
  thing();
} else {
  thing2();
}

// Good
if (test) {
  return false;
}
if (test) {
  thing();
} else {
  thing2();
}
```

- Braces for all multiline blocks. `else` on same line as closing `}`.

### Comments

```js
// Bad
/* This function does xyz */
function foo() { // returns early }

// Good
/**
 * Calculates the sum of two numbers.
 */
function add(a, b) {
  // handle negative input
  return a + b;
}
// TODO: extract this into a utility
// FIXME: this breaks for floats
```

- `/** */` for multiline. `//` single-line above subject. Use `// FIXME:` and `// TODO:`.

### Whitespace & Formatting

```js
// Bad
function foo(){return 1;}
const x=1+2;
if(x){...}
import {a,b} from 'c';

// Good
function foo() { return 1; }
const x = 1 + 2;
if (x) { ... }
import { a, b } from 'c';
```

- 2-space soft tabs. Space before `{`. Space after keywords. Operators surrounded by spaces. Lines ≤ 100 chars. Spaces inside `{ }` for imports/exports. No spaces inside `()` or `[]`. Trailing newline at EOF.

### Commas & Semicolons

```js
// Bad
const a = 1
const b = 2
const obj = {
    a: 1
  , b: 2  // leading comma
}

// Good
const a = 1;
const b = 2;
const obj = {
  a: 1,
  b: 2,   // trailing comma
};
```

- **No leading commas. Always trailing commas.** Always semicolons.

### Naming Conventions

```js
// Bad
const OBJEcttsssss = {};
const this_is_bad = {};
function q() {}
const _privateField = 1;  // no leading underscores
const self = this;        // use arrow functions

// Good
const thisIsGood = {};
function longDescriptiveName() {}
class UserAccount {}
const HTTP_STATUS_OK = 200;  // SCREAMING_SNAKE for constants
```

- `camelCase` for variables, functions, instances. `PascalCase` for classes/constructors. `SCREAMING_SNAKE_CASE` for true constants. Filename matches default export name. No leading/trailing underscores.

### Type Casting

```js
// Bad
const totalScore = new String(this.reviewScore);
const val = new Number(inputValue);

// Good
const totalScore = String(this.reviewScore);
const val = Number(inputValue);
const hasAge = Boolean(age);  // or !!age
const num = parseInt(value, 10);  // always specify radix
```

## JSX / React Rules

See detailed rules in `rules/jsx-rules.md`.

**Key JSX rules:**
- One component per file (multiple stateless OK). `.jsx` extension for components.
- `PascalCase` for component names and files; `camelCase` for instances.
- Double quotes for JSX attributes; single quotes for JS inside JSX.
- Always include `alt` on `<img>`. Use stable keys (not array index).
- Self-close tags with no children: `<Foo />`.
- Wrap multi-line JSX in parentheses.
- Bind event handlers in constructor, not in render.
- No `displayName`. No mixins. No string refs.

## TypeScript Rules

See detailed rules in `rules/typescript-rules.md`.

**Key TS rules:**
- Use `interface` for object shapes; `type` for unions, intersections, and aliases.
- Prefer explicit return types on exported functions.
- Never use `any` — use `unknown` if type is truly unknown.
- Use `readonly` for properties that should not be mutated.
- Prefer optional chaining `?.` and nullish coalescing `??` over manual null checks.
- Use enums only for string enums; prefer string union types for simple cases.

## Enforcement Summary

| Rule | Requirement |
|------|-------------|
| `var` | Never — use `const`/`let` |
| Quotes | Single (JS), Double (JSX attributes) |
| Semicolons | Always |
| Indentation | 2 spaces |
| Line length | ≤ 100 chars |
| Equality | `===`/`!==` always |
| Trailing commas | Always (multi-line) |
| Arrow functions | Always for callbacks |
| `import`/`export` | ES modules only |
| Naming | camelCase / PascalCase / SCREAMING_SNAKE |

## References

- Full guide: https://github.com/airbnb/javascript
- React/JSX guide: https://github.com/airbnb/javascript/tree/master/react
- Detailed rules: `rules/core-rules.md`
- JSX rules: `rules/jsx-rules.md`
- TypeScript rules: `rules/typescript-rules.md`

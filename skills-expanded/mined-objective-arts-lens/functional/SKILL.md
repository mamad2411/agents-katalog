---
name: functional
description: "Functional JS elegance"
---

# Jeremy Ashkenas JavaScript Philosophy

Applying the design philosophy of Jeremy Ashkenas (Backbone.js, Underscore.js, CoffeeScript) to JavaScript library and utility development. Use this when writing JavaScript utilities, designing APIs, building small libraries, or refactoring code toward functional elegance. Auto-invokes for .js files involving utility functions, library design, collection manipulation, or API surface design. Not for framework-heavy code (React, Angular), build tooling, or Node.js server infrastructure.

---

## Core Philosophy

### The Ashkenas Aesthetic

**Readable over clever.** Code is read far more than written. Optimize for the reader who encounters your code six months from now.

**Small, focused functions.** Each function does one thing. Name it for what it does. If the name is awkward, the function does too much.

**Functional foundations.** Prefer `map`, `filter`, `reduce` over loops. Treat data as immutable. Return new values rather than mutating.

**Minimal API surface.** The best library is the smallest one that solves the problem. Every public method is a promise to maintain.

**Convention over configuration.** Establish sensible defaults. Let users override when needed, not require configuration upfront.

---

## Design Patterns

### The Underscore Pattern: Collection-First Thinking

```javascript
// Transform collections, not items
const getActiveUserEmails = (users) =>
  users
    .filter(user => user.active)
    .map(user => user.email);

// Not this - imperative, mutable
const getActiveUserEmails = (users) => {
  const emails = [];
  for (let i = 0; i < users.length; i++) {
    if (users[i].active) {
      emails.push(users[i].email);
    }
  }
  return emails;
};
```

### The Backbone Pattern: Events as Decoupling

```javascript
// Loose coupling through events
class Model {
  constructor() {
    this._events = {};
    this._attributes = {};
  }

  set(key, value) {
    const prev = this._attributes[key];
    this._attributes[key] = value;
    if (prev !== value) {
      this.trigger('change', key, value, prev);
      this.trigger(`change:${key}`, value, prev);
    }
    return this;
  }

  on(event, callback) {
    (this._events[event] ||= []).push(callback);
    return this;
  }

  trigger(event, ...args) {
    (this._events[event] || []).forEach(cb => cb(...args));
    return this;
  }
}
```

### The CoffeeScript Pattern: Expression-Oriented

```javascript
// Everything returns a value
const classify = (score) =>
  score >= 90 ? 'A' :
  score >= 80 ? 'B' :
  score >= 70 ? 'C' :
  score >= 60 ? 'D' : 'F';

// Destructuring for clarity
const formatUser = ({ name, email, role = 'member' }) =>
  `${name} <${email}> (${role})`;

// Default parameters over conditionals
const paginate = (items, page = 1, perPage = 10) =>
  items.slice((page - 1) * perPage, page * perPage);
```

---

## API Design Principles

### Chainable Methods

```javascript
class Query {
  constructor(data) {
    this._data = data;
    this._filters = [];
    this._sort = null;
    this._limit = null;
  }

  where(predicate) {
    this._filters.push(predicate);
    return this; // Always return this for chaining
  }

  sortBy(key, direction = 'asc') {
    this._sort = { key, direction };
    return this;
  }

  limit(n) {
    this._limit = n;
    return this;
  }

  value() {
    let result = this._data;
    for (const filter of this._filters) {
      result = result.filter(filter);
    }
    if (this._sort) {
      const { key, direction } = this._sort;
      const mult = direction === 'asc' ? 1 : -1;
      result = [...result].sort((a, b) => a[key] > b[key] ? mult : -mult);
    }
    if (this._limit) {
      result = result.slice(0, this._limit);
    }
    return result;
  }
}

// Usage reads like English
const topUsers = new Query(users)
  .where(u => u.active)
  .where(u => u.score > 100)
  .sortBy('score', 'desc')
  .limit(10)
  .value();
```

### Sensible Defaults with Override

```javascript
// Good: defaults that work, options that customize
const fetch = (url, options = {}) => {
  const config = {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    timeout: 5000,
    retries: 3,
    ...options
  };
  // ...
};

// Most calls are simple
fetch('/api/users');

// Complex when needed
fetch('/api/users', { method: 'POST', body: data });
```

### Predictable Naming

```javascript
// Predicates start with is/has/can
const isEmpty = (arr) => arr.length === 0;
const hasChildren = (node) => node.children?.length > 0;
const canEdit = (user, doc) => doc.ownerId === user.id;

// Transformers are verbs or "to" + noun
const slugify = (str) => str.toLowerCase().replace(/\s+/g, '-');
const toArray = (value) => Array.isArray(value) ? value : [value];

// Getters match property names
const getName = (obj) => obj.name;
const getById = (id) => (arr) => arr.find(x => x.id === id);
```

---

## Utility Patterns

### Compose Small Functions

```javascript
// Pipe: left-to-right composition
const pipe = (...fns) => (x) => fns.reduce((v, f) => f(v), x);

// Usage
const processUser = pipe(
  validateEmail,
  normalizePhone,
  hashPassword,
  saveToDatabase
);

// Compose: right-to-left (mathematical order)
const compose = (...fns) => (x) => fns.reduceRight((v, f) => f(v), x);
```

### Memoization for Expensive Operations

```javascript
const memoize = (fn) => {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (!cache.has(key)) {
      cache.set(key, fn(...args));
    }
    return cache.get(key);
  };
};
```

### Debounce and Throttle

```javascript
const debounce = (fn, wait) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), wait);
  };
};

const throttle = (fn, wait) => {
  let lastCall = 0;
  return (...args) => {
    const now = Date.now();
    if (now - lastCall >= wait) {
      lastCall = now;
      fn(...args);
    }
  };
};
```

### Partial Application

```javascript
const partial = (fn, ...presetArgs) =>
  (...laterArgs) => fn(...presetArgs, ...laterArgs);

// Usage
const greet = (greeting, name) => `${greeting}, ${name}!`;
const sayHello = partial(greet, 'Hello');
sayHello('World'); // "Hello, World!"
```

---

## Code Review Checklist

When reviewing JavaScript utilities and libraries:

### Function Design
- [ ] Each function does exactly one thing
- [ ] Function name describes what it does, not how
- [ ] Pure functions preferred (same input → same output)
- [ ] Side effects isolated and explicit
- [ ] Parameters ordered from most to least likely to change

### API Surface
- [ ] Minimal public API (fewer methods = less to maintain)
- [ ] Chainable methods return `this`
- [ ] Terminal methods return computed values
- [ ] Consistent naming conventions throughout
- [ ] Sensible defaults for all optional parameters

### Collection Operations
- [ ] `map`/`filter`/`reduce` over imperative loops
- [ ] No mutation of input arrays/objects
- [ ] Early returns with `find`/`some`/`every` when appropriate
- [ ] Destructuring for cleaner access

### Code Style
- [ ] Expressions over statements when natural
- [ ] Arrow functions for simple transforms
- [ ] Regular functions when `this` or `arguments` needed
- [ ] Template literals over string concatenation
- [ ] Optional chaining (`?.`) and nullish coalescing (`??`)

---

## Anti-Patterns to Avoid

### Over-Engineering

```javascript
// Bad: AbstractFactoryProviderManager
class UserServiceFactoryProvider {
  createUserServiceFactory() {
    return new UserServiceFactory();
  }
}

// Good: just a function
const createUser = (data) => ({ id: uuid(), ...data, createdAt: Date.now() });
```

### Premature Abstraction

```javascript
// Bad: abstracting on first use
const makeAdder = (x) => (y) => x + y;
const add5 = makeAdder(5);
add5(3); // Just use 5 + 3

// Good: abstract when you see the pattern repeated
// (wait until you need it in 3+ places)
```

### Configuration Objects for Simple Cases

```javascript
// Bad: over-configured
fetch({ url: '/users', method: 'GET', format: 'json' });

// Good: simple API, options when needed
fetch('/users');
fetch('/users', { method: 'POST' });
```

---

## When This Skill Applies

**Use for:**
- Writing utility functions
- Designing library APIs
- Collection manipulation
- Refactoring imperative code to functional
- Building small, focused modules

**Skip for:**
- React/Vue/Angular component patterns (use framework conventions)
- Node.js server code (use Node idioms)
- Build tooling (use tool conventions)
- Performance-critical hot paths (measure first)

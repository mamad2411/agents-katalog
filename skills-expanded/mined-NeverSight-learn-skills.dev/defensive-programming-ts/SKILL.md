---
name: defensive-programming-ts
description: >
  Tiger Style defensive programming principles for TypeScript/JavaScript.
  Covers assertions, readability, error handling, and exhaustiveness checks.
  Use when writing or reviewing TS/JS code, adding assertions, handling errors,
  or when the user mentions "defensive programming", "tiger style",
  "assertions", "exhaustive", "handle all errors", or needs a code review.
---

# Defensive Programming — TypeScript / JavaScript

Inspired by [Tiger Style](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/TIGER_STYLE.md).

## Assertions

Assert preconditions, postconditions, and invariants at every boundary.
Minimum 2 assertions per function.

### Invariant helper

```typescript
function invariant(condition: boolean, msg: string): asserts condition {
  if (!condition) throw new Error(`Invariant: ${msg}`);
}
```

### Pair assertions
For every property, assert before writing and again after reading from a boundary.

```typescript
function persist(data: Uint8Array): void {
  assert(data.length > 0, "cannot persist empty data");
  writeToDisk(data);
}

function load(): Uint8Array {
  const data = readFromDisk();
  assert(data.length > 0, "corrupt data on disk");
  return data;
}
```

### Split compound assertions

```typescript
// Good
assert(user !== null);
assert(user.id > 0);

// Avoid
assert(user !== null && user.id > 0);
```

### Function boundary assertions

```typescript
function calculateTotal(items: Item[]): number {
  assert(items.length > 0, "expected at least one item");

  const total = items.reduce((sum, item) => {
    assert(item.price > 0, "item price must be positive");
    return sum + item.price;
  }, 0);

  assert(total > 0, "total must be positive");
  return total;
}
```

## Readability

### 70-line function limit
Every function must fit on one screen. If it doesn't, split it.
Push control flow up, push computation down.

### camelCase (language convention)
TS/JS uses camelCase, not snake_case. Follow the language.

```typescript
// Good
function parseUserInput(raw: string): Result { ... }

// Avoid
function parse_user_input(raw: string): Result { ... }
```

### Variable names with units

```typescript
// Good
const timeoutMs = 5000;
const maxRetries = 3;
const latencyMsMax = 1000;

// Avoid
const timeout = 5000;
const max = 3;
const latencyMax = 1000;
```

### State invariants positively

```typescript
// Good
if (index < length) {
  // element exists
} else {
  // out of bounds
}

// Avoid
if (index >= length) {
  // out of bounds
} else {
  // element exists
}
```

### Split compound conditions

```typescript
// Good
if (user.isActive) {
  if (user.hasPermission("write")) {
    // proceed
  }
}

// Avoid
if (user.isActive && user.hasPermission("write")) {
  // proceed
}
```

### Smallest scope for variables

```typescript
// Good
function process(order: Order): void {
  {
    const items = order.fetchItems();
    assert(items.length > 0);
  }
  // items not in scope here
  order.submit();
}
```

## Error Handling

All errors must be handled. 92% of catastrophic production failures
come from unhandled non-fatal errors.

### Use Result types over exceptions

```typescript
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

function parseJson(raw: string): Result<unknown, SyntaxError> {
  try {
    return { ok: true, value: JSON.parse(raw) };
  } catch (e) {
    if (e instanceof SyntaxError) return { ok: false, error: e };
    throw e; // programmer error — crash
  }
}
```

### Crash on programmer errors, handle operational errors

```typescript
function readConfig(path: string): Config {
  const raw = fs.readFileSync(path, "utf-8");
  // If this fails it's a programmer bug — crash
  const parsed = JSON.parse(raw) as Config;
  assert(parsed.host !== undefined, "config missing host");
  return parsed;
}
```

### Exhaustive error discrimination

```typescript
type NetworkError =
  | { kind: "timeout"; ms: number }
  | { kind: "dns"; hostname: string }
  | { kind: "refused"; port: number };

function handleError(err: NetworkError): string {
  switch (err.kind) {
    case "timeout": return `timed out after ${err.ms}ms`;
    case "dns": return `DNS lookup failed for ${err.hostname}`;
    case "refused": return `connection refused on port ${err.port}`;
  }
}
```

## Exhaustiveness Checks

### Discriminated unions + never

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rect"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "rect": return shape.width * shape.height;
    case "triangle": return (shape.base * shape.height) / 2;
    // No default — adding a new Shape variant causes a compile error here
  }
}
```

### Always add a default with assertNever

```typescript
function assertNever(x: never): never {
  throw new Error(`unreachable: ${x}`);
}

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "rect": return shape.width * shape.height;
    case "triangle": return (shape.base * shape.height) / 2;
    default: return assertNever(shape);
  }
}
```

---

> From [Tiger Style](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/TIGER_STYLE.md):
> "The rules act like the seat-belt in your car: initially they are perhaps a little uncomfortable, but after a while their use becomes second-nature and not using them becomes unimaginable."

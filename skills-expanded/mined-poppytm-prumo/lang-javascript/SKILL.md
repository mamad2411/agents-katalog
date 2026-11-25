# Modern JavaScript (ES2024+) Systems, Event Loop & Memory Hygiene

## 1. Purpose
Author, refactor, and audit production systems written in modern **JavaScript (ES2022–ES2024+)**. This skill mandates native ECMAScript Modules (ESM), strict event loop microtask/macrotask queue hygiene, cooperative cancellation via `AbortController`, eradication of prototype pollution vulnerabilities and global leaks, defense against microtask starvation, and proactive memory management via `WeakMap` and `structuredClone()`.

---

## 2. Use When
- Developing modern Node.js, Bun, Deno, or browser runtime engines using vanilla JavaScript or ESM libraries.
- Managing high-throughput asynchronous event streams, WebSocket feeds, or HTTP request multiplexing.
- Auditing JavaScript codebases for memory leaks (detached DOM nodes, uncleaned event listeners, uncleared timers).
- Hardening JavaScript execution environments against prototype pollution and code injection (`eval`, `new Function`).
- Operating in mode(s): `implementation`, `review`, `testing`, `audit`.

---

## 3. Do Not Use When
- Developing in TypeScript with static compilation and static type checking (use `lang-typescript`).
- Writing low-level systems modules where native memory management (C/C++/Rust) is required.
- Maintaining legacy pre-ES6 codebases constrained to ECMAScript 5 environments (e.g., Internet Explorer).

---

## 4. Required Context
Before implementing or modifying JavaScript code, verify:
- **Target Runtime**: Node.js 20+, Bun 1.1+, Deno 1.40+, or modern evergreen browsers.
- **Module Architecture**: Native ECMAScript Modules (`"type": "module"` in `package.json`, `import`/`export` syntax). CommonJS `require()` is forbidden in new development.
- **Asynchronous Protocol**: Universal use of `async`/`await` with `AbortSignal` cancellation support.
- **Linter & Security Rules**: ESLint with `eslint:recommended`, `sonarjs`, and prototype pollution security plugins.

---

## 5. Procedure

```
[Module Design & Scope]
         |
         v
[1. ESM Native Structure] ---------> Native import/export, top-level await
         |
         v
[2. Prototype Pollution Defense] --> Object.create(null) or Map for lookup tables
         |
         v
[3. Async Event Loop Lifecycle] ---> AbortController propagation, microtask hygiene
         |
         v
[4. Memory Leak Audit] ------------> WeakMap/WeakRef, signal-based event listener cleanup
         |
         v
[5. Static & Runtime Gauntlet] ----> ESLint, Node test runner / Vitest
```

### Step 1: Native ESM & Immutability Patterns
1. Eradicate `var` completely. Use `const` by default; use `let` strictly when variable reassignment is required.
2. Use modern non-mutating array methods (ES2023):
   - `.toSorted()` instead of `.sort()`
   - `.toReversed()` instead of `.reverse()`
   - `.toSpliced()` instead of `.splice()`
   - `.with(index, value)` instead of direct index assignment
3. Deep-clone complex state structures using the native platform `structuredClone()` API instead of JSON serialization hacks.

### Step 2: Prototype Pollution Defense
1. Never use plain object literals `{}` as arbitrary key-value dictionaries for untrusted user inputs.
2. Use `new Map()` or `Object.create(null)` (dictionary with null prototype, immune to `__proto__` injection):
   ```javascript
   // SECURE: Null-prototype dictionary
   const safeDictionary = Object.create(null);
   safeDictionary[userSuppliedKey] = value;
   ```
3. In sensitive runtime boundaries, freeze object prototypes at initialization:
   ```javascript
   Object.freeze(Object.prototype);
   Object.freeze(Array.prototype);
   ```

### Step 3: Event Loop Microtask Hygiene & Starvation Defense
- Understand the priority hierarchy:
  1. Synchronous JavaScript call stack
  2. Microtask Queue (`Promise.then()`, `queueMicrotask()`)
  3. Macrotask Queue (`setTimeout()`, `setImmediate()`, I/O callbacks, rendering steps)
- Never create infinite or recursive microtask loops. Unbounded microtask recursion starves the event loop, freezing I/O and user interaction entirely.
- Yield to the macrotask queue in long CPU-bound loops:
  ```javascript
  export function yieldToEventLoop() {
    return new Promise((resolve) => setTimeout(resolve, 0));
  }
  ```

### Step 4: Cooperative Cancellation with `AbortController`
Pass `AbortSignal` across all long-running or asynchronous operations:
```javascript
export async function fetchWithTimeout(url, options = {}, timeoutMs = 5000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(new Error("Timeout")), timeoutMs);

  try {
    const signal = options.signal
      ? AbortSignal.any([options.signal, controller.signal])
      : controller.signal;
    return await fetch(url, { ...options, signal });
  } finally {
    clearTimeout(timeoutId);
  }
}
```

### Step 5: Memory Leak Eradication & Listener Lifecycle
1. Attach event listeners with automatic abort signal disposal:
   ```javascript
   element.addEventListener("click", handler, { signal: abortController.signal });
   ```
2. Store auxiliary object metadata using `WeakMap` or `WeakSet`, ensuring that when the primary object is de-referenced, its metadata is collected automatically by the garbage collector without memory leaks.

---

## 6. Decision Rules & Invariants
- **RULE 1 (Zero `eval` / `new Function`)**: Dynamic string evaluation is strictly banned under all circumstances.
- **RULE 2 (No Unhandled Promise Rejections)**: Every asynchronous call path must be awaited inside `try/catch` or return a handled Promise.
- **RULE 3 (No Prototype Mutation)**: Never assign to `Object.prototype`, `Array.prototype`, or any built-in prototype.
- **RULE 4 (AbortSignal Support)**: Any asynchronous function taking longer than 100ms or performing network/disk I/O must accept an optional `AbortSignal`.

---

## 7. Evidence Required
- **Linter Evidence**: ESLint passes with 0 errors and 0 warnings.
- **Leak Audit Evidence**: Verification that event listeners and timers are cleanly disposed of in tear-down tests.
- **Security Evidence**: Absence of `eval`, `new Function`, `__proto__` mutations, and un-sanitized HTML assignments.

---

## 8. Output Contract
- Modern ESM JavaScript source files (`.js`, `.mjs`) with JSDoc type annotations.
- Package manifest (`package.json`) specifying `"type": "module"`.
- JavaScript Verification Report (`templates/javascript-verification-report.md`).

---

## 9. Stop Conditions
- All test suites execute cleanly under Node/Bun test runners.
- Zero ESLint warnings reported.
- Token budget exhausted.
- Blocked on external dependency.

---

## 10. Escalation Rules
- Escalate to security lead if legacy dependencies require insecure global prototype extensions.
- Escalate if integration with non-ESM CommonJS packages requires complex interop polyfills.

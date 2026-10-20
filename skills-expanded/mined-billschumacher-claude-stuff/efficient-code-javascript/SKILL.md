---
name: efficient-code-javascript
description: Applies when writing or reviewing JavaScript (Node.js or browser) code. Extends the core efficient-code principles with JS-specific primitives (Map/Set over arrays, TypedArrays), V8 hidden classes, monomorphic call sites, holey arrays, array method costs, closure capture, and for-loop vs forEach gotchas.
---

# Efficient Code — JavaScript

This skill assumes you also have the core `efficient-code` skill active.

## Stdlib primitives

- **`Array`** — dynamic; `push`/`pop` amortized O(1); **`shift`/`unshift` are O(n)** (every element shifts).
- **`Map`** — real hash map with arbitrary keys, O(1) average. Prefer over plain objects for dynamic/frequently-mutated keys — preserves insertion order and avoids hidden-class churn.
- **`Set`** — O(1) membership. Use over `Array.includes` (O(n)) inside loops.
- **`Array.prototype.join('')`** — O(n) string build; prefer over `+=` accumulator in loops.
- **`TypedArray`** (`Uint8Array`, `Float64Array`, etc.) — fixed-layout, monomorphic, SIMD-friendly; use for numeric data.
- **`structuredClone(x)`** — built-in deep clone.
- **`Array.from({length: n}, fn)`** — materialize an array of known size in one pass.

## V8 / runtime gotchas

1. **Hidden classes / inline caches:** objects with the same properties added in the same order share a shape. Adding properties later, deleting them, or using different insertion orders causes "shape pollution" and deoptimizes every call site that touches them. **Initialize all fields in the constructor, in the same order, every time.**
2. **`delete obj.foo`** transitions the object to dictionary (slow) mode. Set to `undefined` in hot code instead.
3. **Array "holes"** (sparse arrays via `arr[1000] = 1` or `delete arr[i]`) transition elements-kind to `HOLEY_*` and slow every access. Keep arrays dense and packed.
4. **Mixed-type arrays** (int + double + object) transition to the generic `PACKED_ELEMENTS` kind. Stay monomorphic.
5. **Megamorphic call sites:** a function called with objects of >4 shapes gives up inlining. Keep call sites monomorphic.
6. **Closures capture variables by reference for their full lifetime.** Long-lived closures can retain huge scopes. Don't accidentally keep the whole request object alive via a callback.
7. **`try`/`catch` around hot loops** historically prevented optimization in V8 (fixed in TurboFan, but still a small cost). Keep try/catch outside the hot loop body.
8. **`arguments` object is slow** — use rest parameters `(...args)`.
9. **`with` and direct `eval`** disable scope analysis. Never in hot code.
10. **String concatenation `a + b`** builds rope-like ConsStrings in V8, so `+=` in a loop isn't automatically O(n²) — but forcing materialization (regex, JSON, network send) flattens them. Use `Array.push` + `join` when you need the final string for processing.
11. **`==` invokes coercion; `===` is faster and clearer.**
12. **`JSON.parse` / `JSON.stringify`** are implemented in C++ and usually faster than hand-rolled parsers.
13. **Object property access:** numeric-string keys (`"0"`, `"1"`) are treated as array indices. Non-integer string keys take the slow path.
14. **`for (let i = 0; i < arr.length; i++)` is usually the fastest loop form** — monomorphic, no iterator protocol. `for...of` on arrays is close. `forEach` has per-call function-call overhead.
15. **Hoist `arr.length`** out of `for` conditions when the array doesn't change.
16. **Don't mutate an array while iterating it** — breaks monomorphic assumptions and your logic.

## Profiling

Chrome DevTools Performance panel with flame chart; `node --prof` + `--prof-process` for CLI; `clinic.js flame` for Node.

## Sources

- https://v8.dev/blog/fast-properties
- https://v8.dev/blog/elements-kinds
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference
- https://web.dev/articles/speed-at-scale-web-dev
- https://github.com/tc39/ecma262

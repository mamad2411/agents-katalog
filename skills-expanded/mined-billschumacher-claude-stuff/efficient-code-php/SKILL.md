---
name: efficient-code-php
description: Applies when writing or reviewing PHP code (PHP 7.4+ / 8+). Extends the core efficient-code principles with PHP-specific rules around array copy-on-write, foreach-by-reference pitfalls, OPCache and preloading, interned strings, typed/readonly properties, generators, and the scope of the PHP 8 JIT.
---

# Efficient Code — PHP

This skill assumes you also have the core `efficient-code` skill active.

## Stdlib primitives

- **`array`** — ordered hash map serving as both list and dict; insertion-ordered, O(1) average insert and lookup. This one container covers most needs.
- **`SplFixedArray`** — fixed-size dense array with integer keys; lower memory than `array` when you don't need string keys.
- **`SplObjectStorage`** — object-keyed map without coercing keys to strings.
- **`SplPriorityQueue`, `SplStack`, `SplQueue`** — O(log n) / O(1) operations backed by heap/list.
- **`Generator`** (via `yield`) — streaming iteration without materializing a full array; use for large sequences.
- **`array_count_values`** — single native C call to tally array values; always faster than a manual `foreach` counter loop.
- **`array_unique`, `array_column`, `array_combine`, `array_flip`** — native C-level operations; prefer over equivalent PHP loops.
- **`array_map`, `array_filter`, `array_reduce`** — functional helpers. They call the callback per element and a plain `foreach` often beats them on hot paths.
- **`implode('', $parts)`** — O(n) string join; use over `.=` in a loop when the number of parts is large.
- **`str_contains` / `str_starts_with` / `str_ends_with`** (PHP 8+) — prefer over `strpos(...) !== false` for readability and a slight speedup.

## PHP-specific gotchas

1. **Arrays are copy-on-write.** `$b = $a` is O(1) until one is mutated — then a full copy happens. Passing arrays to functions is similarly cheap until mutation.
2. **`foreach ($arr as $v)` copies each value.** `foreach ($arr as &$v)` takes a reference but you MUST `unset($v)` after the loop — a dangling reference variable causes subtle bugs in later loops that write into `$v`.
3. **`array_merge($a, $b)`** copies both arrays and re-indexes integer keys. `$a + $b` (the union operator) preserves first-key-wins semantics without re-indexing. Spread `[...$a, ...$b]` is often fastest on PHP 7.4+.
4. **`count($arr)` inside a `for` condition** is O(1) (PHP caches the count) but still hoist it for clarity.
5. **References (`&`) interact badly with copy-on-write.** A referenced variable can't share its zval and forces eager copies elsewhere. Avoid unless necessary.
6. **OPCache is on by default in production** and caches compiled opcodes. **`opcache.preload`** pulls classes into shared memory at startup, eliminating per-request autoload — set it up for PHP 7.4+ production.
7. **Interned strings** — string literals are deduplicated across requests; `===` on interned strings is a pointer compare.
8. **PHP 8 JIT (`opcache.jit`) helps CPU-bound numeric code most.** Typical web requests are I/O-bound and the JIT is a small effect; don't rely on it for hot paths over algorithmic fixes.
9. **Typed properties (PHP 7.4+)** enable the engine to skip type checks on read in some paths and pack memory more tightly than untyped properties.
10. **`readonly` properties (PHP 8.1+) are runtime-enforced** — writing to them throws.
11. **`new` on a class with a constructor is slower than a plain array.** For throwaway data records, measure.
12. **Interpolation `"Hello $name"` is usually slightly faster than `"Hello " . $name`** in modern PHP (fewer opcodes).
13. **Closures capture `$this` by default inside methods.** `static function() { ... }` avoids it when you don't need the instance.
14. **`Exception` creation captures a backtrace.** Throwing in a hot loop is expensive; don't use exceptions for normal control flow.
15. **`isset($arr[$k])` is faster than `array_key_exists($arr, $k)`** but returns `false` for `null` values — the semantics differ.
16. **Multibyte string functions (`mb_*`) are much slower** than plain `str*`. Only use when you actually need Unicode semantics.

## Profiling

Xdebug profiler + KCachegrind/QCachegrind (development); SPX, Blackfire, or Tideways for production-grade profiling.

## Sources

- https://www.php.net/manual/en/language.types.array.php
- https://www.php.net/manual/en/book.opcache.php
- https://www.npopov.com/2021/10/13/How-opcache-works.html
- https://wiki.php.net/rfc/jit
- https://www.php.net/manual/en/features.gc.performance-considerations.php

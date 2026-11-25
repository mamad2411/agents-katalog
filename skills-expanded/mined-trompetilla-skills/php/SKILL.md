---
name: PHP
description: Write solid PHP avoiding type juggling traps, array quirks, and common security pitfalls.
metadata: {"clawdbot":{"emoji":"🐘","requires":{"bins":["php"]},"os":["linux","darwin","win32"]}}
---

## Type Juggling Traps
- `==` coerces types: `"0" == false` is true — always use `===` for strict comparison
- `"10" == "10.0"` is true — string comparison converts to numbers if both look numeric
- `0 == "any string"` was true before PHP 8 — still beware legacy code
- `in_array($val, $arr)` uses loose comparison — pass `true` as third param for strict
- `switch` uses loose comparison — use match expression in PHP 8+ for strict

## Array Gotchas
- `array_merge()` reindexes numeric keys — use `+` operator to preserve keys
- `$arr[] = $val` appends, `$arr[0] = $val` replaces — different behaviors
- Unset array element doesn't reindex — use `array_values()` after unset if needed
- `empty([])` is true, `empty("0")` is true — use `count()` or `=== []` for clarity
- `foreach` on reference: `foreach ($arr as &$val)` — unset `$val` after loop or last ref persists

## Null Handling
- `isset()` returns false for null — use `array_key_exists()` to check if key exists
- `??` null coalescing doesn't trigger on false or empty string — only null/undefined
- `?->` nullsafe operator (PHP 8) — chain methods on potentially null objects
- `$obj?->method()` returns null if obj is null — no error thrown
- `is_null($x)` vs `$x === null` — identical, but `===` is faster

## String Pitfalls
- Double quotes interpolate: `"$var"` — single quotes literal: `'$var'`
- Heredoc interpolates like double quotes — nowdoc (with single quote) doesn't
- `strpos()` returns 0 for match at start — use `=== false` not `!strpos()`
- String offset access `$str[0]` works — but `$str[-1]` only works PHP 7.1+
- Multibyte: `strlen()` counts bytes — use `mb_strlen()` for UTF-8 char count

## Variable Scope
- Functions don't see outer variables — pass explicitly or use `global` keyword
- Closures need `use ($var)` to capture outer variables — by value unless `use (&$var)`
- `static` in function persists value across calls — useful for caching
- `$this` not available in static methods — use `self::` or `static::`
- Superglobals (`$_GET`, `$_POST`) available everywhere — but don't trust them

## OOP Quirks
- Objects pass by reference-like handle — clone explicitly with `clone $obj`
- `__clone()` called after shallow clone — implement for deep clone of nested objects
- `private` not accessible in child — use `protected` for inheritance
- `static::` late binding vs `self::` early binding — `static` respects overrides
- Constructor not called on unserialization — implement `__wakeup()` for init

## Error Handling
- `@` suppresses errors — avoid, makes debugging impossible
- `try/catch` only catches exceptions — errors need `set_error_handler`
- PHP 7+ throws `Error` for fatal — catch `Throwable` for both Error and Exception
- `finally` always runs — even if exception thrown or return in try
- `set_exception_handler()` for uncaught — last resort logging

## Security Essentials
- Never concatenate SQL — use prepared statements with PDO or mysqli
- `htmlspecialchars()` output in HTML — prevents XSS, use `ENT_QUOTES`
- Validate `$_GET`/`$_POST` before use — `filter_input()` or explicit validation
- Session fixation: regenerate ID after login — `session_regenerate_id(true)`
- CSRF: verify token on state-changing requests — store in session, check on submit

## Date/Time
- Always set timezone: `date_default_timezone_set()` — or php.ini `date.timezone`
- `DateTime` is mutable — use `DateTimeImmutable` to avoid side effects
- `strtotime()` relative to now or second param — "next monday" depends on current day
- Comparing DateTime objects works with `<` `>` `==` — but `===` checks identity
- Store UTC in database — convert to local timezone on display

## Performance Traps
- `count()` in loop condition recalculates — cache: `$len = count($arr)`
- `array_push($arr, $val)` slower than `$arr[] = $val` — use `[]` for single
- Long-running scripts: unset large variables — `gc_collect_cycles()` if needed
- Include files: `require_once` has lookup overhead — use autoloading
- String concatenation in loop — use array and `implode()` for many pieces

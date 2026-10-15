---
name: result-coding-style
description: >
  Coding style guidelines for the `results` library.
  Use this when writing, reviewing, or modifying any Python code
  that uses Result, Maybe, Ok, Err, Some, or Nothing types.
---

# Result Coding Style Guidelines

This project is a **Rust-inspired `Result[T, E]` and `Maybe[T]` implementation in Python**.
The core value is **functional, composable error handling**.

---

## ❗ Rule 1: Prefer Functional Chaining over Imperative Checks

Always prefer `map()`, `map_err()`, `and_then()` chaining over sequential `is_ok()` / `is_err()` checks.

```python
# ✅ CORRECT — Functional style (idiomatic for this library)
result = (
    parse_input(raw)
    .and_then(validate)
    .map(transform)
    .map_err(lambda e: f"Processing failed: {e}")
)

# ❌ AVOID — Imperative style
result = parse_input(raw)
if result.is_err():
    return Err(f"Processing failed: {result.err()}")
value = result.ok()
result2 = validate(value)
```

**Why:** `and_then` / `map` short-circuit automatically on `Err` / `Nothing`.
Imperative `is_err()` checks break the pipeline, introduce unnecessary intermediate variables,
and defeat the purpose of this library.

---

## ❗ Rule 2: Prefer `match/case` over `if is_ok()` for Dispatch

When branching on a Result or Maybe at a function boundary or API layer:

```python
# ✅ CORRECT — Structural pattern matching
match result:
    case Ok(value):
        print(f"Success: {value}")
    case Err(error):
        print(f"Error: {error}")

# ✅ CORRECT — Maybe
match maybe:
    case Some(value):
        print(f"Found: {value}")
    case Nothing():
        print("Not found")

# ❌ AVOID — Imperative if/else
if result.is_ok():
    value = result.ok()
    ...
else:
    error = result.err()
    ...
```

---

## ✅ When `is_ok()` / `is_err()` IS Acceptable

Only use imperative checks when:

- You need to **log or monitor** before re-raising
- You need **early termination** with side effects (e.g., `raise`, `sys.exit`)
- Branching logic is too complex for a single lambda

```python
# ✅ ACCEPTABLE — early termination with side effect
if result.is_err():
    logger.critical(f"Fatal: {result.err()}")
    raise SystemExit(1)
```

---

## ❗ Rule 3: Chain `context()` for Error Tracing

Add context messages to `Err` / `Nothing` to build a LIFO diagnostic chain (like Rust's `anyhow`):

```python
# ✅ CORRECT
return (
    do_operation()
    .context("performing operation X")
    .context("processing user request")
)

# ✅ Lazy context (for expensive evaluation)
return result.with_context(lambda: f"at {datetime.now()}")
```

---

## ❗ Rule 4: Combine Functional and `match/case` Appropriately

Use `map` / `and_then` for intermediate transforms, `match/case` for final dispatch:

```python
# ✅ CORRECT — chain transforms, then dispatch
result = (
    validate_input(data)
    .and_then(transform)
    .map(enrich)
)

match result:
    case Ok(value):
        return Ok({"processed": value})
    case Err(UserError(code, msg)):
        return Err(f"[{code}] {msg}")
    case Err(ValueError(msg)):
        return Err(f"Validation: {msg}")
```

---

## Type System Rules

- All functions returning `Result` or `Maybe` **must be fully type-annotated**
- Code must pass `mypy --strict` with **zero errors**
- Code must pass `ruff` with **all checks passing**
- Use `@typing_extensions.override` on all ABC method implementations
- Prefer specific error types (`ValueError`, `RuntimeError`, custom `@dataclass`) over bare `str`

---

## Do NOT

- ❌ Use sequential `is_ok()` / `is_err()` checks instead of `and_then` / `map`
- ❌ Use `result.ok()` to extract a value without prior chaining or checking
- ❌ Use `isinstance(result, Ok)` — use `match/case` or `.is_ok()`
- ❌ Call `.unwrap()` in library code — only in tests or top-level entrypoints
- ❌ Replace functional chains with sequential imperative blocks

---

## Quick Reference

| Situation | Preferred API |
|-----------|---------------|
| Transform success value | `.map(fn)` |
| Transform error value | `.map_err(fn)` |
| Chain operation returning Result | `.and_then(fn)` |
| Add error context | `.context("msg")` |
| Lazy error context | `.with_context(lambda: ...)` |
| Debug without breaking chain | `.inspect(fn)` / `.inspect_err(fn)` |
| Dispatch at boundary | `match result: case Ok(v): ... case Err(e): ...` |
| Fallback value | `.unwrap_or(default)` |
| Lazy fallback | `.unwrap_or_else(lambda: ...)` |
| Early exit only | `if result.is_err(): raise ...` |

---
name: stand-odin
description: >-
  Odin coding standards. Use when writing Odin code. Covers idiomatic error
  handling with or_else and or_return, memory/allocator patterns, attributes,
  naming and API conventions, and testing with core:testing.
---

# Odin Standards

Standards for Odin code. Odin is underrepresented in training data — do not
transplant Go/Rust/C error-handling patterns verbatim; reach for Odin
constructs first.

## Idioms

Prefer `or_else` when every failure path returns the same default:

```odin
// Don't — all branches return the same fallback
parse_env_int :: proc(key: string, default: int = 0) -> int {
    v, ok := os.lookup_env(key, context.temp_allocator)
    if !ok || v == "" { return default }
    x, ok2 := strconv.parse_int(strings.trim_space(v), 10)
    if !ok2 { return default }
    return x
}

// Do
parse_env_int :: proc(key: string, default: int = 0) -> int {
    v := os.lookup_env(key, context.temp_allocator) or_else ""
    return strconv.parse_int(strings.trim_space(v), 10) or_else default
}
```

Domain validation after parse is one line, not a rewrite:

```odin
parse_env_f64_nonneg :: proc(key: string, default: f64 = 0) -> f64 {
    v := os.lookup_env(key, context.temp_allocator) or_else ""
    x := strconv.parse_f64(strings.trim_space(v)) or_else default
    return max(0, x)
}
```

Use `or_return` to propagate errors instead of check-and-return blocks:

```odin
// Don't
data, err := os.read_entire_file_or_err(path)
if err != nil { return nil, err }

// Do
data := os.read_entire_file_or_err(path) or_return
```

Use explicit `(value, ok)` checks only when failure modes differ (log,
branch, or propagate differently per case).

Mark file-local helpers and must-use results with attributes:

```odin
@(private = "file")
trimmed :: proc(s: string) -> string { return strings.trim_space(s) }

@(require_results)
checksum :: proc(data: []byte) -> u32 { ... }
```

## Anti-Patterns

- Do not expand `(value, ok)` into multi-branch control flow when every
  branch returns the same value — use `or_else`
- Do not hardcode a `0` fallback when a `default` parameter is appropriate
- Do not pre-check `v == ""` before trimming when a failed parse of the
  empty string already yields the fallback — only distinguish missing vs
  empty vs invalid when the caller needs the distinction
- Do not write Go-style `if err != nil { return err }` ladders — use
  `or_return`

## Memory & Allocators

- `context.temp_allocator` for short-lived scratch data (env lookups,
  parse buffers, per-frame strings); free in bulk with
  `free_all(context.temp_allocator)` at a natural boundary (frame/request)
- `context.allocator` for general heap allocation; pair `make`/`new` with
  `delete`/`free`, typically via `defer`
- In library code, take an explicit `allocator := context.allocator`
  parameter instead of allocating from implicit globals:

```odin
// Don't — caller cannot control allocation
clone_name :: proc(s: string) -> string { return strings.clone(s) }

// Do — caller controls allocation; allocator errors propagate
clone_name :: proc(s: string, allocator := context.allocator) -> (string, mem.Allocator_Error) {
    return strings.clone(s, allocator)
}
```

- Copy strings that must outlive their source; temp-allocate strings that
  do not escape the current scope

## Error Handling

- `or_else` — same default for every failure
- `or_return` — early exit from a procedure whose final return value is an
  error or `ok` boolean
- Explicit `(value, ok)` — failure modes need different handling
- Model recoverable failures as error enums or unions returned as the last
  value; reserve `panic` for unrecoverable programmer error, never library
  control flow
- `assert` / `#assert` only for invariants, not input validation
- Prefer default-parameter fallbacks for config/env parsing helpers

## Types & API Design

- `snake_case` for procedures and variables; `Ada_Case` for types
  (`Entity_Kind`, `Parse_Error`); `SCREAMING_SNAKE_CASE` for constants
- Use default parameter values for fallbacks instead of sentinel checks
- Encode domain constraints in the name (`parse_env_f64_nonneg`) or via
  post-parse validation (`max(0, x)`)
- Prefer plain `proc`s and struct composition — Odin has no classes or
  inheritance; do not simulate them

## Testing

- Use `core:testing` with the `@(test)` attribute; run via `odin test`
- Table-driven cases over one-proc-per-case:

```odin
import "core:testing"

@(test)
parse_env_int_defaults :: proc(t: ^testing.T) {
    cases := [][2]int{{-3, -3}, {0, 0}, {42, 42}}
    for c in cases {
        testing.expect_value(t, parse_env_int("MISSING_KEY", c[0]), c[1])
    }
}
```

- For parsing helpers, cover: missing, empty, whitespace-only, invalid,
  valid, and domain edges (e.g. negative clamp)
- Defer global coverage/commit rules to `stand-general`

## Toolchain

- `odin check` is the primary validation gate; `odin build -vet -strict-style`
  catches unused values and style drift
- Follow the `lint` skill where a project has lintro configured; no lintro
  Odin plugin exists yet, so the compiler vet flags are the linter

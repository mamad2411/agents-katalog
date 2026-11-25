---
name: edict-program-writer
description: >
  How to write correct Edict JSON AST programs. Covers the AST format, node types, ID conventions,
  common patterns, and how to interpret and fix structured errors. Use this skill when writing Edict
  programs, creating example programs, producing JSON ASTs for the Edict compiler, demonstrating
  language features, or debugging AST validation/type/effect errors. Also use when an agent needs
  to produce Edict code via MCP tools like edict_validate, edict_check, edict_compile, or edict_run.
---

# Writing Edict Programs

Edict programs are JSON objects — not text files. You produce an AST directly as structured JSON. There is no syntax to learn, only a schema to conform to.

## The Loop

1. Call `edict_schema` to get the JSON Schema (or read `schema/edict-schema.json`)
2. Write a program as a JSON AST conforming to the schema
3. Call `edict_check` (or `edict_compile`) — if errors come back, fix and resubmit
4. Call `edict_run` to execute the compiled WASM

## Program Structure

Every program is a **module**:

```json
{
  "kind": "module",
  "id": "mod-myprogram-001",
  "name": "myprogram",
  "imports": [],
  "definitions": [ ... ]
}
```

The optional `schemaVersion` field tracks which schema version the AST targets. **You don't need to include it** — programs without `schemaVersion` are treated as v1.0 and auto-migrated to the current version by the compiler. If you include it, set it to the current version (check via `edict_version`).

A module contains **definitions**: functions (`fn`), records (`record`), enums (`enum`), type aliases (`type`), and constants (`const`).

Every module needs a `main` function that returns `Int` (exit code).

## ID Conventions

Every AST node needs a unique `id` string. Convention: `{kind}-{descriptive-name}-{counter}`

| Kind | Prefix | Example |
|------|--------|---------|
| Module | `mod-` | `mod-hello-001` |
| Function | `fn-` | `fn-main-001` |
| Parameter | `param-` | `param-n-001` |
| Literal | `lit-` | `lit-zero-001` |
| Call | `call-` | `call-print-001` |
| Identifier | `ident-` | `ident-x-001` |
| Binary op | `binop-` | `binop-add-001` |
| If | `if-` | `if-check-001` |
| Let | `let-` | `let-result-001` |
| Match | `match-` | `match-shape-001` |
| Record def | `rec-` | `rec-point-001` |
| Enum def | `enum-` | `enum-shape-001` |

IDs must be **globally unique** within a module. Duplicate IDs cause a `duplicate_id` error.

## Type System

| Type | JSON representation |
|------|-------------------|
| Basic | `{ "kind": "basic", "name": "Int" }` — also `Float`, `String`, `Bool` |
| Array | `{ "kind": "array", "element": <TypeExpr> }` |
| Option | `{ "kind": "option", "inner": <TypeExpr> }` |
| Result | `{ "kind": "result", "ok": <TypeExpr>, "err": <TypeExpr> }` |
| Named | `{ "kind": "named", "name": "Point" }` — references a record/enum |
| Tuple | `{ "kind": "tuple", "elements": [<TypeExpr>, ...] }` |
| Function | `{ "kind": "fn_type", "params": [...], "effects": [...], "returnType": <TypeExpr> }` |
| Unit | `{ "kind": "unit_type", "base": "Float", "unit": "usd" }` |
| Refined | `{ "kind": "refined", "id": "...", "base": <TypeExpr>, "variable": "x", "predicate": <Expr> }` |

## Effects

Functions declare effects: `"pure"`, `"reads"`, `"writes"`, `"io"`, `"fails"`.

- A `pure` function **cannot** call an `io` or `fails` function
- Effects propagate through call graphs — if you call a function with `io`, you must declare `io`
- Functions that call `print` need `"io"` effect

## Contracts

Functions can have `pre` and `post` conditions — verified at compile time by Z3:

```json
{
  "kind": "pre",
  "id": "pre-001",
  "condition": {
    "kind": "binop", "id": "cond-001", "op": ">",
    "left": { "kind": "ident", "id": "id-n-001", "name": "n" },
    "right": { "kind": "literal", "id": "lit-0-001", "value": 0 }
  }
}
```

## Common Patterns

### Hello World
```json
{
  "kind": "module", "id": "mod-hello-001", "name": "hello", "imports": [],
  "definitions": [{
    "kind": "fn", "id": "fn-main-001", "name": "main",
    "params": [], "effects": ["io"],
    "returnType": { "kind": "basic", "name": "Int" },
    "contracts": [],
    "body": [
      { "kind": "call", "id": "call-print-001",
        "fn": { "kind": "ident", "id": "ident-print-001", "name": "print" },
        "args": [{ "kind": "literal", "id": "lit-msg-001", "value": "Hello, World!" }] },
      { "kind": "literal", "id": "lit-ret-001", "value": 0 }
    ]
  }]
}
```

### Variable binding (let)
```json
{ "kind": "let", "id": "let-x-001", "name": "x",
  "type": { "kind": "basic", "name": "Int" },
  "value": { "kind": "literal", "id": "lit-42-001", "value": 42 } }
```

### Conditional (if)
```json
{ "kind": "if", "id": "if-001",
  "condition": { "kind": "binop", "id": "cmp-001", "op": ">",
    "left": { "kind": "ident", "id": "id-x-001", "name": "x" },
    "right": { "kind": "literal", "id": "lit-0-001", "value": 0 } },
  "then": [{ "kind": "literal", "id": "lit-pos-001", "value": 1 }],
  "else": [{ "kind": "literal", "id": "lit-neg-001", "value": 0 }] }
```

### Record definition and construction
```json
{ "kind": "record", "id": "rec-point-001", "name": "Point",
  "fields": [
    { "kind": "field", "id": "field-x-001", "name": "x", "type": { "kind": "basic", "name": "Float" } },
    { "kind": "field", "id": "field-y-001", "name": "y", "type": { "kind": "basic", "name": "Float" } }
  ] }
```

```json
{ "kind": "record_expr", "id": "rexpr-001", "name": "Point",
  "fields": [
    { "name": "x", "value": { "kind": "literal", "id": "lit-x-001", "value": 1.0 } },
    { "name": "y", "value": { "kind": "literal", "id": "lit-y-001", "value": 2.0 } }
  ] }
```

## Reading Structured Errors

Every error is a JSON object with an `error` discriminator and `nodeId` pointing to the broken node.

| Error | What it means | How to fix |
|-------|-------------|-----------|
| `duplicate_id` | Two nodes share an ID | Make IDs unique |
| `unknown_node_kind` | Invalid `kind` value | Check `validKinds` in the error |
| `missing_field` | Required field absent | Add the field listed in the error |
| `undefined_reference` | Name not declared | Check `candidates` for similar names |
| `type_mismatch` | Wrong type | Compare `expected` vs `actual` in the error |
| `effect_violation` | Missing effect declaration | Add the effect from `calleeEffects` to your function |
| `contract_failure` | Pre/postcondition violated | Read `counterexample` for concrete failing inputs |
| `verification_timeout` | Z3 timed out | Simplify the predicate |

## Builtins

Available built-in functions (no need to import):
- `print(String) -> Int` — effect: `io`
- `intToString(Int) -> String` — effect: `pure`
- `floatToString(Float) -> String` — effect: `pure`
- `string_length(String) -> Int` — effect: `pure`
- `string_concat(String, String) -> String` — effect: `pure`
- `string_replace(String, String, String) -> String` — effect: `pure`
- `array_length(Array<T>) -> Int` — effect: `pure`
- `array_push(Array<T>, T) -> Array<T>` — effect: `pure`
- `array_get(Array<T>, Int) -> T` — effect: `pure`

## Execution & Security

Programs compile to **WebAssembly** and run in a sandboxed VM with no ambient authority. This is by design — agent-generated code needs stronger isolation than human-reviewed code.

- The WASM sandbox **cannot** access filesystem, network, or OS unless the host explicitly provides those capabilities
- **Effects are security declarations**: when you declare `effects: ["io"]`, you're telling the host "this program needs IO access." The host can refuse to run programs that request unwanted effects
- Host capabilities (file IO, HTTP, crypto) are provided via a pluggable `EdictHostAdapter` — the host controls what's available
- Runtime limits (`timeoutMs`, `maxMemoryMb`, `sandboxDir`) prevent runaway execution and constrain file access

This means your effect annotations aren't just for passing the compiler — they're the capability contract between your program and the host.

## Reference

For the complete AST schema, call the `edict_schema` MCP tool or read `schema/edict-schema.json`.
For example programs covering all features, see the `examples/` directory (28 programs).

---
name: result-check
description: >
  Enforces typed-error rules: RESULT-1 (domain failures should return typed
  errors / Result<T,E> rather than raw exceptions — BLOCK in Rust and
  TypeScript where the pattern is idiomatic, WARN in Python and JavaScript
  where exceptions are conventional), RESULT-2 (avoid null/None for
  not-found — use Option/Maybe/Result), RESULT-3 (no silently swallowed
  errors — empty catch blocks). Loaded by the conductor for write and review
  operations when core-layer code is in scope.
version: "1.0.0"
last-reviewed: "2026-05-13"
languages: [typescript, python, go, rust, javascript]
changelog: "../../CHANGELOG.md"
tools: Read, Grep, Glob, Bash
model: opus
permissionMode: default
---

# Result Check — Typed Error Discipline

Failures that the caller is expected to handle should appear in the function's
return type. Raw exceptions for *domain* failures (validation, business-rule
violations, not-found) hide control flow and make the function signature lie.
Reserve panics/throws for genuine programmer errors that callers cannot
recover from (assertion failures, unreachable branches).

This skill applies *only to files in `core/`* (per the conductor's Section 14
layer detection). Shell code uses idiomatic exceptions freely.

---

## Rules

### RESULT-1 — Domain Failures as Values, Not Exceptions
**Severity**:
- **BLOCK** in **Rust** (`Result<T, E>` is idiomatic and pervasive).
- **BLOCK** in **TypeScript** (discriminated unions, `Result<T, E>` from
  `neverthrow` or similar, or hand-rolled `{ ok: true, value } | { ok: false, error }`).
- **WARN** in **Python** (exceptions are conventional; encourage typed
  exception hierarchies and explicit catch sites but don't fight `raise`).
- **WARN** in **JavaScript** (exceptions are conventional; encourage typed
  results in modern code).
- **WARN** in **Go** (idiom is multi-return `(value, error)`, which already
  satisfies the spirit — flag only when functions `panic` for domain failures).

**Languages**: * | **Source**: CCC

**What it prohibits**: A core function that signals a *domain* failure via a
raw exception/throw/panic. Domain failures include:
- Validation errors (`InvalidEmail`, `NegativeAmount`)
- Business rule violations (`OrderAlreadyShipped`, `InsufficientInventory`)
- Not-found conditions (`OrderNotFound`, `UserNotFound`)
- Authorization failures (`Forbidden`, `Unauthorized`)

**Allowed (panics/throws are fine)**:
- Genuinely unreachable code paths (the `default` case of a sum type match
  where all variants are handled).
- Pre-condition violations the caller cannot recover from (`assert` style).
- Resource-exhaustion / system-level failures where the language convention
  is to throw (e.g., out-of-memory, network kill).

**Detection**: focus on exception-like control flow per language. Typed
error returns (`Err(...)`, Go's `(T, error)` tuple, `Result<T, E>`) are the
*preferred* path and must not be flagged.

1. In core files, grep by language:
   - TS/JS: `throw new` / `throw `.
   - Python: `raise ` (excluding `raise` inside an `except` re-raise chain).
   - Rust: `panic!`, `.unwrap()`, `.expect(`. Do **not** flag `Err(...)` or
     `bail!` — those are typed error returns.
   - Go: `panic(` for domain failures. Do **not** flag `return ..., err`.
2. For each hit: classify by exception/panic type. Domain-failure types
   (anything caller is expected to handle) are violations in Rust/TS;
   warnings elsewhere.

**agent_action**:
1. Cite: `RESULT-1 ({BLOCK|WARN}): Core function '{name}' raises '{type}' for domain failure at {file}:{line}.`
2. Propose: change return type to `Result<T, E>` / discriminated union /
   `Option<T>` (as appropriate). Show the equivalent typed-error version.
3. In Python/JS where WARN: also propose a typed exception class and an
   explicit catch site at the boundary.

---

### RESULT-2 — No `null` / `None` for Not-Found
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: A core function returning `null`/`None`/`nil` to mean
"not found" without an explicit `Option`/`Maybe`/`Result` type. The caller
should not have to read the function body to learn that the return value can
be missing.

**Examples**:
```
// FLAG:
function findOrder(id: OrderId): Order | null { ... }

// PASS:
function findOrder(id: OrderId): Order | undefined { ... }  // OK if convention is consistent
function findOrder(id: OrderId): Result<Order, NotFound> { ... }  // Better
function findOrder(id: OrderId): Option<Order> { ... }  // Best where supported
```

**Detection**:
1. Look for function return types matching `T | null` or returning bare `null`
   from a function whose name starts with `find`, `get`, `lookup`, `tryX`.
2. Python: look for functions annotated `-> Optional[T]` or returning `None`
   without it appearing in the signature.
3. Rust: look for functions returning `T` that panic on missing; suggest
   `Option<T>` or `Result<T, NotFound>`.

**Why WARN, not BLOCK**: `null`/`None`/`undefined` is idiomatic in many
codebases. Pushing toward typed alternatives is a quality lever, not a
correctness blocker.

**agent_action**:
1. Cite: `RESULT-2 (WARN): Function '{name}' returns null/None for not-found at {file}:{line} without an explicit Option/Maybe type.`
2. Propose the language-idiomatic typed alternative.

---

### RESULT-3 — No Silently Swallowed Errors
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: A catch/except/match arm that handles an error by doing
nothing meaningful (empty body, `pass`, a bare log + continue with no recovery).

**Examples**:
```
// FLAG:
try {
  doRisky()
} catch (e) {
  // nothing
}

// FLAG:
try:
    do_risky()
except Exception:
    pass

// PASS (explicit decision to suppress):
try:
    do_risky()
except CacheMissError:
    pass  # cache miss is expected; fall through to fetch
```

**Detection**:
1. Grep for `catch (e) {\s*}` / `catch (_)?\s*\{\s*\}` (TS/JS).
2. Grep for `except.*:\s*pass` (Python).
3. Grep for `_ = err` (Go where `err` is then unused).
4. Grep for `let _ = result;` discards (Rust).

**Allowed**:
- Catch sites with a comment explaining why the error is intentionally
  ignored. The comment is the proof of intent.
- Catches that re-raise after logging (the log is the action).

**agent_action**:
1. Cite: `RESULT-3 (WARN): Error caught and silently discarded at {file}:{line}.`
2. Propose: either (a) re-raise / propagate, (b) handle explicitly with a
   meaningful recovery action, or (c) add a comment explaining the intent
   to suppress.

---

Per-language typed-error idioms (neverthrow, `returns`, Go multi-return,
Rust Result, typed exception hierarchies): see `references/{language}.md`.

Report schema: see `skills/conductor/shared-contracts.md`.

**Severity overrides**: `RESULT-1`, `RESULT-2`, `RESULT-3` are
paradigm-family rules; a project may shift their severity
(`BLOCK` / `WARN` / `INFO`) via `.codex/config.json` `severity_overrides`.
Defaults stay as documented above (note `RESULT-1` defaults to BLOCK in
TypeScript/Rust and WARN in Python/JS/Go). See conductor §7.1.

---
name: immutability-check
description: >
  Enforces immutability rules: IMMUT-1 (no parameter mutation across function
  boundaries in core — produce new values rather than mutate inputs), IMMUT-2
  (no shared mutable state across concurrency boundaries), IMMUT-3 (no field
  reassignment after construction in core types). Loaded by the conductor for
  write and review operations when core-layer code is in scope. Local mutation
  inside a single function is allowed; only mutation observable across a
  public function boundary is enforced.
version: "1.0.0"
last-reviewed: "2026-05-13"
languages: [typescript, python, go, rust, javascript]
changelog: "../../CHANGELOG.md"
tools: Read, Grep, Glob, Bash
model: opus
permissionMode: default
---

# Immutability Check — Value Discipline in Core

Mutation is a local implementation detail, never visible across a public
function boundary. Inside a function, use whatever loop or accumulator is
clearest. But the function's *callers* should never have to wonder whether
their values were silently mutated.

This skill enforces immutability *only on files in `core/`* (per the
conductor's Section 14 layer detection).

---

## Rules

### IMMUT-1 — No Parameter Mutation Across Function Boundary
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: A function in `core/` mutating a value passed in as a
parameter such that the mutation is observable by the caller. This is the
canonical "silent corruption of caller's data" bug.

**Examples**:
```
// FLAG (mutates caller's array):
function applyDiscount(items: LineItem[], rate: number) {
  for (const item of items) {
    item.price = item.price * (1 - rate)
  }
}

// PASS (returns new values):
function applyDiscount(items: LineItem[], rate: number): LineItem[] {
  return items.map(item => ({ ...item, price: item.price * (1 - rate) }))
}
```

**Allowed**:
- Local-scoped mutation of a value *constructed* inside the function (build a
  result, return it).
- Mutation of an explicit `&mut`/output parameter when the language convention
  is clear about it (Rust `&mut`, Go pointer receiver where the caller
  obviously owns the pointer).

**Detection**:
1. For core files: grep for `param.X = ...` patterns where `param` is a
   function parameter.
2. Grep for in-place collection methods: `.push(`, `.splice(`, `.sort(`
   (without copy), `.pop(`, `.shift(`, Python `list.append`, `list.sort`
   without `sorted()`, etc., where the target is a parameter.

**agent_action**:
1. Cite: `IMMUT-1 (BLOCK): Function '{name}' mutates parameter '{param}' at {file}:{line}.`
2. Propose: return a new value (spread, `.map`, `[...]`, `dict({**d, ...})`,
   `struct.clone()`, etc.) instead of mutating in place.
3. Show the equivalent immutable version.

---

### IMMUT-2 — Shared Mutable State Across Concurrency Boundaries
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Module-level mutable state in core that's accessible
from concurrent contexts (worker threads, async tasks, goroutines) without
explicit synchronization.

**Detection**:
1. Look for module-level `let` / `var` / `mut` declarations holding mutable
   collections (not const primitives or frozen objects).
2. Look for `static mut` (Rust), package-level `var` (Go), module-globals in
   Python with mutating access from async functions.

**Why WARN**: legitimate use cases exist (caches, registries) but each is a
red flag worth a human look. Hard to detect reliably without false positives.

**agent_action**:
1. Cite: `IMMUT-2 (WARN): Shared mutable state '{name}' at {file}:{line} may race under concurrency.`
2. Propose: pass state explicitly through call chains, or move to a dedicated
   shell-layer cache adapter with proper synchronization.

---

### IMMUT-3 — No Field Reassignment After Construction
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Constructing an object in core with partial state, then
filling in fields via assignment. Prefer constructing with all fields at once
(builder pattern, factory function, named arguments).

**Examples**:
```
// FLAG (partial construction + reassignment):
const order = new Order()
order.id = orderId
order.customer = customer
order.items = items

// PASS (complete construction):
const order = new Order({ id: orderId, customer, items })
```

**Detection**:
1. In core files: find object construction followed within the same scope by
   field assignment to that object.
2. Particularly suspect: missing required-field assignments that could leave
   the object in an invalid state.

**agent_action**:
1. Cite: `IMMUT-3 (WARN): Object '{name}' is constructed then reassigned at {file}:{line}.`
2. Propose: use a constructor / factory that takes all fields at once. Pair
   with TYPED-2 (sum types for state) when partial construction reflects a
   state-machine concern.

---

Per-language mutation idioms (`.push`/`.splice` in JS, `list.append` in
Python, slice/map mutation in Go, `&mut` discipline in Rust): see
`references/{language}.md`.

Report schema: see `skills/conductor/shared-contracts.md`.

**Severity overrides**: `IMMUT-1`, `IMMUT-2`, `IMMUT-3` are paradigm-family
rules; a project may shift their severity (`BLOCK` / `WARN` / `INFO`) via
`.codex/config.json` `severity_overrides`. Defaults stay as documented
above. See conductor §7.1.

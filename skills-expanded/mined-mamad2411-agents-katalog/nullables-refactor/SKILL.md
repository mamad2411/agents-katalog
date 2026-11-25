---
name: nullables-refactor
description: "Analyze a file and produce a refactoring plan to apply the Nullables pattern. Classifies code by side-effect boundary (PURE, IN_MEMORY, OUTSIDE_WORLD), identifies HARDWIRED_INFRA, recommends INFRASTRUCTURE_WRAPPER or NULLABLE_CLASS conversion, checks DUAL_FACTORY and CREATE_BOUNDARY_RULE compliance, and decides on DELAYED_INSTANTIATION. Use when asked to refactor a file or module to follow the nullables pattern."
---

# Nullables Refactor

Analyze a file and produce a step-by-step refactoring plan to make OUTSIDE_WORLD code nullable.

## Vocabulary

This skill uses terms from `references/vocabulary.md`. Key terms: PURE, IN_MEMORY, OUTSIDE_WORLD, INFRASTRUCTURE_WRAPPER, NULLABLE_CLASS, HARDWIRED_INFRA, INJECTED_INFRA, CREATE_BOUNDARY_RULE, DUAL_FACTORY, EMBEDDED_STUB, NULLABLE, FACTORY_OBJECT, DELAYED_INSTANTIATION, CONFIGURABLE_RESPONSE, OUTPUT_TRACKING, VALUE_OBJECT.

## How We Break Down The World

Code is classified by where its side effects reach:

| Category | Side effects | Nullable treatment needed? | Examples |
|----------|-------------|---------------------------|----------|
| **PURE** | None | No | Computations, transformations, formatters |
| **IN_MEMORY** | Mutates things passed in or held in memory | No | DOM manipulation, mutable data structures, in-memory state |
| **OUTSIDE_WORLD** | Crosses the process boundary (I/O) | **Yes** | Network calls, disk access, database queries, environment reads |

The nullables pattern specifically targets **OUTSIDE_WORLD** code. PURE and IN_MEMORY code is fine as-is.

Within OUTSIDE_WORLD code, there are two kinds of entity:

| Entity | Role | Has DUAL_FACTORY? | Contains I/O directly? |
|--------|------|-------------------|----------------------|
| **INFRASTRUCTURE_WRAPPER** | Wraps one external system. Leaf of the dependency graph. | Yes — owns the EMBEDDED_STUB | Yes — that's its job |
| **NULLABLE_CLASS** | Orchestrates injected dependencies that talk to the outside world. | Yes — injects NULLABLEs in `.createNull()` | No — receives wrappers via injection |

An application-level class is effectively a high-level NULLABLE_CLASS because it holds instances that ultimately reach the outside world.

Code that doesn't talk to the outside world:

| Entity | Treatment |
|--------|-----------|
| **PURE** functions/classes | No special treatment. Plain functions or classes with `.create()` if stateful. |
| **VALUE_OBJECT** | `.create()` + `.createTestInstance()`. No `.createNull()`. Mutable VALUE_OBJECTs are IN_MEMORY, not OUTSIDE_WORLD. |

## Input

The user provides a file path (or file contents). The agent reads the file, analyzes it, and produces a plan. The agent does NOT execute the plan without confirmation.

## Analysis Algorithm

For each exported class, function, or significant code unit in the file:

### Step 1: Classify by side-effect boundary

For each code unit, ask: where do its side effects reach?

- **PURE** — no side effects. Same inputs → same outputs, touches nothing else.
- **IN_MEMORY** — mutates things passed to it or held in memory (DOM nodes, data structures), but never crosses the process boundary.
- **OUTSIDE_WORLD** — performs I/O across the process boundary (network, disk, database, environment, third-party services).

### Step 2: For OUTSIDE_WORLD code — INFRASTRUCTURE_WRAPPER or NULLABLE_CLASS?

Skip to Step 3 for PURE or IN_MEMORY code.

This is the critical first question for any OUTSIDE_WORLD code unit. Before checking anything else:

#### If it's a standalone function with OUTSIDE_WORLD side effects

This is HARDWIRED_INFRA. A function that performs I/O should become an INFRASTRUCTURE_WRAPPER class:

- **Recommend**: convert to a class with DUAL_FACTORY (`.create()` / `.createNull()`).
- The class wraps the external system and provides a clean API.
- `.createNull()` uses an EMBEDDED_STUB to replace the real I/O.
- Name it descriptively: `HttpClient`, `FileStore`, `DatabaseRepo`, etc.
- The class should provide data in the form the application needs, not the external system's raw format.

#### If it's a class — determine its role:

- **Is its sole purpose to wrap one external system** (e.g., HTTP, database, filesystem)? → It should be an **INFRASTRUCTURE_WRAPPER**. It owns the EMBEDDED_STUB, provides CONFIGURABLE_RESPONSE, and is the leaf of the dependency graph.
- **Does it have business logic or orchestration AND also contain I/O calls?** → It is a **NULLABLE_CLASS** that has HARDWIRED_INFRA. The I/O should be **extracted** into a separate INFRASTRUCTURE_WRAPPER and injected into this class.

The difference matters: an INFRASTRUCTURE_WRAPPER *contains* the external calls and stubs them internally. A NULLABLE_CLASS *uses* INFRASTRUCTURE_WRAPPERs via injection and gets NULLABLE versions in tests.

Then check the following:

1. **HARDWIRED_INFRA?**
   - Scan for any OUTSIDE_WORLD calls used directly inside the class (imported and called inline rather than injected). These are HARDWIRED_INFRA.
   - PURE and IN_MEMORY code is fine — only flag code that crosses the process boundary.
   - **Recommend**: extract into an INFRASTRUCTURE_WRAPPER and inject through CREATE_BOUNDARY_RULE.
   - This check comes first because it often reshapes the class — the remaining checks apply to the class *after* extraction.

2. **Has DUAL_FACTORY?**
   - Does the class have a static `.create()` method? If not, flag it.
   - Does the class have a static `.createNull()` method? If not, flag it.
   - Does `.createNull()` accept CONFIGURABLE_RESPONSE parameters? If it has OUTSIDE_WORLD dependencies, it should.

3. **CREATE_BOUNDARY_RULE compliance?**
   - Scan `.create()`: every OUTSIDE_WORLD dependency should be instantiated via `Dependency.create()`, not `new Dependency()`.
   - These calls must be **lexically inside the static `.create()` method** — this is the CREATE_BOUNDARY_RULE. Not in instance methods, not in the constructor.
   - Scan `.createNull()`: same rule, using `Dependency.createNull()`.
   - CONFIGURABLE_RESPONSE parameters from the outer `.createNull()` should flow down to inner `.createNull()` calls where appropriate.
   - If an instance method or constructor calls `SomeClass.create()`, this is a CREATE_BOUNDARY_RULE violation. Two remedies:
     - **Immediate instantiation**: move the `.create()` call into the static `.create()` and inject the instance via constructor.
     - **DELAYED_INSTANTIATION**: if the dependency is only needed conditionally or after an event, pass a FACTORY_OBJECT via the constructor instead.

4. **Decide on DELAYED_INSTANTIATION**
   - For each dependency, ask: is it always needed, or only under certain conditions?
   - **Always needed** → immediate instantiation in `.create()`.
   - **Conditionally needed** (based on runtime state, events, user input) → DELAYED_INSTANTIATION via FACTORY_OBJECT.
   - If multiple delayed dependencies exist, group them into a single FACTORY_OBJECT: `{ Bar: (...) => Bar.create(...), Baz: (...) => Baz.create(...) }`.

5. **OUTPUT_TRACKING needed?**
   - If the class writes to external systems, recommend adding event emission and `trackX()` methods for testability.

### Step 3: For PURE, IN_MEMORY, and VALUE_OBJECT code

#### PURE or IN_MEMORY code
- No nullable treatment needed.
- If stateless → plain functions are fine.
- If stateful with IN_MEMORY mutation → a class with `.create()` is fine. No `.createNull()` needed.
- **Flag any OUTSIDE_WORLD calls found here** — they're HARDWIRED_INFRA that should be extracted.

#### VALUE_OBJECT
- Should have `.create()` (may require all params).
- Should have `.createTestInstance()` with convenient defaults.
- No `.createNull()` needed.
- Mutable VALUE_OBJECTs doing IN_MEMORY work are fine.
- **Flag any OUTSIDE_WORLD operations** — they don't belong here.

### Step 3: Check for third-party framework interactions

- If the code uses a DI framework (e.g., effect-ts), flag it. The boundary between framework-managed injection and DUAL_FACTORY needs case-by-case discussion.
- If the code uses a third-party library for I/O (e.g., tanstack-query, axios), note whether the library provides a test client. Recommend how it fits into the DUAL_FACTORY architecture.

### Step 4: Identify the dependency graph

- List all dependencies the code creates or uses.
- For each dependency, note whether it already has DUAL_FACTORY.
- If not, flag it — the refactoring may need to recurse into those dependencies.
- Order the plan so that leaf dependencies (INFRASTRUCTURE_WRAPPERs) are refactored first, then work up to Application layer.

## Output Format

Present the plan as:

```
## Refactoring Plan: <filename>

### Classification
| Code Unit | Side Effects | Entity Type | Current State | Target State |
|-----------|-------------|-------------|--------------|--------------|
| ...       | PURE / IN_MEMORY / OUTSIDE_WORLD | INFRASTRUCTURE_WRAPPER / NULLABLE_CLASS / PURE / VALUE_OBJECT | ... | ... |

### Issues Found
1. **[HARDWIRED_INFRA | CREATE_BOUNDARY_RULE_VIOLATION | MISSING_DUAL_FACTORY | ...]** `CodeUnit` — description
   - **Recommendation**: what to do
   - **Why**: brief rationale

### Dependency Graph
- `AppClass` → `ServiceClass` → `HttpClient` (leaf)
  - Refactor order: HttpClient → ServiceClass → AppClass

### Steps
1. ...
2. ...
3. ...

### Questions for the human
- Any decisions that need human input (e.g., naming, DELAYED_INSTANTIATION vs immediate, third-party framework boundaries)
```

## After Refactoring

Once the refactoring plan has been executed, use the `nullables-test` skill to write tests. That skill checks that:
- All HARDWIRED_INFRA has been replaced by INJECTED_INFRA
- Every piece of INJECTED_INFRA has `.createNull()` (recursing into dependencies if needed)
- The class under test is ready for narrow, sociable, state-based tests via `.createNull()`

## What This Skill Does NOT Do

- Does not execute the refactoring — it produces the plan for the human to review.
- Does not write tests — use `nullables-test` after refactoring is complete.
- Does not make decisions about third-party framework boundaries — it flags them for discussion.

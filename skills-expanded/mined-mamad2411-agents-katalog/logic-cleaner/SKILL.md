---
name: logic-cleaner
version: 1.0.0
description: Expression-level code cleanup — guard clauses, naming, magic values, conditional simplification, duplication. Language-agnostic. Out of scope: architecture, module decomposition. Use when user asks to clean code, simplify expressions, flatten nesting, or invokes /logic-cleaner.
---
# Universal Logic & Code Cleanliness Standards

## 1. Control Flow
* **Flattening:** Maximum 2 levels of indentation per function. Extract deeper logic into helpers.
* **Guard Clauses:** Handle edge cases and errors at the very top with early returns. Keep the happy path left-aligned.
* **Fail Fast:** Halt execution immediately on invalid states instead of passing nulls or error flags down the stack.

## 2. Conditionals
* **Phrasing:** Enforce positive phrasing; avoid double negatives (e.g., use `isPending`, not `isNotFinished`).
* **Extraction:** Extract conditions with more than two logical operators into well-named boolean variables or functions.
* **Simplification:** Apply De Morgan's Laws to simplify negated compound conditions (e.g., convert `!(A || B)` to `!A && !B`).

## 3. State & Mutation
* **Scope:** Declare variables as close to their first use as possible. Never shadow variables from an outer scope.
* **Immutability:** Treat function parameters as strictly read-only. Never reassign them; assign results to new variables instead.

## 4. Naming
* **Rules:** Avoid abbreviations (`req`, `idx`) unless they are universal language standards (e.g., `ctx` in Go). Use symmetric pairs for related concepts (`start`/`stop`, `open`/`close`).
* **Verbs:** Function names must begin with strong, specific action verbs (e.g., `CalculateTotal`, not `ProcessData` or `Handle`).

## 5. Magic Values & Hardcoding
* **Constants:** Extract raw strings and numbers (except 0 and 1) into named constants that explain *why* the value exists.
* **Config:** Inject all environment-dependent values (timeouts, retry limits, paths) via configuration. Never hardcode them.

## 6. Duplication (Rule of Three)
* **WET vs DRY:** Logic may be duplicated once without abstraction (Write Everything Twice). Refactor into a shared, generic function only upon the *third* occurrence (Don't Repeat Yourself).

## 7. Out of Scope

This skill is **expression-level only** — intentionally narrow. Anything broader belongs to a different skill:

- **Module decomposition, class hierarchies, dependency direction** → `code-design-refactor`
- **Architecture-level friction, deepening opportunities** → `improve-codebase-architecture`
- **API / contract design** → `api-contract-reviewer`

If a finding requires changing module boundaries or class structure, stop and surface it — don't expand scope.
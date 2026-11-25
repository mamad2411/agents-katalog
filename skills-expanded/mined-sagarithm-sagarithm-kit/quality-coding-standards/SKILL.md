<!-- SAGARITHM:START - DO NOT EDIT DIRECTLY -->
---
id: "quality.coding-standards"
name: "Clean Code & Quality Standards"
version: "1.2.0"
domain: "quality"
description: "Author expressive, type-safe, maintainable code with strict error handling, nominal typing, discriminated unions, and concurrency safety."
triggers:
  - "Writing or refactoring functions, classes, or modules"
  - "Handling asynchronous control flow or cancellation tokens"
  - "Designing complex domain state machines or value objects"
  - "Reviewing code quality or addressing static analysis feedback"
prerequisites: []
risk_profile: "medium"
---

# Clean Code & Quality Standards

## Overview
This skill guides AI agents and engineers in authoring code that is immediately readable, strictly typed, resilient to runtime failure, and simple to maintain.

## Core Directives
1. **Strict Type Safety**: Never use `any`, untyped collections, or disable linter rules without justification. Model explicit data shapes.
2. **Prevent Primitive Obsession**: Use branded types or value objects for domain identifiers and units.
3. **Exhaustive State Handling**: Model multi-state domain flows with discriminated unions and enforce exhaustive compile-time checking (`assertNever`).
4. **Explicit Failure Modeling**: For operations where failure is an expected domain branch (validation, parsing), consider `Result<T, E>` types rather than throwing unchecked exceptions.
5. **Never Swallow Errors**: Handle errors at the appropriate layer; never leave empty catch blocks or discard stack traces.
6. **Cancellation & Concurrency Hygiene**: Support `AbortSignal` for cancellable async tasks and guard against race conditions.

## 🛑 Anti-Rationalization Matrix

| Agent Excuse / Shortcut | Quality Reality | Mandatory Action |
|---|---|---|
| *"Using `any` here just speeds things up."* | `any` is a virus that silently disables compiler checking throughout the codebase. | Model explicit TypeScript interfaces or use `unknown` with type guards. |
| *"I'll leave this `catch (e) {}` empty since it rarely fails."* | Swallowed exceptions cause invisible state corruption that takes days to debug. | Log the error or rethrow a domain-specific error. |
| *"A generic string is fine for this ID."* | Primitive obsession causes accidental bugs where user IDs are passed as order IDs. | Use branded nominal types (e.g. `UserId = string & { __brand: 'UserId' }`). |

## Detailed Guidance
- [Clean Code & Typing Principles](references/clean-code-and-typing.md)
- [Advanced Type Algebra & Concurrency Safety](references/type-algebra-and-immutability.md)
- [Robust Error Handling Patterns](examples/robust-error-handling-patterns.md)
- [Advanced Type Patterns & Result Monad](examples/advanced-type-patterns.md)
- [Code Quality Checklist](checklists/code-quality-checklist.md)
<!-- SAGARITHM:END -->

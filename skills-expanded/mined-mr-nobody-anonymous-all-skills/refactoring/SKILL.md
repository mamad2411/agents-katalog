---
name: refactoring
description: Improve the internal structure of existing code without changing external behavior — naming, decomposition, clarity, duplication removal.
category: development
aliases:
- refactor
- clean-up
- simplify
- restructure
triggers:
- refactor this
- clean up this code
- simplify this
- rename this
- extract a function
- make this clearer
keywords:
- refactor
- clean
- simplify
- rename
- extract
- structure
- readability
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- clean
- development
- refactor
- refactoring
- rename
- simplify
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Refactoring

## Purpose

Improve code structure without changing behavior. Extract functions, rename for clarity,
remove duplication, and reorganize for the next reader.

## When to Use

- Code works but is hard to read or change
- Duplication has crept in
- A function has grown too large
- Naming no longer matches purpose

## When NOT to Use

- Behavior is wrong (route to `debugging`)
- The structure needs to change to support a new feature (route to `architecture` first)
- The codebase has no tests (write tests for current behavior FIRST)

## Capabilities

- Extract function / method
- Rename for clarity
- Remove duplication (DRY)
- Replace conditional with polymorphism or table
- Introduce parameter objects
- Move code to better location

## Inputs

- The code to refactor
- Constraints (must preserve behavior, tests must pass)

## Workflow

1. **Have tests.** If not, write characterization tests that pin current behavior.
2. **Make small, atomic changes.** One rename, one extract, one move. Not ten at once.
3. **Run tests after each change.**
4. **Commit frequently.** Each refactor as its own commit makes review and revert easy.
5. **Stop when the code is "good enough."** Refactor is in service of the next change, not perfection.

## Tools

- Editor refactor tools (rename, extract)
- Test runner
- Version control

## Examples

**User:** "This function is 200 lines. Help."
**Response:** "Let's identify 3–5 sub-responsibilities. Extract each into a named helper. Keep the public signature. Run tests after each extraction."

## Safety

- Behavior must be preserved
- Don't refactor without tests
- Don't bundle refactors with feature changes

## Source

Custom skill, written for this library. Based on Fowler's "Refactoring."

## Notes

Pairs with:
- `coding` (when refactor reveals new structure)
- `testing` (always — tests are the safety net)
- `code-review` (the refactor is the review)
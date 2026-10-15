---
name: code-discipline
description: Prevent unnecessary helpers, wrappers, abstractions, and duplicate implementations. Enforce reuse of platform primitives, framework capabilities, shared utilities, and proven libraries. Use when implementing features to ensure code discipline and reduce technical debt.
license: Apache-2.0
metadata:
  author: Mike Willbanks
  repository: https://github.com/mwillbanks/agent-skills
  homepage: https://github.com/mwillbanks/agent-skills
  bugs: https://github.com/mwillbanks/agent-skills/issues
---

# Code Discipline

Use this skill whenever a task involves adding or modifying logic and there is risk of helper sprawl, unnecessary wrappers, duplicate utilities, or abstraction bloat.

This is an anti-laziness skill. It prevents agents from "solving" tasks by inventing new files, helpers, and indirection when existing primitives already solve the problem.

Default assumption:

- The user wants maintainable code with minimal abstraction surface area.
- The user does not want renamed duplicates of existing behavior.
- New helpers and wrappers are disallowed unless justified by clear architectural value.

## When to Use

Invoke this skill for:

- feature implementation that introduces new logic
- refactors that add utility or service layers
- UI changes where component-local helpers may proliferate
- bug fixes that tempt quick wrapper-based patches
- code review focused on maintainability and reuse discipline

Use together with `agent-execution-mode` and `repo-standards-enforcement` for production implementation work.

## Core Enforcement Policy

### Non-Negotiable

- Do not create a helper if the logic is trivial and used once.
- Do not create a wrapper that only forwards calls.
- Do not create renamed duplicates of existing utilities.
- Do not add service, hook, or adapter layers that add indirection without policy.
- Do not reimplement platform or standard library behavior.
- Do not duplicate utility logic across packages.

### Required Posture

- prefer platform primitives first
- prefer framework-native capabilities second
- prefer existing internal utilities third
- prefer existing repository dependencies fourth
- create new abstraction only as a last resort with explicit rationale

## Mandatory Evaluation Order

Before adding any helper, hook, service, wrapper, adapter, formatter, parser, transformer, or utility, evaluate in this exact order:

1. language or runtime primitives
2. standard library APIs
3. framework-native features
4. existing repository utilities
5. existing installed dependencies
6. new abstraction with justification

Skipping this order is non-compliant behavior.

## New Abstraction Admission Gate

A new abstraction is allowed only if at least one is true:

- it enforces domain invariants or policy
- it encapsulates non-trivial repeated logic across multiple call sites
- it isolates an infrastructure boundary
- it provides correctness, validation, or security guarantees
- it improves testability of genuinely complex behavior

A new abstraction is rejected if it only:

- renames existing behavior
- forwards calls one-to-one
- wraps a single primitive or single library call
- exists for style preference only

## Smell Rules

Treat these as automatic scrutiny triggers:

- names starting with `normalize`, `format`, `parse`, `transform`, `sanitize`, `safe`, `to`
- services that only proxy repository or SDK methods
- hooks that only call another hook and return the same shape
- helpers used once in a single file
- utility modules that only contain one-line wrappers

Smells are not always wrong, but they require explicit defense.

## Component Logic Rules

- Keep simple display and one-off transformations inline.
- Extract only when complexity or reuse justifies extraction.
- Do not grow component files into local utility libraries.
- Move reusable logic to the correct shared layer, not the nearest file.

## Monorepo and Workspace Rules

- do not duplicate helpers across packages
- promote shared logic to the correct shared package when reuse exists
- respect architecture boundaries when sharing utilities
- do not bypass boundaries through convenience imports

## Review and Refactor Enforcement

When active in review/refactor mode, agents must:

- flag unnecessary helpers and wrappers
- remove trivial abstractions where safe
- consolidate duplicate utilities
- replace handwritten logic with platform/library primitives where appropriate
- explain each removal or consolidation with maintainability rationale

## Definition of Done

This skill is satisfied only when all are true:

- no newly introduced trivial helper/wrapper layers remain
- no duplicate utility logic remains in changed scope
- new abstractions (if any) are justified by the admission gate
- platform/framework/internal utilities were preferred over reinvention
- changed scope is simpler or equal in surface area, not more bloated

## Output Contract

When responding after this skill is used, report:

- what abstraction/helper candidates were considered
- what existing primitive/utility was reused
- what abstractions were rejected and why
- what consolidations/removals were performed
- any new abstraction added and which admission-gate condition allowed it

## References

Use the reference guides for strict implementation details:

- `references/helper-functions.md`
- `references/abstraction-patterns.md`
- `references/library-preference.md`
- `references/component-logic.md`
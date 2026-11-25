---
name: typescript-6-type-review
description: Reviews TypeScript 6 types, generics, public contracts, type leakage, trust boundaries, and safe type-only refactors. Use when reviewing type quality, improving strictness, removing unsafe casts, or refactoring types without changing runtime behavior.
license: MIT
compatibility: Requires a TypeScript 6.x project or a project migrating to TypeScript 6.x.
---

# TypeScript 6 Type Review

Use this skill when reviewing or improving TypeScript types without turning the work into a broad rewrite.

## What This Skill Checks

- Trust-boundary types.
- API and package contracts.
- Generic constraints and inference quality.
- Type leakage between transport, persistence, framework, and domain layers.
- Unsafe `any`, `as`, double assertions, non-null assertions, and broad suppressions.
- Whether type changes preserve runtime behavior.
- Whether exported declarations remain stable and intentional.

## Review Principles

1. Prefer precise domain types over structural shortcuts.
2. Keep unsafe typing local and documented.
3. Do not make runtime behavior depend on erased TypeScript types.
4. Add runtime validation where the data source is untrusted.
5. Avoid leaking framework, SDK, ORM, or generated transport types into stable domain contracts.
6. Prefer small type improvements over large mechanical rewrites unless the user asked for a migration.
7. Verify with typecheck and affected tests when possible.

## When to Use Each Workflow

Use `workflows/type-review-workflow.md` when reviewing a change, pull request, or design for type quality.

Use `workflows/safe-type-refactor-workflow.md` when improving types while preserving runtime behavior.

## Resources and Examples

- `resources/type-boundary-checklist.md` contains a review checklist for trust boundaries, APIs, generics, and type leakage.
- `examples/safe-type-refactor-example.md` shows a small refactor from unsafe `any` to `unknown` plus validation.
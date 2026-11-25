---
name: typescript-advanced
description: "Use advanced TypeScript deliberately: generics with constraints, conditional and mapped types, template literals, discriminated unions and safe module augmentation."
type: procedural
category: web
domain: web
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - typescript generic constraints
  - conditional type inference
  - typescript mapped types
  - template literal types
  - typescript type error complex
aliases:
  - ts-advanced
keywords:
  - typescript
  - generics
  - conditional-types
  - mapped-types
  - inference
  - declaration
mcp_servers:
  - filesystem
source: custom
enabled: true
---

# Advanced TypeScript Types

## Purpose

Use advanced TypeScript deliberately: generics with constraints, conditional and mapped types, template literals, discriminated unions and safe module augmentation.

## When to Use

- A public API must be typed so callers cannot misuse it.
- Types are duplicated by hand and drift from runtime validation.
- An inference failure needs a real explanation, not an `any`.

## When NOT to Use

- The codebase is plain JavaScript with no migration plan.
- The problem is a runtime bug that types cannot catch.
- A one-off script where `unknown` plus a guard is enough.

## Capabilities

- Design generics with constraints and defaults that infer from call sites.
- Use conditional and mapped types to derive types from a single source.
- Encode string formats and route parameters with template literal types.
- Model state machines with discriminated unions and exhaustive checks.
- Augment or declare modules without leaking globals.

## Inputs

- The runtime contract that the types must describe.
- The TypeScript version, since inference and features differ.
- The consumer surface: library types must be readable in editor tooltips.

## Workflow

1. Write the runtime schema or guard first, then derive the type from it.
2. Prefer one source of truth and `typeof`/indexed access over duplicated interfaces.
3. Add constraints to generics so misuse fails at the call site, not deep inside.
4. Make unions exhaustive with a `never` check in the default branch.
5. Check the emitted `.d.ts` and hover text: types nobody can read are a defect.
6. Run `tsc --noEmit` in strict mode and keep `any` out of public signatures.

## Tools

- typescript
- tsc
- eslint
- zod

## Examples

- ``type Route = `/users/${string}/posts/${number}`` catches malformed links at compile time.`
- `Deriving `type User = z.infer<typeof UserSchema>` removes a whole class of drift.`

## Safety

- Never widen a public type to `any` to silence an error you have not understood.
- Declaration merging can break consumers silently; scope it and document it.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `filesystem` | stdio | core | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/web/typescript-advanced`). First-party skill, maintained in this repository.

## Notes

- If a type needs three comments to explain, the API is probably wrong.
- `satisfies` preserves literals while still checking shape — use it instead of annotation.
- Pairs with: `component-testing`, `nextjs-app-router`.

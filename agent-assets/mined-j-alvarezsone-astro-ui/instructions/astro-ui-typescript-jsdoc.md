---
description: "Use when creating or updating TypeScript functions to enforce JSDoc completeness."
applyTo: "src/**/*.ts,scripts/**/*.mts"
---

# TypeScript Function JSDoc

When creating a new function, always add full JSDoc.

## JSDoc Tags

Minimum required tags:

- `@param` for each function parameter
- `@returns` describing the return value
- `@example` with at least one realistic usage snippet

## JSDoc Content Rules

- Keep examples short and copy-pasteable.
- Keep descriptions practical and specific to behavior.
- Ensure examples use only real API/config keys that exist in current types.
- Ensure example output strings (for example generated CSS vars) match the function's actual emitted names exactly.
- Apply this to exported and non-exported functions unless the function has fewer than 3 lines of code and no branching logic.

## Signature Requirements

For non-trivial functions:

- Type every parameter explicitly.
- Add an explicit return type annotation.
- Do not rely only on inferred return types when branching/complex logic can make intent unclear.

---
name: wp-abilities-mcp-development-ability-design
description: Designs and implements typed, permissioned WordPress Abilities. Use when creating or refactoring an Ability contract, category, callback, schema, annotations, or PHP execution path.
---

# Ability Design

## Use This Skill For

- New server-side Abilities.
- Refactoring existing functions into discoverable contracts.
- Ability categories, names, schemas, callbacks, errors, and annotations.
- PHP-to-PHP composition with `wp_get_ability()`.

## Process

1. Identify the exact business action and caller contexts.
2. Decide whether an Ability is needed or a normal internal function is sufficient.
3. Define a stable namespaced identifier and registered category.
4. Write input and output schemas before callbacks.
5. Define minimum capability and object-level checks using the same input as execution.
6. Implement the execute callback with `WP_Error` failures and schema-compatible output.
7. Mark annotations from observed behavior, not intent.
8. Add tests before enabling REST or MCP exposure.
9. Use `workflows/design-ability-workflow.md` for a complete design pass.
10. Use `resources/ability-contract-checklist.md` before review.

## Example

See `examples/secure-read-only-ability.md` for a read-only, capability-checked pattern.

## Boundaries

- Do not expose the Ability to REST or MCP automatically.
- Do not use `__return_true` as a convenience.
- Do not return WordPress objects or database rows without an explicit output contract.

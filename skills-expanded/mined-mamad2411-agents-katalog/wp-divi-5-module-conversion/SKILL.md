---
name: wp-divi-5-module-conversion
description: Converts Divi 4 custom modules and saved shortcode attributes to Divi 5 with an explicit inventory, attribute mapping, isolated legacy code, deterministic conversion tests, content-preservation checks, and rollback planning. Use only when existing Divi 4 content must remain usable.
---

# wp-divi-5-module-conversion

Use this skill only when real Divi 4 modules or saved content require compatibility. New modules must use the current Divi 5 architecture without a legacy layer.

## Required Inputs

- Divi 4 module PHP and Visual Builder implementation.
- Legacy shortcode name and all saved attributes.
- Representative serialized content fixtures.
- Current Divi 5 module contract.
- Unsupported or changed behavior.
- Site and extension version matrix.
- Rollback and mixed-content requirements.

## Principles

- Inventory before mapping.
- Preserve content meaning, not implementation quirks.
- Keep legacy runtime code isolated.
- Make mappings explicit and deterministic.
- Preserve unknown data or fail visibly; do not silently discard it.
- Test conversion idempotency.
- Keep a rollback or recoverable backup path for production content.
- Do not claim site migration safety from unit tests alone.

## Workflow

Use [`workflows/convert-divi-4-module-workflow.md`](workflows/convert-divi-4-module-workflow.md).

## Resource

Use [`resources/divi-4-to-5-conversion-map.md`](resources/divi-4-to-5-conversion-map.md).

## Completion Evidence

Record the legacy inventory, mapping table, unsupported behavior, fixtures, conversion results, idempotency, mixed D4/D5 behavior, frontend comparison, package impact, and rollback plan.

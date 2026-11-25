---
name: wp-block-implementation
description: Implements and repairs WordPress blocks using block.json, server registration, attributes, wrappers, InnerBlocks, supports, variations, transforms, bindings, and safe rendering.
---

# WordPress Block Implementation

Use this skill after architecture is approved.

## Procedure

1. Inspect the compatibility floor and existing build system.
2. Use `block.json` as the canonical metadata contract.
3. Register from metadata on the server when PHP is available.
4. Keep edit, save, PHP render, styles, and asset declarations consistent.
5. Implement the smallest set of attributes and supports required.
6. Use wrapper APIs instead of manually recreating support classes.
7. Add deprecations before changing static saved markup.
8. Validate metadata with the included auditor.
9. Run build and task-specific tests.

## Workflow

Use `workflows/implement-block-workflow.md`.

## Resource

- `resources/block-json-field-guide.md`

## Examples

- `examples/static-block-example.md`
- `examples/dynamic-block-example.md`

## Script

Run help first:

```powershell
python scripts/audit-block-metadata.py --help
```

From an installed plugin, use the full path documented in the root README.

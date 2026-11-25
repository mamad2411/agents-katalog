---
name: wp-divi-5-module-development
description: Builds or refactors Divi 5 static, dynamic, parent, child, or converted modules with explicit metadata, attributes, settings, editor behavior, PHP frontend rendering, styles, accessibility, failure handling, and tests. Use for module implementation work.
---

# wp-divi-5-module-development

Use this skill after the extension architecture and compatibility boundary are known.

## Required Inputs

- Module purpose and content model.
- Selected module type.
- Attribute contract and defaults.
- Settings and conditional-control requirements.
- Frontend semantics and accessibility requirements.
- Dynamic data and permission needs.
- Parent/child constraints.
- Responsive, hover, sticky, and animation behavior.
- Existing content or Divi 4 conversion requirements.

## Principles

- Design the serialized attribute contract before UI details.
- Keep module and CSS namespaces stable and unique.
- Use generated settings when they fit; add custom settings only for real requirements.
- Keep editor and PHP render behavior aligned.
- Use semantic HTML and preserve logical reading order.
- Bound dynamic queries and handle empty, loading, error, and unauthorized states.
- Avoid storing derived values that can be computed reliably.
- Add tests with the module, not after the feature appears complete.

## Workflow

Use [`workflows/build-divi-module-workflow.md`](workflows/build-divi-module-workflow.md).

## Resources

- [`resources/module-type-decision-matrix.md`](resources/module-type-decision-matrix.md)
- [`examples/module-contract-outline.md`](examples/module-contract-outline.md)

## Completion Evidence

Record the module contract, metadata path, frontend renderer, editor component, state matrix, parent/child rules, tests, build output, and logged-out frontend verification.

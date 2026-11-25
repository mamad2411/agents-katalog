---
name: wp-block-testing-quality
description: Tests and reviews WordPress blocks across builds, serialization, PHP rendering, editor flows, accessibility, performance, compatibility versions, and release artifacts.
---

# WordPress Block Testing and Quality

Use this skill before review, release, or after a regression.

## Procedure

1. Read `resources/test-matrix.md`.
2. Run the metadata auditor.
3. Run production build, lint, formatting, and type checks used by the project.
4. Run JavaScript unit tests and PHP tests where applicable.
5. Test serialization and historical deprecation fixtures.
6. Run focused Playwright E2E flows in the editor and front end.
7. Review accessibility and performance.
8. Test minimum and latest supported WordPress versions.
9. Compare generated assets with source and package contents.

## Workflows

- `workflows/test-block-workflow.md`
- `workflows/review-block-workflow.md`

## Resource

- `resources/test-matrix.md`

## Example

- `examples/serialization-test-example.md`

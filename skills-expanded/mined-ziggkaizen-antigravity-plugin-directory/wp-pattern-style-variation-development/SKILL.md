---
name: wp-pattern-style-variation-development
description: Creates and reviews WordPress block-theme file-based patterns, starter patterns, locking choices, block style variations, and complete theme style variations. Use for reusable visual compositions and alternate design systems.
---

# wp-pattern-style-variation-development

Use this skill when a reusable artifact should be a pattern or style variation rather than a template, part, custom block, or duplicated markup.

## Required Inputs

- Intended reuse and editing model.
- Theme namespace and stable slug.
- Minimum WordPress version.
- Translation requirements.
- Whether content is theme-owned, site-owned, synced, or unsynced.
- Blocks and templates that must support the variation.
- Locking and accessibility requirements.

## Principles

- Use a pattern for reusable block composition.
- Use a template part for structural site regions.
- Use a template for query/document structure.
- Use a style variation for an alternate design system.
- Use a custom block for portable behavior.
- Keep behavior and external side effects out of patterns.
- Use locking only when it improves the editing contract.
- Test style variations across templates, parts, patterns, and common blocks.

## Workflow

Use [`workflows/build-patterns-style-variations-workflow.md`](workflows/build-patterns-style-variations-workflow.md).

## Resource

Use [`resources/pattern-style-variation-decision-matrix.md`](resources/pattern-style-variation-decision-matrix.md).

## Example

Use [`examples/file-based-pattern.php`](examples/file-based-pattern.php).

## Completion Evidence

Record:

- Artifact type and reason.
- Namespace/slug.
- Registration source.
- Translation and locking decisions.
- Templates/blocks tested.
- Style variation compatibility and accessibility results.

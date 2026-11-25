---
name: wp-block-template-development
description: Builds and reviews WordPress block-theme HTML templates and template parts using the documented template hierarchy, semantic block markup, fallbacks, representative content, and database-override awareness. Use for page-structure work.
---

# wp-block-template-development

Use this skill when adding or changing files under `templates/` or `parts/`.

## Required Inputs

- Query types and visitor journeys to support.
- Minimum WordPress version.
- Existing database-saved templates and parts.
- Required header, footer, navigation, sidebar, content, loop, pagination, search, and error behavior.
- Representative content and accessibility requirements.

## Principles

- Use `templates/index.html` as the fallback.
- Use only block markup in HTML templates and parts.
- Choose filenames from the documented block template hierarchy.
- Keep reusable structural regions in template parts.
- Use semantic `tagName` attributes where supported.
- Include Post Content where assigned content must render.
- Design explicit no-results and missing-content behavior.
- Verify which source wins before judging a file change.

## Workflow

Use [`workflows/build-block-templates-workflow.md`](workflows/build-block-templates-workflow.md).

## Resource

Use [`resources/template-hierarchy-checklist.md`](resources/template-hierarchy-checklist.md).

## Completion Evidence

Record:

- URL/query type.
- Selected template and fallback chain.
- Parts and patterns referenced.
- Active source precedence.
- Representative content cases.
- Keyboard, landmark, heading, pagination, search, and logged-out frontend checks.

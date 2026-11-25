---
name: wp-divi-5-theme-builder
description: Builds and reviews Divi 5 Theme Builder templates with narrow assignment scopes, Dynamic Content, Loop Builder, representative-content testing, fallbacks, archives, search, and 404 verification. Use for global headers, footers, posts, pages, and dynamic templates.
---

# wp-divi-5-theme-builder

Use this skill when a structure should be centrally owned and populated from WordPress content rather than copied into individual pages.

## Required Inputs

- Exact Divi 5 version.
- Content types, taxonomy, authors, custom fields, and archive requirements.
- Existing Theme Builder templates and assignment rules.
- Required global header/footer behavior.
- Representative content including long, short, missing, and unusual values.
- Query, pagination, no-results, search, and 404 expectations.

## Core Principles

- Assign templates to the narrowest correct scope.
- Review exclusions and overlaps before saving.
- Use Dynamic Content instead of hardcoded post-specific values.
- Use the Blog module for simple fixed feeds and Loop Builder when custom repeated-item structure is required.
- Keep global template structure separate from content-specific exceptions.
- Test every template while logged out with representative content.

## Workflow

Use [`workflows/build-theme-builder-template-workflow.md`](workflows/build-theme-builder-template-workflow.md).

## Resource

Use [`resources/template-assignment-checklist.md`](resources/template-assignment-checklist.md).

## Completion Evidence

Record template assignments, exclusions, dynamic fields, query rules, fallbacks, representative records tested, breakpoints checked, and logged-out URLs verified.

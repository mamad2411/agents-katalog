---
name: wp-classic-theme-templates
description: Implements and reviews WordPress classic theme PHP templates, template hierarchy choices, The Loop, conditional rendering, secondary queries, and safe output. Use when changing template files or diagnosing incorrect template selection.
license: MIT
compatibility: "General PHP-template guidance; verify project WordPress and PHP versions."
---

# WordPress Classic Theme Templates

## Use this skill when

- Adding or changing PHP template files.
- Diagnosing why WordPress selected a template.
- Implementing archives, singular views, search, 404, comments, or pagination.
- Reviewing The Loop or secondary `WP_Query` usage.
- Reducing duplicated template markup.

## Approach

1. Identify the queried page type.
2. Resolve the narrowest justified template in the hierarchy.
3. Preserve the main query.
4. Use template parts for repeated markup.
5. Escape dynamic output for context.
6. Test fallbacks, empty states, pagination, and plugin-provided content.

## Workflow

Use [template-implementation-workflow.md](workflows/template-implementation-workflow.md).

## Resources

- [php-template-hierarchy.md](resources/php-template-hierarchy.md)
- [loop-and-query-safety.md](resources/loop-and-query-safety.md)
- [safe-template-patterns.md](examples/safe-template-patterns.md)

## Guardrails

- Do not use `query_posts()`.
- Do not mutate global query variables to make a template “work.”
- Use `pre_get_posts` only with precise admin/main-query guards.
- Reset post data after custom loops.
- Do not over-specialize templates by post ID or slug without a durable requirement.

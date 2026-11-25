---
name: py-django-debug-toolbar-7-query-performance
description: Uses Django Debug Toolbar 7.x panels and debugsqlshell to investigate local SQL, cache, template, request, redirect, signal, and profiling issues.
---

# Django Debug Toolbar 7 Query and Performance Debugging

Use this skill when diagnosing local Django request overhead with Django Debug Toolbar 7.x.

## Operating rules

- Use toolbar data as local evidence, not as production monitoring.
- Keep investigations narrow to one route, view, form, template, or local reproduction at a time.
- Separate toolbar overhead from application overhead.
- Do not perform database-specific tuning beyond obvious ORM fixes unless a database plugin is active.

## Workflow

Use `workflows/query-performance-workflow.md`.

## Resource

Use `resources/panel-usage-checklist.md`.

## Example

Use `examples/debugsqlshell-example.md` for local shell-based query inspection.

## Typical fixes

- Add `select_related()` for one-to-one or foreign-key object access.
- Add `prefetch_related()` for reverse/many-to-many access.
- Move repeated expensive context work out of templates.
- Reduce excessive local-only cache/template panel overhead before changing application architecture.
- Add regression tests for query count only when stable enough to maintain.

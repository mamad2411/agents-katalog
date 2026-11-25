---
name: py-django-debug-toolbar-7-upgrade-review
description: Reviews upgrades to Django Debug Toolbar 7.x, including Django/Python compatibility, Shadow DOM changes, custom panels, themes, async limits, and deprecated settings.
---

# Django Debug Toolbar 7 Upgrade Review

Use this skill when upgrading a project from Django Debug Toolbar 6.x or earlier to 7.x.

## Operating rules

- Review the pinned version and changelog before changing dependencies.
- Treat dropping Django 4.2/5.1 support as a hard compatibility boundary.
- Treat Shadow DOM rendering as the main upgrade risk for custom themes and custom panels.
- Do not disable Shadow DOM without a concrete compatibility reason and a follow-up plan.
- Re-check local-only exposure during the upgrade.

## Workflow

Use `workflows/upgrade-to-7-workflow.md`.

## Resource

Use `resources/upgrade-compatibility-checklist.md`.

## Review areas

1. Python and Django versions.
2. Dependency pin and lockfile changes.
3. Custom toolbar panels.
4. Custom CSS/theme overrides.
5. JavaScript or DOM selectors that reach into toolbar internals.
6. Deprecated config such as `OBSERVE_REQUEST_CALLBACK`.
7. Async/ASGI behavior and unsupported Channels usage.
8. Local-only/test-only gating.
9. Browser/static asset compatibility.

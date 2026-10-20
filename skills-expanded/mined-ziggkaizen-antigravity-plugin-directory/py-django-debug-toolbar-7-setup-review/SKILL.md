---
name: py-django-debug-toolbar-7-setup-review
description: Reviews and configures Django Debug Toolbar 7.x local-development setup, settings, middleware, URLconf, test gating, and exposure safety.
---

# Django Debug Toolbar 7 Setup Review

Use this skill when installing, configuring, reviewing, or scanning Django Debug Toolbar 7.x in a Django project.

## Operating rules

- Keep the toolbar local-development only.
- Prefer minimal settings over copying default configuration wholesale.
- Verify settings, middleware, URLconf, templates, staticfiles, internal IPs, test gating, and callbacks together.
- Do not make production settings more permissive to make the toolbar visible.
- Before running included scripts, run them with `--help`.

## Workflow

Use `workflows/setup-review-workflow.md` for full setup or review.

## Resources

Use `resources/setup-checklist.md` as the primary checklist.

## Examples

Use `examples/local-settings-example.md` for a conservative local-only setup pattern.

## Scripts

- `scripts/debug-toolbar-config-scan.py`: read-only static scanner for common configuration issues.
- `scripts/debug-toolbar-command-safety.py`: Antigravity hook helper for risky command gating.

Example script usage:

```powershell
python .\.agents\plugins\py-django-debug-toolbar-7\skills\py-django-debug-toolbar-7-setup-review\scripts\debug-toolbar-config-scan.py --root . --json
```

## Review checklist

1. Confirm the project actually targets Django Debug Toolbar 7.x.
2. Confirm Python and Django compatibility.
3. Confirm `django.contrib.staticfiles` and template app directories are available.
4. Confirm `debug_toolbar` app, middleware, URLconf, and `INTERNAL_IPS` are only enabled locally.
5. Confirm tests disable toolbar setup.
6. Confirm custom callbacks use `django.conf.settings.DEBUG`, not a stale local `DEBUG` variable.
7. Confirm no production, public staging, tunnel, or shared environment path exposes the toolbar.
8. Confirm any persistent toolbar storage is justified and reviewed.
9. Run a local Django system check or scanner when possible.

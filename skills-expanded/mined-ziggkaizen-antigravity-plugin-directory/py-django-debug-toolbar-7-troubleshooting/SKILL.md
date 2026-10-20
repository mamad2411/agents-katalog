---
name: py-django-debug-toolbar-7-troubleshooting
description: Diagnoses Django Debug Toolbar 7.x visibility, static asset, middleware, Docker, CORS, HTMX, Turbo, async, and local browser issues.
---

# Django Debug Toolbar 7 Troubleshooting

Use this skill when Django Debug Toolbar is installed but not visible, broken, slow to render, or failing in local browser/devtools.

## Operating rules

- Diagnose local setup before changing application code.
- Check `DEBUG`, `INTERNAL_IPS`, response type, body tag, middleware order, static files, and browser console first.
- Do not broaden network access or production settings to fix local visibility.
- Treat async/Channels limitations as compatibility boundaries, not bugs to patch around blindly.

## Workflow

Use `workflows/toolbar-not-visible-workflow.md`.

## Resource

Use `resources/troubleshooting-checklist.md`.

## Common diagnosis order

1. Confirm local settings module and `DEBUG = True`.
2. Confirm requester IP matches `INTERNAL_IPS` or reviewed Docker callback.
3. Confirm the response is HTML/XHTML and contains `</body>`.
4. Confirm toolbar middleware order and absence of response compression before injection.
5. Check browser console for static asset MIME/CORS errors.
6. Check URLconf mounting with `debug_toolbar_urls()`.
7. Check tests are not the active runtime path.
8. Check HTMX/Turbo preservation settings if relevant.
9. Check async/ASGI limitations and unsupported Django Channels usage.

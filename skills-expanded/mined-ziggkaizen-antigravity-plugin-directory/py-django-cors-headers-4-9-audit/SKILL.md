---
name: py-django-cors-headers-4-9-audit
description: Audits django-cors-headers 4.9.x settings, middleware order, origin policy, credentials, CSRF interaction, legacy configuration, and test coverage without executing project settings.
---

# django-cors-headers 4.9 Audit

Use this skill for static security/configuration review or before upgrading and releasing a Django application that uses `django-cors-headers` 4.9.x.

## Operating rules

- Do not import or execute production settings to inspect them.
- Treat dynamic settings as unresolved when static proof is unavailable.
- Prioritize allow-all, credential, middleware-order, malformed-origin, and legacy-setting findings.
- Confirm negative tests, not just successful browser requests.
- Run scripts with `--help` before use.

## Workflow

Use `workflows/audit-cors-configuration-workflow.md` for a complete audit.

## Resource

Use `resources/security-review-checklist.md` as the evidence checklist.

## Script

`scripts/cors-settings-scan.py` performs a read-only AST scan. It never imports project modules or modifies files.

```powershell
python .\.agents\plugins\py-django-cors-headers-4-9\skills\py-django-cors-headers-4-9-audit\scripts\cors-settings-scan.py --root . --json
```

## Finding handling

- `error`: unsafe or invalid literal configuration that needs attention.
- `warning`: risky, legacy, incomplete, or ambiguous configuration.
- `info`: dynamic or contextual behavior requiring manual confirmation.

Do not auto-fix findings. Trace project intent, update settings deliberately, and add regression tests.

---
name: wp-multisite-audit
description: Audits WordPress Multisite configuration, topology, sites, access, shared code, domains, updates, backups, caches, cron, and recovery evidence. Use for readiness reviews, periodic checks, migrations, and pre-change assessments.
---

# WordPress Multisite Audit

Use this skill for a read-only network assessment before changes or as a periodic operations review.

## Static Scanner

This skill includes:

```text
scripts/audit-multisite-config.py
```

The scanner:

- reads `wp-config.php`
- optionally reads `.htaccess`
- does not load WordPress or execute PHP
- does not connect to a database or network
- does not modify files
- rejects configuration-file paths that resolve outside the selected root
- reports required Multisite constants, dynamic values, topology, rewrite signals, legacy upload settings, and selected hardening signals
- supports text and JSON output
- returns `0` for clean, `1` for warnings, and `2` for errors

Run `--help` before use.

## Workflow

Use `workflows/multisite-audit-workflow.md`.

## Resource

Use `resources/multisite-audit-checklist.md`.

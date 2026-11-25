---
name: wp-woocommerce-10-operations
description: Plans safe WooCommerce 10.x updates, HPOS operations, debugging, logging, scheduled-action review, cache handling, incidents, and rollback. Use for staging, production maintenance, failed checkout, update failures, backlog, or store outages.
---

# WooCommerce 10 Operations

Use this skill for store maintenance and incidents.

## Before any mutation

- Confirm environment and production status.
- Capture WooCommerce, WordPress, PHP, theme, and extension versions.
- Verify recent backups and restore procedure.
- Check maintenance window and business impact.
- Inspect WooCommerce Status, logs, PHP logs, scheduled actions, cron, database update state, and HPOS status.
- Prefer read-only commands first.
- Define rollback and data integrity checks.

Read:

- `resources/update-readiness-checklist.md`
- `resources/incident-triage-checklist.md`
- `workflows/update-woocommerce-workflow.md`
- `workflows/incident-triage-workflow.md`

## Command guard

The included hook calls:

```text
skills/wp-woocommerce-10-operations/scripts/woocommerce-command-guard.py
```

It only reads Antigravity hook JSON and emits `allow`, `ask`, or `deny`. It never executes commands.

Run its help and self-test manually when validating the plugin:

```powershell
python .\.agents\plugins\wp-woocommerce-10\skills\wp-woocommerce-10-operations\scripts\woocommerce-command-guard.py --help
python .\.agents\plugins\wp-woocommerce-10\skills\wp-woocommerce-10-operations\scripts\woocommerce-command-guard.py --self-test
```

## Operating principles

- Use staging before production updates.
- Treat WooCommerce database updates as explicit operations.
- Verify checkout, payment, shipping, tax, stock, account, email, webhook, REST, and scheduled-action paths after updates.
- Use current `wp wc hpos` commands and inspect status/verification before mutation.
- Do not broadly purge caches without understanding session and checkout effects.
- Keep customer/order data out of logs and chat.
- Do not rerun failed actions blindly; determine idempotency and business effect first.

## Output expected from the agent

- Current state and impact.
- Evidence and likely fault domain.
- Safest next diagnostic.
- Mutations requiring approval.
- Recovery and verification steps.

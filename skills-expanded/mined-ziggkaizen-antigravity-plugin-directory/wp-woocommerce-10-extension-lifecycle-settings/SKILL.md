---
name: wp-woocommerce-10-extension-lifecycle-settings
description: Implements and reviews WooCommerce 10 extension bootstrap, dependency checks, activation, upgrades, deactivation, uninstall, settings, admin notices, scheduled work, and logging. Use when adding lifecycle or merchant-configuration behavior.
---

# wp-woocommerce-10-extension-lifecycle-settings

Use this skill for plugin startup, versioned migrations, merchant settings, admin behavior, scheduled work, diagnostics, or uninstall policy.

## Required Inputs

- Current plugin headers, slug, text domain, namespace, and version.
- Supported WooCommerce, WordPress, and PHP versions.
- Existing options, tables, scheduled actions, roles, capabilities, and migrations.
- Configuration owners and authorized roles.
- Upgrade, downgrade, deactivation, uninstall, and retention requirements.
- Distribution target, because Marketplace-specific headers and deployment metadata differ.

## Core Requirements

- Use `Requires Plugins: woocommerce` where supported, while still failing safely when WooCommerce is unavailable.
- Do not manually add the Marketplace-managed `Woo:` header outside the official deployment flow.
- Keep activation minimal and reversible; defer expensive work.
- Make migrations versioned, restartable, observable, and safe under partial failure.
- Deactivation stops runtime behavior without silently deleting merchant data.
- Uninstall follows an explicit retain/delete policy and privacy commitments.
- Use the Settings API or documented WooCommerce settings surfaces with capability checks and validation.
- Use Action Scheduler for durable background work when appropriate.
- Use `WC_Logger` with an extension-specific source and redaction.

## Workflow

Use [`workflows/implement-extension-lifecycle-workflow.md`](workflows/implement-extension-lifecycle-workflow.md).

## Resource

Use [`resources/lifecycle-settings-checklist.md`](resources/lifecycle-settings-checklist.md).

## Completion Evidence

Record headers, dependency behavior, lifecycle handlers, migration ledger, settings schema, authorization, scheduled-action behavior, log policy, uninstall decision, tests, and rollback procedure.

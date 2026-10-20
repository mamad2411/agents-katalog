---
name: wp-woocommerce-10-extension-testing-release
description: Builds and executes a WooCommerce 10 extension test, compatibility, packaging, interoperability, upgrade, uninstall, and release plan. Use before a pull request, Marketplace or WordPress.org submission, or production release.
---

# wp-woocommerce-10-extension-testing-release

Use this skill to validate a new extension, repair tests, review a release candidate, or assess compatibility after WooCommerce changes.

## Required Inputs

- Exact supported and tested version matrix.
- Extension source, generated assets, manifests, lockfiles, tests, and package process.
- Declared HPOS, Cart/Checkout Blocks, REST, Store API, or other feature compatibility.
- Critical merchant/customer flows and transaction-sensitive paths.
- Existing upgrade, migration, uninstall, rollback, and telemetry behavior.
- Distribution-channel requirements.

## Required Test Layers

- Pure unit tests for domain decisions and data mapping.
- WordPress/WooCommerce integration tests for hooks, CRUD, settings, migrations, and permissions.
- JavaScript tests for UI and state logic.
- End-to-end tests for critical merchant and customer flows.
- HPOS and legacy-order-storage coverage where declared.
- Blocks and classic checkout/cart coverage where supported.
- Negative security, duplicate/retry, timeout, and partial-failure coverage.
- Upgrade, downgrade boundary, deactivation, uninstall, reinstall, and rollback tests.
- Static analysis, PHPCS/WPCS, build, package, license, translation, and clean-install review.
- QIT and representative interoperability tests where relevant.

## Workflow

Use [`workflows/validate-extension-release-workflow.md`](workflows/validate-extension-release-workflow.md).

## Resource

Use [`resources/extension-test-release-matrix.md`](resources/extension-test-release-matrix.md).

## Script

Run the read-only auditor with `--help` first:

```powershell
python .agents/plugins/wp-woocommerce-10-extension-development/skills/wp-woocommerce-10-extension-testing-release/scripts/audit-woocommerce-extension.py --help
```

The auditor finds structural and static-review candidates. It does not prove runtime, security, HPOS, Blocks, or Marketplace compatibility.

## Completion Evidence

Record commands, environments, results, package hash, known limitations, compatibility evidence, rollback procedure, and release decision.

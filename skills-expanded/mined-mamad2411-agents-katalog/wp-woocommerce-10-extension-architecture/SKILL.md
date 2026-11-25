---
name: wp-woocommerce-10-extension-architecture
description: Plans a WooCommerce 10 extension's WordPress bootstrap, WooCommerce dependency boundary, namespaces, services, data ownership, Blocks or Store API integration, build output, tests, compatibility, and package contents. Use before creating or substantially restructuring an extension.
---

# wp-woocommerce-10-extension-architecture

Use this skill before implementation when the extension purpose, runtime boundary, data ownership, integration surface, or package structure is not explicit.

## Required Inputs

- One-sentence extension purpose and merchant/customer outcomes.
- Exact WooCommerce, WordPress, PHP, database, Node.js, package-manager, and browser targets.
- Distribution channel and update mechanism.
- Existing plugin scaffold and manifests, when present.
- Data owned, read, changed, transmitted, retained, or deleted.
- Required admin, storefront, REST, Store API, Blocks, webhook, and scheduled-work surfaces.
- HPOS and classic/Blocks compatibility requirements.
- Security, privacy, accessibility, performance, and licensing constraints.

## Decisions to Make

- Main plugin file, headers, dependency check, and delayed WooCommerce-aware initialization.
- Namespace/prefix, autoloading, service boundaries, and hook registration.
- Domain logic versus WordPress/WooCommerce adapters and presentation.
- Extension-owned options, tables, metadata, scheduled actions, and migrations.
- Public API and feature-compatibility boundaries.
- JavaScript source, PHP source, generated assets, translations, tests, and package allowlist.
- Observability, retries, idempotency, failure behavior, rollback, and uninstall policy.
- Version matrix and deprecation policy.

## Workflow

Use [`workflows/plan-woocommerce-extension-workflow.md`](workflows/plan-woocommerce-extension-workflow.md).

## Resource

Use [`resources/extension-architecture-map.md`](resources/extension-architecture-map.md).

## Example

Use [`examples/bootstrap-contract-outline.md`](examples/bootstrap-contract-outline.md) as a review outline, not copy-paste production code.

## Completion Evidence

Record the chosen architecture, all runtime entry points, data ownership, public API dependencies, compatibility matrix, test layers, package contents, update path, and rollback criteria.

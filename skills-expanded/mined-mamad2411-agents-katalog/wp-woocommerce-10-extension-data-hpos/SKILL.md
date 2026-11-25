---
name: wp-woocommerce-10-extension-data-hpos
description: Designs and reviews WooCommerce 10 data access, order and product mutations, extension-owned storage, migrations, idempotency, Action Scheduler work, and HPOS compatibility. Use whenever an extension reads or changes commerce data.
---

# wp-woocommerce-10-extension-data-hpos

Use this skill whenever work touches orders, products, customers, coupons, stock, taxes, shipping, payments, webhooks, imports, exports, scheduled actions, or extension-owned persistence.

## Required Inputs

- Exact WooCommerce version and enabled features.
- HPOS status and declared compatibility.
- Data objects, identifiers, ownership, volume, retention, and sensitivity.
- Existing direct SQL, post/meta calls, data stores, hooks, caches, and scheduled actions.
- Required consistency, idempotency, retry, and rollback behavior.

## Core Requirements

- Use WooCommerce CRUD objects, factories, query APIs, and data stores for WooCommerce-owned data.
- Treat order identifiers and order storage as abstract contracts.
- Save through the object API after validating a complete state transition.
- Keep extension-owned tables or options explicitly versioned and migrated.
- Make webhooks, payments, fulfillment, syncs, imports, and scheduled work idempotent.
- Use Action Scheduler with bounded payloads, retries, observability, and failure recovery.
- Test HPOS enabled and disabled when the support declaration covers both.
- Do not declare compatibility based only on static scanning.

## Workflow

Use [`workflows/validate-hpos-compatibility-workflow.md`](workflows/validate-hpos-compatibility-workflow.md).

## Resource

Use [`resources/hpos-data-access-matrix.md`](resources/hpos-data-access-matrix.md).

## Example

Use [`examples/hpos-compatibility-declaration.md`](examples/hpos-compatibility-declaration.md) as a declaration pattern after tests pass.

## Completion Evidence

Record every data path, API choice, mutation invariant, idempotency mechanism, migration, compatibility test, declaration, rollback trigger, and unresolved storage dependency.

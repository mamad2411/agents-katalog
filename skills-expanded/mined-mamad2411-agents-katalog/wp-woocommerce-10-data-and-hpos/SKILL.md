---
name: wp-woocommerce-10-data-and-hpos
description: Reviews WooCommerce 10.x product and order data access for CRUD, query API, and HPOS compatibility. Use when code reads or writes products, orders, metadata, custom tables, reports, migrations, or bulk data.
---

# WooCommerce 10 Data and HPOS

Use this skill before changing order or product data access.

## Required approach

1. Confirm the installed WooCommerce version.
2. Determine HPOS state, compatibility mode, pending synchronization, and authoritative datastore.
3. Inventory every read, write, query, migration, report, export, and cleanup path.
4. Replace WordPress post assumptions with WooCommerce objects and query APIs.
5. Test under every datastore configuration the project claims to support.
6. Treat data repair and cleanup as production changes requiring backup and approval.

Read:

- `resources/hpos-compatibility-checklist.md`
- `resources/data-access-patterns.md`
- `workflows/review-hpos-data-access-workflow.md`

## Scanner

Run the read-only PHP scanner with `--help` first:

```powershell
python .\.agents\plugins\wp-woocommerce-10\skills\wp-woocommerce-10-data-and-hpos\scripts\scan-woocommerce-php.py --help
```

Example:

```powershell
python .\.agents\plugins\wp-woocommerce-10\skills\wp-woocommerce-10-data-and-hpos\scripts\scan-woocommerce-php.py --root . --json
```

The scanner does not load WordPress, connect to a database, execute PHP, or modify files. Findings are evidence prompts, not proof of a bug.

## Review focus

- `WP_Query` or `get_posts()` for `shop_order`.
- Direct order post/meta access.
- Direct SQL against order or lookup tables.
- Product queries that bypass `wc_get_products()`.
- Hard-coded WC REST API credentials.
- Sensitive logger context.
- Writes to HPOS options.
- Deprecated `wp wc cot` command strings.

## Output expected from the agent

- HPOS state assumptions.
- Unsafe or version-coupled data paths.
- Supported replacement APIs.
- Migration and synchronization risks.
- Required tests and rollback.

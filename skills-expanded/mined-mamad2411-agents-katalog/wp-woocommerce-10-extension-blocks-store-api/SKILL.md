---
name: wp-woocommerce-10-extension-blocks-store-api
description: Implements and reviews WooCommerce 10 Cart and Checkout Blocks extensibility, Store API data, frontend state, payment or shipping integrations, and classic-versus-Blocks compatibility. Use for block-based cart, checkout, mini-cart, product collection, or Store API work.
---

# wp-woocommerce-10-extension-blocks-store-api

Use this skill when an extension adds block controls, checkout fields, payment or shipping behavior, Store API schema/data, frontend filters, or interactive cart/checkout UI.

## Required Inputs

- Exact WooCommerce and WordPress versions.
- Supported Cart/Checkout Blocks and classic shortcode paths.
- Block names, extension points, package versions, and build configuration.
- Store API data to read or extend.
- Authentication, customer/session, caching, privacy, and failure requirements.
- Existing PHP hooks and JavaScript registrations.

## Core Requirements

- Distinguish the public storefront Store API from the authenticated WooCommerce REST API.
- Use documented Blocks and Store API extension points for the target WooCommerce release.
- Keep privileged data and secrets out of Store API responses and browser state.
- Validate and sanitize extension data on the server; treat client validation as usability only.
- Preserve cart/checkout idempotency and avoid duplicate totals, charges, stock changes, or order creation.
- Define whether classic shortcode compatibility is supported, degraded, or intentionally unavailable.
- Keep editor, frontend, logged-in, guest, empty, loading, error, retry, and stale-cart states accessible and coherent.
- Build and load assets only where needed.

## Workflow

Use [`workflows/integrate-blocks-store-api-workflow.md`](workflows/integrate-blocks-store-api-workflow.md).

## Resource

Use [`resources/blocks-store-api-checklist.md`](resources/blocks-store-api-checklist.md).

## Completion Evidence

Record extension points, API schema, permission/data classification, client/server validation, state transitions, classic fallback, tests, package versions, and release-note sources.

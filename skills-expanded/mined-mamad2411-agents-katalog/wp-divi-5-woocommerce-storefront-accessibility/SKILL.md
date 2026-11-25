---
name: wp-divi-5-woocommerce-storefront-accessibility
description: Reviews Divi 5 WooCommerce product, catalog, cart, and checkout journeys for semantics, labels, keyboard operation, focus, errors, notices, contrast, touch targets, responsive order, motion, and third-party payment UI boundaries.
---

# wp-divi-5-woocommerce-storefront-accessibility

Use this skill for launch review, remediation, or regression testing of the shopper journey.

## Required Inputs

- Critical product-to-order journeys.
- Enabled product types, gateways, shipping methods, coupons, and account modes.
- Relevant Divi breakpoints and sticky or reordered layouts.
- Existing accessibility requirements and known exceptions.
- Representative validation and payment failure paths.
- At least one physical touch-device plan for critical interactions.

## Core Principles

- Test function and recovery, not only appearance.
- Preserve labels, instructions, reading order, keyboard order, and focus.
- Make notices and errors perceivable and actionable.
- Include selected, disabled, sale, error, and out-of-stock states.
- Treat gateway-hosted fields and iframes as separate accessibility surfaces.
- Verify logged-out frontend output.

## Workflow

Use [`workflows/review-divi-woocommerce-accessibility-workflow.md`](workflows/review-divi-woocommerce-accessibility-workflow.md).

## Resource

Use [`resources/commerce-accessibility-checklist.md`](resources/commerce-accessibility-checklist.md).

## Completion Evidence

Record tested journeys, devices, breakpoints, keyboard paths, focus results, errors, notices, contrast states, touch behavior, motion behavior, gateway boundaries, defects, severity, and retest evidence.

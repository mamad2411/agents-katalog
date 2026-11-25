---
name: app-release-readiness
description: "Create and execute an evidence-based Shopify app release checklist covering security, privacy, billing, UX, tests, hosting, migrations, review assets and post-launch support. Deployment and submission require explicit authorization."
---

# Know what is ready before you ship

A passing build is not a production release. Shopify review and Built for Shopify designation are separate external decisions.

## Start here

Inspect the app type/distribution, intended release target, current docs and actual feature set. Explain "ready", "blocked" and "not tested"; don't invent a numerical readiness score. Do not make optional B2B, Functions, Hydrogen, paid ads or paid billing mandatory for every app.

## Release gates

1. Core feature: install, first-value task, saved state, error recovery, uninstall/reinstall and relevant extensions on an authorized dev store.
2. Security: [app-auth](../app-auth/SKILL.md), minimal scopes, shop isolation, validated inputs, injection/XSS/CSRF protections appropriate to framework, abuse/rate limits, secrets and dependency audit, redacted logging.
3. Events and privacy: [webhooks](../webhooks/SKILL.md), duplicate/out-of-order handling, durable processing, uninstall and applicable compliance requests, protected-data approval, data minimization and documented retention/deletion. A 200 response alone is not cleanup.
4. Commerce: [app-billing](../app-billing/SKILL.md) if paid, test-mode decline/cancel/trial/entitlements, disclosed limits and no unauthorized real charge.
5. Usability: [app-accessibility](../app-accessibility/SKILL.md), [ux-onboarding](../ux-onboarding/SKILL.md), [ux-empty-error-states](../ux-empty-error-states/SKILL.md), mobile/keyboard and long-text testing.
6. Reliability: [app-performance](../app-performance/SKILL.md), primary-path regression tests, queues/retries, observed error handling and tenant-safe caching.
7. Operations: app server/database hosting separate from Shopify config/extensions, HTTPS and URLs, secret-store configuration confirmed without revealing values, migration backup/recovery, health checks, rollback, error alerts and support runbook.
8. Review: current App Store requirements, product evidence, accurate screenshots, privacy/terms/support URLs, distribution and protected-data eligibility. Use [app-listing-optimization](../app-listing-optimization/SKILL.md); [built-for-shopify-standards](../built-for-shopify-standards/SKILL.md) is an optional additional program review.

## Execute safely

Present release target, changes, costs and recovery path. Obtain explicit approval for deployment, production migrations, scope changes, charges and submissions. Use the project's existing release process; preserve unrelated changes and never perform irreversible cleanup silently.
After deployment verify actual server health, correct configuration version, authorized install and core task. Keep source/build, deployment, store QA and marketplace acceptance separate.

## Deliver a beginner-readable handoff

Use a compact gate list with observed evidence, blocker and next action. Include only redacted diagnostics. Provide a short support/maintenance plan: monitor errors, test API upgrades before cutover, rehearse data recovery, maintain policies, and respond to merchant feedback.
If account access prevents a test, mark it unverified and explain the exact manual check. Never award approval or call untested gates passed.

Sources: [Shopify app review](https://shopify.dev/docs/apps/launch/app-store-review), [protected data](https://shopify.dev/docs/apps/launch/protected-customer-data), [privacy compliance](https://shopify.dev/docs/apps/build/compliance/privacy-law-compliance).

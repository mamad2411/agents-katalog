---
name: wp-divi-5-child-theme-upgrade-testing
description: Tests Divi parent-theme updates against a child theme. Use when reviewing template drift, PHP compatibility, assets, Theme Builder interactions, critical frontend views, and rollback readiness before rollout.
---

# Divi 5 Child-Theme Upgrade Testing

## Principle

A child theme protects local files from overwrite; it does not guarantee compatibility with changed parent templates, hooks, CSS, JavaScript, PHP requirements, or builder behavior.

## Preconditions

- Recoverable backup and rollback procedure.
- Staging environment representative of production.
- Exact current and target Divi versions.
- Current WordPress, PHP, database, cache, and relevant extension versions.
- Complete template override register.
- Representative content and critical user journeys.

## Method

1. Capture the current baseline and run smoke tests before updating.
2. Run the read-only inspector with current child and parent paths.
3. Compare every registered child override with the target parent file.
4. Review Divi release notes between current and target versions.
5. Update in staging and clear only the caches required by the test plan.
6. Check PHP errors/deprecations, browser console, network failures, CSS generation, and asset duplication.
7. Test WordPress admin, Visual Builder, Theme Builder, and logged-out frontend.
8. Test critical templates, responsive widths, forms, navigation, search, 404, archives, and third-party integrations as applicable.
9. Roll back in staging once to verify the documented procedure.
10. Record evidence, blockers, residual risks, and production rollout decision.

Use [parent-update-test-matrix.md](resources/parent-update-test-matrix.md) and [test-divi-parent-update-workflow.md](workflows/test-divi-parent-update-workflow.md).

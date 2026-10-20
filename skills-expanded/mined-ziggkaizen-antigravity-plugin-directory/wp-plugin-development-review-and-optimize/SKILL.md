---
name: wp-plugin-development-review-and-optimize
description: Reviews WordPress plugin changes for correctness, lifecycle, security, compatibility, maintainability, performance, accessibility, privacy, observability, and regressions. Use for PR or plugin review and measured optimization.
---

# WordPress Plugin Review and Optimization

Use this skill after requirements are known and before release or merge.

## Inputs to collect

- Issue/requirements and explicit non-goals.
- Diff plus surrounding bootstrap, lifecycle, storage, authorization, and tests.
- Compatibility and distribution contract.
- Existing public hooks, routes, options, schema, files, and extension points.
- Performance evidence, production symptoms, and observability constraints when optimization is requested.

## Method

1. Establish scope and changed contracts before reading implementation details.
2. Use the [code review rubric](resources/code-review-rubric.md) in risk order: data loss/security, correctness, compatibility, lifecycle, tests, then maintainability and style.
3. Trace every changed entry point from registration through authorization, input, side effect, output, and failure behavior.
4. Trace stored data through install, upgrade, normal use, deactivation, uninstall, export, and erasure.
5. Compare tests with claimed WordPress/PHP and dependency support.
6. Apply the [performance and observability checklist](resources/performance-and-observability-checklist.md) only with a concrete request path or measured concern.
7. Distinguish blocking findings, actionable medium findings, suggestions, false positives, and out-of-scope follow-ups.
8. Run the [plugin code review workflow](workflows/plugin-code-review-workflow.md).

## Review rules

- Prioritize user impact and exploitability over formatting preferences.
- Review the built artifact when generated/runtime files differ from source.
- Do not approve a migration because it works only on a clean install.
- Do not approve an authorization check without a negative test or direct evidence.
- Do not call a query slow without query count/timing/cardinality evidence.
- Do not trade correctness for cache behavior; caches must remain disposable.
- Do not broaden the change with unrelated refactoring.
- Explain false positives with exact path and control-flow evidence.

## Required output

For each finding provide:

- severity
- path and relevant symbol/line
- expected contract
- observed behavior
- user/security/operational impact
- focused correction
- verification step

End with:

- blocking status
- changed public/data contracts
- test and compatibility gaps
- performance evidence
- residual risk and follow-up issues

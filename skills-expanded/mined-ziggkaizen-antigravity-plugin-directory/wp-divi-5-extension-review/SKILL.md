---
name: wp-divi-5-extension-review
description: Reviews a Divi 5 extension for architecture, compatibility, WordPress security, module metadata, editor/frontend parity, accessibility, performance, tests, conversion, build output, and package safety. Use for pull requests, release candidates, or update readiness.
---

# wp-divi-5-extension-review

Use this skill for evidence-based code review. Rank findings by exploitability, content-loss risk, runtime breakage, editor deception, compatibility, and maintainability.

## Required Inputs

- Diff or release candidate.
- Exact Divi and toolchain versions.
- Extension architecture and module inventory.
- Build and test commands.
- Supported version matrix.
- Package artifact when release readiness is in scope.
- Existing review findings and intended behavior.

## Review Order

1. Critical security, authorization, data exposure, destructive behavior, and content-loss risks.
2. Activation, module registration, metadata, build, and package failures.
3. Visual Builder/frontend divergence.
4. Dynamic data, parent/child, conversion, responsive, and failure-state correctness.
5. Accessibility and performance.
6. Tests, compatibility evidence, documentation, and maintainability.

## Workflow

Use [`workflows/review-divi-extension-workflow.md`](workflows/review-divi-extension-workflow.md).

## Resource

Use [`resources/extension-review-checklist.md`](resources/extension-review-checklist.md).

## Finding Format

For every finding, provide:

- Priority: critical, high, medium, or low.
- Path and line or symbol.
- Concrete failure scenario.
- Why it matters.
- Minimal safe correction.
- Validation needed after the correction.
- Whether the finding blocks release.

## Completion Evidence

Record reviewed commit, versions, files, commands, findings, resolved false positives, test status, package status, unresolved risks, and release recommendation.

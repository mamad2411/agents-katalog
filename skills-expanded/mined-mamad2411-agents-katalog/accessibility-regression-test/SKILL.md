---
name: accessibility-regression-test
description: "Turn a verified accessibility repair into a focused behavior regression test or manual review record. Use for accessibility-specific component, browser, axe, or keyboard regression work; not generic test setup or whole-page certification."
license: MIT
metadata:
  version: "1.0"
---

# Accessibility regression test

Protect the user-facing behavior that failed, after the repair has been verified
in the original state.

## Workflow

1. Read the before evidence and verified after evidence. State the barrier in
   terms of user behavior.
2. Choose the narrowest reliable layer with
   [references/test-selection.md](references/test-selection.md).
3. Make the test fail against the known broken behavior when practical, then
   pass with the repair.
4. Assert outcomes such as focus destination, exposed error, accessible name, or
   absence of the original fingerprint. Do not assert only that an attribute
   string exists.
5. Control route, state, viewport, reduced motion, and data so the test is
   repeatable.
6. Keep manual-only outcomes as an explicit review record rather than a
   misleading automated test.

## Boundaries

Do not snapshot raw axe output, browser versions, run IDs, or timestamps. Do not
weaken a rule, baseline away a new issue, hide content, or remove functionality
to make a test pass. A regression test protects its scoped behavior; it does not
certify the component or page.

## Local integration

Use only tooling already available for the task or dependencies justified by
the requested implementation. Follow browser-tool access rules. Keep source
review, synthetic/component tests, browser observation, and assistive-technology
validation distinct; do not claim unperformed checks. Preserve project scope
and existing authorization for external actions.

---
name: wp-divi-5-rendering-conflict-diagnostics
description: Diagnoses Divi 5 frontend and Visual Builder differences, blank or partial pages, Theme Builder overrides, custom CSS or HTML defects, Safe Mode results, and third-party plugin conflicts using reversible evidence-first tests.
---

# Divi 5 Rendering and Conflict Diagnostics

Use this skill when the live page is stale, broken, blank, partial, or different from the Visual Builder.

## Diagnostic Order

1. Reproduce while logged out and capture evidence.
2. Compare private window, `?nocache=1`, Visual Builder, and live frontend.
3. Determine whether the page is blank/partial or only styled differently.
4. For blank/partial pages, inspect Theme Builder assignments, Custom Body visibility, and Post Content placement.
5. Clear the Divi CSS cache and recheck.
6. Clear other cache layers one at a time.
7. Back up and test custom CSS and custom HTML in small units.
8. Enable Divi Safe Mode for the current user.
9. If Safe Mode resolves the issue, isolate plugins, child theme, and custom code one component at a time.
10. Record causal evidence or prepare a support record.

## Guardrails

- Capture evidence before mutation.
- Do not globally deactivate plugins on production before Safe Mode when Safe Mode can reproduce the issue.
- Do not remove custom CSS or HTML without a recoverable copy.
- Do not assume a cache clear proves root cause unless the symptom can be reproduced and cleared consistently.
- Do not edit Theme Builder assignments until the current assignment map is recorded.

## Workflow

Use [diagnose-divi-rendering-conflict-workflow.md](workflows/diagnose-divi-rendering-conflict-workflow.md).

## Resources

- [rendering-diagnostic-matrix.md](resources/rendering-diagnostic-matrix.md)
- [support-evidence-record-example.md](examples/support-evidence-record-example.md)

## Output

Return:

- Symptom classification.
- Reproduction steps.
- Evidence captured.
- Tests and results in order.
- Most likely cause and confidence.
- Reversible fix or next safe test.
- Support evidence when escalation is needed.

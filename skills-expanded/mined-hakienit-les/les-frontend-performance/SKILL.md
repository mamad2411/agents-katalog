---
name: les-frontend-performance
description: Measure and review frontend performance risks affecting rendering, loading, media, layout stability, or critical user journeys.
invocation: model
maturity: stable
route: frontend-performance
profile: frontend
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/verification.md","../../profiles/frontend/rules/performance.md","../../profiles/frontend/rules/interaction-responsive.md","../../profiles/frontend/rules/browser-evidence.md","../../profiles/frontend/rules/frontend-verification.md"]
---

# Frontend Performance

## Invoke

Bootstrap LES and require the frontend profile when a UI change may affect loading,
rendering, responsiveness, media, or layout stability.

## Inputs

Critical journey, baseline measurement, changed surface, supported devices or
viewports, network assumptions, and available profiling evidence.

## Procedure

1. Establish or locate a reproducible baseline and identify the frontend stack. Done when: one measurement or explicit unavailable constraint, journey, viewport, and stack are recorded.
2. Trace shipped code, renders, blocking work, media, async boundaries, and layout changes. Done when: the likely cost owner is identified and framework-specific guidance is applied only when the stack matches.
3. Check progressive loading, reserved space, responsive cost, and critical interaction feedback. Done when: each applicable risk has evidence.
4. Report measured impact and smallest safe action. Done when: optimization is justified or explicitly deferred with a trigger.

## Output

Performance record with baseline, measurement, affected journey, findings, residual
risk, and next safe action.

## Guardrails

Measure before optimizing. Do not introduce caching, virtualization, dependencies,
or architecture changes without evidence that the acceptance requires them.

## Verification

Keep performance, visual, keyboard, and browser evidence separate. A clean static
check does not prove runtime performance; an unavailable measurement stays explicit.

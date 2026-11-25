---
name: wcag-build
description: "Implement accessible UI and remediate WCAG 2.2 (default) or 2.1 criteria: forms, authentication, focus, pointer targets, gestures, media, semantic components, responsive behavior and assistive technology."
---

# Build and remediate accessible UI with versioned requirements

## Scope

Resolve the target version and level using `../wcag-diagnose/references/standard-selection.md` before coding. **Default WCAG 2.2 AA**, unless explicit user/contract/project policy differs. W3C normative source controls; consult the selected `2.2/criteria.json` or `2.1/criteria.json`, remediation recipes and matching specialist playbooks.

## Procedure

1. Start with the user task and real component states. Choose the applicable SC set; do not silently import 2.2 criteria into an explicit 2.1 project.
2. Prefer accessible semantic HTML and tested built-in controls. Implement keyboard, mouse, touch, screen-reader information, responsive reflow, forms, loading, errors and recovery—not static appearances only.
3. Under WCAG 2.2 AA, consider **focus obscuration (2.4.11)** with sticky UI; **non-drag alternatives (2.5.7)**; **24 CSS-px target size or valid exceptions (2.5.8)**; **help placement consistency (3.2.6)**; **redundant form entry (3.3.7)**; and **accessible authentication (3.3.8)**. For AAA check enhanced variants (2.4.12, 2.4.13, 3.3.9).
4. Consult `references/implementation-contracts.md` plus focused specialist playbooks. Cover every required state and avoid adding ARIA as a substitute for correct interaction.
5. Run focused unit/component tests, then browser interaction/AT checks for behavior that cannot be inferred statically. Do not weaken automated rules to obtain a green scan.
6. Report exact selected SC, implemented change, tests and any manual gap. A valid design/implementation decision is **not** a conformance certificate. Optional WCAG 3.0 draft exploration is an advisory design backlog, never a requirement or release gate.

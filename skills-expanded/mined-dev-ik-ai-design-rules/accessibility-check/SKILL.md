---
name: accessibility-check
description: Use when implemented interactive UI needs practical checks of keyboard navigation, visible focus, accessible names, form labels and errors, dialog focus, touch targets, color-only status, or reduced motion. Skip legal certification and backend-only work.
---

# Accessibility Check

Exercise the user's flow and inspect semantics as well as pixels. This execution skill complements `accessibility-reviewer`; it is not a conformance certificate.

Retrieve matching graph context and read applicable research, particularly `A11Y-001` through `A11Y-004`. Record the actual browser, viewport, data, states, and tools. If only source or a screenshot is available, identify that limited scope and mark behavioral checks unverified.

## Check the implemented flow

- Inspect semantic elements and accessible names. Buttons perform actions; links navigate. Inputs have associated labels. Icon-only controls have meaningful names or decorative icons are hidden. Prefer native elements; inspect existing custom controls without adding unnecessary ARIA.
- Use keyboard input to follow the primary journey. Check Tab and Shift+Tab order, visible focus, Enter/Space where relevant, and access to actions that also work with a pointer. For dialogs and sheets, observe initial focus, containment when modal, Escape behavior where supported, and focus restoration after closing. A role locator alone does not establish keyboard behavior.
- Trigger input errors and recovery. Observe specific textual messages, association with the affected input, retained values, and retry. Check applicable loading, success, and disabled states for understandable feedback and remaining navigation.
- Measure clickable target bounds, not just visible icons, when applying the graph's `A11Y-001`. Inspect responsive collision risks with `responsive-check`.
- Inspect focus and status in screenshots. For contrast, use actual foreground/background values and a suitable measurement tool; a visual impression cannot prove a numeric contrast ratio. State the applicable criterion and report unknown composite/translucent colors as unresolved. Status must remain understandable without color alone.
- When interaction motion exists, exercise the available reduced-motion preference and confirm equivalent function and feedback. Record any assistive-technology testing actually performed; browser DOM/role inspection does not prove screen-reader behavior.

For authorized fixes, preserve business logic, use the existing component system, and repeat the failed keyboard/error/state interaction. Capture focused evidence before and after where visible behavior is involved.

## Output

Return **scoped verdict | tools and conditions | confirmed findings | coverage gaps**. A finding includes severity, affected control/state, keyboard or pointer reproduction, measured/observed evidence, user impact, applicable graph rule or external criterion, fix, verified component/file, and retest status. Distinguish **checked**, **unverified**, and **not applicable** for labels/semantics, keyboard/focus, dialogs, errors/recovery, targets, contrast, reduced motion, and assistive technology. Missing evidence is not a pass or a confirmed implementation defect.

Sources: `CHECK-00001`, `RULE-00009` through `RULE-00013`, `research/accessibility/textual-error-recovery.md`, and `research/accessibility/keyboard-focus-and-interaction-motion.md`. [Playwright role and label locators](https://playwright.dev/docs/locators) provide useful semantic feedback but do not replace accessibility audits.

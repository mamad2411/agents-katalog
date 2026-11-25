---
name: kendo-ui-accessibility
description: Use when implementing or auditing Kendo UI component accessibility including WCAG 2.1 AA compliance, ARIA roles, keyboard navigation, focus management, and screen reader compatibility per component.
---

# Kendo UI Accessibility

## Specialization

Implement and audit accessibility for Kendo UI components covering WCAG 2.1 AA success criteria, WAI-ARIA role contracts, keyboard interaction patterns, focus management, color contrast compliance, and screen reader compatibility — grounded in official Kendo UI accessibility documentation and WAI-ARIA Authoring Practices.

## Trigger Conditions

- Auditing a Kendo UI implementation for WCAG 2.1 AA compliance.
- Implementing keyboard navigation across Kendo UI Grid, Scheduler, TreeView, DropDownList, DatePicker, or Editor.
- Verifying ARIA roles, states, and properties emitted by Kendo UI components.
- Diagnosing focus management failures: focus lost after Dialog close, focus not trapped in modal Window.
- Reviewing color contrast ratios for text inside Kendo UI themed components.
- Implementing accessible error messaging in Kendo UI form widgets.
- A mobile or desktop accessibility audit identifies Kendo UI components as failing.
- Preparing a Voluntary Product Accessibility Template (VPAT) for a Kendo UI-powered application.

## Scope Boundaries

In scope:

- WCAG 2.1 AA success criteria applicable to Kendo UI components (1.3.1, 1.4.1, 1.4.3, 1.4.4, 2.1.1, 2.1.2, 2.4.3, 2.4.7, 3.3.1, 3.3.2, 4.1.2, 4.1.3).
- WAI-ARIA role, state, and property contracts per Kendo UI component.
- Keyboard interaction: focus traversal, navigation keys, activation keys per component type.
- Focus management: modal focus trap, focus restore on dismiss, skip navigation patterns.
- Screen reader compatibility: JAWS, NVDA, VoiceOver — known limitations per component.
- Color contrast: verification strategy for Kendo UI themed text and interactive elements.
- Accessible name assignment: `aria-label`, `aria-labelledby`, `aria-describedby` placement per widget.

Out of scope:

- Full WCAG 2.1 AAA compliance (AAA criteria are advisory only in this skill).
- Non-Kendo UI page-level accessibility (use `web-ux-accessibility` for full page audits).
- Mobile-native accessibility (see `capacitor-accessibility` or `mobile-accessibility-quality-gate`).
- SASS theming changes to color tokens (see `kendo-ui-theming`).

## Inputs

- List of Kendo UI components in scope for the audit or implementation.
- Kendo UI version in use.
- Assistive technology targets (JAWS, NVDA, VoiceOver, TalkBack).
- Existing ARIA attribute overrides or custom widget implementations.
- WCAG conformance target: AA (required) or AAA (advisory).

## Required Outputs

- Component-by-component ARIA role and state inventory.
- Keyboard interaction verification matrix (component, key, expected outcome, actual outcome).
- Focus management assessment: modal traps, restore paths, tab order correctness.
- Color contrast ratio findings for text, borders, and focus indicators.
- Screen reader compatibility notes per component and AT combination.
- Remediation list with severity (Blocker, Major, Minor) and WCAG success criterion reference.
- VPAT-ready finding table if requested.

## Component Accessibility Contracts

### Grid

| Aspect | Contract |
|---|---|
| Role | `grid` on the table element |
| Rows | `role="row"` on each `<tr>` |
| Cells | `role="gridcell"` on data cells, `role="columnheader"` on header cells |
| Sorting | `aria-sort="ascending|descending|none"` on active sort column |
| Selection | `aria-selected="true"` on selected rows |
| Navigation | Arrow keys navigate cells; Enter activates edit mode; Escape cancels edit |
| Focus indicator | Visible focus ring on focused cell — verify contrast ≥ 3:1 against background |

### Dialog and Window (Modal)

| Aspect | Contract |
|---|---|
| Role | `role="dialog"` with `aria-modal="true"` |
| Accessible name | `aria-labelledby` pointing to the Dialog title element |
| Focus trap | Tab and Shift+Tab must cycle within the open Dialog |
| Focus restore | On close, focus must return to the element that opened the Dialog |
| Escape key | Must close the Dialog |

### DropDownList and ComboBox

| Aspect | Contract |
|---|---|
| Role | `combobox` on the input; `listbox` on the dropdown popup |
| State | `aria-expanded="true|false"` on the combobox |
| Option selection | `aria-selected="true"` on the active option |
| Navigation | Arrow keys navigate options; Enter selects; Escape closes |

### DatePicker

| Aspect | Contract |
|---|---|
| Input role | Standard `<input type="text">` with `aria-label` or visible `<label>` |
| Calendar popup | `role="dialog"` with `aria-label="Calendar"` |
| Day cells | `role="gridcell"` with `aria-label` including full date |
| Today / selected | `aria-current="date"` on today; `aria-selected="true"` on selected date |

## Color Contrast Requirements

| Element | WCAG Criterion | Minimum Ratio |
|---|---|---|
| Normal text (< 18pt) | 1.4.3 AA | 4.5:1 |
| Large text (≥ 18pt or 14pt bold) | 1.4.3 AA | 3:1 |
| UI component boundaries (input border) | 1.4.11 AA | 3:1 |
| Focus indicator | 1.4.11 AA | 3:1 |

## Known Kendo UI Accessibility Limitations

- Grid virtual scrolling: may cause ARIA live region announcement gaps. Use non-virtual scrolling for screen reader-critical grids.
- Editor (rich text): contenteditable ARIA support varies by AT. Provide a plain-text fallback or accessible description.
- Chart: charts are not fully accessible via keyboard alone — always provide a tabular data alternative.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Verify ARIA roles on one component | Role, state, and keyboard contract documented for target component |
| L2 Practical | Full keyboard and ARIA audit for a page with multiple Kendo UI widgets | All components pass keyboard matrix; no missing ARIA labels |
| L3 Hardening | AT compatibility testing with JAWS/NVDA and remediation | Screen reader test results documented; blockers resolved |
| L4 Expert | VPAT-ready audit across full Kendo UI application | VPAT table complete; all AA blockers resolved; known limitations documented |

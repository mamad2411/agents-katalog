---
name: ui-accessibility
description: "Inspect semantics, keyboard access, focus, contrast, and announcements. Use for accessibility audit or requested remediation; a11y is the same canonical workflow."
---

# ui-accessibility

Inspect semantics, keyboard access, focus, contrast, and announcements.

## Choose this workflow

Use for accessibility audit or requested remediation; a11y is the same canonical workflow.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [UI and frontend methods](../../references/packs/ui.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; component/flow and target accessibility concerns. Apply for requested remediation.

**Pack prerequisites:** Target screens/flows, existing design conventions, and runnable UI or supplied references. Visual claims require actual renders; accessibility claims distinguish automated, keyboard, and assistive-technology evidence.

- **Infer from evidence:** Inspect the target flow, existing components/tokens, actual renders or supplied references and current responsive behavior.
- **Reasonable default:** Reuse established visual conventions and preserve keyboard behavior; label unrendered changes as visually unverified.
- **Ask only when needed:** Ask about an unresolved interaction or visual direction only when plausible choices materially differ; do not make a missing screenshot block source inspection.

Declared evidence requirements: `project.read`, `browser.inspect`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Semantic roles, labels, focus sequence and focus not obscured, keyboard interactions, pointer target size and dragging alternatives, contrast, reflow and text spacing, accessible authentication, consistent help, redundant entry, and announcements.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: edit the requested local implementation and perform relevant bounded checks while preserving unrelated work. Live data changes, remote actions and paid jobs require their resolved target and existing session authorization.

## Execute

1. Choose the actual task/route and interaction states: initial, loading, empty, error, open/closed and recovery where relevant. Inspect semantics, accessible names, relationships and contrast alongside the visible design, then the WCAG 2.2 AA additions for the stated target: focus not obscured by sticky content, 24 by 24 CSS pixel targets, single-pointer alternatives to dragging, authentication without a cognitive test, consistent help placement and no redundant re-entry.
2. Execute the keyboard path and record focus at each transition. For dialogs test entry, containment where appropriate, escape/close and return to the initiating control; if that control disappears, define a sensible surviving destination.
3. Exercise form errors and dynamic updates using the relevant interaction method. Check programmatic error association and announcements without relying on color or duplicate noisy live regions.
4. Use automated scanning as one evidence source, then verify corrected barriers with the actual keyboard or assistive technology tested. State browser/device/AT and uncovered states; an automated pass is not a blanket conformance claim.

## Technical method

- **Inspect:** Inspect native semantics, accessible name/description, focus sequence, contrast and live updates.
- **Method:** Use native controls first; apply matching APG interaction patterns for custom widgets and test behavior as well as attributes.
- **Avoid misdiagnosis:** Passing an automated checker does not prove keyboard or screen-reader usability; positive tabindex creates fragile ordering.
- **Check the result:** Complete the main flow using only keyboard, inspect focus visibility/return and announced errors, and report assistive-tech coverage actually exercised.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [UI and frontend worked example](../../references/examples/ui.md).
- Creating, editing or reviewing frontend UI, copy, states or visual assets: [Frontend iconography](../../references/frontend-icons.md).
- The affected project uses Flutter: [Flutter](../../references/frameworks/flutter.md).
- The affected project uses React Native / Expo: [React Native / Expo](../../references/frameworks/react-native.md).
- The task specifically involves gsap, motion design, framer motion, view transition, click path; load only the matching method: [Motion, visual direction and click paths](../../references/methods/motion-design.md).
- Auditing a dialog or modal overlay: [dialog interaction](../../references/scenarios/dialog.md).
- Auditing a menu button, tabs, disclosure, tooltip or popover: [menu, tabs, disclosure, tooltip and popover interaction](../../references/scenarios/menu.md).
- Auditing a combobox or autocomplete: [combobox interaction](../../references/scenarios/combobox.md).
- Auditing a date or range input: [date-picker interaction](../../references/scenarios/date-picker.md).

## Decision branches

- **When automated scans pass but focus or announcements fail:** Report the manual barrier and keep automated coverage separate from conformance claims.

## Deliver and verify

- Barrier and affected task/state, exact reproduction, correction, actual browser/input/AT evidence and remaining coverage gaps.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Modal focus returns to its trigger; errors are programmatically associated and usable without color alone.

## Stop and recover

- Do not claim screen-reader verification without running it. Automated scans alone cannot establish full conformance.

## Example requests

- **Normal (inspect):** Audit modal focus, keyboard dismissal, and error announcement behavior.
- **Edge (apply):** Fix modal focus return and server validation announcements without relying on color.
- **Blocked (inspect):** Audit semantics without a screen reader; explicitly leave screen-reader behavior unverified.

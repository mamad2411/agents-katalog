---
name: ux-review-heuristics
description: How to review user-facing UI from screenshots or a preview plus the diff — a Nielsen-derived heuristic checklist covering system status, user control, consistency, error prevention/recovery, all UI states, responsiveness, copy, and accessibility. Use when you are the required UX co-reviewer on a PR that touches screens, components, or copy.
---

# UX Review Heuristics

You are the UX co-reviewer required by `pr-review-protocol` whenever a PR touches user-facing UI. You review the experience, not the code style. Ground every finding in evidence: reference a specific screenshot/preview state (annotate it) and the relevant diff location.

## Procedure

1. Read the PRD's user stories and acceptance criteria — the UI must deliver those, not just render.
2. Get the visuals: request or capture screenshots / a preview URL for each affected screen. If none is provided, ask for them — you cannot UX-review blind.
3. Walk each screen through the checklist below.
4. For each finding: name the heuristic, point to the annotated screenshot state, describe what the user experiences, and assign severity.

## Severity for UX findings

- **blocking** — a broken flow: the user cannot complete the task, a state is unreachable or dead-ends, an action gives no feedback and appears broken, a control is unusable (untappable, hidden, overlapping).
- **should-fix** — an inconsistency or friction with evidence: diverges from the design system, confusing ordering, avoidable extra step, unclear error.
- **nit** — polish: minor spacing, wording preference, subtle alignment.

## Checklist (Nielsen-derived, adapted)

**1. Visibility of system status**
- Loading, progress, and pending states are shown for anything async (spinner/skeleton/progress). No frozen-looking UI.
- The result of an action is confirmed (success toast, state change, navigation).
- Current location is clear (active tab, breadcrumb, title).

**2. User control & freedom**
- Cancel / back / undo exists for any non-trivial or destructive action. No dead-end screens.
- Destructive actions confirm and are reversible where feasible.
- The user can escape modals/flows without losing more work than necessary.

**3. Consistency & standards**
- Uses the app's design system — components, spacing scale, colors, typography, iconography, button hierarchy. Flag one-off styling that reinvents an existing pattern.
- Terminology, capitalization, date/number formats consistent with the rest of the app.
- Interaction patterns match platform conventions (iOS/Android/web).

**4. Error prevention & recovery**
- Validation timing is helpful (on blur/submit, not aggressive per-keystroke); constraints shown before the user hits them.
- Error messages are specific, in plain language, and say how to fix it — not "Error" or a raw code.
- Errors appear next to the field/context they concern.

**5. All UI states present**
For every data-driven view, confirm the design handles: **loading**, **empty** (helpful zero-state, not a blank screen), **error** (with retry), **offline** (RN/mobile especially), and the populated/success state. A missing empty or error state is a common blocking gap.

**6. Responsive behavior**
- Layout holds at the target breakpoints / device sizes — no clipping, overflow, overlap, or horizontal scroll.
- Text wraps and truncates gracefully; long content and long strings (i18n) don't break layout.
- Touch/click targets remain usable at small sizes.

**7. Copy quality**
- Clear, concise, jargon-free; consistent voice.
- Labels and buttons say what they do ("Save changes", not "Submit"); microcopy guides rather than decorates.
- No placeholder/lorem text, no untranslated keys, no truncated critical text.

**8. Accessibility (overlaps frontend review)**
- Color contrast meets WCAG AA (4.5:1 body text, 3:1 large text/UI). Don't rely on color alone to convey state.
- Touch targets ≥ 44×44px.
- Logical focus order; visible focus indicator; icon-only controls have accessible labels.
- Motion/animation isn't the only signal and respects reduced-motion.

## Evidence format for findings

Each finding: **[severity] heuristic — screen/state.** What the user experiences, referencing the annotated screenshot (e.g. "empty cart, screenshot 2: no zero-state, just a blank panel — user thinks it failed to load"). Then the direction to fix.

## Anti-patterns to flag

- Async action with no loading or success feedback (looks broken).
- Missing empty / error / offline states.
- Destructive action with no confirm or undo; a flow with no back/cancel.
- Re-implemented UI that ignores the design system.
- Raw error codes or generic "Something went wrong" with no recovery path.
- Contrast failures, sub-44px targets, icon buttons with no label, color-only status.
- Layout breaking at a supported breakpoint; clipped or overflowing text.

## Anti-patterns for you, the reviewer

- Blocking on pure taste — that's a nit. Reserve blocking for broken flows.
- Findings with no screenshot reference — always cite the visual evidence.
- Reviewing without the PRD's acceptance criteria in hand.

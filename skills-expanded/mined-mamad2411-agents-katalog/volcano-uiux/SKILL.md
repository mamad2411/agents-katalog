---
name: volcano-uiux
description: Use for any user-facing Volcano frontend, web app, page, dashboard, board, gallery, poll, leaderboard, form, UI, or UX. Covers accessible responsive design, loading and progress feedback, forms, navigation, and complete interface states.
---
# Volcano UI/UX Skill

## Role
Build clear, accessible, responsive interfaces for Volcano apps. Pair this skill with the framework and domain skills that define implementation and data flow.

## When to Use
Use this skill for every user-facing frontend. Domain skill examples define the required data and flow; this skill defines how users see and operate them.

## Default Interface
When the prompt does not define a design:
- Reuse the project's components, tokens, layout, and interaction patterns before adding new ones.
- Build a simple visual hierarchy with one page title, logical heading order, a clear primary action, and consistent spacing.
- Start with a narrow-screen layout. Add breakpoints where content needs them, keep primary actions visible, and prevent accidental horizontal scrolling.
- Give each data view explicit loading, empty, error, and success states.
- Keep navigation clear and provide a visible way back or onward.
- Prefer native controls and browser behavior. Do not add a component library, animation system, or custom control unless the project already uses it or the prompt requires it.

## Progress Feedback
Show feedback where work occurs so the user knows the action started. Choose the smallest indicator that explains the wait.

| Situation | Feedback | Behavior |
|---|---|---|
| Work completes within about 200 ms | None | Avoid a spinner flash |
| Initial load with unknown duration | Spinner and short status text | Replace both with content, empty state, or error |
| Progress can be measured | Progress bar or count | Report real progress; do not simulate it |
| Final content layout is known | Skeleton matching that layout | Do not use a generic full-page skeleton |
| Button action | Stable-width button with text such as “Saving…” and an optional small spinner | Disable the trigger to prevent duplicate submits; restore it on completion |
| Background refresh | Small inline status | Keep existing content visible and usable |

Delay a transient spinner for about 200 ms. If it appears, remove it as soon as the operation completes. Never leave an indicator running after success or failure.

Pair visual indicators with text. Put changing status text in `role="status"` or an `aria-live="polite"` region. Hide decorative spinner graphics from assistive technology. Respect reduced-motion preferences.

## Forms and Actions
- Use visible labels. Do not use placeholder text as the only label.
- Keep entered data after recoverable errors and place validation messages next to the relevant field.
- Mark required fields in text and code. Use the correct input type and browser autocomplete value.
- Prevent duplicate submits and show clear success or error feedback.
- Move focus only when it helps the user reach an error, dialog, or new view.

## Accessibility
- Use semantic HTML before ARIA.
- Support keyboard input with visible focus states and logical focus order.
- Use descriptive link and button text.
- Maintain sufficient color contrast.
- Never rely on color, motion, hover, icons, or placeholder text alone to convey meaning.

## Verification Checklist
- The main flow works with keyboard-only input.
- The layout works at narrow and wide viewport sizes without accidental horizontal scrolling.
- Loading, empty, error, and success states are present where applicable.
- Slow actions show local progress feedback and block duplicate submits.
- Progress feedback includes text and is available to assistive technology.
- Forms have visible labels and preserve input after recoverable errors.

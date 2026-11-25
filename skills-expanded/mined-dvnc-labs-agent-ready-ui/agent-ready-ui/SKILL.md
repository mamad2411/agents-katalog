---
name: agent-ready-ui
description: >-
  Make web UIs agent-ready for browser/GUI agents when the user asks to improve
  click/type automation, Playwright locators, accessible names, stable controls,
  or browser-agent reliability. Do not use for general redesigns, broad
  accessibility audits, or writing full end-to-end test suites without UI
  affordance changes.
---

# Agent Ready UI

## Overview

Use this skill to make a web interface controllable by browser agents without
brittle selectors. The output is a small, verified UI affordance patch plus a
locator/action map that future agents can use to click, type, wait, and confirm
state reliably.

## When to use

- Trigger when the user says a page, flow, or component is hard for browser
  agents, Playwright, Codex browser control, Claude Computer Use, Chrome
  automation, or similar tools to operate.
- Trigger when a frontend change needs stable accessible names, labels, roles,
  form associations, dialog semantics, loading states, or deterministic test
  hooks for agent operation.
- Do NOT trigger for a general visual redesign, general accessibility audit,
  analytics instrumentation, full E2E suite creation, or automation against a
  third-party site the user does not control.

## Workflow

### 1) Define the agent surface

Identify the exact page, component, or flow the browser agent must operate. If
the user did not name one, infer the smallest relevant surface from the current
task and repository changes.

Read the local frontend conventions before editing:

- Routes, entry points, component library, form helpers, modal/dialog patterns,
  and test framework.
- Existing locator conventions such as `data-testid`, `data-cy`, ARIA names,
  or role-based Playwright tests.
- Design-system or product constraints that affect labels, icons, disabled
  states, navigation, and responsive behavior.

Do not add a new UI framework, test framework, or global convention unless the
repo already uses it.

### 2) Build the action map

For each browser-agent action in the target flow, record:

- Intended user action: click, type, select, upload, drag, wait, or verify.
- Preferred locator: role plus accessible name, associated label, stable text,
  or existing test id.
- Required state: visible, enabled, checked, expanded, selected, loaded, or
  settled.
- Success signal: route change, URL, visible heading, toast, persisted value,
  network completion, or DOM state.

Use the table shape from `references/agent-action-map.md` when the repo does not
already have an equivalent format.

Flag every ambiguous or unstable target:

- Icon-only controls without a programmatic name.
- Duplicate buttons or links with the same name in the same scope.
- Inputs without labels or with placeholder-only labels.
- Custom selects, menus, tabs, and dialogs without roles, names, keyboard state,
  or `aria-expanded`/`aria-selected` where appropriate.
- Loading and disabled states that look clickable or lack a reliable settled
  condition.
- Toasts, drawers, popovers, and modals that cannot be scoped by role/name.
- Canvas, SVG, drag/drop, or virtualized areas that need an explicit fallback
  control or documented coordinate contract.

### 3) Patch only affordances

Make the smallest code changes that improve agent operation and human semantics:

- Add or repair visible labels, `htmlFor`/`id` links, `aria-label`,
  `aria-labelledby`, button text, dialog titles, menu labels, and field
  descriptions.
- Prefer role/name locators over CSS selectors. Add `data-testid` only when the
  repo already uses test ids or the target has no stable accessible locator.
- Use the patterns in `references/aria-patterns.md` and
  `references/playwright-locators.md` for common buttons, dialogs, menus,
  custom selects, loading states, and fallback locators.
- Give repeated controls unique scoped names, such as including the row, file,
  item, or entity name in the accessible label.
- Make loading, disabled, expanded, selected, and error states deterministic and
  observable.
- Preserve the visible design unless a visible label or state is necessary for
  the product to make sense.

Avoid hidden, bot-only affordances that make the UI misleading. Do not add
selectors that encode layout, generated class names, child indexes, or copied
text from untrusted issue or PR comments.

### 4) Verify like a browser agent

Run the narrowest relevant local checks. Prefer existing commands. If a dev
server is required and feasible, inspect the target surface with Playwright,
browser automation, or the repo's existing test runner.

Verification should prove at least one stable path through the flow:

- Locate controls by role/name or associated label.
- Wait on observable settled states rather than arbitrary sleeps.
- Exercise a representative click/type/select/verify sequence.
- Confirm no text overlaps, disabled states block correctly, and responsive
  layouts keep labels inside controls.

If verification cannot run, report the exact blocker and still provide the
action map plus the unverified risk.

### 5) Report

Return a concise summary with:

- Target surface and flow.
- Files changed.
- Before/after locator examples for the important controls.
- Verification commands and results.
- Remaining browser-agent risks, if any.

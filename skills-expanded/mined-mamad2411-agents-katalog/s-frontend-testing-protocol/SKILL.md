---
name: s-frontend-testing-protocol
description: >-
  Use when building or iterating on frontend UI code, especially when mirroring
  an HTML/JS prototype, to drive a real browser with the Playwright plugin and
  verify every button, input, and interaction as you develop — not after.
---

# Frontend Testing Protocol

Frontend code is not verified until a real browser has exercised it. This skill
governs the tight build→verify loop you run through the Playwright plugin
(`browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`,
`browser_take_screenshot`, `browser_evaluate`) while writing UI code.

Testing-after is the failure mode. Launch the browser at the *start* of frontend
work and keep it open for the whole session.

## The loop

1. Open the browser and load the page before writing much code.
2. Make one small, attributable change.
3. Reload, snapshot the accessibility tree, exercise the surface you touched.
4. Fix any delta, then repeat.

**How big a change before you verify?** Small enough that a regression in the
browser points to exactly one edit. Batching changes turns debugging into
guesswork.

## Exhaustive interaction coverage

The bar: **no interactive element ships unclicked.** Enumerate the interactive
elements from the accessibility snapshot — do not rely on memory of what you
built. For each element, trigger it, assert the resulting state, and screenshot
if the change is visual. Work the full checklist in
`reference/interaction-coverage.md`.

Forms are where coverage silently lapses: test empty submit, invalid input,
validation messages, disabled/loading states — not just the happy path.

## Using browser tabs

When comparing two URLs (prototype vs. live build, staging vs. prod, before vs.
after), open each in its **own tab** at session start and keep both open.
Toggle between them with `browser_switch_tab` rather than navigating away and
back — navigating destroys scroll position, resets state, and makes diffing
harder. One tab per persistent context is the rule.

Open tabs at the start:
1. `browser_navigate` to the first URL — note the tab ID returned.
2. `browser_new_tab` → `browser_navigate` to the second URL — note its tab ID.
3. Switch with `browser_switch_tab(<id>)` throughout the session.

Keep the tab count minimal: one for each distinct URL you are actively
comparing. Close tabs you are finished with so the session stays readable.

## Mirroring a prototype

The prototype is the source of truth; the target is **zero visible diff**.

Do not eyeball it. Keep the prototype in one tab and your live build in another
(see **Using browser tabs** above) and compare *computed* styles via
`browser_evaluate` (`getComputedStyle`) — box model, spacing, font metrics,
color — because screenshots hide subpixel and spacing drift. See
`reference/prototype-parity.md`.

For the tedious styling grind: fix **one delta at a time and re-verify**.
Batched style guesses compound into drift you can no longer localize.

## Screenshots

All screenshots go to `p-tests/screenshots/` in the project root. If the folder
does not exist, create it before taking the first screenshot — do not use a
temp path or omit it. Name files descriptively: `<component>-<state>.png`
(e.g. `login-form-validation-error.png`).

**Live testing screenshots** (taken during iterative development to confirm a
change looks right) are temporary. Delete them once the change is verified —
they go stale the next time the UI shifts and become noise rather than signal.

**Reference screenshots** (taken to capture the canonical look of a prototype
or finished state for parity comparison) can be kept. They remain valid until
the reference itself changes, at which point they must be re-taken or deleted.

## What "verified" means

- Every interactive element triggered and its resulting state asserted
- All applicable states rendered: default, hover, focus, active, disabled,
  loading, error, empty
- Responsive breakpoints checked (mobile and desktop at minimum)
- Against a prototype: computed-style parity, not approximate resemblance
- Console clean — no errors or warnings introduced by the change

## Anti-patterns

- Writing all the code, then opening the browser once at the end
- Screenshot-only prototype comparison (misses spacing and subpixel drift)
- Exercising only a form's happy path; skipping validation and error states
- Leaving console errors because "it looks fine"
- Assuming an element works because the code reads correctly

Design and accessibility judgment live in `s-frontend-design`; test-level and
coverage decisions live in `s-test-strategy`. This skill owns the live browser
verification loop.

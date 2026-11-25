---
name: css-layout-debugging
description: Diagnoses broken flexbox and grid layouts by inspecting the box model and computed styles, then fixes the root rule instead of piling on overrides.
---

# CSS layout debugging

Find the rule that causes the problem. Do not stack `!important` on top of it.

## Steps

1. Pin down the failure: the element, the viewport width, the expected layout versus the actual layout. If a dev server and browser tools exist, load the page at that width and take a screenshot.
2. Walk up from the broken element to the root. For each ancestor read the computed `display`, `position`, `width`, `height`, `min-*`, `max-*`, `overflow`, `margin`, `padding`, `box-sizing`, `flex`, `grid-template-*`, `gap` and `transform`. Use `getComputedStyle` through the browser console when you can.
3. Check the usual causes in order:
   - Flex items default to `min-width: auto`, so long text or images stop them shrinking; the fix is `min-width: 0` on the item.
   - Percentage heights need a parent with a definite height.
   - `overflow` other than visible on an ancestor breaks `position: sticky`.
   - Margins collapse between block siblings and parent and child.
   - `align-items: stretch` and `auto` margins fight each other.
   - A grid track sized with `1fr` has the same min-content trap; use `minmax(0, 1fr)`.
4. Change one property at a time, in the browser first, then in the source file that owns the rule.
5. Recheck at the failing width and at one narrower and one wider width.

## Rules

- Fix the owning rule; never patch with fixed pixel widths, magic margins or `!important`.
- Do not restructure the markup unless the cause is in it.

## Report

Cause in one sentence, the property and file changed, and the widths you rechecked.

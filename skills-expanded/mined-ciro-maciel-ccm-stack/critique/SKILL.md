---
name: critique
description: Before showing a changed screen, capture it in every state, theme and size, score five axes, fix anything under 7. Use after any UI change.
---

# Review before you show

The person should never be the first one to find an overflow, a clipped menu or a spinner that never ends. You find them first, from screenshots of the real screen.

## Capture

For each screen you changed: light and dark theme, desktop and phone width. For each surface that loads data, all five states:

1. **Loading:** a skeleton in the shape of what is coming; after 15 seconds, a line saying it is taking longer than usual.
2. **Empty:** a real empty state that says what to do first.
3. **Error:** the cause in plain words and a way to retry, with what the person typed kept.
4. **Populated:** realistic data.
5. **Edge:** long names, many rows, missing optional fields.

## Score each capture, 0 to 10

| Axis | Ask |
|---|---|
| Coherence | Does it follow the design system exactly: spacing, type, components, icons? |
| Hierarchy | Is the one thing that matters most the first thing the eye lands on? |
| Detail | Alignment, overflow, truncation, padding, nothing touching an edge? |
| Function | Do controls work, answer a 44 px touch target, show focus, and give field errors under the field? |
| Distinction | Is there one deliberate choice that makes it feel made, not generated? |

Fix everything under 7 and capture again.

## Report

Three short lists: **Kept** (what works and why), **Fixed** (what you found and changed), **Still open** (what you could not fix, and why). Attach the final captures.

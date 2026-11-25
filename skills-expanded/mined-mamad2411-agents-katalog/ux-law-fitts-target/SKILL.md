---
name: ux-law-fitts-target
description: Use when sizing or placing any clickable/tappable element (button, icon, link, checkbox) or reviewing a layout for hard-to-hit targets — Fitts's Law and minimizing target distance. Triggers on "button too small", "hard to tap", "click target", "touch target size", "hover distance".
allowed-tools: Read, Edit, Grep, Glob
---

# Fitts's Law / Minimize Target Distance

Time to reach a target is a function of distance to it and its size: `T = a + b*log2(D/W + 1)`. Practically: bigger and closer targets are faster and more accurate to hit.

## Rules of thumb
- Minimum touch target: 44x44px (iOS HIG) / 48x48dp (Material). Never ship a tappable icon smaller than that hit area, even if the visible glyph is smaller (pad the hit box).
- Primary action gets the largest, most reachable target on the screen — don't make "Cancel" and "Confirm" the same visual weight.
- Place related actions near the content they act on (row-level delete button next to the row, not in a far toolbar) to cut travel distance.
- Screen edges and corners are effectively infinite targets (cursor stops at the boundary) — good place for frequently used, hard-to-miss actions (OS menus exploit this).
- Avoid making users travel far and then hit a small target (e.g., a tiny "x" in a far corner of a large modal) — that's the worst combination under Fitts's Law.

## Review checklist
1. Measure/estimate hit-box size on the smallest supported viewport.
2. Check spacing between adjacent tappable targets (avoid mis-taps) — 8px minimum gap.
3. Check distance from the triggering context to the resulting action.

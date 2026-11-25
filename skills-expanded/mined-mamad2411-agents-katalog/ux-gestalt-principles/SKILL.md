---
name: ux-gestalt-principles
description: Use when laying out grouped UI elements (form fields, cards, nav items, related controls) or choosing visual styling to signal relationships — covers Law of Proximity, Law of Similarity, Uniform Connectedness, and Law of Prägnanz. Triggers on "group these fields", "visual hierarchy", "related items layout", "how to signal these belong together".
allowed-tools: Read, Edit, Grep, Glob
---

# Gestalt Principles (Proximity, Similarity, Uniform Connectedness, Prägnanz)

The eye groups elements automatically based on visual cues, before reading any label. Use these cues intentionally instead of fighting them.

## Law of Proximity
Elements placed close together are perceived as related. Use whitespace, not borders, as the primary grouping signal: tighter spacing within a group, larger gaps between groups (e.g., form field + its label + its error message closer together than to the next field).

## Law of Similarity
Elements sharing color, shape, or size are perceived as the same category/function. Keep a single visual style per action type (all destructive actions red, all primary actions the same button style) — don't reuse a style for unrelated purposes, it implies false grouping.

## Uniform Connectedness
Elements visually connected by a shared container, line, or background are perceived as one unit even if physically apart. Use a bounding box/shared background to bind items whose proximity alone isn't enough (e.g., a card wrapping stats scattered across a wide row).

## Law of Prägnanz (simplicity)
The eye resolves ambiguous shapes into the simplest interpretation. Avoid layouts that force the user to reconcile conflicting cues (e.g., proximity says "grouped" but color says "different categories") — simplify until only one grouping reading is possible.

## Review checklist
1. Do whitespace/borders match the actual logical grouping?
2. Is any visual style (color/shape/size) reused across unrelated meanings?
3. Would a first-time viewer parse the grouping correctly with labels hidden?

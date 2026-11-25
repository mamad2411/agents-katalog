---
name: iconography-style-keeper
description: Unifies mismatched icons into one consistent system in the brand style, matching weight, fill, corner, and color.
---

# Iconography Style Keeper

## When to use

Use this skill when icons are mismatched in weight, fill, or color. Symptoms include a slide with one line icon next to one solid glyph, icons at different stroke weights, icons in random colors, a mix of flat and skeuomorphic styles, and clip-art icons sitting beside clean brand icons. Run this in Stage 3 with the other brand-asset work.

## What it does

It converts the deck's icons to a single, consistent system in the brand style: one stroke weight, one fill convention, one corner treatment, one color rule, and a consistent optical size. The result is a deck where icons look like a designed set rather than a collection of finds.

## Method

An icon system is defined by a few consistent attributes. The job is to pick the system and bring every icon onto it.

1. **Define the target style.** Decide the system from the brand: line or solid, the stroke weight (for line icons), the corner radius (sharp or rounded), the color rule (single brand color, or two-tone), and the optical size on a slide. If the brand has an icon library, use it as the source of truth.

2. **Inventory the icons.** Walk the deck and record every icon: its style, weight, fill, color, and size. Note which are on-system and which are not.

3. **Replace off-system icons.** For each off-system icon, find the closest equivalent in the brand library (or a consistent open icon set already in use) and swap it in. Do not try to hand-edit a clip-art glyph into the line style; replace it.

4. **Normalize weight and corners.** For line icons, set a single stroke weight so thick and thin icons match. For corners, apply the system's radius consistently so some icons are not sharp while others are rounded.

5. **Apply the color rule.** Recolor all icons to the brand's icon color (often the primary or a neutral), keeping the one-accent rule: an icon may take the accent color only when it is the emphasized element on the slide. Bind icon color to a theme slot so it moves with the theme.

6. **Size optically, not by bounding box.** Set icons to a consistent optical size. Because a circle and a tall rectangle with the same bounding box look different in weight, adjust so they read as the same size rather than matching pixel boxes.

7. **Align to text and grid.** Vertically center icons with their adjacent labels and align icon rows to the layout grid so a row of feature icons sits on one baseline.

## Inputs

- The deck.
- The brand icon library or the icon-style rules (line or solid, stroke weight, corner, color, size). If undocumented, ask, or pick one consistent open set and state the choice.

## Output format

An icon system report:

- The target style, restated: style, weight, corner, color rule, size.
- A per-icon list: current style and the action (swap to library, recolor, re-weight, resize, realign).
- A note on any icon kept as-is and why.

Close with a confirmation that all icons share one weight, one fill convention, one corner, and the brand color rule.

## Example

Input: a four-feature row mixing two line icons, one solid icon, and one clip-art glyph in three colors.

Output:

- Target: line icons, single stroke weight, sharp corners, primary brand color, one optical size.
- Swap the solid icon and the clip-art glyph for line equivalents from the brand library.
- Recolor all four to the primary, bound to the theme slot.
- Resize to one optical size and align on one baseline.
- Result: a coherent four-icon set in the brand style.

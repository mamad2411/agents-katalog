---
name: theme-color-binder
description: Binds shape and text fills to theme color slots instead of hard-coded RGB so a single re-theme updates the whole deck.
---

# Theme Color Binder

## When to use

Use this skill when shapes and text use hard-coded RGB values instead of theme color slots. The symptom is a deck that looks roughly on-brand but will not update when the theme changes, because every fill is a fixed hex value pasted in by hand. Run this in Stage 2, after the structure is clean, so that the later palette and re-theme work has something to act on.

## What it does

It rebinds fills, lines, and text colors to the theme's named color slots (text and background, the six accents, and the hyperlink colors), so the deck is wired to the theme. After this skill, changing the theme color set recolors the deck correctly, and the Brand Palette Guard and Reskin-to-Template Converter skills can do their job.

## Method

A PowerPoint theme defines twelve color slots: Text 1, Text 2, Background 1, Background 2, Accent 1 through Accent 6, Hyperlink, and Followed Hyperlink. Theme-bound fills move with the theme. Hard-coded RGB does not. The job is to map every color in the deck onto the right slot.

1. **Read the theme color set.** From the template, list what each slot resolves to: which slot is the dark text color, which is the light background, which accent is the primary brand color, which accents are the secondary and tertiary colors, and which slots are reserved for charts. Keep this map at hand.

2. **Inventory the colors in use.** Walk the deck and record the distinct fill, line, and font colors. Group near-duplicates (for example three slightly different blues that all mean "primary").

3. **Map each color to a slot.** For each distinct color, decide the intended theme slot. The main brand color maps to Accent 1 (or whatever the template designates as primary). Dark body text maps to Text 1. Light panel fills map to Background 2. Map near-duplicates to the same slot so they converge.

4. **Rebind fills and lines.** For each shape, set the fill from the theme color picker's top row (Theme Colors), not the Standard Colors row and not a custom hex. Use the matching tint or shade column where the brand allows lighter or darker variants of a slot, since those tints also move with the theme.

5. **Rebind text colors.** Set font colors from Theme Colors too. Body text to Text 1, light-on-dark text to Background 1, accents to the accent slots.

6. **Fix chart colors.** Charts often carry their own hard-coded series colors. Set series fills to theme accents in order, so the chart recolors with the theme. Avoid locking a series to a custom hex.

7. **Verify by test-swapping.** As a check, temporarily switch to a different theme color set and confirm the deck recolors sensibly. Then switch back. Anything that does not move was missed; rebind it.

## Inputs

- The deck to rebind.
- The theme color set and which slot is intended for the primary, secondary, and chart colors. If unknown, ask for the slot map before binding.

## Output format

A binding table as prose or a list:

- Each distinct current color (hex) and the theme slot it should map to.
- Notable rebinds (charts, panels) called out.
- A note on any color that intentionally stays fixed (rare; usually a logo asset).

Close with the test-swap confirmation that the deck recolors with the theme.

## Example

Input: a deck using `#2A41D8` in some places and `#2B40D6` in others for the brand blue, plus a custom grey for panels.

Output:

- `#2A41D8` and `#2B40D6`: both map to Accent 1. Converge to one slot.
- Panel grey `#EEF1F6`: map to Background 2.
- Chart series: bind to Accent 1, Accent 2, Accent 3 in order.
- Test-swap confirms all fills move with the theme.

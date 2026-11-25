---
name: reskin-to-template-converter
description: Rebuilds an off-brand deck on the approved template, recolored and retyped, preserving the content while changing the skin.
---

# Reskin-to-Template Converter

## When to use

Use this skill when an off-brand deck must move onto the approved template. The situation: a deck arrives from another team, an acquired company, or an old template, and it needs to become a brand-compliant deck without rebuilding every slide from scratch. Run this last in Stage 4, or as a one-shot when you receive a foreign deck and want a fast, faithful conversion.

## What it does

It rebuilds the deck on the brand template: every slide moved to a real template layout, content placed in placeholders, colors recolored to theme slots and the approved palette, type set to the brand fonts and scale, and logos, icons, and imagery brought onto the brand style. The content is preserved; the skin is replaced. The output is the same argument, fully on-template.

## Method

This skill orchestrates the other eleven in a fixed order, applied to a foreign deck rather than your own. The order matters: structure first so styling has placeholders to land in, then color and type, then assets, then the audit.

1. **Apply the template.** Attach the brand template to the deck (Design then the brand theme, or copy slides into a file based on the brand .potx). This swaps the theme colors, fonts, and master, which immediately repaints theme-bound elements. Expect the hard-coded ones to remain wrong until step 3.

2. **Remap layouts.** Run the Master and Layout Mapper logic: put each slide on the correct brand layout (Title, Section Header, Title and Content, and so on). Foreign decks often have custom layouts that must be mapped to the nearest brand layout.

3. **Move content into placeholders.** Run Placeholder Discipline: migrate titles and body copy from foreign boxes into the brand layout's placeholders, clear direct formatting, and delete the empty boxes. This is where most of the reskin happens, because placeholder content adopts the brand instantly.

4. **Realign to the grid.** Run Grid, Margin and Safe-Zone Alignment so content sits on the brand margins and grid rather than the foreign deck's.

5. **Recolor and retype.** Run Theme Color Binder, Brand Palette Guard, and the Theme Font and Type-Scale Enforcer: rebind colors to theme slots, replace off-palette colors, apply the one-accent rule, and swap fonts to the brand pair on the scale. Use Replace Fonts deck-wide for speed, and find-and-replace recolor for repeated hard-coded fills.

6. **Fix the assets.** Run Logo and Lockup Compliance, Iconography Style Keeper, and Imagery and Photo Treatment: replace the foreign logo with the brand logo, swap icons to the brand set, and apply the brand image treatment.

7. **Standardize furniture.** Run Title, Footer and Page-Number Consistency so titles, footers, page numbers, and dividers match the brand.

8. **Audit.** Finish with the Brand Compliance Auditor to catch anything the bulk conversion missed, and clear the Blockers.

Throughout, preserve content: do not drop slides, do not rewrite copy, do not lose data in charts. The goal is a faithful reskin, not a rewrite.

## Inputs

- The off-brand deck to convert.
- The brand template (.potx or .thmx) plus the brand rules (palette, fonts, logo, icon and image style, furniture). If the template is not provided, ask for it; the reskin cannot run without it.

## Output format

A conversion plan and result summary:

- The order applied (template, layouts, placeholders, grid, color, type, assets, furniture, audit).
- A per-slide note where a slide needed manual attention (custom layout, complex graphic).
- The final audit headline (Blockers, Majors, Minors) confirming the deck is on-template.

Close with a confirmation that content is preserved and the deck is rebuilt on the brand template.

## Example

Input: a 25-slide deck from an acquired company, on their old template.

Output (excerpt):

- Attached the brand template; theme-bound colors repainted automatically.
- Mapped their five custom layouts to the brand's Title, Section Header, Title and Content, Two Content, and Closing.
- Migrated all titles and body copy into placeholders; deleted 60-plus rogue boxes.
- Replaced their blue with Accent 1 via find-and-replace recolor; swapped their font for the brand pair via Replace Fonts.
- Swapped logo, icons, and applied the brand duotone to photos.
- Final audit: 0 Blockers, 2 Majors flagged for a human. Content preserved, deck on-template.

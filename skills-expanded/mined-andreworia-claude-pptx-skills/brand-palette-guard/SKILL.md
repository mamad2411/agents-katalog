---
name: brand-palette-guard
description: Restricts a deck to the approved brand palette with one accent rule so slides stop drifting into off-brand or rainbow colors.
---

# Brand Palette Guard

## When to use

Use this skill when slides drift into off-brand or rainbow colors. The symptoms: a chart with seven saturated hues, a slide that picked up a color from a pasted screenshot, callouts in a red that is not the brand red, and decorative shapes in colors no one approved. Run this after Theme Color Binder, so you are guarding a deck whose colors are already wired to theme slots.

## What it does

It reduces the deck to the approved palette and enforces a single accent rule: a neutral base, the brand's core colors, and one accent used sparingly to draw the eye. The result is a deck that reads as one brand rather than a swatchbook, with color carrying meaning instead of decoration.

## Method

A brand palette is usually small: one or two primary colors, a couple of neutrals, and one or two accents reserved for emphasis. The job is to map everything onto that set and to use the accent only where it earns its place.

1. **State the approved palette.** List the allowed colors and their roles: primary, secondary, neutral light, neutral dark, and the one accent reserved for emphasis. Note any chart-specific sequence the brand defines.

2. **Find off-palette color.** Scan the deck for any fill, line, or text color outside the approved set. Pasted images, third-party logos, and old slides are the usual sources. Record each offender and where it appears.

3. **Replace off-palette color with the nearest approved slot.** Map each stray color to the closest brand color by role, not by hue alone. A random teal used as a panel becomes the neutral panel color. A random orange used for emphasis becomes the brand accent.

4. **Apply the one-accent rule.** Per slide, the accent color should appear once, on the single thing the slide wants the eye to land on (the key number, the recommended option, the highlighted bar). Recolor everything else to the neutral or primary base. If two things are accented, demote one.

5. **Tame charts.** Replace rainbow chart palettes with a restrained sequence: the brand primary for the focus series and neutral greys for the rest, or the brand's defined chart sequence if it has one. Direct-color the series that carries the message and grey the context.

6. **Check contrast and legibility.** Confirm text on colored fills meets a readable contrast. Light text on a mid-tone accent often fails; switch to the dark or light neutral as needed. Do not introduce a new color to fix contrast; use the palette's existing light and dark ends.

7. **Leave logos alone.** Approved third-party or partner logos keep their own brand colors. Do not recolor a real logo to fit the palette.

## Inputs

- The deck to guard.
- The approved palette with roles (primary, secondary, neutrals, the one accent) and any chart sequence. If not provided, ask for the palette first.

## Output format

A palette enforcement report:

- The approved palette and roles, restated.
- A list of off-palette colors found, where, and the approved color each maps to.
- Per-slide accent calls: what gets the single accent, what gets demoted.
- Chart recolor notes.

Close with a confirmation that the deck uses only approved colors and one accent per slide.

## Example

Input: a five-series bar chart in five bright colors, with the recommendation slide using two different highlight colors.

Output:

- Approved palette: primary blue, dark neutral, light neutral, accent orange. Chart sequence: blue then greys.
- Chart: color the focus series blue, set the other four to graded greys. Drop the five-color scheme.
- Recommendation slide: keep the accent orange on the recommended option only; recolor the second highlight to the neutral.
- Result: one accent per slide, no off-palette color.

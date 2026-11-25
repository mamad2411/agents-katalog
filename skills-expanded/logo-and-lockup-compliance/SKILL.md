---
name: logo-and-lockup-compliance
description: Restores the correct logo lockup with brand clear space and minimum sizing wherever the wrong logo, color, or crop appears.
---

# Logo and Lockup Compliance

## When to use

Use this skill when the wrong logo, color, or crop appears, or when clear space is violated. Symptoms include an old logo on the title slide, the full-color logo on a dark background where the reversed version belongs, a logo stretched out of proportion, a low-resolution logo pulled from a web search, and text or objects crowding the logo inside its clear-space zone. Run this in Stage 3 once color and type are clean.

## What it does

It ensures every logo in the deck is the correct, approved lockup in the right color variant, at a legal size, with the brand's clear space preserved, and undistorted. The output is a deck where the logo always appears the way the brand guidelines require.

## Method

A logo lockup is the approved arrangement of the mark and wordmark. Brands define variants (full color, reversed or white, single color, mark-only), a minimum size, and a clear-space rule (a margin around the logo, usually expressed as a multiple of part of the mark). The job is to enforce all of it.

1. **Identify the approved assets.** List the logo variants the brand provides and where each is used: full color on light, reversed on dark or on photos, single color where color is unavailable, and mark-only for tight spaces. Note the minimum size and the clear-space multiple.

2. **Find every logo instance.** Walk the deck and record each place a logo appears: title slide, footer or corner, dividers, closing slide, partner-logo rows. Note the variant, the background it sits on, and its size.

3. **Swap to the correct variant per background.** On a light background use the full-color (or primary) variant. On a dark background or over a photo use the reversed variant. Never recolor the logo by hand; use the approved file for that variant.

4. **Replace bad files.** Replace any low-resolution, traced, or outdated logo with the current high-resolution asset. Prefer a vector (EMF or SVG) or a high-resolution PNG over a small raster pulled from elsewhere.

5. **Fix distortion.** Confirm the logo is at its native aspect ratio. If it was stretched, reset it: hold Shift while resizing from a corner, or set width and height to the native ratio. Never scale one dimension alone.

6. **Enforce clear space.** Apply the brand's clear-space rule: keep a margin around the logo equal to the defined multiple, and move any text or object that intrudes into that zone. The footer logo especially tends to get crowded by page numbers; separate them.

7. **Enforce minimum size and placement.** Confirm no logo is below the minimum legible size. Place the persistent logo in the brand's designated corner consistently across the deck, not in a different spot per slide.

8. **Handle partner logos fairly.** In a partner or client logo row, keep each logo in its own approved form and color, sized to optical balance rather than identical pixel width, with even spacing.

## Inputs

- The deck.
- The approved logo files and the brand rules: variants, minimum size, clear-space multiple, and designated placement. If not provided, ask for the logo kit and rules first.

## Output format

A logo compliance report:

- A per-instance list: slide, current variant and condition, the correct variant, and the fix (swap, replace file, un-stretch, add clear space, reposition).
- A flag for any low-resolution or outdated file that needs the real asset.

Close with a confirmation that every logo is the approved lockup, correct variant, undistorted, with clear space, at or above minimum size.

## Example

Input: title slide uses last year's logo, a dark divider shows the full-color logo, and the footer logo is stretched wide.

Output:

- Title slide: replace old logo with the current full-color asset.
- Dark divider: swap to the reversed (white) variant.
- Footer: reset to native aspect ratio; move the page number out of the clear-space zone.
- Result: correct variant per background, no distortion, clear space respected.

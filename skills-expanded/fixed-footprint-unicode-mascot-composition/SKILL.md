---
name: fixed-footprint-unicode-mascot-composition
description: "Build terminal mascots whose poses can animate without changing layout by keeping the render area fixed and swapping only the moving fragments."
metadata:
  author: ychampion
---

# SKILL: Fixed-Footprint Unicode Mascot Composition
**Domain:** terminal-ui
**Trigger:** Use when adding a terminal mascot or branded character that should animate via pose swaps but must stay within a fixed footprint so surrounding layout remains stable.
**Source Pattern:** Distilled from reviewed fixed-footprint terminal mascot implementations.

## Core Method
Split the mascot art into stable background spans and separately swappable moving fragments such as eyes, arms, or accessories. Keep the total row and column footprint constant across every pose and render inside a fixed-size container so the rest of the UI never reflows while the character changes expression. This allows expressive terminal art without destabilizing adjacent status lines, banners, or prompts.

## Key Rules
- Keep the row and column count constant for every pose so surrounding layout never shifts.
- Treat body fill, padding, and background spans as stable segments and swap only the moving fragments.
- Render inside a fixed-height container and clip vertical motion so jumps or crouches stay inside the frame.
- Prefer fragment swaps over full-frame redraws to reduce work and avoid alignment drift.

## Example Application
If a CLI banner needs a small animated mascot for loading, keep the character inside a fixed three-line frame and swap only the eyes and arms between idle, alert, and celebration poses so the header stays perfectly aligned.

## Anti-Patterns (What NOT to do)
- Do not let different poses use different widths or heights; that will push neighboring UI around.
- Do not rebuild the entire art every frame when only localized fragments need to change.

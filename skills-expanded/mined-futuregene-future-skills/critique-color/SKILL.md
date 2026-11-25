---
name: critique-color
description: Critique the colour of one rendered screen — WCAG contrast ratios for text and controls, palette coherence against tokens, semantic colour use, and colour-vision / forced-colour robustness — with a pass / minor / major rating per dimension and specific fixes. Use when reviewing a screenshot or build.
license: MIT license
category: docs
metadata: {"version": "1.0", "skill-author": "MC Dean (designer-skills)"}
---

# Critique Colour

Audit every colour decision on a screen and flag each deviation with a measured value and a concrete
fix. 中文触发：配色评审、对比度检查、语义色、色盲可读性。

## Dimensions

### 1. Contrast
- Body text meets **WCAG AA 4.5:1**? Large text (**18px+ regular, 14px+ bold**) meets **3:1**?
- Interactive components (buttons, inputs, focus rings) meet **3:1** against adjacent surfaces?
- Flag every failing pair with its **actual measured ratio and the minimum required**
- Check placeholder text and disabled states — they commonly fail in ways that block use

### 2. Palette coherence
- Is the palette limited to defined token values, or do arbitrary hex values appear?
- Are neutrals, primaries and accents used in their intended roles?
- Do adjacent or overlapping colours create unintended noise or vibration?
- Is the whole palette warm, cool or neutral — and is that register right for the context?

### 3. Semantic use
- Is colour the **sole** indicator of state (error, success, warning)? Flag it — colour must be paired
  with an icon, label or pattern
- Are status colours applied consistently across the screen?
- Does interactive colour clearly differ from non-interactive colour?
- Are decorative colours being mistaken for actionable elements?

### 4. Accessibility beyond contrast
- Do the foreground/background pairs fail for common colour-vision deficiencies (deuteranopia,
  protanopia)?
- Does the interface hold up in Windows High Contrast / forced-colour modes?
- Does decorative colour interfere with legibility?

## Output format

For each dimension give:
1. **Observation** — neutral, factual, with measured values
2. **Problem** — what is broken and why it matters
3. **Fix** — a specific change, including the ratio, token name or pairing

Rate each dimension `pass` / `minor issue` / `major issue`. Sort fixes by user impact, not by
finding order.

Ratio reference: `#767676` on white is exactly 4.54:1 (a safe body-text grey); `#949494` on white is
3.03:1 (large text or UI only); anything below 3:1 fails both.

## Common failures
- Link colour below 4.5:1 on white once the underline is removed
- Error states in red only, with no icon or label
- Placeholder text at 40% opacity failing contrast on light surfaces
- One-off hex values introduced outside the token system
- Interactive and non-interactive elements sharing the same treatment

## Working rules
- Measure, do not eyeball — quote the ratio in the finding
- Judge token compliance against the actual token file, not an approximation of the brand palette
- Never propose a fix that only moves the failure somewhere else (e.g. lifting text contrast by
  dropping the border below 3:1)

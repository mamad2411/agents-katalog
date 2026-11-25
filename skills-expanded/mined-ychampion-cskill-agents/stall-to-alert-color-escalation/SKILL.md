---
name: stall-to-alert-color-escalation
description: "Blend spinner or progress colors toward an alert hue as stall intensity rises so stuck work becomes visually obvious without changing layout."
metadata:
  author: ychampion
---

# SKILL: Stall-to-Alert Color Escalation
**Domain:** terminal-ui
**Trigger:** Use when a spinner or progress indicator should warn about stalls without replacing itself with a larger warning UI.
**Source Pattern:** Distilled from reviewed stall-sensitive terminal indicator rendering patterns.

## Core Method
Start with the indicator's normal theme color, then interpolate it toward a known alert color as stall intensity rises. If exact color math is unavailable, fall back to a semantic alert token instead of failing. This creates a smooth escalation path that preserves the indicator's footprint while still making degraded states obvious.

## Key Rules
- Drive the escalation from a normalized stall intensity rather than fixed hardcoded time branches inside the renderer.
- Keep a safe fallback path when literal color parsing fails.
- Preserve the same spinner or indicator footprint while only changing color and, if needed, subtle glyph intensity.

## Example Application
For a long-running build spinner, fade the normal accent color toward red as the system detects a likely stall, while keeping the same single-cell spinner slot.

## Anti-Patterns (What NOT to do)
- Do not swap the spinner for a larger banner at the first sign of delay.
- Do not hardcode one threshold and one end-state color without a smooth ramp.
- Do not let stall visuals change the indicator's size or alignment.

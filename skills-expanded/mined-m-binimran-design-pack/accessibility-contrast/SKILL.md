---
name: accessibility-contrast
description: Audit a palette or design for WCAG color contrast and legibility, and suggest compliant adjustments. Use when finalizing a palette, design tokens, or any text-over-color/imagery.
---

# accessibility-contrast

Make sure text is actually readable - measured, not eyeballed.

## Process
1. **List the text/background pairs:** body on bg, headings, buttons, links, text over imagery, states.
2. **Compute WCAG contrast** for each (the `contrast-guard` hook checks CSS automatically):
   - Normal text: **>= 4.5:1**; large/bold (>= 24px or >= 18.66px bold): **>= 3:1**; UI/graphics: **>= 3:1**.
3. **Fix failures:** darken text / lighten background, adjust the token, or add a scrim behind text over images.
   Keep the brand feel while reaching the ratio.
4. **Beyond contrast:** don't rely on colour alone; check type size/weight legibility; check focus states.

## Output
- A table: pair -> measured ratio -> pass/fail -> suggested fix. Confirm fixes still hit the target.

## Guardrails
- State measured ratios, not guesses. AA is the floor for client/commercial work.
- A "fix" must actually reach the threshold - re-check after adjusting.

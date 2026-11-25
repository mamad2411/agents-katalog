---
name: ui-ux-polish
description: "Iterative UI/UX polishing workflow for web applications. Achieve Stripe-level visual polish through multiple passes — each iteration adds incremental improvements that compound dramatically. Use when: polish UI, improve UX, make it look better, Stripe-level, world-class design, desktop and mobile optimization, visual polish."
license: MIT
metadata:
  version: 1.0.0
  category: design
  tags: [ui, ux, polish, design, css, tailwind, responsive, mobile, desktop]
---

# UI/UX Polish

Iterative polishing workflow that systematically improves web application interfaces toward production quality.

## Workflow

### Step 1: Audit Current State
Read the application's main pages/components. For each, note:
- Spacing inconsistencies (not on 8px grid)
- Typography issues (too many sizes/weights, poor hierarchy)
- Color contrast violations (check against WCAG 4.5:1 for text)
- Missing states (hover, focus, loading, error, empty)
- Mobile vs desktop issues

### Step 2: Prioritize Improvements
Rank findings by impact:
1. Accessibility violations (contrast, touch targets) — fix first
2. Spacing/alignment inconsistencies — high visual impact
3. Missing interaction states — hover, focus, pressed
4. Typography hierarchy — size and weight cleanup
5. Animation/transition smoothness
6. Dark mode consistency

### Step 3: Apply Changes
For each improvement:
- Make the specific code change
- Explain what changed and why
- Consider both desktop and mobile separately

### Step 4: Verify
After each round, check:
- No regressions introduced
- Changes work on both desktop and mobile
- Accessibility maintained or improved

### Step 5: Iterate
Repeat Steps 1-4. Each pass finds smaller issues. Stop when changes become minimal (typically 3-5 passes for significant improvement).

## Quality Targets
- All text: 4.5:1 contrast ratio minimum
- All spacing: divisible by 4 or 8
- All interactive elements: visible focus state
- All buttons: 44px minimum touch target on mobile
- Typography: max 3 font sizes, 2 weights
- Animations: 200-300ms duration, ease-out curve

## Example Output
```
Pass 1 (12 changes):
- Fixed 4 contrast violations in sidebar text
- Aligned card padding to 8px grid (was 13px -> 16px)
- Added hover states to 3 buttons missing them
- Increased mobile CTA touch target from 36px to 48px

Pass 2 (7 changes):
- Reduced font sizes from 6 to 3 (unified scale)
- Added loading skeleton to data table
- Smoothed page transition (added 200ms ease-out)

Pass 3 (3 changes):
- Fine-tuned shadow consistency across cards
- Added focus-visible outlines for keyboard nav
- Aligned icon sizes to consistent 20px

Quality Score: 8.5/10 (up from 5.5/10)
```

## Error Handling
- If no UI files found: ask user to specify which files/components to polish
- If framework not recognized: apply generic CSS/HTML improvements
- If changes break layout: revert and try smaller changes

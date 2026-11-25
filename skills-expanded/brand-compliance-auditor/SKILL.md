---
name: brand-compliance-auditor
description: Audits a finished deck against the brand and template and returns a flagged list of every off-brand and off-template element.
---

# Brand Compliance Auditor

## When to use

Use this skill when a finished deck needs a check before it ships. It is the pre-flight pass: the deck is built, you think it is on-brand, and you want a systematic sweep that catches the off-template layout, the hard-coded color, the rogue font, the stretched logo, and the missing page number before a partner or client does. Run it near the end of Stage 4, after the structural and asset fixes.

## What it does

It walks the whole deck against a brand-and-template checklist and returns a prioritized list of every violation, grouped by severity, each with the slide, the issue, and the fix. It does not silently change the deck; it produces the punch list so a human (or the Reskin skill) can act.

## Method

Audit against a fixed checklist so nothing is missed, and grade each finding by how much it hurts compliance.

1. **Structure checks.** For each slide: is it on a real template layout (not Blank)? Is content in placeholders rather than rogue boxes? Are titles, content, and furniture inside the margins and safe zone?

2. **Color checks.** Are fills and text bound to theme color slots rather than hard-coded hex? Is every color within the approved palette? Is there one accent per slide, used on the right element? Are charts on the brand sequence, not a rainbow?

3. **Type checks.** Are only the two theme fonts used? Are all sizes on the type scale? Is case consistent? Is line spacing the brand value? Any rogue bold, italic, or all-caps?

4. **Logo checks.** Is the correct, current logo used? The right variant for each background? Undistorted? At or above minimum size? Is clear space respected? Are partner logos fair and balanced?

5. **Icon and image checks.** Do icons share one style, weight, corner, and color rule? Do photos share one treatment, allowed aspect ratios, and the crop convention? Any low-resolution asset?

6. **Furniture checks.** Are titles uniform in position and style? Is the footer consistent? Are page numbers present, uniform, and in the right place? Are dividers parallel? Are the title and closing exceptions deliberate?

7. **Grade each finding.** Classify as Blocker (cannot ship: wrong logo, off-template layout, off-palette brand color, unreadable text), Major (clearly off-brand but shippable in a pinch: rogue font, inconsistent footer, rainbow chart), or Minor (polish: a few points of misalignment, an icon weight mismatch).

8. **Order the punch list.** Sort by severity, then by frequency, so the user fixes the systemic Blockers first. Point each finding at the skill that fixes it.

## Inputs

- The finished deck.
- The brand and template references: template layouts, theme colors and fonts, approved palette, logo rules, icon and image rules, and furniture conventions. If any are missing, audit against what is provided and note the gaps.

## Output format

A prioritized audit punch list:

- A one-line headline count (Blockers, Majors, Minors).
- Blockers, then Majors, then Minors. Each item: slide number, the issue, the rule it breaks, the fix, and the skill that fixes it.
- A short systemic note: the two or three patterns that recur most, so they can be fixed once across the deck.

Close with a ship or hold recommendation based on whether any Blocker remains.

## Example

Input: a 20-slide deck that looks finished.

Output (excerpt):

- Headline: 3 Blockers, 6 Majors, 5 Minors. Recommendation: hold until Blockers cleared.
- Blocker. Slide 1: outdated logo. Fix: replace with current asset (logo-and-lockup-compliance).
- Blocker. Slides 4 and 11: off-template layout (Blank). Fix: map to Title and Content (master-and-layout-mapper).
- Major. Slides 6 to 9: rainbow chart palette. Fix: brand chart sequence (brand-palette-guard).
- Major. Slide 14: Calibri title. Fix: theme font (theme-font-and-type-scale-enforcer).
- Systemic: hard-coded blue recurs across 8 slides; bind to Accent 1 once (theme-color-binder).

---
name: design-review
description: "Review existing UI aesthetics against brand and composition goals; prioritize evidenced layout, typography, color, hierarchy, and imagery issues. Use for visual design audits."
---

# Review visual design and art direction

## Scope

Review an existing UI, screenshot, prototype or implementation against its design intent and brand constraints. Distinguish observed visual issues from untested interaction behavior.

## Procedure

1. Establish actual target: brand, product segment, user task, page type (marketing/editorial/transactional/data dense), design constraints, available artifacts, and target viewports/themes. Separate opinions about style from violations of documented requirements.
2. Observe the full page and at least the important component states; inspect two or more screen sizes when possible. If no browser access, label responsive and interactive judgments **untested**. Inventory typography roles, palette roles, grid, spacing, borders/shadows, imagery and primary focal moment.
3. First-pass scan: **emphasis → contrast → balance → movement → proportion → repetition → unity**. Then examine seven elements: line, shape, form, color, value, texture and space. Use the structured catalog `../design-diagnose/references/principles.json` and ten routing categories.
4. Compare with the actual design system/brand guide. Do not recommend wholesale rebranding as a fix for one misaligned card. Audit cross-screen unity and route each finding to one specialist; cite the exact source article when useful.
5. For each issue: evidence, user or brand consequence, severity, proposed change, tradeoff, and test. Distinguish **confirmed visual observations** from hypotheses about user behavior. Run `wcag-review` and `ux-review` separately where barriers or usability questions arise.
6. Avoid subjective numeric scores. Report **observed** outcomes and reproducible checks. Sort by impact and change leverage; prefer design token fixes when they correct multiple screens.

## Deliverable

Lead with a 2–4 sentence assessment, then a prioritized finding set. Include `surface/viewport`, before-state observation, classifier category, principles and source URL, actionable diff/pattern, verification, outstanding UX/WCAG evidence. If asked for a style direction, give bounded alternatives with explicit tradeoffs rather than invented brand rules.

See `references/review-checklist.md` for a systematic review matrix and an output template.

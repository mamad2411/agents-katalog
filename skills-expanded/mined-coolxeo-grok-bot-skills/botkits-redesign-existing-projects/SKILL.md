---
name: botkits-redesign-existing-projects
description: >-
  Use when improving the design of a site or app that already exists. Audits the
  live pages, ranks the problems by impact, and fixes them in small reviewable
  steps on the current stack without breaking features.
---
# Redesign existing projects

Make an existing site look and work better without starting over. Keep the stack, the features, and what users already rely on.

## 1. Before touching code

- Ask, or infer and state: what is the page supposed to make people do, and what must not change (brand colors, logo, a flow customers know)?
- Read the code: framework, styling method and version (Tailwind 3 or 4, CSS modules, plain CSS), component library, and design tokens if any.
- Screenshot the key pages at mobile and desktop widths. These are the "before".

## 2. Audit

Walk each page and note problems with a screenshot or line reference:

- **Hierarchy:** is the main action the most visible thing? Can you tell what the page is in five seconds?
- **Type:** too many sizes or families, weak scale, lines too long, poor contrast.
- **Color:** clashing or oversaturated colors, accent used everywhere, gray text that fails contrast.
- **Layout and spacing:** no grid, uneven padding, inconsistent max-widths, things that don't align.
- **States:** missing hover, focus, active, loading, empty, and error states.
- **Feedback and control:** users can't tell what happened after a click, can't undo, or get stuck.
- **Accessibility:** keyboard access, visible focus, alt text, labels on inputs, WCAG AA contrast, reduced motion.
- **Template tells:** identical cards everywhere, generic hero, stock testimonials, filler copy (run copy through botkits-no-ai-slop).
- **Code:** one-off magic numbers, `!important` piles, `transition: all`, duplicate components.

## 3. Rank

Score each problem by user impact and effort, then fix in that order. Problems that block the main action or fail accessibility come first, whatever their size. Share the ranked list before starting if the changes are large.

## 4. Fix in small steps

- One theme per commit or PR (for example "type scale", "button states"), so each can be reviewed and reverted alone.
- Work inside the current stack. No framework migrations, no new UI library unless the user agrees. Check the dependency file before importing anything.
- Move repeated values into tokens or variables as you go.
- Run the app and its tests after each step. Nothing that worked before may break.

## 5. Show the difference

Take "after" screenshots at the same widths and pair them with the "before" set. List what changed, what you deliberately left alone, and anything that needs the user's decision (new imagery, copy, brand changes).

## Inspired by

- [Leon Lin, Taste Skill redesign-skill](https://github.com/Leonxlnx/taste-skill/tree/main/skills/redesign-skill) (MIT). Does well: scan, diagnose, fix on the existing stack, with a list of what generated designs usually forget. Missing: no before and after screenshots, almost nothing on accessibility, and a fixed priority list that opens with a font swap whatever the goal.
- [Nielsen Norman Group, 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/). Does well: system status, user control, consistency, and error prevention as a lens for auditing. Missing: no visual design or code guidance.
- [Vercel, Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines) (MIT). Does well: concrete checks for focus, keyboard, forms, motion, and layout. Missing: a checklist, with no process for ranking or rolling out fixes.

## What this version adds

- Goal and "must not change" questions before the audit.
- Before and after screenshots as the deliverable.
- Impact-by-effort ranking instead of a fixed order, with accessibility treated as a blocker.
- One theme per commit so each change can be reviewed and reverted.

---
name: ux-first-principles
description: "Apply the foundational reasoning of a senior UI/UX designer to interface decisions, BEFORE and WHILE generating UI, not just styling it afterward. This is design first principles (visual hierarchy, cognitive load, Gestalt grouping, usability heuristics, accessibility), the why behind good design, not execution (color, fonts, spacing, brand, component libraries). USE FOR: 'design a screen for', 'lay out this dashboard', 'what navigation should this app use', 'is this UI any good', 'structure this form', 'reduce clutter', 'make this clearer', grouping and prioritizing elements, choosing a flow or affordance. DO NOT USE FOR: picking colors, fonts, spacing scales, or brand systems (use a styling/execution skill); medium-specific layout (use ux-desktop, ux-tablet, or ux-mobile)."
---

# UX First Principles

A reasoning skill, not a styling skill. Its job is to make interface decisions the way an experienced UI/UX professional would: by drawing on the established canons of design knowledge to choose *what* to build and *why*, leaving *how it looks* (tokens, color, type, brand) to execution skills that run alongside this one.

## What this skill is for

Use this when a design decision is being made — not when colors are being picked. Good triggers:

- Laying out a screen, dashboard, form, or flow
- Choosing a navigation structure (tabs, drawer, sidebar, breadcrumb, wizard)
- Deciding how much to show at once vs. defer (disclosure, density)
- Grouping, ordering, and prioritizing elements on a surface
- Reviewing or critiquing an existing interface
- Resolving a "this feels cluttered / confusing / off" complaint into specific, fixable causes

If the task is purely "apply our color tokens" or "match the brand," that is execution — defer to the styling skill. This skill stops at the decision; it does not own the pixels.

## The one rule that prevents the most damage

**Principles are universal; their *application* changes by medium (desktop / tablet / mobile), not by platform (iOS / Android / Windows).** Human cognition and perception do not change across operating systems. What changes is the body-to-device interface: what the user points with, how far they can reach, how much they can see, and how many things they can have open. Reason from principles, decide once, and let a thin render-time layer handle mechanical platform substitutions (exact control sizing, system fonts, corner radii, OS-global gestures). Do **not** fork a structural decision (tabs vs. drawer, modal vs. inspector, navigation depth) by platform — those are driven by information architecture and cognition, and the cross-platform overlap of acceptable patterns is wide. Forking them fragments one coherent design into three divergent ones.

When the medium matters to the decision, consult the matching medium skill (`ux-desktop`, `ux-tablet`, `ux-mobile`). This core skill holds the invariant principles; the medium skills hold only what changes by modality.

## How to use the principles

Do not recite all of them. The skilled move is to identify which *few* principles bear on the decision in front of you, name the tension between them, and resolve it deliberately. Most real decisions are a trade-off between two or three principles (e.g., "show everything" for discoverability vs. "show less" for cognitive load). State the trade-off, then choose, and say why.

Workflow for any UI decision:

1. **Name the decision.** What exactly is being chosen? (a layout, a flow, an affordance, a grouping…)
2. **Pull the 2–4 relevant principles.** Use the taxonomy below to find them. Don't over-pull.
3. **Surface the tension.** Which principles pull in opposite directions here?
4. **Decide and justify.** Commit to one answer. Explain the reasoning in one or two sentences a designer would recognize.
5. **Check the medium.** If sizing, reach, density, hover, multi-window, or pointer precision affect the choice, consult the relevant medium skill.
6. **Check accessibility.** Treat it as a constraint on the decision, not a later patch.

## The four buckets (taxonomy)

The canons overlap, so they are organized by *what kind of question they answer*. Read the reference file for the bucket your decision touches.

- **Laws & effects — `references/laws-and-effects.md`**
  Descriptive: *why users behave as they do.* Fitts, Hick, Miller, Jakob, Tesler, Aesthetic-Usability, Doherty, Goal-Gradient, Peak-End, Serial Position, Von Restorff, Zeigarnik. Reach for these when reasoning about speed, choice, memory, expectation, and perceived quality.

- **Heuristics & principles — `references/heuristics-and-principles.md`**
  Normative: *what to aim for.* Nielsen's 10 usability heuristics, Shneiderman's 8 golden rules, Norman's principles (affordances, signifiers, mapping, feedback, constraints). Reach for these when reasoning about usability, error prevention, control, and whether the interface communicates how it works.

- **Compositional & perceptual — `references/compositional-and-perceptual.md`**
  How the eye organizes a surface: visual hierarchy, contrast, proximity, alignment, similarity, common region, figure/ground, progressive disclosure, consistency. Reach for these when reasoning about layout, grouping, emphasis, and "what does the user see first."

- **Accessibility & ethics — `references/accessibility-and-ethics.md`**
  Constraints that make the design usable by everyone and honest: WCAG's POUR (perceivable, operable, understandable, robust), inclusive-design defaults, and dark-pattern avoidance. Reach for these on every decision — accessibility is a design input, not an audit.

## Output expectations

When you apply this skill, make the reasoning visible but brief. A good response names the principles in play, states the trade-off, and commits to a choice — it does not dump a glossary. The user should come away understanding *why* the interface is the way it is, in terms a designer would endorse.

## What this skill deliberately does not do

It does not pick colors, fonts, spacing scales, or component libraries; it does not enforce a brand; it does not generate final styled markup on its own. Those are execution concerns owned by styling skills (e.g., a `frontend-design` skill) that should run alongside this one. Keeping the boundary clean is what lets this skill compose instead of conflict.

## Attribution note

The principle *concepts* referenced here (Fitts's Law, Hick's Law, Nielsen's heuristics, Gestalt principles, etc.) are part of the public HCI and design literature and are described here in original wording. Where a specific published collection is the best further reading — notably Jon Yablonski's *Laws of UX* (lawsofux.com), which is licensed CC BY-NC-ND and must not be copied verbatim — it is cited as a reference, not reproduced. Credit Jakob Nielsen / Nielsen Norman Group for the usability heuristics when reusing them.

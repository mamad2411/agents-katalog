---
name: frontend-craft
description: Design and build professional, distinctive web frontends, and avoid or remove generic AI-generated design ("slop"). Use this skill whenever creating or styling any web UI, including websites, landing pages, dashboards, web apps, React or Vue components, HTML/CSS pages, artifacts, prototypes, and email templates. Also use it when auditing, unslopping, reviewing, or restyling an existing frontend or codebase, when a design looks generic, templated, or AI-generated, or when the user asks to make something look better, more polished, or more professional, even if they never say the word design or slop. Covers design direction, typography, color, layout, spacing, motion, copy tone, accessibility, and a final anti-slop audit, for new builds and for retrofitting existing frontends.
---

# Frontend Craft

AI-generated frontends look alike because models reach for statistically safe defaults: the same fonts, the same purple CTA, the same three identical feature cards. People recognize the result instantly and call it slop. This skill is the countermeasure.

Three facts drive everything below.

**Slop is the absence of decisions, not a particular style.** Every visual choice should be one you can explain in terms of this product and this audience. A choice you cannot explain is a default someone else set.

**The tells migrate.** The 2022 default was purple gradients, glassmorphism, and neon glows on near-black. The 2026 default is warm cream, an editorial serif, and tasteful restraint. Both read as generated for the same reason: nobody decided. Avoiding a fixed list is not the goal. Deciding is.

**Density is the signal.** Automated slop detectors score a page by counting tells: 1-2 is treated as a pass, 3-4 reads as templated, 5 or more is heavy slop. One purple button is not a crime. A purple button plus glass cards plus a stat row plus an eyebrow pill plus a FAQ accordion is a template.

## Workflow

Two entry points, same rules underneath. A blank page needs a direction decided from scratch; a live codebase already has one (good, bad, or accidental) that has to be found before it can be fixed. Pick the path that matches the task.

### Building from scratch

### 1. Read the brief

Work out three things before any code:

- **Purpose and audience.** Who uses this, to do what? A procurement panel, a design-conscious consumer, and a developer skimming docs need different things. The audience picks the aesthetic, not your taste.
- **Surface type.** Brand surface (landing page, portfolio, campaign): the impression is the product, so distinctive type and bold moves earn their keep. Product surface (app UI, dashboard, admin): design serves the task, so density, semantic states, and repeatable components matter more than flourish. Landing-page decoration on a dashboard is its own kind of slop.
- **Constraints.** Existing brand assets, framework, accessibility needs, regulated or trust-first contexts (government, finance, health). These override aesthetic preference.

### 2. Commit to a direction and say it

Before writing code, state the direction in one or two sentences: the aesthetic, the typeface, the palette anchor, and one thing you are deliberately avoiding. For example: "Developer-tool landing page for a technical audience: IBM Plex Mono paired with a grotesque, paper-white background, one saturated signal color, dense and editorial. No gradients, no glass."

Stating it forces a real decision and makes the choice inspectable. If the brief genuinely splits between two directions, ask one question. Otherwise decide and proceed.

Draw the direction from the product's own world: a terminal, a lab notebook, a transit map, a specific era, an IDE theme, a cultural aesthetic. Not from "SaaS landing page" as a genre. And vary between generations: if your last design was cream-and-serif editorial, reaching for it again is the same reflex as reaching for purple.

### 3. Define the system before the pages

Set tokens as CSS variables first: palette, type scale, spacing scale, radius scale, shadow scale. Consistent tokens read as intent; ad hoc values read as generated. Read `references/design-foundations.md` for how to build each scale and the visual principles behind them (hierarchy, balance, contrast, Gestalt grouping).

### 4. Implement with craft

Interfaces succeed because of hundreds of small choices: focus states, hit targets, loading timing, form behavior, motion physics. Read `references/craft-checklist.md` before building anything interactive and treat it as the implementation bar.

### 5. Audit before delivering

Sweep the result against `references/slop-tells.md` and the quick check below. Then check the things code never shows you: you do not see your own render, so composition bugs (borders dying at rounded corners, non-concentric nested radii, monotone spacing) are invisible in source and glaring on screen. If you can render a screenshot, look at it. Subtract before you polish: slop is what piles up, so remove elements until everything left has to be there.

### Unslopping an existing frontend

Different failure mode than a blank canvas: there is already a live codebase with real content, real functionality, and existing patterns, some deliberate and some accidental. A full rebuild wastes the parts that already work and risks breaking what does. Work with what's there instead of replacing it.

### 1. Inventory before touching anything

Find the existing tokens (CSS variables, Tailwind config, theme file), the component library, and whatever conventions are already in use. Read enough to know which pattern is dominant, so a fix reinforces it instead of forking a second design language next to the first.

### 2. Audit against the same catalog, screen by screen

Sweep each screen against `references/slop-tells.md` and the quick tell check below. For a product surface (app, dashboard), also run `references/craft-checklist.md`: a live UI's problem is as often broken focus states, inconsistent hit targets, or missing loading states as it is a visual tell. Render it; don't just read the JSX or CSS, since composition bugs and tell density are invisible in source. List concrete hits (file, line, what it is), not general impressions, and count density per screen: 1-2 is fine, 5+ marks that screen as the priority.

### 3. Diagnose the shape of the problem before fixing it

Usually one of:

- A real direction exists but is applied inconsistently (three different card radii, two icon styles, a spacing scale that's almost followed). The common case: extend and enforce what's already there. Do not replace it with a new direction.
- No real direction exists — the "system" is untouched framework defaults (default Tailwind palette, Inter, default shadow scale) applied everywhere. This is effectively a fresh call, so apply "Commit to a direction" and "Define the system" above, but retrofit the result onto the existing structure rather than rewriting the codebase around it.
- Both at once. Fix one dimension at a time (color, then type, then spacing) rather than redeciding everything in a single sweeping edit.

### 4. Fix at the root, not per instance

If the same purple sits on twelve buttons, change the variable once, not twelve class names. Consolidate scattered ad hoc values into the token scale that already exists; only add a new token when the fix genuinely needs one.

### 5. Match the blast radius to the ask

"This card looks off" means fix that card and its siblings, not the app. "This looks generic, make it better" at the page or app level justifies a fuller pass. Don't turn a targeted fix into a redesign, and don't touch copy, structure, or functionality that wasn't part of the complaint.

### 6. Re-audit and verify nothing broke

Re-run the tell check on what changed. Confirm existing behavior, responsive breakpoints, and any tests still pass — a de-slop pass that regresses functionality is not a win.

## Rules by dimension

**Typography.** Pick the typeface the way you would pick a logo: deliberately, for this product, and be able to say why. Never default to Inter, Roboto, Arial, Open Sans, Lato, or system sans. Also do not "fix" that by grabbing the current trend rotation (Space Grotesk, Instrument Serif, Fraunces, Geist, Syne): those are good faces that became tells precisely because every generator reaches for them. Pair with contrast (display plus mono, serif plus geometric sans) and use extremes: weights 100-200 against 800-900 beat 400 against 600, display sizes 3x body beat 1.5x. Keep one voice per headline: no single word swapped to an italic serif or a different color. Body text at least 16px, line height 1.4-1.65, lines 45-75 characters.

**Color.** Commit to one palette and encode it in CSS variables. Dominant color plus a sharp accent beats an evenly distributed rainbow. Derive semantic colors (success, error, warning) from your palette instead of stock Tailwind blue/amber/green/red boxes. Text is always a solid color, never gradient-clipped. Meet contrast floors (4.5:1 body, 3:1 large text), temper pure black on pure white, and never encode meaning in color alone. Dark themes must be earned by the context, not the default, and dark-theme body text needs to stay readable, around 7:1, not mid-grey on black.

**Layout and hierarchy.** One thing is the most important thing: make it unmistakably biggest and place it deliberately. Use at most 3 sizes per composition and 2-3 type sizes for hierarchy. Group by proximity: related elements tight, unrelated groups far apart, with real jumps in the spacing scale. One shared gap everywhere means nothing belongs to anything. One surface per region: no cards inside cards, group with spacing and hairline dividers instead. Reading order must match visual order.

**Components and effects.** Decoration must carry information. An icon, badge, glow, callout, or glass panel earns its place by meaning something, or it goes. Keep one small radius scale and nest radii concentrically (inner radius = outer radius minus the gap). Shadows are neutral, layered, and smaller than the element casting them; a tinted glow is not depth. Put border and border-radius on the same element so the stroke follows the arc.

**Motion.** Motion is information: animate to show cause and effect, not to decorate. Transition only the properties that change (opacity, transform, color) at 120-200ms with an ease-out curve; never `transition: all`, and save springs for things that physically move. One well-orchestrated entrance with staggered reveals beats scattered hover tricks. Honor `prefers-reduced-motion`.

**Copy.** Specific beats loud. Real numbers are odd and checkable ("cuts build time 38%"); invented ones repeat everywhere ("10K+ users, 99.9% uptime, 24/7"). Ban the AI cadence: "It's not just X, it's Y", "Say goodbye to", punchy triads, buzzwords (streamline, empower, supercharge, world-class, enterprise-grade). No emoji as decoration. Error messages state the fix, not just the failure.

## Quick tell check

Frequencies from a deterministic scan of 1,590 Show HN landing pages. Run this list against every page you produce:

1. Gradient backgrounds or gradient-clipped headline text (30% of sites)
2. Permanent dark theme with muted grey body text (30%)
3. One hero word set apart in a serif italic, second font, or accent color (22%)
4. Numbered 1-2-3 "how it works" step cards (21%)
5. Pill badge or uppercase eyebrow floating above the H1 (21%)
6. Generic FAQ accordion at the bottom of the page (21%)
7. Centered hero set in Inter or a generic system sans (19%)
8. Trend display font as page default: Space Grotesk, Instrument Serif, Fraunces, Geist, Syne (12%)
9. Glassmorphism panels as decoration (12%)
10. Saturated colored glow box-shadows (7%)
11. Indigo/violet default accent on CTAs (7%)
12. Colored stripe on a card's left or top edge (6%, but called "almost as reliable a sign of AI design as em dashes in text")
13. Invented stat banner row (6%)
14. Emoji as nav or feature icons (3%)

A hit is not automatically a failure. It is a prompt to ask: did I choose this for a reason I can say out loud? If yes, keep it. If it is there because that is what landing pages look like, cut it. Full catalog with fixes: `references/slop-tells.md`.

## References

- `references/slop-tells.md`: the full merged catalog of AI-design tells with fixes, organized by category. Read it for the pre-delivery audit and whenever asked to de-slop an existing design.
- `references/craft-checklist.md`: interaction, form, motion, content, accessibility, and performance rules with exact values. Read it before implementing interactive UI, and as an audit checklist when unslopping an existing product surface.
- `references/design-foundations.md`: visual design principles and how to build the type, color, spacing, and motion systems. Read it when establishing the design system for anything new, or reconstructing one that's missing or applied inconsistently in an existing codebase.

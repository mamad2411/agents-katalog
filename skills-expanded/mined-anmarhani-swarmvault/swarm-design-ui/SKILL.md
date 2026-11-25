---
name: swarm-design-ui
description: UI/UX design phase — propose an intentional design system (pattern, brand, color, typography, spacing, atomic components) with the user, offering distinct directions and per-page layout options, for any interface type: Web, Mobile, Desktop, TUI, or CLI. Use when the SRS declares a user interface, when defining a design system or visual identity, choosing layouts, or reviewing UI work against UX laws.
---

# swarm-design-ui — UI/UX design phase

**Gate:** validated SRS declaring a user interface. Runs alongside swarm-design.
The goal is intentional, consistent design decided *with* the user — not templated defaults.

**Load only what you need** (token economy): the per-interface reference for the type at hand
(`references/web.md`, `references/mobile.md`, `references/desktop.md`, `references/tui-cli.md`),
and — for graphical UIs — `references/style-menu.md`, the on-demand catalog of product
categories, style families, layout patterns, and design resources (checklist.design, UX laws,
color/type/psychology tools).

## 1. Interview first

Audience and context of use; brand personality; platform conventions to honor; accessibility
requirements; existing brand assets. Keep it light and options-first — the point is to
understand the product, not to quiz.

## 2. Propose a design system (offer ≥2 directions)

Don't jump to one look. Using the product's category and personality (see
`references/style-menu.md` for the vocabulary), synthesize a **recommended design system** and
at least **one distinct alternative** — e.g. "clinical precision" vs "warm craft" — so the user
chooses with something concrete in front of them. Present each as a compact panel:

```
DESIGN SYSTEM — <recommended | alternative>
  Pattern/layout : <e.g. Hero-centric + social proof>   why: <conversion/trust rationale>
  Style          : <e.g. Soft UI evolution>             best for: <fit>
  Colors         : primary / surface / accent / semantic / bg / text  (WCAG-AA checked)
  Typography     : <display / body pairing>             mood: <…>
  Effects        : <shadows, motion timing, hover>
  Avoid          : <anti-patterns for this domain — see style-menu>
```

The style/category menu is a **guide, not a cage**: if the product's needs point elsewhere,
design for them. Resolve the picked direction into the tokens below.

## 3. Produce the design-system doc (`docs/design-ui.md`)

Everything as **tokens and scales**, never per-screen ad-hoc values:

1. **Color** — palette with roles (background/surface/primary/accent/semantic), light +
   dark, WCAG-AA contrast checked.
2. **Typography** — 1–2 families, a modular size scale, line-height and weight rules.
3. **Spacing & box model** — one spacing scale (e.g. 4px base), consistent
   margin/border/padding discipline, grid + auto-layout container rules.
4. **Atomic inventory** — atoms → components → templates → pages; every screen implied by
   an FR appears here, traced to its FR-ID. Use the *correct component names*
   ([namethatui.com](https://namethatui.com) is the dictionary): "drawer", "segmented
   control", "combobox" — not "that sliding panel". Precise names in specs and tickets mean
   every agent builds the same thing; resolve vague descriptions to the proper name and confirm.
5. **Per-page layout** — for each key screen, offer a couple of layout options
   (`references/style-menu.md` lists landing-page and dashboard patterns) and record the choice
   with its rationale, not just a single default.
6. **Responsive rules** — breakpoints, and a genuinely distinct mobile design where the
   SRS calls for mobile (not a shrunken desktop).
7. **Motion & interaction** — states (hover/focus/active/disabled/loading/error), timing.
8. **Voice** — the design system is half the identity; how the product *sounds* is the other
   half. Every string in the inventory (labels, errors, empty states, tooltips, onboarding)
   goes through **swarm-write**, against the project's `voice.md`. Copy is interface, not
   decoration applied afterwards.

## 4. Review against the UX-laws checklist (apply as review, not jargon)

Fitts (targets big and near) · Hick (fewer choices at decision points) · Jakob (follow
platform conventions) · Miller (chunk information) · proximity/common-region (group
related things) · Doherty (feedback < 400 ms) · error prevention over error messages. Run the
pre-delivery checklist in `references/style-menu.md` before calling UI work done.

## Rules

- Accessibility is explicit for graphical UIs: contrast ratios, focus order, touch
  targets, reduced-motion.
- TUI/CLI projects: skip all graphical guidance and the style menu; help text, flags, exit
  codes, and error style ARE the design (see `references/tui-cli.md`).
- End with user validation (gated) or FR-coverage self-check (auto); update flow-state.

---
*Influences: Laws of UX (Yablonski); Atomic Design (Frost); roadmap.sh/design-system;
checklist.design; Figma typography guide; NameThatUI (component vocabulary); Anthropic
frontend-design skill — see CREDITS.md.*

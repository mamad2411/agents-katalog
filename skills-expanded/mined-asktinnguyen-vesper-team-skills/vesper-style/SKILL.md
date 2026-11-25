---
name: vesper-style
description: Use when designing, reviewing, or implementing Vesper UI so the result feels warm, document-centric, tactile, contrast-safe, and human-led rather than generic SaaS or flashy AI.
version: 1.0.0
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# Vesper Style

The canonical UI design brain for **Vesper**.

This skill does **not** just apply a visual skin. It helps the agent make better product and implementation decisions so Vesper surfaces stay:
- **classy**
- **tactile**
- **responsive**
- **calm under complexity**
- **premium without spectacle**
- **human-led even when the product is deeply agentic**

Use this skill to translate rough ideas, borrowed references, or existing implementations into something that genuinely feels like **Vesper**.

## When to use

Use this skill when the task is about any of the following:
- designing a new Vesper page, panel, or workflow
- making an interface “feel like Vesper”
- translating generic SaaS or shadcn-style UI into Vesper’s language
- fixing clutter, weak hierarchy, or dashboard overload
- reviewing light-mode contrast, chip readability, or semantic color usage
- choosing the right Vesper layout, headers, actions, and progressive disclosure model
- mapping design intent onto Vesper’s existing tokens and shared primitives

## Do not use this skill when

- the task is for a different brand with a conflicting visual identity
- the user wants a literal clone of another product’s styling
- the work is purely backend or invisible infrastructure with no UI/design decision surface
- a tiny local bug fix has no meaningful design implication

## Frame the surface first

Before designing or critiquing, write exactly these three lines:

```text
Audience: <who this Vesper surface is for>
Primary action: <the single most important thing the user should do>
Mandatory sections: <section 1>, <section 2>, <section 3>
```

If those lines are fuzzy, the design is not ready.

## Core truths of Vesper UI

1. **Orientation is a product feature.** The user should quickly understand where they are, what is happening, and what matters next.
2. **Human intent stays primary.** Agents can be powerful, but the interface should keep the user feeling directed, not displaced.
3. **Warm editorial beats control-room spectacle.** Favor readable work surfaces over gadget-heavy dashboards.
4. **Progressive disclosure beats control overload.** Show the next best action clearly; tuck advanced controls behind calmer layers.
5. **Light mode is first-class.** Never accept washed-out surfaces, weak borders, or tiny low-contrast tinted text.
6. **Fix the system before patching the leaf.** Repeated styling problems belong in shared tokens or shared primitives.
7. **Restraint is part of the brand.** One strong idea per surface is better than five decorative flourishes.

## Workflow

### 1. Ground the work in Vesper, not in taste
Read these references before making meaningful UI decisions:
- `references/brand-foundation.md`
- `references/tokens.md`
- `references/layout-patterns.md`
- `references/components.md`

If the task includes copy, critique, or final quality review, also read as needed:
- `references/copy-and-tone.md`
- `references/anti-patterns.md`
- `references/review-checklist.md`

If the task includes implementation, also read:
- `references/implementation-mapping.md`

### 2. Define the primary action
Identify:
- what the user came here to do
- what state they need to understand first
- which controls are truly primary vs secondary vs tertiary

If everything is equally visible, the design is probably wrong.

### 3. Choose the Vesper structure
Default to the lightest pattern that preserves orientation:
- three-pane working model
- list-detail management layout
- document/work surface with a quiet companion rail
- compact panel header with a single obvious primary action

### 4. Apply Vesper visual language
Use the token and component references to enforce:
- warm editorial surfaces
- compact but readable headers
- strong typographic hierarchy
- neutral, readable chip text
- subtle depth and tactile states
- restrained semantic color

### 5. Validate both themes
Always check:
- light mode readability first if the surface uses chips, borders, tints, or muted metadata
- dark mode elegance and session-length comfort
- reduced-motion friendliness
- color is not the only carrier of meaning

### 6. If coding, map design intent to the real system
Do not improvise new primitives before checking the shared ones.
Use `references/implementation-mapping.md` to decide whether the change belongs in:
- global theme tokens
- shared controls
- shared panel/header primitives
- shared chip/badge recipes
- a leaf component only as a last mile refinement

## Routing guide

| Need | Read |
|---|---|
| Product posture, user feeling, brand guardrails | `references/brand-foundation.md` |
| Color, typography, spacing, surfaces, motion | `references/tokens.md` |
| Page structure, hierarchy, disclosure, layout families | `references/layout-patterns.md` |
| Panels, buttons, chips, fields, menus, callouts, empty states | `references/components.md` |
| UX writing, labels, empty states, and system voice | `references/copy-and-tone.md` |
| Hard rejects and drift checks | `references/anti-patterns.md` |
| Final review and polish rubric | `references/review-checklist.md` |
| Repo-grounded implementation targets and code touchpoints | `references/implementation-mapping.md` |

## Non-negotiables

- Keep small text **neutral and high-contrast** on tinted surfaces.
- Avoid stacked translucency in light mode unless scenic mode is explicitly intended.
- Prefer **document-centric composition** over dashboard sprawl.
- Use motion to confirm state change, not to perform personality.
- Make advanced capability feel **available**, not **demanded**.
- Keep actions legible and hierarchy obvious within the first few seconds.
- Reuse the semantic system instead of inventing ad-hoc accent palettes.

## Anti-patterns

Do not push Vesper toward:
- cyberpunk or hacker-terminal styling
- neon gradients as the primary identity layer
- dense toolbelt headers with many equal-weight controls
- rainbow badges
- same-hue text on same-hue semantic chips
- gloomy dark mode or washed-out light mode
- excessive rounding that makes the product feel playful instead of precise
- novelty animation that adds spectacle but reduces trust or clarity

## Output contract

When presenting a design or review result, organize it like this:

```text
Frame:
- audience
- primary action
- mandatory sections

Hierarchy:
- what is primary
- what is secondary
- what is hidden until needed

Surface and tone:
- light mode treatment
- dark mode treatment
- color/contrast decisions

Component decisions:
- headers
- actions
- chips/badges
- forms/lists/panels

Implementation notes:
- shared tokens/primitives to reuse or adjust
- leaf components to touch only if necessary

Risk check:
- light-mode contrast
- progressive disclosure
- color-only meaning
- control overload
```

## Success criteria

This skill is working when:
- the UI feels recognizably like Vesper rather than like a dressed-up demo
- the user feels more oriented and more capable, not more impressed-but-confused
- the primary action becomes easier to spot quickly
- semantic color becomes clearer and more disciplined
- light mode gains clarity instead of losing personality
- implementation decisions get pushed toward shared tokens and primitives when patterns repeat

## Final reminder

**Vesper style is a product behavior system, not a decorative preset.**

The question is not:
> “How do we make this look premium?”

The question is:
> **“How would Vesper make this feel clear, calm, trustworthy, and powerfully human-directed?”**

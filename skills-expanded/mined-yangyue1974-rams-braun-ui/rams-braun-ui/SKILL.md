---
name: rams-braun-ui
description: Braun-era Dieter Rams visual design system for web/app UI. Produces interfaces that look and behave like Braun products (1955–1995) — warm-neutral chassis surfaces, a single functional accent color, all-lowercase labels, strict functional grouping, one global corner radius, matte flat surfaces. Use this skill whenever the user asks for Rams style, Braun style, "less but better", functionalist / Ulm-school design, German industrial minimalism, or wants a calm instrument-like interface — even if they only say "make it feel like a Braun product" or "拉姆斯风格". Applies to landing pages, dashboards, apps, and components generated in HTML/React.
---

# rams-braun-ui

This skill makes Claude design UI the way Braun's design department built products: the interface is an **instrument**, not a poster. Every visual decision below is reverse-engineered from Braun hardware (SK4, TP1, ET66, T3, TG60, regie 510) and Vitsoe 606, then translated to screen. Follow the numbers; they are what makes the result read as "Rams" instead of "generic minimal".

## The one-sentence physics of this style

A large calm neutral chassis; controls grouped by function on a strict grid; text is small, lowercase labeling, never a visual element; **exactly one accent color, bound to the single primary operation**; one small radius everywhere; matte, flat, mechanical.

## Build order (always in this sequence)

1. **Inventory & group.** List every piece of content/control. Group by *function* (what task it serves), not by visual similarity. Each group becomes a "zone" on the panel.
2. **Grid the zones.** Orthogonal layout only. Gap inside a zone = 8–12px; gap between zones = 24–32px (2–3× the inner gap). Outer margins ≥32px desktop / ≥20px mobile. This ratio IS the Braun look — get it wrong and nothing else saves it.
3. **Build entirely monochrome.** Use only the neutral tokens (see `references/tokens.md`). The design must fully work in monochrome: hierarchy from size, position, and grouping — never from color.
4. **Assign the accent.** Find the ONE primary operation of this view (play, save, submit, power). Give it the accent color. Nothing else on the view may carry chroma. If two things feel primary, the grouping is wrong — go back to step 1.
5. **Typography pass.** All UI labels, buttons, and nav: lowercase (`text-transform: lowercase`). Max 2 font sizes per zone, 3 per screen. Weights 400/500 only. Details in `references/tokens.md`.
6. **Subtraction pass.** Remove elements one at a time until removal breaks a function. Decorative dividers, redundant labels, icon+text pairs where one suffices — all go. Target ≤7 interactive elements per zone.
7. **QA against the checklist** in `references/checklist.md` (the ten principles, made checkable).

## Hard rules (non-negotiable)

- ≥95% of rendered surface area is neutral (chassis whites/greys/charcoal).
- One accent hue per view, only on the primary operation. Color = function signal, never decoration.
- Every control displays its current state at rest (slider position, toggle displacement, selected value visible). No hover-only affordances, no hidden gestures.
- One global corner radius (4px). Circles allowed only for genuinely circular 1:1 controls.
- No gradients, no glassmorphism, no shadow stacks, no bounce animation, no uppercase headings, no bold shouting. Full forbidden list: `references/anti-patterns.md`.

## Reference files

- `references/tokens.md` — colors (hex), type scale, spacing, radius, shadow, motion; includes a paste-ready CSS variables block. **Read before writing any code.**
- `references/components.md` — buttons, toggles, sliders, inputs, cards, nav, tables, icons: exact specs.
- `references/anti-patterns.md` — the forbidden list. Read when reviewing or when tempted.
- `references/checklist.md` — ten principles as a QA gate. Run at the end of every design.

## Scope note

This is the **homage** track: output should be recognizably Braun. It is still not skeuomorphism — never draw fake wood, fake speaker grilles, or dials that don't function as dials. The homage lives in the tokens and the discipline, not in props.

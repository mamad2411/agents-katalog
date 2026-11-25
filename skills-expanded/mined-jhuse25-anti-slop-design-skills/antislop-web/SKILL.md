---
name: antislop-web
description: "Use when building or reviewing any web UI so it does NOT look AI-generated. A bias-correction engine: bans the AI tells (Inter, neon purple, pure black, three identical cards, 'Elevate/Seamless', John Doe), sets VARIANCE/MOTION/DENSITY dials, forces required states (loading/empty/error) and performance guardrails, and requires one signature element. Generates a DESIGN.md source of truth per project. Stack-agnostic; no third-party services, no MCP."
license: MIT
tags: [frontend, design, ui, anti-slop, design-system]
---

# Anti-Slop Web — so nothing you ship looks AI-generated

Single goal: **remove the "AI tells"** that give away a generated UI. The problem with
vibe-coded interfaces is not that they fail to work, it is that they look generic (Inter
font, neon purple, three identical cards, "Elevate your workflow", John Doe). This skill
forces deterministic, premium decisions BEFORE you generate, and verifies them at the end.

It is not magic from any vendor: five bias-correction levers, all native to whatever stack
you already use, zero MCP and zero external service.

## When to use it

- At the start of a design phase: generate the project `DESIGN.md` (Part A) before writing
  components.
- While building or refactoring any screen/section: apply the directives (Part B) as
  generation rules.
- In your quality/a11y gate before commit: run the pre-flight (Part C).

## When NOT to use it

- It does not replace the client's brand. The `DESIGN.md` it generates is re-tokenized to
  the client's palette/typography. This skill gives the DISCIPLINE (what to ban, what to
  force); the client gives the BRAND.
- It does not replace your gates. It complements a11y checks, security/code review before
  commit, and your dependency manifest.

## Stack integration (how it runs)

This skill is stack-agnostic. Wherever it names a tool, treat it as an example and map it
to your stack:

- **Animation, lightest tier that achieves the effect:** CSS-only (e.g. `tw-animate-css`,
  0 JS) -> native scroll-reveal (`animation-timeline: view()`) -> a JS animation lib
  (e.g. Framer Motion) -> a scroll library (e.g. GSAP ScrollTrigger) -> canvas/WebGL
  (Three.js). Never add a library that duplicates a tier you already have.
- **Components:** a customized component system (never the untouched default) plus animated
  components only for punctuated motion (ingredient, not product).
- **Icons:** a single consistent icon set (e.g. Phosphor, Radix). Never emojis. Never the
  generic "egg" SVG or the default user-icon as an avatar.
- **Re-tokenization is mandatory:** every output is carried to the client's brand. A client
  should never be able to trace their site back to a template or a recognizable default.

---

# PART A — DESIGN.md generator (per-project source of truth)

Generate a `DESIGN.md` at the project root. It is the single source of truth for visual
identity and bans. Every component is generated against this file.

## A.1 Dials (translate "make it nice" into rules)

Set three values 1-10. Suggested baseline: **VARIANCE 7, MOTION 5, DENSITY 4** (tuned for
conversion and a11y over showing off). Adjust to the brief, not the other way around.

- **VARIANCE** (symmetry 1 <-> artistic chaos 10): controls layout. >4 bans centered heroes
  (forces split/asymmetric).
- **MOTION** (static 1 <-> cinematic choreography 10): >5 enables perpetual micro-interactions
  and spring physics. Always under `prefers-reduced-motion`.
- **DENSITY** (airy gallery 1 <-> data cockpit 10): >7 bans generic cards (use `border-t`/
  `divide-y`/negative space) and forces monospace on numbers.

## A.2 Palette (color bans)

Each color: **descriptive name + hex + functional role**.

- One accent maximum. Saturation < 80%.
- BAN "AI purple/blue neon": no purple glows, no neon gradients.
- Absolute neutral bases (Zinc/Slate) + one singular high-contrast accent (Emerald, Electric
  Blue, Deep Rose, etc.). One palette; do not drift warm/cool.
- Never pure `#000000`: use off-black / Zinc-950 / charcoal.

## A.3 Typography (font bans)

- Display: tight tracking, controlled scale; hierarchy by weight and color, not giant size.
  No screaming H1s.
- Body: relaxed leading, max 65ch.
- BAN `Inter` for premium/creative contexts. Force character: `Geist`, `Outfit`,
  `Cabinet Grotesk`, `Satoshi`.
- Serif: banned in dashboards/software UI. If editorial and needed, only distinctive modern
  serifs (`Fraunces`, `Instrument Serif`, `Editorial New`).
- Dashboards: only sans pairs (`Geist` + `Geist Mono`, or `Satoshi` + `JetBrains Mono`).
- DENSITY > 7: all numbers in monospace.

## A.4 Components (states and materiality)

- Buttons: tactile feedback on `:active` (`-translate-y-[1px]` or `scale-[0.98]`). No outer
  glow. No custom cursors.
- Cards: only when elevation communicates hierarchy; tinted shadow toward the background. In
  high density, replace with `border-t` dividers or negative space.
- Inputs: label ABOVE, optional helper in markup, error BELOW. `gap-2`. Focus ring in the
  accent. No floating labels.
- Loaders: skeletons with the real layout dimensions. Never a generic circular spinner.
- Empty states: a composition that shows how to populate the data, not "No data".
- Error states: clear inline reporting.

## A.5 Layout

- No overlapping elements: each in its clean zone. No absolute stacking.
- VARIANCE > 4: centered hero BANNED -> 50/50 split, left-aligned + asset, or asymmetric
  whitespace.
- BAN "three identical cards in a row": use a 2-column zig-zag, an asymmetric grid, or
  horizontal scroll.
- CSS Grid over flex-math (`w-[calc(33%-1rem)]` banned). Contain with `max-w-[1400px]
  mx-auto` or `max-w-7xl`.
- Full-height: `min-h-[100dvh]`, NEVER `h-screen` (catastrophic jump in iOS Safari).

## A.6 Responsive (non-negotiable)

- Mobile-first collapse < 768px: every multi-column collapses to one. Zero horizontal scroll
  (critical failure).
- Headlines with `clamp()`. Body min `1rem`. Tap targets min 44px.
- Section gaps proportional: `clamp(3rem, 8vw, 6rem)`.

## A.7 Motion (under the right tier)

- Pick the lightest tier that works. Spring physics by default when a JS lib applies
  (`type:"spring", stiffness:100, damping:20`); no linear easing.
- Animate ONLY `transform` and `opacity`. Never `top/left/width/height`. Grain/noise only in
  `fixed pointer-events-none` pseudo-elements.
- Cascade reveals (stagger), do not mount lists all at once. Everything wrapped in
  `prefers-reduced-motion: no-preference` with content visible by default.

## A.8 Anti-patterns (the AI tells — encode as "NEVER" in DESIGN.md)

No emojis. No `Inter`. No generic serif. No `#000`. No glows/neon. No oversaturated accents.
No text gradient in big headers. No custom cursors. No overlaps. No three identical cards. No
generic names ("John Doe", "Acme", "Nexus"). No fake round numbers (`99.99%`, `50%`) ->
organic data (`47.2%`). No AI copy cliches ("Elevate", "Seamless", "Unleash", "Next-Gen") ->
concrete verbs. No broken Unsplash -> `picsum.photos/seed/<str>/800/600` or SVG avatars. No
filler ("Scroll to explore", bouncing chevrons).

## A.9 Signature element (the one AFFIRMATIVE rule — mandatory)

Everything above is prohibition: it stops the UI from looking generated. But a page can pass
EVERY ban and still be forgettable. Absence of tells is not the presence of character.

**Each project declares ONE signature element**: the thing the page is remembered for, the
thing a visitor describes without saying "a landing page". Just one. Two signatures = none.

Criteria (all three, or it is not a signature):
- **Memorable:** a visitor can describe it from memory a week later.
- **Owned:** it comes from the client's brand/business, not a catalog of effects. A
  `spotlight-border` added because it was on a list is NOT a signature; it is decoration.
- **Sustained:** it appears coherently (not one firework in the hero and nothing else).

It can live in any layer, it does not have to be motion:
- **Motion/scene:** a scroll-scrub hero, kinetic type, a physical reveal.
- **Materiality:** an owned photo treatment, grain/print, an anomalous border or radius.
- **Typography:** a display face with character used structurally, not decoratively.
- **Data/content:** one real piece of the business presented as nobody else in the sector
  presents it (the best kind: it cannot be copied without the business).
- **Interaction:** one unique gesture that does something useful, not a trick.

Guard: the signature is declared BEFORE building (it goes in `DESIGN.md`) and verified in the
pre-flight. If you cannot name it in one sentence, it does not exist. If it contradicts the
brief (a product that asks for restraint), the signature IS the restraint executed with rigor
-- say so explicitly.

## A.10 Output template (DESIGN.md)

```markdown
# Design System: [Project] — Client [X]

## 0. Dials
VARIANCE: n | MOTION: n | DENSITY: n   (baseline 7/5/4)

## 1. Atmosphere
[Mood, density, variance and motion in evocative but precise language.]

## 1b. Signature element (mandatory, exactly one)
**[Name in one sentence]** — [what it is, which layer it lives in (motion/materiality/
typography/data/interaction), and WHY it comes from this business and not a catalog.]
Sustained in: [where it recurs across the site].

## 2. Palette and roles
- **[Name]** (#XXXXXX) — [role]   (max 1 accent, sat < 80%, no neon, no #000)

## 3. Typography
- Display: [font] — tight tracking, hierarchy by weight
- Body: [font] — relaxed leading, 65ch
- Mono: [font] — numbers/metadata
- Banned: Inter (premium), serif in dashboards

## 4. Components
[Buttons / cards / inputs / loaders / empty / error — shape, shadow, states]

## 5. Layout
[Grid-first, asymmetric splits, collapse < 768px, max-width, min-h-[100dvh]]

## 6. Motion
[Chosen tier, spring, stagger, prefers-reduced-motion, transform/opacity only]

## 7. Anti-patterns (BANNED)
[Explicit list from A.8, adapted to the client]
```

---

# PART B — Engineering directives (bias correction while generating code)

Rules for writing real components. See `reference/design-vocabulary.md` for the Tailwind
"how".

1. **Verify dependencies [mandatory]:** before importing any library (animation lib, icons,
   etc.) check the manifest (`package.json`). If missing, emit the install command. Never
   assume it exists. Respect the framework/tailwind version lock (no v4 syntax in a v3
   project).
2. **Server-first, isolated interactivity:** static layout as server components. Every
   animation/global state lives in a client leaf. Global state only to avoid deep prop
   drilling, not arbitrarily.
3. **Deterministic typography:** display `text-4xl md:text-6xl tracking-tighter leading-none`;
   body `text-base leading-relaxed max-w-[65ch]` in a secondary color.
4. **Performance:** animate only `transform`/`opacity`; `will-change` sparingly; z-index only
   for systemic contexts (sticky navbars, modals, overlays), no `z-50` spam. Perpetual
   animations memoized and isolated in their own tiny client component; never re-render the
   parent.
5. **Credible data (anti "Jane Doe"):** realistic contextual names, credible avatars (stable
   placeholder photo or owned styling), organic numbers.
6. **External resources:** a customized component system ALWAYS (radii, colors, shadows);
   `picsum.photos` or SVG instead of Unsplash; icons with one consistent global `strokeWidth`
   (1.5 or 2.0).
7. **Creative arsenal (avoid the generic default):** when the brief asks for character, reach
   for premium patterns -- asymmetric hero with image fade, bento 2.0, magnetic button,
   split-screen scroll, kinetic type, spotlight-border card, sticky scroll stack. Hard rule:
   never mix a scroll/canvas library and a UI animation library in the same component tree;
   isolate the heavy one with strict cleanup in `useEffect`.

---

# PART C — Pre-flight (hooks into your quality/a11y gate before commit)

Before calling a UI done, verify. Any failure = not shippable until fixed.

- [ ] Zero A.8 AI tells (font, color, layout, copy, data, images).
- [ ] **Signature element (A.9) present, single, sustained.** Name it in one sentence without
      looking at the code. If it does not come out, or two come out, not shippable: the UI is
      correct but forgettable.
- [ ] Mobile collapse guaranteed (`w-full px-4`, `max-w-7xl mx-auto`); zero horizontal scroll.
- [ ] Full-height with `min-h-[100dvh]`, not `h-screen`.
- [ ] Loading / empty / error states present.
- [ ] Animations under `prefers-reduced-motion`, content visible by default, only
      `transform`/`opacity`, in the lightest possible tier.
- [ ] Animation `useEffect` has cleanup; perpetual ones isolated and memoized.
- [ ] Everything re-tokenized to the CLIENT brand (no component-system default).
- [ ] Source/license of any template or component recorded in the project.

## Limitations

- It gives design discipline, not guaranteed conversion: the brief and the client's content
  rule. "Premium" wrongly applied to a product that asks for restraint is itself a tell.
- The values (fonts, patterns) are 2026 defaults; check them against the brand and the
  project's a11y before locking them in.

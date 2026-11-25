---
name: liquid-glass-claude-skill
description: Brand-agnostic design reasoning system for Liquid Glass and glassmorphic interfaces on any platform (web, SwiftUI, mobile). Use when asked to use, apply, or redesign with Liquid Glass, glassmorphism, frosted or translucent glass UI, or backdrop blur, or to make an interface more Apple-like or iOS 26 style.
---

# Liquid Glass Claude Skill

A design reasoning system, not a snippet library. Liquid Glass is a **material and interaction language**: translucent material used intentionally to establish functional hierarchy above content.

**Objective:** a clear, spatial, adaptive interface. Not "make it look like glass."
**Success test:** people think "this feels incredibly clean and spatial," never "someone added blur to everything." Liquid Glass should be felt before it is noticed.

This skill controls **material, hierarchy, spatial behavior, transparency, blur, depth, interaction.**
The project's brand system controls **color, type, identity, imagery, tone.** Never mix the two.

**References.** Primary: Apple's Liquid Glass principles (functional layering, translucency, material hierarchy, adaptive appearance, spatial separation, depth, continuity, visual hierarchy, clarity, consistency, contextual interaction). Supporting: glassmorphism practice on transparency, background blur, contrast, depth, edge definition, accessibility, readability. Understand the principles and apply them to the product at hand. Never produce an Apple clone.

---

## 0. Scope and safety

This skill is guidance only. When it is active:
- Work only inside the project the user has explicitly selected or shared. Do not read, scan, or modify anything outside it.
- Do not read environment variables, credentials, keys, tokens, or account data.
- Do not make network requests, install packages, or change global or system settings. When a technique needs a library, name it and let the user decide whether to add it.
- Do not overwrite existing files without the user's request. Propose first (section 3).
- Do not collect, store, or transmit user data. Example content must be fictional.
- Version-specific platform facts in section 14 can age. Flag them for the user to verify rather than fetching anything.

---

## 1. Command interpretation

| User says | Interpret as |
|---|---|
| "Use / apply / make it Liquid Glass", "Liquid Glass style" | Apply this system while preserving the product's existing brand and UX requirements. |
| "Make it glassmorphic", "glass UI" | Use glassmorphism techniques, governed by this system's hierarchy, restraint, and accessibility rules. |
| "Redesign this using Liquid Glass" | Run the full Initialization Protocol (section 3). Redesign the material layer, not unrelated UX. |
| "Make it more Apple-like" | Do NOT copy Apple UI. Increase spatial clarity, material hierarchy, restraint, typography quality, alignment, functional layering, interaction clarity. |

Never interpret any of these as: add `backdrop-filter: blur()`, make cards transparent, add rounded white glass cards, or add gradients and shadows.

---

## 2. Reality check on the reference (read before promising anything)

1. **Native vs web gap.** Apple's Liquid Glass is a native, GPU-rendered material: it *lenses* (bends light) rather than only blurring, carries specular highlights that respond to motion, and each component adapts light/dark to what is beneath it. CSS can convincingly reproduce blur, tint, edge light, and shadow. Refraction via SVG filters inside `backdrop-filter` renders in Chromium-based browsers only; Firefox and Safari do not apply SVG `url()` filters in `backdrop-filter`. On the web, refraction is progressive enhancement and must never be load-bearing for legibility or brand.
2. **Legibility is the known failure mode.** After public readability complaints, iOS 26.1 added a user setting (Clear or Tinted) that raises opacity and contrast. Default toward the more opaque, more legible side. Clear glass is the exception, not the baseline.
3. **Apple's stated usage rules** that this system adopts: glass belongs to the navigation layer that floats above content; do not stack glass on glass (use fills and transparency for separation inside a glass surface); tint only to emphasize primary actions; the clear variant is only for media-rich backgrounds, where a dimming layer is acceptable, and content on top is bold and bright.
4. **Do not overclaim.** When delivering, state plainly which effects are native, which are approximated, and which browsers or OS versions get the fallback.
5. **A filter inside `backdrop-filter` knows nothing about the element's shape.** It receives only the backdrop image, which is opaque everywhere. So refraction driven by `feTurbulence` is *uniform*: it wobbles the middle of a pane exactly as much as the rim, which reads as heat haze, not glass. Real lensing is edge-concentrated, and the only way to get it is to build a displacement map from the element's own outline (section 17.2). A "chromatic aberration" made by displacing R/G/B by different uniform amounts is not aberration, it is a desaturation pass; measured side by side, the filtered bar was visibly greyer.
6. **Blur over a flat backdrop is invisible.** Blurring a smooth gradient returns the same gradient. Pixel-diffing a card with the blur on and off over a soft page gradient gave a maximum channel difference of 3/255; the same diff on a bar with real content scrolling under it changed 60% of pixels. Glass needs something with structure behind it (content, an image, a deliberately placed glow), or the blur is pure cost.

---

## 3. Project Initialization Protocol (mandatory)

When this skill activates in a project, **do not modify the UI first.** Complete phases A to C, deliver the proposal, then implement. Skip only if the user explicitly says to go straight to implementation, and say what was skipped.

### Phase A: Inspect
Establish, from the selected project's code, files, and screenshots, or by asking the user:
- Product purpose and target users
- Platform(s) and framework(s); OS or browser support targets
- Information architecture and primary user flows
- Existing design system, component library, tokens
- Brand identity: color, typography, imagery, iconography, tone
- Spacing and radius systems (or their absence)
- Responsive behavior and breakpoints
- Accessibility requirements (target WCAG level and any accessibility laws that apply in the product's markets)
- Performance constraints (low-end devices, image-heavy pages)

If a fact cannot be determined, list it as an open question. Do not invent it.

### Phase B: Classify
Produce a layer map (section 4) and answer:
1. Which elements remain **content**
2. Which elements become **functional floating UI**
3. Which existing components should be **removed**
4. Which components should be **consolidated**
5. Where Liquid Glass **improves UX** (with the functional reason)
6. Where Liquid Glass would **make the experience worse** (with the reason)

### Phase C: Propose
Deliver, before any code or design changes:
- Layer map table: element, layer, glass yes/no, material tier, reason
- Material tiers and starting token values for this project
- Brand integration notes (what comes from the Project Brand System)
- Accessibility and fallback plan
- Performance budget (glass layers per view)
- Honest limitations (section 2)
- **Out of scope:** UX problems noticed but not part of the material change, listed separately and not fixed unless the user asks

**Scope rule:** never use Liquid Glass as an excuse to redesign unrelated UX. Consolidating or removing components is proposed, never done silently.

### No project brand yet
Create a **Project Brand System** first (section 12). Do not borrow a brand from another project.

---

## 4. The layer model

| Layer | What it is | Examples | Glass? |
|---|---|---|---|
| **1. Content** | What the user came for | Photography, artwork, products, editorial, illustration, video, maps, dashboards, documents | **No.** Content stays visually dominant. |
| **2. Structural UI** | How content is organized | Sections, grids, containers, typography, hierarchy | **No** by default. Solve with layout, spacing, type. |
| **3. Functional floating UI** | Controls acting on content | Navigation, search, filters, toolbars, contextual actions, floating buttons, menus, sheets, overlays | **Candidate.** Passes the gate question first. |

The interface should feel like it exists above the content, not like the content is made of glass.

### The gate question
Before applying glass to any element, answer: **"What functional role does this material communicate?"**
Valid answers: it floats above scrolling content; it is contextual and temporary; it must stay reachable while content moves beneath it; it needs separation without hiding context.
If there is no meaningful answer: **do not use glass.** Never add glass for decoration.

---

## 5. Material hierarchy

One glass treatment everywhere is a defect. Assign tiers by function.

| Tier | Use for | Starting fill opacity | Starting blur | Notes |
|---|---|---|---|---|
| **None** | Most content, artwork, product imagery, editorial images, page backgrounds, card grids | n/a | n/a | Default for Layers 1 and 2 |
| **Thin** | Icon-only or large-label controls, compact secondary actions, navigation over controlled backdrops | 0.35 to 0.50 | 16 to 20px | Body text not guaranteed legible (see note) |
| **Regular** | Navigation with text, toolbars, search fields, floating action groups, tab bars | 0.50 to 0.65 | 20 to 28px | Workhorse tier |
| **Thick** | Menus, popovers, sheets, dialogs, text-dense overlays | 0.65 to 0.85 | 24 to 32px | Readability outranks translucency |
| **Scrim** | Dimming behind modal sheets and dialogs | Solid tint 0.20 to 0.45 | 0 to 8px | Separates modal context |
| **Clear** (rare) | Controls over full-bleed media only | 0.15 to 0.30 | 12 to 20px | Requires dimming under it and bold, bright foreground |

All values are **starting points**, not rules. Tune against the actual backdrop (section 6).

**Contrast math (worst case, before blur):** a light fill (near #f5f5f7) with near-black text needs about **0.51 fill opacity** to hold 4.5:1 over a pure black backdrop, and about 0.40 for 3:1. A dark fill (near #16161a) with white text needs about **0.59** for 4.5:1 over pure white, and about 0.46 for 3:1. Blur averages extremes and usually helps in practice, but it is not a guarantee. Below those thresholds, restrict the surface to icons and large text, constrain what can pass beneath it, or raise the fill.

**Glass on glass:** inside a glass surface, separate sub-elements with subtle fills, dividers, or opacity changes. Never nest a second backdrop-blurred layer.

---

## 6. Material properties

### Transparency
- Contextual, never one global value. Decide per component from: backdrop complexity, contrast needs, component importance, light/dark context, accessibility.
- Test over the **worst-case backdrop**: busiest image region, lightest and darkest content that can scroll beneath it.

### Blur
- Purpose is material separation, not decoration.
- Increase blur with backdrop complexity and component size; decrease on small controls and on mobile.
- Never blur content itself.

### Saturation and filters
- Restrained: `saturate()` roughly 110 to 150%. Above 180% reads as candy.
- `brightness()` and `contrast()` adjustments within about ±10%, or none.
- The material stays calm; it may subtly pick up color from beneath.

### Tint
- Material base tint comes from the brand's neutral surface color, not white by default.
- Accent tint **only** on the primary action in a group. Tinting everything destroys hierarchy.

### Edge definition
- Enough edge to stay legible over any backdrop: hairline border (about 1px at low alpha), top inner highlight, subtle contrast step, soft shadow.
- No thick white outlines. No obvious borders. The edge suggests separation; it does not draw attention.

### Shadows
- Soft, atmospheric, low alpha, large radius, small offset.
- Shadow color derived from the brand's ink or a deep neutral, not pure black.
- Increase shadow slightly as the surface rises in hierarchy or as content scrolls beneath it. Elevated, never detached.

### Adaptivity (when the background changes)
Choose explicitly, per component:
- Raise opacity toward the tier maximum over busy regions
- Switch foreground light/dark based on the backdrop (native platforms do this; on web, use scroll position or section-level flags, not per-frame pixel sampling)
- Add a scroll edge effect under fixed bars: a short fixed strip that dissolves content into the page background before it reaches the bar (Apple: it "lifts the glass visually above the moving content"). Show it only once there is content under the bar; it is one more filtered layer, so drop it while a sheet is open on a phone.
- Make the bar's shadow content-aware: heavier over text and images, lighter over a plain light surface. On the web, hit-test two or three points just under the bar per scroll frame (`elementsFromPoint`) and classify what is found; set state only on change.
- Reposition the control away from the busiest region
- Remove glass and use a solid surface

---

## 7. Shape language

### Radius hierarchy (starting scale)
| Element | Radius |
|---|---|
| Large surface (sheet, dialog, panel) | 24 to 32px |
| Medium component (menu, popover, toolbar) | 16 to 24px |
| Control (field, button) | 12 to 16px |
| Small icon button | 10 to 14px |
| Pill | 999px |

Pick one value per role per project and tokenize it. No ad hoc radii.

### Concentricity
Nested shapes share a center: **inner radius = outer radius − padding** (floor at the control minimum). A 28px sheet with 12px padding holds 16px controls. Mismatched nested corners are the fastest way to look cheap.

### Pills
Appropriate for: filters, tags, compact metadata, statuses, compact actions, a single floating control group.
Not for: every heading, every CTA, every navigation item, cards, sections.

---

## 8. Typography, color, gradients

### Typography
- No required font; it comes from the brand. On native Apple platforms the system font is legitimate; on the web do not impose Apple's fonts.
- Clean, highly legible, contemporary, restrained. Decorative type only if the brand requires it.
- Hierarchy through size, weight, spacing, line height, contrast; not through many font styles.
- Text on glass: prefer medium or semibold weights at small sizes; thin weights fail over translucency.

### Color
- Color comes from the brand. Liquid Glass does not require blue/purple gradients, rainbow gradients, neon, white-on-purple, or "futuristic" palettes.
- The material system is constant; the brand system changes. The same material tiers can serve a weather app, a music player, a code editor, or a transit map, each with its own palette.

### Gradients
- Optional. Never used to signal "modern."
- If used: subtle radial ambient light, content-derived color, soft transitions.
- Background is continuous. No banded sections (white, then purple, then blue) unless a deliberate structural transition is required.

---

## 9. Spacing and layout

- Solve spacing and composition **before** adding material. Glass does not rescue a bad layout.
- Base unit 4 or 8px. Scale: 4, 8, 12, 16, 24, 32, 48, 64, 80, 96, 120.
- Generous breathing room. Never compress components to fit more.
- Prioritize alignment, whitespace, hierarchy, rhythm, balance, clear grouping.
- Avoid arbitrary masonry, excess cards, components touching, random floating elements, inconsistent spacing.
- Floating UI keeps a consistent inset from viewport edges (for example 12 to 16px mobile, 16 to 24px desktop) and respects safe areas.

---

## 10. Component decision framework

Answer internally for every component **before styling it**. Record answers in the Phase C layer map for non-trivial components.

1. What is this component?
2. What is its purpose?
3. Content or UI?
4. Persistent or contextual?
5. Does it need to float above content?
6. Does it need material separation?
7. Should it use Liquid Glass? (gate question)
8. Which material tier?
9. Which radius role (and concentric to what)?
10. What contrast is required (text, icons, boundaries)?
11. What happens on hover?
12. What happens on interaction (press, focus, expand, disabled)?
13. What happens on mobile?
14. What happens when the background changes?

### Default classifications (override with reasons)
| Component | Default |
|---|---|
| Top nav / app bar (sticky over scroll) | Regular glass (Thin only if icon-only or over a controlled backdrop) |
| Bottom tab bar / floating nav | Regular glass |
| Search field (floating) | Regular glass; inside a glass bar it is a fill, not a second glass layer |
| Filter / chip bar over content | Thin or Regular glass container; chips are fills inside it |
| Floating action button / contextual toolbar | Regular glass; primary action may take accent tint |
| Menu, popover, dropdown | Thick glass |
| Bottom sheet, dialog | Thick glass plus scrim |
| Toast / snackbar | Thick glass or solid |
| Tooltip | Solid or thick; small text rarely survives translucency |
| Cards, product tiles, article teasers | **No glass** |
| Hero image, galleries, media | **No glass** (content) |
| Page sections, backgrounds | **No glass** |
| Forms in page flow | **No glass**; solid fields |
| Footer | **No glass** |

---

## 11. Interaction, motion, responsive, performance

### States
Every glass control defines: rest, hover (pointer only), pressed, focus-visible, disabled, and expanded where relevant. Glass does not replace state styling.

### Motion
- Reinforces material behavior and communicates state or spatial relationships.
- Allowed: subtle scale (about 0.96 to 1.02 on press), opacity, short translation, material expansion (a control grows into a menu or sheet from its own origin), contextual appearance.
- Durations roughly 150 to 300ms; springs lightly damped, no visible overshoot bounce.
- Avoid bouncing, dramatic or decorative motion.
- Reduced motion: replace movement with opacity changes; never remove state feedback.

### Responsive
- Not desktop-only. On mobile: fewer floating layers, simpler navigation, less blur, no overlapping controls, preserved hierarchy, touch targets at least 44x44pt or 48x48dp.
- Recompose; do not shrink the desktop layout.
- Keep thumb zones and safe areas clear; floating bars must not cover primary content actions.

### Performance
- Backdrop filters are expensive: each one re-samples and blurs what is behind it on every scroll or animation frame.
- Budget: typically no more than 2 to 3 simultaneous backdrop-filtered layers per view on desktop, 1 to 2 on mobile. Justify exceptions.
- Never apply to entire pages, large content grids, image collections, or long lists of items.
- Do not animate blur radius on large surfaces; animate opacity or transform instead.
- Test on mid-range and older devices, not only on a current high-end laptop.
- Measured reference points, software-rendered headless Chromium, 1440px page, scrolling: 0 filtered layers 16.7ms median frame; 1 layer 20ms; 2 layers 24ms; 5 layers 29ms median / 74ms p95; 9 layers 79ms median / 365ms worst. Real GPUs do far better, but the shape of the curve holds.
- Add a static variant to the material (same fill, rim and highlight, `backdrop-filter: none`) for surfaces that sit on the page background rather than above scrolling content. Same look, no per-frame cost. Decide per surface with a pixel diff, not by taste.
- Glass that only frosts on hover is not glass. If a surface is the design's centrepiece and the design shows it frosted at rest, spend the budget there and take it back elsewhere (static content panels, fewer layers on mobile). Do not quietly gate the effect to hover to make the numbers work; say what it costs and let the owner decide.

---

## 12. Brand adaptation

This skill is brand-agnostic. Never assume any project's colors, typography, spacing, logo, or imagery unless the **current** project defines them.

### Project Brand System (create or extract at project start)
- Color tokens: background, surface, ink (text), muted ink, accent, accent-ink, border, semantic (success, warning, danger)
- Typography: families, scale, weights, line heights
- Spacing scale
- Radius roles
- Imagery style
- Iconography (set, stroke weight, fill style)
- Tone of voice and content style

### Combination rule
`Liquid Glass system (material, hierarchy, depth, interaction)` + `Project Brand System (color, type, identity, imagery, tone)` = project UI.
Glass tints and shadows are derived from brand tokens, never hard-coded white and black.

---

## 13. Accessibility (non-negotiable)

Accessibility wins over aesthetics. Verify, over the worst-case backdrop:
- Text contrast: at least 4.5:1 for body text, 3:1 for large text (WCAG 2.x AA)
- Icons, control boundaries, and focus indicators: at least 3:1 against adjacent colors (WCAG 1.4.11)
- Buttons recognizable as buttons without relying on the glass effect
- Visible focus states; complete keyboard navigation; logical focus order; focus trapped in dialogs and sheets
- Touch targets: WCAG 2.2 minimum 24x24 CSS px; design to 44x44pt (Apple) or 48x48dp (Material)
- Reduced motion respected
- Reduced transparency and increased contrast respected (native settings; on web see section 14 and note limited browser support)
- Forced colors / high contrast mode produces solid, bordered surfaces

**If glass reduces readability, in this order:** increase material opacity → change placement → add contrast (scrim, stronger edge, heavier weight) → remove the glass effect.

Because OS-level "reduce transparency" signals do not reach most browsers, the **default** glass must already pass contrast. A preference media query is a bonus, not the safety net.

---

## 14. Implementation techniques (separate from principles)

The principles above are platform-neutral. Techniques below are one realization each; adapt them to the project's stack. Platform versions and APIs change, so flag version-specific items for the user to confirm.

### Token contract (platform-neutral names)
```
material.{thin|regular|thick|clear}.fill       color with alpha, derived from brand surface
material.{tier}.blur                           length
material.{tier}.saturation                     percentage
material.{tier}.edge                           hairline color and alpha
material.{tier}.highlight                      inner top highlight
material.{tier}.shadow                         color, blur, offset
material.solid.{tier}.fill                     opaque fallback per tier
radius.{surface|component|control|icon|pill}
space.{1..12}
motion.{fast|base|slow}, motion.easing.standard
```

### Web (HTML/CSS; applies to React, Next.js, Vue, Svelte)
```css
:root {
  /* placeholders: replace with the Project Brand System */
  --brand-surface: #f5f5f7;
  --brand-ink: #111114;

  --lg-regular-fill: color-mix(in oklab, var(--brand-surface) 56%, transparent);
  --lg-regular-solid: color-mix(in oklab, var(--brand-surface) 94%, var(--brand-ink));
  --lg-regular-blur: 24px;
  --lg-saturation: 140%;
  --lg-edge: color-mix(in oklab, white 22%, transparent);
  --lg-highlight: color-mix(in oklab, white 35%, transparent);
  --lg-shadow: 0 8px 32px color-mix(in oklab, var(--brand-ink) 10%, transparent);
  --radius-component: 20px;
}

/* Fallback first: legible without backdrop-filter */
.lg-regular {
  background: var(--lg-regular-solid);
  border-radius: var(--radius-component);
  box-shadow: inset 0 1px 0 var(--lg-highlight), inset 0 0 0 1px var(--lg-edge), var(--lg-shadow);
}

@supports ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .lg-regular {
    background: var(--lg-regular-fill);
    -webkit-backdrop-filter: blur(var(--lg-regular-blur)) saturate(var(--lg-saturation));
    backdrop-filter: blur(var(--lg-regular-blur)) saturate(var(--lg-saturation));
  }
}

@media (prefers-reduced-transparency: reduce) {   /* limited browser support */
  .lg-regular { background: var(--lg-regular-solid); backdrop-filter: none; -webkit-backdrop-filter: none; }
}
@media (prefers-contrast: more) {
  .lg-regular { background: var(--lg-regular-solid); box-shadow: inset 0 0 0 1px var(--brand-ink); backdrop-filter: none; -webkit-backdrop-filter: none; }
}
@media (forced-colors: active) {
  .lg-regular { background: Canvas; border: 1px solid CanvasText; backdrop-filter: none; -webkit-backdrop-filter: none; }
}
@media (prefers-reduced-motion: reduce) {
  .lg-regular { transition-property: opacity; }
}
```
Dark mode: redefine brand tokens and fills under the project's theme mechanism; do not reuse light-mode alphas unchanged (dark glass usually needs a higher fill alpha and a dimmer highlight).

Web gotchas:
- **Backdrop root:** `backdrop-filter` only samples up to the nearest ancestor that creates a backdrop root (for example an ancestor with `filter`, `opacity` below 1, `mask`, `mix-blend-mode`, or its own `backdrop-filter`). Nested glass and glass inside faded containers silently show nothing. Another reason not to nest.
- If the blur bleeds past rounded corners in a given engine, add `overflow: hidden` to the glass element.
- SVG displacement "refraction" is Chromium-only in `backdrop-filter`. Safari and Firefox drop the **entire** `backdrop-filter` declaration if any function in the list is unsupported, so an ungated `url(#filter)` removes the blur outright in two engines. Gate it: `@supports (backdrop-filter: blur(1px) url(#a)) { ... }`, and make the non-refracted version the designed baseline.
- Chrome silently renders **neither** effect on an element that carries both `mask-image` and `backdrop-filter` (verified live). Put the mask on an outer element and the blur on an unmasked inner child. The older `clip-path` + `backdrop-filter` bug is separate and also real.
- A highlight or specular layer with `mix-blend-mode` forces its parent into an isolated group, and an isolated ancestor is a backdrop root: the sibling glass samples nothing. Use plain translucent gradients for highlights.
- Tailwind v4: colour tokens declared in `@theme inline` are baked as literals into every utility (`.bg-surface{background-color:#fff}`), so a themed override changes nothing. Put colour tokens in plain `@theme` so utilities emit `var(--color-…)`. Verify in the built CSS.
- Components expose a `material` prop (`"none" | "thin" | "regular" | "thick"`) instead of ad hoc class stacks, so tiers stay enforceable.
- Utility CSS frameworks: define tiers as named utilities or component classes backed by the tokens; do not scatter one-off blur values.

### SwiftUI (Apple platforms with Liquid Glass, version 26 and later)
- Prefer the native material over any custom blur: standard bars, tab bars, toolbars, and sheets adopt Liquid Glass automatically when built with system components.
- Custom floating controls: `.glassEffect()` with an explicit shape; `.buttonStyle(.glass)` for secondary and `.buttonStyle(.glassProminent)` for the single primary action; group related glass elements in a `GlassEffectContainer` so they render and morph as one material.
- Tint via the glass API only for primary emphasis; do not recolor all glass.
- Earlier OS versions: fall back to system `Material` levels (`.ultraThinMaterial` to `.thickMaterial`) mapped to the tiers above.
- Respect `accessibilityReduceTransparency`, `colorSchemeContrast`, and `accessibilityReduceMotion` environment values in any custom material.

### Other platforms
- **Android (Compose/Views):** there is no general in-app backdrop blur. `RenderEffect` (API 31+) blurs a view's own content, not what is behind it; window background blur applies to dialogs and windows. In-app glass needs a third-party library (recommend one; the user decides whether to add it) with a solid fallback, and only on small floating bars.
- **Flutter:** `BackdropFilter` inside `ClipRRect`; keep the count low, and avoid it in scrolling list items.
- **React Native:** use a native blur or glass module chosen by the user, with a solid fallback on platforms where blur is weak or expensive.

### Design tools
- Build each tier as a reusable style: fill (brand surface at tier alpha) + background blur + inner highlight + hairline stroke + soft shadow.
- Publish tiers and radius roles as tokens or variables. Prototype over realistic content, including a worst-case image, never over a flat gray.

---

## 15. Anti-pattern database

If the output starts resembling any of these, stop and correct.

| # | Anti-pattern | Correction |
|---|---|---|
| 1 | Glass card grids | Solid or borderless cards; glass only on the filter bar above |
| 2 | Glass page backgrounds | Continuous brand background; ambient light at most |
| 3 | Glass sections | Structure with spacing and type |
| 4 | Glass inside glass | One material layer; fills and dividers inside |
| 5 | Giant rounded rectangles | Apply the radius hierarchy; reduce surface size |
| 6 | Excessive white transparency | Tint from brand surface; raise opacity |
| 7 | Heavy shadows | Low alpha, large blur, brand-ink color |
| 8 | Neon gradients | Brand palette only |
| 9 | Purple "AI" gradients | Remove; brand palette only |
| 10 | Random floating blobs | Remove; ambient light must be content- or brand-derived |
| 11 | Decorative glass circles | Remove; fails the gate question |
| 12 | Glass everywhere | Rerun the layer map; Layer 3 only |
| 13 | Pills everywhere | Pills for filters, tags, statuses, compact actions only |
| 14 | Excessive blur | Lower toward tier minimum; blur is separation |
| 15 | Low-contrast text | Section 13 remediation order |
| 16 | Generic "AI startup" look | Re-anchor on the Project Brand System |
| 17 | Generic Web3 look | Remove glow, neon, chrome gradients |
| 18 | Generic website-template look | Rebuild hierarchy from content and brand, not from effects |
| 19 | Accent tint on every glass control | Tint the single primary action only |
| 20 | Clear glass over text-heavy or light content | Use Regular or Thick |
| 21 | Refraction or blur as the only affordance | Controls must read as controls with glass disabled |
| 22 | Apple clone (Apple icons, iOS chrome on a web brand) | Adopt principles, not Apple's visual assets |
| 23 | Frost that switches on only on hover | Frost at rest; rebalance the layer budget elsewhere |
| 24 | Uniform noise "refraction" across the whole pane | Edge-concentrated displacement from the element's outline, or no refraction |
| 25 | Matching a design tool's slider numbers instead of its look | Match the rendered reference by eye and by pixel; the numbers do not translate (section 17.1) |
| 26 | Opaque brand fill on the primary button inside glass | Tinted glass: brand colour at ~80-85% with the material's rim and key light; measure the text contrast |

Visual character check. Should feel: light, spatial, precise, calm, premium, tactile, adaptive, modern, intentional. Must not feel: glossy, plastic, futuristic for its own sake, Web3, generic AI, template-like, neon, overly colorful, excessively rounded, visually noisy.

---

## 16. Design quality test (before finalizing)

Answer each explicitly. Any "no" means revise.

| Check | Question | Evidence to produce |
|---|---|---|
| Hierarchy | Can I immediately tell what is important? | Squint or blur test of the full screen |
| Spatiality | Does the UI feel layered? | Content vs floating UI distinguishable at a glance |
| Material | Does every glass surface communicate function? | Gate-question answer per glass element |
| Restraint | Is glass used selectively? | Count of glass layers per view within budget |
| Clarity | Can everything be understood quickly? | No control relies on glass to be recognized |
| Consistency | Do shapes, spacing, type belong together? | All radii, spacing, type values map to tokens |
| Adaptability | Does the material work over different backgrounds? | Screenshots over lightest, darkest, and busiest backdrops |
| Accessibility | Can users read and interact with it? | Measured contrast ratios, keyboard pass, fallback rendering (no backdrop-filter, forced colors) |
| Brand | Does it belong to this specific product? | Colors, type, imagery traceable to the Project Brand System |

When delivering, report the checks, the measured contrast values where measurable, the fallback behavior, and any limitation that remains. Do not claim a check passed without evidence.

### How to measure (web)
- **Contrast over glass:** screenshot with every text node made invisible first (`* { color: transparent !important }`), sample the background at each text box's centre from that image, composite the text colour over it if the text is semi-transparent, then compute the ratio. Sampling with the glyphs visible measures the glyph pixels and reports false failures.
- **Whether a blur earns its cost:** screenshot the surface with the blur on and off; report max channel difference, mean, and the fraction of pixels differing by more than 2. Under ~5/255 max the blur is invisible and the surface should be static.
- **Scroll cost:** record `requestAnimationFrame` deltas while scrolling programmatically; report median, p95 and worst, with all filters off as the control.
- **Layer count:** count elements whose computed `backdrop-filter` is not `none` and are in the viewport, per page and per state (menu open, hover).
- **Rim and fallbacks:** render at 2-3x device scale and crop the edge; render with `forced-colors: active` and `prefers-contrast: more` emulated and confirm solid fills and visible borders.

---

## 17. Field notes from a production build

Findings from applying this system end to end on a live site, measured rather than assumed. They refine the principles above; they do not replace them.

### 17.1 Design-tool parity: Figma's Glass effect
Figma's Glass effect (Light, Refraction, Depth, Dispersion, Frost, Splay) composites differently from CSS, so its numbers are a brief, not a spec. What each slider corresponds to on the web, and what it took to match the *rendered* look:

| Figma control | What it does | Web counterpart | Note |
|---|---|---|---|
| Fill (white, N%) | pane opacity over the blurred backdrop | `background: color-mix(surface N%, transparent)` | Figma 50% needed ~72% in CSS to look the same over a blurred photo; at CSS 50% the pane read as milk. Match the look, then record the number. |
| Frost | backdrop blur | `backdrop-filter: blur()` | Frost in the mid-30s on a pane roughly 270px wide landed at 14px. |
| Refraction + Depth | edge lensing: how far and how wide the rim bends the backdrop | displacement map from the outline (17.2), `scale` in px and bevel width as a fraction of the short side | Depth ≈ bevel band width; ~13-16% of the height read right. |
| Dispersion | colour fringe at the rim | three displacement passes at reach ±Δ, one per channel, recombined | Only with an edge-weighted map; uniform dispersion desaturates. |
| Splay | how strongly content stretches outward at the edge | sign and magnitude of the displacement (inward-pointing vector = content splays outward) | |
| Light (angle, %) | rim light direction and strength | lighting map from the same outline normals, or a top-edge gradient stroke | -45° = key light from the upper left. |

Workflow that worked: build to the numbers, screenshot next to the reference at 2-3x, then move fill and frost until the *look* matches, and write the final numbers and the reason into the token comments.

### 17.2 Edge-concentrated lensing on the web
The one technique that separates a blurred rectangle from something that reads as glass, and it only works in Chromium:

1. Rasterise the element's outline once on a canvas; compute the distance of every inside pixel to the outline.
2. Apply a biconvex profile over a band of width zR inside the edge: `h(d) = sqrt(d · (2zR − d))`, flat beyond it (from the open-source liquidglass shader).
3. Take the normal `N = normalize(−∇h, 1)`. `N.xy` is zero across the flat middle and grows to unit length at the rim; encode `−N.xy` into the R/G channels of a PNG (128 = no displacement).
4. Hand it to the filter as `<feImage href="data:…" preserveAspectRatio="none">` with `filterUnits="objectBoundingBox"`, feed `feDisplacementMap`. Chromium honours `feImage` inside `backdrop-filter` (verified with a stripe test first). Run the lens *before* the blur in the filter list.
5. The same normals against a fixed light give a rim-light overlay: bright where the bevel faces the light, faintly shaded where it faces away, plus a hairline on the outline.

Gate the whole thing behind `@supports (backdrop-filter: blur(1px) url(#a))`. Safari and Firefox get the frosted pane, rim light and fill without the bend, which must already be the designed baseline.

### 17.3 Apple guidance that translated directly
From Apple's Liquid Glass overview, the HIG Materials page and WWDC25 "Meet Liquid Glass":
- **Scroll edge effect** under the bar (section 6). Split across two elements because of the mask + backdrop-filter bug.
- **Content-aware shadow** on the bar (section 6).
- **Tinted primary action:** an opaque brand fill "breaks the visual character of Liquid Glass". Brand colour at 84% with the rim and key light measured 5.2-5.5:1 for white text in every scroll state; below ~78% it starts to fail over a pale backdrop.
- **Interactive illumination:** on press the material lights from the point of contact and the glow spreads. One delegated `pointerdown` listener writes `--press-x/--press-y` to the pressed element; CSS draws a radial glow from that point that scales up while `:active`.
- **Thicker material when a surface morphs larger:** a wider bevel band and brighter Fresnel line on the Thick tier.
- **Not adopted, on the owner's instruction:** Apple says not to use Liquid Glass in the content layer. When the product owner explicitly wants glassmorphic content panels, use the static variant (no blur) so the aesthetic is kept at zero per-frame cost, and record the override where the next person will read it.

### 17.4 Give the glass something to be glass to
A footer that had been a page's one dark slab became a Thick frosted pane sitting on its own backlight: three soft radial glows in the brand colours, blurred 28px, painted as a *sibling before* the pane (a child would paint over the material; an ancestor with a filter would become a backdrop root). Without the backlight the frost had nothing to work on. The same logic fixed the page background: near-white pastel blobs behind 50-75% white panels meant there was nothing to see through; saturated blobs cost nothing to render and made the material legible as material.

### 17.5 Working with the owner
- **Reference first.** A screenshot of the design tool's render, or a photo of the intended look, resolves more than any number of adjectives. Ask for it before tuning.
- **One knob per property.** Every value someone might ask to change (fill, frost, bevel width, offsets, tint) is a single token with a comment saying why it has that value. Revisions become one-line changes.
- **Polish passes are single revertable commits.** State in the PR what moved and what did not (geometry, positions, assets, motion), and how to revert.
- **Autonomous mode.** When the owner says to proceed without proposals, skip Phase C and put the layer map, the measurements and every deliberate override into commit messages instead. The reasoning still has to exist somewhere the next person will find it.
- **Assets:** design-tool "SVG" exports are often a bitmap in an SVG wrapper with a provenance manifest (0.2-1.2 MB each). Render each one and sample the corners before trusting it to be transparent; then rasterise at ~2.5x the display size and re-encode (WebP), keeping the filename so nothing else changes.

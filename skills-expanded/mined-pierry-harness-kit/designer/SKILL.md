---
name: designer
description: Visual + UX design defaults for new UIs. Material Design 3, dark/light theme, modern type, Behance-grade polish, i18n (en, pt-BR, es), context-aware favicon. No emojis and no em-dashes; use MD3/modern icons instead. Apply when building something new. Project conventions in .claude/conventions/web.md override these defaults.
user_invocable: false
---

Designer conventions. Apply when SSE builds something **new** with a UI (new app, page, feature,
landing). Layers on top of the area skill (web/mobile), does not replace it. Project override:
`{repo}/.claude/conventions/web.md` wins. Match existing design system if repo already has one; only
green-field gets these defaults.

## READ FIRST: Material Design 3 is non-negotiable

Every visual surface this skill touches **must** be Material Design 3. Not "M3-inspired", not "close
enough". M3 is the system: token-driven color roles, the shape scale, tonal elevation, state layers,
and motion. If you are about to write a color, a border, a radius, or a callout, it comes from M3,
not from instinct or a CMS habit. This rule has been broken before; do not break it again.

**Before you ship any surface, self-check against these top offenders. Each one is a hard rule with
its own section below; this is the unmissable summary, not the exception list.**

- **No colored left-border accent bars.** A `border-left: 3px/4px solid var(--primary)` on a card,
  hint, callout, banner, or "supporting" box is forbidden. It collides with the shape-scale radius
  and leaves a colored sliver in the rounded corner (the classic "corzinha no canto"). Color the
  **surface** with a tonal container (`secondary-container` / `surface-container-high`), never one
  edge. See "Info, help, and supporting surfaces".
- **Tonal containers, not ad-hoc borders, carry meaning.** Reach for a `*-container` role + its
  `on-*` text + a real shape radius + an MD3 `info` icon. A stripe is not a design system.
- **Tokens only, never raw hex** in component CSS. Define roles once for light and dark.
- **No emoji, ever.** Use Material Symbols or a single modern open set. Draw brand marks original.
- **No em-dashes or en-dashes** anywhere: copy, headings, comments, commits, PRs, docs, all locales.
- **Both themes, always.** Light and dark, system-preference first, choice persisted.
- **Vivid, on-trend color, never a timid grey wash.** Saturated modern seed + a second accent +
  purposeful gradients. A washed-out palette is a build blocker. See "Vivid, on-trend color".
- **A real, beautiful typeface, never the raw system stack.** Load/embed a current variable face
  (Geist, Instrument Sans, Bricolage Grotesque, etc.); system-ui as the final look is forbidden.
- **Depth and motion on every surface.** Layered + tinted shadows, accent glow, highlights/glass,
  and animation are always on (with `prefers-reduced-motion`). Flat and shadowless is a defect.

When in doubt, open the matching section below and follow it literally. The detailed rules win over
any quick instinct, and the "Forbidden" list at the end is exhaustive. Treat a violation of any of
these as a build blocker, the same as a failing test.

## Design language: Material Design 3

Use M3 as the system, not the look. Token-driven, not hardcoded.

- **Color**: define color **roles**, not raw hex. Roles: `primary`, `on-primary`,
  `primary-container`, `on-primary-container`, `secondary`, `tertiary`, `surface`,
  `surface-container` (lowest..highest), `on-surface`, `on-surface-variant`, `outline`, `error`,
  `on-error`. Derive from a single seed color (dynamic color). Pick the seed from product context, not
  default purple.
- **Typography scale**: display / headline / title / body / label, each L/M/S. Map to CSS classes.
- **Shape scale**: none 0, xs 4, s 8, m 12, l 16, xl 28, full. Cards `l`, buttons `full` or `m`,
  sheets `xl`.
- **Elevation**: 6 levels via layered `surface-container` tints + subtle shadow. Prefer tonal
  elevation (container tint) over heavy shadows.
- **State layers**: hover 8%, focus 10%, pressed 10% of `on-*` over the component.
- **Motion**: M3 easing `emphasized` (cubic-bezier(.2,0,0,1)), standard 200-300ms, small 100ms. No
  gratuitous animation. Motion is required, not optional:
  - Every interactive element gets an M3 **state layer** (hover 8%, focus 10%, pressed 10% of the
    `on-*` role over the component), not just a color swap.
  - Every show/hide, expand/collapse, or reveal **animates** both directions. Animate height with the
    `grid-template-rows: 0fr -> 1fr` technique (or `max-height`) plus opacity and a small translate;
    never toggle `display:none` with no transition.
  - Content entrance: stagger cards/sections in with a short rise-and-fade on load.
  - Animate meaningful value changes: count-up on headline numbers/totals, a subtle pulse when a key
    result updates. Build the result DOM once and update in place so values can tween.
  - Always wrap motion in `@media (prefers-reduced-motion: reduce)` to disable it.

## Theme: dark + light

Mandatory both. System preference first, user toggle second, choice persisted.

```css
:root { color-scheme: light dark; }
/* tokens as CSS custom properties, two sets */
:root[data-theme="light"] { --surface:#FDFCFF; --on-surface:#1A1C1E; --primary:#0B57D0; /* ... */ }
:root[data-theme="dark"]  { --surface:#1A1C1E; --on-surface:#E3E2E6; --primary:#A8C7FA; /* ... */ }
```

- Default to `prefers-color-scheme`; toggle writes `data-theme` + `localStorage`.
- Never ship one theme. Verify both for contrast (see Accessibility).
- Dark is not pure black: use `#1A1C1E`-ish surface, elevate with lighter container tints.

## Type: beautiful modern font (never the system stack)

A shipped UI must load a real, characterful typeface. `system-ui` / `-apple-system` as the intended
look is forbidden: it reads as unfinished, the "default" tell of a template. Inter is allowed but it
is now the safe, over-used default, so treat it as a fallback, not the pick.

- **Body / UI default (pick one, current and good):** `Geist`, `Instrument Sans`, `General Sans`,
  `Manrope`, or `Inter Tight`. Variable weight. This is the workhorse for body, labels, and data.
- **Display / headline (pick one, pair with the body face):** `Bricolage Grotesque`, `Clash Display`,
  `Sora`, `Fraunces` (for a warmer editorial feel), or `Space Grotesk`. One display + one text face,
  no more. The display face carries the hero and big numbers; give it real weight (600-800) and tight
  tracking.
- **Numbers:** always `font-variant-numeric: tabular-nums` for data, meters, and KPIs. A mono face
  (`Geist Mono`, `JetBrains Mono`) is fine for code/IDs only, not for prose.
- **Loading, offline-safe:** self-host or embed. When the surface must work with no network or under a
  strict CSP (standalone HTML, an Artifact, an embedded tool), **embed the variable font as a base64
  `woff2` `@font-face` data URI** so the real face always renders. Never ship the system stack as the
  final design and call it done. Always `font-display: swap`. Keep a system fallback in the stack for
  the first paint only.
- Stack example: `"Geist", "Inter Tight", system-ui, sans-serif` (fallback trails, never leads the intent).
- **Never use em-dashes (`—`) or en-dashes (`–`)** in any user-facing copy, headings, labels, empty
  states, microcopy, or content strings. Hard rule. Use a comma, colon, parentheses, or rewrite the
  sentence. Same rule in code comments, commit messages, PR text, and docs. Applies to all three
  locales. Hyphen (`-`) is fine for compound words.

## Behance-grade polish (the "new and good" bar)

Inspiration: top Behance UI work. **Actually research it, do not just invoke the name.** Before
designing a new surface, run a real web search for current Behance/Dribbble work in the product's
domain (e.g. "Behance fintech investment calculator dark UI"), look at several results, and extract
concrete directives (accent treatment, card and result styling, data-viz patterns, spacing, motion).
Note in the build what you took from it. Behance gallery pages are JS-rendered, so screenshots may
not be machine-readable; rely on the search result summaries and the patterns they describe, and
state the sources.

A recurring, high-value pattern from fintech/finance results UIs: **visualize the breakdown, do not
just list numbers.** For any result that is a sum of parts (gross = principal + yield + taxes,
budget = categories, score = components), add a lightweight visual (a stacked composition bar, a
donut, or a sparkline) with a value legend, animated on update. Pure CSS/SVG, no chart lib, to keep
load fast. A bare list of figures is the unfinished version.

What top Behance work means concretely:

- **Generous whitespace.** 8pt spacing grid (4/8/12/16/24/32/48/64). Let layouts breathe.
- **Strong hierarchy.** One clear focal point per view. Big confident headline, calm body.
- **Vivid, on-trend color** (see the dedicated section below). A washed-out, timid, grey-on-grey
  palette is a defect, the same as a bug. Saturated, modern, confident color is the default.
- **Intentional contrast.** Size, weight, and space carry hierarchy; color makes it feel alive.
- **Crisp components.** Consistent radius, aligned grids, optical alignment, no orphaned elements.
- **Real content.** Design with realistic copy and data, never lorem. Empty/loading/error states
  designed, not afterthoughts.
- **Micro-interactions.** Hover, focus, press feedback on every interactive element, and depth on
  every surface (see "Depth and motion"). Subtle, fast, but always present.

Avoid the generic AI-template look: centered everything, default Bootstrap blue, timid greys, one
flat gradient slapped on a hero. The fix is not "no color", it is *considered, vivid* color plus real
depth.

## Vivid, on-trend color (mandatory)

The palette must feel current and alive, not corporate-muted. This is a hard requirement, and it wins
over any instinct toward a safe neutral wash. Stay inside the MD3 token/role system, just push the
chroma and depth up:

- **Seed with real chroma.** Pick a saturated, modern seed from the product's world (electric indigo,
  vivid violet, cyber-lime, hot coral, aqua/cyan, magenta). Not a desaturated slate, not Bootstrap
  `#0d6efd`, not the default M3 purple. State the seed and why.
- **A second accent for energy.** Beyond the primary seed, define a vivid secondary/tertiary
  (analogous or a punchy complementary) and use it in gradients, chart series, active states, and
  focal highlights. Two lively hues in tension read as "designed", one flat hue reads as "template".
- **Gradients are welcome, used with intent.** Multi-stop or mesh gradients on the hero, primary
  buttons, key numbers, and accent surfaces. Vibrant, directional, not a single grey-to-grey fade.
  A subtle animated gradient or aurora wash in the background is encouraged.
- **Rich, dimensional surfaces.** Dark theme especially: deep, slightly-tinted near-black grounds
  (tint the neutral toward the seed), luminous accent surfaces, and glow. Light theme: crisp bright
  ground with saturated accent fills, never muddy.
- **Container roles keep their vivid `on-*` pairs.** `primary-container` / `secondary-container` etc.
  should be visibly tinted and lively, not a faint 4%-opacity ghost. Keep AA contrast in both themes.
- **Color still earns its place.** Vivid does not mean noisy: one confident focal hue + its accent
  partner + tuned neutrals + separate semantic status colors. Saturation with hierarchy, not confetti.

## Depth and motion (always on)

Every surface has dimension and every view has life. Flat, static, and shadowless is not acceptable
for a shipped UI. Layer these, tastefully but always present:

- **Shadow play.** Real, layered elevation shadows (a soft ambient + a tighter key shadow), tuned per
  theme. Colored/tinted shadows and accent **glow** on primary and focal elements (a soft seed-colored
  bloom behind a key button, KPI, or the hero mark). Not one flat `box-shadow: 0 1px 2px`.
- **Highlights and reflections.** Top edge highlights (a 1px inner light line), subtle glass /
  frosted surfaces (`backdrop-filter: blur()` with translucency) where it suits, and gentle specular
  sheen on primary buttons and cards. Give surfaces a sense of material.
- **Motion is required, not decorative.** Staggered entrance on load, hover/press micro-interactions
  with MD3 state layers, animated value changes (count-up, meter fill, a pulse when a key result
  updates), and animated show/hide (both directions, never a `display:none` snap). A slow ambient
  background motion (drifting gradient/aurora) is a nice touch. M3 `emphasized` easing.
- **Always** wrap motion in `@media (prefers-reduced-motion: reduce)` and keep interactions 60fps
  (animate `transform`/`opacity`, not layout). Effects must never cost legibility or AA contrast.

These raise the bar; they do not relax the MD3 correctness rules. Tonal containers still carry meaning
(no colored left-border bars), tokens still drive color (no raw hex in components), both themes still
ship, and never an emoji or a dash.

## Info, help, and supporting surfaces

For any callout, help text, tooltip body, inline explanation, hint, banner, or "supporting"
surface:

- **Never use a colored left-border accent bar** (`border-left: 3px solid ...`) to mark it. That
  reads as a generic CMS blockquote or a Bootstrap alert, not MD3. Hard rule.
- Use an **MD3 tonal container**: `secondary-container` / `on-secondary-container` (or
  `surface-container-high` / `on-surface-variant` for a quieter look), with a real shape radius
  (`shape-m` or `shape-l`), full padding, and an MD3 **info icon** (Material Symbols `info`) leading
  the text. Theme the icon and text with the container's `on-*` role.
- Color the surface, not its edge. Tonal fill carries the meaning; a stripe on one side does not.
- For inline reveals (the "?" expander pattern), animate open and closed (see Motion). A reveal that
  snaps via `display:none` is incomplete.

```css
/* Good: MD3 tonal supporting surface */
.help-panel__body {
  display: grid; grid-template-columns: auto 1fr; gap: 12px;
  padding: 12px 16px; border-radius: var(--shape-m);
  background: var(--secondary-container); color: var(--on-secondary-container);
}
/* Bad: never do this */
.callout { border-left: 3px solid var(--primary); background: var(--surface-container); }
```

## Form inputs are real MD3 text fields

An input is not a bare bordered box with a label floating above it in plain text. Use the MD3 text
field anatomy:

- **Outlined or filled** container (pick one and keep it consistent), 56px tall, proper shape radius.
- **Floating label** that sits as the resting placeholder, then animates up onto the outline (or to
  the top of a filled field) on focus or when filled. Label turns `primary` on focus.
- **Supporting text** under the field for the hint/example (do not abuse the placeholder for hints).
- **Leading/trailing affixes and icons** live inside the field (currency prefix, unit suffix, an
  info or clear trailing icon button), not floating outside it.
- Focus state thickens the outline to `primary` (a 2px look via inset box-shadow is fine).

Skip this only if the repo already standardizes a different field component, in which case match it.

## Page headers and hero structure

A page header is not a wordmark thrown at the top. Build it on the M3 type scale with real hierarchy:

- **Eyebrow** (optional): an M3 `label` (uppercase, tracked, `primary` color) that frames the context.
- **Title**: M3 `display` or `headline`, tight letter-spacing, the single focal point of the view.
- **Subtitle**: M3 `body`/supporting text in `on-surface-variant`, max ~48ch.
- Put the brand mark and utility controls (theme toggle, etc.) in a top bar above the title, not
  inline with it. Give the header generous top space and let it breathe.
- A restrained tonal background wash (one or two soft radial tints from the seed) is allowed; avoid
  gradient-on-everything.

Map the type scale to classes once (`.t-display`, `.t-headline`, `.t-title`, `.t-label`) and reuse
them; do not hand-size headings per page.

## Iconography: original, modern, never emoji

- **Never use emojis.** Not as icons, not in buttons, labels, headings, empty states, or copy. Emojis
  are not a design system: they render differently per platform, break visual consistency, and read as
  unfinished. This is a hard rule. **Use Material Design 3 (Material Symbols) icons, or another modern
  open set (Lucide, Phosphor), in place of any emoji.** Need a glyph -> reach for an MD3/modern icon,
  never an emoji.
- **Create original icons.** Design a custom SVG icon set for the product's key actions and brand
  marks, drawn on a consistent grid (e.g. 24px, 2px stroke, rounded joins) with one visual language
  (stroke weight, corner radius, terminals). The logo/brand glyph and the primary actions should be
  original, not stock.
- **Modern style.** Clean line or duotone icons, optically balanced, legible at 16-20px. Pixel-snap
  and align to the grid. Match stroke weight to the type weight.
- If a full custom set is out of scope, use **one** modern open set as the base (Lucide, Material
  Symbols, Phosphor) and still draw the brand and hero marks original. Never mix icon families.
- Ship icons as inline SVG or a sprite, currentColor-driven so they theme with light/dark. Give each
  an accessible label (`aria-label` or `<title>`).

## i18n: en, pt-BR, es

All user-facing copy translatable. Three locales shipped: `en` (default), `pt-BR`, `es`.

- No hardcoded strings in components. Use a `t('key')` lookup.
- Files: `locales/{en,pt-BR,es}.json`, same key set in all three.
- Detect: `navigator.language` -> fallback `en`. User can switch; persist to `localStorage`.
- Set `<html lang="...">` dynamically. Format dates/numbers/currency with `Intl` per locale.
- Keep keys semantic (`cart.empty.title`), not English text as key.

```json
// locales/pt-BR.json
{ "cart.empty.title": "Seu carrinho está vazio", "action.continue": "Continuar" }
```

Plurals via the i18n lib's plural rules. RTL not required for these three.

## Favicon: context-aware

Generate a favicon that reflects the **product context** (its name, initial, domain symbol, brand
seed color), not a placeholder.

- Author as **SVG** (crisp, themeable). Use the brand seed; respect dark/light via
  `@media (prefers-color-scheme: dark)` inside the SVG or a separate dark file.
- Derive the mark from context: product initial/monogram, or a simple glyph matching the domain
  (e.g. a cart for commerce, a chart for analytics). Keep it legible at 16px.
- Ship sizes: `favicon.svg` (primary), `favicon.ico` 32, `apple-touch-icon.png` 180, plus a
  `site.webmanifest` with 192 + 512 maskable PNGs.
- Tags:

```html
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#FDFCFF">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#1A1C1E">
```

State which symbol + seed you chose and why (the context link).

## Accessibility (non-negotiable)

- Contrast: body text >= 4.5:1, large text/UI >= 3:1, in **both** themes.
- Visible focus ring on every interactive element (`:focus-visible`).
- Hit target >= 44x44px. Respect `prefers-reduced-motion`.
- Semantic HTML + ARIA where needed. Label every input. Keyboard reachable.

## Before building

- If the repo already has a design system or theme, **use it**. Read 3 existing screens first.
- Confirm the framework's styling approach (CSS vars, Tailwind, SCSS, CSS-in-JS) and match it.
- Confirm whether an i18n lib already exists; reuse it.

## Deliver with a new UI

1. Token file (color roles + type + shape) for light **and** dark, with a vivid, on-trend seed.
2. Theme toggle wired to system preference + persistence.
3. A real, beautiful variable font loaded (`font-display: swap`), embedded as a `woff2` data URI when
   the surface must run offline / under a strict CSP. Never the bare system stack as the final look.
4. `locales/{en,pt-BR,es}.json` + `t()` wiring + lang switch.
5. Original, modern SVG icon set (currentColor, accessible labels). No emoji.
6. Context-aware favicon set + manifest + tags.
7. Depth and motion: layered/tinted shadows, accent glow, highlights or glass, and entrance +
   interaction animations (all under `prefers-reduced-motion`).
8. Designed empty / loading / error states.

## Forbidden

- Emojis anywhere (UI, icons, buttons, copy, empty states). Use MD3/modern icons instead.
- Em-dashes (`—`) or en-dashes (`–`) anywhere (copy, headings, comments, commits, PRs, docs).
- Stock/generic icons for brand or primary marks; mixing icon families.
- Colored left-border accent bars (`border-left`) for info, help, callouts, or supporting surfaces.
  Use an MD3 tonal container (see Info, help, and supporting surfaces).
- Reveals or expanders that toggle `display:none` with no animation.
- Page headers that are a bare wordmark with no eyebrow/title/subtitle hierarchy.
- Hardcoded colors instead of tokens/roles.
- A single theme (light-only or dark-only).
- Hardcoded user-facing strings.
- Placeholder favicon (default framework icon).
- lorem ipsum in shipped UI.
- Contrast below AA in either theme.
- The raw system font stack (`system-ui`/`-apple-system`) shipped as the intended typeface. Load or
  embed a real, current variable face.
- A timid, washed-out, grey-on-grey or default-Bootstrap-blue palette. Color must be vivid and
  considered (saturated seed + a second accent + purposeful gradients).
- Flat, shadowless, effect-free surfaces. Every surface needs layered/tinted depth and glow; every
  view needs motion (entrance, interaction, value changes), always under `prefers-reduced-motion`.

## Mark gaps

```
<!-- TBD - verify with design/tech lead: {seed color source, brand assets, locale copy owner} -->
```

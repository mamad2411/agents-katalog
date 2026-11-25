---
name: pericles-branding-ui
version: 2026.07.12
description: >
  How Pericles looks and feels — the brand color system (Pericles Purple / Athenian
  Gold / warm neutral), the light + dark theme token architecture, typography, the
  gold fillet device, and the responsive rules that make the same codebase work on
  desktop, iOS, and Android. Use this WHENEVER you touch color, theme tokens,
  typography, spacing/elevation, dark mode, or any layout that must survive a phone.
  Encodes the three-layer token model (ramps → role tokens → utilities), the
  contrast-validated light/dark pairs, the risk-severity color mapping, and the
  mobile/device constraints (touch targets, safe areas, dvh, no-hover, PWA chrome).
doctrine_refs: [§6; GitHub #17 "Modernize UI and Apply Brand Color Palette"]
depends_on: [pericles-frontend-foundations, pericles-persona-layer, pericles-mobile]
last_reconciled: 2026-07-28
---

# Pericles Branding & UI System (build skill)

Pericles is an **alerting product for executives**. The visual system has one job beyond
looking good: make risk state unmistakable at a glance, and never let a decorative
flourish be confusable with a severity signal. Everything below follows from that.

The brand is two founding colors — **Pericles Purple `#524765`** (authority, gravity,
trust) and **Athenian Gold `#D19B2F`** (distinction, signal, ceremony) — on a **warm
neutral grey** that carries a trace of the purple hue, so the greys read as *ours*
rather than as a generic UI kit.

## When to use this skill

Any change to color, theme tokens, dark mode, typography, radius/elevation/motion, or
a layout that has to hold up on a phone. Read `pericles-frontend-foundations` first for
stack and component conventions; this skill is the visual layer on top of it.

## Ground truth (migration completed 2026-07-28, `frontend/`)

The migration described below has **landed**. Current state:

- `src/app/globals.css` holds the three-layer token system; the default Tailwind
  palettes are **cleared** (`--color-gray-*: initial` and 20 more), so `bg-slate-500`
  and friends compile to nothing.
- **Zero** default-palette classes remain in `.tsx`/`.ts` (was 1,372).
- **Zero** dead `dark:` pairs on removed palettes (was 401, none of which ever
  rendered because nothing set the `dark` class).
- `next-themes` is installed; provider, light/dark/system toggle, per-mode
  `themeColor`, `color-scheme`, and `app/manifest.ts` are wired.
- Fonts: Geist Sans (UI) + Cormorant Garamond (display) + IBM Plex Mono (data).
- Stack: Tailwind **v4** (`@tailwindcss/postcss`, no `tailwind.config.js`), shadcn
  "new-york" with `cssVariables: true`, Next.js 16 App Router, React 19.
- **No template copies** (GH #35): the duplicated `templates/*` files were deleted —
  the shipped files this skill references are the single authoritative copy. When a
  ramp or role token moves, edit `frontend/src/app/globals.css` once; never re-create
  a copy.

**Two sanctioned raw-hex exceptions**, both because the consumer cannot read CSS
custom properties: `src/lib/atlas-brand.ts` (Google Maps markers, routes, and the
light/dark map styles) and the PWA `themeColor`/manifest colours. Both mirror the
ramps and must be updated together with them.

The migration history is kept below because the *ordering* is the reusable part — if a
sibling app or a new surface needs the same treatment, follow it.

## The three-layer token architecture

This is the core discipline. Skipping a layer is what produces an unmaintainable theme.

```
Layer 1  RAMPS          --color-purple-600, --color-grey-200, --color-danger
         (mode-independent brand primitives; defined once in @theme)
             ↓ referenced by
Layer 2  ROLE TOKENS    --background, --card, --border, --primary, --risk-critical-fg
         (mode-DEPENDENT; defined twice — :root and .dark)
             ↓ exposed by @theme inline as
Layer 3  UTILITIES      bg-background, text-muted-foreground, border-border
         (what components actually use)
```

**Components consume Layer 3 role utilities. Ramp utilities (`bg-purple-600`,
`text-gold-500`) are reserved for deliberate brand moments** — the wordmark, a fillet,
a marketing surface. If you write `bg-purple-800` inside a card, you have hardcoded a
mode and it will break in the other one.

The authoritative theme file is `frontend/src/app/globals.css` — edit it in
place; there is no copy to keep in sync (GH #35). Ramps and rationale are in
`references/palette.md`.

### Layer 1 — the ramps

Purple 50–900 (base **600**), Gold 50–900 (base **500**), Grey 50–950, and four
semantic families with `-light` / base / `-dark` steps. Exact hexes in
`references/palette.md` and `frontend/src/app/globals.css`.

Two notes that matter:

- **Grey is warm and purple-tinted on purpose.** `#5F5A68`, not `#6B7280`. Do not
  substitute Tailwind's `gray`/`zinc`/`slate`.
- **Warning is hue 28° while brand gold is hue 40°.** That gap is deliberate so an
  "elevated risk" badge is never confusable with a gold brand accent on the same
  screen. **Never close that gap** by using gold for warning or warning for emphasis.

### Layer 2 — role tokens (the light/dark contract)

**The whole app is purple-tinted in both modes.** Light mode is a light purple
family; dark mode is a *dark purple* family — **not** neutral greys. A near-black
canvas under a purple shell reads as a generic dashboard with a brand bar stuck on
top, which is precisely what this replaced.

| Role | Light | Dark |
|---|---|---|
| `--background` | `#FFFFFF` | `purple-900` `#1D1825` |
| `--foreground` | `grey-900` | `purple-50` |
| `--card` / `--popover` | `#FFFFFF` | `purple-800` `#2E273A` |
| `--muted` | `purple-50` | `purple-700` |
| `--muted-foreground` | `grey-600` | `purple-300` ← floor; not `grey-500`/`purple-400` |
| `--border` / `--input` | `purple-100` | `purple-700` |
| `--primary` | `purple-600` | `purple-200` ← **must differ from `--muted-foreground`** |
| `--primary-foreground` | `grey-50` | `purple-900` |
| `--accent` (**neutral** hover) | `purple-200` | `purple-500` ← **must differ from `--muted`** |
| `--brand-accent` (gold) | `gold-500` | `gold-400` |
| `--ring` | `purple-600` | `purple-200` (tracks `--primary`) |

The dark ladder is **shell `purple-600` → canvas `purple-900` → card `purple-800`**:
the chrome is the lightest and most dominant, the canvas drops a shade below it, and
cards lift back toward the shell so content reads as raised. Light mirrors it —
shell `purple-100`, canvas white, cards white.

**`--accent` is not the brand accent.** shadcn uses `--accent` as the subtle hover
surface on every ghost/outline button and menu item. Mapping gold there puts gold on
every hover and destroys the one-gold-per-screen rule. Gold lives in the separate
`--brand-accent*` tokens, which are used deliberately and rarely.

The two "floor" notes are measured, not stylistic: `grey-500` on a dark card is 4.16:1
and `purple-400` on a dark card is 4.43:1 — both fail AA for body text. Step lighter.

### The brand shell — flips with the mode

The shell (sidebar + top bar) is `purple-100` in light and `purple-600` in dark. It
does **not** stay dark in both. An earlier build pinned it to a dark purple in both
modes; in light mode that gave a heavy dark slab against a white page, which is not
"light mode".

| | Light shell (`purple-100`) | Dark shell (`purple-600`) |
|---|---|---|
| label | `purple-900` 14.46:1 | `grey-50` 8.30:1 |
| muted label | `purple-600` 7.15:1 | `purple-200` 5.75:1 |
| gold accent | **`gold-800`** 6.11:1 | **`gold-300`** 5.02:1 |
| active fill | `purple-200` | `purple-800` |

**Gold moves opposite to its backdrop.** As the shell lightens, gold must *darken*:
`gold-700` on `purple-100` is 4.01:1 and fails, `gold-800` is 6.11:1. As the shell
darkens, gold must lighten: `gold-400` on `purple-600` is 4.15:1 and fails, `gold-300`
is 5.02:1. **No single gold works on both shells** — this is why `Fillet` resolves its
colour from `--sidebar-accent` / `--brand-accent` rather than a fixed ramp class.

**Active nav item:** the fill is one ramp step from the shell in either mode (1.24:1
light, 1.67:1 dark), so it is a recess, not the signal. The **gold rule** carries the
active state. The brand device and the state indicator are the same object.

**Anything placed on the shell must invert with it.** A fixed ramp value disappears in
one mode: the avatar disc was `bg-purple-600` (invisible on the dark shell), then
`bg-grey-50` (invisible on the light one). It is now `bg-primary` /
`text-primary-foreground`, which contrasts in both (7.15:1 light, 3.88:1 dark).

### Dark-mode risk accents are lifted

The `-accent` steps (icons, dots, borders) are `color-mix(… X 70%, X-light)` in dark.
The `purple-800` card is lighter than the `grey-900` it replaced, which dropped the raw
`danger` base to **2.55:1** — under the 3:1 non-text floor. Lifted 30%, all four clear
it: danger 3.95, info 4.87, low 5.29, elevated 6.24.

## Color discipline (the 90 / 8 / 2 rule)

From the brand rationale, made enforceable:

- **~90% neutral.** Surfaces, text, borders, dividers, disabled states.
- **~8% purple.** Primary actions, navigation, focus rings, selected states.
- **~2% gold.** Gold used broadly stops meaning anything.
- **Semantic colors are for risk and system state only. Never decorative.**

**Gold has two distinct jobs — don't collapse them.** Getting this wrong once already
produced a UI where gold was effectively absent:

1. **Structural (always present).** The **fillet** under the wordmark and every page
   heading, and the active-nav rule. This is the brand's signature and the colour
   system sets it on *every* section head — it is not "an emphasis element" and the
   one-per-screen limit does not apply to it. A screen with no gold at all is off-brand,
   not disciplined.
2. **Emphasis (at most one per screen).** A CTA, a highlighted key data point, a
   destination-port pin. This is where "one gold element per screen" bites. Use the
   `--brand-accent*` tokens.

Purple and gold are the *two* founding colours. If a screenshot shows only purple and
neutral, the implementation is wrong regardless of how correct the tokens are.

**Gold's contrast trap:** `gold-500` on white is **2.49:1** and on `grey-100` is
**2.29:1** — it fails the 3:1 non-text boundary. So on light surfaces: a gold fill
needs a `gold-600` border (3.38:1) to have an edge, gold *text* must be `gold-700`
(4.82:1), and a bare gold hairline on white is decorative only and may not carry
meaning. On the purple-900 shell, `gold-400` is safe for both text and rules.

## Risk severity mapping (the highest-value table here)

Name tokens by **risk meaning**, not by color — the UI says "critical", not "red".

| Risk state | Family | Light: surface / text / accent | Dark: surface / text / accent |
|---|---|---|---|
| Critical | danger | `danger-light` / `danger-dark` / `danger` | `danger@18%` over card / `danger-light` / `danger` |
| Elevated | warning | `warning-light` / `warning-dark` / `warning` | `warning@18%` / `warning-light` / `warning` |
| Low | success | `success-light` / `success-dark` / `success` | `success@18%` / `success-light` / `success` |
| Monitoring | info | `info-light` / `info-dark` / `info` | `info@18%` / `info-light` / `info` |

Validated: light badge text 5.41–8.05:1; dark badge text 10.58–12.23:1 over the
composited tint. Dark surfaces are `color-mix(in oklab, var(--color-danger) 18%, var(--card))`.

**A role token is only validated against the surfaces you measured it on.** The
`-text` steps were sized against `--card` and then used on `--muted` wells, where
danger dropped to 3.81:1 — `--muted` is the LIGHTER dark surface, so it sets the floor.
Measure a text token against the lightest surface it can land on, not the commonest.

**`--destructive` is a FILL, not a text colour.** White on it is 5.61:1; as text on the
dark card it is 2.55:1. Destructive *text* uses `--risk-critical-text`. The "Error
loading Google Maps" message was the least legible text on the page.

**A ramp step used as a fill can collide with any surface token.** Dark `--muted` is
`purple-700`, the same step a workflow node used — the swatch measured 1.00:1 against
its own background. Fills drawn from the ramp (node types, categorical swatches) need
their own delineation (a ring or border), because you cannot know what surface they
will end up on. Verified via the audit; see #25.

**`-fg` vs `-text` — two different jobs.** `-fg` is text sitting ON its own tinted
`bg-risk-*` surface. `-text` is severity text standing alone on a plain card. In light
mode they coincide; **in dark they must not**. The dark `-fg` tints are ~90% lightness
by design, so on a card all four collapse into the same off-white and severity stops
being readable at a glance — in an alerting product, that is the whole product failing
quietly. `-text` lifts 55/45 toward the tint, keeping hue while clearing 4.5:1
(danger 4.98, monitoring 6.00, low 6.42, elevated 7.20). `getRiskColor` returns `-text`.

**Bucket boundaries must match the label function.** `severityLabel` has four buckets
and `getRiskColor` briefly had three, so a 0.1-severity event read "Medium" in the
Low/green family — a caution painted as good news. Any change to one must change both.

Three rules that fall out of the audit:

1. **Base semantic colors are not body text on white.** `warning` on white is 3.05:1
   and `success` is 4.08:1 — both fail AA. Use the `-dark` step for text; the base step
   is for icons, dots, and borders (all ≥3:1).
2. **The `-light` tints are unusable as dark-mode surfaces** (they're near-white). Dark
   mode composites the base color over the card instead — never swap the tint in.
3. **Severity is never carried by color alone.** Badge borders measure 1.5–2.5:1
   against their surfaces, so the chip edge is not a reliable signal — and colorblind
   users get nothing from hue. Every severity indicator carries a **label and/or icon**.
   This is a hard accessibility requirement, not a preference.

## Typography

**`<body>` needs an explicit `font-sans`.** Tailwind's preflight sets the base family
on `<html>` from `--default-font-family`, which resolves to `var(--font-geist-sans)` —
and `next/font` declares that variable on `<body>`, not `:root`. Without `font-sans` on
the body element the entire app renders in `ui-sans-serif`/`system-ui` with the brand
font downloaded and unused. Same root cause as the token rule below, different path.

**Font tokens MUST be declared inside `@theme inline`, never plain `@theme`.**
`next/font` puts `--font-cormorant` et al. on `<body>` via its `.variable` classes.
A plain `@theme` emits `--font-display: var(--font-cormorant)` into `:root`, where
that variable does not exist — the token computes to *guaranteed-invalid*, inherits
down invalid, and every `font-family: var(--font-display)` silently falls back to
system sans. `inline` substitutes the reference into the utility, so it resolves on
the element, where the variable is defined.

This shipped broken for several rounds: the utilities emitted, the build passed, and
`grep` found `.font-display` in the CSS — the wordmark, every page heading and every
mono eyebrow were rendering in fallback sans the whole time. **Verify fonts with
`getComputedStyle(el).fontFamily` in the browser, not by checking the CSS emitted.**
`contrast-audit.mjs` now asserts the placement.

The palette alone won't de-genericize the UI; the type pairing does most of that work.

| Role | Face | Usage |
|---|---|---|
| Display | **Cormorant Garamond** 600, often *italic* | Page titles, section heads, the wordmark. Classical, matches the Pericles name. |
| UI / body | **Geist Sans** (keep; brand doc specifies Inter — visually equivalent neo-grotesque) | Everything functional. |
| Data / eyebrow | **IBM Plex Mono** 400/500 | Metrics, hex/IDs, timestamps, uppercase eyebrows at 11px / `0.18em` tracking. |

Replace `Geist_Mono` with `IBM_Plex_Mono` and add `Cormorant_Garamond` via
`next/font/google` (see `frontend/src/app/layout.tsx`). Never render a serif display face
below 20px, and never set body copy in the serif.

## The fillet (brand device)

The recurring gold rule from the brand system — a 2px `gold-500` line above a 1px
`gold-500 @50%` line. It marks section heads, the active nav item, and card headers.
It is the cheapest way to make a screen unmistakably Pericles. Ship it as one component
(`components/ui/fillet.tsx`); do not re-hand-roll the divs.

## Shape, elevation, motion

- **Radius** `--radius: 0.625rem` (10px) for cards/blocks, 6px for chips and swatches,
  full for pills. Already correct in the repo — don't churn it.
- **Elevation is borders + tint, not drop shadows.** Light: `border-border` on white.
  Dark: `grey-900` card on a `grey-950` canvas, `grey-800` border. At most one soft
  shadow per screen (a floating overlay). Stacked shadows read as generic.
- **Motion** 120ms micro-interaction, 200ms surface, 320ms overlay, all `ease-out`.
  Every transition pairs with `motion-reduce:transition-none`.

## Light / dark implementation

Add **`next-themes`** (not installed yet):

```tsx
// app/layout.tsx
<html lang="en" suppressHydrationWarning>   // required: the script mutates <html>
  <ThemeProvider attribute="class" defaultTheme="system" enableSystem
                 disableTransitionOnChange>
```

Non-negotiables:

- `suppressHydrationWarning` on `<html>`, or React logs a mismatch every load.
- `color-scheme: light` / `dark` on `:root` / `.dark` so **native** controls, scrollbars
  and form widgets follow the theme — this is what makes iOS/Android inputs stop
  looking wrong in dark mode.
- Per-mode `themeColor` in the Next.js `viewport` export, so the Android Chrome address
  bar and iOS Safari chrome match the app rather than flashing white.
- Default to **`system`**, persist the user's explicit choice, and offer
  light / dark / system in the toggle. Do not force dark.
- The existing 401 `dark:` classes become live the moment the class is applied — expect
  the first toggle to expose ugly pairs. Migrate them to role tokens (below) rather
  than patching `dark:` variants.

Reference implementations: `frontend/src/providers/theme-provider.tsx`,
`frontend/src/components/layout/theme-toggle.tsx`, `frontend/src/app/layout.tsx`.

## Responsive & device rules

`pericles-mobile` puts a **Next.js PWA over `frontend/` as the preferred V1 mobile
client** — so the responsive layer *is* the iOS/Android app. Treat phone as a first-class
target, not a fallback.

**Mobile-first, always.** Base classes are the phone; `sm:`/`md:`/`lg:` add. Tailwind v4
breakpoints: `sm` 640 · `md` 768 · `lg` 1024 · `xl` 1280 · `2xl` 1536.

**Touch**
- Minimum hit area **44×44 px** (Apple HIG) / 48dp (Material) — `min-h-11 min-w-11`.
  This is the single most common failure when a desktop UI is shrunk.
- Tailwind v4's `hover:` already compiles under `@media (hover: hover)`, so hover styles
  won't stick on touch — but **no affordance may be hover-only.** If a row action is
  revealed on hover, it needs a persistent control on touch.
- `-webkit-tap-highlight-color: transparent` plus an explicit `active:` state.
- `overscroll-behavior: contain` on scrollable panels — otherwise Android pull-to-refresh
  and iOS rubber-banding fire mid-scroll.

**Viewport & safe areas (iOS)**
- Use **`dvh`/`svh`, never `vh`** — `100vh` is wrong under the iOS Safari toolbar and
  cuts off content. Full-height shells are `h-dvh`.
- `viewportFit: 'cover'` + `env(safe-area-inset-*)` padding on the top bar, bottom nav,
  and any fixed sheet, or the notch/home indicator overlaps them.
- **Inputs must be ≥16px** (`text-base`) on mobile, or iOS Safari auto-zooms on focus
  and never zooms back.

**Layout transforms** (not just reflow)
- Sidebar → bottom tab bar or a drawer sheet below `md`.
- Data tables → stacked cards below `md`. A horizontally scrolling table is a last
  resort and must be an explicit `overflow-x-auto` container, never a body scroll.
- **Atlas**: full-bleed map with the events feed as a draggable bottom sheet (this is
  also what issue #8 asks for). Set `gestureHandling: 'greedy'` on the Google Map so
  one-finger pan works, and keep the layer/filter controls out of the safe-area zone.
- **Plans / reactflow**: enable `panOnScroll` + pinch zoom, and give nodes touch-sized
  handles; the default handles are unusable on a phone.

**Test matrix** — iPhone SE (375), iPhone 15 Pro (393), Pixel 8 (412), iPad (768/1024),
desktop (1440). Each in **both** themes. A change isn't done until 375px in dark mode
looks right.

## Migration path (staged — do not big-bang 1,372 classes)

1. **Land the token layer.** Ship the token system in `frontend/src/app/globals.css` —
   the shipped file is the reference, there is no template copy (GH #35). Ramps
   are additive; nothing breaks.
2. **Alias `gray` → brand grey.** Setting `--color-gray-*` to the brand grey values
   re-hues all 226+125+… existing `text-gray-*` usages to the warm neutral **with zero
   code churn**. Biggest visual win per line changed; do it in the same PR as step 1.
3. **Ship the provider + toggle**, then walk surfaces fixing what the first toggle
   exposes.
4. **Migrate risk colors by hand** — `red/green/amber/blue-*` → the risk role tokens.
   These are semantic, so no alias shortcut exists; they carry meaning and deserve the
   review.
5. **Convert remaining `gray-*` → role tokens** (`text-muted-foreground`, `bg-card`,
   `border-border`), deleting the paired `dark:` class as you go.
6. **Close the door:** once step 5 is done, set `--color-gray-*: initial` (and the other
   unused default families) so `bg-slate-500` becomes a nonexistent class and the theme
   can't regress.

## Surface hierarchy — the migration's biggest trap

A bulk `gray-*` → role-token sweep destroys **relative** distinction. `bg-gray-50`,
`bg-gray-100` and `bg-gray-200` all collapsing to `bg-muted` is individually
defensible and collectively broken: it produced a skeleton whose shimmer bars were the
same colour as their container, avatar discs that vanished into their rows, and
"Off" chips indistinguishable from the card behind them.

Keep three distinct levels, and never put an element on a surface of its own colour:

| Level | Token | Element sitting *on* it |
|---|---|---|
| Page canvas | `bg-background` | cards |
| Card | `bg-card` | text, inset panels |
| Inset / sunken | `bg-muted` | use `bg-muted-foreground/20` for discs, bars, skeletons |

**`--accent` must never equal `--muted`.** They were identical twice (both
`grey-100`, later both `purple-50`), which silently killed every
`hover:bg-accent` on a muted surface. Hover is one step *toward* the viewer:
`purple-50 → purple-200` light, `purple-700 → purple-500` dark.

**`bg-muted` is a surface, not a fill.** It is ~1.1:1 against the card, so anything
relying on it to be *seen* — switch off-tracks, progress tracks, timeline connectors —
disappears. Controls need 3:1 (WCAG 1.4.11): use `bg-muted-foreground/70` (3.31:1
light, 3.98:1 dark). Decorative tracks can use `bg-muted-foreground/25`.

**Never put a label on a `-accent` step.** `intelligence-utils.ts` says so and the
same PR then broke it: white on the *lifted* dark danger accent is 3.62:1. Destructive
buttons use `--destructive` (raw danger, white at 5.61:1 in both modes).

Corollaries worth checking by grep, because the compiler cannot:
- `bg-background` inside a `bg-card` dialog is invisible in **light** mode (both are
  `#FFFFFF`). Insets go to `bg-muted`.
- `hover:bg-muted` on an element already `bg-muted` is a dead hover. Same for
  `hover:text-muted-foreground` on `text-muted-foreground`. Hover goes to
  `bg-accent` / `text-foreground`.
- A `dark:` override that resolves to the surface behind it (`dark:bg-card` on a chip
  inside a card) erases the element in one mode only.

## Third-party surfaces the token system does not reach

Some surfaces are outside the cascade and will silently break on theme switch:

- **Google InfoWindow** (`.gm-style-iw-c`) is always white and the map style array
  can't theme it, but its content renders in the app DOM where `.dark` applies. Use
  **ramp** classes (`text-grey-900`) there, never role tokens. Re-scoping `--foreground`
  on the bubble does *not* work — it is resolved into `--color-foreground` at `:root`.
- **Google Maps object colours must flip with the mode too**, not just the map
  style. `PERICLES.purple` #524765 tops out at **2.45:1 against pure black**, so a
  purple-600 supplier pin can never clear 3:1 on *any* dark map — the fix is the pin,
  not the land. See `MAP_COLORS` / `mapColors(isDark)` in `atlas-brand.ts`.
- **reactflow** takes literal colours for `Background`, `MiniMap` `nodeColor`, and
  `connectionLineStyle`. These must be kept in sync with the node header classes by
  hand; a className sweep will not touch them, and a mismatch means the minimap shows
  a different legend from the canvas.
- **PWA chrome** (`themeColor`, `manifest.theme_color`) can't read CSS variables and
  can't follow next-themes. Because the shell is purple-600 in both modes, use one
  value for all three; keying `themeColor` on `prefers-color-scheme` makes the browser
  chrome follow the OS while the app follows the user's choice.

## One scale, one family

The bottom of the severity scale must be the **same risk family everywhere**.
`SEVERITY_CONFIG[1]`, `getRiskColor`, `getRiskBgColor`, `RiskBadge level="low"` and the
dashboard's `calculateRiskLevel` all describe the same thing; two of them once used
Monitoring (blue) while three used Low (green), so a 0.2-severity event was green on
the dashboard and blue in the event list. They are all **Low** now.

## Literal colours need a mode, and a hook

Anything that can't read a CSS variable — Google Maps, reactflow, canvas — needs the
resolved mode at **first paint**. `useResolvedDark()` combines next-themes'
`resolvedTheme` with the `dark` class next-themes already wrote on `<html>`, via
`useSyncExternalStore`. Do not read the DOM in a `useState` initializer: the React
Compiler bails out of optimising the whole component ("Existing memoization could not
be preserved").

## What this forbids

Default Tailwind palette classes (`gray`, `slate`, `zinc`, `indigo`, …) in new code;
raw hex or `oklch()` in a component; ramp utilities for ordinary UI surfaces; gold used
for more than one element per screen or for any risk state; semantic colors used
decoratively; severity conveyed by color alone; `vh` units; hover-only affordances;
sub-44px touch targets; `<16px` inputs; adding a `dark:` variant pair instead of using a
role token; a new drop shadow on a card; a serif face in body copy.

## Verification

- **Both founding colours are actually on screen.** `grep -rn "Fillet\|brand-accent\|
  sidebar-accent" frontend/src --include=*.tsx` returns real call sites, not just the
  component definition. A token that is defined but never consumed is not shipped —
  check the rendered screen, not the stylesheet.
- `node .claude/skills/pericles-branding-ui/references/contrast-audit.mjs` passes — it
  asserts every published light/dark pair against WCAG AA (4.5:1 text, 3:1 non-text).
  Add a row when you add a token pair.
- `grep -rE '\b(bg|text|border)-(gray|slate|zinc|neutral)-[0-9]' frontend/src` returns
  nothing new versus the baseline (1,372 at 2026-07-28, trending down).
- No raw hex/`oklch()` outside `globals.css`.
- Toggling light → dark → system leaves no unreadable text and no flash on reload.
- Every severity indicator has a text label or icon, verified with a grayscale
  screenshot.
- 375px wide, dark mode: no horizontal body scroll, no clipped safe-area content, all
  interactive targets ≥44px.
- `npm run lint` + `npm run build` in `frontend/`.

## Existing standards (read alongside)

`.claude/rules/08-frontend.md` (component pattern, Tailwind class ordering, WCAG AA);
`pericles-frontend-foundations`; `pericles-mobile`; `pericles-atlas-ui` (map surface);
GitHub issue **#17** and its two attachments (`pericles-color-system.html`,
`pericles-theme.css`), mirrored in `references/palette.md`.

## Open questions

- **Geist Sans vs Inter** for UI body — the brand doc specifies Inter; Geist is already
  wired and visually equivalent. Kept Geist to avoid churn; confirm with design.
- **Persistent purple-900 chrome in light mode** — validated for contrast and it's what
  makes the app distinctive, but it's a heavier light mode than a white-shell app.
  Designer call; tokens support either.
- `components.json` still says `baseColor: "neutral"`; harmless (generation-time only)
  but worth switching so newly-added shadcn components come out brand-correct.
- **Phone rendering is not yet visually verified.** The responsive rules are applied
  and compile (`pointer-coarse:min-h-11`, `pt-safe`/`pb-safe`, `h-dvh`, `gestureHandling:
  'greedy'`), and there is no horizontal overflow at desktop width — but no screenshot
  at 375/390px has been taken, and no real iOS or Android device has been checked.
  Safe-area insets in particular only report real values on a notched device.
- **PWA icons are missing.** `app/manifest.ts` deliberately omits `icons` because no
  brand icon assets exist in `public/`. Until a 192px and a 512px icon are added the
  app renders fine but is **not installable** on either platform.
- The workflow node palette uses `purple-500/600/700` + `grey-600/800`, which are close
  in hue; node type is carried mainly by icon and label. If users report confusion,
  this is the place to add a second differentiator (shape or border), not more colour.

## Changelog

- 2026.07.12 — Ninth round (two reviews, one with `--fix`). The `--fix` agent found
  that my previous fix was **dead on arrival**: `border-muted-foreground/70` sat in
  `cn()`'s base string and tailwind-merge dropped it for the `border-input` argument
  that followed — verified with `twMerge()` directly. Border colours must go on the
  branch that wins, not the base. Also fixed here: `--destructive` used as TEXT was
  2.55:1 on the dark card (the map-error message); `-text` tokens on `--muted` wells
  were below AA until lifted 55→60%; the `aria-invalid` ring was left on the un-lifted
  `--destructive` while its border had moved to the lifted accent; switch tracks got a
  `border` that shifted the knob off-centre (now `ring-1`, which costs no layout);
  reactflow's attribution chip and default edge stroke were never themed. The audit
  gained assertions for all of these — it had been measuring `-text` only against
  `--card`, and had no light-mode fillet row at all. One trap was **retired with
  reasoning**: `-text` on its own tinted surface no longer fails AA after the lift, so
  the rule is now semantic (`-fg` is 9.74:1 vs 5.54:1), not a contrast failure.
- 2026.07.11 — Eighth review (`/code-review xhigh`), 14 findings; 12 real, 1 rejected,
  1 deferred. The bad one: **`STATUS_CONFIG` paired `bg-risk-*` surfaces with `-text`
  instead of `-fg`** (critical chip 4.39:1, under AA) — my earlier `-fg`→`-text` sweep
  matched line-by-line and `bgColor`/`textColor` sit on *separate* lines, so the
  "no bg on this line" guard never saw the pairing. Also: all five workflow node
  colours were under 3:1 against the dark canvas, one at exactly 1.00:1; the skill's
  own `templates/` had drifted from the shipped code (still teaching the pre-rename
  `--sidebar-accent` gold); and the audit had three stale rows asserting `--primary`
  was purple-300 while printing "all checks pass". The audit now **parses globals.css
  and asserts its own token→ramp assumptions** — verified by breaking a token and
  watching it fail. **Rejected one finding**: the `handleMapClick` dependency array is
  required; reverting it to `[]` fails `react-hooks/preserve-manual-memoization`,
  tested directly.
- 2026.07.10 — Seventh `/code-review high` (`--fix`). The reviewer found that
  **`<body>` never had `font-sans`**, so the whole app rendered in system-ui with Geist
  loaded and unused — the same failure mode as the `@theme inline` fix one round
  earlier, on the preflight path I hadn't checked. Worse: in dark mode the four risk
  `-fg` tints are ~90% lightness, so **all severity text on cards read as the same
  off-white** — severity was no longer distinguishable at a glance. Added a distinct
  `-text` token layer for standalone severity text. Also: `getRiskColor`'s buckets
  didn't match `severityLabel` (a 0.1 "Medium" event painted green); the tap-highlight
  suppression covered only Button and nav links, so the platform default is restored
  rather than shipping partial feedback; and `viewportFit: 'cover'` had no horizontal
  or bottom insets, so in landscape the header, nav rail and Atlas overlays sat under
  a 44px notch — now applied additively via `pl-safe`/`pr-safe` and `max()`.
- 2026.07.9 — Sixth `/code-review high`; 9 findings, all real. The dark map painted
  land in `purple-600` — byte-identical to the supplier-pin fill — and the arithmetic
  showed purple-600 cannot reach 3:1 on *any* dark surface, so map object colours are
  now mode-aware (`MAP_COLORS`). Also: the bottom of the severity scale disagreed
  between surfaces (blue vs green); `-webkit-tap-highlight-color: transparent` had
  removed touch press feedback with no replacement (`active:opacity-80` added);
  the workflow canvas still had the first-paint theme flash Atlas had already fixed
  (both now use `useResolvedDark`); switch on/off were both mid-dark purples; and
  `SEVERITY`/`severityColor()` were dead code carrying a false docstring.
- 2026.07.8 — Fifth `/code-review high`. **The typography never rendered.** The
  three font tokens sat in plain `@theme`, so they resolved at `:root` where
  `next/font`'s vars aren't defined — Cormorant and IBM Plex Mono fell back to
  system sans from the first commit, and my earlier "serif headings verified" claim
  was wrong: I had checked that the utility *emitted*, not that it *resolved*. Also
  fixed: `pb-safe` replaced `py-4`'s bottom padding (same layer, later wins) so the
  nav had zero bottom padding on every non-notched device; the Atlas feed's severity
  dot and label still used the map-marker hexes, which are 2.55:1 on the dark card;
  and the map passed `styles: undefined` until the theme resolved, flashing Google's
  stock roadmap on every load. Audit now asserts font-token placement.
- 2026.07.7 — Fourth `/code-review high`; 9 findings, all real, several introduced
  while fixing round three. Same root shape again — **`--primary` and
  `--muted-foreground` were both `purple-300` in dark**, so `text-primary` links were
  indistinguishable from muted text and toggle on/off differed only by alpha (primary
  is now `purple-200`). Atlas had two identity collisions: a subsidiary colour equal to
  `SEVERITY.medium` and another equal to the supplier-pin fill — the palette is
  rebuilt with an explicit exclusion list and the audit now asserts it. Dark map land
  and water were 1.03:1 (no coastlines). `aria-invalid` borders used the unlifted
  `--destructive` (2.55:1). `Fillet`'s vertical `h-full` beat the caller's `inset-y-1`
  and overhung the nav item. The theme dropdown never marked the active option.
- 2026.07.6 — Third `/code-review high`; all 12 findings verified and real. The
  recurring shape is **two distinct states resolving to the same token**:
  `--accent` was identical to `--muted` (dead hovers), pills matched the cards
  containing them, badges matched their log container, and `bg-muted` fills
  (switch off-tracks, progress tracks) were ~1.1:1 against the card. Also fixed:
  white on the lifted dark danger accent was 3.62:1 (destructive buttons now use
  `--destructive`), the manifest locked the PWA to portrait (WCAG 1.3.4), the
  active-nav rule was hand-rolled instead of using `Fillet` — which this skill
  explicitly forbids — and several comments still described the old
  purple-600-in-both-modes shell.
- 2026.07.5 — **Dark mode was black, not purple.** The canvas/cards were
  grey-950/grey-900, so the purple shell floated on a neutral void and the app read
  as a generic dark dashboard. Dark mode is now a purple family (canvas purple-900,
  cards purple-800, shell purple-600) and **the shell flips with the mode** rather
  than staying dark — light is purple-100, resolving the open question about a heavy
  light mode. Knock-ons, all measured: gold must move *opposite* to its backdrop
  (gold-800 light / gold-300 dark — no single value works), the avatar disc must
  invert with the shell, and the dark risk `-accent` steps needed a 30% lift because
  the lighter purple card dropped `danger` to 2.55:1.
- 2026.07.4 — Fixes from two independent `/code-review high` passes; all 12 findings
  verified against the code and real. Added the **Surface hierarchy** and **Third-party
  surfaces** sections, which are where the damage was: collapsing three grey steps onto
  `bg-muted` made skeleton bars, avatar discs and "Off" chips invisible; role tokens in
  Google's always-white InfoWindow gave white-on-white in dark mode; reactflow's literal
  hexes still showed the pre-migration red/blue/teal legend. Also: `pt-safe` on the
  header broke the `top-16` assumption in the nav and full-bleed pages (now one
  `--app-header-h` variable), the iOS 16px input rule was in `@layer base` where every
  `text-sm` beat it (now unlayered), and the Settings theme picker was inert while
  claiming "Light". Introduced `useMounted()` (useSyncExternalStore) because the
  `useState`+`useEffect` mount idiom trips the repo's `react-hooks/set-state-in-effect`.
- 2026.07.3 — **Purple was missing too.** The shell had been set to `purple-900`,
  which renders as near-black, so the brand's *dominant* colour never appeared —
  the app read as a generic dark dashboard with a gold hairline. Shell moved to
  `purple-600` in both modes. Knock-ons found by doing it: gold on the shell must
  step to `gold-300` (gold-400 is 4.15:1, fails AA), and the `bg-purple-600` avatar
  went invisible against the new shell and is now an inverted grey-50 disc. Two new
  traps pinned in the audit.
- 2026.07.2 — **Gold was missing from the shipped UI.** All 43 ramp values matched the
  ticket exactly, but `Fillet`, `RiskBadge` and every `--brand-accent*` token were
  defined and never mounted, so gold rendered in exactly one place app-wide and the
  product read as monochrome purple. Root cause was applying "one gold element per
  screen" to the *structural* fillet as well as to emphasis; the colour system puts a
  fillet under every section head. Rule split into structural vs emphasis, fillet
  mounted on the wordmark and all 13 page headings, `RiskBadge` mounted, and a
  "both founding colours are on screen" check added to Verification.
- 2026.07.1 — Migration executed on `feature/17-brand-ui-migration`; ground truth
  rewritten to the post-migration state. Two corrections found by building it for
  real: **`--accent` must stay neutral** (shadcn uses it as the ghost/outline hover
  surface — gold there put gold on every hover), so brand gold moved to
  `--brand-accent*`; and **categorical colours are not risk colours** — the first
  scripted pass mapped workflow node types onto risk tokens, making a Trigger node
  read as "critical". Also resolved the dark Google Maps style and the chart palette,
  which were open questions.
- 2026.07.0 — Initial draft for issue **#17**. Palette and rationale taken from the
  issue's `pericles-color-system.html` + `pericles-theme.css`; every light/dark pair
  contrast-checked (`references/contrast-audit.mjs`, 8 initial failures found and
  designed around); reconciled against the live `frontend/` audit (1,372 default-palette
  classes, 401 dead `dark:` classes, no theme provider).

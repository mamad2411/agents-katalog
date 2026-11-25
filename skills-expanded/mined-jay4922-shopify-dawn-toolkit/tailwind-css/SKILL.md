---
name: tailwind-css
description: Team CSS architecture and Tailwind v4 conventions for Shopify Dawn theme projects. Use this skill whenever the user mentions Tailwind, utility classes, css/application.css, styling any section or component, fonts, color schemes, breakpoints, overriding Dawn styles, or setting up CSS for a new project — even if they just say "style this" or "set up the project".
---

# Tailwind CSS v4 + Dawn — CSS Architecture

## 0. Mandatory compliance (hard rule)

Every rule in this file applies to every section build from a Figma link — no partial follow, no skipping because a section "seems simple." Covers at minimum: `@apply`-by-default, no arbitrary color/font values, registered-token breakpoints only, full-range responsive coverage, global h1–h6/`.content`/`.ctm-title` classes, global button component, container width, file-scope rules (§2), design recipes (§5). If project setup (§1) hasn't happened yet, do that FIRST — never build a section's CSS ad hoc while setup is missing.

## 1. Project setup (before writing any section)

### 1.1 Design system intake

Analyze the **entire** Figma first and establish the full design system before touching a section — colors, font families/sizes/weights, line heights, letter spacing, border radius, breakpoints, spacing scale, shadows, z-index values, CSS variables. Not just colors/fonts/breakpoints. This is intake work, not backfill — a token discovered mid-build (a shadow, a z-index scale) means retrofitting every section built before it.

### 1.2 File structure & entry point

```
css/
  application.css   ← entry point ONLY: Tailwind import + theme vars + file imports
  base.css          ← global typography, container, root vars, HTML elements, Dawn typography overrides
  components.css    ← reusable UI components only (see Global Components, §2)
  layout.css        ← header, footer, nav, global layout wrappers, grid/flex helpers
  utilities.css     ← utility/helper classes (Dawn default-section overrides live here too)
  app.css           ← 3rd-party app styles (only if needed)
```

`application.css` is compiled by Tailwind CLI to `assets/application.css.liquid` (auto-generated — never edit the output). Import order, always:

```css
@import "tailwindcss";
@import "./base.css";
@import "./components.css";
@import "./layout.css";
@import "./utilities.css";
@import "./app.css"; /* only if needed */
```

`application.css` stays clean: Tailwind import, theme variables, imports above — no component/custom CSS directly in this file.

### 1.2a `package.json` (create at project init, before any CSS)

Copy `references/package.json` (next to this skill) to the theme root, replace the `<project-name>` / `<org>/<repo>` placeholders with the project's values, then run `npm install`. Do not hand-write a new one or pull from another project's `package.json` — the reference is the team standard.

The `build` script is fixed and must be exactly:

```json
"build": "npx @tailwindcss/cli -i css/application.css -o assets/application.css.liquid -w -m"
```

- Input `css/application.css`, output `assets/application.css.liquid` — no other paths.
- `-w` (watch) and `-m` (minify) both required — `npm run build` is the long-running watcher (§6), not a one-off build.
- Don't rename the script, split it into `build`/`watch`/`dev` variants, add a PostCSS/Vite pipeline, or add a `tailwind.config.js` (Tailwind v4 config lives in `@theme` inside `application.css`).

Other scripts/tooling come with the reference as-is: `format` (Prettier + `@shopify/prettier-plugin-liquid` over theme folders), `lint` (ESLint), `prepare: husky` (installs git hooks), and `lint-staged` (on staged `.js`: ESLint fix THEN Prettier, in sequence — never two overlapping globs that run both on the same file in parallel; Prettier alone on `.css/.md/.liquid`).

Copy the rest of `references/` to the theme root at the same time — these are the configs the scripts depend on:

| File | Purpose |
|---|---|
| `eslint.config.mjs` | Lints ONLY `assets/custom*.js` (Dawn's JS ignored). Declares Dawn's globals (`debounce`, `fetchConfig`, `publish`/`subscribe`, `Swiper`, etc.) so `custom.js` doesn't fail `no-undef`. |
| `.prettierrc.json` | Loads `@shopify/prettier-plugin-liquid`. |
| `.prettierignore` | Never formats `assets/application.css.liquid` (minified build output) or Dawn's original `assets/*.js`/`*.css`. |
| `.husky/pre-commit` | Runs `lint-staged`, then `shopify theme check`. Needs Shopify CLI installed globally (`npm install -g @shopify/cli`); the hook stops the commit if it's missing. |

### 1.3 Theme configuration (in `application.css`)

Pixel-based spacing so `px-10` = `padding-inline: 10px`:

```css
--spacing: 1px;
```

Pixel utilities — `text-32` = font-size 32px, `rounded-5` = border-radius 5px:

```css
@utility text-* {
  font-size: calc(--value(integer) * 1px);
}
@utility rounded-* {
  border-radius: calc(--value(integer) * 1px);
}
```

**Breakpoints — always this set, registered in `application.css`. Every breakpoint used anywhere, including Dawn-native widths (990/750), must be a named `--breakpoint-*` token here before use — no exceptions live outside this scale:**

```css
--breakpoint-1920: 1921px;
--breakpoint-1600: 1601px;
--breakpoint-1512: 1513px;
--breakpoint-1440: 1441px;
--breakpoint-1366: 1367px;
--breakpoint-1199: 1200px;
--breakpoint-1024: 1025px;
--breakpoint-992: 993px;
--breakpoint-768: 769px;
--breakpoint-750: 750px;
--breakpoint-640: 641px;
--breakpoint-576: 577px;
--breakpoint-480: 480px;
--breakpoint-425: 426px;
--breakpoint-375: 376px;
--breakpoint-990: 990px;
```

`990`/`750` are Dawn's own native cutoffs (Dawn's components + the section-padding pattern split at 990px) — separate purpose from the device-label scale above, but registered and consumed identically: bare `990:`/`max-990:`, never bracket syntax. Don't "fix" one scale to match the other; both are real tokens either way. Full breakpoint hard rule (define-then-use, no brackets): **§3**.

A section's own mobile↔desktop layout switch (wrap→nowrap, grid columns, gap) must break at the SAME width as that section's padding query (990px) — a bare `md:`(768)/`lg:`(1024) switch opens a mismatched 768–989px zone (desktop layout, mobile padding) that overflows/clips multi-item rows. Use `990:`/`max-990:` for any layout-switching class, and always check a width in 768–989px, not just phone + wide-desktop.

**Hard rule — 990/max-990 is the structural layout switch only, not a complete responsive solution.** Every section must additionally apply registered named tokens (`768:`, `1024:`, `1199:`, `1366:`, `1440:`, `1512:`) for spacing, gap, typography, and visual fine-tuning at every distinct step across the full device range (mobile → tablet → laptop → desktop). A section limited to only 990/max-990 runs the mobile layout from 0px to 989px and the desktop layout from 990px to 1920px+ with zero adjustment at any intermediate or wide-screen width — this is always incomplete. Full-range coverage: §1.3b.

### 1.3b Full-range responsive coverage (hard rule)

**Never build a section with only two breakpoints — and never limit to 990/max-990 alone.** A Figma handoff gives a mobile frame and a desktop frame, but nothing covers the real device range between them — a naive `max-990`/`990:` split runs raw desktop (or raw mobile) unchecked from 769px to 1439px, which is where most "not px perfect" / "broken on tablet" reports come from.

1. Mobile per the mobile Figma frame (`max-990` and below; refine with `max-576`/`max-425`/`max-375` if the frame itself varies by phone size).
2. Desktop per the desktop Figma frame (`1440:`/`1512:`/`1199:` per the frame's actual canvas width).
3. Every width BETWEEN the frames (`768:`, `992:`, `1024:`, `1199:`, `1366:`) — interpolate a sane layout even with no matching Figma frame; don't let it silently inherit whichever extreme is nearest without checking for overflow/clipping/oversized gaps.
4. Actually render-check a width in each band (~375, 600, 768, 992, 1200, 1440, 1920) before calling a section done — this applies to every build, not just when the user says "responsive."

### 1.4 Dawn cleanup after setup

Remove styles from Dawn's `base.css` that you've redefined (headings, paragraphs, links) — only what you explicitly replaced, verifying the page still works after each removal. Remove interfering code blocks from `theme.liquid` before development.

### 1.5 Fonts (hard rule)

1. Identify every font family in the Figma design.
2. Check Shopify Typography settings FIRST — use it if it's already there; don't add an external link for a font Shopify already has.
3. Not in Shopify but on Google Fonts → official Google Fonts CDN link in `theme.liquid`. Don't self-host unless specifically required.
4. Not on Google Fonts/Adobe → download the files into `assets/`, attach via `@font-face` with `font-display: swap`:
   ```css
   @font-face {
     font-family: "Custom Font";
     src: url("./assets/fonts/custom-font.woff2") format("woff2");
     font-weight: 400;
     font-style: normal;
     font-display: swap;
   }
   @theme {
     --font-global: "Custom Font", sans-serif;
   }
   ```
   Registering in `@theme` (not `:root`) is what makes Tailwind compile the matching utility class (`font-global`) — see §1.7.
5. Either path: define the theme variable, then consume it everywhere via its utility class (`font-global`) — never the font name directly at the call site. No arbitrary inline values (`font-['Helvetica_Neue',...]`); a font name alone isn't usable until the file's in `assets/` and `@font-face` is wired.
6. Font Scale (Theme settings) stays 100% unless explicitly approved.

### 1.6 Colors (hard rule)

- Every Figma color → a variable in `application.css` first (`--color-off-white: #f3f3f3;`), then the token. Never `text-[#020002]`-style arbitrary classes.
- Section background/text colors come from **Shopify color schemes** (Theme settings → Colors: primary/secondary/background minimum) — never hardcoded per section, unless a documented fixed `bg_color` setting (see `shopify-liquid` skill).
- Never default a section's background to white/transparent without checking Figma — e.g. light-blue product sections (`var(--color-light-blue, #e8f4f8)`), cream testimonial sections (`var(--color-cream, #f5f3ea)`), card backgrounds inside coloured sections (`var(--color-card-bg, #faf6ec)`). A split section's right panel shares the outer section's background unless Figma explicitly shows a contrast.

### 1.7 Verify tokens actually work, not just that they're referenced

Fonts and colors fail silently (fallback font, no color, zero console error) when wired wrong:

1. New `--font-*`/theme vars must live inside `@theme { }`, not plain `:root {}` — Tailwind v4 only generates the utility class from vars registered in `@theme`; a `:root` var still works via raw `var()` but the class never compiles. Grep compiled `assets/application.css.liquid` for the expected rule before trusting the class.
2. Every `var(--color-x)` used → grep for its definition; undefined silently falls back to inherited (often a plausible-looking Dawn default).
3. Check whenever adding a new token, not just when something looks wrong — the failure mode is plausible-looking-wrong, not visibly broken.

### 1.8 Typography

`base.css` gets Figma-accurate typography for `h1`–`h6`/`p`/`a`/`body` at setup, immediately — not deferred. Container set from Figma at the same time (§1.10).

**Hard rule: every heading anywhere in the project consumes the global `h1`–`h6`/`.h1`–`.h6` classes below. No section ever redefines or inlines heading font-size/style — no exception.**

```css
::before,
::after {
  @apply box-border;
}
html,
body {
  @apply !scroll-smooth;
}
body {
  @apply p-0 m-0 font-body text-base leading-22 tracking-normal;
  -webkit-font-smoothing: auto;
}
a {
  @apply transition-all duration-300 ease-in-out cursor-pointer font-body tracking-normal;
}
p {
  @apply font-body text-16 leading-22 font-normal text-black-28;
}
h1,
h2,
h3,
h4,
h5,
h6 {
  @apply m-0 outline-0! text-current font-heading font-bold;
}
h1,
.h1 {
  @apply text-36 leading-44 768:text-40 768:leading-44 1199:text-52 1199:leading-56 1512:text-60 1512:leading-64;
}
h2,
.h2 {
  @apply text-28 leading-36 768:text-32 768:leading-38 1199:text-42 1199:leading-48 1512:text-48 1512:leading-54;
}
h3,
.h3 {
  @apply text-22 leading-28 768:text-24 768:leading-30 1199:text-26 1199:leading-32 1512:text-28 1512:leading-34;
}
h4,
.h4 {
  @apply text-20 leading-26 768:text-20 768:leading-26 1199:text-22 1199:leading-28 1512:text-24 1512:leading-30;
}
h5,
.h5 {
  @apply text-18 leading-24 768:text-18 768:leading-24 1199:text-20 1199:leading-26 1512:text-22 1512:leading-28;
}
h6,
.h6 {
  @apply text-16 leading-22 768:text-16 768:leading-22 1199:text-18 1199:leading-24 1512:text-20 1512:leading-26;
}
img {
  @apply overflow-hidden select-none;
}
.img-fluid-cover {
  @apply w-full h-full object-cover;
}
.img-fluid-none {
  @apply w-full h-full object-none;
}
```

Pixel values above always come from THIS project's Figma, not copied verbatim — the pattern is fixed, the numbers aren't.

**Migrating off Dawn's default typography** (Dawn ships its own in `assets/base.css`) when the project uses a custom system: (1) comment out Dawn's typography, don't delete — keep it recoverable; (2) recreate the project's typography via Tailwind's `@layer base` in `base.css`; (3) keep using Shopify CSS variables (`--font-*`, `--color-*`) rather than hardcoded values; (4) define all heading classes (`h1`–`h6`, `.h0`–`.h2`), `.text-body`, `.caption`, `blockquote` globally in `base.css`. The "never redefine per section" rule above applies here too.

### 1.8b Content & title color/size modifiers (hard rule)

At the same setup step as §1.8, define `.content`/`.ctm-title` modifier rules in `base.css` for `h1`–`h6`, `p`, `a`, `ul`, `ol`, `span` — from the Figma color/size variants, not deferred. Fixed structure: a base `.content`/`.ctm-title` class plus modifiers (`.content-white`, `.title-sky-blue`, `.content-medium`, `span.blue`, etc.) that a section applies on a wrapper — never by re-styling `p`/`h*`/`span` locally. Canonical shape (numbers/colors from Figma, names from this project's actual variants — don't copy example names verbatim):

```css
.content p strong {
  @apply font-bold;
}
.content.content-white p {
  @apply text-white;
}
.content.content-black p {
  @apply text-black-28;
}
.content.content-small p {
  @apply text-14 leading-20;
}
.content.content-medium p {
  @apply text-18 leading-24 max-768:text-16 max-768:leading-22;
}
.content.content-large p {
  @apply text-18 leading-28 768:text-24 768:leading-36 1199:text-28 1199:leading-32 1512:text-32 1512:leading-48;
}
.content.content-bold p {
  @apply font-bold font-heading;
}
.content a {
  @apply underline text-sky-blue hover:text-black-14;
}
.content ol,
.content ul {
  @apply list-disc pl-20 space-y-10;
}
.content p {
  @apply 767:mb-20 mb-16 last:mb-0;
}
.ctm-title {
  @apply font-heading;
}
.title-black h1,
.title-black h2,
.title-black h3,
.title-black h4,
.title-black h5,
.title-black h6 {
  @apply text-black-25;
}
.title-white h1,
.title-white h2,
.title-white h3,
.title-white h4,
.title-white h5,
.title-white h6 {
  @apply text-white;
}
span.blue {
  @apply text-sky-blue;
}
```

Build at setup time, same moment as §1.8, not backfilled. Lives in `base.css` (§2 file scope). A section applies `.content`/`.content-{variant}` or `.title-{color}` on a wrapper; it never writes its own `p`/`h*`/`span` color or size CSS.

**Mandatory wrapper structure (hard rule — applies to every section, no exceptions):**

Every `h1`–`h6` in any section MUST be wrapped in a `div` carrying `.ctm-title` + the appropriate color modifier. Every `p`, `a`, `ul`, `ol`, `span` in any section MUST be wrapped in a `div` carrying `.content` + the appropriate variant modifier. The CSS for these targets (`h1`–`h6`, `p`, `a`, etc.) already lives in `base.css` — styles only apply when the wrapper structure is present. Writing a bare `<h2>` or `<p>` without these wrappers means the Figma colors/sizes silently don't apply.

Required Liquid structure:

```liquid
{{- Content / body text -}}
<div class="content content-black">
  <p>{{ section.settings.description }}</p>
</div>

{{- Heading -}}
<div class="ctm-title title-black">
  <h2>{{ section.settings.heading }}</h2>
</div>
```

Rules:
- Color/size variant on the wrapper matches the Figma color for that element in that context — check Figma before choosing the modifier, never assume `black`.
- A section that omits these wrappers and writes inline color/font CSS instead is a hard violation — fix it; don't document it as an exception.
- When a richtext setting is used (`{{ section.settings.body | metafield_tag }}` or similar), the `.content` wrapper is still required — it's what scopes the `p`/`a`/`ul` rules from `base.css` to the emitted HTML.
- Never add both a `.content` wrapper AND local `{% style %}` rules targeting the same `p`/`h*` — pick one; the wrapper is always preferred.
- **Never set `color` or `font-*` as inline `style=""` attributes directly on `h1`–`h6`, `p`, or any other text element.** If an element already has an inline style for color or font, remove it and apply the correct `.content-` / `.title-{color}` modifier class on the wrapper `div` instead. Inline styles on text elements bypass the modifier system, cause specificity fights, and make global color/font changes impossible — the wrapper class is always the right fix.

### 1.9 Global button component (hard rule)

Built once in `components.css` from Figma, reused everywhere — no section-scoped button CSS. One base class carries shape/behavior; variants carry only color/border:

```css
.button,
.ctm-button {
  @apply cursor-pointer transition-all duration-300 ease-in-out font-body min-h-10 max-mdscreen1:min-h-8 w-fit text-[13px] max-mdscreen1:text-[12px] leading-4.5 max-mdscreen1:leading-4 text-center flex justify-center items-center px-6 py-2.5 max-mdscreen1:px-5 max-mdscreen1:py-1.5 rounded-[10px] max-mdscreen1:rounded-[8px] border border-transparent;
}
.btn-white {
  @apply bg-white-1 text-black-1 hover:bg-transparent hover:text-white-1 hover:border-white-1;
}
.btn-black {
  @apply bg-black-1 text-white-1 hover:bg-transparent hover:text-black-1 hover:border-black-1;
}
.button-outline-white {
  @apply bg-transparent text-white-1 border-white-1 hover:bg-white-1 hover:text-black-1;
}
```

A section needing a button applies `.button` + a variant class — it never redefines shape/spacing/radius locally.

### 1.10 Container width

Defined in `base.css` at the same time as typography, from Figma:

```css
.custom-container {
  @apply px-6 1199:px-55 !max-w-full mx-auto;
}
.container-48,
.page-width {
  @apply px-5 1024:px-48 !max-w-full;
}
```

**Dawn's `page_width` theme setting** (Theme settings → Layout, defaults `1200px`, shared by every section using `.page-width`): check it against Figma's actual layout **before the first section**, not after. Derive from Figma: find a full-width section's outer gutter and compute `canvas_width - 2 × gutter`; set `config/settings_data.json`'s `current.page_width` to that value (raise `config/settings_schema.json`'s range `max`/`step` first if outside the default 1000–1600 slider bounds). A mismatch silently narrows every section built afterward — cheap to catch at intake, expensive after multiple sections exist.

### 1.11 JS setup at project init

Create `assets/custom.js` at project init — single shared file for all custom JS, attached in `theme.liquid` so it runs project-wide. Mirrors the CSS pipeline (every CSS file → `application.css` → attached once in `theme.liquid`).

## 2. File scope rules — where CSS goes (strict)

- **Custom sections** → inline Tailwind in the section's Liquid file, unless the pattern repeats elsewhere (→ Global Components below).
- **Dawn default sections** (announcement bar, header, footer, PDP, cart, cart drawer) → overrides in `utilities.css`, kept minimal.
- **h1–h6** → globally in `base.css` per Figma (§1.8's hard rule).
- Buttons/forms/badges/cards → `components.css`. Header/footer/nav → `layout.css`. Plain utility/helper classes → `utilities.css`.

Full scope per file: **`base.css`** — global typography, container, root vars, HTML elements, Dawn typography overrides. **`components.css`** — reusable UI only (buttons, inputs, cards, badges, tabs, accordions, pagination). **`layout.css`** — header, footer, nav, global layout wrappers, grid/flex helpers. **`utilities.css`** — utility/helper classes + Dawn default-section overrides only; never a reusable component (→ `components.css` if used more than once).

### Section `<style>` blocks vs `utilities.css` (hard rule)

Never write generic/static CSS inline in a liquid `<style>` block — it belongs in `utilities.css`/`components.css`/`layout.css` as `@apply` utilities. A `{% style %}` block is only for CSS rendered per-instance from `section.settings`/`section.id` — values Tailwind can't compile ahead of time.

Wrong (static CSS hardcoded in liquid):

```liquid
<style>
  .template-404 .title + * { margin-top: 1rem; }
  @media screen and (min-width: 750px) {
    .template-404 .title + * { margin-top: 2rem; }
  }
</style>
```

Right (moved to `utilities.css`, `@apply` + breakpoint token):

```css
.suite-detail__inner {
  @apply flex items-center justify-between gap-60 max-1199:gap-40 max-992:flex-col max-992:items-start max-992:gap-35 max-w-1243 mx-auto relative z-2;
}
```

Exception — settings-driven CSS: when a build needs CSS driven by that section's own schema settings, it stays in the section's own `{% style %}` block, scoped by `.section-{{ section.id }}-...`, and stays raw CSS (Liquid values never pass through the Tailwind compiler):

```liquid
{%- style -%}
  .section-{{ section.id }}-padding {
    padding-top: {{ section.settings.padding_top | times: 0.75 | round: 0 }}px;
  }
  @media screen and (min-width: 750px) {
    .section-{{ section.id }}-padding {
      padding-top: {{ section.settings.padding_top }}px;
    }
  }
{%- endstyle -%}
```

### Global components

During analysis, identify repeated UI patterns (button variants, product cards, form fields/labels, badges/chips, section spacing, containers, common padding/margin, flex/grid wrappers) and build them once instead of retyping utility strings per section. Rule of thumb: a one-off tweak stays inline; anything recurring in 2+ sections gets promoted to a component class.

## 3. Hard rules (absolute, no exceptions)

**`@apply` by default — raw CSS only where genuinely unmappable.** Every rule in `css/*.css` defaults to `@apply` with real theme utilities. Add a custom `@utility` (see `text-*`/`rounded-*`, §1.3) whenever a scalar value repeats without one. Raw declarations are for the handful of things no utility can express: `calc()` expressions, multi-function `transform` (a single function still uses the utility, e.g. `rotate-180`), multi-property `transition` with custom easing, `::marker`/`::-webkit-details-marker`-type pseudo-elements, one-off bespoke `box-shadow`. Mixing is expected — don't fabricate a contorted arbitrary-value utility just to avoid one raw line. **A section's own `{% style %}` block is exempt entirely** — it's Liquid-rendered per-instance, never Tailwind-compiled, so `@apply` there silently does nothing; those blocks stay raw CSS (documented in CLAUDE.md's error log).

Wrong: `.pages-ctm { line-height: 1; word-break: break-all; }` — Right: `.pages-ctm { @apply leading-none break-all; }`

**Media queries — registered breakpoint tokens only, never bracket syntax.** Never a raw `@media (...)` block; never arbitrary brackets (`min-[990px]:`, `max-[989px]:`, etc.) anywhere, including Dawn-native widths. Two steps, strict order:

1. **Define first** — the value must exist as a named `--breakpoint-*` var in `application.css`'s `@theme` (§1.3) before use. Need an unregistered width? Add the token first, then use it — never a bracket as a shortcut.
2. **Use bare, second** — `768:pt-20`, `990:flex-row`, `max-990:gap-40`. Tailwind auto-generates both the min-width (`768:`) and max-width (`max-768:`) variant from one registered value.

```css
/* Wrong — raw media query */
@media (min-width: 750px) {
  .rail { @apply flex flex-col gap-12; }
}
/* Wrong — bracket syntax */
.footer-row { @apply flex flex-col max-[989px]:gap-40 min-[990px]:flex-row min-[990px]:gap-60; }

/* Right — token registered in application.css (§1.3), then bare
   (syntax example only — shows the no-brackets pattern; a real section also applies
   768:, 1024:, 1199:, 1366:, 1440:, 1512: for full-range coverage per §1.3b) */
.rail { @apply 750:flex 750:flex-col 750:gap-12; }
.footer-row { @apply flex flex-col max-990:gap-40 990:flex-row 990:gap-60; }
```

Find a bracket breakpoint anywhere in the codebase during any edit — not just code you're actively touching — register the missing token and convert it as part of that change.

**No arbitrary color/font values.** Full rules in §1.5/§1.6 — restated here because it's audited on every section: no `text-[#...]`, no `font-['Name',...]`, ever.

## 4. Overriding & working with Dawn

Priority when a Dawn style conflicts with Figma: (1) remove the unnecessary CSS from Dawn's own file, if safe; (2) if not, override via parent-class specificity (`.shopify-section-header .header__menu-item {...}`); (3) `!important` — last resort, sparingly, documented — especially avoid in announcement bar, header/nav, footer, PDP info, cart page/drawer. An override that "should" apply but doesn't is usually a token-registration problem (§1.7), not a specificity problem — check that before reaching for `!important`.

## 5. Design patterns / recipes

**Z-index & layering** — Never add explicit z-index to a content wrapper just to sit above an absolute-positioned bg image, and never layer a decorative image "behind" content with negative `-z-*`. DOM order already guarantees later siblings paint on top; put bg/decorative elements first, content after. Negative z-index on an element inside a `relative overflow-hidden` parent can composite below the parent's own painted background in Chromium — invisible even though computed style looks right. Pattern: bg image → `absolute inset-0` (no z-index); content → `relative` (no z-index). Explicit `z-*` only for intentional cross-section stacking (sticky nav, modal, drawer), documented. If something "isn't showing" despite looking right in devtools, verify with a pixel sample (`getImageData`) before assuming faint/low-opacity.

**Three-layer image stacking** (Figma card: bg photo + product overlay + text) — Tailwind classes per layer:

```
card wrapper:                 relative overflow-hidden rounded-20
  bg image (.fsb-bg-img):     w-full h-full object-cover                → z: auto
  gradient overlay (::before): absolute inset-0                          → z-1
  product overlay (.fsb-product-img): absolute pointer-events-none       → z-2
  text top / bottom:          absolute                                   → z-3
```

Always scope the background `image_tag` (e.g. `.fsb-bg-img`) — without it, a broad `.card img { @apply object-cover; }` also hits the product overlay and breaks its contain-fit.

**Rounded floating card in coloured outer section** — outer section keeps the Figma background color (never default to white) with `p-[clamp(32px,4vw,60px)]`; inner grid `gap` shows that background through as the "floating" effect; the floating card itself gets `rounded-20 overflow-hidden relative`. Do NOT put `overflow-hidden` on the outer wrapper — it clips the card's drop shadow if one is added later.

**Dual-band gradient for text legibility** — Figma hero cards use a light dual-band gradient (top band for heading legibility, bottom band for subtitle/button), NOT a heavy single overlay that darkens the whole image. The multi-stop gradient value itself is the one genuinely unmappable piece (§3) — `@apply` the rest, keep only `content`/`background` raw:

```css
.card::before {
  @apply absolute inset-0 pointer-events-none z-1;
  content: "";
  background:
    linear-gradient(180deg, rgba(0, 0, 0, 0.3) 0%, transparent 45%),
    linear-gradient(0deg, rgba(0, 0, 0, 0.4) 0%, transparent 50%);
}
```

Max opacity: top band ≤ 0.35, bottom band ≤ 0.45 — heavier kills the product photography.

## 6. Build pipeline

- Watcher must be running (`npm run build`) or new utility classes won't compile — check the watcher FIRST if a class has no effect. The `build` script is the fixed watch+minify command from §1.2a; if a project's `package.json` differs, restore it to that exact command.
- Never build class names by string concatenation (`` text-${x}-500 ``) — the compiler can't see them.
- Converting raw CSS to `@apply`: verify, don't assume equivalence — rebuild (`npx @tailwindcss/cli -i css/application.css -o <scratch-file> -m`) and diff the compiled selector's values against the pre-change output. A successful build only proves the syntax parsed. Breakpoint token off-by-ones are the easiest miss — confirm the registered `--breakpoint-*` value matches the literal pixel boundary you mean (`--breakpoint-990: 990px` gives `max-990:` a sub-pixel-below-990 cutoff, matching an inclusive `≤989px` mobile range).

## 7. General rules

- Keep `application.css` clean — imports and theme variables only.
- Keep reusable CSS in the appropriate file, not scattered inline.
- Avoid duplicated utility classes across sections — extract to a component.
- Prefer reusable component classes over repeated one-off utility strings.
- Follow this design-system approach on every project, not just complex ones.

## 8. Audit checklist (used by the qa agent)

This skill is the single source of truth for CSS; the `qa` agent verifies against this list. Flag every ✗.

**Design system intake**
- [ ] Full system established before any section built: colors, fonts (family/size/weight), line height, letter spacing, border radius, breakpoints, spacing scale, shadows, z-index, CSS variables — not just colors/fonts/breakpoints

**`@apply` vs raw CSS / media queries**
- [ ] `css/*.css` defaults to `@apply`; raw declarations only for genuinely-unmappable cases (§3) — not habit
- [ ] No raw `@media (...)` and no bracket breakpoints anywhere — only bare registered `--breakpoint-*` tokens, each defined in `application.css` before use
- [ ] Section built from a Figma desktop+mobile pair covers the full range, not just the two frame widths — tablet/laptop bands (768–1439px) checked and adjusted where the two-frame layout would overflow/clip/gap (§1.3b)
- [ ] `{% style %}` blocks are exempt from `@apply` (flag only if one uses `@apply` and expects it to work — raw CSS there is correct)
- [ ] `assets/custom.js` exists and is attached in `theme.liquid`

**Structure & entry point**
- [ ] `css/` has `application.css`, `base.css`, `components.css`, `layout.css`, `utilities.css` (+ `app.css` only if needed)
- [ ] `application.css` imports base → components → layout → utilities → (app), in order; contains only imports + theme vars
- [ ] `--spacing: 1px;` defined; `text-*`/`rounded-*` custom utilities defined
- [ ] Theme vars (fonts, colors, breakpoints, spacing) defined in `application.css`

**File scope**
- [ ] `base.css`: only global typography, container, root vars, HTML elements, Dawn typography overrides
- [ ] `components.css`: only reusable UI — no Dawn overrides, no one-off section CSS
- [ ] `utilities.css`: only utility/helper classes + Dawn default-section overrides — no components
- [ ] Custom sections use inline Tailwind unless the pattern repeats (then it's a global component)
- [ ] Repeated UI patterns extracted into global components, not duplicated inline across sections

**Fonts & color**
- [ ] Font checked in Shopify Typography before any external link; Font Scale = 100%; custom fonts in `assets/` with `@font-face` + `font-display: swap`
- [ ] Figma fonts/colors defined as variables in `application.css`; no arbitrary `font-[...]`/`text-[#...]`
- [ ] Section background/text colors come from a color scheme or a documented fixed `bg_color` — no ad hoc hardcoded colors
- [ ] Every `font-*`/color class used actually exists in compiled `assets/application.css.liquid` (vars registered in `@theme`, not stray `:root`); every `var(--color-x)` referenced is defined somewhere

**Headings & Dawn typography**
- [ ] h1–h6, `.h0`–`.h2`, `.text-body`, `.caption`, `blockquote` defined globally in `base.css` matching Figma; no inline heading styles in sections
- [ ] Base boilerplate present (`::before/::after` box-border, `html/body` scroll-smooth, `body`/`a`/`p`/`img` base rules, `.custom-container`/`.container-48`/`.page-width`)
- [ ] No section overrides h1–h6 CSS locally
- [ ] Custom typography system: Dawn's default in `assets/base.css` commented out (not deleted); Shopify CSS variables still used
- [ ] `.content`/`.ctm-title` modifiers defined globally in `base.css` per Figma variants — no section restyles `p`/`h*`/`span` locally

**Buttons**
- [ ] Global `.button`/`.ctm-button` base + color variants built once in `components.css`, sourced from Figma
- [ ] No section writes its own button CSS

**Padding (per section)**
- [ ] No static padding on section root — dynamic `.section-{{ section.id }}-padding`; mobile override at `max-width: 989px`; root carries both the padding class and `{{ section.settings.custom_class }}`
- [ ] Any in-component layout switch breaks at the SAME width as this section's padding query (990px) — flag bare `md:`/`lg:` or any bracket breakpoint instead of `990:`/`max-990:`; check 768–989px specifically for overflow/clipping

**Container width & layering**
- [ ] `page_width` matches Figma's derived content width, not left at Dawn's `1200px` default unchecked
- [ ] No decorative element relies on negative `-z-*` inside `overflow-hidden` to sit behind content — use DOM order instead

**Overrides & cleanup**
- [ ] Priority followed: remove conflicting CSS → parent-class specificity → `!important` last; every `!important` flagged
- [ ] Redefined Dawn `base.css` styles removed (only what was explicitly replaced); interfering `theme.liquid` blocks removed
- [ ] No duplicated utility classes across sections that should have been a shared component
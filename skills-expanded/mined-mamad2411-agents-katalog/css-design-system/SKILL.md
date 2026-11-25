---
name: css-design-system
description: >-
  Generate a CSS design-token styleguide for any web project — palette,
  typography scale, spacing, radius, light/dark theme, per-component CSS,
  and (by default) an HTML preview page. Ships seven design systems as
  ready-to-copy CSS blocks in references (Minimal, Material Design 3,
  Uber Base, IBM Carbon, Shopify Polaris, Radix Themes, Maximal). **Before
  writing any file, Claude must first ask the user which of the seven
  systems to use and wait for the answer** — the only exception is when
  the user has already named a system in the triggering message. No silent
  defaults. Once the system is chosen, Claude assembles the files directly
  (no build script). Use this skill whenever the user asks for CSS design
  tokens, CSS variables for a theme, a styleguide, a typography scale, a
  color palette, spacing/radius tokens, a preview of how a named design
  system looks, component CSS (`.btn`, `.input`, `.card`, etc.), or wants
  to apply / compare Minimal / Maximal / Material / Uber / Carbon /
  Polaris / Radix / Fluent / etc. Also use for "refresh the CSS tokens",
  "rebuild theme.css", "set up CSS variables", "show all sizes/colors on
  one page" — even if "styleguide" is never said. Project-agnostic; works
  for React, Vue, Svelte, Angular, or plain HTML/CSS.
---

# CSS Styleguide

Write a CSS design-token styleguide for any web project by assembling ready-to-copy blocks from `references/`. No build script — you write the files directly with the Write tool.

## First action — blocking gate

**Before reading the tree, reading references, or writing any file**, ask the user which of the seven design systems to use. See Workflow §1 for the exact list and wording. The skill is not allowed to proceed past this gate without either (a) an explicit system name in the user's message, or (b) the user's reply to this question. "Just do it" / silent defaulting to `minimal` is a bug, not a shortcut.

## What gets produced

```
<output>/
├── index.css              single import entry point — pulls in everything below, in order
├── primitives/            variable layer only (no classes)
│   ├── palette.css        every color token the system exposes
│   ├── size.css           every dimension token (spacing, radius, button heights, transition, shape scales)
│   ├── typography.css     every type token (families, semantic scale, type roles)
│   ├── extras.css         catch-all for tokens that don't fit palette / size / typography (elevation, motion, overlay, icon defaults, …) — written only when the system defines any
│   └── index.css          aggregator — imports the files above
├── theme.css              variable layer — semantic mapping (light + dark)
├── components/            class layer — plain class names, always written
│   ├── typography.css     .text-* OR role classes (per-system, mutually exclusive)
│   ├── button.css
│   ├── form.css           field + label + help + input + textarea + select + choice + switch
│   ├── badge.css
│   ├── avatar.css
│   ├── card.css
│   ├── alert.css
│   ├── progress.css
│   ├── tabs.css
│   ├── table.css
│   ├── link.css
│   └── index.css          aggregator
└── styleguide.html        self-contained preview — CSS inlined via <style> (preview only)
```

Architectural rules:

- **Variables are internal to this bundle; consumers interact via classes only.** All CSS custom properties live under `primitives/` and `theme.css`. Everything a consumer applies is a class from `components/`.
- **Each `primitives/*.css` owns its category, not a fixed list of tokens.** `size.css` holds *every* dimension token the system exposes (the semantic invariants *and* any system-specific extensions — e.g., Maximal's 18-step `--space-scale-*`, Material's full `--md-shape-*`). Same for `typography.css` (semantic `--font-*` *plus* every `--typography-<role>-*`). `extras.css` is strictly the remainder: tokens that do not fit palette / size / typography (elevation, motion easing/duration, overlay dim, icon defaults, …).

Consumers only need to import the top-level `index.css`; every other file is pulled in by its `@import` chain.

### Semantic tokens

Semantic token names are identical across all systems (`--bg`, `--fg`, `--space-md`, `--font-lg`, `--radius-md`, etc.). Only the values differ. System-specific tokens live in `extras.css` and never collide with the semantic layer.

### Basic components

The `components/` directory ships eleven per-component stylesheets with plain class names that read only variables from the primitives + theme layer. Pick just the ones you need via `@import` — or import `components/index.css` for everything.

| File | Classes | Purpose |
|---|---|---|
| `typography.css` | `.text-xs` … `.text-2xl` (Minimal) **or** role classes such as `.display-large` / `.headline-medium` / `.body-large` (Material, Uber Base, Carbon, Polaris, Radix, Maximal) | Per-system typography utilities (mutually exclusive — a system ships one vocabulary or the other, never both) |
| `button.css` | `.btn` + `.primary` / `.secondary` / `.ghost` / `.danger` / `.disabled` / `.sm` / `.lg` | Call-to-action buttons |
| `form.css` | `.field` / `.label` / `.input` / `.textarea` / `.select` / `.help` / `.choice` / `.switch` | Inputs + choice + toggle, with focus, error, disabled states |
| `badge.css` | `.badge` + solid / soft / outline / danger / success / warning | Labels + status chips |
| `avatar.css` | `.avatar` + `.accent` / `.lg` | User avatars |
| `card.css` | `.card` | Grouped content surface |
| `alert.css` | `.alert` + info / success / warning / danger | Inline banners |
| `progress.css` | `.progress` + `.progress-fill` | Linear progress |
| `tabs.css` | `.tabs` + `.tab` + `.active` | Tab bar |
| `table.css` | `.table` | Data tables |
| `link.css` | `.link` | Inline hyperlinks |

All classes swap correctly when the theme toggles and when the active design system is regenerated. If one of the plain names clashes with an existing class in the consumer's codebase, rename it with a single global search-and-replace before importing.

## When to trigger

User phrases:

- "make / generate a styleguide", "give me a style guide"
- "CSS design tokens", "CSS variables for my theme", "set up theme tokens"
- "typography scale", "color palette", "spacing scale", "radius tokens"
- "apply Material / Uber / Carbon / Polaris / Radix to this project"
- "compare design systems", "preview how X looks"
- "refresh / regenerate / reset the tokens / the theme"
- Any request that ends in writing CSS custom properties for a design system, even in scratch projects

Do not trigger for: editing one component's CSS, fixing a single style rule, or framework-specific build-config work.

## Workflow

### 1. Ask which design system to use — BLOCKING

**This step is a hard gate. Do not read references, do not call the Write tool, do not plan files until the system is chosen.** Ask the user with this exact shape (or equivalent) and then STOP and wait for their reply:

> Which design system would you like? Pick one:
> - **minimal** — Monochrome + accents, system font. Clean, quiet baseline.
> - **material** — Google MD3. Roboto, tonal palette, shape + elevation scales, full type roles.
> - **uber-base** — Uber Base. UberMove → system, mono-heavy, tight radii. Data-dense.
> - **carbon** — IBM Carbon v11. Plex Sans, sharp, 16-step gray, high-contrast enterprise.
> - **polaris** — Shopify Polaris. Inter, soft rounded, commerce-friendly.
> - **radix** — Radix Themes. Inter / system, 12-step scales, developer UI, crisp accent.
> - **maximal** — Expressive — vivid purple brand, 27 type roles, 18-step spacing, shadow-heavy.

**The only two cases where you may skip the question:**

1. The user named **one of the seven system keys verbatim** (case-insensitive) in their triggering message: `minimal` / `material` / `uber-base` / `carbon` / `polaris` / `radix` / `maximal`, or a clearly equivalent proper name ("Material Design", "MD3", "IBM Carbon", "Shopify Polaris", "Radix Themes", "Uber Base"). Use that system.
2. You are regenerating an existing `<output>/` and the top-level `index.css` header comment already records the chosen system. Reuse it unless the user asked to switch.

**Vibe descriptions are NOT system names — still ask.** Examples that look like hints but are not: "modern / clean / playful / enterprise / AI vibe / dark-mode / brutalist / pastel / minimal look / corporate / consumer / dev-tool". Present the list and let the user choose. You may add a one-sentence suggestion next to the question (e.g., "AI vibe coding often pairs with **maximal** for expressive chrome or **radix** for crisp developer UI — your call.") but the choice is still theirs.

**If the user replies with "whatever / default / any / no preference" to the question above:** pick `minimal`, **tell them that's what you're using, and offer to switch** — do not treat this as authorization to skip the question on the next first-time invocation.

Once the system is chosen, also infer or ask (these rarely warrant a follow-up — infer when possible):

- **Output directory?** Default: `styleguide-preview` relative to the current working directory.
- **Preview?** On by default. Skip preview files only if the user says things like "tokens only", "no preview", "skip preview", "no html", or "just the CSS".

### 2. Read only what you need

- Always: `references/<system>.md` — contains one code block per file to write.
- If preview is on: `references/preview.md` — shared HTML + CSS template + component examples.
- Only if the user is comparing systems or picking between them: `references/design-systems.md`.

Do not read references for systems you aren't generating.

### 3. Write the token files and components.css (always)

Copy blocks **verbatim** from `references/<system>.md`:

| Source block in reference | Write to |
|---|---|
| `## primitives/palette.css` | `<output>/primitives/palette.css` |
| `## primitives/size.css` | `<output>/primitives/size.css` |
| `## primitives/typography.css` | `<output>/primitives/typography.css` |
| `## primitives/extras.css` (if present) | `<output>/primitives/extras.css` |
| `## theme.css` | `<output>/theme.css` |
| `## components/typography.css` | `<output>/components/typography.css` |

From `references/preview.md`:

| Source block | Write to |
|---|---|
| `## components/button.css` | `<output>/components/button.css` |
| `## components/form.css` | `<output>/components/form.css` |
| `## components/badge.css` | `<output>/components/badge.css` |
| `## components/avatar.css` | `<output>/components/avatar.css` |
| `## components/card.css` | `<output>/components/card.css` |
| `## components/alert.css` | `<output>/components/alert.css` |
| `## components/progress.css` | `<output>/components/progress.css` |
| `## components/tabs.css` | `<output>/components/tabs.css` |
| `## components/table.css` | `<output>/components/table.css` |
| `## components/link.css` | `<output>/components/link.css` |
| `## components/index.css` | `<output>/components/index.css` |

Always also write `<output>/primitives/index.css`. Base case:

```css
@import './palette.css';
@import './size.css';
@import './typography.css';
@import './extras.css';
```

Omit the `@import './extras.css';` line for systems that don't define one: Minimal, Carbon, Polaris, Radix. Include it for Material, Uber Base, Maximal.

Don't invent values. If something looks wrong in the reference, fix the reference first and then regenerate.

**If the user asks for tokens or effects that don't exist in any reference** (custom additions like `--glow-*`, `--sweep-*`, project-specific brand tokens, gradient tokens, animation keyframes, etc.) — do NOT silently invent them inside `primitives/extras.css`. Instead, after the base system is chosen, ask:

> "[Those tokens] aren't in the `<system>` reference. Two options:
> (a) One-off — add them to `<output>/primitives/extras.css` for this project only (they'll be lost the next time you regenerate).
> (b) Permanent — add them to `references/<system>.md` first so they survive regeneration. I can do either — which do you want?"

Wait for the answer. Never write unreferenced tokens on your own judgment.

The `components/` directory is written even when the user asks to skip the preview — components are part of "what the skill produces". Typography is per-system, so it comes from `references/<system>.md`; the other ten class files are system-agnostic and come from `references/preview.md`.

Finally, always write the top-level `<output>/index.css` — the single import entry point consumers use. Template:

```css
/*
 * Design system: {{SYSTEM_NAME}}
 * Generated by the css-design-system skill. Do not edit tokens here — edit
 * the per-layer files instead and this file will keep working.
 *
 * How to use
 *   1. Import this one file from your app stylesheet:
 *        @import 'styleguide-preview/index.css';
 *      — or link it from HTML:
 *        <link rel="stylesheet" href="styleguide-preview/index.css">
 *   2. Theme defaults to light. Toggle dark mode with:
 *        <html data-theme="dark">
 *      Remove the attribute (or set "light") to return to the default.
 *   3. Style your markup with the classes from components/* (e.g. .btn,
 *      .input, .heading-lg). Do not reference --* variables from consumer
 *      code — treat them as internal.
 *
 * Layers (imported in this order — later layers depend on earlier ones):
 *   primitives (variables)
 *     → theme (semantic variables, light + dark)
 *       → components (classes)
 */

@import './primitives/index.css';
@import './theme.css';
@import './components/index.css';
```

Replace `{{SYSTEM_NAME}}` with the chosen system's display name (from `## Preview metadata` → name in the system reference). Every system uses the same three-line import order — `primitives/extras.css` is chained into `primitives/index.css` already, so the top-level file never references extras directly.

### 4. Write the preview (on by default)

If the user didn't ask to skip it, write a **single self-contained** `<output>/styleguide.html`. No separate `styleguide.css` file — all CSS lives in a `<style>` block inside the HTML so the preview opens directly from the filesystem with no link resolution.

Use the `## HTML template` from `references/preview.md`. Replace the `{{BUNDLED_CSS}}` placeholder with the following blocks concatenated in this exact order:

   1. `## Reset` from `references/preview.md`
   2. `## primitives/palette.css` from `references/<system>.md`
   3. `## primitives/size.css` from `references/<system>.md`
   4. `## primitives/typography.css` from `references/<system>.md`
   5. `## primitives/extras.css` from `references/<system>.md` (only for systems that have one: Material, Uber Base, Maximal)
   6. `## theme.css` from `references/<system>.md`
   7. `## Base` from `references/preview.md`
   8. `## components/typography.css` from `references/<system>.md`
   9. All ten system-agnostic `## components/*.css` blocks from `references/preview.md` (skip `index.css` — it's `@import`-only and those imports won't resolve inline)
  10. `## Preview chrome CSS` from `references/preview.md`

Then substitute the remaining placeholders per:

   | Placeholder | Source |
   |---|---|
   | `{{SYSTEM_NAME}}` | `## Preview metadata` → name, in the system reference |
   | `{{SYSTEM_DESCRIPTION}}` | `## Preview metadata` → description |
   | `{{FONT_FAMILY_ROWS}}` | Two fixed rows — one sample each for `--font-sans` and `--font-mono`. Pattern in preview.md. |
   | `{{TYPOGRAPHY_ROWS}}` | Mutually exclusive: Minimal (the only system with `type_roles: none`) emits six rows — one per `--font-xs` … `--font-2xl`. Every other system emits one row per role listed in its Preview metadata. Never both. Patterns in preview.md. |
   | `{{SEMANTIC_SWATCHES}}` | Exhaustive — one swatch per key in the light `theme.css` `:root` block. |
   | `{{PRIMITIVE_SWATCHES}}` | Exhaustive — one swatch per **every** `--*` variable in `primitives/palette.css` (every ramp step + every accent), in source order. No skipping. |
   | `{{SPACING_ROWS}}` | Exhaustive — one row per spacing token declared anywhere in `primitives/size.css`. Includes `--space-*` and any system-specific extensions like `--space-scale-*`. |
   | `{{RADIUS_BOXES}}` | Exhaustive — one box per corner-radius / shape token declared in `primitives/size.css` (`--radius-*`, plus any `--md-shape-*` or similar if present). |
   | `{{BUTTON_SIZE_ROWS}}` | Three value rows for `--btn-sm/md/lg`. Pattern in preview.md. |
   | `{{MOTION_ROW}}` | One row with the `--transition` value and a hover demo. |
   | `{{ELEVATION_SECTION}}` | Full section block if the system has elevation tokens (live in `primitives/extras.css`), else empty string. |
   | `{{EXTRAS_SECTION}}` | Catch-all section surfacing any `primitives/extras.css` tokens not already shown in Elevation (MD3 motion, Maximal overlay + icon defaults, etc.). Empty when the system has no `primitives/extras.css` at all (Minimal, Carbon, Polaris, Radix). Grouped tables — pattern in preview.md. |
   | `{{COMPONENTS_BLOCK}}` | Verbatim from `## Components HTML` in preview.md. |

**Completeness test**: after substitution, every `--*` variable declared anywhere in `primitives/*` + `theme.css` must be visible somewhere in the preview. The `[data-var]` spans are refreshed by the theme-toggle script, so variable values stay live when the user switches light ↔ dark.

### 5. If existing files would be overwritten

Check whether `<output>/` has content. If it does and the user hasn't said "overwrite", ask before proceeding. Never clobber silently.

### 6. Report

After writing, tell the user:
- The file paths written.
- The chosen system.
- Whether preview was included.
- How to open the preview (`open <output>/styleguide.html` on macOS, or equivalent).

## Invariants across systems

Every system's bundle is required to declare the following **minimum set of semantic token names**. Systems are free to add more tokens in the same files — the invariant is the names must exist, not that these are the only names. These are implementation details; classes in `components/` read them, consumers don't touch them directly.

From `theme.css`: `--bg`, `--bg-subtle`, `--bg-muted`, `--bg-elevated`, `--fg`, `--fg-muted`, `--fg-subtle`, `--border`, `--border-strong`, `--accent`, `--accent-muted`, `--highlight`, `--highlight-muted`, `--danger`, `--success`, `--warning`.

From `primitives/typography.css`: `--font-sans`, `--font-mono`, `--font-xs` … `--font-2xl`. (Plus any `--typography-<role>-*` tokens the system adds.)

From `primitives/size.css`: `--space-xs` … `--space-xl`, `--radius-sm/md/lg`, `--btn-sm/md/lg`, `--transition`. (Plus any `--space-scale-*`, `--md-shape-*`, or similar the system adds.)

If a system-specific token is a **color, dimension, or typography value**, it belongs in `palette.css`, `size.css`, or `typography.css` respectively — not in `extras.css`. `primitives/extras.css` is strictly the remainder: elevation/shadow, motion (easing, duration), overlay dim, icon defaults, etc.

## Adding a new system

If the user wants a system not in the list (Fluent, Ant Design, Atlassian, Tailwind defaults, custom house style…):

1. Add `references/<new-system>.md` using the same section structure as the existing six files: `primitives/palette.css` / `primitives/size.css` / `primitives/typography.css` / `primitives/extras.css` (optional) / `theme.css` / `components/typography.css` / Preview metadata / Source.
2. Pull values from the upstream spec; note the source URL.
3. **Classify new tokens by category, not by origin**: a system's type-role tokens go in `typography.css`; a system's extended spacing ladder or shape scale goes in `size.css`; only tokens that don't fit palette / size / typography (elevation, motion, overlay, icon, misc) go in `extras.css`. If the system has no such leftover tokens, omit `primitives/extras.css` entirely.
4. In `components/typography.css`, emit one class per type role (or `.text-xs`..`.text-2xl` if the system has no roles). Classes must read only from variables defined in this system's primitives + theme.
5. Run the same workflow against the new reference.

Keep the minimum semantic token names intact — everything else is free to vary per system.

## References

- `references/design-systems.md` — selection guide and invariants.
- `references/preview.md` — shared reset + base + preview CSS + HTML template + 10 system-agnostic components.
- `references/<system>.md` × 7 — per-system CSS blocks including `components/typography.css`.

## What this skill does not do

- **No automatic project integration.** The output sits in the directory you pass. Wiring is one line: `@import '<output>/index.css';` from a root stylesheet (or a `<link>` tag in HTML). The top-level `index.css` chains primitives → theme → components for you.
- **No script runner.** Generation is manual — open references, write files. Keeps the skill light and transparent.
- **No namespace guarantee.** `components/` uses plain class names (`.btn`, `.input`, `.card`, …). If any clash with your codebase, rename via global search-and-replace before importing.
- **No utility classes for palette / spacing / radius.** Consumers compose these through the ready-made component classes. If you need a custom surface that isn't in `components/`, build it in your own CSS — variables are an internal detail and the skill does not export a `.bg-accent` / `.p-md` style layer.

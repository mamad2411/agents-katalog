---
name: angora-design-system-init
description: Initialize a brand-new Angora design system from scratch — run the creative-direction interview (audience, feel, domain vocabulary, signature element, dark-mode opt-in), translate into OKLCH tokens (palette, type scale, spacing, shadows, radii), and build the foundational design-system pages (buttons, icons, grid, cards, forms). Trigger when the project is uninitialized — `system.md` has `[TBD]` or `[Placeholder]` values, or `global.css` tokens are unset — or when the user explicitly wants to start, restart, or kick off the design system. Phrases like 'initialize the design system', 'our tokens are still placeholder', 'start Angora from scratch', 'set up the tokens and type scale', 'where do we begin on this project' all trigger this.
---

**Everything in this repo is scaffolding.** Existing components, design system pages, wireframes, tokens, and system.md are all starter placeholders — not approved design work. Use their file structure but replace all content. Nothing here is precious.

# Resumability

Before starting, check `system.md` for an **Init Progress** section at the bottom. If it exists:
1. Read the completed steps — skip them entirely.
2. Resume from the first uncompleted step.
3. If a step has pending user decisions noted (e.g., "needs: icon set from user"), ask for those before building.
4. Tell the user where you're resuming from: *"Picking up from Step X — [step name]. Last completed: [previous step]."*

If no Init Progress section exists, this is a fresh start — begin at Phase 1.

**Progress tracking:** After completing each step, update the Init Progress section in `system.md` immediately. Mark the step as done, note any pending decisions for the next step. This ensures the process survives context compression and new sessions.

**Phase 1 resumability:** Since Phase 1 is a multi-step conversation, record each answer in Init Progress as it's received (e.g., "Step 2 done — audience: mid-stage startup CTO evaluating developer tools"). Include reference analysis notes if applicable. This way a new session can pick up mid-conversation without re-asking questions the user already answered.

# Roadmap

At the start of the process (or when resuming), present the full build sequence to the user so they always know what's ahead:

> **Here's what we're building (you'll approve at each checkpoint):**
>
> 1. **Creative direction** — audience, feel, color world, signature element, anti-patterns, dark mode decision
> 2. **Tokens + style guide** — OKLCH palette, semantic tokens, type, spacing, shadows, radii in browser
> 3. **Dark mode** *(if opted in)* — `.dark` overrides, sidebar toggle, light/dark view routes
> 4. **Buttons** — sizes, variants, icon buttons
> 5. **Icons** — starter icon set as components + downloadable SVGs
> 6. **Grid + Section** — Section container component, section spacing rhythm, grid-gap utility, column patterns
> 7. **Cards** — card types for your pages
> 8. **Forms** — inputs, selects, checkboxes, radios, toggles, all states

Mark the current step with ← and update the marker at each checkpoint. Always tell the user what decisions are coming next.

# Phase 1: Domain Exploration

**Do not read any files yet.** This phase is a conversation with the user — no codebase exploration, no file reads. Everything you need comes from their answers. Ask one question at a time, respond to each answer before moving on, and let earlier answers inform how you frame later questions.

## Step 1: Kickoff — project overview + references

Start with a single open prompt:

> *"Tell me about the project. And if you have any reference sites or screenshots that capture something about the direction — the typography, color palette, layout feel, overall vibe — share URLs or drop screenshots in `inbox/`. Not 'copy this' — 'there's something in here worth pulling from.'"*

**If references are provided:** Analyze them before asking anything else. For URLs, fetch and study the visual language. For screenshots in `inbox/`, read and study them. Extract: color palette choices, type treatment, spacing rhythm, signature visual elements, overall density/whitespace approach. Summarize what you see — what's worth borrowing and what to deliberately avoid. This analysis informs every subsequent question.

## Step 2: Audience

Ask who specifically is landing on this site. Not "users" — the actual person. A CFO evaluating enterprise software? A developer choosing a tool? If the references or project description already imply an audience, propose one and ask the user to confirm or correct: *"From what you've described, I'd say this is a [specific persona] — does that track?"*

## Step 3: Goal

Ask what that person must accomplish. Not "learn about the product" — the specific action. Sign up? Request a demo? Compare tiers? Informed by the audience answer — a developer evaluating a tool has different goals than a founder comparing vendors.

## Step 4: Feel

Ask how this should feel. Push for specific, evocative language — "confident like a bank vault," "energetic like a launchpad." NOT "clean and modern." If references were shared, anchor the question: *"The [reference] reads as [your interpretation] — is that the territory, or something different?"*

## Step 5: Propose the creative direction

Synthesize everything — the references, audience, goal, and feel — into the full structured output. Every field must be filled:

1. **Named audience** — the specific persona (from Step 2)
2. **Goal** — the specific action (from Step 3)
3. **Feel** — the evocative description (from Step 4)
4. **Accessibility standard** — default to EAA/EN 301 549 (European Accessibility Act — WCAG 2.1 AA plus: `lang` on `<html>`, reflow at 320px, non-text contrast ≥ 3:1, text spacing override support, text resizable to 200%). Recommend this as the default: *"I'd go with EAA/EN 301 549 — it's the most complete standard and future-proofs against European requirements. Override if you prefer a different level."* Record the chosen standard in `system.md`. Then write `tests/a11y/config.json` with the matching axe tags:

   | Standard | `tags` value |
   |----------|-------------|
   | WCAG 2.0 AA | `["wcag2a", "wcag2aa"]` |
   | WCAG 2.1 AA | `["wcag2a", "wcag2aa", "wcag21aa"]` |
   | WCAG 2.2 AA | `["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"]` |
   | EAA / EN 301 549 | `["wcag2a", "wcag2aa", "wcag21aa", "EN-301-549"]` |

5. **Domain vocabulary** — 5+ words from the product's world (cybersecurity: shields, vaults, perimeters, sentinel)
6. **Color world** — 5+ colors that exist naturally in the product's domain
7. **Signature element** — One visual choice that could only exist for THIS product (fails the swap test)
8. **Defaults to reject** — 3+ obvious/generic choices named explicitly to consciously avoid
9. **Differentiation** — What makes this UNFORGETTABLE? The one visual thing someone will remember after closing the tab
10. **Dark mode** — Ask: *"Do you want dark mode support? If yes, I'll generate a full dark palette and wire up the toggle. If no, you still get the semantic token architecture — dark mode can be added later without changing components."* Record the answer. Dark mode is a token + tooling concern — component code is identical either way

**Checkpoint.** Present the full creative direction to the user. Ask explicitly: *"Does this creative direction feel right? Anything to adjust before I start translating this into tokens?"* Do not proceed to Phase 2 until they approve. Update Init Progress in `system.md`.

Once approved, let the user know: *"Creative direction is saved to `system.md`. If you'd like to free up context for the build phase, you can run `/clear` and then `/angora-design-system-init` to continue — I'll pick up from Phase 2 using what's saved."*

# Phase 2: Design System Setup

**Now read files.** Start with [design-principles.md](../docs/design-principles.md) for detailed guidance on color (hue rotation, shade generation, grey temperature), typography (line-height rules, type scale), and depth (two-part shadows, five-level scale). Then read `src/system.md` and `src/styles/global.css` for the template structure to fill in.

## 2a. Structural tokens (personality-agnostic)

- Spacing scale (base 8px, ~25% jumps: 4, 8, 12, 16, 24, 32, 48, 64, 80, 96, 128, 192, 256 — no linear scales, no arbitrary values)
- Type scale (hand-crafted, not modular ratio). Body text as fixed px: 12, 14, 16, 18, 20. Heading/display sizes use `clamp()` with `cqi` so they scale fluidly with container width: `clamp(floor, Xcqi, max)` where X = max ÷ 12 (hits max at the 1200px container). Requires a `@container` ancestor.
- Line height rules, max content widths, breakpoints

## 2b. Personality tokens (from Phase 1)

Translate Phase 1 outputs into concrete token decisions:

- **Color world → OKLCH palette.** Pick the strongest 1–2 domain colors as primary/accent hue(s). Generate full 50–950 shade ranges in OKLCH. Choose grey temperature (warm/cool) based on the feel — "bank vault" is cool grey (blue hue ~264°), "launchpad" is warm grey (yellow/orange hue ~60°). Greys get a subtle chroma (0.005–0.018) for temperature.
- **Feel → shape and depth.** "Confident" = smaller radii, firm shadows. "Playful" = larger radii, softer shadows. Match border radius scale and shadow strategy to the feel words.
- **Domain vocabulary → signature element.** The signature element from Phase 1 becomes a concrete CSS/markup choice — a specific color accent, radius treatment, animation, or layout pattern.
- Font family, full color palette (50–950 shade ranges for primary + grey at minimum)
- Shadow scale using two-part shadows (consistent application — don't mix soft diffuse with solid flat on similar elements)
- **Hover/active tokens** for every brand color: `--color-primary-hover`, `--color-primary-active` (and destructive, etc.). Light mode steps darker down the scale (600→700→800), dark mode steps lighter (300→200). Dedicated tokens, not opacity — better visual quality on vibrant brand colors

## 2c. Tokens + Style Guide

`src/system.md` and `src/styles/global.css` are **scaffolding** — placeholder structure meant to be replaced with real values from Phase 1. Use the file structure (sections, `@theme` block) but replace all placeholder content (`[TBD]`, `[Placeholder]`, template token values). Don't preserve placeholder values out of caution — they're disposable. `system.md` is the "why" file — fill in Intent, Accessibility, Anti-Patterns, and Decisions Log. All token values go in `global.css` only.

### Three-tier token architecture

`global.css` uses a three-tier structure that enforces correct usage architecturally:

**Tier 1 — Primitive palette** (`:root` block, outside `@theme`). Raw OKLCH values for the full shade range: `--gray-50` through `--gray-950`, `--primary-50` through `--primary-950`, plus any additional palettes. These are plain CSS custom properties with **no `--color-` prefix** — this means Tailwind generates no utility classes for them. Components cannot use `bg-gray-50` or `text-primary-500` because those classes don't exist.

**Tier 2 — Semantic tokens** (`@theme` block). Role-based aliases using shadcn naming: `--color-background`, `--color-foreground`, `--color-card`, `--color-card-foreground`, `--color-primary`, `--color-primary-foreground`, `--color-secondary`, `--color-secondary-foreground`, `--color-muted`, `--color-muted-foreground`, `--color-accent`, `--color-accent-foreground`, `--color-destructive`, `--color-destructive-foreground`, `--color-border`, `--color-input`, `--color-ring`, `--color-success`, `--color-success-foreground`, `--color-warning`, `--color-warning-foreground`, `--color-highlight`, `--color-highlight-foreground`, plus hover/active tokens. These reference Tier 1 values (e.g., `--color-background: var(--gray-50)`). Only these generate Tailwind utilities (`bg-background`, `text-foreground`, `border-border`, etc.).

**Tier 3 — Component tokens** (not needed yet). Would be `--button-bg`, `--card-border`, etc. Only add if a component needs to deviate from semantic defaults.

### Additional infrastructure in `global.css`

- `@custom-variant dark (&:where(.dark, .dark *))` — enables Tailwind `dark:` variants
- `@layer base` — applies `border-border outline-ring/50` to all elements, `bg-background text-foreground` to body
- `:root` also sets `color-scheme: light`
- Shadow tokens in `@theme` use two-part shadows (direct + ambient). Dark mode overrides increase opacity (e.g., 0.08 → 0.25)

### Dark mode (if opted in)

After the semantic tokens in `@theme`, add a `.dark` block that remaps every semantic color token to dark-appropriate values:
- Background: darkest gray (~L=0.16), never pure black (halation)
- Foreground: near-white (~L=0.98)
- Card/popover: one step lighter than background (~L=0.21) for tonal elevation
- Muted/secondary/accent: dark gray (~L=0.27)
- Primary: shift lighter and reduce chroma to avoid visual vibration
- Borders: can use alpha transparency (e.g., `oklch(1 0 0 / 10%)`) for natural blending
- `.dark` also sets `color-scheme: dark` and overrides shadow opacity

If dark mode is **not** opted in, still use the same semantic token architecture (same `@theme` structure, same shadcn names) — just omit the `.dark` block. Components are identical either way, and dark mode can be added later by only touching `global.css`.

### Disabling dark mode (if opted out)

Dark mode is controlled by a single flag in `src/config.ts`:

```ts
export const config = {
  darkMode: false, // set to true to enable
};
```

When `darkMode` is `false`:
- **Layout.astro** — imports `config` and passes `darkMode={config.darkMode}` to Sidebar. This is the wiring that makes the flag work
- **Sidebar** — toggle button is hidden (prop-gated, not deleted)
- **FullscreenLink** — renders a plain link, no theme swapping
- **`view/[theme]/[...slug].astro`** — `getStaticPaths()` only generates `/view/light/*` routes
- **`global.css`** — still needs the `.dark` block and `@custom-variant dark` removed (or left inert — no routes generate dark pages anyway). For a clean build, remove them

When `darkMode` is `true`:
- Layout passes the prop, toggle appears, link swaps light/dark, both route sets are generated

The result: flip one boolean to enable/disable. No file deletion needed. Adding dark mode later is `config.darkMode = true` + adding the `.dark` block to `global.css`.

### Style guide page

The `index.astro` style guide shows palette swatches using **inline `style` attributes** referencing CSS custom properties (e.g., `style="background-color: var(--gray-50)"`), since palette utility classes don't exist. Semantic token specimens use Tailwind utilities (`bg-background`, `bg-card`, etc.).

### Build sequence

1. `global.css` — Full three-tier token structure
2. `system.md` — Intent, accessibility standard, anti-patterns, decisions log (include dark mode decision)
3. `index.astro` (Style Guide) — Visual preview of all tokens (palette swatches with inline styles, semantic token specimens, type scale, spacing, shadows, radii)

**Checkpoint.** Ask the user to open the style guide in browser (`pnpm dev`). Then ask explicitly: *"How do the tokens look? Anything to adjust — palette, type scale, shadows, radii?"* Do not proceed until the user confirms the tokens are correct. If they report issues, fix them and ask again. Update Init Progress in `system.md`.

## 2c-dark. Dark mode infrastructure (if opted in)

Skip this step if the user opted out of dark mode in Phase 1.

1. **Sidebar toggle** — Add a dark mode toggle to `Sidebar.tsx` (below search, above nav). Reads/writes `localStorage` under `angora-ds-theme`. Toggles `.dark` class and `color-scheme` style on `<html>`. Use sun/moon icons.
2. **Full-screen view routing** — Create `src/pages/design-system/view/[theme]/[...slug].astro` dynamic route. `getStaticPaths()` generates `light` × `dark` × all slugs. View content goes in `view/_content/<name>.astro` (pure markup, no layout wrapper). The dynamic route imports content and wraps in `FullScreen.astro` with the theme prop.
3. **FullScreen.astro** — Accepts `theme` prop (`'light' | 'dark'`, defaults to `'light'`). Sets `.dark` on `<html>` and `color-scheme` meta tag when dark.
4. **Layout.astro** — Add `<meta name="color-scheme" content="light dark">`.
5. **A11y tests** — Update test discovery to find `view/_content/*.astro` and test both `/view/light/*` and `/view/dark/*` routes.

**Checkpoint.** Ask the user to toggle dark mode in the sidebar. Verify the whole design system shell switches. Check a full-screen view at both `/view/light/` and `/view/dark/` paths. Update Init Progress in `system.md`.

## 2d. Foundational design system pages

All sections must have a `@container` ancestor (required for responsive type tokens to work).

Before building pages, ask the user to start the dev server in a separate terminal: *"Make sure `pnpm dev` is running — you'll want it to review each page in the browser, and I'll need it for a11y testing."*

**Dev tools convention:** every component's root element gets `data-component="ComponentName"` (PascalCase). Sub-components too (`data-component="CardBody"`). This makes components identifiable in browser dev tools. Always first attribute in the list. Landmark components also set flow participation attributes: `data-component="Hero" data-seamless data-full-width`.

**Token usage:** All components use semantic token utility classes only (`bg-card`, `text-foreground`, `border-border`, etc.). Never use raw palette classes — they don't exist. Read `global.css` to see available semantic tokens in the `@theme` block.

**Full-screen views:** Each design system page that has a full-screen view creates a content file at `src/pages/design-system/view/_content/<name>.astro` (pure markup, no FullScreen wrapper). The dynamic route at `view/[theme]/[...slug].astro` handles wrapping with FullScreen and applying the theme. If dark mode is enabled, both `/view/light/<name>` and `/view/dark/<name>` are generated automatically.

**A11y:** Run `pnpm test:a11y` after building each design system page (dev server must be running). Read the output and fix any failures before proceeding. This is mechanical work — no user confirmation needed.

Before building each page, ask the user any decisions noted below. Build one page at a time, or batch pages that don't need user input.

1. `buttons.astro` — Sizes (sm, md, lg), variants (primary, secondary, ghost), icon buttons. Present 2–3 specific options for icon button layout (icon-left, icon-only, icon-right) and ask the user to pick.
2. `icons.astro` — Icon gallery at sm (16px), md (20px), lg (24px), xl (32px) sizes, plus color variants, with copy-to-clipboard buttons for raw SVG. The default icon library is **Lucide** (`@lucide/astro` package) — but ask the user if they'd prefer a different set (Heroicons, Phosphor, Tabler, etc.). Each icon in `src/icons/` is a thin Astro wrapper that re-exports from the chosen library. Components always import from `@/icons/`, never from the library directly — this keeps the library swappable. Ask the user to name a starter set of 8–12 icons, then create a wrapper in `src/icons/` for each one.
3. `grid.astro` — Section component + section spacing rhythm + `grid-gap` utility + column patterns.

   **Build the Section component first** (`src/components/Section.astro`):
   - Renders `<section>` with `@container` and `data-component="Section"`
   - Section does NOT own width or horizontal padding — the flow utility (`section-flow`/`prose-flow`) handles all width constraints on direct children
   - Props: `seamless` (boolean → adds `data-seamless`, adds standardized vertical padding tied to `--section-gap`), `fullWidth` (boolean → adds `data-full-width`, drops flow width constraint), `narrow` (constrains to `--container-narrow`), `withWrap` (re-constrains children of full-width sections to container width), `withPadding` (adds vertical padding without seamless behavior), `title` (renders `<h2>` with automatic `aria-labelledby`), `aria-label` (for untitled sections), `class` (pass-through)
   - Non-seamless sections get no vertical padding — `section-flow` margin handles spacing. Seamless sections get vertical padding matching `--section-gap` for consistent rhythm
   - `title` prop renders a `<h2>` and automatically wires `aria-labelledby`. Pass `aria-label` for sections without a visible heading
   - When `seamless`: adds `data-seamless` attribute so `section-flow` collapses gap between adjacent seamless sections
   - Section is a primitive (single file, not a directory) since it has no sub-components — content goes in the default slot

   **Flow contexts:** `section-flow` for page-level rhythm, `prose-flow` for editorial content. Both include ambient `prose` via `@apply prose` — typography for raw HTML elements is automatic at low specificity (`:where()`). Component classes naturally override.

   **Then build the grid design system page** showing:
   - Section specimens: section with `title` prop, untitled section (`aria-label`), seamless section (backgrounded, `data-seamless`), full-width section (`fullWidth`), full-width with wrap (`fullWidth withWrap`)
   - Two sections stacked in `section-flow` showing correct inter-section rhythm (`--section-gap`)
   - Two seamless sections stacked showing zero gap (backgrounds butt up)
   - Column patterns using the `grid-gap` utility (`--grid-gap` token)
   - Show the default spacing values in context and ask if the rhythm feels right before building variants.
4. `cards.astro` — Basic card patterns (content card, feature card, pricing card shell). Show the 3 variants and ask: are these the right types for your pages? Missing any?
5. `forms.astro` — Form elements: text input, textarea, select, checkbox, radio, toggle/switch, file upload, search input. All states, sizes, and variants. Form components that need icons (checkbox checkmark, select chevron, search icon) must import from `src/icons/` — never inline SVGs.

**Checkpoint.** Ask the user to open all design system pages in browser (`pnpm dev`). Ask explicitly: *"How do the components look? Anything to adjust before we move on to building pages?"*

**Cleanup.** Once the user approves, remove the Init Progress section from `system.md` entirely — it's process scaffolding, not permanent documentation. The completed design system speaks for itself. With Init Progress removed, the `/angora` entry point will recognize init as complete (Intent section filled in, no Init Progress section present).

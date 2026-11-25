---
name: theme-switch
description: "Select a design theme and compile it into CSS variables (index.css) that a website-building agent can directly consume. 12 built-in themes covering Brutalist, Neubrutalism, Minimal, Startup SaaS, Magazine, Glassmorphism, Dark Console, Cyberpunk, Bento Grid, Notion-core, Corporate, and Fashion Luxury. Also supports extracting themes from reference URLs or discovering trending styles via web search. Outputs shadcn/ui + Tailwind aligned CSS custom properties — swap the :root block, change nothing else."
when_to_use: Use when the user asks to change the website's design style, switch to a different theme, apply a specific visual aesthetic, or says "换个风格" / "make it look like Stripe" / "switch to brutalist" / "什么风格比较流行". Also use when setting up a new project's visual system or when an agent needs CSS variables to build a themed website.
license: Proprietary
compatibility: Requires Read (project files), WebFetch (optional: reference URL extraction and trend discovery). Works with any project using CSS custom properties / Tailwind / shadcn/ui.
metadata:
  author: harness-engineering
  version: "1.0.0"
  allowed-tools: Read Bash WebFetch
---

# Theme Switch — Design Theme Compiler

Select a design philosophy, compile it into CSS variables, and let your website-building agent consume them directly. Swap the `:root` block in `index.css`, change nothing else.

## Core Principle

**Theme switches only the visual layer — colors, fonts, radius, shadows, spacing, motion. Components and page structure stay the same.** This is the game-engine skin change: the character doesn't change, only the skin does.

```
Theme (Design Philosophy)
  ↓ compile
CSS Custom Properties (index.css :root)
  ↓ consume
Tailwind / shadcn/ui Components
  ↓ compose
Pages
```

## Execution Flow (Mandatory)

### Step 1: Read Current Project State

Scan the project to understand what exists:

```
1. Find CSS entry point:
   → index.css / globals.css / app.css
   → Read current :root CSS variables (if any)

2. Find config (if exists):
   → tailwind.config.ts / tailwind.config.js
   → Read font families, color token mappings, container widths

3. Find design docs (if exists):
   → style.md
   → Read current token values and derived_from info
```

If no existing CSS variables found, start fresh from the CSS output schema.

### Step 2: Select Theme

Three entry paths — ask the user which they prefer:

**Path A — Built-in Selection**

Present the 12 built-in themes as a choice. For each theme, show:
- Name + one-line philosophy
- 2-3 representative websites
- Key visual signature (e.g., "0px radius + mono font" for Brutalist)

Built-in themes live in `references/themes/`. Each file contains the complete 10-dimensional profile and compiled token values.

| # | Theme | Philosophy | Signature | Representative Sites |
|---|---|---|---|---|
| 1 | Brutalist | Raw, functional, anti-polish | 0px radius, mono font, no shadows | PostHog, Craigslist, Hacker News |
| 2 | Neubrutalism | Brutal + playful | Hard offset shadows, thick borders, bold flat color | Gumroad, Figma Community |
| 3 | Minimal | Less but better | Grayscale + 1 accent, generous whitespace | Linear, Apple, Notion, Figma |
| 4 | Startup SaaS | Credibility by default | Indigo→purple gradient, pill CTAs, Inter only | Stripe, Vercel, Raycast |
| 5 | Magazine / Editorial | Typography is illustration | Serif headings, multi-column, drop caps, thin rules | NYT, The Verge, Bloomberg |
| 6 | Glassmorphism | Light through frosted crystal | Backdrop-blur, translucent surfaces, gradient orbs | macOS, iOS, Windows 11 |
| 7 | Dark Console | Terminal aesthetics | Near-black bg, monochrome + 1 neon, code feel | Vercel Dashboard, Cursor, Arc |
| 8 | Cyberpunk | Neon wasteland | Glowing text, cut corners, scanlines, neon cyan+magenta | Gaming sites, sci-fi projects |
| 9 | Bento Grid | Modular order | Large radius, subtle elevation, asymmetric grid cells | Apple product pages |
| 10 | Notion-core | Productivity zen | Serif headings, narrow column, block hover, no shadows | Notion, Obsidian |
| 11 | Corporate Friendly | Safe professionalism | Blue primary, medium radius, system sans, compact | Atlassian, Salesforce |
| 12 | Fashion Luxury | Emptiness is luxury | Thin serif, B&W + gold, extreme spacing, slow fades | Vogue, Aesop, Balenciaga |

**Path B — Reference URL**

User provides a website URL. Extract its visual DNA:

1. Fetch the URL with WebFetch
2. Extract CSS custom properties, font families, color palette, border-radius patterns
3. Match against the 12 built-in themes to find the closest match
4. Present: "This site is closest to **{Theme}**. Use that theme as-is, or create a custom variant?"
5. If custom variant → use extracted values as starting point, let user adjust

**Path C — Discover Trending Styles**

User asks "what's popular" or "show me more options":

1. WebFetch `aesthetic.fyi` for the full catalog (~70 styles)
2. Search web for "web design trends 2025 2026"
3. Present top results with one-line descriptions
4. If user selects an unlisted style → WebFetch its `aesthetic.fyi/{slug}` page → extract characteristics → compile into a Theme profile → add as custom theme

### Step 3: Compile Theme → CSS Variables

Read the selected theme file from `references/themes/{theme-name}.md`. It contains:

1. **10-dimensional profile** — ranges and strategies for each dimension
2. **Compiled token values** — concrete CSS values ready for output
3. **Theme-specific variables** — extra CSS properties unique to this theme (e.g., `--backdrop-blur` for Glassmorphism)

Map the token values to the CSS output schema defined in `references/css-output-schema.md`.

**If the user chose a custom variant** (from Path B or C):
- Start from the closest built-in theme's compiled values
- Override with user's adjustments or extracted values
- Document deviations in `style.md`'s `derived_from.note`

**Key mapping rules** (from `references/dimensional-matrix.md`):

| 10-D Dimension | CSS Variable(s) Affected |
|---|---|
| Border | `--border-width`, `--border` (color) |
| Shadow | `--shadow-sm`, `--shadow-md`, `--shadow-elegant` |
| Radius | `--radius` |
| Typography | `--font-display`, `--font-sans`, `--font-mono` + Tailwind fontSize/fontWeight |
| Spacing | `--section-py`, `--card-p`, Tailwind spacing scale |
| Grid | Tailwind container max-widths, column config |
| Motion | `--motion-duration`, `--motion-easing` |
| Density | `--section-py`, line-height multiplier, Tailwind spacing scale |
| Elevation | `--shadow-*` values, shadow strategy (flat/layered/blur-based) |
| Color | All `--background` through `--ring` HSL values |

### Step 4: Generate Outputs

**Output 1: `index.css` (primary — agent-consumable)**

Replace (or create) the `:root` block in the project's CSS entry file. Use the exact format from `references/css-output-schema.md`.

```css
@layer base {
  :root {
    /* ... all CSS variables from compiled theme ... */
  }
  .dark {
    /* ... dark mode overrides if applicable ... */
  }
}
```

**CRITICAL**: Only modify the `:root` and `.dark` variable blocks. Do not modify any other CSS rules, component styles, or layout definitions.

**Output 2: `style.md` (optional — human-readable)**

If the project has a `style.md`, update its YAML front matter with the new token values. Update the `derived_from` section to record which theme was applied and any custom deviations.

If no `style.md` exists, offer to create one with YAML front matter containing the same token values as the CSS output (colors, typography, rounded, spacing, etc.) plus a `derived_from` section recording the theme name and any custom deviations.

**Output 3: Change Report**

Always output a diff table:

```
| Token | Before | After | Theme Rationale |
|---|---|---|---|
| --radius | 0.75rem | 0px | Brutalist: sharp corners only |
| --primary | 142 76% 36% | 0 0% 0% | Brutalist: black on white |
| --font-display | 'Inter' | 'JetBrains Mono' | Brutalist: monospace functional |
| --motion-duration | 200ms | 0ms | Brutalist: instant, no animation |
```

### Step 5: Quality Validation

Run quality checks from `references/quality-gates.md`:

1. **Contrast check**: `--foreground` on `--background` ≥ 4.5:1 (WCAG AA)
2. **Type scale check**: H1 fontSize vs body fontSize ≥ 2.5:1 ratio
3. **Density consistency**: section spacing, card padding, and gap values form a coherent scale
4. **CSS variable completeness**: every variable in `css-output-schema.md` has a value
5. **Theme-specific rules**: e.g., Glassmorphism must have `--backdrop-blur`; Brutalist must have `--motion-duration: 0ms`

If any check fails, flag it in the output and suggest a fix. Do not silently pass a failing check.

### Step 6: Sync Tailwind Config (if applicable)

If the project has a `tailwind.config.ts`:

- Update `fontFamily` section to match new `--font-display`, `--font-sans`, `--font-mono`
- Update `borderRadius` section to match new `--radius`
- Update `animation` / `keyframes` if motion values changed
- Do NOT change container widths, spacing scale, or plugin configs

## Network Discovery Protocol

When the user asks for more styles or trending designs:

1. **Search aesthetic.fyi**: WebFetch `https://aesthetic.fyi/` → parse the full style list → present as numbered options
2. **Get detail on selection**: WebFetch `https://aesthetic.fyi/{slug}` → extract Philosophy, Characteristics, Style Reference prompt, and Use Cases
3. **Compile on-the-fly**: Convert the aesthetic.fyi characteristics into the 10-dimensional profile format → fill in compiled token values → present preview
4. **Save as custom theme**: Write to `references/themes/custom-{name}.md` for future reuse

## Theme Mixing

Users may want to combine aspects of multiple themes. Handle this by:

1. Declaring a **base theme** (primary source)
2. Listing **overrides** from other themes (specific dimensions only)
3. Recording the mix in `style.md`'s `derived_from.note`

Example: "Base Minimal, but with Magazine's serif headings and Glassmorphism's backdrop-blur on cards"

## Constraints

- **Theme does NOT change component structure** — Button stays Button, Card stays Card, Hero stays Hero
- **Theme does NOT change page composition** — section order and skeleton remain fixed
- **Theme does NOT change content** — copy, images, and data are untouched
- **CSS variable replacement is atomic** — replace the entire `:root` block, not individual properties
- **Dark mode must be provided** for every theme (even Brutalist — it just inverts to white-on-black)
- **Never hardcode hex/rgb in component className** — always use semantic tokens (`bg-primary`, `text-foreground`)

## File Reference

| File | Purpose |
|---|---|
| `references/themes/*.md` | 12 built-in theme definitions (10-dim profile + compiled tokens + dark mode) |
| `references/dimensional-matrix.md` | 10-dimensional matrix definition, value ranges, and general mapping rules |
| `references/css-output-schema.md` | Standard CSS variable output format (shadcn/ui + Tailwind aligned) |
| `references/quality-gates.md` | Quality validation rules for compiled output |
| `scripts/validate-tokens.ps1` | PowerShell script for automated token consistency validation |

## Cost Reference

| Step | Tool | Time | When to Run |
|---|---|---|---|
| Read project state | Read | <2s | Always first |
| Select built-in theme | — | 0s | User choice |
| Extract from URL | WebFetch | <5s | Path B only |
| Discover trends | WebFetch | <10s | Path C only |
| Compile tokens | — | <2s | Always |
| Generate CSS output | Write | <2s | Always |
| Quality validation | Bash | <3s | Always after compile |
| Sync Tailwind config | Read + Edit | <3s | If tailwind.config exists |

Total for built-in theme: <10s. Total with URL extraction: <15s. Total with trend discovery: <20s.

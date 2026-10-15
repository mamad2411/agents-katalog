---
name: design-md-to-tailwind-v4
description: >
  Converts a DESIGN.md file (Google Stitch / open-source spec) into a
  production-ready index.css / globals.css for Tailwind CSS v4.
  Covers the full token surface: colors (light + dark), typography scale,
  font families, font weights, letter-spacing, line-heights, spacing scale,
  border-radius, shadows, breakpoints, animations, and component tokens.
  Use this skill whenever the user mentions DESIGN.md, Stitch, design tokens,
  globals.css, index.css, Tailwind v4 theme, @theme, or asks to "translate",
  "convert", "export", or "generate CSS from" a design file. Also trigger
  when the user pastes or uploads a DESIGN.md and asks for a Tailwind setup.
---

# Design → Tailwind v4 Skill

Converts a `DESIGN.md` (Google Stitch alpha spec) into a complete, production-grade
`globals.css` using Tailwind CSS v4's CSS-first `@theme` configuration.

## Quick Reference

Before writing any CSS, load the reference files when needed:

| Reference | When to read it |
|---|---|
| `references/tailwind-v4-namespaces.md` | Always — maps every token category to the correct `--*` namespace and which utilities it generates |
| `references/design-md-spec.md` | When the input is ambiguous or uses non-standard sections |
| `references/conversion-patterns.md` | For edge cases: dark mode, `{token.ref}` resolution, shadows, animations |
| `examples/heritage.DESIGN.md` + `examples/heritage.globals.css` | As a worked reference for the expected input/output shape |

---

## Workflow

### Step 1 — Ingest the DESIGN.md

Accept input as:
- Pasted text in the conversation
- An uploaded file (read from `/mnt/user-data/uploads/`)
- A file path provided by the user

Parse two layers:
1. **YAML front matter** (between `---` fences at the top) — the machine-readable tokens
2. **Markdown prose sections** — supplementary context for tokens not in the YAML
   (e.g. shadow descriptions, animation intent, layout philosophy)

Resolve all `{token.references}` in the YAML before generating CSS. For example:
`backgroundColor: "{colors.tertiary}"` → look up `colors.tertiary` and emit its hex value
OR emit `var(--color-tertiary)` when the value will definitely exist at runtime.

Prefer `var(--color-tertiary)` inside `@layer components` because it stays
runtime-themeable. Use literal hex only inside `@theme` itself.

---

### Step 2 — ⚠️ MANDATORY: Detect shadcn/ui

> **This step is NOT optional. It MUST be completed before writing a single line of CSS.**
> Skipping it produces a broken output when shadcn is present.

Ask the user — or infer from context clues — whether the project uses **shadcn/ui**:

**Ask explicitly if not obvious:**
> "Does your project use shadcn/ui? This changes the variable naming convention."

**Infer as YES if any of these are present:**
- `components.json` mentioned
- imports like `@/components/ui/button` in the codebase
- `npx shadcn` or `shadcn-ui` in package.json / chat context
- The user mentions "shadcn", "shadcn components", or "radix"

---

#### If shadcn = NO → continue to Step 3 normally.

#### If shadcn = YES → apply the shadcn compatibility layer:

> ### ⛔ CRITICAL — Three imports required in this exact order
>
> When shadcn is present, **three imports are required in this order**:
> - `@import "tailwindcss"` — provides the Tailwind engine
> - `@import "tw-animate-css"` — shadcn animation utility (required by shadcn components)
> - `@import "shadcn/tailwind.css"` — layers shadcn base styles and component tokens
>
> Without all three, or out of order, shadcn components will be broken or unstyled.
>
> ```css
> /* ✅ CORRECT when shadcn = YES — all three imports, in this exact order */
> @import "tailwindcss";
> @import "tw-animate-css";
> @import "shadcn/tailwind.css";
>
> /* ── Dark mode custom variant (optional but recommended) ── */
> @custom-variant dark (&:is(.dark *));
>
> /* ❌ WRONG — missing tw-animate-css, animations won't work */
> @import "tailwindcss";
> @import "shadcn/tailwind.css";
>
> /* ❌ WRONG — missing shadcn import, components will be unstyled */
> @import "tailwindcss";
> @import "tw-animate-css";
>
> /* ❌ WRONG — wrong order, imports must be tailwindcss → tw-animate-css → shadcn */
> @import "tw-animate-css";
> @import "tailwindcss";
> @import "shadcn/tailwind.css";
> ```

shadcn/ui requires a **specific set of CSS variable names** in `:root`. These are NOT
the same as the `--color-*` names the DESIGN.md generates. You must emit both layers.

**A) Keep the full `@theme` block unchanged** (Tailwind utilities still need `--color-*`).

**B) Add a shadcn mapping block in `@layer base`** that aliases DESIGN.md tokens
to the exact names shadcn expects:

```css
/* ═══ SHADCN/UI COMPATIBILITY LAYER ═════════════════════════
   shadcn reads these exact variable names from :root.
   They alias the @theme tokens — no values are duplicated.
   ════════════════════════════════════════════════════════════ */
@layer base {
  :root {
    /* Core */
    --background:         var(--color-neutral);
    --foreground:         var(--color-primary);

    /* Card */
    --card:               var(--color-surface);
    --card-foreground:    var(--color-primary);

    /* Popover */
    --popover:            var(--color-surface);
    --popover-foreground: var(--color-primary);

    /* Primary (maps to DESIGN.md tertiary/CTA — the action color) */
    --primary:            var(--color-tertiary);
    --primary-foreground: var(--color-on-tertiary, #fff);

    /* Secondary */
    --secondary:          var(--color-surface);
    --secondary-foreground: var(--color-primary);

    /* Muted */
    --muted:              var(--color-neutral);
    --muted-foreground:   var(--color-secondary);

    /* Accent */
    --accent:             var(--color-tertiary-container, var(--color-neutral));
    --accent-foreground:  var(--color-primary);

    /* Destructive — use error token if present, otherwise synthesize */
    --destructive:        var(--color-error, #dc2626);
    --destructive-foreground: #fff;

    /* Border / Input / Ring */
    --border:             var(--color-border);
    --input:              var(--color-border);
    --ring:               var(--color-tertiary);

    /* Radius — shadcn uses a single --radius base value */
    --radius:             var(--radius-md, 0.5rem);
  }

  /* Dark mode — only if the DESIGN.md defines dark colors */
  .dark,
  [data-theme="dark"] {
    --background:         var(--color-primary);
    --foreground:         var(--color-neutral);
    --card:               color-mix(in oklab, var(--color-primary) 85%, white);
    --card-foreground:    var(--color-neutral);
    --popover:            color-mix(in oklab, var(--color-primary) 85%, white);
    --popover-foreground: var(--color-neutral);
    --muted:              color-mix(in oklab, var(--color-primary) 70%, white);
    --muted-foreground:   var(--color-secondary);
    --border:             color-mix(in oklab, var(--color-primary) 60%, white);
    --input:              color-mix(in oklab, var(--color-primary) 60%, white);
  }
}
```

**Token mapping rules for shadcn:**

| shadcn variable | Maps to DESIGN.md token | Rule |
|---|---|---|
| `--primary` | `colors.tertiary` (CTA color) | shadcn "primary" = action color, not brand color |
| `--background` | `colors.neutral` | Page background |
| `--foreground` | `colors.primary` | Default text |
| `--muted-foreground` | `colors.secondary` | Subdued text |
| `--border` | `colors.border` | Dividers and inputs |
| `--ring` | `colors.tertiary` | Focus rings match CTA |
| `--radius` | `rounded.md` | shadcn uses one base radius; components scale from it |

**Important:** if the DESIGN.md has an explicit `colors.error` or `colors.destructive`,
use it for `--destructive`. Otherwise emit `#dc2626` (Tailwind red-600) as a safe default
and add a comment flagging it as synthesized.

---

### Step 3 — Map tokens to @theme namespaces

Read `references/tailwind-v4-namespaces.md` for the full mapping table.
The critical rule: **every token in `@theme` generates utility classes**.
Use `:root {}` for variables that should NOT generate utilities.

Key mapping summary:

```
colors.*           → --color-{name}
typography.*.fontFamily → --font-{name}  (deduplicated by family name)
typography.*.fontSize   → --text-{scale} (+ --text-{scale}--line-height companion)
typography.*.fontWeight → --font-weight-{scale}
typography.*.letterSpacing → --tracking-{scale}
typography.*.lineHeight    → --leading-{scale}  (only when not paired with --text-*)
rounded.*          → --radius-{scale}
spacing.*          → --spacing-{scale}
shadows.*          → --shadow-{scale}
breakpoints.*      → --breakpoint-{name}
animations.*       → --animate-{name}  (+ nested @keyframes inside @theme)
```

---

### Step 4 — Handle dark mode tokens

**Pattern A — Semantic aliases (recommended):**
When the DESIGN.md has explicit dark color entries (e.g. `primary-dark`, `surface-dark`,
or a `dark:` prose section), use `@theme inline` + `@layer base`:

```css
@theme inline {
  --color-bg: var(--bg);
  --color-fg: var(--fg);
}

@layer base {
  :root {
    --bg: #F7F5F2;
    --fg: #1A1C1E;
  }
  .dark, [data-theme="dark"] {
    --bg: #1A1C1E;
    --fg: #F7F5F2;
  }
}
```

**Pattern B — Direct override (simple projects):**
When dark colors are a simple inversion, emit both blocks without `@theme inline`:

```css
@layer base {
  .dark {
    --color-primary: #F7F5F2;
    --color-surface: #1A1C1E;
  }
}
```

Choose Pattern A when there are 4+ semantic color pairs.
Choose Pattern B for 1–3 simple overrides.

---

### Step 5 — Generate @layer base resets

Always emit a `@layer base` block that wires the theme tokens to actual HTML elements:

```css
@layer base {
  *, *::before, *::after { box-sizing: border-box; }

  html {
    font-family: var(--font-sans);        /* primary body font */
    font-size: var(--text-body-md);       /* base font size */
    line-height: var(--leading-body-md);  /* base line height */
    color: var(--color-primary);
    background-color: var(--color-neutral);
    -webkit-font-smoothing: antialiased;
  }

  h1 { font-size: var(--text-h1); line-height: var(--text-h1--line-height); }
  h2 { font-size: var(--text-h2); line-height: var(--text-h2--line-height); }
  /* ... continue for all typography scale levels present in the DESIGN.md */

  a { color: var(--color-tertiary); }
  a:hover { color: var(--color-tertiary-container, var(--color-tertiary)); }
}
```

Only wire elements that have corresponding tokens. Don't invent tokens.

---

### Step 6 — Emit @layer components for component tokens

When the DESIGN.md has a `components:` section, emit semantic CSS classes in
`@layer components`. Use `var(--token)` references — never hardcode hex here.

```css
@layer components {
  .btn-primary {
    background-color: var(--color-tertiary);
    color: var(--color-on-tertiary, #fff);
    border-radius: var(--radius-sm);
    padding-block: 0.75rem;
    padding-inline: 1.25rem;
    font-family: var(--font-sans);
    font-weight: var(--font-weight-semibold, 600);
    transition: background-color 150ms ease;
  }
  .btn-primary:hover { background-color: var(--color-tertiary-container, color-mix(in oklab, var(--color-tertiary) 80%, transparent)); }
}
```

---

### Step 7 — Output structure

The file header depends entirely on whether shadcn is present:

```
/* shadcn = NO  */    @import "tailwindcss";
/* shadcn = YES */    @import "tailwindcss";            ← always first
                      @import "tw-animate-css";        ← shadcn animation utils (always second)
                      @import "shadcn/tailwind.css";    ← shadcn styles (always third)
@plugin (optional)

/* ── Dark mode custom variant (optional but recommended) ── */
@custom-variant dark (&:is(.dark *));

/* ═══ 1. THEME ══════════════════════════════════════════ */
@theme { … }

/* ═══ 2. DARK MODE PRIMITIVES (if applicable) ═══════════ */
@theme inline { … }   ← only Pattern A
@layer base { :root / .dark / [data-theme] { … } }

/* ═══ 3. SHADCN/UI COMPATIBILITY LAYER (if shadcn = YES) ═ */
@layer base { :root { --background / --foreground / --primary … } }

/* ═══ 4. BASE RESETS ════════════════════════════════════ */
@layer base { html / body / elements { … } }

/* ═══ 5. COMPONENT TOKENS (if applicable) ═══════════════ */
@layer components { … }

/* ═══ 6. MAX-W OVERRIDES — ALWAYS REQUIRED ══════════════════
   ⚠️ MANDATORY: Tailwind v4 reserves xs/sm/md/lg/xl/2xl as
   responsive BREAKPOINTS, not container widths. When @theme
   defines ANY --container-* token (e.g. --container-max,
   --container-sm, etc.), you MUST emit overrides for ALL
   responsive breakpoint utilities so they don't collide.
   ══════════════════════════════════════════════════════════════ */
@utility max-w-xs {
    max-width: var(--container-xs) !important;
}
@utility max-w-sm {
    max-width: var(--container-sm) !important;
}
@utility max-w-md {
    max-width: var(--container-md) !important;
}
@utility max-w-lg {
    max-width: var(--container-lg) !important;
}
@utility max-w-xl {
    max-width: var(--container-xl) !important;
}
@utility max-w-2xl {
    max-width: var(--container-2xl) !important;
}
/* If @theme defines --container-max (or any other custom name), add: */
@utility max-w-container {
    max-width: var(--container-max) !important;
}
```

---

### Step 8 — Self-check before delivering

Run through this checklist mentally:

- [ ] **shadcn detected?** — Step 2 was completed; answer is explicit YES or NO
- [ ] If shadcn = YES — file has ALL THREE imports in this exact order: `@import "tailwindcss";` then `@import "tw-animate-css";` then `@import "shadcn/tailwind.css";`. Never two, never reordered.
- [ ] If shadcn = YES — `--background`, `--foreground`, `--primary`, `--radius` etc. are all present in `@layer base`
- [ ] If shadcn = YES — `--primary` maps to the CTA/action color (DESIGN.md `tertiary`), NOT `--color-primary`
- [ ] If shadcn = YES — `--destructive` has a value (real token or synthesized `#dc2626` with comment)
- [ ] Every `@theme` variable name uses the correct namespace prefix
- [ ] No `var()` references inside `@theme {}` unless using `@theme inline`
- [ ] Typography scale has `--text-{scale}` AND `--text-{scale}--line-height` companions
- [ ] Font families are deduplicated (one `--font-*` per unique family, not per scale level)
- [ ] Spacing tokens are in `rem` or `px`, not unitless (unitless only valid for `--spacing` multiplier)
- [ ] Component classes use `var(--token)`, never hardcoded hex
- [ ] Dark mode override variables are in `@layer base`, NOT inside `@theme`
- [ ] If DESIGN.md has `{token.ref}` syntax — it's resolved to `var(--css-equiv)`
- [ ] File starts with `@import "tailwindcss";`
- [ ] Section comments are present for readability
- [ ] If shadcn = YES — `@custom-variant dark (&:is(.dark *));` is present after imports (optional but recommended for nested dark mode selectors)
- [ ] If `@theme` defines ANY `--container-*` token — ALL of the following `@utility` overrides are present at the END of the file with `!important`. Do NOT skip any:
      `@utility max-w-xs { max-width: var(--container-xs) !important; }`
      `@utility max-w-sm { max-width: var(--container-sm) !important; }`
      `@utility max-w-md { max-width: var(--container-md) !important; }`
      `@utility max-w-lg { max-width: var(--container-lg) !important; }`
      `@utility max-w-xl { max-width: var(--container-xl) !important; }`
      `@utility max-w-2xl { max-width: var(--container-2xl) !important; }`
      Plus one `@utility` per custom `--container-*` token (e.g. `--container-max`). This is NOT conditional — it is ALWAYS required when a container token exists.

---

## Notes on Common DESIGN.md Sections

| DESIGN.md section | How to handle it |
|---|---|
| `## Overview` / `## Visual Theme` | Use as comments; informs naming choices but not tokens |
| `## Colors` prose | Confirms roles; use `@layer base` to wire roles to elements |
| `## Typography` prose | Reveals font intent — prefer named `--font-display`, `--font-body` etc. |
| `## Layout` prose | May define max-width, grid columns → emit as `--container-*` or `:root` variables |
| `## Depth & Elevation` | Maps to `--shadow-*` tokens |
| `## Motion` / `## Animation` | Maps to `--animate-*` + `@keyframes` inside `@theme` |
| `## Do's and Don'ts` | Critical guardrails — respect them in naming and class semantics |
| Extended sections (VoltAgent format) | Same rules; just more sections to extract |

---
name: kb-tailwind-v4
description: Portable Tailwind v4 patterns anchored to this repo's CSS-first config in `src/app/globals.css` — v3→v4 breaking changes LLMs miss, `{util}-(--prop)` CSS-var syntax, two-layer token pattern across `.light`/`.dark`/`.midnight`, `@theme inline` / `@plugin` / `@source` directives. Invoke when writing Tailwind classes, editing `globals.css`, or migrating v3 syntax.
last-verified: 2026-04-23
---

# Tailwind v4 — Patterns for This Repo

> Stack: Next.js 16+ App Router + Tailwind CSS v4.x. Config lives in `src/app/globals.css` (CSS-first, no `tailwind.config.js`).
> **LLMs default to v3 syntax** because training data skews v3. Verify version before generating classes — this file wins for this repo.

---

## 1. v3 → v4 — what actually changed

| v3 (legacy)            | v4 (this repo)                                                                                                                   |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `tailwind.config.js`   | CSS-native `@theme` directive in `globals.css`                                                                                   |
| PostCSS plugin         | Oxide engine (Rust, ~10× faster)                                                                                                 |
| JIT mode flag          | Always on                                                                                                                        |
| Plugin system          | CSS-native features                                                                                                              |
| `{util}-[var(--prop)]` | `{util}-(--prop)` (parentheses, implicit `var()`)                                                                                |
| `{util}-[Npx]`         | `{util}-{N/4}` (dynamic spacing scale: any pixel value — `N/4` may be integer or decimal, e.g. `bottom-[-5px]` → `-bottom-1.25`) |

> Before generating classes, check `package.json` → `tailwindcss`. If `^4.x` → use v4 syntax. Never assume.

### Dynamic spacing scale — convert any px value

v4 introduced a dynamic spacing scale: any number `N` resolves to `N × var(--spacing)` (default `0.25rem` = `4px`). `N` can be **integer or decimal** and **negative**. Arbitrary `[Npx]` brackets are a v3 leftover whenever the value is a fixed pixel quantity — IntelliSense (`bradlc.vscode-tailwindcss`) flags these as `suggestCanonicalClasses` hints.

| ❌ v3 arbitrary | ✅ v4 dynamic scale | Resolved value                                   |
| --------------- | ------------------- | ------------------------------------------------ |
| `min-w-[500px]` | `min-w-125`         | 125 × 0.25rem = 500px                            |
| `max-w-[200px]` | `max-w-50`          | 50 × 0.25rem = 200px                             |
| `min-h-[180px]` | `min-h-45`          | 45 × 0.25rem = 180px                             |
| `gap-[20px]`    | `gap-5`             | 5 × 0.25rem = 20px                               |
| `p-[16px]`      | `p-4`               | 4 × 0.25rem = 16px                               |
| `h-[18px]`      | `h-4.5`             | 4.5 × 0.25rem = 18px (decimals OK)               |
| `bottom-[-5px]` | `-bottom-1.25`      | -1.25 × 0.25rem = -5px (negatives + decimals OK) |
| `top-[37px]`    | `top-9.25`          | 9.25 × 0.25rem = 37px                            |

**Rule of thumb:** **any fixed px value is convertible.** Compute `N/4` (may be decimal); negate the prefix for negative values (`-bottom-1.25`, not `bottom-[-1.25]`). The brackets `[Xunit]` are only legitimate when:

- The value is **not pixels** without a clean rem mapping (e.g. `top-[3vh]`, `w-[calc(100%-2rem)]`)
- Typography sizes outside the kit's `text-*` scale (`text-[10px]` is OK if no `text-2.5` token defined for fine-print)
- Color literals that aren't tokens (`bg-[#ff00ff]` for one-off marketing pages — but prefer adding to `@theme`)

Document the legitimate brackets with an inline comment so the next reader knows it was intentional, not legacy.

**Why v4 prefers the scale:**

- Theme-aware: if `--spacing` base changes, every `{util}-N` adapts; `[Npx]` is hardcoded and drifts.
- Bundle: each unique arbitrary value generates a one-off class; the scale shares a single utility table.
- Consistency: large numbers (`min-w-125`) trade one-time legibility cost for system rhythm — accept it.

---

## 2. Config in CSS — `@theme inline` mapping (this repo's idiom)

> The repo uses a **two-layer pattern**: raw tokens under theme-scoped selectors (`:root, .light`, `.dark`, `.midnight`), then `@theme inline` maps Tailwind utility names to `var(--…)` references. This lets one set of utilities (`bg-primary`, `text-muted-foreground`) work across all 3 themes via class switching.

### Real shape (`src/app/globals.css`)

```css
@import 'tailwindcss';

/* Positive @source — scan src/config even if gitignored elsewhere */
@source '../../src/config';

/* Negative @source — exclude markdown dirs that would crash Oxide */
@source not '../../docs';
@source not '../../.agent';

/* Plugins use the @plugin directive (v4, not plugins: [] in JS config) */
@plugin '@tailwindcss/typography';

/* ── Layer 1: raw tokens per theme ─────────────────────────── */
:root,
.light {
  --background: #e0e5ec;
  --foreground: #0f172a;
  --primary: #1e40af;
  /* … many more … see globals.css */
}

.dark {
  --background: #2d2d32;
  --primary: #60a5fa;
  /* … */
}

.midnight {
  --background: #1a2332;
  --primary: #3b82f6;
  /* … */
}

/* ── Layer 2: map raw tokens to Tailwind utility names ─────── */
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  /* …repeat for every token you want as a utility… */

  --font-sans: var(--font-geist-sans);
  --font-mono: var(--font-geist-mono);
}
```

### Why this pattern matters

- **Theme switching** works by toggling `.light` / `.dark` / `.midnight` on `<html>` — the Layer-2 `var(--…)` references resolve to whichever theme is active. No class-per-theme at the component level.
- **`@theme inline`** (note the `inline` modifier) tells Tailwind to resolve the CSS variables at build time into the utility classes, so `bg-primary` compiles to `background-color: var(--primary)`.
- **Do not hardcode colors at component scope**. Add a new token via Layer 1 (in all 3 themes), then expose via Layer 2. See `kb-design-system` for the discipline.

> **For the full token surface** (badge colors, neomorphic shadows, status colors, etc.) → consult `src/app/globals.css` directly. It's the SSOT — don't enumerate it here.

---

## 3. 🔴 CSS variable syntax (v4 breaking change)

> The single most common v4 mistake. LLMs write v3 syntax unless told otherwise.

| Condition                            | Pattern                  | Example                               |
| ------------------------------------ | ------------------------ | ------------------------------------- |
| Property has a `@theme` mapping      | `{utility}-{token-name}` | `bg-primary`, `text-surface`          |
| Property has **no** `@theme` mapping | `{utility}-(--{prop})`   | `bg-(--sidebar-bg)`                   |
| One-off arbitrary literal value      | `{utility}-[{literal}]`  | `bg-[#25D366]` (avoid — prefer token) |

### Side-by-side — same intent, three stacks

```tsx
// Themed token (preferred)
<div className="bg-primary text-surface" />

// Untheked CSS variable (use parens, NOT var() wrapper)
<div className="bg-(--sidebar-bg)" />

// One-off literal (last resort)
<div className="bg-[#25D366]" />
```

### ❌ v3 patterns to stop generating

```tsx
// v3 syntax — broken in v4
<div className="bg-[var(--sidebar-bg)]" />   // ❌ brackets + var()
<div className="w-[var(--sidebar-w)]" />     // ❌ same
```

---

## 4. 🔴 `@source` directives — positive and negative

> Real incident: Oxide scans **all non-gitignored files** for class-looking strings. A markdown file with a malformed CSS example inside backticks crashed Turbopack with `"Unexpected end of input"` and returned 500 on the entire app.

### This repo's real directives (in `src/app/globals.css`)

```css
@import 'tailwindcss';

@source '../../src/config'; /* positive — force-scan even if otherwise excluded */
@source not '../../docs'; /* markdown with CSS in backticks */
@source not '../../.agent'; /* legacy skill dir (if present) */

@plugin '@tailwindcss/typography';
```

### Positive `@source` — force-scan a directory

Use when class strings live in a path outside Oxide's default scan (e.g., generated files, config modules). The repo scans `src/config` this way so label/permission strings referenced there compile.

### Negative `@source not` — exclude markdown dirs

| Directory  | Risk                                                    | Status in this repo                       |
| ---------- | ------------------------------------------------------- | ----------------------------------------- |
| `docs/`    | Discovery/design/backlog markdown with CSS in backticks | Excluded                                  |
| `.agent/`  | Legacy skill dir (migration residue)                    | Excluded                                  |
| `.claude/` | Current skill markdown with CSS examples                | Not needed — already outside default scan |
| `project/` | Non-source markdown (old layout)                        | Not present in this repo                  |

### Rules

1. Add `@source not` for any directory under the project root that contains markdown with CSS in code blocks and is otherwise visible to Oxide.
2. **Paths are relative to `globals.css`**, not to the project root. From `src/app/globals.css`, `../../` = project root.
3. `@source not` is a no-op if the directory doesn't exist → safe to include preemptively.
4. Place **after** `@import 'tailwindcss'` — order matters.

> 🛑 If you see `"Unexpected end of input"` or a 500 on every route after editing a markdown file, the first check is `@source not` coverage. Add the offending directory and restart the dev server.

### `@plugin` directive (not `plugins: []`)

v4 loads Tailwind plugins via `@plugin '<pkg-name>'` inside `globals.css` — no `tailwind.config.js`, no `plugins: [typography()]` array. This repo uses `@tailwindcss/typography` for `prose` classes.

### VSCode Tailwind extension — exclude markdown

The `bradlc.vscode-tailwindcss` extension will validate class strings in fenced code blocks and flag v3 anti-patterns documented in skills/docs. Add to `.vscode/settings.json`:

```json
"tailwindCSS.files.exclude": [
  "**/*.md",
  "**/*.mdx",
  "**/.claude/**",
  "**/docs/**"
]
```

Requires VSCode reload to take effect.

---

## 5. Breakpoints & mobile-first

| Prefix | Min width | Target        |
| ------ | --------- | ------------- |
| (none) | 0         | Mobile base   |
| `sm:`  | 640       | Large phone   |
| `md:`  | 768       | Tablet        |
| `lg:`  | 1024      | Laptop        |
| `xl:`  | 1280      | Desktop       |
| `2xl:` | 1536      | Large desktop |

Mobile-first → write the base classes for small screens, then override with prefixes:

```tsx
<div className="w-full md:w-1/2 lg:w-1/3" />
```

---

## 6. Container queries (v4 native)

| Type                         | Responds to          | Use when                        |
| ---------------------------- | -------------------- | ------------------------------- |
| Breakpoint (`md:`, `lg:`, …) | Viewport width       | Page-level layouts              |
| Container (`@container`)     | Parent element width | Reusable components, card grids |

```tsx
<div className="@container">
  <div className="grid @md:grid-cols-2 @lg:grid-cols-3" />
</div>
```

Prefer container queries when the same component appears in different layout contexts (main + sidebar, modal + page).

---

## 7. Theme switching — 3 themes, not 2

> This repo ships **3 themes** (`.light`, `.dark`, `.midnight`), toggled by setting a class on `<html>`. Because components consume theme tokens via `bg-primary` / `text-muted-foreground` (not `dark:bg-zinc-900`), the same JSX works across all 3 themes without `dark:` variants.

| Theme    | Selector        | Feel                          |
| -------- | --------------- | ----------------------------- |
| Light    | `:root, .light` | Warm neomorphic gray surfaces |
| Dark     | `.dark`         | Charcoal (#2d2d32)            |
| Midnight | `.midnight`     | Deep blue (#1a2332)           |

### Pattern — prefer theme tokens over `dark:` variants

```tsx
// ✅ Works across all 3 themes — tokens resolve per-theme via @theme inline
<div className="bg-card text-card-foreground neo-outset" />

// ❌ Only flips between light and .dark — breaks on .midnight
<div className="bg-white text-zinc-900 dark:bg-zinc-900 dark:text-zinc-100" />
```

### When `dark:` variants are still OK

For one-off ornamental classes that aren't semantically bound to a token (e.g., a decorative gradient). Any component-level color should go through a `@theme inline` token instead.

---

## 8. Layout — common recipes

### Flex

| Intent           | Classes                             |
| ---------------- | ----------------------------------- |
| Center both axes | `flex items-center justify-center`  |
| Vertical stack   | `flex flex-col gap-4`               |
| Row with gap     | `flex gap-4 items-center`           |
| Spread + align   | `flex justify-between items-center` |

### Grid

| Intent                    | Classes                                                    |
| ------------------------- | ---------------------------------------------------------- |
| Auto-fit responsive cards | `grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))]`      |
| Sidebar + content         | `grid grid-cols-[auto_1fr]`                                |
| Asymmetric/bento          | `grid grid-cols-3 grid-rows-2` + `col-span-*`/`row-span-*` |

---

## 9. Color — what this repo actually uses

> This repo uses **hex + rgba** for tokens, not OKLCH. The priority is **consistent tokens across `:root/.light`, `.dark`, `.midnight`**, not the color format.

```css
:root,
.light {
  --primary: #1e40af;
  --neo-dark: rgba(136, 150, 171, 0.35);
}
.dark {
  --primary: #60a5fa;
}
.midnight {
  --primary: #3b82f6;
}
```

### Color format — use what the token system already uses

| Format    | When to use in this repo                                                  |
| --------- | ------------------------------------------------------------------------- |
| **hex**   | Default — matches existing palette, easy to diff                          |
| **rgba**  | When an alpha is semantically needed (neomorphic shadows, badge overlays) |
| **OKLCH** | Only if the wider token system already uses it — don't mix in this repo   |

### Two-layer token system (this repo's real shape)

| Layer       | Where                                   | Example                            |
| ----------- | --------------------------------------- | ---------------------------------- |
| Raw         | `:root, .light` / `.dark` / `.midnight` | `--primary: #1e40af;`              |
| Utility map | `@theme inline`                         | `--color-primary: var(--primary);` |

> For the full token inventory (badge colors, neomorphic shadow stack, status colors, etc.) **consult `src/app/globals.css` directly** — it is the SSOT. See also `kb-design-system` for when to add a new token vs. reuse existing.

---

## 10. Anti-patterns

| ❌                                       | ✅                                                                 |
| ---------------------------------------- | ------------------------------------------------------------------ |
| Arbitrary values everywhere              | Use the design-system scale / existing token                       |
| `!important`                             | Fix specificity properly                                           |
| Inline `style={{…}}`                     | Use utilities / theme tokens                                       |
| Long repeated class strings              | Extract a component                                                |
| Heavy `@apply` usage                     | Prefer components over utility bundles                             |
| `{util}-[var(--x)]` (v3)                 | `{util}-(--x)` (v4)                                                |
| `{util}-[Npx]` for any fixed pixel value | `{util}-{N/4}` integer or decimal, negate prefix for `-` (see §1)  |
| Hardcoded hex/rgb on a component         | Add a token in all 3 themes + `@theme inline`, consume via utility |
| `dark:bg-zinc-900` for theme-bound color | Use `bg-card` / `bg-background` — resolves per active theme        |
| Enumerating token catalog in a doc/skill | Anchor to `src/app/globals.css` — it's the SSOT                    |

---

## 11. Quick diagnostic cheatsheet

| Symptom                                        | Likely cause                                                                |
| ---------------------------------------------- | --------------------------------------------------------------------------- |
| "Unexpected end of input" / 500 on every route | Missing `@source not` for a markdown directory                              |
| A class renders with no style                  | v3 syntax (`[var(--x)]`) on v4 — switch to `(--x)`                          |
| Dark mode doesn't toggle                       | `.dark` class not applied to `<html>` / no `dark:` variant                  |
| Classes work in dev, disappear in prod build   | The source file isn't in the default scan path and needs explicit `@source` |

---

_Cross-reference: `kb-design-system` for token discipline & scale rules. `kb-ui` for React/Next.js component patterns that consume these classes._

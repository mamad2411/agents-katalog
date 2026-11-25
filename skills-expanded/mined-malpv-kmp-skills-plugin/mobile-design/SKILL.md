---
name: mobile-design
description: Design and build mobile UIs (Compose Multiplatform) from DESIGN.md tokens. If DESIGN.md is missing it creates one by interviewing the user about identity, visual references, and palette; if it exists it audits and completes it before mapping it to the theme. Use whenever the user themes or styles the app, mentions DESIGN.md, colors/palette, MaterialTheme, dark mode, typography/fonts, component styling, or reports UI cut off by the status/navigation bar (edge-to-edge insets) — even if they just say "make it look good" or "match our brand".
---

# Skill: mobile-design

This skill owns **how the app looks**: design tokens, theme, and components. It does not define what a screen knows (`kmp-expert-presentation`) or where it navigates (`kmp-expert-navigation`).

Apply it **after** a screen has its state and data resolved: styling a UI whose contract is still going to change is rework.

> [!NOTE]
> **Placement (architecture-agnostic):** the theme, tokens, and reusable components live in the **shared design layer**. In a **modular** project that is a `:core:design-system` module the features consume — see `kmp-modular-architecture`. In a **single-module** project it is a package under `commonMain`. `DESIGN.md` always lives at the **project root**.

## Mobile Design Philosophy

1. **Visual Hierarchy and Information Density**: mobile UIs are optimized for small touch screens. Prioritize visual clarity and ease of interaction (touch zones).
2. **Consistency via Tokens**: the theme is the single source of truth. No color, radius, or font size is written by hand in a screen.
3. **Touch Ergonomics**: design for the thumb zone and a 48dp minimum touch target.
4. **Prevent "AI Slop" on Mobile**: avoid generic layouts that ignore screen density, missing interactive states (loading, pressed, disabled), and inconsistent corner radii.

---

## Workflow

This skill **acts**, it does not describe. Run the steps in order.

### Step 1 — Locate `DESIGN.md`

Look for `DESIGN.md` at the project root. The result decides the branch: **missing** → Step 2A. **Present** → Step 2B.

### Step 2A — Missing: create it by asking

> [!WARNING]
> **Do not invent a visual identity silently.** Choosing a palette for the user is a product and brand decision that is not yours to make, and it then propagates across the whole app and is costly to reverse. Ask **before** writing a single line.

Ask the user, in one batch:

1. **Is there an existing brand or palette?** Hex colors, a logo, a brand manual, or an app/site for the same product.
2. **Is there a reference UI?** A screenshot, an app they like, a site, a Figma. This is the most valuable input: one concrete reference beats ten adjectives.
3. **What tone is the product after?** For example: sober/corporate, warm/friendly, premium/dark, minimalist.
4. **Light theme, dark, or both?**
5. **Any typography constraint?** A mandatory brand font or a license.

If the user has nothing defined, **do not block them**: propose 2–3 concrete, contrasting directions (each with its palette and rationale) and let them pick. Reacting to options is easier than describing a design from scratch.

Only with those answers, write `DESIGN.md` in the format below.

### Step 2B — Present: audit before using

A `DESIGN.md` that exists is not a `DESIGN.md` that is complete. Check it against this list and **fill the gaps** before mapping:

- **Are the content pairs there?** Every `primary` needs its `on-primary`. If it is missing, the color of text on that surface is left to chance.
- **Is there a dark scheme, or only light?** If the product needs it and it is absent, define it.
- **Do contrasts meet WCAG AA** (4.5:1 for normal text)? A pretty token that cannot be read is an accessibility bug.
- **Are `error`, `surface`, and `outline` present?** They are the ones that usually go missing and then get hardcoded.
- **Are radii and spacing a system** (multiples of 8dp) or loose values?

Report the gaps to the user and propose values. Do not silently change what contradicts something already defined: an existing token may come from the brand.

---

## `DESIGN.md` Format

Tokens go in YAML blocks. This is the contract Step 3 consumes:

```yaml
colors:
  light:
    primary: "#4F46E5"
    on-primary: "#FFFFFF"
    primary-container: "#E0E7FF"
    on-primary-container: "#1E1B4B"
    secondary: "#0EA5E9"
    on-secondary: "#FFFFFF"
    background: "#FDFCFF"
    on-background: "#1B1B1F"
    surface: "#F5F3FA"
    on-surface: "#1B1B1F"
    outline-variant: "#C7C5D0"
    error: "#B3261E"
    on-error: "#FFFFFF"
  dark:
    primary: "#A5B4FC"
    on-primary: "#1E1B4B"
    # ... the same set of tokens
typography:
  display: "Hanken Grotesk"
  body: "Inter"
rounded:
  small: 4
  medium: 8
  large: 16
```

Each `colors:` token maps 1:1 to a `MaterialTheme.colorScheme` property.

### Step 3 — Map tokens to the theme

Translate `DESIGN.md` into `lightColorScheme(...)` / `darkColorScheme(...)`, `Typography`, and `Shapes`, in the shared design layer.

**Detailed reference:** [design_system_mapping.md](references/design_system_mapping.md) — full token → `ColorScheme` table, font loading, and shape mapping.

### Step 3b — Resources: create the structure and request fonts

Compose Multiplatform resources live in the design module under `src/commonMain/composeResources/`. Create the three folders even if they start empty: if they do not exist, everyone invents where things go and they scatter across modules.

```
core/design-system/src/commonMain/composeResources/
├── drawable/            # icons and images (Res.drawable.*)
├── font/                # typefaces (Res.font.*)
└── values/strings.xml   # text (Res.string.*)
```

The module needs `implementation(compose.components.resources)`.

> [!WARNING]
> **A font is a binary: you cannot create it, and you must not degrade it silently.** If `DESIGN.md` declares `typography: display: "Plus Jakarta Sans"` and the `.ttf` is not present, `Res.font.plusjakartasans_regular` will not compile. The easy way out is to drop in `FontFamily.Default` and move on — and then `DESIGN.md` **lies**: the token file says the app uses a font the app does not use. Nobody finds out until the designer looks at a screen.
>
> When a file is missing:
> 1. **Tell the user exactly which files to add and where**, with the final name. Compose Resources requires lowercase and underscores: `plusjakartasans_regular.ttf`, `plusjakartasans_bold.ttf` → `Res.font.plusjakartasans_regular`.
> 2. **Ask whether they want to supply them now or start with the system font.**
> 3. If they start with the system font, leave the trail visible in code **and** call it out in your reply:
>
> ```kotlin
> // WRONG — DESIGN.md declares Plus Jakarta Sans and this contradicts it with no trace
> val AppTypography = Typography(
>     headlineLarge = TextStyle(fontFamily = FontFamily.Default, ...)
> )
>
> // RIGHT — explicit fallback, with the debt recorded in one place
> // TODO(design): DESIGN.md declares Plus Jakarta Sans (display) and Inter (body).
> // The .ttf files are missing from composeResources/font/. Once added, replace with:
> //   FontFamily(Font(Res.font.plusjakartasans_bold, FontWeight.Bold), ...)
> private val DisplayFontFamily = FontFamily.Default
> private val BodyFontFamily = FontFamily.Default
> ```
>
> Centralize the fallback in a constant; never repeat `FontFamily.Default` in every `TextStyle`. When the fonts arrive it changes in one place, not nine.

### Step 4 — Apply to the screens

Always consume from the theme, never literals.

**Detailed reference:** [mobile_ui_guidelines.md](references/mobile_ui_guidelines.md) — touch ergonomics, touch targets, component specs, and anti-patterns.

### Step 5 — Verify

The first two checks are read from code; the last two **require running the app**.

- No literals in the presentation layer: `grep -rn "Color(0x"` over the screens must come back empty.
- Every interactive element is 48x48dp or larger.
- **Safe areas**: no text is covered by the status bar and no action sits under the navigation bar. If the project has `enableEdgeToEdge()` and the root does not apply `WindowInsets.safeDrawing`, this is **broken** even though it compiles — see the safe-areas section in the UI reference.
- The app looks consistent in light **and** dark, if both are defined.

---

## When to Use

- When designing and coding new mobile screens or flows.
- When refactoring views to align them with a design system.
- When creating reusable components in the shared design module.

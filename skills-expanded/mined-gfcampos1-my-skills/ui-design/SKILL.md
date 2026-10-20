---
name: ui-design
description: "UX/UI design skill for web and mobile apps. Use when implementing any visual component, page, screen, or design system. Covers design style selection (Glassmorphism, Neumorphism, Material, Flat, Minimal/Linear, Aurora), typography, color palettes, and produces Tailwind/CSS implementation examples. Trigger phrases: 'design', 'UI', 'UX', 'component visual', 'tela', 'interface', 'estilo visual', 'layout', 'theme', 'design system'."
argument-hint: "Descreva o que será implementado (ex: 'dashboard de finanças', 'formulário de login', 'card de transação')"
---

# UI Design Skill

This skill guides the design decision process before implementing any visual component or screen. It interviews the user, recommends the best-fit design styles for the context, collects typography and color choices, and outputs concrete Tailwind/CSS implementation examples.

## When to Use

Load this skill before implementing:
- New screens or pages
- New components with significant visual surface (cards, modals, dashboards, forms)
- Design system setup or theme changes
- Any task where the breakdown or plan mentions "UI", "layout", "component", or "design"

---

## Procedure

### Step 1 — Analyze Context

Before asking anything, read the task description, spec (`docs/specs/`), and any existing theme/design files in the codebase:
- Look for `theme.json`, `theme.css`, `tailwind.config.js`, or any existing design tokens.
- Identify the **app category** (finance, productivity, e-commerce, social, etc.).
- Identify the **component type** (dashboard, data table, form, navigation, card, modal, etc.).
- Check if a design system is already established in the codebase — if so, follow it unless the user explicitly wants to change.

### Step 2 — Recommend Design Styles

Based on the app category and component type, select **2–3 most appropriate styles** from [design-systems.md](./references/design-systems.md) and present them to the user.

For each recommended style, show:
1. Name + one-line description
2. Best suited for (your reasoning based on the current context)
3. A minimal Tailwind CSS example snippet for the specific component being built

Then ask the user to pick one (or a blend — e.g., "Minimal base with Glassmorphism accents").

**Selection guidance by context (quick reference):**
| Context | Top recommendations |
|---------|-------------------|
| Finance dashboard | Minimal/Linear, Glassmorphism, Material 3 |
| Data-heavy tables | Material 3, Carbon, Flat |
| Mobile-first app | Material 3, Neumorphism, Flat |
| SaaS product | Minimal/Linear, Flat, Aurora |
| Marketing/landing | Aurora, Glassmorphism, Brutalism |
| Admin panel | Material 3, Carbon, Flat |

### Step 3 — Typography Interview

Ask the user about typography. Load [typography.md](./references/typography.md) and present the top 3 font choices for the chosen style, with:
- Font name + pairing (heading / body)
- Visual scale example (H1 → Body → Caption sizes)
- Import snippet (Google Fonts / local)

Ask: heading font, body font, base scale preference (compact / default / spacious).

### Step 4 — Color Palette Interview

Ask the user about color. Load [color-palettes.md](./references/color-palettes.md) and present 3 palette options suited to the chosen design style, each showing:
- Primary, surface, background, accent, text hex values rendered as a named swatch list
- The emotional/brand tone it conveys
- A short Tailwind config extension snippet

Ask: preferred palette, or custom primary color to generate a palette around.

### Step 5 — Output Design Tokens

After all choices, produce a consolidated design token block:

```css
/* Design Tokens — [Feature Name] */
/* Style: [chosen style] | Typography: [fonts] | Palette: [palette name] */

:root {
  /* Colors */
  --color-primary: #...;
  --color-primary-hover: #...;
  --color-surface: #...;
  --color-background: #...;
  --color-text: #...;
  --color-text-muted: #...;
  --color-accent: #...;
  --color-border: #...;

  /* Typography */
  --font-heading: '...', sans-serif;
  --font-body: '...', sans-serif;
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;

  /* Spacing */
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-full: 9999px;
}
```

Also output the `tailwind.config.js` extension block mapping these tokens.

### Step 6 — Implementation Example

Produce a complete, styled example of the specific component being built using the chosen design style, typography, and palette. This should be production-ready Tailwind JSX (React) that the Execute agent can use as the visual baseline.

---

## Constraints

- DO NOT skip the interview — never choose a design style without asking the user.
- DO NOT generate generic examples — always tailor to the specific component being built.
- DO NOT invent color values arbitrarily — derive systematic palettes (use HSL steps or reference established palettes from [color-palettes.md](./references/color-palettes.md)).
- If a design system already exists in the codebase, flag it explicitly and ask whether to extend or replace it.
- Always consider accessibility: minimum 4.5:1 contrast ratio for text, sufficient touch target sizes (min 44×44px) for interactive elements.

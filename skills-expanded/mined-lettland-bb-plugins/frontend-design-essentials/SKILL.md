---
name: frontend-design-essentials
description: Use for design tokens, design systems, Figma→code, component architecture, typography, color — the whole visual layer.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [frontend-tailwind, frontend-daisyui, frontend-shadcn-ui, react, ux-wcag-a11y]
---

# Frontend Design Essentials

**Iron Law: tokens at the bottom, components in the middle, pages on top. Never hard-code colors/spacing in component CSS. Dark mode from day one.**

| Layer           | Holds                                               | Consumed by          |
| --------------- | --------------------------------------------------- | -------------------- |
| Scale tokens    | `--color-blue-500`, `--space-4`, `--radius-md`      | Semantic tokens only |
| Semantic tokens | `--color-action`, `--color-surface`, `--space-card` | Components           |
| Primitives      | `Button`, `Input`, `Icon`                           | Patterns             |
| Patterns        | `Form`, `Modal`, `Toast`                            | Pages                |

## Design tokens — two layers

Mixing scale and semantic is the most common mistake.

```css
:root {
  /* scale — objective */
  --color-blue-500: oklch(60% 0.18 250);
  --space-4: 1rem;
  /* semantic — intent, references scale */
  --color-action: var(--color-blue-500);
  --space-card-padding: var(--space-4);
}
.button {
  background: var(--color-action);
  padding: var(--space-card-padding);
}
```

**Components use semantic only. Scale stays private.** This seam is what makes reskinning tractable.

**Naming.** kebab-case, category-prefixed (`color-`, `space-`, `radius-`, `shadow-`, `font-`, `z-`). Scale: `<category>-<scale>-<step>`. Semantic: `<category>-<role>-<state?>`. **Avoid** value-in-name (`color-red-error` rots when red becomes orange) and component-in-name (`color-button-bg` couples token to component). **Tooling:** Style Dictionary / Theo (multi-platform), Tailwind v4 `@theme { ... }` (collapses build step), DTCG JSON for portability, Figma Variables on the design side.

## Color systems

| Space     | Use when                                                      |
| --------- | ------------------------------------------------------------- |
| **OKLCH** | **Palettes + lightness scales** — perceptually uniform        |
| HEX       | Storage, paste from designers                                 |
| HSL       | Quick by-hand tweaks (uneven perception — don't build scales) |
| P3        | Wide-gamut displays                                           |

Per hue, 10 steps (50, 100…900, 950) at consistent OKLCH lightness. Required hues: **primary** (brand/action), **neutral** (warm or cool grey, never pure black), **status** (success/warning/danger/info).

**WCAG contrast (non-negotiable).** AA: 4.5:1 body, 3:1 large/UI. AAA: 7:1 body, 4.5:1 large. **Check both themes** — AA on light + AA on dark are two problems. APCA (Lc) replaces WCAG 2.x in WCAG 3 drafts; track but not legal yet.

**Dark mode strategies (ordered):** 1) **Semantic token swap** — same names, different values per `[data-theme]`. Components untouched. **Recommended.** 2) **`color-mix()`** to derive `hover`/`active` at runtime. 3) **`light-dark()`** — modern browsers, dual-value. Loses explicit `data-theme` for 3+ themes. Don't: duplicate components per theme, JS-driven re-renders, `filter: invert()`.

**Colour blindness.** ~8% of men. **Don't encode meaning in hue alone** — pair status colours with icons (✓/✕) or text. Test with simulators (Sim Daltonism, Stark, Chrome devtools).

## Typography

Pick **one modular scale ratio** for the whole product. Multiple = noise.

| Ratio     | Name            | Feel                      |
| --------- | --------------- | ------------------------- |
| 1.125     | Major second    | Editorial-light           |
| 1.200     | Minor third     | Calm, app-friendly        |
| **1.250** | **Major third** | **Balanced web standard** |
| 1.333     | Perfect fourth  | Confident marketing       |
| 1.500     | Perfect fifth   | Dramatic hero             |

Calculate once at typescale.com / utopia.fyi, commit as tokens. **Leading (unitless):** display 1.0–1.2, subheads 1.2–1.35, body UI 1.4–1.5, long-form 1.5–1.7, dense tables 1.2–1.3. **Bigger text → tighter leading.**

**Pairing + weights.** Two fonts max (same family + weights is safest — Inter 400+700; sans+serif classic, match x-height). Three weights max (400, 500/600, 700). Variable fonts ship the range smaller than two statics. **Web font loading:** `font-display: swap` (FOUT, readable) for UI. `optional` only if cached. `block` (default!) → FOIT, hurts LCP. Pair with `size-adjust` on fallback to prevent layout shift (Next.js/Fontaine/Capsize automate). Body min **16px**. Optimal line length **45–75ch** (`max-width: 65ch`).

## Component architecture

**Composition over configuration.** Slots beat prop explosions.

```tsx
// bad: <Card title="X" subtitle="Y" actionLabel="Go" onAction={fn} footer={...} />
<Card>
  <Card.Header>
    <Card.Title>X</Card.Title>
  </Card.Header>
  <Card.Footer>...</Card.Footer>
</Card>
```

**Variants with CVA — no boolean explosions.**

```ts
import { cva, type VariantProps } from "class-variance-authority";
export const button = cva("inline-flex items-center rounded font-medium", {
  variants: {
    variant: { primary: "bg-action text-on-action", ghost: "bg-transparent text-action" },
    size: { sm: "h-8 px-3", md: "h-10 px-4", lg: "h-12 px-6" },
  },
  defaultVariants: { variant: "primary", size: "md" },
  compoundVariants: [{ variant: "primary", size: "sm", class: "shadow-sm" }],
});
type ButtonProps = VariantProps<typeof button> & React.ButtonHTMLAttributes<HTMLButtonElement>;
```

Alternatives: **tailwind-variants** (CVA-compatible + slots), **vanilla-extract recipes** (zero-runtime).

| Pattern                          | Use                                                                    |
| -------------------------------- | ---------------------------------------------------------------------- |
| `children`                       | Single insertion (default)                                             |
| Named slots (`header`, `footer`) | Multiple zones — Modal, Card, Page                                     |
| `asChild` / Radix `Slot`         | "Render with these styles" — avoid nested interactives                 |
| Render-prop slot                 | Slot needs parent state — `<Disclosure>{({open}) => ...}</Disclosure>` |
| Compound (`Card.Header`)         | Tight parent/child, discoverable, typed                                |

**Controlled vs uncontrolled** — support both when in doubt (Radix/React Aria do). Helper `useControllable(controlled, default, onChange)` toggles internal state.

**Prop API rules.** Required props first. Booleans default `false`, positive naming (`disabled`, not `enabled={false}`). `forwardRef` on every DOM wrapper. Spread `...rest` to root for `aria-*`/`data-*`/`id`/`className`. Merge classes via `cn()` (`clsx` + `tailwind-merge`).

**Extract when:** 2+ usages with same shape, non-trivial behaviour (focus trap/ARIA/keyboard), or 3+ sub-elements with relationships. **Don't extract** for one-off layouts or single-className wrappers.

## Design systems (lite governance)

Library = buttons. System = **tokens + primitives (Button/Input/Icon) + patterns (Form/Modal/Toast) + layouts (Stack/Grid/Center) + docs (Storybook/Ladle/MDX, stories beside components) + versioning**, shipped as one unit.

**Versioning (semver, literal):** major = removal/rename/breaking visual; minor = new component/prop/token; patch = bug/doc/internal. **Deprecate before delete** — `@deprecated` for one minor cycle. **Multi-brand:** token layer diverges, components stay neutral. Switch via build target or `data-brand="a"`. **Build a system when:** 2+ apps share UI, design is core to brand, or "which blue?" is recurring.

## Figma → code

Design = intent, code = truth. **Failure modes:** pixel chase (verbatim → magic numbers) and eyeball (drift). Goal: **token alignment** — same names both sides, single source. **Naming alignment is the biggest single win.** Figma `Button/Primary/Large` ↔ code `<Button variant="primary" size="lg" />`. Enforce in lint/CI.

| Figma             | Code                                 |
| ----------------- | ------------------------------------ |
| Collection / Mode | `:root` / `[data-theme]` block       |
| Variable / Alias  | CSS custom property / `var(--other)` |
| Text style        | type token / utility class           |

Pull variables via Figma REST API (`/v1/files/{key}/variables/local`), plugins (Tokens Studio), or Figma MCP (`get_design_context`, `get_code_connect_map`). Normalize to DTCG JSON → Style Dictionary or Tailwind `@theme`. **Code Connect** maps Figma → code component so Dev Mode shows the real snippet (`figma.connect(Button, "<node-url>", {...})`).

**Handoff checklist** before reimplementing: all colours as variables (no raw fills), all text via text styles, Auto Layout for spacing (no manual offsets), components for repeated UI, annotations for states. If not, send it back.

## Anti-patterns

- Hard-coded hex codes in components — always via semantic token
- Token names like "main", "darkBlue", "primary2" — use roles, not values
- Magic numbers for spacing (`margin: 13px`) — must reference the scale
- Retrofitting dark mode — build both day one via semantic swap
- Boolean-prop explosions on buttons (`primary`, `large`, `outlined`, `loading`...) — use CVA `variant`/`size`
- One-off Figma components per variant instead of mapping props
- Versioning components independently from tokens — system ships as one
- Branding via `if (brand === 'a')` in components — that's what tokens are for
- Docs in a wiki separate from code — drifts within weeks
- `filter: invert()` for dark mode — breaks images, shadows, brand

## Red flags

| Thought                                            | Reality                                          |
| -------------------------------------------------- | ------------------------------------------------ |
| "I'll hardcode this hex for now"                   | "For now" = forever. Add the token now.          |
| "Dark mode is a v2 thing"                          | Retrofitting is 5x the cost. Build both day one. |
| "I'll add one more prop to Button"                 | Three booleans = time for CVA variants.          |
| "Designer changed the blue, I'll grep and replace" | You'll miss half. Tokens exist for this.         |

## Hand-off

Tailwind + `@theme`: `Skill(frontend-tailwind)`. Semantic kits: `Skill(frontend-daisyui)`. Copy-paste Radix: `Skill(frontend-shadcn-ui)`. React: `Skill(react)`, `Skill(react)`. A11y: `Skill(ux-wcag-a11y)`.

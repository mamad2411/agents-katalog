---
name: sk-tokens-neomorphism
description: Active design-system tokens for the TimeKast Starter Kit (Neomorphism 2.0) — CSS vars `--neo-*` in `src/app/globals.css`, Tailwind v4 `@theme inline` aliases, utilities (`neo-outset`/`neo-inset`/`neo-interactive` + variants), 3-theme support (light/dark/midnight), and anti-tokens prohibited in kit code. Invoke when writing styles, extending surfaces, or debugging theme drift. For portable token-system patterns → `kb-design-tokens`.
last-verified: 2026-04-23
---

# sk-tokens-neomorphism — TimeKast Kit's Active DS Tokens (Neomorphism 2.0)

> Pair: [`kb-design-tokens`](../kb-design-tokens/SKILL.md). Upstream narrativo: [`.claude/docs/design-system-neomorphism.md`](../../docs/design-system-neomorphism.md). Tokens SSOT: [`src/app/globals.css`](../../../src/app/globals.css). Tailwind v4 mapping: `@theme inline` block (mismo archivo, lines 338-394).

> **Kit-shipped — not portable.** El sistema de tokens del kit es Neomorphism 2.0: **shadows define edges, no borders** (todos los `--*-border` son `transparent` por diseño). Si estás trabajando en un proyecto derivado del TimeKast Starter Kit, estos tokens son tu vocabulario obligatorio — valores hardcoded están prohibidos.

---

## 0. Regla de oro

```
✅ OBLIGATORIO: Usar tokens CSS vars + Tailwind aliases + utilities `neo-*`
❌ PROHIBIDO: Hex literals, `bg-white`, `bg-gray-*`, `shadow-md/lg`, `border-gray-*`, off-scale px
```

Shadows definen edges → **no agregues `border` a surfaces neumórficas** (rompe el efecto óptico). Si necesitas separación visual usa shadow tier distinto (`neo-outset-sm` vs `neo-outset-lg`), no un border.

---

## 1. Token Map (CSS vars → Tailwind alias → Usage)

### 1.1 Colores semánticos

| Token CSS              | Tailwind alias            | Usage                                              |
| ---------------------- | ------------------------- | -------------------------------------------------- |
| `--background`         | `bg-background`           | Page background (surface base; mismo que `--card`) |
| `--foreground`         | `text-foreground`         | Body text                                          |
| `--card`               | `bg-card`                 | Card surface (= background, shadow lo separa)      |
| `--card-foreground`    | `text-card-foreground`    | Text sobre card                                    |
| `--primary`            | `bg-primary`              | Brand blue (CTAs)                                  |
| `--primary-foreground` | `text-primary-foreground` | Text sobre primary                                 |
| `--secondary`          | `bg-secondary`            | Surface secundaria                                 |
| `--muted`              | `bg-muted`                | Surfaces pasivas (empty states, disabled)          |
| `--muted-foreground`   | `text-muted-foreground`   | Text de menor énfasis                              |
| `--accent`             | `bg-accent`               | Highlight sutil (hover, selected)                  |
| `--destructive`        | `bg-destructive`          | Errores, delete                                    |
| `--success`            | `bg-success`              | Success states                                     |
| `--error`              | `bg-error`                | Error states                                       |
| `--warning`            | `bg-warning`              | Warning states                                     |
| `--info`               | `bg-info`                 | Info states                                        |
| `--popover`            | `bg-popover`              | Dropdowns, tooltips, popovers                      |
| `--ring`               | `ring-ring` / `focus:`    | Focus ring (accesibilidad)                         |
| `--border`             | `border-border`           | **= `transparent` en todos los temas** (neumo)     |

### 1.2 Surfaces neumórficas (shadow tokens)

| CSS var              | Utility          | Usage                                                |
| -------------------- | ---------------- | ---------------------------------------------------- |
| `--neo-outset`       | `.neo-outset`    | Elevated surface por defecto (cards, modals)         |
| `--neo-outset-sm`    | `.neo-outset-sm` | Elevación baja (buttons idle, small cards)           |
| `--neo-outset-lg`    | `.neo-outset-lg` | Elevación alta (hero surfaces, featured cards)       |
| `--neo-outset-hover` | —                | Shadow intermedia usada por `.neo-interactive:hover` |
| `--neo-inset`        | `.neo-inset`     | Inputs, recessed surfaces, selected pills            |
| `--neo-inset-sm`     | `.neo-inset-sm`  | Small recessed (chips, tags en estado "on")          |
| `--neo-pressed`      | `.neo-pressed`   | Botón presionado (active)                            |
| `--neo-float`        | `.neo-float`     | Floating overlays (toast, dropdown, popover)         |
| `--neo-flat`         | `.neo-flat`      | `box-shadow: none` — opt-out explícito               |

### 1.2.1 Elevation system — semantic view

Los tokens `--neo-*` mapean a 7 niveles de elevación semántica. Esta vista te dice **cuál elegir** según el rol del componente:

| Nivel                 | Significado                | Aplica a                                                | Token / utility                  |
| --------------------- | -------------------------- | ------------------------------------------------------- | -------------------------------- |
| **Flat**              | Sin superficie (reset)     | Tabla interna dentro de DataTable, resets               | `.neo-flat`                      |
| **Raised (small)**    | Elevación baja interactiva | Buttons idle, icon buttons, filter triggers, paginación | `.neo-outset-sm`                 |
| **Raised (standard)** | Elevación de contenedor    | Cards, sidebar, wrapper de DataTable, BottomNav         | `.neo-outset`                    |
| **Raised (large)**    | Superficie prominente      | Dropdowns, popovers (NO sobre backdrop)                 | `.neo-outset-lg`                 |
| **Overlay**           | Flota sobre backdrop       | Dialogs, sheets                                         | `.neo-float`                     |
| **Sunken (small)**    | Inset / pressed            | Active nav item, botones presionados, toggle tracks     | `.neo-inset-sm` / `.neo-pressed` |
| **Sunken (deep)**     | Totalmente hundido         | Inputs, search fields                                   | `.neo-inset`                     |

**Patrón de interacción:**

- **Hover** sube una superficie un nivel
- **Active / pressed** convierte una surface raised en sunken
- **Containers** permanecen raised; **inputs** permanecen sunken; **overlays** flotan

**4 principios clave:**

1. Hover = subir un nivel; active = press (invertir a sunken)
2. Raised = clickable/container, sunken = input/active, flat = reset
3. Nunca apilar raised-sobre-raised — cancelar elevación interior primero
4. Overlays usan float/drop shadow dedicado, no elevación de container (evita glow borroso sobre backdrops oscuros)

> El composite `.neo-interactive` encadena los 3 estados relevantes para buttons: `outset-sm` (idle) → `outset` (hover) → `pressed` (active). Usarlo en lugar de stackear las utilities a mano.

### 1.3 Component-scoped tokens

| CSS var prefix        | Usage                                                                                           |
| --------------------- | ----------------------------------------------------------------------------------------------- |
| `--sidebar-*`         | Sidebar surface, foreground, active                                                             |
| `--header-*`          | App header                                                                                      |
| `--input-*`           | Form inputs (`bg`, `border`, `focus`)                                                           |
| `--table-*`           | Table header/row/hover/border                                                                   |
| `--badge-{color}-*`   | 7 badge palettes × 3 slots (`bg`/`text`/`dot`) — purple, blue, slate, emerald, red, amber, pink |
| `--showcase-banner-*` | Template showcase banner (removable)                                                            |

### 1.3.1 Sidebar vars × 3 themes

Enumeración del set completo para `--sidebar-*`. Redefinidos en `:root`, `.midnight` y `.dark` en `globals.css`:

| Variable                      | Light (`:root`) | Midnight (`.midnight`) | Dark (`.dark`) |
| ----------------------------- | --------------- | ---------------------- | -------------- |
| `--sidebar-bg`                | `#d5dae2`       | `#1e293b`              | `#18181b`      |
| `--sidebar-foreground`        | `#334155`       | `#94a3b8`              | `#a1a1aa`      |
| `--sidebar-active`            | `#1e40af`       | `#3b82f6`              | `#71717a`      |
| `--sidebar-active-foreground` | `#1e293b`       | `#ffffff`              | `#ffffff`      |
| `--sidebar-border`            | `transparent`   | `transparent`          | `transparent`  |

**Consumo en Tailwind v4:** `bg-(--sidebar-bg)`, `text-(--sidebar-foreground)` (sintaxis de alias dinámico — ver [`kb-tailwind-v4`](../kb-tailwind-v4/SKILL.md) §1).

> Los otros prefijos component-scoped (`--header-*`, `--input-*`, `--table-*`, `--badge-*`) siguen el mismo patrón 3-theme. Para el enum completo, abrir `src/app/globals.css` — este skill no duplica la enumeración exhaustiva (SSOT).

---

## 2. Anti-tokens (prohibidos en kit code)

| Prohibido                               | Por qué                                                              | Alternativa correcta                                               |
| --------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `bg-white` / `bg-black`                 | Rompe 3-theme support; hardcoded                                     | `bg-background` / `bg-card`                                        |
| `bg-gray-{50..900}`                     | No respeta tema; no-neumórfico                                       | `bg-muted` / `bg-secondary` / `bg-accent`                          |
| `text-gray-{50..900}`                   | No respeta tema                                                      | `text-foreground` / `text-muted-foreground`                        |
| `border-gray-*` / `border-{color}-*`    | En neomorphism `--border: transparent` — shadows separan, no borders | Eliminar el border; usar shadow tier                               |
| `shadow-sm/md/lg/xl` (Tailwind default) | No son shadows neumórficas (carecen de highlight)                    | `.neo-outset-sm` / `.neo-outset` / `.neo-outset-lg` / `.neo-float` |
| `#RRGGBB` literal                       | Hardcoded, no-themeable                                              | `var(--token)` o `bg-{semantic}`                                   |
| `rgb(...)` / `rgba(...)` literal        | Igual que hex; salvo opacity ya expresada en token                   | Token existente o extender en `globals.css`                        |
| `p-[17px]` / `w-[173px]` off-scale      | Rompe rhythm; imposible mantener                                     | Scale Tailwind (`p-4`, `w-44`, `gap-6`)                            |
| `!important` para override de tokens    | Señal de que el token no cubre el caso                               | Extender tokens en `globals.css`                                   |
| Inline `style={{ background: '#...' }}` | Bypasea tema                                                         | `className` con alias semántico                                    |
| Editar `src/components/ui/*`            | Shadcn primitives son inmutables (SK.md §3.3)                        | Wrapper en `shared/` o `common/`                                   |

> ℹ️ **Auditoría rápida:** buscar `#` en JSX/CSS (excluyendo fragments/hex en data), o `shadow-md|shadow-lg|bg-white|bg-gray-` en `src/**/*.tsx`. Violations >10 → crear follow-up issue.

---

## 3. Escalas

| Scale          | Valores                                                                                                                                        | Alias Tailwind / Utility                                           |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Radius**     | `--radius: 0.75rem` (12px, kit default)                                                                                                        | `rounded-md` / `rounded-lg` (via theme)                            |
| **Spacing**    | Tailwind default (0, 0.5, 1, 2, 3, 4, 6, 8, 12, 16, 24…) + custom `--spacing-10` (2.5rem), `--spacing-50` (12.5rem) para `min-w-10`/`min-h-50` | `p-*`, `m-*`, `gap-*`, `space-*`, `min-w-10`, `min-h-50`           |
| **Elevation**  | 4 tiers outset + 3 inset + float + flat                                                                                                        | `.neo-outset-sm` → `.neo-outset` → `.neo-outset-lg` → `.neo-float` |
| **Typography** | `--font-sans: var(--font-geist-sans)`, `--font-mono: var(--font-geist-mono)`                                                                   | `font-sans`, `font-mono`                                           |
| **Transition** | Global `* { transition: bg/shadow/border/color 0.1-0.2s ease }`                                                                                | (aplicado global; no hace falta util)                              |

> No agregues valores off-scale. Si el scale no cubre → discute en PR y extiende `globals.css`, no pongas arbitrary values.

---

## 4. Utility classes (kit-shipped)

Definidas en `globals.css` § "NEUMORPHIC UTILITY CLASSES" (lines 485-547). **Todas añaden `border: none`** — shadows definen edges.

| Class              | Estado                 | Uso típico                                                                     |
| ------------------ | ---------------------- | ------------------------------------------------------------------------------ |
| `.neo-outset`      | Idle elevated          | Cards, modals, section containers                                              |
| `.neo-outset-sm`   | Idle elevated (small)  | Buttons idle, compact cards                                                    |
| `.neo-outset-lg`   | Idle elevated (large)  | Hero cards, featured surfaces                                                  |
| `.neo-inset`       | Recessed               | Inputs, selected tabs, active pills                                            |
| `.neo-inset-sm`    | Recessed (small)       | Chips, small selected states                                                   |
| `.neo-pressed`     | Pressed                | Button `:active`                                                               |
| `.neo-float`       | Floating               | Toast, popover, dropdown                                                       |
| `.neo-flat`        | No elevation           | Opt-out explícito (e.g., inline ghost btn)                                     |
| `.neo-interactive` | Idle + hover + active  | Composite para botones — auto-transiciona entre `outset-sm`→`outset`→`pressed` |
| `.neo-focus`       | Focus-visible (outset) | Agregar a elementos interactivos elevated                                      |
| `.neo-focus-inset` | Focus-visible (inset)  | Agregar a inputs                                                               |
| `.focus-ring`      | Outline-based focus    | Links, non-neumo elementos                                                     |

**Ejemplo composición correcta:**

```tsx
<button className="neo-interactive neo-focus rounded-md bg-primary px-4 py-2 text-primary-foreground">
  Click me
</button>

<input className="neo-inset neo-focus-inset rounded-md bg-input px-3 py-2 text-foreground" />
```

---

## 5. 3-theme support

| Theme        | Trigger class      | Background base                      | Estrategia neumórfica                                                 |
| ------------ | ------------------ | ------------------------------------ | --------------------------------------------------------------------- |
| **Light**    | `:root` / `.light` | `#e0e5ec` (warm gray, NO pure white) | Shadows: `--neo-light` (beige) + `--neo-dark` (blue-gray)             |
| **Midnight** | `.midnight`        | `#1a2332` (deep blue)                | Shadows: `--neo-light` (mid-blue) + `--neo-dark` (near-black)         |
| **Dark**     | `.dark`            | `#2d2d32` (charcoal)                 | Shadows: `--neo-light` (lighter charcoal) + `--neo-dark` (near-black) |

Cada tema redefine el mismo set completo de `--*` vars en `globals.css`. **Tu código siempre escribe alias semánticos** (`bg-background`, `.neo-outset`) — el tema se encarga del resto al cambiar la clase en `<html>`.

> Provider: `next-themes` (ver `src/app/providers.tsx`). Los 3 temas deben verse correctos para todo componente/página.

---

## 6. Cómo extender el DS

### 6.1 Agregar una nueva surface variant (ej: `neo-ghost`)

1. Agrega el shadow CSS var en **los 3 temas** (`:root`, `.midnight`, `.dark`) en `globals.css`:
   ```css
   --neo-ghost: 2px 2px 4px var(--neo-dark), -2px -2px 4px var(--neo-light);
   ```
2. Agrega la utility class en § NEUMORPHIC UTILITY CLASSES:
   ```css
   .neo-ghost {
     box-shadow: var(--neo-ghost);
     border: none;
   }
   ```
3. Documenta en esta skill (tabla §1.2 + §4) y en `.claude/docs/design-system-neomorphism.md`.
4. No agregues utilities de un solo uso — si no vas a usarla en 2+ lugares, aplica el shadow inline con `style={{ boxShadow: '...' }}` **PROHIBIDO** → usa una de las existentes o discute.

### 6.2 Agregar un color semántico nuevo

1. Definir en los 3 temas en `globals.css`: `--brand-accent: #...`
2. Agregar alias Tailwind en `@theme inline`: `--color-brand-accent: var(--brand-accent);`
3. Ya disponible como `bg-brand-accent` / `text-brand-accent`.

### 6.3 Agregar una nueva elevation tier

Nombra con sufijo consistente (`-xs`, `-xl`) siguiendo el patrón `outset-sm` → `outset` → `outset-lg`. Mantén la relación `{offset}px {offset}px {blur}px` proporcional.

---

## 7. Anti-patterns kit-específicos

| Anti-pattern                                              | Regla                                                                                                                       |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Editar `src/components/ui/button.tsx` para cambiar shadow | SK.md §3.3 — primitives shadcn son inmutables. Wrapper en `shared/`.                                                        |
| `<div style={{ boxShadow: '6px 6px 12px ...' }}>`         | Usar `.neo-outset` (el shadow ya está en token)                                                                             |
| `<Card className="shadow-md">`                            | `shadow-md` no es neumórfico → `className="neo-outset"`                                                                     |
| `bg-gray-100` para hover state                            | `hover:bg-accent` o `.neo-interactive` composite                                                                            |
| `border border-gray-200` para separar cards               | En neumo los cards se separan con shadow, no border. Eliminar el border y usar `gap-*` en el parent o escalón de elevation. |
| Hardcoded `!important` para overrides                     | El token no cubre tu caso → extiende `globals.css`                                                                          |
| Agregar CSS var a un solo tema                            | **SIEMPRE** definir var en los 3 temas, aunque el valor sea idéntico                                                        |

---

## 8. Pointer — dónde vive qué

| Artefacto                          | Path                                                                                            |
| ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| **SSOT de tokens CSS**             | `src/app/globals.css` (3 theme blocks + @theme inline)                                          |
| **Tailwind v4 setup**              | `postcss.config.mjs` (`@tailwindcss/postcss` plugin) + `@import 'tailwindcss'` en `globals.css` |
| **Config sources (Tailwind scan)** | `@source '../../src/config'` en `globals.css`                                                   |
| **Utility classes `neo-*`**        | `src/app/globals.css` § NEUMORPHIC UTILITY CLASSES                                              |
| **Narrativa del DS**               | `.claude/docs/design-system-neomorphism.md`                                                     |
| **Theme provider / switcher**      | `next-themes` via `src/app/providers.tsx`                                                       |
| **Shadcn primitives (inmutables)** | `src/components/ui/*` — NO editar (SK.md §3.3)                                                  |

---

Cross-reference: [`kb-design-tokens`](../kb-design-tokens/SKILL.md) — portable token-system patterns. [`kb-tailwind-v4`](../kb-tailwind-v4/SKILL.md) — Tailwind v4 `@theme inline` syntax and CSS-first config. [`kb-design-system`](../kb-design-system/SKILL.md) — DS discipline universal (stack-agnostic). [`sk-ui`](../sk-ui/SKILL.md) — components que consumen estos tokens. [`sk-features-index`](../sk-features-index/SKILL.md) — kit catalog entry point.

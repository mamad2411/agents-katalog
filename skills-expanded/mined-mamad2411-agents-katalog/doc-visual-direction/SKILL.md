---
name: doc-visual-direction
description: Documentation-phase skill that picks the visual language for a product before implementation — produces inputs for `15_DESIGN.md`, not code. Defines skin family, surface system, typography posture, iconography treatment, motion profile, and aesthetic stance. Route here during `/design`, `/discovery`, or proposal work when the product lacks identity or the UI feels generic. Not auto-loaded during coding.
last-verified: 2026-04-23
---

# Visual Direction — Documentation Phase

> **Phase:** Discovery / Design — produces content for `project/project/planning/15_DESIGN.md`.
> **Not a coding skill.** This skill decides the visual language; `kb-design-engineering` + `kb-ui` + `kb-tailwind-v4` implement it.
> **Prefix `doc-*`** signals documentation-phase purpose — won't auto-load during `/implement`.

---

## 1. When to use

**Use during:**

- `/design` workflow — producing the visual direction section of `15_DESIGN.md`
- `/discovery` when the product needs an initial aesthetic posture
- Proposal / kickoff work — choosing a skin family before committing to tokens
- UI audits where the product "feels generic" and needs a cohesive redirection

**Don't use for:**

- Writing or editing actual UI code → `kb-ui`, `kb-design-engineering`
- Token definition → `kb-design-system`
- Tailwind class syntax → `kb-tailwind-v4`
- Dashboard chart design → `kb-dataviz`

---

## 2. Required process

When invoked, produce the following outputs in order:

1. **Product posture** — what the product is trying to signal (precision / warmth / density / aspiration)
2. **Trust vs novelty** — where on the axis the product sits (finance trust = high, creator tool = novelty OK)
3. **Density requirement** — low (editorial), medium (dashboards), high (operator tools)
4. **Skin family recommendation** (§3) + rationale
5. **Surface behavior** — how base / panel / overlay differ
6. **Typography posture** (§4)
7. **Iconography system** (§5)
8. **Motion profile** (§6)
9. **Anti-patterns to avoid** for this product
10. **Optional fallback skin** — second-best choice with why

---

## 3. Skin families

### 3.1 Midnight Executive

**Intent:** premium, trustworthy, dark-forward for finance, admin, analytics, governance.

| Best for                           | Avoid when                          |
| ---------------------------------- | ----------------------------------- |
| Fintech, admin systems, dashboards | Product should feel playful or warm |
| Investor portals, internal tools   | App is mostly editorial content     |

**Visual traits:** deep navy / charcoal backgrounds, restrained accents, layered subtle surfaces, strong hierarchy, premium dark mode, clean stable navigation.

**Tables:** crisp, dense, legible, strong row hierarchy, minimal decoration.
**Icons:** neutral outlines; accent only in KPI / highlighted surfaces.
**Motion:** crisp, restrained, premium.

---

### 3.2 Editorial Premium

**Intent:** typography-led, brand-aware, polished composition with less chrome and more character.

| Best for                              | Avoid when                                     |
| ------------------------------------- | ---------------------------------------------- |
| AI products, content platforms        | Extremely dense operational software dominates |
| Founder tools, premium B2B dashboards | —                                              |

**Visual traits:** stronger heading presence, more composition rhythm, fewer generic cards, better whitespace discipline, elegant hierarchy.

---

### 3.3 Dense Operator

**Intent:** high-clarity interface for serious multi-step operational work.

| Best for                              | Avoid when                                     |
| ------------------------------------- | ---------------------------------------------- |
| Ops, logistics, trading-like UIs      | Product should feel soft, aspirational, luxury |
| Internal consoles, monitoring systems | —                                              |

**Visual traits:** compact surfaces, strong zoning, stable shells, hierarchy through density and grouping, less decorative styling.

---

### 3.4 Soft Glass Accent

**Intent:** modern premium feel using restrained translucency on overlays, not as the full system.

| Best for                                          | Avoid when                                |
| ------------------------------------------------- | ----------------------------------------- |
| Premium dashboards, AI apps, command-heavy shells | Interface is highly dense                 |
| Consumer-facing modern products                   | Accessibility contrast is already fragile |

**Rules:** don't make every panel glass; prefer glass on overlays, highlighted widgets, topbars, or command surfaces; maintain strong contrast and readable boundaries.

---

### 3.5 Warm Productive

**Intent:** human, approachable, calm for wellness, education, creator, family-oriented products.

| Best for                           | Avoid when                                    |
| ---------------------------------- | --------------------------------------------- |
| Education, creator tools, wellness | Brand must feel highly formal / institutional |
| Family-focused apps                | —                                             |

---

## 4. Typography posture

Choose one posture — it sets heading weight, scale ratio, and rhythm:

| Posture          | Ratio       | Use with                                  |
| ---------------- | ----------- | ----------------------------------------- |
| Dense technical  | 1.125 – 1.2 | Dense Operator, finance tables            |
| Balanced product | 1.25        | Midnight Executive, general dashboards    |
| Editorial        | 1.333       | Editorial Premium, AI / content platforms |
| Hero / landing   | 1.5 – 1.618 | Marketing surfaces, premium consumer apps |

Pair with a typeface family decision: neutral sans for operator tools, humanist sans for warm productive, display serif/mono for editorial.

---

## 5. Iconography system

### Tiered library strategy

1. **Base system icons** — Lucide or Tabler. Used for navigation, actions, utilities, CRUD, settings.
2. **Accent / expressive icons** — Phosphor or custom SVG. Used for KPI cards, highlights, marketing surfaces, premium callouts.
3. **Brand / domain icons** — custom SVG for product-specific entities. Use sparingly.

### Policy rules

- Navigation icons stay neutral and consistent
- KPI cards may use richer treatment (filled, duotone, gradient container)
- Don't mix too many icon families on the same surface
- Glow / gradients only in accent contexts
- Outline icons are safer for system-level navigation
- Filled / duotone only in emphasis roles
- Money / dense data → preserve trust and precision (outline, consistent stroke)

### Anti-patterns

- Random mixing of icon sets
- Inconsistent stroke weights
- Over-glowing every icon
- Decorative icons in dense tables
- Duotone everywhere
- Icons without a role distinction

---

## 6. Motion profile

### Tone (choose one per product)

| Tone       | Description                 | Best for                       |
| ---------- | --------------------------- | ------------------------------ |
| Calm       | Slow, gentle, breathing     | Wellness, education            |
| Crisp      | Fast, snappy, immediate     | Admin, operator tools          |
| Premium    | Smooth, deliberate, elegant | Fintech, executive dashboards  |
| Restrained | Minimal, functional only    | Dense data tools               |
| Reduced    | Near-zero motion            | A11y-first, monitoring systems |

### Interaction feedback (define behavior per state)

- **Hover** — subtle scale, shadow lift, or background shift
- **Pressed** — inward motion (scale down) or color shift
- **Selected** — persistent indicator (underline, fill, ring)
- **Focused** — visible focus ring, meets WCAG
- **Disabled** — reduced opacity, no interaction feedback

### Container transitions

| Element                 | Recommendation                 |
| ----------------------- | ------------------------------ |
| Modal                   | Scale + fade from center       |
| Drawer                  | Slide from edge                |
| Tooltip                 | Fade with slight offset        |
| Page transitions        | Cross-fade or slide (if SPA)   |
| Tab / content switching | Fade or slide within container |

### Data-UI motion rules

- Tables: row highlight on hover, sort animation optional
- Charts: staggered entrance on load, tooltip follows cursor
- KPI cards: count-up on first paint
- Filters: smooth height transitions when toggling
- Empty states: gentle fade-in

### Reduced motion strategy

When `prefers-reduced-motion: reduce`:

- Remove all decorative transitions
- Keep state-change indicators (selected, focus)
- Use instant visibility changes instead of animated ones

---

## 7. Global anti-patterns

- Generic "clean SaaS" with no character
- Overusing cards until the UI loses hierarchy
- All surfaces at the same depth
- Neon accents without strong rationale
- Glassmorphism as the full system default
- Neumorphism for dense productivity tools
- Trendy style choices that weaken trust
- Purple / violet by default (AI-product cliché)
- Mesh / aurora gradients as lazy background

---

## 8. Output format — what to write into `15_DESIGN.md`

Always produce:

- **Chosen skin** + rationale (why this product needs this skin)
- **Visual tone** (1-paragraph narrative description)
- **Surface rules** (base / panel / overlay behavior)
- **Typography posture** (family + scale ratio + weight decisions)
- **Icon strategy** (base library + accent library + allowed styles)
- **Motion profile** (tone + interaction feedback rules)
- **Anti-patterns for this product** (what to avoid, with rationale)
- **Optional fallback skin** (second choice + when to prefer it)

---

## 9. Handoff to coding-phase skills

`doc-visual-direction` es **fase design** — produce la dirección visual que alimenta `15_DESIGN.md`. Después de cerrar la dirección, la **fase coding** toma el relevo a través de las skills siguientes:

| Skill                   | Consumes what this skill produced                                                                                    |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `kb-design-tokens`      | Portable token-system discipline (what a token system is, anti-tokens, scales, swap rule)                            |
| `sk-tokens-neomorphism` | Kit-shipped tokens concretos del DS activo (CSS vars `--neo-*`, Tailwind aliases, anti-tokens específicos, 3 themes) |
| `kb-design-system`      | Token discipline; the scale rules to apply consistently                                                              |
| `kb-tailwind-v4`        | Class syntax for the repo's Tailwind v4 setup                                                                        |
| `kb-design-engineering` | Polish execution process; how to apply the skin                                                                      |
| `kb-ui`                 | React/Next.js component patterns for the stack                                                                       |

**Regla de handoff (par `kb-design-tokens` + `sk-tokens-neomorphism`):** cuando `/design` cierra la dirección visual, la implementación consume `sk-tokens-neomorphism` (tokens shipped por el kit) + `kb-design-tokens` (discipline portable). Si el DS cambia (ej: swap neumorphism → glassmorphism), se reemplaza la skill concreta de tokens actual (`sk-tokens-neomorphism`) por la nueva variante del kit; `kb-design-tokens` sobrevive al swap porque modela el sistema de tokens en abstracto, no los valores concretos.

- [`kb-design-tokens`](../kb-design-tokens/SKILL.md) — patterns portable de token systems
- [`sk-tokens-neomorphism`](../sk-tokens-neomorphism/SKILL.md) — tokens concretos del DS activo del kit

---

_TimeKast Factory — doc-visual-direction (documentation-phase, not coding)_

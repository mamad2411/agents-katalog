---
name: kb-design-system
description: Portable design-system discipline — stack-agnostic rules for tokens, component-kit reuse, scale consistency (radius/spacing/shadow), multi-theme coherence, plus core UX laws (Hick/Fitts/Miller), 60-30-10 color rule, and typography scales. Route here when reviewing UI for consistency, auditing tokens, deciding kit-vs-inline, or enforcing multi-theme behavior.
last-verified: 2026-04-23
---

# Design System — Universal Discipline

> **Scope:** Stack-agnostic. Same rules apply to React/Tailwind, Flutter/Material, SwiftUI, or vanilla CSS.
> **Goal:** Consistency through tokens, kit reuse, and scale discipline. Premium feel comes from restraint, not decoration.

---

## 1. Core principles

1. **Tokens over values** — every color/spacing/radius/shadow comes from the system, never a literal.
2. **Kit over inline** — use the component kit; if something isn't in the kit and it should be, extend the kit (don't re-invent it in a page).
3. **Scale over arbitrary** — stick to the predefined scale. Three values of the same concept (three random radii, three random paddings) on one screen is a bug.
4. **Multi-theme always** — verify coherence in every theme the project defines, not just the default.
5. **Paradigm-agnostic** — these rules are true for neumorphism, glassmorphism, material, and custom skins. They're about discipline, not aesthetics.

---

## 2. Five anti-patterns to catch on review

### 2.1 Hardcoded values instead of tokens

| ❌                       | ✅                                          | Why                                   |
| ------------------------ | ------------------------------------------- | ------------------------------------- |
| Hex/literal color inline | Token from the system (CSS var, theme prop) | Themes can't override inline values   |
| Literal shadow           | Shadow token                                | Each paradigm defines shadows its way |
| Fixed pixel radius       | Radius token                                | Consistency with the defined scale    |

Examples across stacks:

| Stack        | ❌ Hardcoded            | ✅ Token                                   |
| ------------ | ----------------------- | ------------------------------------------ |
| CSS/Tailwind | `#25D366`, `8px`        | `var(--brand-success)`, `var(--radius)`    |
| Flutter      | `Color(0xFF25D366)`     | `Theme.of(context).colorScheme.primary`    |
| SwiftUI      | `.init(red: 0.14, ...)` | `Color.accentColor` from the asset catalog |

### 2.2 Mixing style paradigms

> **Rule:** if the project defines custom tokens for a concept (shadow, radius, spacing), the framework's generic utilities for that concept are **forbidden**. The project redefined them for a reason.

| Stack    | ❌ Generic framework                            | ✅ Project token                     |
| -------- | ----------------------------------------------- | ------------------------------------ |
| Tailwind | Generic shadow utility when custom tokens exist | The custom shadow token              |
| Flutter  | `elevation: 4` when `AppShadows.card` exists    | `AppShadows.card`                    |
| Any      | Framework defaults                              | Tokens defined by the project system |

### 2.3 Inline elements instead of kit components

| ❌                              | ✅                                                      |
| ------------------------------- | ------------------------------------------------------- |
| Raw element with ad-hoc styling | Kit component that inherits styling from the theme      |
| Bare input without wrapper      | Kit `Input` with consistent focus/error/disabled states |
| `<div>` styled like a card      | Kit `Card` component                                    |

> 🔴 **Mandatory:** consult the component inventory before inlining. If it exists → reuse. If not → add it to the kit, not to the page.

| Stack               | Inventory to consult                  |
| ------------------- | ------------------------------------- |
| This repo (Next.js) | `project/reference/INVENTORY.md`      |
| Flutter             | `lib/widgets/` + pubspec dependencies |
| Other               | Project's components directory        |

### 2.4 Scale inconsistency

| ❌                                            | ✅                              |
| --------------------------------------------- | ------------------------------- |
| 3+ different radii on the same screen         | One consistent radius token     |
| Mixed spacing (12, 16, 14) in the same layout | The spacing scale of the system |
| Shadows with arbitrary intensities            | The defined elevation scale     |

> If a screen uses 3+ values for the same visual concept, it's a bug. Design systems define scales on purpose.

### 2.5 Single-theme development

| ❌                                               | ✅                                                       |
| ------------------------------------------------ | -------------------------------------------------------- |
| Only verify light mode                           | Verify **every** theme the project defines               |
| Assume dark = light with inverted colors         | Each theme may have different contrast, spacing, shadows |
| Skip additional themes (midnight, high contrast) | Verify coherence across the full palette                 |

---

## 3. UX laws that shape decisions

| Law                     | Principle                            | Practical use                                        |
| ----------------------- | ------------------------------------ | ---------------------------------------------------- |
| **Hick's Law**          | More choices → slower decisions      | Limit visible options; progressive disclosure        |
| **Fitts' Law**          | Larger + closer = easier to click    | Size primary CTAs; place them near the action source |
| **Miller's Law**        | ~7±2 items in working memory         | Chunk lists, navs, forms                             |
| **Von Restorff Effect** | Different = memorable                | Make the primary CTA visually distinct               |
| **Serial Position**     | First and last items remembered most | Put key items at the start and end of lists          |

---

## 4. Color — the 60-30-10 rule

| Band | Share                                       | Role                              |
| ---- | ------------------------------------------- | --------------------------------- |
| 60%  | Primary / background — calm, low saturation | Fills most of the screen          |
| 30%  | Secondary — supporting surfaces             | Cards, panels, secondary sections |
| 10%  | Accent — CTAs, highlights, destructive      | Used sparingly for attention      |

**If the accent hits ≥20% of the screen it's no longer an accent** — the user stops perceiving it as "the important thing."

### Palette intent — what each family signals

| You want to signal | Consider            | Avoid            |
| ------------------ | ------------------- | ---------------- |
| Trust, calm        | Blue family         | Aggressive reds  |
| Growth             | Green family        | Industrial grays |
| Energy             | Orange / red        | Passive blues    |
| Luxury             | Teal, gold, emerald | Cheap brights    |

### Banned defaults (the "AI look")

When no direction is provided, these are the clichés to avoid:

| AI default               | Why it's bad                        |
| ------------------------ | ----------------------------------- |
| Purple / violet          | Overused AI-product fingerprint     |
| Fintech "deep cyan"      | Safe but forgettable                |
| Mesh / aurora gradients  | Lazy background filler              |
| Glassmorphism everywhere | Becomes the whole UI, not an accent |
| Dark + neon glow         | Generic "AI aesthetic"              |

> Ask for direction before defaulting to one of these.

---

## 5. Typography — scale & readability

### Scale ratios

| Content type   | Ratio     | Feel     |
| -------------- | --------- | -------- |
| Dense UI       | 1.125–1.2 | Compact  |
| General web    | 1.25      | Balanced |
| Editorial      | 1.333     | Spacious |
| Hero / landing | 1.5–1.618 | Dramatic |

Pick one ratio for a product and derive heading sizes from it (`h1 = body × ratio³`, etc.). Mixed ratios create visual noise.

### Readability

| Property         | Target           |
| ---------------- | ---------------- |
| Line length      | 45–75 characters |
| Body line-height | 1.4–1.6          |
| Body font size   | ≥16px on web     |

---

## 6. Spacing rhythm

**Eight-point grid** — all spacing in multiples of 8 (or 4 for dense data UI):

| Bucket | Values |
| ------ | ------ |
| Small  | 4, 8   |
| Medium | 12, 16 |
| Large  | 24, 32 |
| XL     | 48, 64 |

A consistent grid gives the UI rhythm for free. Arbitrary paddings (13px, 19px) break it.

---

## 7. Animation & motion — discipline

| Action   | Easing        | Why                        |
| -------- | ------------- | -------------------------- |
| Entering | `ease-out`    | Settles in naturally       |
| Leaving  | `ease-in`     | Exits with acceleration    |
| Emphasis | `ease-in-out` | Deliberate, symmetric feel |

**Performance rules:**

- Animate only `transform` and `opacity` (cheap on the compositor).
- Respect `prefers-reduced-motion: reduce` — remove decorative motion, keep state indicators.

> For motion profile selection (Calm / Crisp / Premium / Restrained / Reduced) see `doc-visual-direction`.

---

## 8. Review checklist

Before closing any UI task:

- [ ] Every color comes from a token, no literals
- [ ] Shadows, radii, and spacing use system tokens
- [ ] Kit components reused; nothing that belongs in the kit is inlined
- [ ] Values of the same category (radius, spacing, shadow) are consistent within the screen
- [ ] Verified in **every** theme the project defines
- [ ] Primary CTA is visually distinct (Von Restorff) and sized for its priority (Fitts)
- [ ] Accent color stays under ~10% of the screen
- [ ] Typography uses one scale ratio; body line length 45–75 ch, line-height 1.4–1.6
- [ ] Motion respects `prefers-reduced-motion`

---

## 9. Relationship with other skills

| Skill                   | Relationship                                                                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `kb-ui`                 | Stack-specific (Next.js + Tailwind + shadcn). This skill = principles; `kb-ui` = how in React.                                              |
| `kb-tailwind-v4`        | Framework-specific syntax. This skill = token discipline; `kb-tailwind-v4` = Tailwind v4 patterns.                                          |
| `kb-design-engineering` | Execution of visual polish. This skill defines the baseline rules that polish must respect.                                                 |
| `doc-visual-direction`  | Upstream — picks the skin family, motion profile, iconography for a product. This skill governs how those choices are applied consistently. |
| `kb-dataviz`            | Dashboards and charts. This skill governs the surrounding UI; `kb-dataviz` governs chart-specific rules.                                    |

---

_TimeKast Factory — kb-design-system (universal, stack-agnostic)_

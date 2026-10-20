---
name: kb-design-tokens
description: Portable design-token patterns independent of any specific DS — primitive vs semantic layers, anti-tokens rule (no hardcoded hex/px/shadows), scale modeling as discrete tiers, token-to-CSS-var pipeline, theme swapping via remap, and agent discipline (map to nearest token or extend the scale). Route here when designing or auditing a token system. → `sk-tokens-neomorphism` for this kit's active tokens.
last-verified: 2026-04-23
---

# kb-design-tokens — Portable Token System Patterns

> Pair: [`sk-tokens-neomorphism`](../sk-tokens-neomorphism/SKILL.md)

> **Scope:** Stack-agnostic. Applies to CSS variables, Tailwind theme config, styled-components themes, CSS-in-JS, or any token-driven system.
> **Goal:** Every visual value in the product is a named token. No raw hex, no raw px, no arbitrary shadows.

---

## 1. What is a token system

A design token is a **named reference to a value**. The system has two layers:

| Layer         | Purpose                             | Example (conceptual)                                                                  |
| ------------- | ----------------------------------- | ------------------------------------------------------------------------------------- |
| **Primitive** | Literal value, named by what it is  | `color-brand-500`, `space-4`, `radius-md`, `shadow-2`                                 |
| **Semantic**  | Purpose-driven alias of a primitive | `color-btn-primary-bg`, `surface-card-padding`, `radius-control`, `elevation-overlay` |

Components consume **semantic tokens**, never primitives. Primitives are the palette the semantic layer draws from.

```
primitive layer   →   semantic layer   →   component
color-blue-500        color-link-fg        <a> uses color-link-fg
```

Why two layers: when the brand changes blue to teal, you remap one primitive. When a button's bg should stop being the brand color and become a neutral, you remap one semantic. Components never change.

---

## 2. Anti-tokens rule

If a concept is tokenized in the system, **raw values for that concept are forbidden in application code**.

| ❌ Raw value                      | ✅ Token               | Why                                          |
| --------------------------------- | ---------------------- | -------------------------------------------- |
| Hex/rgb/hsl literal in JSX        | Color token            | Can't be themed, audited, or searched        |
| Pixel or rem literal padding      | Spacing token          | Breaks the grid, causes drift                |
| Arbitrary border-radius           | Radius token           | Off-scale radii accumulate visual noise      |
| Inline `box-shadow: ...`          | Elevation/shadow token | Shadows define the paradigm (flat/neo/glass) |
| Font-size / line-height literal   | Typography token       | Type scale must stay coherent                |
| Framework default when DS has own | Project token          | The DS redefined it on purpose               |

**Detection patterns for review** (applies across stacks):

- Any `#RRGGBB`, `rgb(`, `hsl(`, `rgba(` outside the token definition file
- Any arbitrary bracket utility in Tailwind-like systems (e.g. `[17px]`, `[#f3f3f3]`)
- Inline style props carrying color / spacing / shadow / radius values
- Framework-provided generic utilities for concepts the DS has tokenized

---

## 3. Scale modeling — discrete tiers, not arbitrary values

Scales are **discrete** by design. A designer picks 5–8 tiers per axis; anything between tiers is a bug.

### 3.1 Radius scale

| Tier | Typical use                |
| ---- | -------------------------- |
| none | Sharp edges, dividers      |
| xs   | Small chips, badges        |
| sm   | Inputs, small buttons      |
| md   | Default controls, cards    |
| lg   | Modals, large surfaces     |
| xl   | Hero panels, feature cards |
| full | Pills, avatars             |

### 3.2 Spacing scale

Built on a base unit (typically 4 or 8). The scale is multiples, not linear:

```
4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96
```

Off-scale values (13, 17, 22) break rhythm. If a layout "needs" 17px, the real answer is either `16` or `20`.

### 3.3 Elevation scale

Typically 0–5 discrete levels. Each level defines its own shadow recipe (offset, blur, color, possibly a second layer).

| Level | Role                              |
| ----- | --------------------------------- |
| 0     | Flat / no shadow                  |
| 1     | Subtle lift (hover on flat cards) |
| 2     | Resting cards                     |
| 3     | Dropdowns, popovers               |
| 4     | Modals                            |
| 5     | Toasts, notifications             |

### 3.4 Typography scale

Pick one ratio (1.125, 1.25, 1.333, 1.5) and derive tiers from body size:

| Token   | Role                        |
| ------- | --------------------------- |
| display | Hero / marketing headings   |
| h1 – h6 | Document/page headings      |
| body    | Default running text        |
| body-sm | Secondary text, helper copy |
| caption | Meta, timestamps, labels    |
| code    | Monospace inline / block    |

Each tier carries `font-size`, `line-height`, and often `font-weight` as a bundle.

---

## 4. Token → CSS var → utility pipeline

Conceptual flow (works for any CSS / Tailwind / styled-system):

```
tokens.json (source)
  │
  ├─►  generated CSS custom properties   (primitive + semantic vars)
  │       :root { --color-brand-500: ...; --color-btn-bg: var(--color-brand-500); }
  │
  ├─►  generated utility / theme config
  │       bg-brand-500, text-link, rounded-md  ← mapped to vars
  │
  └─►  component code
          consumes semantic utility or semantic var, never raw value
```

Key properties of the pipeline:

1. **One source of truth** for tokens (JSON, YAML, or a TS module) — never hand-write the same value twice.
2. **CSS variables at runtime** — so theme swap happens by re-binding `:root` vars, not re-bundling.
3. **Utility framework config** reads from the same source — Tailwind `theme.colors`, styled-system `theme`, etc.
4. **Components consume the semantic layer** — `text-link`, not `text-blue-500`.

---

## 5. Primitive vs semantic — which layer do agents use?

| Scenario                               | Layer                                 |
| -------------------------------------- | ------------------------------------- |
| Writing a component                    | **Semantic** (`color-btn-primary-bg`) |
| Defining a new semantic token          | Map it to a **primitive**             |
| Adding a new primitive                 | Rare — requires DS owner approval     |
| Theme file overriding brand colors     | Remap **primitives**                  |
| Theme file overriding a component look | Remap **semantics**                   |

> 🔴 **Rule for agents:** in component code, `color-blue-500` (primitive) is almost as bad as `#3b82f6` (raw). If the semantic alias doesn't exist, that's a missing token — propose adding it, don't reach into primitives.

---

## 6. Theme swap via token remap

A theme is **a different set of token → value bindings**, not a different set of components.

```
Light theme:
  --surface-bg: var(--color-neutral-50);
  --text-body:  var(--color-neutral-900);

Dark theme:
  --surface-bg: var(--color-neutral-900);
  --text-body:  var(--color-neutral-50);
```

Components don't know which theme is active — they consume `--surface-bg` and `--text-body`.

Consequences:

- Adding a theme = adding a set of token values + a selector (`.theme-dark`, `[data-theme='midnight']`).
- No component code changes to support a new theme.
- If a screen "only looks right in one theme", the component hardcoded a value — fix the component, not the theme.

---

## 7. Agent discipline — rules when writing/editing UI

1. **Never invent a value.** Hex, px, shadow recipe, font-size — all come from tokens.
2. **Map to nearest token.** If a spec says "18px padding" and the scale has `16` and `20`, pick one — don't create an `18`.
3. **Missing token → propose, don't inline.** If the needed token doesn't exist, the correct move is to add it to the DS, get it approved, and then use it.
4. **Extend the scale with care.** A new tier (e.g. adding `space-20`) changes the system for everyone. Requires DS owner sign-off.
5. **Prefer semantic over primitive.** `text-muted` over `color-neutral-500`. `surface-card` over `color-white`.
6. **Theme-check.** After any token-touching change, verify every theme the project declares (light / dark / any others).

---

## 8. Anti-patterns to reject on review

| Anti-pattern                                                | Why it fails                                                                            |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Arbitrary bracket utility (`[#ff0000]`, `[17px]`)           | Escapes the token system — un-auditable, un-themeable                                   |
| Inline `style={{ color: '#...', padding: 12 }}`             | Same as above, one level worse (no utility class trace)                                 |
| Component defines its own local color palette               | Fragments the DS — every feature drifts in its own direction                            |
| Mixing framework default and project token for same concept | Project redefined it on purpose; framework default is wrong in this DS                  |
| Raw value gated by a comment "TODO: tokenize later"         | It will not get tokenized later. Tokenize now or don't write it.                        |
| `!important` to force a value through a token               | A token that can't win specificity is mis-layered — fix the layering, not the call site |
| Copy-paste of a shadow recipe across components             | That's a missing elevation token                                                        |

---

## 9. Review checklist

Before closing a UI task:

- [ ] No hex / rgb / hsl literals outside the token definition file
- [ ] No arbitrary bracket utilities for color / spacing / radius / shadow
- [ ] Components consume semantic tokens, not primitives
- [ ] No new radius / spacing / elevation / type tier introduced without DS owner approval
- [ ] Any new semantic token is mapped to an existing primitive
- [ ] Every theme the project declares still renders coherently
- [ ] No inline `style` carrying tokenized concepts
- [ ] `!important` not used to force-override a token

---

Cross-reference: [`sk-tokens-neomorphism`](../sk-tokens-neomorphism/SKILL.md) — kit's active DS tokens. [`kb-design-system`](../kb-design-system/SKILL.md) — universal DS discipline. [`kb-tailwind-v4`](../kb-tailwind-v4/SKILL.md) — Tailwind v4 theme config.

---

_TimeKast Factory — kb-design-tokens (portable, stack-agnostic)_

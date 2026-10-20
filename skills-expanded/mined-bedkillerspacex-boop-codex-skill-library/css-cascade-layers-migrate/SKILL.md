---
name: css-cascade-layers-migrate
description: >
  Migrate stylesheets to CSS cascade layers (@layer) on owned frontends: layer
  order, unlayered specificity interactions, framework/vendor layering, and
  incremental adoption without visual regressions. Use when refactoring global
  CSS, design systems, or battling specificity wars with layered architecture.
---

# CSS Cascade Layers Migrate

## Scope And Authorization

- **In scope:** Front-end codebases and design systems you maintain.
- **Out of scope:** Injecting CSS into third-party sites; unauthorized restyling.
- Prefer visual regression tests (Chromatic/Percy/Playwright) before wide rollout.
- Pair with `css-specificity-debugging` and `code-quality-standards`.

## When To Use

- Specificity wars between reset, base, components, utilities, and overrides.
- Introducing `@layer reset, base, components, utilities, overrides`.
- Migrating Bootstrap/Tailwind/custom CSS coexistence.
- Reducing `!important` reliance via explicit layer priority.
- Teaching teams cascade layer semantics vs selector specificity.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Specificity bug hunt only | `css-specificity-debugging` |
| Container queries | `css-container-queries` |
| CSS injection security | `css-injection-exfiltration` |
| Design token architecture alone | design-system skills |
| Implementation quality baseline | `code-quality-standards` |

## Cascade layer rules (essentials)

| Fact | Implication |
| --- | --- |
| Later **layer** wins over earlier layer | Order declaration matters more than selector weight across layers |
| Unlayered styles beat layered styles | Legacy CSS outside `@layer` still dominates — migrate carefully |
| `!important` reverses layer order | Avoid; complicates migration |
| `@import` can load into a layer | `@import url(a.css) layer(components);` |

## Workflow

### 1. Confirm scope and success criteria

1. Inventory stylesheets, CSS-in-JS, and third-party CSS.
2. Success: agreed layer map; key pages pixel-stable; fewer `!important`; docs for contributors.

### 2. Define target layer map

```css
/* Establish order once early in the entry CSS */
@layer reset, base, tokens, components, utilities, overrides;
```

| Layer | Contents |
| --- | --- |
| reset | normalize/reboot |
| base | element defaults, typography |
| tokens | CSS variables (sometimes unlayered intentionally) |
| components | BEM/blocks, design system |
| utilities | atomic helpers |
| overrides | rare app-level fixes |

### 3. Baseline visuals

```bash
# Example
npx playwright test --update-snapshots  # or run existing VRT
```

Capture: home, forms, modals, dense tables, dark mode if any.

### 4. Incremental migration

1. Create empty layers and order first (no visual change yet if no layered rules).
2. Move **reset** into `@layer reset { ... }`.
3. Move components file-by-file into `@layer components`.
4. Leave problematic legacy unlayered until last; track list.
5. Finally layer utilities; remove redundant `!important` where safe.

```css
@layer components {
  .btn {
    padding: 0.5rem 1rem;
    border-radius: var(--radius-sm);
  }
}

@layer utilities {
  .u-hidden {
    display: none;
  }
}
```

### 5. Handle third-party CSS

```css
@import url("vendor.css") layer(vendor);
@layer reset, vendor, base, components, utilities, overrides;
```

Or wrap vendor after build. Ensure vendor layer sits where intentional (often under components).

### 6. Common pitfalls

| Pitfall | Fix |
| --- | --- |
| Forgot unlayered still wins | Layer remaining globals or accept intentional override |
| Layer order redeclared differently | Single source of order in entry file |
| CSS modules + layers | Define strategy for module injection order |
| Shadow DOM | Layers don't cross shadow roots — separate plan |

### 7. Verify and document

1. Re-run VRT; fix regressions by adjusting layer placement not random specificity hikes.
2. Lint guidance: no new unlayered app CSS without review.
3. Contributor doc: which layer for new code.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Order | One entry `@layer a, b, c` | Per-file conflicting orders |
| Migration | Incremental + VRT | Big-bang rewrite Friday |
| Overrides | Rare `overrides` layer | Everything in overrides |
| Vendor | Explicit vendor layer | Unlayered vendor last-wins chaos |
| !important | Remove as layers stabilize | Add more !important to “fix” layers |

## Output Checklist

- [ ] Layer map agreed and documented
- [ ] Entry order established
- [ ] Visual baseline captured
- [ ] Reset/base/components migrated in steps
- [ ] Vendor strategy defined
- [ ] Unlayered remainder inventoried
- [ ] VRT/pass on key flows
- [ ] Contributor guidelines updated
- [ ] !important debt reduced or ticketed
- [ ] Residual unlayered exceptions listed

## Rules

- Unlayered beats layered — know where legacy sits.
- Prefer layer order over specificity hacks.
- Focus on **migrating to CSS cascade layers**.

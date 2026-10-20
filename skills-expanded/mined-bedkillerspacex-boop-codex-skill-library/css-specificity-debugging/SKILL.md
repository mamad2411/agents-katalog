---
name: css-specificity-debugging
description: >
  Debug CSS specificity and cascade conflicts on owned frontends: compute
  specificity tuples, identify winning rules in DevTools, resolve fights with
  refactor (not only !important), and account for layers, inline styles, and
  shadow DOM. Use when styles “won't apply” or overrides behave inconsistently.
---

# CSS Specificity Debugging

## Scope And Authorization

- **In scope:** Stylesheets and components you maintain.
- **Out of scope:** Injecting overrides into third-party production sites without authorization.
- Prefer fixing architecture (layers, methodology) over permanent `!important` debt.
- Pair with `css-cascade-layers-migrate` when layer migration is the real fix.

## When To Use

- A rule appears in DevTools but is struck through.
- Utility classes lose to component selectors.
- Inline styles or ID selectors block theme overrides.
- Post-layer-migration unexpected winners.
- Teaching developers cascade order.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Cascade layers adoption | `css-cascade-layers-migrate` |
| Container queries | `css-container-queries` |
| CSS injection security | `css-injection-exfiltration` |
| Design visual QA only | VRT workflows |
| Implementation quality baseline | `code-quality-standards` |

## Cascade order (simplified)

```text
1. Origin + importance (!important reverses origin order)
2. Cascade layers (unlayered > layered; !important reverses layer order)
3. Specificity
4. Order of appearance
5. Inline style attribute (high specificity)
```

### Specificity tuple (a, b, c)

| Selector piece | Counts as |
| --- | --- |
| Inline `style=""` | Style attribute (above normal selectors) |
| `#id` | a += 1 |
| `.class`, `[attr]`, `:hover` | b += 1 |
| `element`, `::before` | c += 1 |
| `:where()` | Zero specificity |
| `:is()` / `:has()` | Contribution of most specific argument |
| `:not()` | Specificity of argument |

## Workflow

### 1. Reproduce

1. Exact URL, component state, viewport, theme (dark/light).
2. Note expected property/value vs actual.

### 2. DevTools inspection

1. Select element → **Styles** pane.
2. Find property; see which rule wins and which are crossed out.
3. Check **Computed** for final value.
4. Expand inherited vs direct.
5. Note `element.style` (inline) and user-agent rules.

### 3. Compute specificity

```text
Example:
.nav .link.active  → (0, 3, 0)
#nav a             → (1, 0, 1)  wins on a
button             → (0, 0, 1)
:where(.link)      → (0, 0, 0)
```

Document tuple for the losing and winning selectors.

### 4. Check layers and importance

```css
/* Is the losing rule inside @layer while winner is unlayered? */
@layer components {
  .btn {
    color: blue;
  }
}
/* unlayered */
.btn {
  color: red;
} /* wins despite same specificity */
```

### 5. Shadow DOM / iframe

1. Styles outside shadow do not pierce closed roots (except CSS variables / `::part` / `::slotted` patterns).
2. Confirm whether the element is in shadow tree — standard page CSS may never apply.

### 6. Fix strategies (preferred order)

| Strategy | When |
| --- | --- |
| Fix source order / layer placement | Architecture issue |
| Lower winning selector weight | Over-specified component |
| Raise losing selector **slightly** | Local need; keep methodology |
| `:where()` for low-spec base | Design system defaults |
| Split utilities later in cascade/layers | Utility-first systems |
| Remove inline styles | Unblock theming |
| `!important` | Last resort emergency / utilities intentional |

```css
/* Prefer */
:where(.btn) {
  padding: 0.5rem;
} /* easy to override */

/* Avoid specificity arms race */
div#app header.nav ul li a.link {
  color: red;
}
```

### 7. Verify

1. Intended state wins; other states (hover/focus) still correct.
2. No regression on sibling components sharing classes.
3. Add a regression test or Storybook story if fight was recurring.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Diagnosis | DevTools + tuple + layer note | “Add !important” first |
| Base styles | `:where` / layers | IDs everywhere |
| Utilities | Explicit layer last | Random order per import |
| Inline | Avoid for theming | style= for everything |
| Shadow | Use parts/tokens | Expect page CSS to pierce closed shadow |

## Output Checklist

- [ ] Reproduction details recorded
- [ ] Winning and losing rules identified
- [ ] Specificity tuples computed
- [ ] Layers/!important/inline checked
- [ ] Shadow/iframe considered
- [ ] Fix applied with least cascade violence
- [ ] Related states retested
- [ ] Structural follow-up ticketed if needed
- [ ] Docs note for team if pattern recurring
- [ ] Residual `!important` justified if any

## Rules

- Understand why a rule wins before increasing specificity.
- Prefer architecture (layers/methodology) over one-off hacks.
- Focus on **CSS specificity and cascade debugging**.

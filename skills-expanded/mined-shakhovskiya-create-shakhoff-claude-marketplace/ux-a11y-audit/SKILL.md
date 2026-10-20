---
name: ux-a11y-audit
description: WCAG 2.2 AA accessibility audit. Static checks (missing alt, contrast, label association, focus order) plus optional axe-core dynamic run on routes. Used by /audit:ux-a11y.
---

# ux-a11y-audit

## Static checks

| Rule | Detection | WCAG ref |
|------|-----------|----------|
| `a11y.img.alt_missing` | `<img>` без `alt` | 1.1.1 |
| `a11y.label.missing` | `<input>` без label/aria-label | 1.3.1, 4.1.2 |
| `a11y.contrast.low` | Tailwind/CSS color ratio < 4.5:1 | 1.4.3 |
| `a11y.focus.outline_none` | `outline: none` без replacement | 2.4.7 |
| `a11y.heading.skip` | h1→h3 без h2 | 1.3.1 |
| `a11y.button.empty` | `<button>` без text/aria-label | 4.1.2 |
| `a11y.link.empty` | `<a>` без accessible name | 2.4.4 |
| `a11y.role.invalid` | Non-existent role | 4.1.2 |
| `a11y.lang.missing` | `<html>` без `lang` | 3.1.1 |
| `a11y.skiplink.missing` | No skip-to-content на page-level layout | 2.4.1 |

## Dynamic (axe-core)

Iterates routes from `architecture-audit` route map. For each:
1. Spin headless browser (Playwright if MCP available, else `npx @axe-core/cli`).
2. Run axe scan.
3. Map violations to findings (one finding per violation type per route).

## Heuristic bonus

- Modal/Dialog без focus-trap: HIGH.
- Form without `aria-describedby` for errors: MEDIUM.
- Animation без `prefers-reduced-motion`: LOW.

## Severity table

| Issue | Severity |
|-------|---------:|
| Empty button/link in payment flow | CRITICAL |
| Missing label in form input | HIGH |
| Low contrast body text | HIGH |
| Missing skip-link | MEDIUM |
| Heading skip | LOW |

## Output

Findings tagged `phase: ux_a11y`. Each:
- `evidence[].kind = "file"` для статики, `"screenshot"` для dynamic axe runs.
- `recommendation` includes concrete WCAG technique reference.

---
name: web-a11y-navigation
description: Builds accessible navigation and wayfinding with landmarks, headings, skip links, breadcrumbs, nav lists, current-page state, disclosure navigation, and menu-vs-navigation decisions. Use when implementing headers, sidebars, nav bars, or complex page structure.
---

# Web A11y Navigation

## Navigation Rules

1. Use landmarks to communicate page regions.
2. Label repeated landmarks clearly and uniquely.
3. Use headings to expose information hierarchy.
4. Represent navigation lists semantically when count and structure help orientation.
5. Mark the current page or item semantically and visually.
6. Do not use ARIA menu roles for ordinary site navigation.

## Checklist

```markdown
Navigation checklist

- [ ] Main content and navigation are easy to jump to
- [ ] Skip links are available where repeated content creates friction
- [ ] Breadcrumbs use a labeled nav, list semantics, and current-item indication
- [ ] Current page state does not rely on color alone
- [ ] Disclosure navigation uses buttons for toggles and links for navigation
- [ ] Responsive navigation preserves keyboard and screen reader flow
```

## Output

Explain landmark labels, current state, skip-link strategy, keyboard behavior, and any menu/navigation trade-offs.

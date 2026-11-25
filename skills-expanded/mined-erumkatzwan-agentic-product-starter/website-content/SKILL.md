---
name: website-content
description: Use when changing the copy, sections or styling of the one-page landing website (apps/website).
---

# Website content

- One page, minimal: hero, what's inside, how it works, quality, footer.
- Plain, short sentences; one idea per card.
- Style only with tokens from `tokens.css` (`var(--color-primary)`, `var(--space-l)` …). Never hard-code colours.
- Keep it accessible: one `h1`, headings in order, descriptive link text.
- Run `npm run validate` and `npm run e2e`; update `e2e/landing.spec.ts` when sections change.

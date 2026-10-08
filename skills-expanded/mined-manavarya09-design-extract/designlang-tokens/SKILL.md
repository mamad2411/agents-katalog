---
name: designlang-tokens
description: Use when styling UI for webflow.com — references the extracted design system tokens instead of inventing colors, spacing, or typography.
---

# designlang tokens
Source: https://webflow.com
Extracted by designlang v7.0.0 on 2026-06-25T08:28:55.721Z

## Semantic tokens (use these)
- color.action.primary: #146ef5
- color.surface.default: #ffffff
- color.text.body: #000000
- radius.control: 2px
- typography.body.fontFamily: WF Visual Sans Variable

## Regions
- sidebar
- nav
- nav
- nav
- nav
- nav
- nav
- nav
- nav
- pricing
- sidebar
- nav
- content
- content
- testimonials
- content
- content
- content
- nav
- pricing
- footer
- nav

## How to use
- Prefer `semantic.*` tokens over `primitive.*`.
- Never invent new tokens or hex values; reuse the ones above.
- When a value is missing, pick the closest existing semantic token and flag the gap.
- Reference tokens by their dotted path (e.g. `semantic.color.action.primary`).

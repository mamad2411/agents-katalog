---
name: salkarsaui
description: Use when building, changing or reviewing UI in a web app that uses the SalkarsaUI design system, or when the user mentions SalkarsaUI, Salkarsa tokens, or asks for screens, pages or components with Next.js or React, Tailwind CSS v4 and shadcn/ui that should follow a mobile-first design system with light and dark themes.
---

# SalkarsaUI

SalkarsaUI is a mobile-first design system for the web. Every color, space, radius and font comes from a token, and every component maps to a shadcn/ui component restyled with those tokens.

All exact values and component specs live in `DESIGN.md` next to this file. This file only tells you how to work. When the two seem to disagree, `DESIGN.md` wins.

| File | What it holds |
|---|---|
| `DESIGN.md` | The full guide. Read sections 0, 2, 3 and 4 before writing UI. Section 5 has page patterns and copy rules. |
| `tokens/tokens.css` | All tokens as CSS variables, light and dark, plus the `.text-*` type classes |
| `tokens/shadcn.css` | Points the shadcn/ui and Tailwind v4 variables at SalkarsaUI tokens |
| `tokens/tokens.json` | The same tokens in DTCG format. Each has a `$description` that says when to use it. |

## 1. Check the project setup

Open the project's global stylesheet (usually `app/globals.css` or `src/app/globals.css`).

- If it already imports `tokens.css` and `shadcn.css`, go to step 2.
- If not, copy `tokens/tokens.css` and `tokens/shadcn.css` from this skill next to `globals.css`, then follow the setup in DESIGN.md section 1.

Never edit the token files. They are generated from Figma.

## 2. Build

1. Find the component in DESIGN.md section 4. Add the mapped shadcn component with `npx shadcn@latest add <name>`, then set its variants and sizes to the values in that table.
2. Style only with shadcn aliases, semantic tokens and the spacing steps in DESIGN.md section 2.2. No hex or rgb values, no arbitrary values like `p-[13px]`, no palette classes like `bg-blue-500`, no primitive tokens like `--color-*`.
3. Write mobile-first: base styles for mobile, then `md:` and `lg:`. Swap components at the breakpoints in DESIGN.md section 2.3.
4. Give every interactive element the states in DESIGN.md section 3.1.
5. Switch dark mode with `data-theme="dark"` or `.dark` on `<html>`. Never pick colors in JavaScript.
6. Write UI copy as described in DESIGN.md section 5, unless the user's project says otherwise.

## 3. When something is missing

- No fitting token: pick the most semantic one and check its `$description` in `tokens/tokens.json`. If nothing fits, ask the user instead of inventing a value.
- No matching component: compose it from DESIGN.md section 4 or restyle the shadcn default with tokens, and write "candidate component: <name>" in your reply.
- Never build the Status bar or Home indicator. They exist in Figma for mockups only.

## 4. Before you finish

- [ ] This search finds nothing in UI code (token files excluded):
  `grep -rnE "#[0-9a-fA-F]{3,8}\b|\[[0-9]+px\]|(bg|text|border)-(gray|slate|zinc|blue|red|green|yellow)-[0-9]" src app components`
- [ ] The layout works at 375px, 768px and 1280px
- [ ] It works in light and dark
- [ ] Focus is visible, and icon-only buttons have an `aria-label`
- [ ] The active nav item has `aria-current="page"`

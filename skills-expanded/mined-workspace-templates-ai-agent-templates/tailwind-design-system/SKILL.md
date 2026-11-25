---
name: tailwind-design-system
description: Sets up Tailwind theme tokens, component classes and typed variants so a UI stays consistent without piles of repeated utility strings.
---

# Tailwind design system

Make the design decisions explicit, then make the code follow them.

## Steps

1. Audit first. Search the markup for arbitrary values (`bg-[#1a2b3c]`, `w-[13px]`) and list the most used raw colors, font sizes and radii. Show the counts before changing anything.
2. Define tokens in the theme, not in components. Tailwind v4: `@theme { --color-brand-500: ...; --radius-card: ...; }` in the main CSS file. v3: `theme.extend` in the config. Name tokens by role (`surface`, `text-muted`, `brand`), not by value (`blue-dark`).
3. Support dark mode through semantic variables that switch under `.dark` or `prefers-color-scheme`, so components never write `dark:` pairs for ordinary colors.
4. Extract a component only when a pattern appears three or more times. Prefer a framework component (React, Vue, Svelte) over `@apply`.
5. Build variants with a typed helper such as `cva` (class-variance-authority) and merge overrides with `tailwind-merge`. Variants are named by intent: `intent: primary | quiet | danger`, `size: sm | md`.
6. Replace the raw values you found in step 1 with tokens, one file group at a time.

## Rules

- No new arbitrary values without a comment saying why a token does not fit.
- Never build class names by string concatenation: Tailwind cannot see a class that only exists at runtime. Map each option to a full class string.
- Keep focus rings and contrast intact: body text at least 4.5:1.

## Report

Tokens added, components extracted, raw values removed (before and after counts).

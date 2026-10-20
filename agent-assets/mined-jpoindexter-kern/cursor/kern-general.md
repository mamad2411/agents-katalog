---
description: General project rules and conventions
globs: **/*
---

# Project Rules

Stack: Next.js 16.1.6 + TypeScript + Tailwind CSS

## Rules

- Use semantic design tokens (bg-primary, text-foreground). Never hardcode colors.
- Type all parameters. Avoid `any`.
- Use Tailwind scale values. No arbitrary values like `w-[137px]`.
- Default to Server Components. Add `'use client'` only for interactivity.

## Commands

- `pnpm dev` — Development server
- `pnpm build` — Production build
- `pnpm test` — Run tests
- `pnpm lint` — Lint code

## Detected Patterns

- Testing: Vitest

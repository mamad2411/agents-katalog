---
name: verify-nextjs-shadcn
description: "ShadCN-specific Next.js verification checklist — components.json, cn(), next-themes."
disable-model-invocation: true
---

# Skill: Verify Next.js (ShadCN)

## Purpose
ShadCN-specific checklist for a Next.js + ShadCN UI project. Run alongside `verify-nextjs.md` (general concerns) — this file only covers what ShadCN adds. ShadCN is Tailwind-based, so also run the **Tailwind v4** section of `verify-nextjs.md`.

## Verification Process

Flag each as PASS, WARN, or FAIL.

### 1. Configuration
- [ ] `components.json` exists and its aliases are correct — notably `"ui": "@/components/ui"` — so the CLI installs components to the right place
- [ ] `cn()` exists in `lib/utils.ts` as `twMerge(clsx(...))`

### 2. Components & className
- [ ] ShadCN components are imported from `@/components/ui/<component>`, not relative paths or a barrel
- [ ] Conditional/merged classNames go through `cn()` — never string concatenation or template literals for class merging (so conflicting Tailwind classes resolve correctly)

### 3. Theming (next-themes)
- [ ] `ThemeProvider` from `next-themes` wraps the app with `attribute="class"` and `disableTransitionOnChange`
- [ ] Dark mode is driven by the `.dark` class (Tailwind v4 `@custom-variant dark`), not a separate stylesheet

## Output
Produce a `verification-report.md` (same format as verify-django), adding a "ShadCN" section.

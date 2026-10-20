---
name: follow-lib-zaidan-ui
description: Use Zaidan UI for SolidJS components with Kobalte, Corvu, and Tailwind CSS
argument-hint: "[scope]"
related:
  - follow-lib-animejs
  - follow-lib-arktype
  - follow-lib-better-auth
  - follow-lib-shadcn-solid
  - follow-lib-unocss
  - follow-best-practice
  - use-my-packages-on-registry
  - setup-cicd

---

## Goal

Use Zaidan UI for UI components on SolidJS with accessible, customizable components built with Kobalte, Corvu, and Tailwind CSS

## Scope

Use for creating UI components with the Zaidan registry on SolidJS for Vite, SolidStart, TanStack Start, Astro

- Use when the project needs components from the Zaidan registry (`@zaidan/*`) via the `shadcn` CLI + Tailwind CSS v4
- If the project uses the `shadcn-solid` CLI or needs UnoCSS styling, use `/follow-lib-shadcn-solid` instead

- Latest: `shadcn@4.21.0` / `@kobalte/core@0.13.14` / `corvu@0.7.2` / `solid-js@1.9.15` / `tailwindcss@4.3.3` (verified 2026-09-16)

## Execute

### 1. Install And Setup

> Goal: install Zaidan UI for SolidJS

1. Pick the framework and create the project:
   - Vite: `pnpm create vite@latest --template solid-ts`
   - SolidStart: `pnpm create solid@latest --solidstart --ts --template with-tailwindcss`
   - TanStack Start: `pnpm dlx shadcn@latest init -t start`
   - Astro: `bun create astro@latest --template with-tailwind --add solid --git`
2. Install Tailwind CSS v4 (`tailwindcss` and `@tailwindcss/vite`) per the framework
3. Set up the `@/` path alias in `tsconfig.json` and the Vite config
4. Run `bunx shadcn@latest init` to create `components.json`
5. Read additional guidance at 

### 2. Configure Registry

> Goal: configure the Zaidan registry in components.json

1. Set `style` to `kobalte` and `rsc` to `false`
2. Add `registries` to `components.json`:
   ```json
   "registries": {
     "@zaidan": "https://zaidan.carere.dev/r/{style}/{name}.json"
   }
   ```
3. Set `tailwind.css` to `src/styles/globals.css` (or the path the project uses)
4. Set `aliases` to match the project (`@/components`, `@/lib/utils`, `@/lib`, `@/hooks`)
5. See the full example in 

### 3. Add Components

> Goal: add Zaidan components with the shadcn CLI

1. Use `bunx shadcn@latest add @zaidan/button` to add a single component
2. Use `bunx shadcn@latest add @zaidan/card @zaidan/dialog` to add multiple components
3. Components are copied to `src/components/ui/`
4. Import with `import { Button } from "@/components/ui/button"`
5. For Better Auth UI use `bunx shadcn@latest add https://better-auth-ui.com/r/solid/auth.json`

### 4. Learn Key Concepts

> Goal: understand Zaidan's core concepts

1. Zaidan is a shadcn registry for SolidJS, not an npm package
2. Components are built on Kobalte and Corvu primitives
3. Styled with Tailwind CSS v4
4. Supports copy-paste or pulling via the shadcn CLI
5. Has components, blocks, charts, and typeset
6. See details in 

### 5. Customize And Apply Best Practices

> Goal: customize components per best practices

1. Customize the components copied into `src/components/ui/`
2. Adjust CSS variables in `src/styles/globals.css`
3. Use the `cn` helper for merging Tailwind classes
4. Always use accessible components
5. Use dark mode via `data-kb-theme` or the scheme the project defines

### 6. Integrate With SolidJS

> Goal: integrate with SolidJS

1. Use the components with Vite, SolidStart, TanStack Start, or Astro
2. Configure the Tailwind CSS v4 plugin in the Vite config
3. Use the `@/components/ui/*` import alias per `components.json`
4. Read the official docs at https://zaidan.carere.dev/docs

### 7. Troubleshoot

> Goal: fix common problems

1. Check that `components.json` `registries` points to the Zaidan registry correctly
2. Check that `style` is `kobalte` and `rsc` is `false`
3. Check the `@/` path alias in `tsconfig.json` and the Vite/SolidStart config
4. Read the FAQ at https://zaidan.carere.dev/docs/faq

### Workflows

- Setup theme — registry config, Tailwind v4 variables, dark mode → `workflows/setup-theme/SKILL.md`
- Tune theme tokens — colors, radius, Tailwind v4 mapping → `workflows/config-tokens/SKILL.md`

## Rules

- Use the `bunx shadcn@latest` CLI, not `shadcn-solid`
- Use the `@zaidan/<component>` registry for adding components
- Always use the copy-to-own pattern
- Use Kobalte and Corvu for accessible primitives
- Use Tailwind CSS v4 for styling
- Use backticks for commands, components
- Use code blocks for component examples
- Always use accessible components
- Customize components as needed
- Avoid modifying core Kobalte/Corvu primitives

- Use `/follow-lib-animejs` if needed
- Use `/follow-lib-arktype` if needed
- Use `/follow-lib-better-auth` if needed
- Use `/follow-lib-shadcn-solid` if needed
- Use `/follow-lib-unocss` if needed
- Use `/follow-best-practice` if needed
- Use `/use-my-packages-on-registry` if needed
- Use `/setup-cicd` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- UI components that are accessible and customizable
- Code that is copy-to-own and maintainable
- Smooth integration with SolidJS
- Components that follow accessibility best practices

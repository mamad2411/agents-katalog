---
name: follow-lib-shadcn-solid
description: shadcn/ui port for SolidJS - accessible, customizable copy-paste components
argument-hint: "[scope]"
related:
  - follow-create-web
  - follow-lib-animejs
  - follow-lib-unocss
  - follow-lib-zaidan-ui
  - follow-best-practice
  - use-my-packages-on-registry
  - setup-cicd

---

## Goal

Use shadcn/ui for SolidJS component library with the copy-to-own pattern and accessible components

## Scope

Used for building UI components with shadcn-solid on SolidJS for SolidStart, Astro, Vite

- Use when the project needs the `shadcn-solid` CLI + its own registry (supports Tailwind CSS and UnoCSS)
- If the project uses the Zaidan registry (`@zaidan/*` via the `shadcn` CLI, Kobalte/Corvu + Tailwind v4), use `/follow-lib-zaidan-ui` instead

- Latest: `shadcn-solid@0.7.7` (CLI) (verified 2026-09-13)

## Execute

### 1. Install And Setup

> Goal: install shadcn/ui for SolidJS

1. Create the SolidJS project with `pnpm create solid@latest` and pick the tailwind or uno template
2. Install the shadcn-solid CLI via `bunx shadcn-solid@latest init` (or `pnpm dlx shadcn-solid@latest init`)
3. Choose the CSS framework `TailwindCSS` or `UnoCSS` per the CLI prompts
4. Configure `components.json` with base color, global CSS file, import alias (`@/components`), utils alias (`@/lib/utils`)
5. Read additional guidance at 

### 2. Add Components

> Goal: add components with the CLI

1. Use `bunx shadcn-solid@latest add [component]` to add a single component
2. Use `bunx shadcn-solid@latest add button card dialog` for multiple components
3. Use `bunx shadcn-solid@latest add --all` to install everything
4. Use `bunx shadcn-solid@latest add [component] --overwrite` to overwrite existing files
5. Use `bunx shadcn-solid@latest diff` to check upstream updates

### 3. Learn Key Concepts

> Goal: understand shadcn-solid's core concepts

1. shadcn-solid is an unofficial community-led port of shadcn/ui for SolidJS
2. Components are copy-to-own source code in `src/components/ui/`
3. Built on Kobalte UI primitives for accessibility
4. Supports Tailwind CSS and UnoCSS
5. No component library installed as a dependency
6. See more details in 

### 4. Configure Styles

> Goal: configure styles and theme

1. Configure Tailwind CSS or UnoCSS per the chosen template
2. Use CSS variables for colors, radius, and theme tokens
3. Use the `cn` helper built from `clsx` and `tailwind-merge`
4. Configure dark mode via the `data-kb-theme="dark"` attribute
5. Use utility classes from the design system, don't hard-code colors

### 5. Customize Components

> Goal: customize components as needed

1. Customize the components copied into `src/components/ui/` directly
2. Use `cva` (class-variance-authority) for type-safe variants
3. Adjust CSS variables in the global CSS file
4. Use the UnoCSS theme per `/follow-lib-unocss` if UnoCSS was chosen
5. Avoid editing the shadcn-solid CLI source or Kobalte primitives directly

### 6. Integrate With SolidJS

> Goal: integrate with the SolidJS ecosystem

1. Configure the path alias `@/` in `tsconfig.json` and the Vite config
2. Use the components in SolidStart, Astro, or Vite projects
3. Use `@solidjs/meta` and `@solidjs/router` for meta and routing if needed
4. Read the official docs at https://shadcn-solid.com/docs

### 7. Troubleshoot

> Goal: fix common problems

1. Check `components.json` and path aliases if imports are wrong
2. Use `bunx shadcn-solid@latest diff <component>` to see upstream changes
3. Read the troubleshooting guide at https://shadcn-solid.com/docs

### Workflows

- Setup theme — `components.json`, CSS variables, dark mode → `workflows/setup-theme/SKILL.md`
- Adjust theme tokens, `cva` variants → `workflows/config-tokens/SKILL.md`

## Rules

- Use the CLI `bunx shadcn-solid@latest init` for initial setup
- Always use the copy-to-own pattern
- Use Kobalte UI primitives
- Use Tailwind CSS or UnoCSS for styling
- Use backticks for commands, components
- Use code blocks for component examples
- Always use accessible components
- Customize components in your own project
- Avoid editing core Kobalte primitives directly
- Use `diff` to check upstream updates

- Use `/follow-solid-framework` if needed
- Use `/follow-lib-animejs` if needed
- Use `/follow-lib-unocss` if needed
- Use `/follow-lib-zaidan-ui` if needed
- Use `/follow-best-practice` if needed
- Use `/use-my-packages-on-registry` if needed
- Use `/setup-cicd` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Accessible and customizable UI components
- Copy-to-own, maintainable code
- Smooth integration with SolidJS
- Components that follow accessibility best practices

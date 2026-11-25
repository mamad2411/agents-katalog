---
name: kumo-cli
description: Guide to the Kumo UI CLI (npx @cloudflare/kumo) — listing components, querying component docs and props from the terminal, and scaffolding customizable "Blocks" into a project's source directory. Use whenever the user is setting up Kumo UI in a React project, asks how to install or run the Kumo CLI, wants to add a Block like PageHeader or DeleteResource, needs Kumo's semantic color token / Tailwind v4 / ESM conventions, or mentions "npx @cloudflare/kumo" by name.
---

# Kumo UI CLI

Kumo is Cloudflare's accessible, design-system-compliant component library for building modern React web applications. It combines Base UI primitives with semantic color tokens adapting to light and dark mode using Tailwind CSS v4.

The CLI provides tools to query component documentation directly from the terminal and scaffold customizable "Blocks" directly into a project's source directory.

## Prerequisites

Before using Kumo in a project, ensure the required peer dependencies are installed:

```bash
pnpm add react react-dom @phosphor-icons/react
```

Installation of the main library:

```bash
pnpm add @cloudflare/kumo
```

## Available CLI commands

The CLI is invoked using `npx @cloudflare/kumo <command>`.

**1. List components** — outputs a complete list of all available UI components in the Kumo library.
```bash
npx @cloudflare/kumo ls
```

**2. View component documentation** — query detailed documentation, props, and usage examples for a specific component right from the command line.
```bash
npx @cloudflare/kumo doc ComponentName
# Example: npx @cloudflare/kumo doc Button
```

**3. View all documentation** — fetch and print the documentation for all components.
```bash
npx @cloudflare/kumo docs
```

**4. Add/scaffold blocks** — adds customizable blocks (e.g., `PageHeader`, `DeleteResource`) directly into the local source directory (by default into a folder like `src/components/kumo/`).
```bash
npx @cloudflare/kumo add BlockName
# Example: npx @cloudflare/kumo add PageHeader
```
Blocks usually depend on standard Kumo components — the CLI will warn if you attempt to add a block without `@cloudflare/kumo` installed.

## Usage guidelines & conventions

When operating within a codebase that uses Kumo UI, follow these conventions:

**Components vs. Blocks.** Components (`Button`, `Input`, `Dialog`, etc.) are imported directly from the package: `import { Button } from '@cloudflare/kumo';`. Blocks are larger, complex UI patterns that are *not* exported from the package index — they must be installed via the `kumo add` command so the raw code can be edited locally.

**Styling & theming.** Always use Kumo's semantic color tokens (`kumo-*`, e.g. `bg-kumo-base`, `bg-kumo-elevated`) — never raw Tailwind colors (like `bg-blue-500`) or raw dark variants (`dark:bg-black`), since those bypass Kumo's light/dark adaptation. Mode switching is handled exclusively via data attributes on parent elements: `data-mode="light"` or `data-mode="dark"`. Compose class names using the provided utility: `import { cn } from '@cloudflare/kumo';`.

**Tailwind v4 configuration.** Tailwind CSS v4 does not scan `node_modules` by default. To ensure Kumo components render correctly (e.g., dialogs centering properly), the project's main CSS file needs a source directive pointing to the Kumo package:
```css
@source "../node_modules/@cloudflare/kumo/dist/**/*";
```

**ESM only.** Kumo is exclusively an ESM library (`"type": "module"`). Avoid CommonJS (`require()`) imports when working with Kumo configurations or extending components.

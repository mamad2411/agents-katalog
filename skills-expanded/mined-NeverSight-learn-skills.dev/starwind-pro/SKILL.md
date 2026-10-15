---
name: starwind-pro
description: Discover, install, and adapt Starwind Pro blocks in Astro projects. Use when Codex needs to search Pro blocks, explain Pro setup, distinguish free and paid availability, install exact Pro block commands returned by current tools, or avoid assuming license access.
user-invocable: false
allowed-tools: Bash(npx starwind@latest *), Bash(pnpx starwind@latest *), Bash(pnpm dlx starwind@latest *), Bash(yarn dlx starwind@latest *)
---

# Starwind Pro

## Start Here

Use this skill when the user wants production-ready Starwind Pro blocks, Pro setup help, or a free/pro block recommendation for an Astro project.

Starwind Pro builds on Starwind UI. Blocks are native `.astro` components styled with Tailwind CSS v4, installed into the user's codebase, and customized directly.

## Core Rules

- Starwind Pro is for Astro projects. Confirm the project is Astro before setup or install work.
- Pro setup requires Starwind UI configuration. If it is missing, initialize with Pro support.
- Use current metadata before naming a block. Prefer the Starwind MCP `search_starwind_pro_blocks` tool when available.
- Use the exact install command returned by the MCP, CLI, or block page. Do not invent slugs, dependencies, plans, or private URLs.
- Distinguish free and premium blocks. Free blocks do not require a paid license; premium blocks require Starwind Pro access.
- Never expose, hardcode, or ask the user to paste a license key into source files.

## Required Context

Before recommending or installing a block, check:

1. `package.json`, `astro.config.*`, and project layout to confirm this is an Astro app.
2. `components.json`, `src/styles/starwind.css`, and local components to confirm Starwind UI and Pro setup.
3. `.gitignore` for `.env.local` if license setup is involved.
4. The target page/layout and import aliases before wiring a block into the app.

## Common Workflows

### Setup

- New project or missing Starwind UI: use `npx starwind@latest init --pro`.
- Existing Starwind project: use `npx starwind@latest setup`.
- For package-manager-specific commands, use the Starwind MCP result or the CLI `--package-manager` option instead of guessing.
- pnpm projects may need the `.npmrc` settings from `setup.md`.

### Find And Install Blocks

1. Search by intent, category, or plan, such as hero, pricing, authentication, FAQ, navigation, footer, feature, testimonial, contact, or theme-switcher.
2. Use the returned `installCommand` as written, or use `starwind_add` to generate the validated command. Pro commands can include Starwind UI component dependencies such as `button` or `aspect-ratio`.
3. After installation, read the added files before using them.
4. Wire the block into the requested route using the project's aliases and layout conventions.
5. Replace placeholder copy, links, images, and data while preserving Astro syntax and Starwind imports.

## Design And Customization

- Pro blocks use the same Starwind UI theme variables and `dark:` class strategy. Prefer theme variables and focused class changes over broad rewrites.
- Keep container-query, responsive, animation, and dark-mode behavior intact unless the user asks to change it.
- If adding scroll-entry animation, prefer the documented `motion-on-scroll` approach for Astro pages.
- Keep edits local to installed blocks or their data/config unless a shared theme change is intended.

## Detailed References

- Setup, license, registry, and troubleshooting: `setup.md`
- Block search, install commands, and adaptation: `blocks.md`

Load only the reference needed for the current task.

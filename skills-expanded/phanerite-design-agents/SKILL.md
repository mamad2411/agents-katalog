# Repository Guidelines

## Project Structure & Module Organization

A SvelteKit 2 launcher UI prototype using Svelte 5, TypeScript, and Tailwind CSS.

- `src/routes/` contains application routes, root page, layout, and global stylesheet.
- `src/lib/components/app/` contains launcher-specific views and dialogs. Place feature UI here.
- `src/lib/components/ui/` contains shadcn-svelte primitives. Prefer composing these rather than modifying generated primitives unless the change applies to every consumer.
- `src/lib/types.ts`, `seed.ts`, and `state.svelte.ts` define shared domain types, preview data, and global prototype state.
- `src/lib/assets/` holds source assets; `static/` holds files served unchanged.

Use `$lib` aliases, e.g. `import { app } from "$lib/state.svelte";`.

## Build, Check, and Development Commands

Use Deno for dependency resolution and commands. This project uses `package.json`
through Deno's npm compatibility layer; `deno.lock` is the authoritative lockfile.
Use the existing package scripts through `deno task`; do not add an npm, pnpm, or
Bun lockfile.

```sh
deno task dev       # start the Vite development server
deno task check     # sync SvelteKit types and run svelte-check
deno task build     # produce a production build
deno task preview   # serve the production build locally
```

There is no automated test suite yet. At minimum, run `deno task check` after
every change, and run `deno task build` for route, configuration, or
production-impacting changes.

## Coding Style & Naming Conventions

Write strict TypeScript and Svelte 5 runes, as configured in `vite.config.ts`. Follow the existing two-space indentation, double quotes, semicolons, and trailing commas where already used. Format Svelte and TypeScript with the repository's `oxfmt` configuration before committing.

Name Svelte components in `PascalCase` (`LaunchDialog.svelte`), TypeScript modules in descriptive lowercase names (`state.svelte.ts`), functions and variables in `camelCase`, and types/interfaces in `PascalCase`. Keep shared types in `types.ts`; model state changes as methods on `AppState` instead of mutating it from arbitrary components.

## UI and State Practices

Keep launcher preview data in `seed.ts` and state transitions in `state.svelte.ts`. Preserve the separation between app-specific components and reusable UI primitives. Use Tailwind utilities and the CSS variables defined in `src/routes/layout.css`; do not introduce one-off hard-coded colors when a theme token exists. Phanerite supports Vanilla, Fabric, Forge, and NeoForge only. Treat Forge and NeoForge as distinct loaders, do not add Quilt.

## Commits and Pull Requests

Recent history uses short, imperative summaries such as `Update dependencies` and `Remove the direct use of RawDownloader`. Keep commits focused and concise.

Pull requests should explain the user-visible change, note validation run, link related issues, and include screenshots or a short recording for UI changes. Do not commit generated directories such as `.svelte-kit/`, `build/`, or `node_modules/`.

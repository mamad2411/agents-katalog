---
name: follow-create-web-svelte
description: Set up Vite + Svelte 5 Runes + TypeScript (client-side only)
argument-hint: "[scope]"
related:
  - follow-lib-unocss
  - refactor
  - run-dev

---

## Goal

Set up and develop a Svelte 5 project with Runes, Vite, and TypeScript (client-side only)

## Scope

For Svelte 5 projects that use Vite as the build tool (client-side only)
Note: if you need a fullstack meta-framework, use SvelteKit mode (Step 8) — SSR/CSR/prerendering + file-based routing in `src/routes/`

- Packages: `svelte` 5.x (runes, Node >= 18), `@sveltejs/kit` 2.x, `@sveltejs/vite-plugin-svelte`, `sv` CLI (`bunx sv create`, `sv check`, `sv migrate svelte-5`) — always verify the latest versions with `/deep-research` + `/follow-best-practice` (no pinning in this file — per `/update-devin-global-skills`)

## Execute

### 1. Setup Project

> Goal: Setup Project

1. Create `vite.config.ts` with `@sveltejs/vite-plugin-svelte`
2. Create `svelte.config.js` with `vitePreprocess` and `runes: true`
3. Set up `tsconfig.json` with `moduleResolution: bundler`
4. Add scripts to `package.json` (dev, build, preview)
5. Configure the server port and build options
6. Use the latest Svelte 5.x — verify the version with `/deep-research` + `/follow-best-practice` before setup

### 2. Configure TypeScript

> Goal: Configure TypeScript

1. Set `target: ES2022` and `module: ESNext`
2. Use `moduleResolution: bundler`
3. Configure `paths` for import aliases — never use `baseUrl` (removed in TypeScript 7; use relative `"./..."` in `paths` instead)
4. Enable `strict: true`
5. Support TypeScript 6.0 (svelte-check 4.7.6+, svelte2tsx 0.7.61+) — pin `typescript@6` until TS 7.1 (svelte-check uses a compiler API not yet stable in 7.0)

### 3. Svelte 5 Runes

> Goal: Svelte 5 Runes

Use Runes correctly for reactivity

1. Use `$state()` for reactive state (deeply reactive by default)
2. Use `$derived()` for computed values (lazy evaluation)
3. Use `$effect()` for side effects only (DOM, network, analytics)
4. Use `$props()` for component props with destructuring
5. Use `$bindable()` for bindable props
6. Use `$state` in plain `.ts` files instead of Svelte stores
7. Never use `$effect` to sync state; use `$derived` instead
8. Use `$effect.pre` for effects that must run before DOM updates

### 4. Snippets And Components

> Goal: Snippets And Components

Use Snippets instead of Slots

1. Use `{#snippet name()}` for reusable markup
2. Use `{@render children()}` to render snippet content
3. Use snippets instead of Svelte 4 slots
4. Use `mount(Component, props)` instead of `new Component()`
5. Declarations in markup are allowed (Svelte 5.56+)

### 5. Setup Styling

> Goal: Setup Styling

1. Run `/follow-lib-unocss` for styling
2. Use UnoCSS throughout where possible
3. Avoid scoped styles

### 6. State Management Patterns

> Goal: State Management Patterns

1. Use `$state` in classes for reusable business logic
2. Group related state into cohesive objects (granular reactivity)
3. Use Svelte stores (`writable`, `readable`, `derived`) for RxJS-style subscriptions
4. Stores are still supported and not deprecated, but runes are the default
5. Use `$state.snapshot()` to get an immutable snapshot

### 7. Event Handling

> Goal: Event Handling

1. Use `onclick` instead of `on:click` (Svelte 5 syntax)
2. Event handlers are properties like any other attribute
3. Use event attributes for DOM elements

### 8. SvelteKit Mode (Optional Fullstack)

> Goal: fullstack SvelteKit when client-side alone isn't enough

1. Scaffold with `bunx sv create <project>` (`--types ts`, `--add-ons`, `--no-install`; `create-svelte` is deprecated) — `sv sync`/`sv prepare` generate types, `sv check` verifies, `sv migrate svelte-5` handles auto-migration
2. File-based routing in `src/routes/` — `+page.svelte`, `+layout.svelte`, `+page.ts`/`+page.server.ts` (`load`), `+server.ts` (API routes), `+error.svelte`
3. Data loading: `export const load: PageLoad | PageServerLoad` in `+page.ts`/`+layout.ts`; form mutations with `export const actions` in `+page.server.ts`
4. Runtime modules: `$app/state` (`page`, `navigating`, `updated` — Svelte 5; `$app/stores` for Svelte 4 compat), `$app/navigation` (`goto`, `invalidate`, `invalidateAll`, `preloadData`), `$app/forms` (`enhance`, `applyAction`), `@sveltejs/kit` exports (`error`, `redirect`, `fail`, `json`)
5. Rendering: SSR by default — disable with `export const ssr = false` or prerender with `export const prerender = true` per route
6. Progressive enhancement: form actions work without JS (use `use:enhance` for enhancement)

## Rules

### 1. Configuration

Set up the project to Svelte 5 standards:

- Use `@sveltejs/vite-plugin-svelte` for Svelte transformation
- Use `vitePreprocess` for TypeScript preprocessing
- Set `runes: true` for Svelte 5 Runes
- Set `moduleResolution: bundler` in TypeScript
- Support TypeScript 6.0

### 2. Runes Best Practices

Use Runes correctly:

- `$state` for reactive values (explicit, opt-in)
- `$derived` for computed values (lazy, composable)
- `$effect` for side effects only (it's an escape hatch)
- Never use `$effect` to sync state; use `$derived` instead
- `$props` for component props with destructuring
- Use `$state` in `.ts` files instead of stores where possible

### 3. Component Development

Develop components following best practices:

- Use `.svelte` with `lang="ts"` for all components
- Use `$props()` for typed props
- Use snippets instead of slots
- Use `onclick` instead of `on:click`
- Use `mount()` instead of `new Component()`
- Use UnoCSS for styling

### 4. Migration From Svelte 4

Migrating from Svelte 4:

- `let count = 0` → `let count = $state(0)`
- `$: doubled = count * 2` → `let doubled = $derived(count * 2)`
- `$: { console.log(count) }` → `$effect(() => { console.log(count) })`
- `export let prop` → `let { prop } = $props()`
- `on:click` → `onclick`
- Slots → Snippets (`{#snippet}` and `{@render}`)
- Use `npx sv migrate svelte-5` for auto migration
- Old and new syntax can be mixed during migration

### 5. Code Quality

Maintain code quality:

- Use TypeScript strict mode
- Set up path aliases correctly
- Use svelte-check for type checking
- Always run `/refactor` while developing
- Use /run-dev if needed

## File Structure

Canonical file structure + layer table: [templates/file-structure-web-svelte.md](templates/file-structure-web-svelte.md)

## Expected Outcome

- A fully configured Svelte 5 project with Vite and Runes
- Reactivity using `$state`, `$derived`, and `$effect` correctly
- Snippets instead of slots for reusable markup
- Correct TypeScript configuration
- Successful UnoCSS integration
- Component development following Svelte 5 best practices

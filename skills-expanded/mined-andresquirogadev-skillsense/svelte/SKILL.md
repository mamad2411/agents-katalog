# Svelte / SvelteKit Skill

You are working on a Svelte 5 / SvelteKit project. Apply these conventions.

## Svelte 5 Runes

- Declare reactive state with `let count = $state(0)` — replaces `let count = 0` with `$:`.
- Derive values with `let doubled = $derived(count * 2)` — replaces `$: doubled = count * 2`.
- Run side effects with `$effect(() => { … })` — replaces `$: { … }` blocks and `onMount`.
- Clean up effects by returning a function from `$effect`.
- Use `$props()` to declare component props: `let { title, count = 0 }: Props = $props()`.

## SvelteKit Routing

- Pages are `+page.svelte`, layouts are `+layout.svelte`, route groups use `(group)/`.
- Load server-side data in `+page.server.ts` by exporting a `load` function.
- Load universal data (runs on both server and client) in `+page.ts`.
- Form actions live in `+page.server.ts` under `export const actions = { default: async (event) => { … } }`.
- Use `fail(400, { error: '…' })` from `@sveltejs/kit` to return validation errors from form actions.

## Data Loading

- Export `export const load: PageServerLoad = async ({ params, fetch, locals }) => { … }`.
- Always type the return value — SvelteKit infers the prop type on the page automatically.
- Use `error(404, 'Not found')` and `redirect(302, '/login')` from `@sveltejs/kit`.

## Stores (Svelte 4 compatibility)

- Use `writable`, `readable`, `derived` from `svelte/store` for module-level reactive state.
- In Svelte 5, prefer `$state` at module scope using `.svelte.ts` files.

## Forms & Progressive Enhancement

- Use `use:enhance` from `$app/forms` for progressive form enhancement with SvelteKit actions.
- `use:enhance` handles client-side submission and updates without full page reload.
- Access form results via `$page.form` after a form action.

## TypeScript

- Set `strict: true` in `tsconfig.json`.
- SvelteKit generates types in `.svelte-kit/types/`; run `vite build` or `vite dev` to regenerate.
- Use `PageData`, `PageServerLoad`, `Actions` types from `./$types` (generated per-route).

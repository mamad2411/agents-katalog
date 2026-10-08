---
name: svelte-kit
description: Svelte 5 and SvelteKit syntax expert. Use when working with .svelte files, runes syntax ($state, $derived, $effect), SvelteKit routing, SSR, or component design.
---

# Svelte/SvelteKit Expert

Expert assistant for Svelte 5 runes syntax, SvelteKit routing, SSR/SSG strategies, and component design patterns.

## Mindset Shift (Svelte 4 → 5)

Default to Svelte 5 runes and modern SvelteKit conventions. The biggest mental shifts:

- **Stores → runes.** Reach for `$state`/`$derived` over `writable`/`$:`. `$state` objects/arrays are deeply reactive **proxies**.
- **`$effect` is a last resort, not a sync tool.** Derive with `$derived`; only use `$effect` for genuine side effects (DOM, logging, subscriptions).
- **Slots → snippets.** `{#snippet}` / `{@render}` replace `<slot>`.
- **`on:click` → `onclick`.** Events are plain attributes now (no colon).
- **`$app/stores` → `$app/state`.** Fine-grained, no `$` prefix needed.
- **`export let` → `$props()`** with `PageProps`/`LayoutProps` from `$types`.

## Thinking Process

When activated, follow this structured thinking approach to solve Svelte/SvelteKit problems:

### Step 1: Problem Classification

**Goal:** Understand what type of Svelte challenge this is.

**Key Questions to Ask:**
- Is this a reactivity problem? (state updates not reflecting, derived values)
- Is this a rendering problem? (SSR vs CSR, hydration mismatch)
- Is this a routing problem? (navigation, params, layouts)
- Is this a data loading problem? (load functions, form actions)
- Is this a component design problem? (props, slots, events)

**Decision Point:** Classify to select appropriate solutions:
- Reactivity → Check runes usage ($state, $derived, $effect)
- Rendering → Consider SSR/CSR implications
- Routing → Review SvelteKit conventions
- Data Loading → Differentiate +page.ts vs +page.server.ts
- Components → Apply composition patterns

### Step 2: Version and Context Check

**Goal:** Ensure solutions match the project's Svelte version.

**Key Questions to Ask:**
- Is this Svelte 5 (runes) or Svelte 4 (stores)?
- What SvelteKit version is in use?
- What rendering mode is configured? (SSR, SPA, SSG)

**Actions:**
1. Check `package.json` for svelte and @sveltejs/kit versions
2. Look for `svelte.config.js` adapter configuration
3. Note any prerender settings

**Version-Specific Syntax:**
| Concept | Svelte 4 | Svelte 5 |
|---------|----------|----------|
| Reactive state | `let x = 0` | `let x = $state(0)` |
| Derived | `$: doubled = x * 2` | `let doubled = $derived(x * 2)` |
| Effects | `$: console.log(x)` | `$effect(() => console.log(x))` |
| Props | `export let name` | `let { name } = $props()` |

**Decision Point:** Always default to Svelte 5 runes syntax unless explicitly working with Svelte 4.

### Step 3: SSR/CSR Analysis

**Goal:** Understand the rendering context and its implications.

**Thinking Framework:**
- "When does this code run?" (server, client, or both)
- "What data is available at each stage?"
- "Could this cause a hydration mismatch?"

**SSR Decision Matrix:**

| Code Location | Runs On | Use For |
|---------------|---------|---------|
| +page.server.ts | Server only | DB access, secrets, auth |
| +page.ts | Server + Client | Public API calls, URL-dependent data |
| +page.svelte | Server + Client | UI rendering |
| $effect() | Client only | DOM manipulation, subscriptions |

**Common SSR Pitfalls:**
- Browser APIs (window, document) in SSR context
- Different content between server and client render
- Accessing cookies/headers incorrectly

**SSR Safety Pattern:** guard browser-only APIs with `import { browser } from '$app/environment'`, and run DOM access inside `$effect(() => { if (browser) { /* ... */ } })` (effects are client-only).

### Step 4: Data Flow Design

**Goal:** Design correct data loading and mutation patterns.

**Thinking Framework:**
- "Where does this data come from?" (server, client, URL)
- "When should it be fetched?" (navigation, action, interval)
- "Who can access this data?" (public, authenticated, authorized)

**Load Function Selection:**

| Need | Use | Why |
|------|-----|-----|
| Access secrets/DB | +page.server.ts | Never exposed to client |
| Public API call | +page.ts | Runs on both, good for caching |
| SEO-critical data | +page.server.ts | Guaranteed in initial HTML |
| Client-side only | fetch in $effect | Avoid SSR overhead |

**Form Action Thinking:**
- "What mutation does this form perform?"
- "What validation is needed?"
- "What should happen on success/failure?"

**Load Rerun & Auth Implications:**
- Rerun loads with `invalidate(url)` / `invalidateAll()`; declare deps with `depends()`; opt out of tracking with `untrack()`.
- **Layout loads do not auto-rerun on client-side navigation.** For auth, prefer the `handle` hook or per-page server loads over a single root layout load.
- When an action changes auth, update `event.locals` so subsequent loads see the new state.
- Use `getRequestEvent()` (SvelteKit ≥ 2.20) in shared server functions to read `locals`/`url` without threading the event through params.

**Streaming:** return an unawaited promise from a server load and render it with `{#await}` for progressive data.

### Step 5: Reactivity Design

**Goal:** Apply correct reactivity patterns for the use case.

**Thinking Framework - Runes Selection:**

| Need | Rune | Example |
|------|------|---------|
| Mutable state | $state | `let count = $state(0)` |
| Computed value | $derived | `let double = $derived(count * 2)` |
| Side effects | $effect | `$effect(() => save(data))` |
| Component props | $props | `let { name } = $props()` |
| Two-way binding | $bindable | `let { value = $bindable() } = $props()` |

**Reactivity Rules:**
1. Only use `$state` for values that need to trigger updates
2. Use `$derived` for any computed values (not manual updates); keep derived expressions **pure** (no side effects). Use `$derived.by(() => { ... })` for multi-line logic.
3. Use `$effect` sparingly — **only for genuine side effects** (DOM, logging, subscriptions), never to synchronize/derive state. Return a teardown function for cleanup.
4. Never mutate `$derived` values to "fix" them with `$effect`. Derived values **can** be reassigned for optimistic UI and self-revert when dependencies change.

**Deep Reactivity & State Nuances:**
- `$state` objects/arrays are deeply reactive **proxies** — mutating nested fields triggers updates.
- **Never destructure** reactive state or props — it captures a snapshot and breaks reactivity. Access fields directly (`obj.x`) or via getters.
- `$state.raw(...)` — shallow/non-tracked state; reassign the whole value, don't mutate.
- `$state.snapshot(...)` — plain (non-proxy) copy for passing to external/non-Svelte APIs.
- Pass live state into functions via **getter functions** (`() => count`), not the bare variable.

**Effect Variants:** `$effect.pre` (run before DOM update, e.g. autoscroll), `$effect.tracking()` (is this in a reactive context?), `$effect.root` (manually-scoped, manual cleanup).

**Anti-Patterns to Avoid:**
```svelte
<script>
  // BAD: using $effect to derive/sync state
  let doubled = $state(0);
  $effect(() => { doubled = count * 2; }); // use $derived instead

  // BAD: destructuring reactive state/props (loses reactivity)
  let { user } = data;        // snapshot — won't update
  let { x, y } = $state({ x: 0, y: 0 });

  // BAD: mutating props
  let { count } = $props();
  count += 1;                 // props are read-only; use $bindable() for two-way
</script>
```

### Step 6: Component Design

**Goal:** Design reusable, composable components.

**Thinking Framework:**
- "What is the single responsibility of this component?"
- "What props does it need?"
- "How flexible should slot composition be?"

**Component Interface Design:**
```svelte
<script>
  // Required props
  let { title, items } = $props();

  // Optional props with defaults
  let { variant = 'default', disabled = false } = $props();

  // Callback props
  let { onClick = () => {} } = $props();

  // Bindable props for two-way binding
  let { value = $bindable() } = $props();
</script>
```

**Slot Patterns:**
- Default slot: Main content area
- Named slots: Header, footer, sidebar
- Slot props: Passing data to slot content

### Step 7: Performance Optimization

**Goal:** Ensure optimal rendering performance.

**Thinking Framework:**
- "How often does this reactive value change?"
- "What is the cost of re-rendering?"
- "Can this be memoized or debounced?"

**Performance Checklist:**
- [ ] Avoid expensive computations in $derived
- [ ] Use {#key} block for forced re-renders
- [ ] Implement virtualization for long lists
- [ ] Lazy load heavy components
- [ ] Preload critical routes

### Step 8: Error Handling

**Goal:** Provide good error experiences.

**Error Boundaries:** `+error.svelte` (route-level), try/catch in load functions,
`fail()` in form actions, `<svelte:boundary>` (component-level, see Quick Reference).

**Error Pattern:** throw `error(404, 'Not found')` from a load when data is missing;
SvelteKit renders the nearest `+error.svelte` with `page.error`/`page.status`.

## Project Setup

**Preferred Package Manager:** bun

```bash
# Create new SvelteKit project with the modern `sv` CLI
# (replaces the deprecated `npm create svelte`)
bunx sv create my-app
cd my-app
bun install
bun run dev
```

**Minimal modern dependencies** (all devDependencies): `@sveltejs/adapter-auto ^6`, `@sveltejs/kit ^2`, `@sveltejs/vite-plugin-svelte ^5`, `svelte ^5`, `vite ^6`.

## Documentation Resources

**Context7 Library ID:** `/websites/svelte_dev` (5523 snippets, Score: 91)

**AI usage guidance:** `https://svelte.dev/docs/ai`

**Official llms.txt Resources** (package-level files; the old top-level `/docs/llms-small.txt` 404s):
- `https://svelte.dev/llms.txt` - Documentation index
- `https://svelte.dev/docs/svelte/llms-full.txt` - Complete Svelte docs
- `https://svelte.dev/docs/svelte/llms-small.txt` - Compressed Svelte docs
- `https://svelte.dev/docs/kit/llms.txt` - SvelteKit docs

## Quick Reference

### Svelte 5 Runes

```svelte
<script>
  // Reactive state
  let count = $state(0);

  // Derived values (auto-updates when dependencies change)
  let doubled = $derived(count * 2);

  // Side effects
  $effect(() => {
    console.log(`Count is now ${count}`);
  });

  // Multi-line derived
  let summary = $derived.by(() => items.reduce((a, b) => a + b.n, 0));

  // Props: defaults, rename, rest
  let { name = 'World', super: trouper, ...rest } = $props();

  // Bindable props (opt-in two-way binding; default to one-way)
  let { value = $bindable() } = $props();

  // SSR-safe unique id
  const id = $props.id();
</script>
```

### Modern Template Syntax

```svelte
<script>
  import type { Snippet } from 'svelte';
  let { header, children }: { header?: Snippet; children: Snippet } = $props();
  let active = $state(true);
</script>

<!-- Events are plain attributes (no `on:` colon) -->
<button onclick={() => (active = !active)}>Toggle</button>

<!-- class accepts an object (clsx-like) -->
<div class={{ active, disabled: !active }}>...</div>

<!-- Snippets replace slots -->
{#snippet row(label, value)}
  <tr><th>{label}</th><td>{value}</td></tr>
{/snippet}

{@render header?.()}
{@render children()}
{@render row('Status', active ? 'on' : 'off')}

<!-- Error boundary with failed/pending snippets -->
<svelte:boundary>
  <RiskyComponent />
  {#snippet failed(error, reset)}
    <p>{error.message}</p>
    <button onclick={reset}>Retry</button>
  {/snippet}
</svelte:boundary>
```

### SvelteKit Routing

Files under `src/routes/`: `+page.svelte` (UI), `+page.ts` (universal load),
`+page.server.ts` (server load/actions), `+layout.svelte` / `+layout(.server).ts`
(layouts), `+server.ts` (API endpoint), `+error.svelte` (error boundary).
Dynamic segments use `[slug]`; rest params `[...rest]`; optional `[[lang]]`.

### Load Functions & Typed Data

```typescript
// +page.server.ts - Server-only
import type { PageServerLoad } from './$types';
export const load: PageServerLoad = async ({ params, locals, fetch }) => {
  const post = await fetch(`/api/posts/${params.slug}`);
  return { post: await post.json() };
};
```

```svelte
<!-- +page.svelte - typed props (replaces `export let data`) -->
<script lang="ts">
  import type { PageProps } from './$types';
  let { data }: PageProps = $props();
</script>
```

### Page State (use `$app/state`, not `$app/stores`)

```svelte
<script>
  // `$app/stores` is deprecated. `$app/state` is fine-grained, no `$` prefix.
  import { page, navigating, updated } from '$app/state';
</script>

<p>Path: {page.url.pathname} · Status: {page.status}</p>
{#if navigating.to}<progress></progress>{/if}
```

### Form Actions

```typescript
// +page.server.ts
import { fail } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions: Actions = {
  default: async ({ request, locals }) => {
    const data = await request.formData();
    const email = data.get('email');
    // Use fail() for validation errors — do NOT throw
    if (!email) return fail(400, { email, missing: true });
    return { success: true };
  }
};
```

```svelte
<!-- Progressive enhancement via use:enhance (not raw onsubmit) -->
<script>
  import { enhance } from '$app/forms';
</script>
<form method="POST" use:enhance>...</form>
```

### Page Options

```typescript
// +page.ts / +page.server.ts
export const prerender = true;   // or false | 'auto'
export const ssr = false;        // SPA shell (client-rendered)
export const csr = false;        // static HTML, no JS/hydration

// Dynamic prerender entries
export function entries() {
  return [{ slug: 'first' }, { slug: 'second' }];
}
```

### Hooks

| Hook | File | Scope | Purpose |
|------|------|-------|---------|
| `handle` / `handleFetch` / `init` | hooks.server | Server | Request interception, auth, fetch rewriting, startup |
| `handleError` | hooks (.server/.client) | Shared | Centralized error logging/shaping |
| `reroute` / `transport` | hooks | Universal | URL rewriting; custom-type (de)serialization across server↔client |

## State Management

- The server is **stateless** — never store per-user data in module-level globals (it leaks across requests). Keep load functions pure.
- Share client state via the **context API** (`setContext`/`getContext`), URL params, or snapshots — not module-level mutable singletons.

## Modern Patterns (Experimental — Opt-In)

> These are **experimental** APIs. Enable them explicitly and prefer the stable runes/load/action patterns above unless a project has opted in.

### Async Svelte

Experimental in Svelte 5.36 (flag removed / default in Svelte 6). Allows `await` in top-level `<script>`, inside `$derived(...)`, and directly in markup.

```js
// svelte.config.js
export default { compilerOptions: { experimental: { async: true } } };
```

```svelte
<script>
  let { id } = $props();
  // await directly in $derived
  let post = $derived(await getPost(id));
</script>

<!-- Must be wrapped by a boundary with a `pending` snippet -->
<svelte:boundary>
  <h1>{post.title}</h1>
  {#snippet pending()}<p>loading…</p>{/snippet}
</svelte:boundary>
```

- Detect in-flight async with `$effect.pending()`.
- A `await_waterfall` warning fires when independent async work is needlessly serialized — start independent work together.
- Errors bubble to the nearest `<svelte:boundary>`.

### SvelteKit Remote Functions

Opt-in type-safe server functions callable from the client; can **replace load functions and form actions**. Pairs naturally with async Svelte.

```js
// svelte.config.js
export default { kit: { experimental: { remoteFunctions: true } } };
```

`.remote.ts` files export from `$app/server`:

| Export | Use For | Highlights |
|--------|---------|-----------|
| `query` | Read dynamic data | Cached per-page, `.refresh()`, Standard Schema (Zod/Valibot) validation |
| `form` | Form mutations | Spread `{...createPost}` onto `<form>`; progressive enhancement; single-flight `.updates()`; `withOverride` optimistic UI; `buttonProps` per-button |
| `command` | Programmatic writes | `.updates(query())`; cannot run during render; no redirects |
| `prerender` | Build-time reads | `inputs:` seeds; `{ dynamic: true }` option |

```ts
// data.remote.ts
import { query } from '$app/server';
import * as v from 'valibot';

export const getPost = query(v.string(), async (slug) => {
  return await db.posts.find(slug); // server-only, type-safe end to end
});
```

- Validation failures return **400**; customize via `handleValidationError`.
- `getRequestEvent()` works inside remote functions (no `params`/`route.id`; cookies only settable in `form`/`command`).

## Present Results to User

When answering Svelte/SvelteKit questions:
- Provide complete, runnable code examples
- Use Svelte 5 runes syntax and modern SvelteKit conventions (`$app/state`, `PageProps`, snippets) by default
- Explain the difference between server and universal load functions
- Note any breaking changes between SvelteKit versions
- Flag experimental APIs (async Svelte, remote functions) as opt-in
- Include TypeScript types when applicable

## Troubleshooting

**"Cannot use $state outside of component"**
- Runes only work inside `.svelte` files or `.svelte.ts` files

**"Hydration mismatch"**
- Ensure server and client render the same content initially
- Check for browser-only code running during SSR

**"Load function not running"**
- Verify file naming: `+page.ts` or `+page.server.ts`
- Check if `load` function is properly exported

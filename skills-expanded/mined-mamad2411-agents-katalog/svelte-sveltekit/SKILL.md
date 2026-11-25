---
name: svelte-sveltekit
description: Build, review, refactor, and debug modern Svelte 5 and SvelteKit apps using current idioms rather than legacy patterns. Use whenever a task involves `.svelte` components, SvelteKit routes, `load` functions, form actions, SSR or hydration issues, runes, navigation, invalidation, component API design, or state flow in a Svelte/SvelteKit codebase, even if the user only asks for a bugfix or small feature.
---

# Svelte + SvelteKit

Work from current Svelte 5 and current SvelteKit idioms. Optimize for code that is easy to reason about under SSR, hydration, and navigation.

Do not spend time explaining basic syntax unless the user asks. Focus on architectural choices, caveats, and the shortest correct implementation.

## Workflow

1. Establish the local style before changing code.
- Inspect `package.json`, `svelte.config.*`, route layout, and nearby components.
- Prefer the repo's existing conventions in touched files unless the task is an explicit migration.
- For new code, default to runes mode and current SvelteKit APIs.

2. Choose the right boundary before writing code.
- Put server-only work in `+page.server.*`, `+layout.server.*`, `+server.*`, hooks, or `$lib/server/*`.
- Put reusable view logic in components, not route files.
- Keep route data flow obvious: params -> load/action -> typed props -> component.

3. Solve data flow first, then UI details.
- Decide where truth should live: URL, server data, component state, context, or a shared reactive object.
- Prefer deriving state over synchronizing copies of state.
- Add effects only for external side effects such as DOM APIs, timers, subscriptions, analytics, or imperative libraries.

4. Be explicit about SSR and navigation behavior.
- Check whether code runs on the server, in the browser, or both.
- Check whether state should survive navigation, reload, back/forward, or SSR.
- Check whether data should rerun automatically or only after explicit invalidation.

## Core Svelte Idioms

- Use runes-first patterns in new code: `$state`, `$derived`, `$props`, snippets, and current event syntax.
- Use `$state` only for values that must participate in reactivity. Keep plain variables plain, and prefer `$state.raw` for large objects or arrays that are replaced wholesale rather than mutated in place.
- Prefer `$derived` for computed values. Do not use `$effect` to keep one piece of state in sync with another unless there is no better source of truth.
- Use `$derived.by(...)` when the computation needs multiple statements. Remember that derived objects and arrays are returned as-is rather than made deeply reactive.
- Treat `$effect` as an escape hatch for external systems, not a general state-management tool.
- Do not update state inside `$effect` unless you are bridging to something outside Svelte. Prefer direct event handlers, function bindings, `{@attach ...}`, or `createSubscriber(...)` before reaching for an effect.
- Use `$inspect` and `$inspect.trace(...)` when debugging reactivity instead of leaving logging effects in place.
- Treat props as live inputs. Derive from them instead of snapshotting them into local variables that will silently drift when the parent changes.
- Avoid copying props into local mutable state unless the component intentionally forks from the parent value.
- Prefer explicit component APIs over "smart" components with many optional behaviors.
- Keep components narrow. Move data loading, auth, and persistence out of leaf UI components.
- Prefer snippets and explicit children rendering over legacy slot patterns in new code.
- Top-level snippets can also be referenced from `<script>`, which is often clearer than splitting tiny render helpers into separate components.
- Prefer `onclick={...}` and other current event attributes. Use `<svelte:window>` or `<svelte:document>` for global listeners instead of wiring them up in `onMount` or `$effect`.
- Prefer keyed `{#each}` blocks for stable identity. Do not use array index as the key.
- Avoid destructuring each-block items when the template mutates them.
- Prefer JS-to-CSS handoff with `style:--token={value}` and CSS custom properties when component state or parents need to influence styling.
- Prefer CSS custom properties to let parents influence child presentation. Reach for `:global(...)` only when styling third-party output or a boundary you do not control.
- Prefer `createContext` over ad hoc `setContext`/`getContext` pairs when context is the right tool.
- Do not default to stores for local sharing. In Svelte 5, a reactive object or class with `$state` fields is often simpler.
- Keep stores for cases where the store contract is actually useful: async streams, external subscriptions, or existing ecosystem integrations.

## Component Design

- Keep presentational components pure: props in, events/callbacks out, minimal ownership of app state.
- Put side-effectful orchestration in route components, layout components, or focused controller modules.
- Avoid "prop drilling fixes" that introduce global state too early. Use context when the ownership is local to a subtree.
- Prefer a small number of well-named props over catch-all config objects unless the object is a real domain shape.
- When a component exposes many booleans or variant combinations, consider splitting it or introducing a clearer discriminated API.

## SvelteKit Data and Mutation Rules

- Use `+page.server.*` or `+layout.server.*` when code needs secrets, direct database access, cookies, or trusted request context.
- Use universal `load` only when the logic is safe on both server and client and rerunning in the browser is acceptable.
- Keep `load` side-effect free. Fetch, read, and derive there; mutate in actions, endpoints, or other server handlers.
- Use the `fetch` provided by SvelteKit inside `load` instead of a generic client so cookies and auth flow correctly on the server.
- Use `parent()` deliberately. Avoid creating fragile hidden coupling across nested loads.
- Use `depends()` and targeted invalidation only when automatic reruns are insufficient. Do not scatter `invalidateAll()` as a general refresh button.
- Prefer returning typed, already-shaped data from `load` instead of pushing reshaping work into every consumer.
- Use generated `$types` helpers like `PageProps`, `LayoutProps`, and route-specific load/action types.

## Forms, Actions, and Endpoints

- Prefer form actions for user-driven mutations that naturally come from a page form.
- Keep actions close to the route that owns the UI and validation unless multiple routes truly share the mutation.
- Return validation errors through action results rather than throwing generic errors for expected bad input.
- Use `use:enhance` for progressive enhancement, not to reinvent client-side mutation handling from scratch.
- Use `+server.*` endpoints for API-style interactions, webhooks, non-form clients, or cases where the route action model is awkward.
- Do not hide straightforward form workflows behind custom fetch wrappers if the native action flow already fits.
- For idempotent filter/search forms, prefer `GET` plus URL params over `POST`.

## State Placement

- Put SSR-relevant or shareable state in the URL when it should survive reloads, deep links, or server rendering.
- Keep disposable UI state in the component if losing it on reload is fine.
- Use snapshots when ephemeral state should survive history navigation without becoming URL or server state.
- Do not put request-specific server state in shared modules. In SvelteKit, mutable module state can leak across requests.
- If state is shared only within one rendered subtree, prefer context over module-level singletons.
- Remember that route components are often preserved across navigation. If a value should reset on route change, key the subtree or derive it from `page.url` instead of assuming remounts.

## SSR and Hydration Caveats

- Guard browser-only APIs such as `window`, `document`, storage, observers, and media APIs behind `onMount` or a browser check.
- Do not read auth, cookies, or secrets in client code when the server can decide once and send the result as page data.
- Hydration mismatches usually come from non-deterministic rendering:
  - browser-only branches rendered on the server
  - time/randomness during render
  - locale differences between server and client
  - data that changes between SSR and hydration
- Prefer rendering stable placeholders from SSR and upgrading in the browser rather than branching into incompatible markup.

## Navigation and Invalidation

- Use links and forms in ways that let the router help you. Avoid manual navigation code when a declarative `href` or form submission is enough.
- Lean on SvelteKit preload behavior for perceived performance before inventing custom prefetch logic.
- Use `goto` when navigation is truly imperative, not as a replacement for normal links.
- When data goes stale after a mutation, invalidate the narrowest dependency you can.
- If UI state should not survive a route change, key the relevant subtree explicitly instead of manually resetting many variables.

## Performance and Review Heuristics

- Remove unnecessary effects before trying micro-optimizations.
- Prefer derived values close to their source over widely shared mutable state that forces synchronization.
- Watch for oversized layout loads that fetch data unrelated to most children.
- Watch for route-level waterfalls created by avoidable sequential `await`s.
- Watch for over-centralized stores that make simple features depend on global mutation.
- Watch for components that both fetch data and render complex UI; split ownership before the file turns into a control tower.

## Debugging Checklist

- If data is unexpectedly stale, check `load` rerun conditions, `depends()`, invalidation, and whether the code is in universal or server load.
- If state unexpectedly persists across navigation, remember that components may be reused. Key the subtree or derive from route state.
- If state unexpectedly resets, verify whether it belongs in component state, URL params, snapshots, or server data.
- If a form mutation behaves differently with and without JavaScript, compare native action behavior against custom `use:enhance` logic.
- If auth behaves inconsistently, verify that protected reads happen in server-only code and that cookies are read or written in the right boundary.
- If hydration fails, compare SSR markup assumptions against browser-only logic and non-deterministic rendering.

## Migration and Compatibility

- For existing pre-runes code, do not churn files into modern syntax unless the task is migration or the touched code becomes materially clearer.
- When touching legacy code, prefer local consistency plus small targeted improvements over mixed paradigms inside one file.
- If introducing a modern pattern into an older area, explain the tradeoff in comments or the summary only when it is not obvious from the diff.
- Prefer modern replacements in new code: runes over `$:` and `export let`, snippets over slots, direct component references over `<svelte:component>`, and classes with `$state` fields over stores when sharing local reactive state.
- Use promise-in-template features such as await expressions only when the project is on a compatible Svelte version and has the relevant experimental option enabled.

## Official References

Consult the current Svelte docs when framework behavior matters or seems version-sensitive:
- `https://svelte.dev/docs/svelte/best-practices`
- `https://svelte.dev/docs/svelte/$state`
- `https://svelte.dev/docs/svelte/$derived`
- `https://svelte.dev/docs/svelte/$effect`
- `https://svelte.dev/docs/svelte/$props`
- `https://svelte.dev/docs/kit/load`
- `https://svelte.dev/docs/kit/form-actions`
- `https://svelte.dev/docs/kit/state-management`

---
name: svelte-sveltekit-engineering
description: Svelte and SvelteKit engineering guidance. Use when adding, changing, reviewing, or testing .svelte components, Svelte 5 runes, stores, context, SvelteKit routing, load functions, form actions, hooks, adapters, or deciding between standalone Svelte and full SvelteKit. Use javascript-typescript-engineering for generic JS/TS package/build/test mechanics, css-scss-styling for stylesheet and Tailwind decisions, api-design for backend contract shape, and ux-accessibility-review for accessibility audits. Do not use for non-Svelte frontend frameworks.
---

# Svelte and SvelteKit Engineering

Use this skill for Svelte component design, Svelte 5 runes/reactivity, and
SvelteKit application structure, routing, data loading, and form handling.
Inspect the repository before assuming a version: check `package.json` for
`svelte`/`@sveltejs/kit` major versions, `svelte.config.js` for the adapter, and
whether components use runes (`$state`, `$derived`, `$effect`, `$props`) or
legacy Svelte 4 syntax (`export let`, `$:`, `writable` stores as the default
reactivity model). Do not silently rewrite Svelte 4 idioms to runes, or vice
versa, unless the task is an explicit migration.

Load [`javascript-typescript-engineering`](../javascript-typescript-engineering/SKILL.md)
for package manager workflow, TypeScript configuration, bundler/Vite mechanics,
and generic JS/TS lint/build/test commands. Load
[`css-scss-styling`](../css-scss-styling/SKILL.md) for `<style>` block
architecture, Tailwind, CSS modules, and design tokens. This skill owns
Svelte-specific and SvelteKit-specific decisions only.

## Svelte (Standalone) vs. SvelteKit

Choose deliberately; do not default to SvelteKit for every UI, and do not reach
for standalone Svelte once routing or server behavior is needed.

Use **standalone Svelte** (via Vite's `svelte` template, a component library, or
embedding Svelte components into an existing non-Svelte page) when:

- The project is a single component, a widget embedded in another site or CMS,
  a design-system/component-library package, or a browser extension UI.
- There is no need for file-based routing, multiple pages, or navigation state
  owned by the framework.
- Rendering is client-only and SEO, first-paint content, or crawlability do not
  matter — e.g., an internal dashboard behind auth, an admin widget, or a
  `<canvas>`/data-viz component.
- The app has no server-side concerns of its own: no need to keep secrets off
  the client, call a database directly, or render personalized HTML before
  JavaScript runs.
- Deployment target is a static asset host or the component ships inside
  another application's bundle (npm package, Web Component wrapper).

Use **SvelteKit** when any of these apply:

- The app needs more than one route, nested layouts, or URL-driven navigation.
- Pages need SSR or prerendering for SEO, social-preview metadata, or fast
  perceived load on slow connections/devices.
- The app must keep secrets (API keys, database credentials) off the client —
  `+page.server.js`/`+server.js` run only on the server.
- The app needs form handling with progressive enhancement, cookie-based
  sessions, or server-validated mutations (form actions).
- Deployment targets a Node server, edge runtime (Cloudflare Workers, Vercel
  Edge, Deno Deploy), or a serverless platform — SvelteKit adapters exist for
  these; plain Svelte does not manage server output.
- The app benefits from SvelteKit's file-based conventions (`+page.svelte`,
  `+layout.svelte`, `+server.js`) to avoid hand-rolling a router, data-loading
  convention, or error-boundary pattern.

If a project starts as standalone Svelte and later needs routing, SSR, or a
backend-for-frontend layer, migrating to SvelteKit is straightforward because
SvelteKit is built on the same component model — prefer that migration over
hand-building routing/SSR on top of plain Svelte.

## Reactivity: Runes vs. Legacy Reactivity

Svelte 5 introduced runes as the default reactivity primitive. Match the
repository's actual syntax; a mixed codebase mid-migration is normal but new
code should follow the direction the repo has already chosen.

- **`$state`** replaces implicit top-level reactive `let` bindings. Use it for
  any local mutable value a component template reads. `$state` is deeply
  reactive for plain objects/arrays; mutating a property (`obj.x = 1`,
  `arr.push(...)`) triggers updates without needing to reassign.
- **`$derived`** (and `$derived.by(() => ...)` for multi-statement logic)
  replaces `$:` reactive declarations for computed values. Prefer `$derived`
  over `$effect` whenever a value is *computed from* other state — `$effect` is
  for side effects, not for producing values other code reads.
- **`$effect`** replaces `$:` used for side effects (DOM APIs, subscriptions,
  logging, syncing to `localStorage`). Keep effects narrow and clean up
  subscriptions/timers/listeners by returning a teardown function. Avoid
  `$effect` for state derivation — an effect that only sets another `$state`
  from its dependencies is a smell; use `$derived` instead.
- **`$props`** replaces `export let` for declaring component inputs, including
  defaults (`let { count = 0 } = $props()`) and rest props
  (`let { class: className, ...rest } = $props()`).
- **`$bindable`** marks a prop that a parent may bind to with `bind:`; only mark
  props bindable when two-way binding is a deliberate part of the component's
  contract, not by default.
- Stores (`writable`, `readable`, `derived` from `svelte/store`) are still
  useful for state that must be shared across component instances without
  prop-drilling, state that outlives a single component tree (app-wide
  settings, auth session), or state consumed outside components (e.g., in a
  `.ts` module). Runes replace stores for component-local reactive state; they
  do not replace the store contract for cross-cutting shared state, though
  `$state` in a plain `.svelte.js`/`.svelte.ts` module is now a common
  runes-based alternative to a store for shared state.
- Use the **context API** (`setContext`/`getContext`) to pass state down a
  component tree without prop-drilling through intermediate components that
  don't use it themselves — typically paired with a `$state` object so
  descendants get reactive updates. Context is not a global store: it is scoped
  to the component tree rooted where `setContext` was called, which makes it
  safe for per-request/per-instance state (important in SSR, where a
  module-level singleton would leak state between requests).

### Reactivity Anti-Patterns

- Module-level mutable `$state`/store used to hold per-request or per-user data
  in a SvelteKit app. On the server, module scope is shared across concurrent
  requests — this leaks one user's data into another's response. Use `load`
  return values, `event.locals`, or context populated per-request instead.
- Using `$effect` to derive a value that other code reads (`$effect(() => count2 = count * 2)`).
  Use `$derived` — it is pull-based and avoids ordering bugs and extra renders.
- Deep-cloning or reassigning entire objects/arrays to force reactivity. With
  `$state`, mutation is already tracked; reassignment gymnastics left over from
  Svelte 4's array-reassignment workaround are unnecessary and hurt
  readability.
- Subscribing to a store manually with `.subscribe()` inside a component instead
  of using the `$store` auto-subscription syntax, causing manual unsubscribe
  bugs and memory leaks in components without a matching cleanup.
- Putting business logic inside `$effect` blocks that reach into the DOM
  directly when a declarative binding (`bind:value`, `class:`, `style:`) would
  do the same thing more predictably.

## Component Design

- Keep components focused on presentation and local interaction; push data
  fetching, validation, and cross-cutting business rules to `load` functions,
  form actions, or plain `.ts` modules that components import. A component that
  both fetches data and renders it is harder to test and reuse.
- Prefer composition (slots/snippets, `{#snippet}`/`{@render}` in Svelte 5, or
  child components) over large components with many boolean props that toggle
  internal branches. A `variant`/boolean-prop explosion is a sign the component
  should split or use composition instead.
- Type props explicitly in TypeScript projects (`let { items }: { items: Item[] } = $props();`)
  rather than inferring from usage; this keeps the component's contract visible
  at a glance and catches mismatches at the call site.
- Keep two-way binding (`bind:`) to genuine form-control-like components. Avoid
  exposing `bind:` on every prop by default — most parent/child communication
  should flow one-directionally down via props and up via callback props or
  events, reserving `$bindable` for controls that behave like native form
  elements.
- Name event-handling props consistently (`onclick`, `onsubmit`, or a domain
  name like `onSelect`) since Svelte 5 uses plain props for event handlers
  rather than `createEventDispatcher` in new code; reserve
  `createEventDispatcher` for maintaining existing Svelte 4 component
  contracts.
- Co-locate a component's styles in its own `<style>` block; Svelte scopes
  styles per component automatically, so avoid hand-rolled class-name
  namespacing to prevent collisions. Route non-trivial styling architecture
  decisions to [`css-scss-styling`](../css-scss-styling/SKILL.md).

## Project Structure and File Conventions

- Respect SvelteKit's routing conventions in `src/routes`: `+page.svelte` for a
  page, `+layout.svelte` for shared layout, `+page.server.js`/`.ts` and
  `+layout.server.js` for server-only data and actions, `+server.js` for
  standalone API endpoints, and `+error.svelte` for route-scoped error UI.
  Route groups (`(group)`) organize routes without affecting the URL; matcher
  files (`src/params/*.js`) validate dynamic segment shape.
- Put shared, non-route code under `src/lib` (aliased as `$lib`) — components,
  utilities, stores/runes modules, server-only helpers. Use `$lib/server` (or an
  equivalent convention) for modules that must never be imported from
  client-rendered code, and treat any import of a server-only module from a
  `+page.svelte` as a bug: SvelteKit only enforces this boundary for code that
  actually reaches `+page.server.js`/`+server.js`/`hooks.server.js` — a
  client-imported module has no such protection, so keep secrets and
  privileged logic out of anything reachable from the client bundle.
- Keep `hooks.server.js`/`hooks.client.js` for cross-cutting concerns:
  authentication population (`event.locals`), request logging, error
  normalization. Avoid stuffing route-specific logic into hooks — that belongs
  in the route's own `load`/action/server endpoint.
- Use `app.d.ts` to type `App.Locals`, `App.PageData`, `App.Error`, and
  `App.Platform` so `event.locals` and `load` return values are typed
  end-to-end instead of `any`.
- Keep a clear module boundary between UI components (`$lib/components`),
  domain/service logic (`$lib/server/*` or `$lib/domain/*`), and route glue
  (`+page.server.ts`, `+server.ts`). Route files should stay thin — parse
  input, call a service function, shape the response — mirroring the
  thin-handler guidance in
  [`hexagonal-architecture`](../hexagonal-architecture/SKILL.md) when the
  backend logic is substantial enough to warrant explicit ports/adapters.

## Design Patterns

Load the [Svelte/SvelteKit patterns reference](references/patterns.md) for
worked guidance on layout composition, `load` function design (universal vs.
server, streaming/parallel loading, invalidation), form actions and
progressive enhancement, and other patterns that appear repeatedly in
production SvelteKit apps.

## Anti-Patterns

Load the [Svelte/SvelteKit anti-patterns reference](references/anti-patterns.md)
for a fuller catalogue. Highest-impact items:

- Fetching data in `onMount`/`$effect` inside a page component instead of a
  `load` function — this delays rendering, breaks SSR, and duplicates
  loading/error-state handling that SvelteKit already provides.
- Calling a database, ORM, or secret-bearing API directly from a `.svelte`
  component or a universal `load` (`+page.js`) that also runs in the browser.
  Use `+page.server.js`/`+server.js` for anything that must stay server-only.
- Storing all application state in one global store, turning it into an
  untyped, unscoped god-object. Scope state to the route or component tree that
  owns it; use context or route-level `load` data instead.
- Reimplementing form submission with `fetch` and manual `preventDefault` when
  a form action plus `use:enhance` would give the same UX with progressive
  enhancement and less code.
- Ignoring `+error.svelte` and letting every failure fall through to a generic
  crash page, instead of throwing `error()`/`redirect()` from `load` or actions
  with actionable status codes and messages.

## Backend Integration

Load the [backend integration reference](references/backend-integration.md)
when a SvelteKit frontend talks to a separate backend service (Rust/Axum, PHP,
Python/FastAPI or Django, or another API) rather than owning all server logic
itself. It covers API communication patterns, authentication handoff (cookies
vs. bearer tokens, BFF vs. direct-to-API), and deployment topology choices.

Route the backend's own implementation to its owning skill:
[`rust-async-web`](../rust-async-web/SKILL.md) for Axum,
[`php-engineering`](../php-engineering/SKILL.md) for PHP, and
[`python-engineering`](../python-engineering/SKILL.md) for FastAPI/Django. Use
[`api-design`](../api-design/SKILL.md) when the contract itself (resource
shape, error envelope, versioning) is still being decided. This skill owns only
how the SvelteKit side consumes and is deployed alongside that backend.

## Performance

- Prefer `load` functions and streaming (`export const load = async () => ({ streamed: { slow: slowPromise() } })`)
  over client-side spinners for expensive data — SvelteKit can render the
  shell immediately and stream slow data in.
- Use `data-sveltekit-preload-data` (on by default for `hover`) deliberately;
  disable preloading for expensive or side-effecting links rather than leaving
  it default everywhere.
- Prefer prerendering (`export const prerender = true`) for content that is the
  same for every visitor and does not depend on cookies/session — it removes
  server round-trips entirely for that route.
- Avoid importing large libraries into universal code that also ships to the
  client; keep heavy parsing/formatting/crypto libraries in `+page.server.ts`
  when the result, not the library, is what the client needs.
- Use `$derived` instead of recomputing expensive values in the template or in
  an `$effect` on every dependency change; `$derived` values are cached until a
  dependency actually changes.
- Route deeper profiling, bundle-budget, or Core Web Vitals work to
  [`performance-review`](../performance-review/SKILL.md).

## Error Handling

- Use `error(status, message)` from `@sveltejs/kit` in `load` functions and
  actions for expected failures (404, 403, validation) so SvelteKit renders the
  nearest `+error.svelte` with the right status code.
- Return `fail(status, data)` from form actions for validation errors so the
  form re-renders with the submitted values and field errors, instead of
  throwing and losing form state.
- Implement `handleError` in `hooks.server.js`/`hooks.client.js` to log
  unexpected exceptions with a correlation id and return a safe, user-facing
  message — never leak stack traces or internal error details to the client in
  production. Route structured logging/correlation-id design to
  [`observability-engineering`](../observability-engineering/SKILL.md).
- Distinguish expected domain errors (validation, not-found, unauthorized) from
  unexpected exceptions (bugs, network failures) — only the former should
  produce a specific status code and message; let the latter hit `handleError`.

## Testing

- Unit-test pure logic (utilities, derived-state functions, form-validation
  schemas) with the repository's configured runner (commonly Vitest) without
  mounting components.
- Component-test with `@testing-library/svelte` (or the repo's established
  tool) for rendering behavior, prop/event contracts, and accessibility roles —
  test what the user sees and does, not internal component state.
- Test `load` functions and form actions directly as functions (they are plain
  exported functions) with a constructed `event`-like object, rather than only
  through full page renders.
- Use [`playwright-e2e`](../playwright-e2e/SKILL.md) for checked-in end-to-end
  coverage of navigation, form submission with progressive enhancement,
  authentication flows, and hydration-sensitive behavior that only a real
  browser can verify. Load [`testing-strategy`](../testing-strategy/SKILL.md)
  for deciding the overall unit/component/E2E balance.

## Accessibility

Svelte's compiler emits accessibility warnings (missing `alt`, invalid ARIA
roles, non-interactive elements with click handlers) — treat these as build
warnings to fix, not noise to suppress with `<!-- svelte-ignore -->` unless the
suppression is justified and commented. Load
[`ux-accessibility-review`](../ux-accessibility-review/SKILL.md) for a full
accessibility audit of interactive components, forms, and focus management
(especially around client-side navigation, where SvelteKit does not
automatically move focus or announce route changes the way a full page load
would).

## Security Review Prompts

Load [`security-review`](../security-review/SKILL.md) when SvelteKit work
touches authentication, session cookies, CSRF, form actions that mutate state,
redirects, file uploads, `+server.js` endpoints exposed to the internet, or
data rendered with `{@html ...}` (a raw HTML injection point). Use
[`threat-modeling`](../threat-modeling/SKILL.md) before or during new
`hooks.server.js` auth logic, new `+server.js` endpoints, or a new
backend-for-frontend boundary. Use
[`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md)
for `svelte`/`@sveltejs/kit`/adapter/plugin version bumps and new dependencies.

## Deployment and Adapters

- Match the SvelteKit adapter to the actual deployment target:
  `@sveltejs/adapter-node` for a long-running Node server,
  `@sveltejs/adapter-static` for a fully prerendered static site,
  `@sveltejs/adapter-vercel`/`adapter-netlify`/`adapter-cloudflare` for those
  platforms, and community adapters for other targets. Do not assume Vercel by
  default — check `svelte.config.js`.
- Static/prerendered output has no server runtime: `+page.server.js`,
  `+server.js`, and form actions requiring a live server will not work under
  `adapter-static` unless the route is explicitly excluded from prerendering
  and the platform still runs a server.
- Route Dockerfile/Compose packaging to
  [`container-engineering`](../container-engineering/SKILL.md) and hosted CI/CD
  pipeline configuration to
  [`ci-release-engineering`](../ci-release-engineering/SKILL.md); keep adapter
  selection and environment-variable/platform-binding mechanics here.

## Review Checklist

- Standalone Svelte vs. SvelteKit was a deliberate choice based on routing,
  SSR, secret-handling, and deployment needs — not a default.
- Reactivity uses `$state`/`$derived`/`$effect`/`$props` correctly in Svelte 5
  code, with no `$effect` used purely to derive a value.
- No per-request mutable state lives in module scope on the server.
- Data fetching and secret-bearing calls happen in `load`/`+server.js`/actions,
  never directly in `.svelte` components or client-reachable code.
- Route files stay thin; domain/service logic lives in `$lib`.
- Forms use actions plus `use:enhance` where progressive enhancement matters;
  validation errors return via `fail`, not thrown exceptions.
- Errors distinguish expected (`error()`/`fail()`) from unexpected
  (`handleError`) cases, and no internal details leak to the client.
- The adapter matches the real deployment target, and prerendered routes don't
  depend on per-request server behavior.
- Accessibility warnings from the Svelte compiler are addressed, not
  suppressed, and route-change focus/announcement is considered.
- Tests exist at the right layer: unit for logic, component tests for
  rendering/interaction, Playwright E2E for hydration- and navigation-sensitive
  flows.

## Zod SvelteKit Routing

For selected Zod schemas, load [`zod-engineering`](../zod-engineering/SKILL.md). Parse in server loads/actions/endpoints where appropriate, keep server-only code out of client bundles, validate runtime responses, and map expected failures to supported `fail`/`error` shapes.

---
name: ui-stack-svelte
description: "Building interfaces in Svelte 5 and SvelteKit: project layout, runes ($state, $state.raw, $derived, $effect only for side effects, typed $props, $bindable, $props.id), snippets and render tags, event attributes, keyed each blocks, class and style directives, attachments, shared state in .svelte.ts modules and context, boundaries, transitions, SvelteKit routes, server and universal load functions, form actions with use:enhance, hooks for auth, env modules, Superforms, Bits UI and Melt UI, testing, svelte-check, and the traps. Read when the project uses Svelte or SvelteKit."
---

# Svelte 5 and SvelteKit

Generated Svelte mixes versions (`export let` beside `$props`, `on:click`
beside `onclick`), computes values in `$effect`, forgets keys in `{#each}`,
keeps per-user state in a module the server shares between requests, and
imports database code into a load function that also runs in the browser.
This is Svelte 5 (5.57 in September 2026) with SvelteKit 2 as written now:
runes, snippets, server-only data, and forms that work before JavaScript
loads. SvelteKit 3 is in release candidate: follow the project's version.

## 1. Version and layout

Match the project's Svelte version: these are Svelte 5's runes; a Svelte 4
project uses `export let` props and `$:` statements instead, and one
component never mixes the two.

```text
src/app.html  src/app.css  src/app.d.ts  src/hooks.server.ts
src/lib/components/ui/        primitives: Button, Field, Dialog
src/lib/components/orders/    the parts of one feature
src/lib/server/               database and secrets: server imports only
src/lib/state/cart.svelte.ts  shared state written with runes
src/routes/orders/            +page.svelte, +page.server.ts, +error.svelte
src/routes/api/orders/        +server.ts for other clients
```

A new project starts with `npx sv create`, then `npx sv add` for Tailwind,
Vitest, Playwright and ESLint rather than wiring them by hand.

## 2. Components

- One component per `.svelte` file. Props with `let { title, variant =
  "primary", ...rest } = $props()`, typed, and `rest` spread onto the native
  element a primitive wraps.
- Content through snippets (`{@render children()}`) rather than a prop per
  variation; snippets with parameters for rows and items.

```svelte
<!-- src/lib/components/ui/Button.svelte -->
<script lang="ts">
  import type { Snippet } from "svelte";
  import type { HTMLButtonAttributes } from "svelte/elements";
  type Props = HTMLButtonAttributes & { variant?: "primary" | "quiet"; children: Snippet };
  let { variant = "primary", type = "button", class: className, children, ...rest }: Props = $props();
</script>

<button {type} class={["btn", `btn--${variant}`, className]} {...rest}>
  {@render children()}
</button>
```

```svelte
<!-- a list that renders rows its caller defines -->
<script lang="ts" generics="T extends { id: string }">
  import type { Snippet } from "svelte";
  let { items, row, empty }: { items: T[]; row: Snippet<[T]>; empty: Snippet } = $props();
</script>

{#each items as item (item.id)}{@render row(item)}{:else}{@render empty()}{/each}
```

- `class` takes arrays and objects like `clsx` (5.16+); `class:active={on}`
  and `style:--progress="{pct}%"` for single toggles and values.
- Events are attributes (`onclick={...}`), with no modifiers: call
  `event.preventDefault()` in the handler. A component reports up through
  callback props (`onselect`), not `createEventDispatcher`.
- `$bindable` only for a value the parent really shares both ways (a
  field's `value`, a dialog's `open`); otherwise callbacks.
- `$props.id()` (5.20+) gives an id that matches on server and client, for
  `for`, `aria-describedby` and `aria-controls`.
- Attachments, `{@attach tooltip}` (5.29+), replace `use:` actions for DOM
  behaviour: a function of the element that returns its cleanup.
- Styles in the component's `<style>` (scoped by default) or the project's
  Tailwind; tokens as CSS variables in one global place (`app.css`).

## 3. State

- `$state` for what changes, `$derived` for what follows from it; `$effect`
  only for work outside Svelte (a subscription, the canvas, a chart
  library), with cleanup.

```svelte
<script lang="ts">
  let { orders }: { orders: Order[] } = $props();
  let query = $state("");
  const visible = $derived(orders.filter((o) => o.customer.toLowerCase().includes(query.toLowerCase())));
  const total = $derived.by(() => visible.reduce((sum, o) => sum + o.amount, 0));
</script>
```

- `$state.raw` for large data replaced whole (an API response), reassigned
  to update; `$state.snapshot(value)` before handing state to other code.
- A `$derived` can be assigned for an optimistic value (5.25+); it returns
  to the computed value when its inputs change.
- Destructuring `$state` copies the current values: read `cart.count`, not
  `const { count } = cart`.
- Shared state lives in a `.svelte.ts` module as a class, and reaches
  components through context:

```ts
// src/lib/state/cart.svelte.ts
import { createContext } from "svelte";
export class Cart {
  items = $state<CartItem[]>([]);
  count = $derived(this.items.reduce((n, item) => n + item.quantity, 0));
  add(item: CartItem) { this.items.push(item); }
}
export const [getCart, setCart] = createContext<Cart>(); // 5.40+; setContext and getContext before
```

`setCart(new Cart())` in the root layout, `const cart = getCart()` below. A
module-level instance is shared by every request on the server, one user's
cart shown to the next: module state only for what never differs per user.

- Loading, error and empty as branches: `{#await}` for a promise, explicit
  states otherwise, `{:else}` for an empty `{#each}`. `<svelte:boundary>`
  with a `failed` snippet (and its `reset`) around a part that can throw.

## 4. Lists and motion

- `{#each items as item (item.id)}`: keyed by a stable id, for every list
  that changes.
- `svelte/transition` (`fade`, `fly`, `slide`) for purposeful motion and
  `animate:flip` in keyed lists, with duration 0 when reduced motion is on
  (`prefersReducedMotion.current` from `svelte/motion`; `motion-stacks`).

## 5. SvelteKit: data

- `+page.server.ts` loads anything touching the database, secrets or
  cookies; `+page.ts` (universal) runs on the server and in the browser, so
  it calls public APIs only. `$lib/server` never reaches a browser bundle.

```ts
// src/routes/orders/+page.server.ts
import { redirect } from "@sveltejs/kit";
import { listOrders, listActivity } from "$lib/server/orders";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals, url }) => {
  if (!locals.user) redirect(303, `/login?next=${encodeURIComponent(url.pathname)}`);
  return {
    orders: await listOrders(locals.user, url.searchParams.get("status") ?? "open"),
    activity: listActivity(locals.user), // not awaited: streams in after the page
  };
};
```

- The page reads `let { data }: PageProps = $props()` (2.16+) and streams
  the slow part with `{#await data.activity}` and a skeleton.
- `redirect()`, `error(404, "Order not found")` and `fail()` come from
  `@sveltejs/kit`; in SvelteKit 2 they throw on their own.
- `+error.svelte` per section for failures, `+layout.svelte` for the shared
  frame, `<svelte:head>` for the title and description.
- Auth in `hooks.server.ts`: `handle` puts the session's user in
  `event.locals.user`. A layout's load does not guard form actions or
  `+server.ts` routes: check the user in each (`backend-auth`).
- `$env/static/private` and `$env/dynamic/private` in server files only;
  browser code reads `$env/static/public` (names starting `PUBLIC_`).
- `page` from `$app/state` (2.12+) in new code, not the `$page` store.
- Remote functions (`query`, `form`, `command` in `.remote.ts`) are still
  experimental (2.27+, two flags): only where the project has them on.

## 6. Forms

Form actions in `+page.server.ts`, a real `<form method="POST">`, and
`use:enhance` from `$app/forms`: it works without JavaScript and upgrades
with it.

```ts
// src/routes/orders/new/+page.server.ts
import { fail, redirect } from "@sveltejs/kit";
import { createOrder } from "$lib/server/orders";
import type { Actions } from "./$types";

export const actions = {
  default: async ({ request, locals }) => {
    if (!locals.user) redirect(303, "/login");
    const title = String((await request.formData()).get("title") ?? "").trim();
    if (!title) return fail(400, { title, errors: { title: "Give the order a title." } });
    const order = await createOrder(locals.user, { title });
    redirect(303, `/orders/${order.id}`);
  },
} satisfies Actions;
```

```svelte
<script lang="ts">
  import { enhance } from "$app/forms";
  import type { PageProps } from "./$types";
  let { form }: PageProps = $props();
  let saving = $state(false);
</script>

<form method="POST" use:enhance={() => {
  saving = true;
  return async ({ update }) => { await update(); saving = false; };
}}>
  <label for="title">Title</label>
  <input id="title" name="title" value={form?.title ?? ""}
    aria-invalid={!!form?.errors?.title} aria-describedby="title-error" />
  <p id="title-error">{form?.errors?.title}</p>
  <button disabled={saving}>{saving ? "Creating..." : "Create order"}</button>
</form>
```

- Superforms for larger forms: `superValidate(request, zod4(schema))` on the
  server (`zod4` from `sveltekit-superforms/adapters`, `zod` for Zod 3),
  `superForm(data.form)` in the page for errors, constraints and a
  `$submitting` flag (`frontend-forms`).

## 7. Accessible widgets

- Menus, dialogs, selects, comboboxes and popovers from Bits UI (headless,
  what shadcn-svelte is built on) or Melt UI's builders, themed with the
  tokens, not hand-rolled; `<dialog>` and `popover` for simple cases.
- `svelte-check` reports the compiler's accessibility warnings (a click
  handler on a `div`, a missing label): fix them rather than silence them.

## 8. Testing

Vitest with `@testing-library/svelte`, or Vitest browser mode with
`vitest-browser-svelte`, querying by role and name; Playwright for flows
across pages (`frontend-testing`).

## 9. Traps

- `$effect` computing a value (`$effect(() => { total = ... })`): use
  `$derived`. An effect that writes state it reads loops.
- Mutating a prop the parent owns: callbacks, or `$bindable`.
- Missing keys: after a delete, the next row inherits the removed row's
  input and focus.
- Server-only code in a universal load (`+page.ts`) or a component.
- A reassigned `$state` primitive exported from a module: export an object
  or a class and change its properties.
- `window` or `localStorage` read at a component's top level, which also
  runs on the server: read it in `$effect`, or behind `browser` from
  `$app/environment`.
- `{@html}` with anything but sanitised content: it bypasses escaping.

## Check it

- `npm run check` (`svelte-kit sync` and `svelte-check`): types and
  accessibility warnings. `npm run build`, and `npx vitest run`.
- Look at it with the `preview` tool: `url` `http://localhost:5173/` and
  `start` `npm run dev -- --port 5173 --strictPort`.
- With JavaScript off, pages still render and forms still post.

## Avoid

Svelte 4 and 5 syntax in one component; `$effect` for derived values;
stores for new state; module-level state holding user data; unkeyed lists
that change; database or secret imports in `+page.ts` or components; a
layout load as the only auth check; `createEventDispatcher` in new code;
`{@html}` with user input; forms that only work with JavaScript.

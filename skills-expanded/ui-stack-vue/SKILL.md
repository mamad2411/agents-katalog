---
name: ui-stack-vue
description: "Building interfaces in Vue 3 and Nuxt: project layout, script setup with typed defineProps, defineEmits and defineModel, attribute fallthrough, slots and scoped slots, template refs, ref, reactive and computed, watch versus watchEffect, composables and VueUse, provide and inject, Pinia, keyed v-for, transitions, Nuxt 4 (app directory, pages, layouts, useFetch and useAsyncData keys, $fetch in handlers, server routes, runtime config, useSeoMeta, NuxtImg, middleware), VeeValidate forms, Reka UI and Nuxt UI, testing, vue-tsc, and the traps. Read when the project uses Vue or Nuxt."
---

# Vue 3 and Nuxt

Generated Vue mixes the Options API into `<script setup>`, destructures a
`reactive` object and loses its reactivity, watches one ref to set another,
mutates props, fetches page data with `$fetch` so a Nuxt page requests it
twice, and leaves the starter's green look in place. This is Vue 3.5 with
Nuxt 4 (4.5 in 2026) as written now: typed `<script setup>`, composables,
keyed data fetching, and the Nuxt built-ins.

## 1. Project layout

```text
Vite (npm create vue@latest)           Nuxt 4
src/main.ts  src/App.vue               app/app.vue  app/error.vue
src/router/  src/stores/               app/pages/orders/index.vue, [id].vue
src/components/ui/                     app/layouts/default.vue, dashboard.vue
src/components/orders/                 app/components/  app/composables/
src/composables/  src/views/           app/middleware/  app/assets/css/main.css
                                       server/api/orders.get.ts   server only
                                       shared/   types both sides use
```

- Nuxt auto-imports components, composables and Vue's APIs; a Vite project
  imports them explicitly.
- Delete the starter: create-vue's `HelloWorld.vue`, `TheWelcome.vue` and
  its `base.css` and `main.css` (the green links), or `<NuxtWelcome />`.

## 2. Components

- Single-file components with `<script setup lang="ts">`, named for what
  they are (multi-word: `OrderTable.vue`), one per file.
- Props with `defineProps<{ ... }>()`, destructured with defaults (3.5);
  events with typed `defineEmits`; `v-model` on components through
  `defineModel`. Slots for content, not a prop per variation.

```vue
<!-- components/ui/TextField.vue -->
<script setup lang="ts">
import { useId } from "vue";
const model = defineModel<string>({ required: true });
const { label, error } = defineProps<{ label: string; error?: string }>();
const id = useId(); // stable between server and client (3.5)
</script>

<template>
  <div class="field">
    <label :for="id">{{ label }}</label>
    <input :id="id" v-model="model" :aria-invalid="!!error"
      :aria-describedby="error ? `${id}-error` : undefined" />
    <p v-if="error" :id="`${id}-error`">{{ error }}</p>
  </div>
</template>
```

- Attributes a component does not declare (`class`, `type`, `aria-*`,
  listeners) fall through to its root element, so a Button stays a button.
  When the root is a wrapper, `defineOptions({ inheritAttrs: false })` and
  `v-bind="$attrs"` on the native element.
- Scoped slots let the caller render each item; `defineSlots` types them
  and `generic` types the item:

```vue
<script setup lang="ts" generic="T extends { id: string }">
defineProps<{ items: T[] }>();
defineSlots<{ row(props: { item: T }): any; empty(): any }>();
</script>

<template>
  <ul v-if="items.length">
    <li v-for="item in items" :key="item.id"><slot name="row" :item="item" /></li>
  </ul>
  <slot v-else name="empty" />
</template>
```

- Template refs with `useTemplateRef<HTMLInputElement>("search")` and
  `ref="search"` (3.5); DOM work in `onMounted`.
- Styles scoped, or the project's Tailwind; tokens as CSS variables in one
  place.

## 3. Reactivity

- `ref` by default, for primitives and objects; `computed` for anything
  derived; `reactive` only for an object never reassigned or destructured
  (destructuring copies; `toRefs` if you must).
- Derive with `computed` instead of watching one value to set another:

```ts
// not this
const fullName = ref("");
watch([first, last], () => { fullName.value = `${first.value} ${last.value}`; });
// this
const fullName = computed(() => `${first.value} ${last.value}`);
```

- `watch` for effects outside the component (a request, `localStorage`, a
  chart) on named sources; `watchEffect` when the effect should track
  whatever it reads. `onWatcherCleanup` (3.5) aborts the previous run.
- Destructured props are reactive in the template and in `computed`, but a
  `watch` needs a getter: `watch(() => id, load)`.
- `shallowRef` for large data replaced whole (an API response, a chart's
  dataset). `.value` in script, never in the template.

## 4. Shared logic and state

- Logic several components share goes in a composable (`useX`), not a
  mixin; it accepts refs or getters (`MaybeRefOrGetter`) and reads them
  with `toValue`. VueUse already has most browser ones (`useMediaQuery`,
  `useLocalStorage`, `onClickOutside`, `useEventListener`): use them before
  writing one.
- `provide` and `inject` with a typed `InjectionKey` for compound components
  (tabs and their panels, a form and its fields), not for app state.
- Pinia for shared client state, as setup stores; `storeToRefs` to
  destructure state and getters (actions destructure directly):

```ts
export const useCartStore = defineStore("cart", () => {
  const items = ref<CartItem[]>([]);
  const count = computed(() => items.value.reduce((n, item) => n + item.quantity, 0));
  function add(item: CartItem) { items.value.push(item); }
  return { items, count, add };
});
// in a component: const cart = useCartStore(); const { count } = storeToRefs(cart);
```

- Server data is not store state: `useFetch` in Nuxt; TanStack Query for
  Vue or Pinia Colada in a Vite app (`frontend-data`).

## 5. Templates

- `v-for` with a stable `:key` from the data; never `v-if` and `v-for` on
  the same element (a `<template v-for>` around, or a filtered `computed`).
- Loading, error and empty as three branches in the template.
- `<Transition>` and `<TransitionGroup>` for purposeful motion, turned off
  under `prefers-reduced-motion` (`motion-stacks`).
- `<Teleport to="body">` for an overlay when no library renders it.
- `v-html` only with sanitised content.

## 6. Nuxt

- `NuxtLink` for internal links, `NuxtImg` or `NuxtPicture` when
  `@nuxt/image` is installed (`width`, `height`, `sizes="100vw md:50vw"`),
  `@nuxt/fonts` to self-host the faces the CSS names, `useSeoMeta` or
  `useHead` for a title and description per page, layouts in `app/layouts/`
  chosen with `definePageMeta({ layout: "dashboard" })`.
- Page data with `useFetch` or `useAsyncData`: fetched on the server and
  handed to the client without a second request.

```vue
<script setup lang="ts">
const route = useRoute();
const status = computed(() => String(route.query.status ?? "open"));
const { data: orders, status: load, error, refresh } = await useFetch("/api/orders", {
  query: { status }, // refetches when it changes
});
useSeoMeta({ title: "Orders", description: "[What this page lists]" });
</script>

<template>
  <OrdersSkeleton v-if="load === 'pending'" />
  <LoadError v-else-if="error" what="orders" @retry="refresh" />
  <NoOrders v-else-if="!orders?.length" />
  <OrderTable v-else :orders="orders" />
</template>
```

- `useAsyncData` takes a key that names its data (`order-42`); in Nuxt 4
  calls with one key share one state, so different data needs different
  keys. `lazy: true` (or `useLazyFetch`) lets navigation finish first.
- `$fetch` in event handlers and actions (a click, a submit), never at the
  top of `<script setup>` for page data, where it runs on the server and
  again on the client; `useFetch` never inside a handler.
- Server routes in `server/api/` (`orders.get.ts`, `orders.post.ts`) with
  `defineEventHandler`, validating with `getValidatedQuery` and
  `readValidatedBody` (`backend-api`).
- `runtimeConfig`: top-level keys are server-only (`NUXT_API_SECRET`),
  `public` ones ship to the browser (`NUXT_PUBLIC_SITE_URL`); read with
  `useRuntimeConfig()`.
- Route middleware in `app/middleware/` redirects with `navigateTo("/login")`;
  the server route still checks the user on every request.
- `useState("key", () => ...)` for SSR-safe shared state; `<ClientOnly>`
  or `onMounted` for browser-only parts; `app/error.vue` and
  `createError({ statusCode: 404, statusMessage: "Order not found" })` for
  failures.

## 7. Forms and accessible components

- VeeValidate with a zod schema through `toTypedSchema` from
  `@vee-validate/zod` (`frontend-forms`):

```ts
const { defineField, handleSubmit, errors, isSubmitting } = useForm({
  validationSchema: toTypedSchema(z.object({ email: z.string().email("Enter an email like name@example.com") })),
});
const [email, emailAttrs] = defineField("email");
const onSubmit = handleSubmit((values) => $fetch("/api/invites", { method: "POST", body: values }));
```

  In the template: `<form @submit="onSubmit">`, the input with
  `v-model="email" v-bind="emailAttrs"`, `errors.email` under the field
  with `aria-describedby`, and the button `:disabled="isSubmitting"`.
- With Nuxt UI, `UForm` takes the schema and the state directly and
  `UFormField` wires the label, hint and error.
- Accessible widgets from Reka UI (headless, formerly Radix Vue),
  shadcn-vue (Reka UI with Tailwind), Nuxt UI v4 (Reka UI and Tailwind v4)
  or Headless UI for Vue; PrimeVue for data-heavy screens. Themed from the
  tokens: Nuxt UI's colours in `app.config.ts` (`ui.colors`, green and
  slate by default) and a `@theme static` scale for the brand colour.

## 8. Testing

Vitest with `@vue/test-utils` (`mount`, then
`await wrapper.get("button").trigger("click")` and `wrapper.emitted()`) or
`@testing-library/vue` (queries by role); `@nuxt/test-utils` and
`mountSuspended` for components that use Nuxt composables; Playwright for
flows (`frontend-testing`).

## 9. Traps

- Destructuring `reactive()` or a store loses reactivity: `toRefs`,
  `storeToRefs`. Reassigning a `reactive` object breaks every reference to
  it: use `ref`.
- Watchers instead of computed; mutating props, including an object prop's
  fields (emit, or `defineModel`).
- `v-if` with `v-for` on one element; index keys on lists that change.
- `$fetch` for page data in setup, `useFetch` in a handler, two
  `useAsyncData` calls sharing a key for different data.
- `window`, `document` or `localStorage` read during setup, which runs on
  the server: `onMounted`, `import.meta.client`, or `<ClientOnly>`.
- Class instances or functions in `useState` or Pinia state: the SSR
  payload cannot carry them.
- A date or random value rendered on the server and again on the client:
  format with a fixed locale and time zone, or put `data-allow-mismatch`
  (3.5) on that one element.

## Check it

- Types: `npm run type-check` (create-vue runs `vue-tsc --build`), or
  `npx nuxt typecheck`; then `npm run build`, `npm run lint` and
  `npx vitest run`.
- Look at the result with the `preview` tool: with Vite, `url`
  `http://localhost:5173/` and `start` `npm run dev -- --port 5173
  --strictPort`; with Nuxt, `url` `http://localhost:3000/` and `start`
  `npm run dev -- --port 3000`.
- Hydration mismatches in the console the `preview` report lists are bugs.

## Avoid

Options API and `<script setup>` mixed in one component; destructured
`reactive` state; `watch` to derive a value; mutated props; `v-if` with
`v-for`; `$fetch` for page data at setup; shared `useAsyncData` keys; a
store for server data; browser APIs in setup; hand-rolled dialogs and
menus; Nuxt UI left on its default green and slate; the starter's
components and colours left in place.

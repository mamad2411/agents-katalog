---
name: vue-ecosystem
description: Expert Vue 3.5+ and Nuxt 3 guidance covering reactivity, composables, SFC architecture, SSR/data fetching, state management, and testing. Use when writing or reviewing Vue or Nuxt code.
source: https://github.com/JetBrains/skills/tree/main/vue-best-practices
---

# Vue Ecosystem

Production-grade Vue 3.5+ and Nuxt 3.x practices: Composition API, fine-grained reactivity, composable design, route-level SSR with `useFetch`/`useAsyncData`, Pinia state, and Web Vitals discipline.

## Stack Baseline (2026)

| Component | Default | Notes |
| --- | --- | --- |
| Vue | 3.5.x | `defineModel`, `useTemplateRef`, `useId`, reactive props destructure stable, `useShallow*` family. |
| Compiler | Vapor mode (opt-in) | Compile-to-imperative for non-VDOM perf; not yet default. |
| Nuxt | 3.x (Nitro 2) | File-based routing, server routes, hybrid rendering. |
| Build | Vite 6 + `@vitejs/plugin-vue` | See frontend-tooling skill. |
| Routing | Vue Router 4 (Nuxt uses pages/) | Lazy route components by default. |
| State | Pinia 2 | Replaces Vuex. |
| Server data (Nuxt) | `useFetch` / `useAsyncData` / server routes | SSR-aware with payload transfer. |
| Client data | TanStack Query Vue / VueUse `useFetch` | When Nuxt isn't in play. |
| Forms | VeeValidate 4 + Zod, or native + `:invalid` styles | |
| UI | Headless UI Vue, Radix Vue, Vuetify 3, Quasar 2 | |
| Testing | Vitest + Vue Test Utils + Playwright | |
| TypeScript | 5.6+, `strict: true` | Use `<script setup lang="ts">`. |

## When to Use

- Building Vue 3 components, composables, or feature modules.
- Refactoring large SFCs.
- Working on Nuxt routing, data fetching, hybrid rendering.
- Designing shared composables or Pinia stores.
- Reviewing component contracts, reactivity, and SSR boundaries.

## Instructions

### 1. Default to Composition API + `<script setup lang="ts">`

```vue
<script setup lang="ts">
import { computed, ref, useId } from "vue";

const props = defineProps<{ initialCount?: number }>();
const emit = defineEmits<{ change: [value: number] }>();

const count = ref(props.initialCount ?? 0);
const doubled = computed(() => count.value * 2);
const inputId = useId();

function increment() {
  count.value++;
  emit("change", count.value);
}
</script>

<template>
  <label :for="inputId">Count</label>
  <input :id="inputId" type="number" :value="count" @input="count = +($event.target as HTMLInputElement).value" />
  <p>Doubled: {{ doubled }}</p>
  <button type="button" @click="increment">+1</button>
</template>
```

Options API is fine in legacy code; do not mix the two styles in the same file.

### 2. Reactivity: Minimal Source State, Derive Everything Else

- `ref` for primitives and replacement-style updates; `reactive` for objects you mutate in place.
- **Computed beats watchers** for derivation. Use `watch`/`watchEffect` only for side effects (network, DOM, logging).
- Vue 3.5 supports **reactive props destructure** in `<script setup>` - safe to write `const { id } = defineProps<{ id: string }>()`.
- Use `shallowRef` / `shallowReactive` / `markRaw` for large objects you don't mutate deeply (chart data, model instances).
- `toRefs` to spread a reactive object while keeping reactivity at the property level.

```ts
const { items, query } = defineProps<{ items: Item[]; query: string }>();
const filtered = computed(() => items.filter(i => i.name.toLowerCase().includes(query.toLowerCase())));
```

Anti-patterns: a watcher that calls `.value =` to derive state (use `computed`); destructuring a `reactive()` object outside a `<script setup>` props context (loses reactivity - use `toRefs`).

### 3. Component Boundaries

Split when any of:

- The SFC exceeds ~200 lines.
- It mixes more than one concern (data fetching + form + chart).
- Two child sections need different lifecycles or `KeepAlive` behavior.

Contract:

- **Props down**, **events up** for parent-child.
- `defineModel()` for two-way binding sugar (Vue 3.4+).
- `provide`/`inject` for cross-cutting concerns within a subtree (typed via `InjectionKey<T>`); avoid as a global state replacement.
- Slots (default + named + scoped) for layout flexibility.

```vue
<script setup lang="ts">
const model = defineModel<string>({ required: true });   // <Comp v-model="search" />
</script>
<template>
  <input :value="model" @input="model = ($event.target as HTMLInputElement).value" />
</template>
```

### 4. Composables: Reusable Stateful Logic

Convention: file `useThing.ts`, returns plain object of refs/functions.

```ts
// composables/useDebouncedRef.ts
import { customRef } from "vue";
export function useDebouncedRef<T>(value: T, delay = 200) {
  let timer: number | undefined;
  return customRef<T>((track, trigger) => ({
    get() { track(); return value; },
    set(v) {
      clearTimeout(timer);
      timer = window.setTimeout(() => { value = v; trigger(); }, delay);
    },
  }));
}
```

Rules:

- Composables that subscribe to anything must clean up in `onScopeDispose` (works outside components too) or `onUnmounted`.
- Don't call composables conditionally; always at top level of `setup`/another composable.
- Prefer returning refs (consumer keeps reactivity); document if you intentionally return plain values.
- Reach for VueUse before writing one yourself - it ships dozens (`useEventListener`, `useIntersectionObserver`, `useStorage`, `useFetch`, ...).

### 5. State Management: Pinia (Not Vuex)

```ts
// stores/cart.ts
import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const useCartStore = defineStore("cart", () => {
  const items = ref<CartItem[]>([]);
  const total = computed(() => items.value.reduce((s, i) => s + i.price * i.qty, 0));
  function add(item: CartItem) {
    const existing = items.value.find(i => i.id === item.id);
    existing ? existing.qty += item.qty : items.value.push(item);
  }
  function reset() { items.value = []; }
  return { items, total, add, reset };
});
```

Rules:

- One store per bounded concept; not one global mega-store.
- Server data (lists, entities from API) should live in a query cache (TanStack Query Vue), not Pinia. Pinia is for **client state** (cart draft, UI prefs, current user).
- For SSR (Nuxt), Pinia state is serialized into the payload; keep it small.

### 6. Nuxt 3: Routing, Data, and Rendering Modes

File-based routing under `pages/`. Auto-imports for components, composables, utils. Server routes under `server/api/` and `server/routes/`.

```ts
// pages/products/[id].vue
<script setup lang="ts">
const route = useRoute();
const { data: product, error, status, refresh } = await useFetch(`/api/products/${route.params.id}`, {
  key: `product:${route.params.id}`,
  transform: (p) => ({ ...p, priceLabel: formatMoney(p.price) }),
  // server: true (default) - runs on SSR, payload transferred to client
});
</script>
<template>
  <div v-if="status === 'pending'">Loading...</div>
  <div v-else-if="error" role="alert">Failed: {{ error.message }}</div>
  <ProductDetail v-else :product="product!" />
</template>
```

`useFetch` vs `useAsyncData`:

- `useFetch(url, opts)` = `useAsyncData(key, () => $fetch(url, opts), opts)`. Use `useFetch` for HTTP, `useAsyncData` for non-HTTP work.
- Both deduplicate by `key`. Always pass an explicit `key` if the URL is dynamic.

Rendering modes (`nuxt.config.ts` `routeRules`):

```ts
export default defineNuxtConfig({
  routeRules: {
    "/": { prerender: true },                              // SSG
    "/blog/**": { isr: 3600 },                             // ISR (revalidate hourly)
    "/dashboard/**": { ssr: false },                       // SPA
    "/api/**": { cors: true, headers: { "x-foo": "bar" } },
    "/admin/**": { ssr: true, robots: false },
  },
});
```

Server-only secrets in `runtimeConfig` (private), public values in `runtimeConfig.public`. Never read `process.env` directly in components.

### 7. Server Routes (Nitro)

```ts
// server/api/products/[id].get.ts
import { z } from "zod";

const ParamsSchema = z.object({ id: z.string().uuid() });

export default defineEventHandler(async (event) => {
  const { id } = await getValidatedRouterParams(event, ParamsSchema.parse);
  const product = await useDb().product.findById(id);
  if (!product) throw createError({ statusCode: 404, statusMessage: "Not found" });
  setResponseHeader(event, "Cache-Control", "public, max-age=60, stale-while-revalidate=300");
  return product;
});
```

Validate params/body with Zod or Valibot. Use `createError` for typed errors; do not `throw new Error("...")` in handlers.

### 8. Performance

- **`v-show` vs `v-if`**: `v-show` toggles CSS (cheap toggle, paid render); `v-if` removes from tree (cheap when hidden, paid toggle).
- **`v-memo`**: cache a subtree by deps for huge static lists. Rare; measure first.
- **Lazy components**: `defineAsyncComponent(() => import("./Heavy.vue"))` plus `<Suspense>` for graceful loading.
- **Virtualize long lists**: `vue-virtual-scroller` or `@tanstack/vue-virtual` for >200 items.
- **Images**: `<NuxtImg>` / `@nuxt/image` for responsive `srcset`, modern formats, blur placeholders.
- **Hydration**: Nuxt 3 supports lazy hydration via `LazyHydrate*` components and Vue 3.5's hydration improvements; defer below-the-fold interactive parts.
- Keep computed dependencies small (they retrack on every read).
- Avoid `:key="index"` on dynamic lists - breaks identity, forces re-renders.

### 9. Accessibility

- Semantic HTML; ARIA only when no native equivalent.
- Pair every input with `<label :for>` (use `useId()` for stable IDs).
- Manage focus on route change (Nuxt: `usePageLoadingEvent` or focus the H1 in `onMounted`).
- Live regions for async toasts (`aria-live="polite"`).
- `eslint-plugin-vuejs-accessibility` in CI; Axe in unit + E2E tests.

### 10. Testing

```ts
// __tests__/Counter.test.ts
import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";
import Counter from "@/components/Counter.vue";

describe("Counter", () => {
  it("increments", async () => {
    const wrapper = mount(Counter, { props: { initialCount: 1 } });
    await wrapper.get("button").trigger("click");
    expect(wrapper.text()).toContain("2");
    expect(wrapper.emitted().change?.[0]).toEqual([2]);
  });
});
```

For Nuxt: `@nuxt/test-utils` to boot a Nuxt instance. For E2E across environments: Playwright.

## Common Pitfalls

| Anti-pattern | Why it hurts | Fix |
| --- | --- | --- |
| Watcher to derive state | Extra render, drift, missed updates | `computed` |
| Destructuring `reactive()` outside script setup | Loses reactivity | `toRefs(state)` then destructure |
| `provide`/`inject` as global state | Hidden coupling, hard to test | Pinia for shared state |
| One mega SFC for a whole feature | Hard to test/maintain | Split into smaller components + composables |
| Forgetting `key` on `<TransitionGroup>` / `v-for` | Wrong DOM reuse, animation bugs | Stable, unique keys |
| `v-html` on user input | XSS | Sanitize (DOMPurify) or render as text |
| Reading `process.env` in components | Bypasses Nuxt runtime config | `useRuntimeConfig()` |
| `useFetch` without `key` for dynamic URLs | Cache collisions | Always set `key` |
| Heavy synchronous work in computed | Recomputed on every dep read | Memoize separately or move out |
| Subscribing in composable without cleanup | Memory leak | `onScopeDispose` / `onUnmounted` |
| Storing server data in Pinia | Stale state, manual sync | Use a query cache |
| `v-show` for things that are rarely shown | Pays render cost upfront | `v-if` for rare branches |

## Output Format

When applying this skill, deliver:

1. Component boundary plan (which SFCs, which composables).
2. Reactivity model (refs vs reactive vs shallow), with rationale for non-trivial state.
3. Pinia store catalog vs query-cache split.
4. Nuxt rendering decision per route (`prerender`, `isr`, `ssr`, `spa`).
5. Data fetching plan (`useFetch` keys, server route validators).
6. A11y + perf checklist (LCP/INP/CLS targets, axe results).
7. Test plan (unit with Vitest, E2E with Playwright).

## Authoritative References

- Vue 3 docs: https://vuejs.org/
- Vue 3.5 release notes: https://blog.vuejs.org/posts/vue-3-5
- Vue Router: https://router.vuejs.org/
- Pinia: https://pinia.vuejs.org/
- Nuxt 3 docs: https://nuxt.com/docs
- Nuxt routing: https://nuxt.com/docs/getting-started/routing
- Nuxt data fetching: https://nuxt.com/docs/getting-started/data-fetching
- Nuxt rendering modes: https://nuxt.com/docs/guide/concepts/rendering
- Nitro server: https://nitro.unjs.io/
- VueUse: https://vueuse.org/
- Vue Test Utils: https://test-utils.vuejs.org/
- @nuxt/test-utils: https://nuxt.com/docs/getting-started/testing
- VeeValidate: https://vee-validate.logaretm.com/v4/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- web.dev (Web Vitals): https://web.dev/articles/vitals
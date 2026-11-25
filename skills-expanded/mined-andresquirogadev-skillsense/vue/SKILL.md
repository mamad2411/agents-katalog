# Vue Skill

You are working on a Vue 3 project. Apply these conventions.

## Composition API

- Always use the Composition API with `<script setup>` — avoid the Options API for new code.
- Declare reactive state with `ref()` for primitives and `reactive()` for objects.
- Access `ref` values via `.value` in `<script setup>`; template auto-unwraps them.
- Use `computed()` for derived values; they are cached automatically.
- Use `watch()` for side effects on reactive sources; prefer `watchEffect()` when dependencies are obvious.

## Component Design

- Use `defineProps<{ title: string; count?: number }>()` for typed props.
- Use `defineEmits<{ update: [value: string] }>()` for typed events.
- Use `defineExpose()` only when parent components need to call child methods directly.
- Prefer `v-model` over manual `emit('update:modelValue')` for two-way binding.

## Routing (Vue Router 4)

- Define routes in a typed router with `RouteRecordRaw[]`.
- Use `<RouterLink>` for navigation; `useRouter()` and `useRoute()` in `<script setup>`.
- Use route guards with `router.beforeEach()` for auth; use `meta` fields for route metadata.
- Lazy-load routes: `() => import('./views/HomeView.vue')`.

## State Management (Pinia)

- Define stores with `defineStore('id', () => { … })` (Setup syntax preferred over Options).
- Export and use stores only inside components and composables, never in plain JS modules at module scope.
- Use `storeToRefs()` to destructure reactive state without losing reactivity.

## Reactivity Pitfalls

- Destructuring a `reactive()` object breaks reactivity — use `toRefs()` first.
- Adding new properties to a `reactive()` object is fine in Vue 3 (uses Proxy), unlike Vue 2.
- Never reassign a `reactive()` variable itself; mutate properties instead.

## Templates

- Use `v-bind="$attrs"` on the root element in components that forward attributes.
- Use `:key` on `v-for` items that are unique database IDs, not array indices.
- Use `v-memo` on expensive list items to skip re-renders when data hasn't changed.

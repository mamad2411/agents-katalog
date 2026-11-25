---
name: Vue
description: Avoid common Vue mistakes — reactivity traps, ref vs reactive, computed timing, and Composition API pitfalls.
metadata: {"clawdbot":{"emoji":"💚","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

## Reactivity System
- `ref` for primitives — access with `.value` in script, auto-unwrapped in template
- `reactive` for objects — no `.value`, but can't reassign whole object
- Destructuring `reactive` loses reactivity — use `toRefs(state)` to preserve
- Array index assignment reactive in Vue 3 — `arr[0] = x` works, unlike Vue 2

## ref vs reactive
- `ref` can hold any value — including objects, `.value` always needed in script
- `reactive` only for objects — returns Proxy, same reference
- `ref` unwraps in template — `{{ count }}` not `{{ count.value }}`
- Nested refs unwrap inside reactive — `reactive({ count: ref(0) }).count` is number

## Computed and Watch
- `computed` is cached — only recalculates when dependencies change
- `computed` should be pure — no side effects, use `watch` for effects
- `watch` lazy by default — `immediate: true` for initial run
- `watchEffect` runs immediately — auto-tracks dependencies, no need to specify

## Watch Pitfalls
- Watching reactive object needs deep — `watch(state, cb, { deep: true })` or `watch(() => state.prop, cb)`
- Watch callback receives old/new — `watch(source, (newVal, oldVal) => {})`
- `watchEffect` can't access old value — use `watch` if needed
- Stop watcher with returned function — `const stop = watch(...); stop()`

## Props and Emits
- `defineProps` for type-safe props — `defineProps<{ msg: string }>()`
- Props are readonly — don't mutate, emit event to parent
- `defineEmits` for type-safe events — `defineEmits<{ (e: 'update', val: string): void }>()`
- `v-model` is `:modelValue` + `@update:modelValue` — custom v-model with `defineModel()`

## Template Refs
- `ref="name"` + `const name = ref(null)` — must match name
- Available after mount — access in `onMounted`, not setup body
- `ref` on component = component instance — `ref` on element = DOM element
- Template ref with v-for — `ref` becomes array

## Lifecycle Hooks
- `onMounted` for DOM access — component mounted to DOM
- `onUnmounted` for cleanup — subscriptions, timers
- `onBeforeMount` runs before DOM insert — rarely needed
- Hooks must be called in setup — not in callbacks or conditionals

## Provide/Inject
- `provide('key', value)` in parent — `inject('key')` in any descendant
- Reactive if value is ref/reactive — otherwise static
- Default value: `inject('key', defaultVal)` — third param for factory
- Symbol keys for type safety — avoid string collisions

## Vue Router
- `useRoute` for current route — reactive, use in setup
- `useRouter` for navigation — `router.push('/path')`
- Navigation guards: `beforeEach`, `beforeResolve`, `afterEach` — return `false` to cancel
- `<RouterView>` with named views — multiple views per route

## Common Mistakes
- Async setup needs `<Suspense>` — `async setup()` component must be wrapped
- `v-if` vs `v-show` — v-if removes from DOM, v-show toggles display
- Key on v-for required — `v-for="item in items" :key="item.id"`
- Event modifiers order matters — `.prevent.stop` vs `.stop.prevent`
- Teleport for modals — `<Teleport to="body">` renders outside component tree

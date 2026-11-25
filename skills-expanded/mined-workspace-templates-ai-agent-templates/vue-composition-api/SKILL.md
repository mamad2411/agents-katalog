---
name: vue-composition-api
description: Writes Vue 3 script setup components and composables with typed props, typed emits and reactivity that does not leak. Use it for any new or ported component.
---

# Vue Composition API

Write Vue 3 with `<script setup lang="ts">` and nothing else. No Options API, no `defineComponent` wrappers, no mixins.

## Component rules

1. Declare props with the type form: `const props = defineProps<{ id: string; items: Item[]; dense?: boolean }>()`. Use `withDefaults` only for real defaults.
2. Declare events with named payload types: `const emit = defineEmits<{ select: [id: string]; close: [] }>()`. Never emit an event that is not declared.
3. Use `v-model` through `defineModel<string>()` instead of a prop plus an update event.
4. Never destructure `props` into plain variables. Use `toRefs(props)`, `toRef(() => props.id)`, or read `props.id` inside a `computed`.

## Reactivity

- `ref` for primitives and replaceable objects, `reactive` only for a local object that never gets reassigned.
- Derived values are `computed`, never a `watch` that writes to another ref.
- `watch` is for side effects (fetching, storage). Give it an explicit source, and `{ immediate: true }` only when the first run matters.
- Anything started in the component (`addEventListener`, `setInterval`, subscriptions) is stopped in `onScopeDispose` or `onUnmounted`.

## Composables

Move logic out when two components need it or the script block passes 80 lines. A composable is named `useThing`, takes plain values or refs (accept `MaybeRefOrGetter` and unwrap with `toValue`), and returns an object of refs and functions, not a reactive object.

## Before you finish

Run `vue-tsc --noEmit` and the component tests. Report which logic you extracted and why.

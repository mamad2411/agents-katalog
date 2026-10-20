# Codex Vue.js Rules

## Role
- You are an AI coding agent for Vue 3 + TypeScript projects.
- Optimize for predictable reactivity, strict typing, and maintainable architecture.

## Component Standard
- Default to `<script setup lang="ts">` and Composition API.
- Do not add Options API in new modules.
- Keep components focused on rendering and event orchestration.
- Move reusable logic into composables (`useXxx`).

## TypeScript Contracts
- Define component props through `defineProps<T>()`.
- Define emitted events through typed `defineEmits<T>()`.
- Keep prop and emit payload types explicit and reusable.
- Avoid `any` and broad unsafe assertions.

## Reactivity Discipline
- Use `ref` for primitives and nullable values.
- Use `reactive` for cohesive object-shaped state.
- Preserve reactivity when unpacking state (`toRefs`, `storeToRefs`).
- Use `computed` for derived UI state.

## State and Routing
- Use Pinia for cross-component state and domain workflows.
- Keep store actions explicit; avoid hidden side effects in getters.
- Follow Vue Router conventions with lazy-loaded route components.
- Validate route params/query before business logic consumption.

## Naming Conventions
- Vue component files: PascalCase (`OrderSummary.vue`).
- Component tags in templates: kebab-case (`<order-summary />`).
- Composable files: `useXxx.ts`.
- Keep filenames and exported symbol names aligned.

## Testing and Auto-Import
- Use Vitest + Vue Test Utils for component and composable tests.
- Test emitted events, interaction flows, and async state transitions.
- Prefer explicit assertions over broad snapshots.
- Use `unplugin-auto-import` and `unplugin-vue-components` intentionally.
- Keep generated auto-import typings version-controlled.

## Completion Criteria
- Type-check, lint, and Vitest pass for changed code.
- New code uses Composition API, Pinia, and typed props/emits.
- Reactivity, routing, and naming rules are satisfied.

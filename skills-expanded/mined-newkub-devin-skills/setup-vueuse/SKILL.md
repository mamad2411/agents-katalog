---
name: follow-lib-vueuse-setup-vueuse
description: Install VueUse — install, auto-import integration, common composables
argument-hint: "[scope]"
related:
  - follow-lib-vueuse
  - follow-lib-vue
  - run-install
  - run-test
  - resolve-errors
---

## Goal

Install and configure VueUse in a Vue 3 project — install, auto-import integration, and the frequently used composables

## Scope

Use when setting up VueUse for the first time in a Vue 3.5+ or Nuxt project — covers install, the `@vueuse/nuxt` module, auto-import config, and a common-composables smoke test

## Execute

### 1. Install VueUse

> Goal: install `@vueuse/core` per the framework

1. Vue: `bun add @vueuse/core` — requires Vue 3.5+
2. Nuxt: `bun add -D @vueuse/nuxt` or `bunx nuxi@latest module add vueuse`, then add it to `modules` in `nuxt.config.ts`
3. If `package.json` already has VueUse → verify the version only (idempotent)
4. Check the Vue version in `package.json` is >= 3.5 — VueUse v14 requires Vue 3.5+

### 2. Setup Auto-Import (Optional)

> Goal: configure auto-import for composables

1. Nuxt: auto-imports work automatically via `@vueuse/nuxt` — no extra config needed
2. Vite: use `unplugin-auto-import` — add `VueUse` to the `imports` preset or the `vueuse` resolver per the official docs at `https://vueuse.org`
3. If you don't use auto-import → normal named imports from `@vueuse/core`
4. Merge with the existing config — never overwrite the whole `vite.config`/`nuxt.config`

### 3. Use Common Composables

> Goal: test the frequently used composables

1. State: `useLocalStorage`, `useSessionStorage`, `useAsyncState`
2. Browser: `useMediaQuery`, `useDark`, `useTitle`, `useClipboard`
3. Elements: `useWindowSize`, `useElementBounding`, `useIntersectionObserver`
4. Network: `useFetch`, `useEventSource`
5. Utilities: `useEventListener`, `onClickOutside`, `useDebounce`/`useThrottle`
6. See the full list at `https://vueuse.org/functions`

### 4. Verify

> Goal: confirm VueUse works correctly

1. Run dev — use one composable in `<script setup>` and check reactivity
2. If you use auto-import — confirm you don't need to import manually and typecheck passes
3. Do `/run-test` if there are relevant tests
4. If it breaks → do `/resolve-errors` max 3 rounds, then stop and report

## Rules

- VueUse v14 requires Vue 3.5+ — check the version before installing
- Use auto-imports or named imports — never import the whole package
- Use composables only in `<script setup>`
- Don't call composables in loops or mutable conditionals
- Use `/follow-lib-vueuse` for the full reference, v14 features, and best practices

## Expected Outcome

- `@vueuse/core` is installed and usable in Vue/Nuxt
- Auto-import works if configured, or named imports are correct
- Common composables are usable immediately
- Typecheck and the dev server pass

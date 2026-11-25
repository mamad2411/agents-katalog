---
name: follow-lib-vueuse
description: Use VueUse v15 composables per best practices
argument-hint: "[scope]"
related:
  - follow-lib-vue
  - follow-best-practice
  - use-my-packages-on-registry
  - setup-cicd

---

## Goal

Use VueUse v15 composables effectively for Vue 3.5+ applications

## Scope

For Vue 3.5+ projects using VueUse v15 — covers installation, core composables, the latest features, best practices, and testing

- Latest: `@vueuse/core@15.0.0` (verified 2026-09-24) — v15 breaking: drops Node 20, removes deprecated timer options (use `scheduler` only), `useThrottleFn` default `trailing` false→true, removes `templateRef`, `useIDBKeyval` syncs across tabs

## Execute

### 1. Setup VueUse

> Goal: install and configure VueUse in a Vue or Nuxt project

1. Install `@vueuse/core` v15+ with `bun add @vueuse/core` (v15 requires Node 22+)
2. For Nuxt, install `@vueuse/nuxt` or run `bunx nuxt@latest module add vueuse`
3. Configure the Nuxt module in `nuxt.config.ts`
4. Use auto-imports for VueUse composables
5. Declare the imports you use if you don't use auto-imports

### 2. Use VueUse Composables

> Goal: pick composables by use case from VueUse's main categories

1. State: `useLocalStorage`, `useSessionStorage`, `useAsyncState`, `useStorage`, `createSharedComposable`
2. Elements: `useElementBounding`, `useWindowSize`, `useScroll`, `useIntersectionObserver`, `useResizeObserver`
3. Browser: `useMediaQuery`, `useClipboard`, `useDark`, `useCssSupports`, `useTitle`
4. Sensors: `useMouse`, `useGeolocation`, `useNetwork`, `useDraggable`, `useDropZone`
5. Animation: `useInterval`, `useTimeout`, `useTransition`, `useRafFn`
6. Network: `useFetch`, `useWebSocket`, `useEventSource`
7. Utilities: `useSortable`, `useEventListener`, `onClickOutside`, `tryOnScopeDispose`
8. See the full details at `https://vueuse.org/functions`

### 3. Use VueUse v14.4+ Features

> Goal: use the VueUse v14.4/v15 features improved over prior versions

1. `useIntersectionObserver` supports a reactive `rootMargin` (no need to recreate the observer)
2. `useDraggable` has auto-scroll in scrollable containers
3. `useDropZone` has a validation function for file type/size
4. `useSortable` has `watchElement` to auto re-init when the DOM changes
5. `useCssSupports` for reactive CSS feature detection (new in v14)
6. `useWebSocket` supports a function for `autoConnect.delay`
7. `useElementVisibility` has an `initialValue` option
8. `useElementOverflow` to detect element overflow (new in v14.4)
9. `useSpeechRecognition` exposes the confidence of the latest result (v14.4)
10. `useVirtualList` scrollTo supports `behavior`, `block`, `inline` (v14.4)
11. Custom scheduler for time-based composables (v14.4+; v15 removes the old timer options — use `scheduler` only)
12. New in v15: `useWebMCP`, `useLiveAnnouncer`, `useTemporalNow`
13. `watchPausable` is deprecated because Vue 3.5's native `watch` has `pause/resume/stop`
14. `computedEager` is deprecated in v14 — use a plain `computed` instead

### 4. Integrate With Components

> Goal: use VueUse in components systematically and testably

1. Use VueUse in `<script setup>` components
2. Split complex logic into composables
3. Use TypeScript for type inference
4. Test composables with Vitest
5. Use the `controls` option for advanced configuration

### 5. Optimize Performance

> Goal: reduce re-renders and side-effects with VueUse utilities

1. Use `useThrottle` for scroll/resize events
2. Use `useDebounce` for input/search
3. Use `shallowRef` when you don't need deep reactivity
4. Reduce unnecessary watchers
5. Use `tryOnScopeDispose` to clean up side-effects
6. Use `effectScope` for grouped effect disposal

### Workflows

- Install + auto-import integration + common composables → `workflows/setup-vueuse/SKILL.md`

## Rules

### 1. Import Conventions

- Use auto-imports for VueUse composables
- Use named imports for composables that aren't configured
- Don't import VueUse you don't use (tree-shaking)
- VueUse v14 requires Vue 3.5+

### 2. Usage Patterns

- Use VueUse only in `<script setup>`
- Split complex logic into composables
- Use destructuring for return values
- Use `reactive()` to unwrap refs if you want object properties
- Use reactive getter arguments instead of refs (VueUse 9.0+)
- Use TypeScript types from VueUse

### 3. Authoring Guidelines

- Import Vue APIs from `"vue"`
- Use `ref` instead of `reactive` when possible
- Use `shallowRef` instead of `ref` for large data
- Use an options object as arguments for flexibility
- Use `configurableWindow` when using global variables like `window`
- Use `tryOnScopeDispose` for cleanup
- Make the `immediate` and `flush` options configurable
- Use the `isSupported` flag for Web APIs that aren't yet widely supported

### 4. Performance

- Use `useThrottle` for events
- Use `useDebounce` for inputs
- Avoid calling VueUse in loops
- Use `computed` from VueUse getters
- Use `shallowRef` for large data

### 5. VueUse Breaking Changes

- v15: requires Node 22+ (drops Node 20), Vue 3.5+
- v15: deprecated timer options removed — use `scheduler` only
- v15: `useThrottleFn` default `trailing` changed from `false` to `true`
- v15: `templateRef` removed — use Vue 3.5's `useTemplateRef`
- v14: migrated to `tsdown` and the dist files moved location (breaking)
- Deprecated alias exports — use the original function name
- `watchPausable` deprecated — use Vue 3.5 native `watch` controls
- `computedEager` deprecated — use a plain `computed`

### 6. Testing

- Mock VueUse composables in unit tests
- Use `flushPromises` for async composables
- Test composables that extend from VueUse
- Use `effectScope` for test isolation

- Use `/follow-lib-vue` if needed
- Use `/follow-best-practice` if needed
- Use `/use-my-packages-on-registry` if needed
- Use `/setup-cicd` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- VueUse v15 composables used effectively
- Clean and maintainable code
- Type safety from VueUse's TypeScript support
- Better performance with `shallowRef` and `effectScope`
- Custom composables written per the VueUse guidelines

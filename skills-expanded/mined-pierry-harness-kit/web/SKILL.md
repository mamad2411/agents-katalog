---
name: web
description: Web frontend engineering conventions for team. Vue.js stack. Project conventions in .claude/conventions/web.md override these defaults.
user_invocable: false
---

Web frontend conventions, team default.

Project override: if `{repo}/.claude/conventions/web.md` exists, overrides any rule here. See guides/conventions-override.md.

## Defaults (team frontend stack)

Stack:
- Vue 2.6 Options API. Avoid Composition API unless repo already uses Vue 3.
- Vuex with namespaced modules: `createNamespacedHelpers`.
- TMS Design System: `IpPageBase`, `IpTabs`, `IpFormField`, `IpSelect`, `IpDialog`, `IpSnackbar`.
- PrimeVue 2.10 alongside TMS in some repos.
- `@team-js` packages: `secure-components`, `secure-providers`, `secure-ui`.
- Feature folders: `/features/private`, `/features/public`.

Component order:
- data, computed, watch, created/mounted, methods, components.

Styling:
- Scoped SCSS.
- BEM-like naming.
- CSS variables for theming.

UX feedback:
- Snackbar via `this.$ipSnackbar.add()`.
- Async: `.catch()` before `.finally()`. Toast on failure.

State:
- Vuex actions for side effects, mutations for state changes.
- Getters for derived state.

Tests:
- Vitest or Jest depending on repo.
- Vue Test Utils for component tests.
- Cover happy path, error path, edge case.

## Before writing code

Read at least 3 similar components in repo to confirm:
- Vue version (2 vs 3)
- API style (Options vs Composition)
- Design system in use (TMS, PrimeVue, custom)
- State management (Vuex, Pinia, none)

Never assume.

## Forbidden in PR

- Composition API in Vue 2 repos
- Inline styles when SCSS exists
- Direct mutation of Vuex state outside mutations
- Components without tests
- console.log in production code

## Mark gaps

```vue
<!-- TBD - verify with tech lead: {what you searched, what is missing} -->
```

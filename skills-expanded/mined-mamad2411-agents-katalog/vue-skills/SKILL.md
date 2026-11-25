---
name: vue-skills
description: Vue.js framework patterns, Composition API, and best practices
category: stacks/frontend/vue
applies_to: vue
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# Vue.js Skills

Progressive JavaScript framework for building user interfaces.

## Sub-Skills

### Architecture
- [project-structure.md](architecture/project-structure.md) - Project organization
- [component-patterns.md](architecture/component-patterns.md) - Component design
- [state-management.md](architecture/state-management.md) - Pinia/Vuex patterns

### Composition API
- [setup-function.md](composition/setup-function.md) - setup() patterns
- [reactivity.md](composition/reactivity.md) - ref/reactive patterns
- [computed.md](composition/computed.md) - Computed properties
- [watchers.md](composition/watchers.md) - Watch patterns
- [composables.md](composition/composables.md) - Composable patterns

### Components
- [props-emits.md](components/props-emits.md) - Props and emits
- [slots.md](components/slots.md) - Slot patterns
- [provide-inject.md](components/provide-inject.md) - Provide/Inject
- [lifecycle.md](components/lifecycle.md) - Lifecycle hooks

### Performance
- [lazy-loading.md](performance/lazy-loading.md) - Lazy loading
- [memoization.md](performance/memoization.md) - Computed caching
- [virtual-scroll.md](performance/virtual-scroll.md) - Virtual scrolling

### Forms
- [v-model.md](forms/v-model.md) - v-model patterns
- [validation.md](forms/validation.md) - Form validation
- [vee-validate.md](forms/vee-validate.md) - VeeValidate

### Testing
- [vitest.md](testing/vitest.md) - Vitest patterns
- [vue-test-utils.md](testing/vue-test-utils.md) - Vue Test Utils
- [component-testing.md](testing/component-testing.md) - Component tests

## Detection
Auto-detected when project contains:
- `vue.config.js` or `*.vue` files
- `vue` package
- `<template>` or `createApp` patterns

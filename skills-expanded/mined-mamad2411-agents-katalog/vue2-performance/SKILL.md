---
name: vue2-performance
description: "Vue 2.x performance optimization guide with 9 core techniques. Triggers when writing, reviewing, or refactoring Vue 2.x code for: (1) component rendering optimization (2) large data list/table handling (3) route switching & page load optimization (4) reactive data tuning (5) Webpack build optimization (6) first-screen loading speed-up"
---

# Vue 2.x Performance Optimization

Based on Guillaume Chau's 9 performance secrets from Vue Conf US 2019, combined with code-level, build-level, and web technology-level best practices.

## Optimization Decision Guide

Choose optimization based on the performance bottleneck:

| Symptom | Recommended Optimization | Ref |
|---------|--------------------------|-----|
| Many simple display components render slowly | Functional components | #1 |
| Parent re-render causes child to repeat heavy computation | Child splitting / computed cache | #2 |
| Multiple reactive property access in computed | Local variable caching | #3 |
| Frequently toggled heavy components | v-show instead of v-if | #4 |
| Route switch re-initializes components | KeepAlive caching | #5 |
| Complex page first render blocks UI | Deferred progressive rendering | #6 |
| Bulk data commit freezes the page | Time slicing | #7 |
| Large data objects don't need reactivity | Non-reactive data | #8 |
| Long list scrolling is laggy | Virtual scrolling | #9 |

## 9 Core Optimization Techniques

### 1. Functional Components

Stateless display-only components should use `<template functional>`. Functional components skip component instantiation and reactivity setup, directly producing plain vnodes.

```vue
<template functional>
  <div class="cell">
    <div v-if="props.value" class="on"></div>
    <section v-else class="off"></section>
  </div>
</template>
```

Use when: component has no state, no lifecycle hooks, no reactive data.

### 2. Child Component Splitting + computed Cache

Extract heavy computation into child components or computed properties. Vue updates at component granularity - when a parent re-renders, a child with no reactive data changes won't re-render.

**Preferred: use computed for caching**

```js
computed: {
  heavyResult() {
    const n = 100000
    let result = 0
    for (let i = 0; i < n; i++) {
      result += Math.sqrt(Math.cos(Math.sin(42)))
    }
    return result
  }
}
```

### 3. Local Variable Caching for Reactive Properties

In loops or intensive computation, assign `this.xxx` to a local variable first. Each `this.xxx` access triggers the getter and dependency collection; a local variable triggers it only once.

```js
// Anti-pattern
result() {
  for (let i = 0; i < 1000; i++) {
    result += this.base * this.base + this.base
  }
}

// Optimized
result({ base, start }) {
  let result = start
  for (let i = 0; i < 1000; i++) {
    result += base * base + base
  }
}
```

### 4. Reuse DOM with v-show

For frequently toggled heavy components, prefer `v-show`. `v-if` destroys/creates components with full lifecycle on each toggle; `v-show` only toggles `display` CSS.

Note: `v-show` has higher initial render cost than `v-if` (both branches render). Only use for **frequent toggle** scenarios.

### 5. KeepAlive Component Caching

Wrap `<keep-alive>` around route views to avoid re-initialization. Caches vnode and DOM, reuses them on next render.

```vue
<keep-alive>
  <router-view />
</keep-alive>
```

Trade-off: uses more memory (space-for-time strategy).

### 6. Deferred Progressive Rendering

Split complex page rendering across multiple frames to avoid single long render blocking UI. Uses `requestAnimationFrame` to increment priority each frame.

See detailed mixin implementation: [references/deferred-mixin.md](references/deferred-mixin.md)

### 7. Time Slicing

Split bulk data commits into batches, each in a `requestAnimationFrame` callback, keeping UI responsive.

See detailed implementation: [references/time-slicing.md](references/time-slicing.md)

### 8. Non-reactive Data

Data not used in templates should not go into `data()` to avoid reactive overhead:

```js
// Method 1: Object.defineProperty with configurable: false
Object.defineProperty(itemData, 'data', {
  configurable: false,
  value: item
})

// Method 2: attach to this instead of data
export default {
  created() {
    this.scroll = null
  },
  mounted() {
    this.scroll = new BScroll(this.$el)
  }
}

// Method 3: Object.freeze for large read-only data
this.largeList = Object.freeze(data)
```

### 9. Virtual Scrolling

For lists with hundreds+ items, use virtual scrolling to only render visible DOM. Recommended: `vue-virtual-scroller`.

```vue
<recycle-scroller :items="items" :item-size="24">
  <template v-slot="{ item }">
    <ItemView :item="item" />
  </template>
</recycle-scroller>
```

## Build & Loading Optimization

See full Webpack config, CDN strategy, and first-screen optimization: [references/build-optimization.md](references/build-optimization.md)

Key points:
- **Route lazy loading**: `() => import('./views/Foo.vue')`
- **On-demand component import**: `babel-plugin-component`
- **externals + CDN**: load vue/vue-router/element-ui via CDN
- **Gzip/Brotli compression**
- **Disable production source map**
- **Image optimization**: WebP format, lazy loading, compression

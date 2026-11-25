---
name: vael-ui
description: Use whenever writing, editing, or debugging Vue 3 code that imports from "vael-ui" or "vael-ui/vapor", an animation-agnostic component library with full Vue Vapor support. Covers installation, the vdom/vapor split, auto-import, theming, the animation-agnostic contract (motionCss/forceMount/beforeClose), and imperative composables (openDialog, openPopover, confirmAction, useToast, useTour).
license: MIT
metadata:
  author: Mini-Sylar
  version: 1.0.0
---

# vael-ui `vael-ui@0.2.5`

Vue 3 component library. 62 components across Setup, Actions, Forms & Inputs, Selection, Overlays, Navigation & Menus, Feedback, Data Display, Layout & Structure, and Gestures, plus 11 standalone composables.

**References:** [Component index](./references/docs/_INDEX.md) · [Composable index](./references/composables/_INDEX.md) · [Animation integration](./references/guides/animation-integration.md) · [Auto import](./references/guides/auto-import.md) · [Styling & CSS variables](./references/guides/styling-and-layers.md)

Before writing code, check a component's own reference file for its exact current props/slots/events/exposed. The conventions below are stable, but the exact API surface is generated from the library's real types and evolves; if something here ever disagrees with a reference file, the reference file is right.

## What makes this library different

1. **Two compiled variants of every component**, from the same source: a normal Vue DOM (vdom) build and a Vue Vapor build.
2. **Animation-agnostic.** Every component that shows/hides content exposes real hooks (`motionCss`, `forceMount`, `beforeClose`, exposed element refs) so an app can swap the built-in CSS transition for GSAP, motion-v, or anything else. See [Animation integration](./references/guides/animation-integration.md) before reaching for CSS overrides or `!important` to fight a default transition.

## Install

```sh
npm install vael-ui vue   # or pnpm/yarn/bun
```

Requires Vue `^3.5.0`. The Vapor build (`vael-ui/vapor`) requires Vue `^3.6.0` and `createVaporApp`. Vapor is still pre-1.0 in Vue itself, so **pin an exact prerelease version** (e.g. `3.6.0-rc.4`), not a floating `rc`/`beta` dist-tag, to avoid a compiler/runtime mismatch between what vael-ui's Vapor build was compiled against and what's actually installed. If Vapor components render with no styles, or throw errors specifically inside `<Transition>`-wrapped components, check this first.

A Nuxt module ships as `vael-ui/nuxt`. Add it to `modules` in `nuxt.config.ts` instead of manual imports.

Auto-import via `unplugin-vue-components` is the recommended setup instead of importing every component by hand. See [Auto import](./references/guides/auto-import.md).

## API Changes

- `0.2.x`: added a `vapor` package export condition, letting a whole project resolve bare `import { X } from 'vael-ui'` to the Vapor build via `resolve.conditions`/`customConditions`, instead of importing from the `/vapor` subpath everywhere. See [Auto import](./references/guides/auto-import.md#one-shared-import-no-vapor-subpath).
- Pre-`0.2.0`: CSS wasn't split per component. Only relevant if pinned to an old version.

## Best Practices

- **Pick vdom or vapor per-project, don't mix them.** `import { Button } from 'vael-ui'` (vdom, works with `createApp`) and `import { Button } from 'vael-ui/vapor'` (works with `createVaporApp`) export identical names/props/composables; only the compiled implementation differs. Using vdom imports with `createVaporApp` (or vice versa) breaks.

  ```ts
  // vdom
  import { createApp } from 'vue'
  import { Button } from 'vael-ui'

  // vapor
  import { createVaporApp } from 'vue'
  import { Button } from 'vael-ui/vapor'
  ```

- **Don't fight the default transition with CSS.** If a component isn't animating the way an app needs, reach for `motionCss={false}` + `forceMount` + `beforeClose` (see [Animation integration](./references/guides/animation-integration.md)) before trying to override built-in transition timing via selector specificity.

  ```vue
  <Dialog ref="dialogRef" v-model:open="open" :before-close="beforeClose">
  ```

- **Theme app-wide via `ConfigProvider`, override per-instance via the `ui` prop.** Every component accepts a `ui` prop shaped like its internal part names; a part's value is either a plain class string or `{ class, style }` for cases a class alone can't express.

  ```vue
  <ConfigProvider :theme="{ primary: '#6d28d9', radius: '8px' }">
    <App />
  </ConfigProvider>

  <Dialog :ui="{ panel: 'my-custom-panel-class' }" />
  ```

  `ui` part classes concatenate with internal classes by default (no dedup). Inject a real class merger (e.g. `tailwind-merge`'s `twMerge`) via `ConfigProvider` if the project uses Tailwind and needs conflicting utilities to resolve correctly.

- **Prefer imperative composables over manual `v-model` juggling for one-off flows.** `confirmAction()`, `openDialog()`/`openPopover()`, and `toast()` all return real Promises/imperative handles. See the [composable index](./references/composables/_INDEX.md).

  ```ts
  import { confirmAction } from 'vael-ui'

  const { result } = confirmAction({
    title: 'Delete this item?',
    variant: 'danger',
    onConfirm: async () => api.delete(id),
  })
  if (await result) refresh()
  ```

- **Mind cascade layers when overriding styles.** vael-ui's CSS lives in `@layer ui-components`; an app's own *unlayered* CSS already wins by default (correct for one-off overrides), but an app's own *layered* base styles (some CSS resets are layered) need to be ordered before `ui-components` explicitly, or they'll silently lose regardless of specificity. See [Styling & CSS variables](./references/guides/styling-and-layers.md).

- **Reach for CSS variables before reaching for `ui` prop overrides on every instance.** Every color/radius/shadow/motion value is a `--ui-*` custom property. For a global change (brand color, corner radius), override the variable once instead of passing `ui` to every component instance.

- **Give a component `min-inline-size: 0` when it sits inside a shrinkable flex row/column** (a resizable panel, a narrow sidebar). A flex item's default `min-width: auto` refuses to shrink below its content's natural width — long text, an inline `<input>`, anything not already ellipsis-truncated — so without it the component (or the row causing it) overflows its container instead of shrinking or truncating to fit.

  ```css
  .my-resizable-sidebar > * {
    min-inline-size: 0;
  }
  ```

- **Give a component `flex: 1` (not the flex default) when its own responsive behavior depends on measuring its available width** — `Toolbar`'s overflow-collapse is the concrete case: it watches its own root via `ResizeObserver`. Left at the flex default (`flex: 0 1 auto`), the root only ever sizes to fit its *current* content, so once something collapses into the overflow menu, the observer never sees that more room exists and previously-collapsed items never restore after the container grows back.

## Common mistakes

- Importing from `vael-ui` while using `createVaporApp` (or the reverse).
- Using a floating `vue@rc`/`vue@beta` dist-tag with Vapor instead of an exact pinned prerelease version. Causes compiler/runtime mismatches that surface as confusing runtime errors, especially around `<Transition>`.
- Assuming `ui` prop values dedupe against internal classes automatically. They don't unless a class merger is configured.
- Reaching for `vael-ui/style.css` (the full, untreeshaken bundle) by default. Per-component CSS already loads automatically via each component's own JS import; only use the full bundle if there's a specific reason to.
- Embedding a component in a resizable/narrow flex layout without `min-inline-size: 0` — it overflows the container instead of shrinking.
- Leaving `Toolbar` (or anything else with its own `ResizeObserver`-driven behavior) at the flex default instead of `flex: 1` — its own size never reflects real available space.

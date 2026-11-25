---
name: svelte-runes-components
description: Builds Svelte 5 components with runes and snippets, and replaces stores and legacy reactive statements. Use it when writing or upgrading Svelte code.
---

# Svelte runes components

Write Svelte 5. If the file uses `export let`, `$:` or `<slot>`, convert it unless the user said to leave it.

## Rules

1. Props: `let { title, items = [], onselect }: Props = $props();` with an `interface Props` above it. Callback props replace `createEventDispatcher`.
2. Local state is `$state`. When two components need the same state, export it from a `.svelte.ts` module as an object, never as a bare reassigned primitive.
3. Anything computed from state is `$derived` (use `$derived.by` for multi-line logic). Never assign to another `$state` inside an effect to mirror a value.
4. `$effect` is the last resort: DOM measurement, third-party widgets, syncing to storage. Return a cleanup function for every listener or timer. Reading a signal after an `await` inside an effect does not track it.
5. Replace `<slot>` with `{#snippet}` and `{@render children?.()}`. Typed snippet props use `Snippet<[Item]>`.
6. Bindable props need `$bindable()` and a reason: prefer a callback.
7. Deeply mutated arrays and objects are fine in `$state` (they are proxied); use `$state.raw` for large read-only data from an API.

## Verify

Run `npx svelte-check` and fix every warning that mentions state or reactivity. Open the dev server only if the user asked.

## Report

List each legacy construct you replaced and any `$effect` you kept, with the reason it could not be `$derived`.

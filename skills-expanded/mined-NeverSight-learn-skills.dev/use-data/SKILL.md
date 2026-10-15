---
name: use-data
description: Use this skill when editing this Vue 3 project and the user wants a page or block to load data automatically, refresh when filters, tabs, pagination, or mutations change, or let a child component trigger a reload through this project's `DataLoader`, even if they do not mention `DataLoader` by name.
---

# use-data

Use this skill only for this project's `DataLoader` workflow. Follow the behavior implemented in `src/DataLoader.vue`, not generic Vue fetching patterns.

## When to use

- Add or refactor async data loading so a page or block uses `DataLoader`.
- Replace `onMounted`, `watch`, or local refresh code that fetches the same request.
- Reload after query, tab, pagination, save, delete, filter, or status changes.
- Render fetched results from the default scoped slot.
- Trigger refresh from descendants with `inject`.
- React to successful loads through the `loaded` event.

Read [REFERENCE.md](references/REFERENCE.md) only when you need the prop contract, slot shape, or a code example.

## Default workflow

1. Read the target component and identify which inputs should trigger a reload.
2. Move the fetch into one `loadData` function and pass request params as one `loadDataArgs` object.
3. Build a stable `hash` from every input that should invalidate the current result.
4. Render from slot props: `data`, `filtered-data`, `loaded`, and `reload`.
5. Use slot `reload()` by default; use `inject` only when a descendant must trigger refresh.
6. Use `filter` only for derived display data, not as a replacement for raw `data`.
7. Validate that the chosen `hash` changes whenever the effective query changes.

## Gotchas

- Prefer truthy string `hash` values; avoid `hash=false` because internal `loaded` also starts as `false`.
- `loadDataArgs` is forwarded as a single argument to `loadData`.
- `filter` changes `filtered-data`, not the raw `data` slot prop.
- `loaded` means internal state matches the current `hash`, not merely that a request once finished.
- If the parent customizes `reloaderName`, descendants must inject that exact name.
- Keep one fetch lifecycle. Do not combine `DataLoader` with parallel `onMounted`, `watch`, or local refresh requests for the same data.

## Validation

- Confirm `hash` covers every query input that should trigger reload.
- Confirm reload uses slot `reload()` or the injected reloader instead of a duplicate request path.
- Confirm templates read from slot props instead of a parallel copy of the same server state.

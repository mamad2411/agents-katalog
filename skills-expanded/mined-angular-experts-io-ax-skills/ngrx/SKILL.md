---
name: ngrx
description: Use when implementing or modifying NgRx state management in Angular applications, especially state slices, events, reducers, effects, selectors, and store registration.
author: Tomas Trajan @tomastrajan
license: copyright 2026
---

# NgRx

Use this skill for NgRx state management work in Angular applications.

## General

- **Immutable updates**: always update state immutably. Re-create objects and arrays when they change, never mutate them at any level of nesting. Prefer the JavaScript `...` spread operator and immutable array methods such as `map()`, `filter()`, and `reduce()`.

## References

- For the state management architecture and read/write boundaries, read [architecture.md](references/architecture.md).
- For state serializability, persistent state, client state, transient state, local UI state, and error modeling, read [state-modeling.md](references/state-modeling.md).
- For registering and configuring runtime checks for the global store, read [store.md](references/store.md).
- For creating state slices, sharing existing state slices between isolated lazy features by extracting them to core, and splitting state slices, read [state-slice.md](references/state-slice.md).
- For creating or changing selectors, consuming state in container components, and testing selectors, read [selectors.md](references/selectors.md).
- For implementing reducers, handling events in isolated handlers versus a single handler, and testing reducers, read [reducers.md](references/reducers.md).
- For side effects such as backend requests, navigation, deep linking, reflecting and consuming state from the URL, scrolling, loading data based on URL path parameters, and testing effects, read [effects.md](references/effects.md).
- For reading router state with NgRx router-store, registering router-store, or creating router selector factories, read [router-store.md](references/router-store.md).
- For consuming observable data sources, for example from services outside our control, and exposing the data through selectors so it is composable with the rest of the application state, read [consuming-observable-data-sources.md](references/consuming-observable-data-sources.md).

---
name: Redux Store
description: 'Use when changing Redux Toolkit slices, selectors, async services, middleware, or store setup.'
applyTo: src/store/**
---

# Redux Store

- Before adding a slice, service, or selector, search `src/store/` for existing implementations to reuse or extend.
- Follow the nearest existing slice, service, selector, and middleware patterns; the project contains both singular and plural service filenames, so do not rename them for consistency alone.
- Reuse the configured store and typed hooks from `src/store/index.ts`. Do not add another state-management library or duplicate store/API setup.
- Keep state transitions in reducers, async work in the established service/thunk modules, and state reads in selectors when that matches the feature's existing structure.
- Keep changes local to the affected feature unless a shared store contract requires otherwise.

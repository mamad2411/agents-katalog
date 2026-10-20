---
description: Centralize constants; avoid hardcoded routes/keys/event names/thresholds.
globs: "app/**/*.ts, app/**/*.tsx, components/**/*.ts, components/**/*.tsx, actions/**/*.ts, lib/**/*.ts, hooks/**/*.ts, utils/**/*.ts"
alwaysApply: false
---

## Constants and \"no magic values\" (critical)
- Avoid magic values: defaults, thresholds, timings, delays, labels, storage keys, route strings, query keys, event names.
- Create constants in `@/lib/constants/*` (feature-based modules) and optionally re-export from `@/lib/constants`.

## Never hardcode these
- localStorage/sessionStorage keys -> `STORAGE_KEYS`
- custom event names -> `CUSTOM_EVENTS`
- react-query keys -> `QUERY_KEYS`
- route strings -> `ROUTES` (see navigation rule)

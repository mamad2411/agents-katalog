---
description: Navigation rules: centralized ROUTES and navigation utilities, no hardcoded route strings.
globs: "app/**/*.tsx, lib/**/*.ts, components/**/*.tsx"
alwaysApply: false
---

## Navigation patterns

- Use centralized navigation utilities in `@/lib/navigation.ts`.
- Prefer `useNavigation()` hook over direct `router.push()` calls.
- Define all route strings in `ROUTES` for maintainability (no hardcoded strings).
- Prefer descriptive functions like `goToTimerList()` over generic `navigate()`.

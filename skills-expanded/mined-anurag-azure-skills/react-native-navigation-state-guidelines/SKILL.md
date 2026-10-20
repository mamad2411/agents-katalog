---
name: "react-native-navigation-state-guidelines"
description: "Expo Router + React Query + SessionContext for React Native: typed routes, hrefs, modals, deep links, storyRegistry. Use when wiring navigation and app state for Expo apps."
version: 2
created: "2026-06-27"
updated: "2026-07-06"
sources_merged: "anurag-azure v1; Jeffallan/react-native-expert navigation section"
---

# Expo Router Navigation & State Guidelines

## Navigation (Expo Router — default for greenfield Expo)

### File structure
```
app/
  _layout.tsx
  (family-plan)/
    _layout.tsx
    highplan-carousel.tsx
    …
```

### Wiring from TSA
- Build routes from `design_source.screens[].expo_route` and `route` (href path).
- `navigation_graph[]` + requirement per-screen `navigateTo` / `successRoute` / `ctaRoutes`:
  - Single CTA → `navigateTo` on `ScreenConfig`.
  - Multiple CTAs → `ctaRoutes: Record<label, href>` (case-insensitive label match on canvas text).
- Modals (FP-MODALS): Expo Router modal presentation; `onCancel` → `router.back()` without API call.
- Deep links: `app.json` scheme + `expo-router` linking config aligned with TSA routes.

### API
```tsx
import { router, useLocalSearchParams } from 'expo-router';

router.push('/family-plan/highplan-swipe');
router.replace('/family-plan/highplan-confirmation');
router.back();
```

### storyRegistry
Single source of truth:
```ts
{ storyId, componentName, routeName, routePath, epic }
```
Every story ID in TSA must appear; tests assert 54/54 coverage.

### React Navigation fallback
Use `@react-navigation/native-stack` only when TSA/ADR explicitly requires it (not default for Expo pipeline).

## State
- **React Query** for all server state.
- **SessionContext** for `accountNum` + JWT (injected into every API path — CONSTR-006).
- No server data in Redux/Zustand unless ADR mandates.

## Auth storage
- **expo-secure-store** via auth service shim; 401 → silent refresh → retry.

## Anti-patterns
- Untyped route strings scattered in components (centralize hrefs / registry).
- Navigating on cancel of destructive modal before ConfirmationModal gate.
- Missing modal parent stack entry.

---
name: "react-native-test-stabilization"
description: "Stabilize Expo + Jest + React Testing Library tests: jest-expo preset, expo-router mocks, QueryClient providers, screen completeness tests. Use during validation/build fix."
version: 2
created: "2026-06-27"
updated: "2026-07-06"
---

# React Native Test Stabilization (Expo + RTL)

## Setup
- Preset: **jest-expo**; `@testing-library/react-native` + `@testing-library/jest-native`.
- `jest.setup.ts`:
  - Mock `expo-router` (`router.push`, `router.back`, `useLocalSearchParams`).
  - Mock `expo-secure-store`.
  - Mock `react-native-reanimated` if used.
  - Mock axios / MSW using `tsa.api_integration` shapes.

## renderWithProviders
Wrap tests with: `QueryClientProvider`, `SessionContext`, theme if needed.

## Common failures
| Issue | Fix |
|-------|-----|
| Invalid hook call | Missing provider wrapper |
| act warnings | `findBy*`, `waitFor`, `await` mutations |
| Navigation | Spy `router.push` / `router.replace` |
| 401 / network | Mock api client; assert correct path + Bearer header |

## Screen completeness gate
- `allScreens.test.tsx`: every story ID in `storyRegistry` renders without throw.
- Per-screen: loading skeleton, empty, error, success states where applicable.
- CONSTR-004 test: delete flow — cancel must not call DELETE API.

## Gate
`tsc --noEmit` + ESLint + `npm test` / `npm run test:coverage` before VALIDATION_GATE PASS.

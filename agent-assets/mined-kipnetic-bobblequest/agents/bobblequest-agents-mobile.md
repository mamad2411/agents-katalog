# AGENTS.md — apps/mobile

Scope: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\apps\mobile\**
Routed here from the root Scope Routing Table when an agent touches apps/mobile/**.

## 1. What This Is

Expo + React Native client for the template monorepo. Ships to iOS App Store and Google Play via
EAS Build / Submit. File-based routing (expo-router), NativeWind styling, Clerk auth with
SecureStore token cache, typed tRPC v11 client against apps/api, RevenueCat for in-app purchases.

## 2. Tech Stack

| Concern       | Package / Version                                      |
| ------------- | ------------------------------------------------------ |
| Runtime       | Expo SDK ~54.0.34, New Architecture enabled            |
| RN            | react-native 0.81.5                                    |
| Navigation    | expo-router ~6.0.23 (file-based, typed routes)         |
| Styling       | NativeWind ^4.1.0 + Tailwind v3 ^3.4.0 (pinned)        |
| Auth          | @clerk/clerk-expo ^2.19.31 + expo-secure-store ~15.0.8 |
| API client    | @trpc/react-query ^11 + @tanstack/react-query ^5        |
| Billing / IAP | react-native-purchases 10.0.1 (RevenueCat)             |
| Analytics     | posthog-react-native ^4.43.5                           |
| Animations    | react-native-reanimated ~4.1.1                         |
| Tests         | Vitest ^2.1.0 + @testing-library/react-native ^13.3.3  |

NativeWind v4 requires Tailwind v3 AST output. Do NOT bump tailwindcss alongside web/website.
NativeWind v5 (Tailwind v4 compat) is planned for 2026 — stay on v4 until it ships.

## 3. Entry Points

```
app/_layout.tsx              RootLayout — ClerkProvider + Providers + Stack nav
app/index.tsx                HomeScreen — session gate, trpc.users.me
app/(auth)/login.tsx         Clerk sign-in / sign-up
app/(app)/                   Authenticated stack
src/lib/providers.tsx        QueryClient + trpc.Provider + Bearer header
src/lib/clerk.ts             Clerk instance with expo-secure-store tokenCache
src/lib/trpc.ts              createTRPCReact<AppRouter> + getTrpcUrl()
app.json                     Expo config (scheme: template, bundle IDs, plugins, newArchEnabled)
metro.config.js              withNativeWind + monorepo watchFolders
android/app/src/main/AndroidManifest.xml
```

No ios/ dir yet — use EAS Build (managed workflow) or `expo run:ios` to generate.

## 4. Run / Test / Build Commands

```
bun run dev                                              # expo start
bun run android / ios                                    # expo run:android / ios
bun run check                                            # biome check .
bun run typecheck                                        # tsc --noEmit
bun run test                                             # vitest run
bun turbo run check typecheck test --filter=@t/mobile   # from repo root

eas build  --profile development|production --platform all
eas submit --platform ios|android
eas update --branch production --message "<msg>"
```

## 5. App-Specific Conventions

- **Styling:** NativeWind v4 `className` on all RN primitives. No StyleSheet.create for new code
  unless NativeWind cannot express the style. Do not extend packages/config/tailwind.config.ts.
- **Navigation:** Groups: `(auth)` unauthenticated, `(app)` authenticated. Typed routes via
  `typedRoutes: true` in app.json experiments.
- **Secure storage:** expo-secure-store for ALL sensitive persistent data. Never AsyncStorage for
  secrets; never localStorage (web-only, crashes on RN).
- **Auth tokens:** Clerk session token via `getToken()` injected as `Authorization: Bearer` on every
  tRPC request. Auth state via `useAuth()` / `useUser()` hooks only.
- **Billing:** RevenueCat primary — `react-native-purchases` + `react-native-purchases-ui` for all
  IAP, paywall UI, and entitlement checks. Stripe is web-only — never import Stripe SDK on mobile.
- **Platform divergence:** `Platform.OS` for inline checks; `.ios.tsx` / `.android.tsx` suffixes only
  for substantial divergence (distinct layouts, native-only APIs). Comment the reason.
- **Animations:** `useNativeDriver: true` always. Reanimated worklets over JS-thread for 60-fps paths.
- **Lists:** FlatList / FlashList over .map for lists that may exceed ~20 items.
- **Deep links:** Scheme `template://`. Clerk OAuth → `template://clerk`; billing → `template://receipt`.

## 6. Banned in This Scope

- `localStorage` — web-only; crashes on RN.
- Web-only RN packages — no native code, rely on DOM APIs.
- Stripe SDK (`@stripe/stripe-react-native`, `stripe-js`) — RevenueCat handles all mobile billing.
- NativeWind v5 — pre-release as of 2026-04; breaks Tailwind v3 pipeline.
- `AsyncStorage` for secrets — use expo-secure-store.
- `any`, `@ts-ignore`, `eslint-disable` — Biome + TypeScript strict enforces.

## Links

Full architecture reference: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\docs\architecture\apps\mobile.md

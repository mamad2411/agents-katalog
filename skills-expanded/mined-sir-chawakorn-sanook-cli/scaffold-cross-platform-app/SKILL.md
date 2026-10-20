---
name: scaffold-cross-platform-app
description: Scaffolds React Native (Expo Router) and Flutter app shells — feature-first folder layout, typed navigation + deep links, client-store wiring (Zustand/Redux Toolkit/Riverpod/Bloc), platform-divergent code and native bridges (Expo config plugin/Flutter platform channel), token-driven theming with dark mode, and env/build-flavor tooling.
when_to_use: Standing up or restructuring a whole React Native (Expo) or Flutter app — choosing navigation, client state, platform-conditional code, bridging a native module, theming, and build flavors. Distinct from build-native-mobile-ui (SwiftUI/Compose screens, not RN/Flutter), manage-client-server-state (server cache/data fetching), design-token-system (the token pipeline this skill consumes), and ship-mobile-app-store-release (signing + store upload).
---

## When to Use

Reach for this skill when the request is about **standing up or reorganizing a whole RN/Flutter app**, not a single screen:

- "Set up a new Expo app with tabs + a typed navigation stack and deep links"
- "Start a Flutter app with go_router and Riverpod, organized by feature"
- "Pick state management — Redux Toolkit vs Zustand / Bloc vs Riverpod — and wire it"
- "I need iOS-only and Android-only versions of this code / an adaptive widget"
- "Bridge a native module / write an Expo config plugin / add a Flutter platform channel"
- "Apply our design tokens + dark mode across the app shell"
- "Add dev/staging/prod flavors with separate env, bundle IDs, and icons"

NOT this skill:
- A **native** iOS/Android screen in SwiftUI or Jetpack Compose (not RN/Flutter) → build-native-mobile-ui
- Building one reusable RN component in an existing tree → build-react-component
- Server-cache, fetching, optimistic updates, query invalidation → manage-client-server-state (this skill wires *client* state only)
- Designing the token **architecture/pipeline** (primitive/semantic tiers, Style Dictionary, W3C export) → design-token-system (this skill *consumes* the exported tokens)
- Pixel-matching a Figma/screenshot for a screen → implement-from-design
- Tailwind/responsive web layout → style-responsive-tailwind
- E2E flows on the running app → write-playwright-e2e
- Code signing, keystores, TestFlight/Play upload, phased rollout → ship-mobile-app-store-release
- The CI workflow that calls build/sign/upload lanes (EAS/Codemagic/Fastlane in CI) → cicd-pipeline-author
- Storing signing keys / API secrets safely → secrets-management

## Steps

1. **Pick the framework lane and don't drift mid-project.** Default to **Expo (managed) + Expo Router** for RN, **Flutter stable + go_router** for Dart. Go bare RN only when a dependency needs native build config the managed prebuild can't express.

   | Need | RN choice | Flutter choice |
   |---|---|---|
   | Standard app, OTA updates, fast start | **Expo managed** + `expo-dev-client` | Flutter stable |
   | Custom native code you control | Expo + **config plugin** (stay managed) | Flutter + plugin/FFI |
   | Native build settings Expo can't model | bare RN (`expo prebuild` then own `ios/`,`android/`) | n/a |
   | Routing | **Expo Router** (file-based, typed) | **go_router** (typed routes) |
   | New project command | `npx create-expo-app@latest -t default` | `flutter create --org com.acme app` |

   Reject React-Navigation-only (no router) for new apps: Expo Router *is* React Navigation underneath but gives file-based deep linking for free.

2. **Lay out feature-first, not type-first.** Group by domain so a feature is one deletable folder. Avoid the top-level `screens/ components/ reducers/` split — it scatters every feature across the tree.

   ```
   src/
     app/                 # Expo Router routes (file = route). Flutter: lib/routing/
       (tabs)/index.tsx   # deep link: myapp://  →  /
       (tabs)/profile.tsx
       post/[id].tsx      # myapp://post/42
       _layout.tsx        # Stack/Tabs + theme provider
     features/
       auth/  { ui/  store.ts  api.ts  types.ts }
       feed/  { ui/  store.ts  api.ts }
     shared/  { ui/  hooks/  theme/  lib/ }
     platform/            # *.ios.tsx / *.android.tsx live next to use site
   ```
   Flutter mirror: `lib/features/<x>/{presentation,application,data,domain}`, `lib/core/theme`, `lib/routing/app_router.dart`.

3. **Make routes typed and deep-linkable from day one.**
   - **Expo Router:** enable typed routes in `app.json` → `"experiments": { "typedRoutes": true }`. Set `scheme` in `app.json` (`"scheme": "myapp"`) so `myapp://post/42` resolves; for universal/app links add `expo-router` `+native-intent` or `associatedDomains`. Nest with `_layout.tsx`: a `(tabs)` group holds `<Tabs>`, a sibling `_layout` holds a `<Stack>` for modals/detail. Navigate with `router.push({ pathname: '/post/[id]', params: { id } })` — params are type-checked.
   - **go_router:** define routes once, use `GoRoute` + `context.goNamed('post', pathParameters: {'id': id})`. Configure `MaterialApp.router(routerConfig: appRouter)`. Deep links work via the platform `<intent-filter>` (Android) / `CFBundleURLTypes` (iOS) — wire `uriPrefix`/`scheme` to match the route table.

4. **Wire client state by app shape — opinionated defaults, no "it depends":**

   | App | RN | Flutter | Why |
   |---|---|---|---|
   | Small/medium, mostly local UI state | **Zustand** | **Riverpod** | Minimal boilerplate, no provider-tree gymnastics |
   | Large, many devs, time-travel/devtools, strict conventions | **Redux Toolkit** | **Bloc** | Enforced structure, traceable events, predictable reducers |
   | Server data (lists, caches, mutations) | **TanStack Query** | Riverpod `AsyncNotifier` / `dio` | Don't hand-roll cache in the store → manage-client-server-state |

   Default to **Zustand** (RN) / **Riverpod** (Flutter) unless team size or audit needs push you to RTK/Bloc. **Boundary rule:** keep *server cache* out of the global store; the store holds session, auth, theme, navigation-adjacent UI state. One `store.ts`/notifier per feature; compose at app root, never one god-store.

   ```ts
   // features/auth/store.ts — Zustand slice, typed, selector-friendly
   export const useAuth = create<AuthState>()((set) => ({
     user: null, token: null,
     signIn: async (c) => { const { user, token } = await api.login(c); set({ user, token }); },
     signOut: () => set({ user: null, token: null }),
   }));
   // read narrowly to avoid re-renders: const user = useAuth(s => s.user)
   ```

5. **Diverge by platform with the cheapest tool that works.** Escalate only as needed:
   - **One value differs:** `Platform.select({ ios: 12, android: 8, default: 8 })` or `Platform.OS === 'ios'`. Flutter: `Theme.of(context).platform == TargetPlatform.iOS` or `defaultTargetPlatform`.
   - **A whole component differs:** split files — `Button.ios.tsx` / `Button.android.tsx`; import `./Button` and Metro resolves per-platform. Flutter: `Platform.isIOS ? CupertinoButton(...) : ElevatedButton(...)`, or conditional imports for web vs native.
   - **Adaptive by design:** Flutter `Switch.adaptive`, `CupertinoIcons` on iOS; RN use a wrapper that picks the native control. Never branch on `Platform.OS` deep inside business logic — isolate divergence at the UI/platform layer.

6. **Bridge native code through the framework's official channel — never patch generated folders by hand.**
   - **Expo config plugin** (stay managed): write a plugin that mutates native config at prebuild, e.g. `withInfoPlist` / `withAndroidManifest`, register in `app.json` `"plugins": ["./plugins/with-foo"]`. For real native APIs use the **Expo Modules API** (`createModule`, Swift/Kotlin) — typed JS interface, no manual bridge boilerplate.
   - **Bare RN:** Turbo/Native Module — declare a TS spec, run Codegen, implement on iOS (Swift/ObjC) + Android (Kotlin/Java).
   - **Flutter platform channel:** `MethodChannel('com.acme/foo')` on Dart side; implement the matching handler in `AppDelegate.swift` and `MainActivity.kt`. Keep the channel name and method strings in one shared constants file so both sides can't drift.
   ```dart
   const _ch = MethodChannel('com.acme/battery');
   Future<int> level() async => await _ch.invokeMethod<int>('getLevel') ?? -1;
   ```
   After any native change run `expo prebuild --clean` (Expo) or `flutter clean` and rebuild — JS/Dart hot reload will NOT pick up native edits.

7. **Consume design tokens at the app shell; theme from them, don't hardcode.** Build the token source/pipeline with design-token-system; *this* step wires its output into RN/Flutter theming. One `theme/tokens.ts` (or `core/theme/tokens.dart`) holds colors/spacing/radii/typography. Build light+dark from the same tokens; resolve via system scheme.
   - **RN:** export a `light`/`dark` theme object keyed off tokens; read `useColorScheme()`; pass to a `ThemeProvider` (or Expo Router's `<ThemeProvider value={scheme === 'dark' ? Dark : Light}>`). Never inline hex in components — pull from theme.
   - **Flutter:** `MaterialApp(theme: lightFromTokens, darkTheme: darkFromTokens, themeMode: ThemeMode.system)`; build `ColorScheme.fromSeed(seedColor: tokens.brand)`; use `CupertinoTheme` where you ship iOS-native chrome. Dark mode = the dark token set + `themeMode`, not ad-hoc `if (isDark)` checks.

8. **Set up tooling once so the app is reproducible:**
   - **Env/flavors:** RN — `app.config.ts` reading `process.env`, build profiles in `eas.json` (`development`/`preview`/`production`), distinct `bundleIdentifier`/`package` per profile. Flutter — `--flavor dev|staging|prod` with `--dart-define-from-file=env/dev.json`, matching Xcode schemes + Android `productFlavors`. **Secrets never in `app.json`/committed `.env`** → secrets-management. **Signing certs, keystores, and store upload** are out of scope → ship-mobile-app-store-release.
   - **Fonts/assets:** RN `expo-font` `useFonts()` (or `expo-asset` preload), gate render on loaded; Flutter declare under `pubspec.yaml` `fonts:`/`assets:`.
   - **Types/lint:** TS `strict: true`, `eslint` + `eslint-config-expo`, `prettier`; Flutter `flutter analyze` + `flutter_lints`. Add a `typecheck` script (`tsc --noEmit`) to CI.
   - **Fast refresh** is on by default — if it stops working, it's almost always a non-component export or a circular import, not the bundler.

## Common Errors

- **Type-first folders (`screens/`, `reducers/`, `components/`).** Every feature smears across the tree; deleting a feature touches 6 folders. Group by feature, share only truly shared code in `shared/`.
- **One global store for everything including server data.** Caching API responses in Zustand/Redux means manual invalidation and stale UI. Put server cache in TanStack Query / Riverpod `AsyncNotifier`; keep the store for session/UI state.
- **`Platform.OS` checks buried in business logic.** Divergence leaks everywhere and is untestable. Isolate it at the UI/platform layer via `.ios`/`.android` files or `Platform.select`.
- **Editing `ios/` or `android/` by hand on a managed Expo app.** The next `prebuild` wipes it. Express native changes as a **config plugin** or Expo Module instead.
- **Native change with no rebuild.** Hot reload/Fast Refresh only reloads JS/Dart. A new native module or channel needs `expo prebuild --clean` / `flutter clean` + a fresh native build, or you'll debug a phantom "method not found."
- **Hardcoded hex colors / magic spacing.** Dark mode and rebrands become a find-and-replace. Pull every color/space/radius from the token theme; derive light+dark from one source.
- **Missing `scheme` / intent-filter, so deep links silently no-op.** Set `scheme` in `app.json` (RN) and the Android `<intent-filter>` + iOS `CFBundleURLTypes` (Flutter) to match the route table, or `myapp://post/42` opens the app to the home screen.
- **Mismatched platform-channel/method names across Dart↔native.** A typo yields a silent `MissingPluginException` at runtime. Keep channel + method strings in one shared constant referenced by both sides.
- **Same `bundleIdentifier`/`applicationId` across flavors.** Dev and prod overwrite each other on-device and can't coexist. Give each flavor a distinct id + icon + display name.
- **Untyped navigation params.** `router.push('/post/' + id)` loses type-checking and breaks on refactor. Enable typed routes (Expo) / named go_router routes and pass params as objects.

## Verify

Run on **both** an iOS simulator and an Android emulator/device — a single-platform pass proves nothing cross-platform.

1. **Boots clean both OSes:** `npx expo run:ios` and `npx expo run:android` (or `flutter run -d ios` / `-d android`) start with **no red box / no exception**, app reaches the first screen.
2. **Typed navigation + deep links:** a wrong route param fails `tsc --noEmit`/`flutter analyze`. `xcrun simctl openurl booted myapp://post/42` and `adb shell am start -a android.intent.action.VIEW -d "myapp://post/42"` both open the correct detail screen with the right id.
3. **State wiring:** an action mutates the store and exactly the subscribed components re-render (verify with a render log/devtools); unrelated screens do not. Server data lives in the query cache, not the store.
4. **Platform divergence resolves:** the `.ios`/`.android` (or adaptive) variant renders the native-looking control on each OS — confirm by screenshot, not assumption.
5. **Native bridge round-trips:** call the module/channel method on both platforms and get a real value back (not `-1`/`MissingPluginException`); confirm a rebuild was done after the native edit.
6. **Theming + dark mode:** toggle system appearance on each OS → colors/typography flip via tokens, no hardcoded color survives; no contrast regressions.
7. **Flavors:** build `dev` and `prod` → distinct bundle id + icon + name, each reading its own env, no committed secret in the bundle.
8. **Lint/types green:** `tsc --noEmit` + `eslint .` (or `flutter analyze`) pass with zero errors.

Done = the app builds and runs on iOS *and* Android, deep links and typed nav resolve on both, state/theming/native-bridge round-trip correctly per platform, and lint + typecheck are green.

---
name: react-native-expo-patterns
description: Conventions for building React Native apps with the Expo managed workflow (SDK 53+) and expo-router — navigation, styling, lists, images, offline/permissions, OTA updates, and testing. Use when writing or reviewing Expo app code or deciding whether a change forces a dev build.
---

# React Native (Expo) Patterns

Apply when working in an Expo (SDK 53+) React Native app. Stay in the managed workflow unless a hard native requirement forces otherwise.

## Workflow & navigation

- Use the **Expo managed workflow** with `expo-router` (file-based routing, mirrors Next.js conventions): `app/_layout.tsx`, `app/(tabs)/`, `app/[id].tsx`.
- Use `expo-dev-client` builds when you need custom native code, but prefer config plugins over ejecting.
- Type navigation. With expo-router, enable typed routes (`experiments.typedRoutes`) and use the generated `Href` types; avoid stringly-typed navigation.

```tsx
import { Link } from 'expo-router';
<Link href={`/product/${id}`}>Details</Link>;
```

> **Architecture gate:** Adding a native module that requires a **dev build / prebuild** (i.e. not supported by Expo Go, or needing custom native code) is a gated architecture decision. Confirm no managed/config-plugin alternative exists, then record the choice in an ADR before adding it. Swapping between Expo Go and a dev client changes the whole team's run/CI story.

## Styling & platform branching

- Use `StyleSheet.create` for static styles; keep style objects out of render. A design-token/theme layer (or NativeWind if the project uses it) beats scattered literals.
- Branch platform behavior with `Platform.OS`/`Platform.select` and platform-specific files (`.ios.tsx`, `.android.tsx`) for larger divergence.
- Respect safe areas with `react-native-safe-area-context`. Don't hardcode status-bar/notch insets.

```tsx
const styles = StyleSheet.create({
  card: { padding: 16, ...Platform.select({ ios: { shadowOpacity: 0.1 }, android: { elevation: 2 } }) },
});
```

## Lists

- Use **FlashList** (`@shopify/flash-list`) for long or dynamic lists — far better memory and scroll perf than `FlatList`. Provide `estimatedItemSize`.
- Give every item a stable `keyExtractor`; never index keys for mutable lists.
- Memoize row components and their props; keep `renderItem` referentially stable.
- Use `ScrollView` only for short, bounded content. Never map a large array inside a `ScrollView`.

## Images

- Use **`expo-image`** over RN `Image`: built-in caching, `contentFit`, placeholders, and better memory.
- Always size images explicitly; provide `placeholder` (blurhash/thumbhash) and pick `cachePolicy` deliberately.
- Serve appropriately sized assets; don't ship 4000px images into 100px thumbnails.

## Offline & permissions

- Request permissions lazily, in context, right before the feature needs them; explain why first. Handle denied/undetermined states gracefully.
- Use `expo-secure-store` for tokens/secrets, `AsyncStorage`/MMKV for non-sensitive cache.
- Design for offline: cache reads, queue writes, reconcile on reconnect (`@react-native-community/netinfo` to detect state). Show clear offline UI.

## OTA updates vs store releases

- **`expo-updates` (OTA)** for JS/asset changes only — bug fixes, copy, styling. Ship behind release channels/branches; test on a canary before promoting.
- **Store release (new build)** is required for any native change: new native modules, SDK upgrades, permission/entitlement changes, app config that affects the binary.
- Never OTA a JS bundle that assumes native code not present in the installed binary — it will crash on launch.

## Testing

- Unit/component: **Jest + React Native Testing Library**. Query by accessibility role/label; test behavior, not internals.
- Mock native modules at the module boundary; keep tests off the device.
- E2E: **Maestro** for user flows (simple YAML flows, resilient selectors). Run on CI against a simulator/emulator.
- Type-check and lint in CI; treat `react-hooks/exhaustive-deps` as an error.

## Anti-patterns to flag

- Mapping large data into `ScrollView`/`FlatList` where FlashList belongs.
- Inline styles/functions recreated each render in list rows.
- Requesting all permissions at launch.
- OTA-shipping code that needs newer native code than the installed binary.
- Storing tokens in AsyncStorage instead of SecureStore.
- Blocking the JS thread with heavy synchronous work — offload or defer.

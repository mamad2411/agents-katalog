---
name: animations
description: Animation standards for React Native / Expo projects. Covers react-native-reanimated for UI motion, Rive for illustration/splash animations, and rules for when to use each. Use when building animated components, transitions, gestures, or splash screens.
---

Apply the following animation standards to all code in this project.

## Libraries

| Library | Package | When to use |
| --- | --- | --- |
| Reanimated | `react-native-reanimated` | UI motion: layout transitions, gestures, shared element transitions, scroll-driven effects |
| Rive | `rive-react-native` | Illustration-quality animations: splash screen, onboarding, lottie-style playback from `.riv` files |

Never use the built-in `Animated` API from React Native — always prefer Reanimated.

## react-native-reanimated

Install via Expo:

```bash
yarn expo install react-native-reanimated
```

Add the Babel plugin in `babel.config.js` — it must be last:

```js
plugins: ['react-native-reanimated/plugin'],
```

### Core patterns

**Layout animation (enter/exit):**

```tsx
import Animated, { FadeIn, FadeOut, LinearTransition } from 'react-native-reanimated';

<Animated.View entering={FadeIn.duration(200)} exiting={FadeOut.duration(150)} layout={LinearTransition}>
  {children}
</Animated.View>
```

**useAnimatedStyle + useSharedValue:**

```tsx
import Animated, { useSharedValue, useAnimatedStyle, withSpring } from 'react-native-reanimated';

const scale = useSharedValue(1);
const animatedStyle = useAnimatedStyle(() => ({ transform: [{ scale: scale.value }] }));

// Trigger: scale.value = withSpring(1.05);
```

**Gesture handler (press feedback):**

```tsx
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import Animated, { useSharedValue, useAnimatedStyle, withSpring } from 'react-native-reanimated';

const scale = useSharedValue(1);
const style = useAnimatedStyle(() => ({ transform: [{ scale: scale.value }] }));

const tap = Gesture.Tap()
  .onBegin(() => { scale.value = withSpring(0.96); })
  .onFinalize(() => { scale.value = withSpring(1); });

<GestureDetector gesture={tap}>
  <Animated.View style={style}>{children}</Animated.View>
</GestureDetector>
```

### Rules

- All animated values must live in `useSharedValue` — never in `useState`
- Never read `.value` on the JS thread inside render — only inside `useAnimatedStyle` or `runOnJS` callbacks
- Prefer built-in presets (`FadeIn`, `SlideInRight`, `ZoomIn`) over custom worklets for standard transitions
- Durations: enter 200–300 ms, exit 100–200 ms, spring stiffness 120–180 for snappy feel
- **Don't keep an animated overlay persistently mounted at the root** — conditionally render it (see the Fabric gotcha below). A persistent reanimated sibling of the navigator can crash during navigation.

### Fabric gotcha: don't keep an animated overlay mounted at the root

On the new architecture (Fabric), a persistent reanimated view mounted high in
the tree — e.g. a status/offline banner rendered as a sibling of the navigator
and merely translated off-screen when idle — can crash with:

```
IllegalStateException: The specified child already has a parent
  → addViewAt: failed to insert view [x] into parent [y] at index 0
  (culprit: ReactClippingViewManager)
```

It fires when the surface re-mounts on a **navigation or native-activity
transition** (pushing a screen, "continue as guest", or returning from a native
activity like Google Sign-In): Fabric replays the mount items and races on the
always-present animated sibling. The crash class simply won't appear until you
add that persistent root-level animated view — then it's intermittent and hard
to reproduce.

Fix: **conditionally mount overlays — render `null` when there's nothing to
show** so the view is absent from the tree during those transitions, and let the
enter/exit animation run only when it's actually needed:

```tsx
// ❌ persistent: mounted even when idle, just slid off-screen — reparented on transitions
<Animated.View style={[styles.banner, offscreenWhenIdleStyle]} />

// ✅ conditional: absent from the tree while idle; enter/exit runs only on the state change
if (mode === 'hidden') return null;
return (
  <Animated.View entering={enter} exiting={exit} pointerEvents="none" style={styles.banner}>
    …
  </Animated.View>
);
```

Bonus: because the enter/exit now runs only on the state change that reveals the
overlay (never during navigation), you also avoid a class of "flash then crash"
on resume. For a top strip, prefer a **custom worklet** that slides exactly the
banner's own height — the built-in `SlideInUp`/`SlideOutUp` travel a full window
height, so a 30 px strip snaps in only at the very end.

## Rive

Rive files (`.riv`) go in `assets/animations/`. Import and play:

```tsx
import Rive, { Fit, Alignment } from 'rive-react-native';

<Rive
  resourceName="splash"   // assets/animations/splash.riv
  fit={Fit.Cover}
  alignment={Alignment.Center}
  autoplay
/>
```

Use state machines for interactive Rive animations — pass `stateMachineName` and control inputs via the `RiveRef`.

### Splash screen pattern

For the app splash screen, use `@anicca-labs/react-native-splash-view` (wraps `rive-react-native`) in `app/_layout.tsx`:

```tsx
import { SplashView } from "@anicca-labs/react-native-splash-view";
import { Platform } from "react-native";
import splash from "../assets/animations/splash.riv";

<SplashView
  source={splash}
  style={{ backgroundColor: themes[colorScheme].splashBackground }}
  animationViewStyle={Platform.OS === "android" ? { width: 288, height: 288, alignSelf: "center" } : undefined}
  fadeOutDelay={1500}
  fadeOutDuration={500}
/>
```

Place `SplashView` as the last child inside `QueryClientProvider` (outside all navigation providers) so it overlays the entire screen. The 288dp `animationViewStyle` is Android-only — it matches the 288dp Android 12+ native splash icon clip limit for a seamless transition.

**Critical:** never gate `SplashView` behind a `fontsLoaded` check. Only gate the navigation/content behind it — `SplashView` must render on the very first React render so it covers the screen before the native overlay is dismissed:

```tsx
// ✅ correct
if (!fontsLoaded) return null; // ← remove this early return

return (
  <QueryClientProvider ...>
    ...
    {fontsLoaded ? <RootLayoutNav /> : null}  // ← gate content, not SplashView
    <SplashView ... />
  </QueryClientProvider>
);
```

Gating `SplashView` on font load causes a visible flash of the unstyled root view between native splash dismissal and the JS overlay appearing.

**Testing splash without a dev client:** the dev client loads the JS bundle over Metro (~1s), which amplifies any native overlay flash and is not representative of production. Use embedded-bundle builds to test splash behavior accurately:

Add to `eas.json`:

```json
"preview-simulator": {
  "distribution": "internal",
  "ios": { "simulator": true }
}
```

Add to `package.json` scripts:

```json
"build-sim": "yarn pre-build && doppler run ... -- eas build --platform ios --profile preview-simulator --local",
"build-sim:prd": "ENV=prd yarn build-sim",
"build-ipa": "yarn pre-build && doppler run ... -- eas build --platform ios --profile preview --local",
"build-ipa:prd": "ENV=prd yarn build-ipa"
```

After `build-sim` finishes, install on the running simulator:

```sh
tar -xf <output.tar.gz>
xcrun simctl install booted <path-to.app>
xcrun simctl launch booted <bundle-id>
```

## ReanimatedSwipeable (swipe-to-delete)

Use `ReanimatedSwipeable` from `react-native-gesture-handler/ReanimatedSwipeable` for swipe-to-reveal action rows (e.g. delete). Requires `GestureHandlerRootView` at the app root (already present in `app/_layout.tsx`).

```tsx
import ReanimatedSwipeable from 'react-native-gesture-handler/ReanimatedSwipeable'
import { useRef, type ComponentRef } from 'react'

const ref = useRef<ComponentRef<typeof ReanimatedSwipeable>>(null)

<ReanimatedSwipeable
  ref={ref}
  renderRightActions={() => <DeleteAction onPress={confirmDelete} />}
  rightThreshold={60}
>
  <RowContent />
</ReanimatedSwipeable>
```

**Put the handler on the action, not `onSwipeableOpen`.** Wire `onPress` directly to the action button so the user taps to confirm after swiping. `onSwipeableOpen` fires the moment the swipe threshold is crossed — before the user taps anything.

```tsx
// ✅ correct — tap the revealed button to confirm
const DeleteAction = ({ onPress }: { onPress: () => void }) => (
  <BaseTouchable onPress={onPress} bg="$red10" justify="center" items="center" width={72} rounded="$4">
    <Ionicons name="trash-outline" size={22} color="white" />
  </BaseTouchable>
)
```

**Direction gotcha.** If you do use `onSwipeableOpen`, the `direction` parameter is the side that opened, not the swipe direction — they are opposite:

| User swipes | Side that opens | `direction` value |
| --- | --- | --- |
| left | right actions | `'left'` |
| right | left actions | `'right'` |

```tsx
// ✅ right actions (renderRightActions) → direction is 'left'
onSwipeableOpen={(direction) => {
  if (direction !== 'left') return
  handleDelete()
}}
```

**Tab navigator conflict.** `MaterialTopTabNavigator` with `swipeEnabled: true` intercepts horizontal swipes before `ReanimatedSwipeable` can handle them. Disable tab swiping on any screen that contains swipeable rows:

```tsx
<MaterialTopTabs.Screen
  name="reflections"
  options={{
    swipeEnabled: false,   // lets ReanimatedSwipeable win the gesture
    title: t`Reflections`,
  }}
/>
```

This works because `MaterialTopTabView` reads `focusedOptions.swipeEnabled` and passes it to the underlying `TabView`/`PagerView` when the screen is active.

## When to use which

| Use case | Library |
| --- | --- |
| Button press feedback | Reanimated gesture |
| Modal / sheet enter-exit | Reanimated layout preset |
| Scroll-driven header collapse | Reanimated scroll handler |
| Shared element between screens | Reanimated shared transition |
| Splash / onboarding illustration | Rive |
| Loading skeleton shimmer | Reanimated (loop worklet) |
| Lottie-style branded animation | Rive (preferred over Lottie) |

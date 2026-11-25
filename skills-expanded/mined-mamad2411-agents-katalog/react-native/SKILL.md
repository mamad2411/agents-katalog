---
name: "react-native"
description: "- Building React Native apps with Expo managed or bare workflow"
---

# React Native and Expo

## When to activate
- Building React Native apps with Expo managed or bare workflow
- Configuring EAS Build and EAS Update (OTA)
- Setting up React Navigation with nested navigators
- Implementing animations with Reanimated 2
- Adding or debugging native modules
- Choosing between managed and bare workflow

## When NOT to use
- Flutter or other non-React Native mobile frameworks
- Pure React web applications (use the standard React skill)
- Expo Snack one-offs that will never leave the browser sandbox

## Instructions

### Managed vs Bare Workflow

**Managed workflow** — Expo manages the native layer. No `ios/` or `android/` directories in the repo. Native functionality comes from Expo SDK modules and config plugins.

Choose managed when:
- All required native modules exist in the Expo SDK
- The team has no native iOS/Android experience
- You want zero-setup local development (`npx expo start`)
- OTA updates (EAS Update) are a priority

**Bare workflow** — React Native project with full native code exposed. Generated via `npx expo eject` or `npx create-expo-app --template bare`.

Choose bare when:
- A required native library has no Expo config plugin
- Custom native code must be written in Swift/Kotlin
- Fine-grained control over `Podfile`, Gradle, or `AndroidManifest.xml` is needed

In managed workflow, use config plugins in `app.json`/`app.config.js` to modify native code at build time without ejecting:

```js
// app.config.js
export default {
  expo: {
    name: "MyApp",
    plugins: [
      ["expo-camera", { cameraPermission: "Allow MyApp to use the camera." }],
      ["expo-location", { locationWhenInUsePermission: "Used for delivery tracking." }],
      "./plugins/withCustomAndroidManifest.js",   // custom config plugin
    ],
  },
};
```

### React Navigation 6 — Nested Navigators

```jsx
// navigation/RootNavigator.tsx
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab   = createBottomTabNavigator<TabParamList>();

function TabNavigator() {
  return (
    <Tab.Navigator screenOptions={{ headerShown: false }}>
      <Tab.Screen name="Home"   component={HomeScreen} />
      <Tab.Screen name="Orders" component={OrdersScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}

export function RootNavigator() {
  const { isSignedIn } = useAuth();

  return (
    <NavigationContainer>
      <Stack.Navigator>
        {isSignedIn ? (
          <>
            <Stack.Screen name="Tabs"        component={TabNavigator} options={{ headerShown: false }} />
            <Stack.Screen name="OrderDetail" component={OrderDetailScreen} />
            <Stack.Screen name="Settings"    component={SettingsScreen} />
          </>
        ) : (
          <>
            <Stack.Screen name="Login"    component={LoginScreen}    options={{ headerShown: false }} />
            <Stack.Screen name="Register" component={RegisterScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

Type the param list for type-safe navigation:

```ts
// navigation/types.ts
export type RootStackParamList = {
  Tabs: NavigatorScreenParams<TabParamList>;
  OrderDetail: { orderId: string };
  Settings: undefined;
};

export type TabParamList = {
  Home: undefined;
  Orders: undefined;
  Profile: undefined;
};

// In a screen component
const navigation = useNavigation<NativeStackNavigationProp<RootStackParamList, "OrderDetail">>();
navigation.navigate("OrderDetail", { orderId: "42" });
```

### Reanimated 2 — useAnimatedStyle

All animation worklets run on the UI thread, not the JS thread. Never access React state or refs directly inside worklets.

```jsx
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
  interpolate,
  Extrapolation,
} from "react-native-reanimated";
import { Gesture, GestureDetector } from "react-native-gesture-handler";

function SwipeableCard() {
  const translateX = useSharedValue(0);
  const opacity    = useSharedValue(1);

  const panGesture = Gesture.Pan()
    .onUpdate((e) => {
      translateX.value = e.translationX;
      opacity.value = interpolate(
        Math.abs(e.translationX),
        [0, 150],
        [1, 0.5],
        Extrapolation.CLAMP,
      );
    })
    .onEnd(() => {
      if (Math.abs(translateX.value) > 100) {
        translateX.value = withTiming(translateX.value > 0 ? 400 : -400);
        opacity.value = withTiming(0);
      } else {
        translateX.value = withSpring(0);
        opacity.value = withTiming(1);
      }
    });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: translateX.value }],
    opacity: opacity.value,
  }));

  return (
    <GestureDetector gesture={panGesture}>
      <Animated.View style={[styles.card, animatedStyle]}>
        {/* card content */}
      </Animated.View>
    </GestureDetector>
  );
}
```

Use `runOnJS(fn)(args)` inside worklets when you must call a JS function (e.g., updating React state after animation completes).

### Expo SDK Key Modules

| Module | Purpose |
|---|---|
| `expo-camera` | Camera access with `useCameraPermissions` hook |
| `expo-location` | GPS / geolocation with `requestForegroundPermissionsAsync` |
| `expo-notifications` | Push notifications, local notifications, badges |
| `expo-secure-store` | Keychain/Keystore for secrets and tokens |
| `expo-file-system` | Read/write to device filesystem |
| `expo-image-picker` | Gallery and camera photo/video selection |
| `expo-av` | Audio and video playback |
| `expo-sqlite` | SQLite database |
| `expo-haptics` | Haptic feedback (iOS Taptic Engine + Android vibration) |
| `expo-constants` | App version, device info, Expo config at runtime |

### EAS Build — eas.json Profile Structure

```json
{
  "cli": {
    "version": ">= 10.0.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": { "simulator": true },
      "env": {
        "APP_ENV": "development",
        "API_URL": "http://localhost:3000"
      }
    },
    "preview": {
      "distribution": "internal",
      "channel": "preview",
      "env": {
        "APP_ENV": "staging",
        "API_URL": "https://api.staging.example.com"
      }
    },
    "production": {
      "distribution": "store",
      "channel": "production",
      "autoIncrement": true,
      "env": {
        "APP_ENV": "production",
        "API_URL": "https://api.example.com"
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "team@example.com",
        "ascAppId": "1234567890",
        "appleTeamId": "ABCDE12345"
      },
      "android": {
        "serviceAccountKeyPath": "./google-services-key.json",
        "track": "internal"
      }
    }
  }
}
```

Build commands:
```bash
eas build --platform ios --profile development
eas build --platform android --profile preview
eas build --platform all --profile production
eas submit --platform ios --profile production
```

### OTA Update Strategy

EAS Update delivers JavaScript and asset changes without a store release. Native code changes always require a new build.

```bash
# Publish an update to the preview channel
eas update --channel preview --message "Fix cart total display"

# Publish to production
eas update --channel production --message "v2.1.1 hotfix"
```

In `app.json`, configure the update runtime version policy:

```json
{
  "expo": {
    "runtimeVersion": {
      "policy": "sdkVersion"
    },
    "updates": {
      "url": "https://u.expo.dev/<project-id>",
      "fallbackToCacheTimeout": 3000
    }
  }
}
```

`sdkVersion` policy: updates are compatible as long as the Expo SDK version is the same. Use `nativeVersion` policy for tighter control — only compatible when both SDK and native code version match.

For critical updates, force an immediate reload:

```js
import * as Updates from "expo-updates";

async function checkForUpdate() {
  const update = await Updates.checkForUpdateAsync();
  if (update.isAvailable) {
    await Updates.fetchUpdateAsync();
    await Updates.reloadAsync();
  }
}
```

## Example

A feed screen with pull-to-refresh using Reanimated and EAS Update:

```jsx
// screens/FeedScreen.tsx
import Animated, { useAnimatedScrollHandler, useSharedValue } from "react-native-reanimated";
import { FlatList, RefreshControl } from "react-native";
import { useQuery } from "@tanstack/react-query";

export function FeedScreen() {
  const scrollY = useSharedValue(0);
  const [refreshing, setRefreshing] = React.useState(false);

  const { data, refetch } = useQuery({
    queryKey: ["feed"],
    queryFn: () => fetchFeed(),
  });

  const onRefresh = async () => {
    setRefreshing(true);
    await refetch();
    setRefreshing(false);
  };

  const scrollHandler = useAnimatedScrollHandler((e) => {
    scrollY.value = e.contentOffset.y;
  });

  return (
    <Animated.FlatList
      data={data ?? []}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <FeedCard item={item} />}
      onScroll={scrollHandler}
      scrollEventThrottle={16}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    />
  );
}
```

Deploy update after fixing a feed bug:
```bash
eas update --channel production --message "Fix feed infinite scroll crash"
```

---

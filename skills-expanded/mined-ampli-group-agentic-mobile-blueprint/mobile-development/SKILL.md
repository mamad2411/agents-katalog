---
name: mobile-development
description: React Native mobile app development patterns with Expo 54, Tamagui, and expo-router. Use when creating screens, components, or navigation in the mobile app.
---

# Mobile Development

## Stack

Expo 54, React Native 0.81, expo-router (file-based routing), Tamagui v4 (UI), TypeScript strict mode.

## Local Build Prerequisites

Required to run `expo run:android` or `expo prebuild`:

| Requirement | Check | Install |
|---|---|---|
| Java JDK 17 | `java -version` (must show `17.x`) | `brew install openjdk@17` |
| Android SDK | `echo $ANDROID_HOME` (must be set) | `mise run install` |

If `expo run:android` fails with a Java error:
```bash
brew install openjdk@17
export JAVA_HOME="$(brew --prefix openjdk@17)/libexec/openjdk.jdk/Contents/Home"
export PATH="$JAVA_HOME/bin:$PATH"
```

If `expo run:android` fails with `ANDROID_HOME not set` or SDK not found:
```bash
export ANDROID_HOME="$HOME/Library/Android/sdk"
export PATH="$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools:$PATH"
```

Both are set permanently by `mise run install`. If missing, re-run it or add to `~/.zshrc` manually.

iOS builds require Xcode (App Store). No additional toolchain needed beyond Xcode.

## Imports

Use `@/` path alias for project root: `@/lib/supabase`, `@/lib/posthog`.

## UI Components

Use Tamagui components with shorthand props. Never use raw React Native `View`/`Text`.

```tsx
// ✅
import { YStack, XStack, Text, Button, Card, Spinner, ScrollView } from 'tamagui';

<YStack gap="$4" p="$4">
  <Text fos="$6" fow="bold">Title</Text>
  <Button>Action</Button>
</YStack>

// ❌
import { View, Text } from 'react-native';
```

Common shorthand: `bg` (background), `p`/`px`/`py` (padding), `m`/`mt` (margin), `br` (borderRadius), `bw` (borderWidth), `boc` (borderColor), `fos` (fontSize), `fow` (fontWeight), `col` (color), `ai` (alignItems), `jc` (justifyContent), `gap`, `elevate`, `bordered`.

## Routing

File-based via expo-router:
- `app/_layout.tsx` — layout wrappers (Stack, Tabs)
- `app/index.tsx` — home screen
- `app/settings.tsx` — named route

Use `Stack` with `headerShown: false` (current convention).

## New Screen

```tsx
import { YStack, Text } from 'tamagui';

export default function MyScreen() {
  return (
    <YStack f={1} ai="center" jc="center" bg="$background">
      <Text>My Screen</Text>
    </YStack>
  );
}
```

## Supabase

```tsx
import { supabase } from '@/lib/supabase';
```

Single shared client. Uses `EXPO_PUBLIC_SUPABASE_URL` and `EXPO_PUBLIC_SUPABASE_PUBLISHABLE_KEY`.

## Theme

Default theme is `dark`. TamaguiProvider wraps the app in `_layout.tsx` with `defaultTheme="dark"`.

## Environment Variables

All public config uses `EXPO_PUBLIC_*` prefix. Access via `process.env.EXPO_PUBLIC_*`.

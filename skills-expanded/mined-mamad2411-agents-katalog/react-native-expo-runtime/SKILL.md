---
name: "react-native-expo-runtime"
description: "Expo SDK runtime: expo doctor, Metro bundler, native builds, FlatList performance, KeyboardAvoidingView, platform splits. Merged from Jeffallan/react-native-expert. Use during Impl and Build Fix agents."
version: 1
created: "2026-07-06"
updated: "2026-07-06"
license_note: "Patterns merged from MIT-licensed Jeffallan/claude-skills react-native-expert"
---

# React Native Expo Runtime

Senior mobile engineer patterns for **production Expo** apps. Use alongside `react-native-best-practices` and `react-native-component-scaffold`.

## Core workflow
1. **Setup** — Expo Router, TypeScript strict → run `npx expo doctor`; fix SDK mismatches before coding.
2. **Structure** — feature-based `app/(feature)/` + `src/` support code.
3. **Implement** — platform-aware components; verify Metro clean.
4. **Optimize** — FlatList, memo boundaries, image sizing.
5. **Verify** — `npx tsc --noEmit`; `npx expo export --platform web` when build server available.

## Error recovery
| Symptom | Fix |
|---------|-----|
| Metro bundler errors | `npx expo start --clear` |
| iOS build fails | Check Xcode logs; `npx expo run:ios` after `npx expo install` |
| Android build fails | Gradle/SDK versions; `npx expo run:android` |
| Native module not found | `npx expo install <package>` then rebuild |

## FlatList (member lists)
```tsx
const ListItem = memo(({ title, onPress }: { title: string; onPress: () => void }) => (
  <Pressable onPress={onPress} accessibilityRole="button">
    <Text>{title}</Text>
  </Pressable>
));

const renderItem = useCallback(
  ({ item }: { item: Item }) => <ListItem title={item.title} onPress={() => handlePress(item.id)} />,
  [handlePress],
);

<FlatList
  data={members}
  keyExtractor={(item) => item.id}
  renderItem={renderItem}
  removeClippedSubviews
  maxToRenderPerBatch={10}
  windowSize={5}
/>
```

## Forms
- `KeyboardAvoidingView` with `behavior={Platform.OS === 'ios' ? 'padding' : 'height'}`.
- `keyboardShouldPersistTaps="handled"` on scroll containers with inputs.

## Platform styling
Use `Platform.select` for shadow (iOS) vs `elevation` (Android) — values still from theme where possible.

## MUST DO
- FlatList for long lists (not ScrollView + map).
- `memo` + `useCallback` on list hot paths.
- Safe area on full-screen layouts.
- Test both platforms for navigation back behavior.

## MUST NOT
- `ScrollView` for unbounded member lists.
- Inline style objects in list items (use StyleSheet).
- `waitFor`/`setTimeout` for animations — use Reanimated when animations required.
- `react-native-keychain` on Expo managed workflow (use expo-secure-store).

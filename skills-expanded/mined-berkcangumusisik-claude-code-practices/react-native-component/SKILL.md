---
name: react-native-component
description: Generates a React Native component with platform-specific styles and accessibility
argument-hint: <ComponentName> [description]
user-invocable: true
allowed-tools: Read Glob Edit
effort: medium
---

## Generate React Native Component

Component: **$1**
Description: **$2**

1. Detect stack:
```bash
cat package.json | grep -E '"react-native"|"expo"|"nativewind"|"@shopify/restyle"|"tamagui"'
ls src/components/ components/ 2>/dev/null | head -5
```

2. Read 1-2 existing components to match patterns.

3. Generate the component:

```tsx
import { StyleSheet, Text, TouchableOpacity, Platform } from 'react-native'

interface $1Props {
  label: string
  onPress: () => void
  disabled?: boolean
}

export function $1({ label, onPress, disabled }: $1Props) {
  return (
    <TouchableOpacity
      style={[styles.container, disabled && styles.disabled]}
      onPress={onPress}
      disabled={disabled}
      accessible
      accessibilityRole="button"
      accessibilityLabel={label}
      accessibilityState={{ disabled }}
    >
      <Text style={styles.label}>{label}</Text>
    </TouchableOpacity>
  )
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    borderRadius: 8,
    ...Platform.select({
      ios: { shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1 },
      android: { elevation: 2 },
    }),
  },
  // ...
})
```

4. Include:
   - Accessibility props (`accessibilityRole`, `accessibilityLabel`, `accessibilityState`)
   - Platform-specific styles (`Platform.select`)
   - Proper hitSlop for small touch targets
   - Dark mode support with `useColorScheme` if project uses it

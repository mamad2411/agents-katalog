---
name: expo-app-design
slug: expo-app-design
description: Build robust, productivity apps with Expo. Covers UI building, API routes, data fetching, navigation, styling, and Expo Router best practices.
version: 1.0.0
category: mobile-development
complexity: complex
author: "Evan Bacon (Expo)"
license: MIT
triggers:
  - "expo app"
  - "expo router"
  - "expo ui"
  - "react native expo"
  - "expo navigation"
  - "expo styling"
  - "expo api routes"
tags:
  - expo
  - react-native
  - mobile
  - ios
  - android
  - expo-router
---

# Expo App Design


## Core Workflows

### Workflow 1: Primary Action
1. Analyze the input and context
2. Validate prerequisites are met
3. Execute the core operation
4. Verify the output meets expectations
5. Report results

Build robust, productivity apps with Expo. This skill covers the complete guide for building beautiful apps with Expo Router including fundamentals, styling, components, navigation, animations, patterns, and native tabs.

## References

Consult these resources as needed:

- ./references/building-ui.md -- Complete UI guidelines for Expo Router apps
- ./references/api-routes.md -- API routes with EAS Hosting

## Running the App

**CRITICAL: Always try Expo Go first before creating custom builds.**

Most Expo apps work in Expo Go without any custom native code. Before running `npx expo run:ios` or `npx expo run:android`:

1. **Start with Expo Go**: Run `npx expo start` and scan the QR code with Expo Go
2. **Check if features work**: Test your app thoroughly in Expo Go
3. **Only create custom builds when required** - see below

### When Custom Builds Are Required

You need `npx expo run:ios/android` or `eas build` ONLY when using:

- **Local Expo modules** (custom native code in `modules/`)
- **Apple targets** (widgets, app clips, extensions via `@bacons/apple-targets`)
- **Third-party native modules** not included in Expo Go
- **Custom native configuration** that can't be expressed in `app.json`

### When Expo Go Works

Expo Go supports a huge range of features out of the box:

- All `expo-*` packages (camera, location, notifications, etc.)
- Expo Router navigation
- Most UI libraries (reanimated, gesture handler, etc.)
- Push notifications, deep links, and more

## Code Style

- Be cautious of unterminated strings. Ensure nested backticks are escaped
- Always use import statements at the top of the file
- Always use kebab-case for file names, e.g. `comment-card.tsx`
- Always remove old route files when moving or restructuring navigation
- Never use special characters in file names
- Configure tsconfig.json with path aliases

## Routes

- Routes belong in the `app` directory
- Never co-locate components, types, or utilities in the app directory
- Ensure the app always has a route that matches "/"

## Library Preferences

| Avoid | Use Instead |
|-------|-------------|
| Legacy Picker, WebView, SafeAreaView | Modern alternatives |
| `expo-av` | `expo-audio` and `expo-video` |
| `@expo/vector-icons` | `expo-symbols` |
| `Platform.OS` | `process.env.EXPO_OS` |
| `React.useContext` | `React.use` |
| Intrinsic `img` | `expo-image` Image component |

## Responsiveness

- Always wrap root component in a scroll view
- Use `<ScrollView contentInsetAdjustmentBehavior="automatic" />`
- Use flexbox instead of Dimensions API
- Prefer `useWindowDimensions` over `Dimensions.get()`

## Styling

Follow Apple Human Interface Guidelines:

- Prefer flex gap over margin and padding
- Use `{ borderCurve: 'continuous' }` for rounded corners
- Use CSS `boxShadow` style prop (NEVER legacy shadow or elevation)
- Inline styles, not StyleSheet.create unless reusing

## Navigation

Use `<Link href="/path" />` from 'expo-router' for navigation:

```tsx
import { Link } from 'expo-router';

<Link href="/path" />

// With custom component
<Link href="/path" asChild>
  <Pressable>...</Pressable>
</Link>
```

Add context menus and previews frequently:

```tsx
<Link href="/settings">
  <Link.Trigger><Card /></Link.Trigger>
  <Link.Preview />
  <Link.Menu>
    <Link.MenuAction title="Share" icon="square.and.arrow.up" />
  </Link.Menu>
</Link>
```

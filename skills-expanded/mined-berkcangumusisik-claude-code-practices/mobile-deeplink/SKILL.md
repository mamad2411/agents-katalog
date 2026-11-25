---
name: mobile-deeplink
description: Sets up or audits deep linking for React Native / Expo apps
argument-hint: [scheme]
user-invocable: true
allowed-tools: Read Glob Edit Bash
effort: medium
---

## Deep Link Setup

App scheme: **$1** (e.g., `myapp` → `myapp://`)

1. Detect navigation library:
```bash
cat package.json | grep -E '"@react-navigation"|"expo-router"|"react-native-navigation"'
cat app.json 2>/dev/null | grep -E "scheme\|intentFilters\|associatedDomains"
```

2. For Expo Router (file-based):
   - Check `app.json` for `scheme`
   - Review `app/` directory structure for dynamic routes
   - Generate `app/+not-found.tsx` if missing

3. For React Navigation:
   - Review `linking` config
   - Ensure all screens are mapped
   - Check for missing parameter types

4. Universal Links / App Links:
   - `apple-app-site-association` for iOS
   - `assetlinks.json` for Android
   - Generate templates for both

5. Testing:
```bash
# iOS Simulator
xcrun simctl openurl booted "$1://path/to/screen"

# Android Emulator
adb shell am start -W -a android.intent.action.VIEW -d "$1://path/to/screen"
```

6. Generate a deeplink test matrix - all routes with test URLs.

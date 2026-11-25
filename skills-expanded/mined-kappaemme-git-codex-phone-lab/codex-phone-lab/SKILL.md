---
name: codex-phone-lab
description: Build and iterate mobile apps that run on a real phone through Expo/React Native live preview. Use when Codex is asked to create a phone app, prototype an iPhone or Android app, run an app on a physical phone, show a QR code for Expo Go, set up a mobile dev workflow, or turn a prompt into a live mobile app without starting from Xcode/TestFlight/App Store distribution.
---

# Codex Phone Lab

Use this skill to turn a product prompt into a React Native/Expo app that the user can open on a physical phone with Expo Go. Optimize for a fast "prompt -> app -> phone" loop before considering simulator, native builds, TestFlight, or app store distribution.

## Operating Model

Prefer this path unless the user explicitly needs native iOS/Android modules:

1. Check local prerequisites with `scripts/doctor.sh`.
2. If no mobile project exists, create an Expo app with `scripts/new-expo-app.sh <app-name>`. This defaults to `expo-template-default@sdk-54` so it opens in the current Expo Go version used by this workflow.
3. Build the first usable screen quickly; do not create a landing page.
4. Start the phone preview with `scripts/start-phone-preview.sh [lan|tunnel|local]`.
5. Keep the dev server running while editing. Use Metro/Expo logs to fix runtime errors.
6. Tell the user to install Expo Go, scan the QR, and keep the phone on the same network for LAN mode.
7. Iterate in small visible changes: edit, observe logs, reload, fix.

## Project Detection

Before creating a new app, inspect the current directory:

- `package.json` with `expo` dependency: treat as existing Expo app.
- `app.json`, `app.config.*`, `app/`, or `expo-router`: treat as Expo app even if dependencies need install.
- `ios/` and `android/` without Expo: ask only if the user needs Expo migration; otherwise keep existing stack.
- Empty directory: create a new Expo app with the SDK 54 template.

## Phone Preview

Use Expo Go for the first "wow" demo because it avoids App Store/TestFlight friction.

Use SDK 54 by default. The current Expo Go in this workflow rejects SDK 55 projects with "Project is incompatible with this version of Expo Go". Override only when the user's Expo Go is known to support a newer SDK:

```bash
CODEX_PHONE_LAB_EXPO_TEMPLATE=expo-template-default@sdk-55 <skill-dir>/scripts/new-expo-app.sh my-app
```

Run:

```bash
<skill-dir>/scripts/start-phone-preview.sh lan
```

Use `tunnel` when the phone is not on the same Wi-Fi or LAN mode cannot connect. Tunnel mode may ask Expo to install a tunneling dependency.

The user workflow:

1. Install Expo Go on the phone.
2. Run the preview command.
3. Scan the QR code from Expo Go or the phone camera.
4. Keep the terminal open; app edits refresh live.

## App-Building Guidance

Make the first screen feel like a real app:

- Use safe areas and mobile-sized layouts.
- Build actual interaction: forms, lists, navigation, toggles, timers, mock data, or state.
- Include loading, empty, and error states when the workflow implies them.
- Keep typography compact enough for mobile.
- Avoid web landing-page patterns, oversized hero sections, nested cards, and explanatory in-app text.
- Prefer Expo Router for multi-screen apps when the template already includes it.

## Distribution Decision

Choose the lightest route that matches the user's goal:

- Fast prototype on user's phone: Expo Go QR.
- App with custom native modules: Expo development build.
- Beta users on iPhone: TestFlight via EAS/Apple Developer account.
- Public release: App Store / Play Store submission.

Do not imply Expo Go is production distribution. It is a live development preview.

## References

Read `references/expo-phone-workflow.md` when deciding between Expo Go, development builds, TestFlight, and app store release.

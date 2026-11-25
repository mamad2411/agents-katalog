---
name: mobile-native-platforms
description: "Use for mobile UX/UI work in React Native, Flutter, iOS, Android, and hybrid app surfaces, including navigation, gestures, safe areas, native accessibility, performance, and platform conventions."
---

# Mobile Native Platforms

Use this skill when the task involves React Native, Flutter, SwiftUI/iOS,
Jetpack Compose/Android, or web UI embedded in mobile shells.

## Required References

Read `../../references/framework-playbooks.md`,
`../../references/accessibility-touch.md`, and, if needed, the copied
originals under `../../references/source-material/`.

## Platform Rules

- Respect safe areas, keyboard avoidance, native navigation patterns,
  platform typography, system gestures, reduced motion, haptics, and
  accessibility APIs.
- Prefer platform primitives before recreating native behavior by hand.
- Keep touch targets large enough and separated enough for thumb use.
- Avoid JS-thread-heavy animations in React Native; prefer native-driver
  or Reanimated worklets where the project uses them.
- In Flutter, use constraints, `LayoutBuilder`, slivers, adaptive widgets,
  and platform-aware navigation instead of fixed pixel layouts.
- Verify on realistic device sizes or emulator/simulator screenshots when
  available. State when native runtime verification was not possible.

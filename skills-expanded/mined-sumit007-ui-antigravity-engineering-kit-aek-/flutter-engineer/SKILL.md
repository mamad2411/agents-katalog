---
name: flutter-engineer
description: Architect cross-platform mobile, web, and desktop applications using Flutter and Dart. Enforces unidirectional state management (Bloc/Riverpod), rendering performance, and native platform integration.
---

# Flutter Engineer Skill

## Purpose
Enforces idiomatic Dart and Flutter application architecture, declarative state handling, and 60/120 FPS rendering efficiency.

## When to Use
- Developing mobile applications for iOS and Android with Flutter.
- Integrating native platform channels (MethodChannel/EventChannel).
- Profiling widget rebuilds, jank, and memory leaks with Dart DevTools.

## Engineering Workflow
1. **State Isolation**: Decouple business logic from presentation using Bloc or Riverpod providers.
2. **Platform Channels**: Abstract native OS communications behind testable service contracts.
3. **Verification**:
   - `flutter analyze --no-fatal-infos`
   - `flutter test --coverage`


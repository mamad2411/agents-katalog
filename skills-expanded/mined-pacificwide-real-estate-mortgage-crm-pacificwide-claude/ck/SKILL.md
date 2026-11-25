---
name: ck:mobile-development
description: Build mobile apps with React Native, Flutter, Swift/SwiftUI, Kotlin/Jetpack Compose. Use for iOS/Android, mobile UX, performance optimization, offline-first, app store deployment.
license: MIT
version: 1.0.0
argument-hint: "[platform] [feature]"
---

# Mobile Development Skill

## When to Use

- Building iOS/Android apps (cross-platform or native)
- Mobile-first UX, offline-first architecture
- Performance optimization, app store deployment
- Platform-specific guidelines (iOS HIG, Material Design 3)

## Framework Selection

| Need | Choose |
|------|--------|
| JS team, web code sharing | React Native |
| Performance, complex animations | Flutter |
| Maximum iOS performance | Swift/SwiftUI |
| Maximum Android performance | Kotlin/Compose |
| Rapid prototyping | React Native + Expo |
| Enterprise JS team | React Native |

## Performance Targets

- Launch: <2s to interactive (70% abandon if >3s)
- Memory: <100MB typical, <200MB peak
- Animations: 60 FPS (16.67ms/frame)
- App size: <50MB initial download

## Architecture

- MVVM for small-medium; MVVM + Clean Architecture for large apps
- Offline-first with hybrid sync (push + pull)
- State: Zustand (RN), Riverpod 3 (Flutter), StateFlow (Android)

## Security (OWASP Mobile Top 10)

- OAuth 2.0 + JWT + Biometrics
- Keychain (iOS) / KeyStore (Android) for sensitive data
- Certificate pinning, never hardcode credentials

## Testing

- Unit: 70%+ coverage for business logic
- E2E: Detox (RN), XCUITest (iOS), Espresso (Android)
- Real device testing mandatory before release

## Deployment

- Fastlane for automation
- Staged rollout: Internal → Closed → Open → Production
- CI/CD: GitHub Actions + Fastlane

## Reference Navigation

- `references/mobile-frameworks.md` — Framework comparison matrices
- `references/mobile-ios.md` — Swift 6, SwiftUI, HIG, App Store
- `references/mobile-android.md` — Kotlin, Compose, Material 3, Play Store
- `references/mobile-best-practices.md` — Performance, security, accessibility
- `references/mobile-debugging.md` — Profiling, crash analysis, network debugging

## Resources

- React Native: https://reactnative.dev/
- Flutter: https://flutter.dev/
- iOS HIG: https://developer.apple.com/design/human-interface-guidelines/
- Material Design: https://m3.material.io/

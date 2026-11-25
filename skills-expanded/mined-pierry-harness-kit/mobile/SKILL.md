---
name: mobile
description: Mobile engineering conventions for team. iOS and Android. Project conventions in .claude/conventions/mobile.md override these defaults.
user_invocable: false
---

Mobile conventions, team default.

Project override: if `{repo}/.claude/conventions/mobile.md` exists, overrides any rule here. See guides/conventions-override.md.

## Defaults

team mobile work limited; repos vary widely. Always read repo before writing.

iOS:
- Swift 5.x. Avoid Objective-C unless repo already uses it.
- Xcode project conventions per repo.
- Tests: XCTest. Naming `test_givenX_whenY_thenZ`.

Android:
- Kotlin. Avoid Java unless repo already uses it.
- Gradle build. Check `build.gradle.kts` vs `build.gradle`.
- Tests: JUnit 4 or JUnit 5. Espresso for UI.

Shared:
- Match existing architecture (MVVM, MVI, Clean, etc).
- Match existing DI (Hilt, Koin, Dagger).

## Before writing code

Read at least 3 similar files in repo to confirm:
- language version (Swift/Kotlin)
- architecture pattern
- DI framework
- test framework
- networking (Retrofit, Alamofire, URLSession)

Mobile stacks vary more than backend or web. Verify everything.

## Forbidden in PR

- mixing architecture patterns (e.g., MVP + MVVM in same module)
- hardcoded strings (use string resources)
- direct file system access without permission checks
- code without tests
- TODOs without ticket references

## Mark gaps

```kotlin
// TBD - verify with mobile tech lead: {what is missing}
```

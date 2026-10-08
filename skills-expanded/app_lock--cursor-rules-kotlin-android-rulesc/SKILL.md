---
description: Kotlin/Android naming conventions, foreground service rules, UsageStats handling, and platform channel contract
globs: **/*.kt
alwaysApply: false
---

# Kotlin / Android Rules

## Naming

- Files: PascalCase (`AppMonitorService.kt`)
- Classes: PascalCase
- Variables/methods: camelCase
- Constants: UPPER_SNAKE_CASE

## Service Rules

- AppMonitorService must always run as a foreground service
- AppMonitorService must return START_STICKY
- Always check permissions before accessing UsageStats
- Always handle SecurityException when accessing UsageStats
- LockActivity must use FLAG_ACTIVITY_NEW_TASK when launching
- All SharedPreferences keys must be defined as constants, never inline strings

## Platform Channel Contract

- Channel name: `com.multiprofilelock/applock`
- Every method call must have a matching `when()` branch in MainActivity
- Always call `result.success()`, `result.error()`, or `result.notImplemented()`
- Never leave a method call without a result response

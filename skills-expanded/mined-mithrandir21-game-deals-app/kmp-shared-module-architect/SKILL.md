---
name: kmp-shared-module-architect
description: Design or refactor a Kotlin Multiplatform shared module — source-set hierarchy, expect/actual placement, iOS framework export, SKIE / KMP-NativeCoroutines setup, CocoaPods or SPM publishing, and Android/iOS interop boundaries. Use whenever the user mentions "KMP shared module", "expect/actual", "commonMain", "iosMain", "Kotlin Multiplatform", "iOS framework", "SKIE", "CocoaPods integration", or wants to set up or restructure a shared module. Also use when "code I want to share between Android and iOS" comes up.
---

# KMP Shared Module Architect

A well-shaped KMP module shares Kotlin code without leaking Kotlin idioms into Swift. The decisions about source sets, what to expose, and how to bridge async types determine whether iOS developers want to work with your code or work around it.

## When to use

Triggers: "KMP module", "shared module", "expect/actual", "commonMain", "iosMain", "iOS framework", "SKIE", "KMP-NativeCoroutines", "CocoaPods", "Swift Package Manager", "publish to iOS".

For single-platform Kotlin work, this skill doesn't apply.

## Process

### Phase 1: Decide what to share

Not everything belongs in shared code. A useful filter:

| Share | Don't share |
|---|---|
| Networking layer (DTOs, API calls) | UI |
| Data models, validation logic | Platform-specific navigation |
| Repository layer | Push notification handling |
| Use cases / business logic | Background work scheduling |
| State holders (Presenter / Store / ViewModel-equivalent) | Platform integrations (camera, biometrics) |

The further you push toward UI, the more friction you hit. Start small (networking + models), grow toward business logic, stop at platform integrations.

### Phase 2: Set up source-set hierarchy

Modern KMP uses the **hierarchical source set** template. For Android + iOS:

```
commonMain                    ← shared Kotlin code
├── androidMain              ← JVM/Android-specific
└── iosMain                  ← intermediate, shared between iOS variants
    ├── iosX64Main           ← simulator (Intel)
    ├── iosArm64Main         ← device
    └── iosSimulatorArm64Main ← simulator (Apple Silicon)
```

In `build.gradle.kts`:

```kotlin
kotlin {
    androidTarget()
    listOf(iosX64(), iosArm64(), iosSimulatorArm64()).forEach { it ->
        it.binaries.framework {
            baseName = "Shared"
            isStatic = true
        }
    }

    sourceSets {
        commonMain.dependencies {
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.kotlinx.serialization.json)
            implementation(libs.ktor.client.core)
        }
        androidMain.dependencies {
            implementation(libs.ktor.client.okhttp)
        }
        iosMain.dependencies {
            implementation(libs.ktor.client.darwin)
        }
    }
}
```

Put code in the highest source set that compiles. `iosMain` for code shared across all iOS variants; `androidMain` for Android-only.

### Phase 3: Use expect/actual sparingly

`expect`/`actual` is for platform APIs that don't exist in common. Don't reach for it when:

- An interface + DI binding works. Define an interface in `common`, implement per platform, inject.
- A library already covers it (Ktor for HTTP, kotlinx-datetime for time, Multiplatform Settings for prefs).

Good use cases:
- Random / UUID generation differs.
- Logging needs platform tools (Android Logcat vs. iOS OSLog).
- Platform-specific limits (max heap, screen density).

Pattern:

```kotlin
// commonMain
expect class PlatformLogger() {
    fun log(message: String)
}

// androidMain
actual class PlatformLogger {
    actual fun log(message: String) { Log.d("App", message) }
}

// iosMain
actual class PlatformLogger {
    actual fun log(message: String) { NSLog("%s", message) }
}
```

Prefer interfaces + DI for non-trivial cases; `expect`/`actual` couples implementations to the source set tree and makes them harder to test.

### Phase 4: Shape the iOS-facing API

This is where most KMP projects pay tax. Swift sees Kotlin through ObjC headers (or Swift bindings via SKIE). What's pleasant in Kotlin can be ugly in Swift.

**Default rules for the public surface:**

- **Avoid Kotlin generics with variance.** `interface Repository<out T>` becomes painful on the Swift side.
- **Avoid raw `Flow`/`StateFlow`.** Swift can't subscribe to it idiomatically without help.
- **Avoid `suspend` on the outermost API** unless you're using SKIE or KMP-NativeCoroutines.
- **Sealed classes work**, but in raw interop they become a base class + subclasses, not a Swift enum. SKIE makes them Swift enums.
- **Don't expose `Result<T>`** — Kotlin's `Result` doesn't bridge cleanly. Use your own sealed `Outcome<T>` and translate.
- **Default arguments don't translate** — every Kotlin default becomes a parameter that Swift must provide. Use overloads or builders.

**With SKIE**:

Add the Gradle plugin:

```kotlin
plugins {
    id("co.touchlab.skie") version "..."
}
```

SKIE transforms generated headers so Swift sees:
- Sealed classes as Swift enums.
- Flows as `AsyncSequence`.
- Suspend functions as Swift `async` functions.
- Default arguments preserved.

It's the path of least resistance for new projects. Adopt unless there's a specific reason not to.

**With KMP-NativeCoroutines** (alternative to SKIE for Flow/suspend interop):

```kotlin
@NativeCoroutines
suspend fun fetch(): Foo

@NativeCoroutines
val updates: Flow<Foo>
```

Generates Swift extensions that call into the suspend/Flow with completion handlers or `AsyncSequence`.

### Phase 5: Publish the iOS framework

Three options:

**1. Direct Xcode integration** — Gradle task produces a `.framework`, Xcode references it. Simple for monorepos.

```kotlin
// In iosApp's project, add a Run Script Build Phase:
cd "$SRCROOT/.." && ./gradlew :shared:embedAndSignAppleFrameworkForXcode
```

**2. CocoaPods** — KMP Gradle plugin generates a podspec. iOS project does `pod install`.

```kotlin
kotlin {
    cocoapods {
        summary = "Shared module"
        homepage = "..."
        ios.deploymentTarget = "14.0"
        framework {
            baseName = "Shared"
            isStatic = true
        }
    }
}
```

**3. Swift Package Manager** — KMP Gradle plugin can produce a Swift package via `kmmbridge`. More moving parts but doesn't require CocoaPods.

For app-internal use, option 1 is simplest. For shared-with-third-parties, options 2 or 3.

### Phase 6: Testing

- `commonTest` for tests of common code with `kotlin.test`.
- `androidUnitTest` / `iosTest` for platform-specific tests when needed.
- For Flow-based shared code, use `Turbine` (works in `commonTest`).
- For HTTP, use Ktor `MockEngine` in `commonTest`.

### Phase 7: Verify the experience for iOS callers

Have an iOS developer actually use the shared module before declaring it done. Specifically:

- Can they call the main entry points without help?
- Are async/Flow usages ergonomic?
- Do error types make sense from Swift?
- Do imports auto-complete and show docs?

If any of these are no, fix the public surface (Phase 4) before scaling out the shared code.

## Output

For a new shared module:

1. **Source set diagram** with what goes where.
2. **Public API sketch** — top-level interfaces, with iOS-facing notes.
3. **Tooling choices** — SKIE / KMP-NativeCoroutines, publishing method.
4. **Test setup** outline.

For a refactor:

1. **What's there now** — pain points.
2. **What changes** — source set moves, API reshape.
3. **Migration sequence** — keep the iOS app compiling at each step.

## Common pitfalls

- **Trying to share UI.** Compose Multiplatform is improving but adds friction. Start with non-UI.
- **Putting everything in `commonMain`.** Even Android-only code. Hurts compile times and blocks platform-specific implementations later.
- **Exposing `Flow` without SKIE / KMP-NativeCoroutines.** Swift developers will hate you.
- **Static `object` singletons holding mutable state.** Tied to Kotlin/Native memory model quirks; works fine on new memory model but still a footgun.
- **Generic `Result<T, E>` in the public API.** Swift can't see `E`. Use a sealed outcome type instead.
- **Forgetting to commit the `.framework` Run Script.** Then iOS builds work on your machine but not in CI.

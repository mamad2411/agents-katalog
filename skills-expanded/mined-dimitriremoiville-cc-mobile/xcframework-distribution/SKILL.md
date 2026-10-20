---
name: xcframework-distribution
description: Distribute the `:shared` KMP module to iOS — XCFramework output, CocoaPods vs SPM vs direct XCFramework consumption, versioning, cinterop, and when to ship a Swift Package wrapper. Load whenever touching iOS consumption of the shared module or publishing a new version.
---

# XCFramework distribution

## Three distribution modes

1. **Direct XCFramework binary in the same repo.** The `iosApp/` Xcode project embeds the shared framework produced by Gradle. This is the default for a mono-repo KMP setup.
2. **CocoaPods plugin.** The `cocoapods { ... }` block on the `:shared` module emits a `.podspec` and the Xcode project pulls it via CocoaPods. Fine for legacy iOS projects already on Pods.
3. **Swift Package Manager** (SPM). A Swift Package wrapping the XCFramework via `binaryTarget(url:, checksum:)`. The most iOS-idiomatic distribution for an external consumer.

Choose exactly one per project. Don't run two at the same time — duplicate framework linking breaks debug symbols.

## Mode 1 — Direct XCFramework

`:shared` `build.gradle.kts`:

```kotlin
kotlin {
    listOf(iosX64(), iosArm64(), iosSimulatorArm64()).forEach {
        it.binaries.framework {
            baseName = "Shared"
            isStatic = true
            export(libs.kotlinx.datetime)
        }
    }

    tasks.register("buildSharedXCFramework", XCFrameworkTask::class) {
        frameworks(
            iosArm64().binaries.getFramework(NativeBuildType.RELEASE),
            iosX64().binaries.getFramework(NativeBuildType.RELEASE),
            iosSimulatorArm64().binaries.getFramework(NativeBuildType.RELEASE),
        )
        baseName = "Shared"
        outputDir = layout.buildDirectory.dir("XCFrameworks/release").get().asFile
    }
}
```

`isStatic = true` is preferred for iOS — the Xcode app target links it, no dynamic loading overhead, and debug symbols stay clean.

In the Xcode project, add the produced `Shared.xcframework` to **Frameworks, Libraries, and Embedded Content** and set **Embed & Sign** for the app target.

### Build script integration

A Run Script phase builds the framework before compiling Swift:

```bash
cd "$SRCROOT/.."
./gradlew :shared:buildSharedXCFramework -Pkotlin.native.cocoapods=false
```

For debug iterations, `linkDebugFrameworkIos*` produces a slimmer framework on every incremental build.

## Mode 2 — CocoaPods

```kotlin
plugins {
    kotlin("multiplatform")
    kotlin("native.cocoapods")
}

kotlin {
    cocoapods {
        version = "1.0.0"
        summary = "Shared KMP module"
        homepage = "https://example.com"
        ios.deploymentTarget = "16.0"
        framework {
            baseName = "Shared"
            isStatic = true
        }
    }
}
```

Generates a `shared.podspec`; consumer Xcode project `Podfile`:

```ruby
pod 'shared', :path => '../shared'
```

Run `pod install` after every bump. The podspec regenerates from Gradle.

## Mode 3 — SPM with binaryTarget

For a clean external consumer, publish the XCFramework as a zipped binary artifact:

```kotlin
tasks.register<Zip>("zipSharedXCFramework") {
    dependsOn("buildSharedXCFramework")
    from(layout.buildDirectory.dir("XCFrameworks/release/Shared.xcframework"))
    archiveFileName.set("Shared.xcframework.zip")
    destinationDirectory.set(layout.buildDirectory.dir("artifacts"))
}
```

Upload the zip to a storage bucket (S3, GitHub release artifact). Compute its SHA256, then `Package.swift`:

```swift
let package = Package(
    name: "SharedKit",
    platforms: [.iOS(.v16)],
    products: [.library(name: "SharedKit", targets: ["SharedKit"])],
    targets: [
        .binaryTarget(
            name: "SharedKit",
            url: "https://cdn.example.com/releases/1.0.0/Shared.xcframework.zip",
            checksum: "3c9a6e2f..."
        ),
    ]
)
```

Cut a new tag per version. The checksum must match exactly.

## Exporting dependencies

Public API that leaks types from other libraries (`kotlinx.datetime`, custom modules) needs `export(...)`:

```kotlin
framework {
    baseName = "Shared"
    export(libs.kotlinx.datetime)
    export(project(":shared:models"))
}
```

Transitive types without `export` appear as opaque `Any` on the Objective-C side.

## Obj-C interop hygiene

See the existing [kmm-ios-interop skill](../kmm-ios-interop/SKILL.md). For distribution specifically:

- Every exported type goes through Obj-C. Generics collapse; sealed hierarchies become class hierarchies; `internal` types are invisible.
- `@ObjCName("...")` renames on the iOS side without changing Kotlin.
- `@HidesFromObjC` hides irrelevant helpers.
- `@Throws(MyDomainError::class)` on suspend functions; otherwise Swift sees a non-throwing `async`.

## Versioning

- Semver on the shared module.
- Breaking changes to the framework API (renames, removed types) bump major.
- Wire compat with the server lives separately; treat them as two independent contracts.
- Tag releases in git; CI builds the XCFramework + zips + publishes.

## Debugging

- dSYMs: `isStatic = true` bakes them in. When `isStatic = false`, upload the framework's dSYM to Crashlytics.
- If Swift can't see a Kotlin declaration: check `export(...)`, `public` visibility, and that it's not a `typealias` to a non-exported type.
- If the iOS consumer crashes with "module not found" after a Kotlin version bump: reset derived data (`~/Library/Developer/Xcode/DerivedData/*`) and clean Gradle (`./gradlew clean`).

## Hard nos

- No mixing CocoaPods + direct XCFramework in the same Xcode project.
- No dynamic XCFramework (`isStatic = false`) without a documented reason.
- No committing the framework binary. Generate on CI.
- No `export(...)` on libraries you don't own the API of, unless you're willing to rebuild the framework every time they bump.
- No shipping `:shared` with `internal` types in the public API. Swift can't see them; the iOS side breaks.

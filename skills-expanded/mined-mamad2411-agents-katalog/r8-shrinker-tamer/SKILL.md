---
name: r8-shrinker-tamer
description: Diagnose release-build R8 failures and bloat — incorrect keep rules for reflection-based libraries (Moshi, Retrofit, Hilt, Compose, kotlinx.serialization), missing rules from third-party deps, crashes only in release, and APK size investigation. Use whenever the user mentions "release crash", "works in debug", "R8", "ProGuard", "minification", "keep rules", "missing rules", "obfuscation", or wants to shrink APK size. Also use when a release build won't compile due to R8.
---

# R8 Shrinker Tamer

R8 removes and renames code aggressively. Anything that uses reflection (most serialization, DI, Compose, navigation) needs keep rules — sometimes provided by libraries, sometimes you have to write them. This skill walks through the common failure modes.

## When to use

Triggers: "release crash but debug works", "R8 error", "ProGuard rules", "missing rules", "obfuscation", "minifyEnabled", "shrinking", "APK too big", "AAB size".

For "release builds are slow", use `startup-jank-profiler`. For "release tests fail differently", check whether instrumented tests run with `testProguardFiles`.

## Process

### Phase 1: Reproduce in release

If the dev only saw the crash in production, get a local repro:

```kotlin
buildTypes {
    release {
        isMinifyEnabled = true
        isShrinkResources = true
        proguardFiles(
            getDefaultProguardFile("proguard-android-optimize.txt"),
            "proguard-rules.pro"
        )
        // Important: keep signing config testable locally
    }
}
```

`./gradlew assembleRelease` and install. Reproduce.

### Phase 2: Read the crash

Common shapes:

| Crash | Cause |
|---|---|
| `java.lang.NoSuchMethodException`, `NoSuchFieldException` | Reflection target was renamed/stripped. |
| `Caused by: java.lang.RuntimeException: Cannot serialize ...` | Moshi/Gson/kotlinx.serialization can't find a constructor or class. |
| `Class 'XxxImpl' is not assignable to ...` | Generic types erased; reflection can't reconstruct. |
| `ClassNotFoundException` on a Hilt-generated class | Hilt component or `@HiltAndroidApp` Application stripped. |
| Compose screen crashes with weird state | Stable types renamed; equality breaks. Rare. |
| Native library load fails | `System.loadLibrary` looking for stripped symbols. |

Get a deobfuscated stack trace using the `mapping.txt` from `app/build/outputs/mapping/release/`. Most crash reporters auto-deobfuscate if uploaded.

### Phase 3: Find missing rules

Most rule problems fall into one of three buckets:

**1. The library has rules but they're not being picked up**
- Most modern libraries (Retrofit, Moshi, Hilt, Coil) ship `consumer-proguard-files`. If they're not applied, something's wrong with the build.
- Confirm via the merged config:
```
./gradlew :app:assembleRelease
# then read
app/build/outputs/mapping/release/configuration.txt
```
- Look for the library's rules in the merged file. If absent, the library version may be old or the dependency type may be wrong (`compileOnly` instead of `implementation`).

**2. The library doesn't ship rules but documents them**
- Check the library's docs/README. Some still want you to copy a block into `proguard-rules.pro`.

**3. Your own reflection**
- Code that uses `Class.forName`, `KClass`, `@JsonClass`, or any annotation-driven reflection on your own types may need rules.

### Phase 4: Add rules carefully

Write rules narrowly. Broad rules (`-keep class com.app.** { *; }`) defeat the point.

**Pattern: data classes used for serialization (Moshi, Gson)**

```proguard
# Moshi data classes
-keep,allowobfuscation,allowshrinking @com.squareup.moshi.JsonClass class *
-keepclassmembers class com.app.network.dto.** { <init>(...); }
```

kotlinx.serialization handles itself via the plugin — usually you don't need rules unless you're doing polymorphic serialization with reflection.

**Pattern: Retrofit interfaces**

```proguard
-keep,allowobfuscation,allowshrinking interface retrofit2.Call
-keep,allowobfuscation,allowshrinking class retrofit2.Response

# Keep your service interfaces if you use generics in returns
-keep,allowobfuscation,allowshrinking interface com.app.network.** { *; }
```

Retrofit 2.10+ ships better rules; if on older, you may need more.

**Pattern: Hilt**

Hilt's generated rules are usually sufficient. If you see issues, ensure `@HiltAndroidApp` Application class is kept (it is by default if declared in manifest).

**Pattern: enums used with `valueOf`**

```proguard
-keepclassmembers enum * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}
```

**Pattern: Parcelable**

```proguard
-keepclassmembers class * implements android.os.Parcelable {
    public static final ** CREATOR;
}
```

### Phase 5: Investigate bloat

If APK size is the concern, not crashes:

```
./gradlew :app:assembleRelease
# Then in Android Studio: Build → Analyze APK
```

Look for:

- **Resources**: unused drawables, large PNGs that should be vector or WebP, multiple density variants you don't need.
- **Native libraries**: `arm64-v8a` is non-negotiable; consider App Bundles to ship only what each device needs.
- **`assets/`**: bundled files that could be downloaded on demand.
- **Classes (DEX)**: large libraries pulled in for one feature. Check whether `R8` is shrinking effectively (`shrinkResources = true` and `minifyEnabled = true`).
- **Kotlin stdlib + runtime**: usually around 1.5MB. Not worth shrinking unless you're embedded.

For dependency bloat, run `./gradlew :app:dependencies | head -200` and look for big libs you didn't expect.

### Phase 6: Verify and harden

- Confirm the release APK runs through the user flows that crashed.
- Add a "release smoke test" instrumented test config that runs against the release build periodically.
- Keep the `mapping.txt` for every release — upload to your crash reporter automatically.

## Output

For a crash:

1. **The crash** — deobfuscated trace.
2. **Cause** — which reflection / generic / renaming.
3. **Rule added** — narrow, justified.
4. **Verified** — release build now passes the affected flow.

For bloat:

1. **APK breakdown** — what's biggest.
2. **Targets** — items to cut, with size estimates.
3. **App Bundle config** — confirmed.

## Common pitfalls

- **`-dontobfuscate` to "make crashes readable".** You give up the size win. Keep obfuscation, ship `mapping.txt` to your crash reporter.
- **Broad keep rules.** `-keep class com.app.**` keeps everything. You've effectively disabled R8 for your code.
- **Disabling R8.** "Set `minifyEnabled = false`" is not a fix. The release build is now huge and slow.
- **Not testing release builds before publishing.** Catches 90% of these issues before users do.
- **Stale rules.** When a library updates and ships new consumer rules, your local `proguard-rules.pro` may have stale overrides. Audit periodically.

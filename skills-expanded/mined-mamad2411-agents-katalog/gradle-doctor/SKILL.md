---
name: gradle-doctor
description: Diagnose Gradle issues for Android/KMP projects — build failures, configuration-cache violations, version catalog drift, AGP/Kotlin compatibility, slow builds, isolated-projects readiness, and Kotlin 2.0+ migration issues. Use whenever the user mentions "Gradle error", "build failed", "configuration cache", "slow build", "AGP upgrade", "Kotlin upgrade", "version catalog", "buildSrc", "build-logic", "isolated projects", or anything about the build system. Also use when a CI build works but local doesn't, or vice versa.
---

# Gradle Doctor

Gradle issues split into a small number of categories: dependency resolution problems, plugin/compiler version mismatches, build-script errors, and performance. This skill helps place the issue and fix it without trial-and-error.

## When to use

Triggers: "Gradle", "build failed", "configuration cache", "slow build", "AGP", "Kotlin compiler", "KSP", "KAPT", "version catalog", "convention plugin", "buildSrc", "isolated projects", "incremental build broken".

For "I want to set up a new project", this skill is overkill. Use for diagnosing problems in an existing build.

## Process

### Phase 1: Get the actual error

Re-run with diagnostics:

```
./gradlew assembleDebug --stacktrace --info
```

If still unclear:

```
./gradlew assembleDebug --debug 2>&1 | tee build-debug.log
```

Look at the first error, not the last. Gradle often cascades failures; the second error is a consequence of the first.

### Phase 2: Classify

| Symptom | Category |
|---|---|
| `Could not resolve dependency X` | Dependencies |
| `Plugin X requires Y` | Plugin compatibility |
| `Cannot access class ... is internal in module ...` | Module visibility / API surface |
| `Configuration cache state could not be cached` | Configuration cache |
| `Execution failed for task ':compile...'` | Compiler — Kotlin, KSP, AGP |
| `Could not find method X on extension` | DSL / plugin order |
| `Duplicate class X found in modules Y and Z` | Dependency conflict |
| Build is slow with no error | Performance |

### Phase 3: Apply the right fix

**Dependency resolution**

- `./gradlew :app:dependencies` to see the graph.
- `./gradlew :app:dependencyInsight --dependency <name>` to see why a version was chosen.
- Resolution strategies in `settings.gradle.kts`:
  ```kotlin
  dependencyResolutionManagement {
      repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
      repositories {
          google()
          mavenCentral()
      }
  }
  ```
- Force a version:
  ```kotlin
  configurations.all { resolutionStrategy.force("com.x:y:1.2.3") }
  ```
  Use sparingly — it's a band-aid.

**Plugin compatibility**

The big four are bound together — AGP, Kotlin, Compose Compiler, KSP:

| If you upgrade | Also check |
|---|---|
| AGP | Gradle wrapper version, Kotlin version, Java toolchain |
| Kotlin | Compose Compiler version, KSP version, all Kotlin plugins (serialization, parcelize, etc.) |
| Compose Compiler | Now decoupled from Kotlin on 1.5.8+; still verify it works with current Kotlin |
| KSP | Must match Kotlin version exactly (e.g. KSP `1.9.22-1.0.17` ties to Kotlin 1.9.22) |

When upgrading, do one at a time and run the full build between each.

**Version catalog issues**

`gradle/libs.versions.toml` is the source of truth. Common mistakes:
- A version referenced in `[versions]` that no entry uses (harmless but noisy).
- `[libraries]` entries with `version.ref` pointing at a missing version (build fails).
- Aliases with hyphens: `androidx-core-ktx` becomes `libs.androidx.core.ktx` (Gradle replaces hyphens with dots).
- Bundles missing entries.

**Configuration cache violations**

Configuration cache is the way forward. Common violations:
- Tasks accessing `Task.project` at execution time (capture `providers.gradleProperty(...)` instead).
- Custom tasks referencing the `project` object inside actions.
- Reading environment variables outside of providers.

Fix: convert to `Provider`/`Property` APIs. The error message tells you the offending file and line.

```kotlin
// Bad
val token = project.findProperty("token") as String  // accessed at execution

// Good
@get:Input
val token = providers.gradleProperty("token")
```

To enable: `org.gradle.configuration-cache=true` in `gradle.properties`.

**Compiler failures**

- `Cannot inline bytecode` → Kotlin version mismatch across modules. Make sure all modules use the same Kotlin version (version catalog helps).
- `Could not load class …` during KSP → KSP and Kotlin versions don't match. Update.
- `Compose Compiler version is not compatible` → bump or pin the Compose Compiler plugin separately.

**Duplicate class errors**

Two libraries pull in the same class. Use:

```kotlin
configurations.all {
    exclude(group = "com.example", module = "old-library")
}
```

Or drop one of the conflicting dependencies.

**Slow builds**

Steps in order of impact:

1. **Enable configuration cache**: `org.gradle.configuration-cache=true`.
2. **Enable parallel execution**: `org.gradle.parallel=true`.
3. **Enable caching**: `org.gradle.caching=true`. Remote cache if your team has one.
4. **Heap size**: `org.gradle.jvmargs=-Xmx4g -XX:+UseG1GC -XX:MaxMetaspaceSize=1g`.
5. **`./gradlew --scan`** — uploads a build scan you can inspect to see what's slow.
6. **Profile a build**: `./gradlew assembleDebug --profile`. Reports in `build/reports/profile/`.
7. **Audit modules**: too many = configuration time grows. Too few = bad incremental builds.
8. **Audit annotation processors**: KAPT is slow. Migrate to KSP where possible (Hilt, Moshi, Room, Glide).
9. **Audit transformations**: AGP's resource processing is expensive on huge resource sets.

**Isolated Projects (Gradle 8.x+ preview)**

If preparing for it (target Gradle 9.x):
- No cross-project access at configuration time. `project(":other").extensions.getByType(...)` is out.
- Convention plugins must not reach into other projects.
- The `--configuration-cache` build is a precursor to isolated projects readiness.

Run `./gradlew help --isolated-projects` to see violations.

### Phase 4: Verify

- Run the failing build, see green.
- Run `./gradlew clean assembleDebug` to confirm a cold build works.
- If you fixed a perf issue, profile before-and-after to confirm.
- Run on CI if the issue was local-only or vice versa.

### Phase 5: Lock it in

- Pin versions in the catalog.
- Add a `gradle/dependency-locking` lock file for reproducible builds if you don't have one.
- Document the fix in the project's `CONTRIBUTING.md` or build readme — version compatibility is forgotten quickly.

## Output

For a failure:

1. **The first real error** (not the last).
2. **Category** from Phase 2.
3. **Root cause** — version mismatch, configuration cache violation, etc.
4. **Fix** — specific change.
5. **Verification** — what command proves it's fixed.

For perf work:

1. **Baseline timing** — clean build, incremental build of a typical change.
2. **Bottlenecks** identified from `--scan` or profile.
3. **Changes applied** — ordered.
4. **New timing** — same scenarios.

## Common pitfalls

- **Reading the last error.** Gradle cascades; the first error is the real one.
- **Upgrading multiple things at once.** Then you can't isolate which one broke. One at a time.
- **`exclude` chains everywhere.** Symptom of dependency conflicts that should be fixed at the source. Audit and rationalize.
- **Skipping configuration cache because it's "annoying".** Each violation is a real perf cost. Fix them; they're future-proofing.
- **Editing `gradle-wrapper.properties` by hand.** Use `./gradlew wrapper --gradle-version <v>` so other files (the jar) update too.
- **Trusting `--refresh-dependencies` to fix things.** Forces network reads, doesn't change resolution.
- **Heap-bumping without measuring.** 8GB doesn't help if you only use 2GB; it just slows GC.

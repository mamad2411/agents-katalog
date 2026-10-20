---
name: devel-jb-kotlin-tooling-agp9-migration
description: "--| | `android.uniquePackageNames` | `false` | `true` | Ensure each library has a unique namespace | | `android."
domain: cybersecurity
---

--|
| `android.uniquePackageNames` | `false` | `true` | Ensure each library has a unique namespace |
| `android.enableAppCompileTimeRClass` | `false` | `true` | Refactor `switch` on R fields to `if/else` |
| `android.defaults.buildfeatures.resvalues` | `true` | `false` | Enable `resValues = true` where needed |
| `android.defaults.buildfeatures.shaders` | `true` | `false` | Enable shaders where needed |
| `android.r8.optimizedResourceShrinking` | `false` | `true` | Review R8 keep rules |
| `android.r8.strictFullModeForKeepRules` | `false` | `true` | Update keep rules to be explicit |
| `android.proguard.failOnMissingFiles` | `false` | `true` | Remove invalid ProGuard file references |
| `android.r8.proguardAndroidTxt.disallowed` | `false` | `true` | Use `proguard-android-optimize.txt` only |
| `android.r8.globalOptionsInConsumerRules.disallowed` | `false` | `true` | Remove global options from library consumer rules |
| `android.sourceset.disallowProvider` | `false` | `true` | Use `Sources` API on androidComponents |
| `android.sdk.defaultTargetSdkToCompileSdkIfUnset` | `false` | `true` | Specify `targetSdk` explicitly |
| `android.onlyEnableUnitTestForTheTestedBuildType` | `false` | `true` | Only if testing non-default build types |

Check for and remove properties that now cause errors:
- `android.r8.integratedResourceShrinking` — removed, always on
- `android.enableNewResourceShrinker.preciseShrinking` — removed, always on

## Pure Android Tips

For non-KMP Android modules upgrading to AGP 9.0:

- **Remove `org.jetbrains.kotlin.android`** plugin — AGP 9.0 includes Kotlin support built-in (see "Built-in Kotlin Migration" above)
- **Migrate kapt** to KSP or `com.android.legacy-kapt`
- **Migrate `kotlinOptions`** to `kotlin { compilerOptions {} }`
- **Migrate `kotlin.sourceSets`** to `android.sourceSets` with `.kotlin` accessor
- **Review new DSL interfaces** — `BaseExtension` is removed; use `CommonExtension` or specific extension types
- **Java default changed** from Java 8 to Java 11 — ensure `compileOptions` reflects this
- **R class is now compile-time non-final** in app modules — refactor any `switch` statements on R class fields to `if/else`
- **targetSdk defaults to compileSdk** if not set — specify `targetSdk` explicitly to avoid surprises
- **NDK default changed to r28c** — specify `ndkVersion` explicitly if using native code
- **Temporary opt-out**: `android.builtInKotlin=false` + `android.newDsl=false` in `gradle.properties` (removed in AGP 10)

## Verification

After migration, verify with the [checklist](assets/checklist.md). Key checks:

1. `./gradlew build` succeeds with no errors
2. `./gradlew :androidApp:assembleDebug` succeeds (if app module exists)
3. No `com.android.library` or `com.android.application` in KMP modules
4. No `org.jetbrains.kotlin.android` in AGP 9.0 modules
5. Source sets use correct names (`androidMain`, `androidHostTest`, `androidDeviceTest`)
6. No deprecation warnings about variant API
7. Run configurations point to correct modules

## Common Issues

See [references/KNOWN-ISSUES.md](references/KNOWN-ISSUES.md) for details. Key gotchas:

### KMP Library Plugin Issues
- **BuildConfig unavailable** in library modules — use DI/`AppConfiguration` interface, or use [BuildKonfig](https://github.com/yshrsmz/BuildKonfig) or [gradle-buildconfig-plugin](https://github.com/gmazzo/gradle-buildconfig-plugin) for compile-time constants
- **No build variants** — single variant architecture; compile-time constants can use BuildKonfig/gradle-buildconfig-plugin flavors, but variant-specific dependencies/resources/signing must move to app module
- **NDK/JNI unsupported** in new plugin — extract to separate `com.android.library` module
- **Compose resources crash** without `androidResources { enable = true }` (CMP-9547)
- **Consumer ProGuard rules silently dropped** if not migrated to `consumerProguardFiles.add(file(...))` in new DSL
- **KSP** requires version 2.3.4+ for AGP 9.0 compatibility

### AGP 9.0 General Issues
- **Built-in Kotlin conflicts** — `org.jetbrains.kotlin.android` must be removed; kapt must be replaced
- **BaseExtension removed** — convention plugins using old DSL types need rewriting
- **Variant APIs removed** — `applicationVariants`, `libraryVariants`, `variantFilter` replaced by `androidComponents`
- **R class non-final** — `switch` on R fields fails in app modules; refactor to `if/else`
- **targetSdk defaults to compileSdk** — set explicitly to avoid unexpected behavior changes
- **R8 rule changes** — strict full mode, no global options in consumer rules
- **Plugin compatibility** — many plugins need updates or opt-out flags; check Plugin Compatibility section
- **Convention plugins** need refactoring — old `android {}` extension helpers are obsolete

## Reference Files

- [DSL Reference](references/DSL-REFERENCE.md) — side-by-side old→new DSL mapping
- [Version Matrix](references/VERSION-MATRIX.md) — AGP/Gradle/KGP/IDE compatibility
- [Plugin Compatibility](references/PLUGIN-COMPATIBILITY.md) — third-party plugin status and workarounds

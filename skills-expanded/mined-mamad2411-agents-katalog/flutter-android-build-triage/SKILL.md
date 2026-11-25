---
name: flutter-android-build-triage
description: Use when a Flutter Android build fails (`flutter build apk`, Gradle errors, plugin incompatibility, AGP/Gradle version conflicts, native-assets errors like sqlite3_initialize, ENOSPC/disk full, corrupted pub cache). Diagnose by finding the blame line in the Gradle output, apply the matching fix from the symptom table, then verify with a clean build.
---

# Flutter Android build triage

Fix a failing Flutter Android build by locating the **blame line** — the one line in Gradle's wall of output that names the actual culprit (a plugin, a version, a missing symbol, a full disk) — and matching it to the fix table below. Everything above the blame line is noise.

## Steps

1. **Reproduce and capture.** Run the failing build and keep the output:
   `flutter build apk --debug 2>&1 | grep -B5 -A15 -iE 'what went wrong|error:|caused by|Could not|ENOSPC|No space|license|sdk' | head -60`
   Completion criterion: you have 10–60 lines containing the blame line — the line that names the missing/incompatible thing.
2. **Match the blame line to a row** in the symptom table and apply that fix. If the line names a native function (e.g. `sqlite3_initialize`), it's a packaging problem, not Dart code — see the native-libs row.
3. **Verify with a clean build**: `flutter clean && flutter pub get && flutter build apk --debug`.
   Completion criterion: output ends with `Built build/app/outputs/flutter-apk/app-debug.apk`.
4. **If Dart APIs changed** (e.g. after a package downgrade), fix call sites and re-run `flutter analyze` + `flutter test` until both are clean.

## Symptom table

| Blame line | Diagnosis | Fix |
|---|---|---|
| `NullPointerException` in Gradle / `Could not apply plugin` / AGP 9-era errors | Flutter template shipped AGP 9.0.1 + Gradle 9.1; some pub plugins (older DSL) are incompatible with AGP 9 | Pin AGP 8.9.1 in `android/settings.gradle.kts` and Gradle 8.14.3 in `android/gradle/wrapper/gradle-wrapper.properties`; re-run the build |
| Plugin error mentioning `namespace` or DSL from 2021 (e.g. `file_picker 3.0.4`) | Plugin version pinned far too old (no `namespace`, no modern DSL) | Upgrade the plugin to a current major (`flutter pub add file_picker:^10.0.0`); watch for transitive conflicts and adjust neighbors (e.g. `flutter_secure_storage:^10`) |
| Runtime `Couldn't resolve native function 'sqlite3_initialize'` / `No available native assets` | `sqlite3` 3.x needs native-assets build hooks; `sqlite3_flutter_libs 0.6.0+eol` is an empty stub that bundles no lib | Downgrade to `sqlite3:^2.9.0` + `sqlite3_flutter_libs:^0.5.28` (classic bundling, FTS5 works); note `close()` → `dispose()` in 2.x |
| `ENOSPC: no space left on device` / Gradle `Could not download` (403/404) / pub cache missing packages | Disk full (often >95%); partially-written caches corrupt `.pub-cache` | Free space (`df -h`, prune `~/.gradle/wrapper/dists`, `build/`), then `flutter pub get` to re-download missing packages; rerun build |
| `.pub-cache` missing packages after an interrupted run | Corrupted cache from an earlier ENOSPC/crash | Run `flutter pub get` (it re-fetches); verify with `flutter analyze` |

## Reference

- **Env stack that worked here**: AGP 8.9.1 + Gradle 8.14.3, `flutter_secure_storage ^10`, `file_picker ^10`, `sqlite3 ^2.9` + `sqlite3_flutter_libs ^0.5`, minSdk 23.
- A debug APK is ~150MB; installs over wifi adb are slow but fine (300s timeout).
- Check disk pressure before blaming the network: `df -h /System/Volumes/Data` — most "download failed" errors on a full disk are ENOSPC in disguise.

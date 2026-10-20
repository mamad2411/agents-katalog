---
name: flutter-impeller
description: >
  Work with Flutter Impeller rendering backend: enable/disable flags, platform support,
  shader/runtime implications, performance debugging, and fallback to Skia. Use when
  optimizing owned Flutter apps' graphics performance, diagnosing Impeller-specific
  visual bugs, or validating rendering on iOS/Android/desktop targets.
---

# Flutter Impeller

## Scope And Authorization

- **In scope:** Flutter applications you own or are authorized to modify/profile.
- **Out of scope:** reverse engineering third-party apps solely to abuse rendering pipelines.
- Profile on real devices; lab builds preferred for experiments.
- Pair Dart/UI changes with `code-quality-standards` and Flutter security skills when shipping.

## When To Use

- Enabling or troubleshooting **Impeller** as Flutter’s rendering engine.
- Investigating jank, shader compilation stutters (historically Skia), or Impeller regressions.
- Platform differences (iOS Metal, Android Vulkan/OpenGL paths as supported by your Flutter version).
- Comparing Impeller vs Skia for a release train.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Flutter security (storage, channels, pinning) | `flutter-security-basics` |
| Secure storage plugin ops | `flutter-secure-storage-ops` |
| Flutter web Wasm | `flutter-wasm-web` |
| General frontend design system | `frontend-design` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Topic | Notes |
| --- | --- |
| Impeller | Flutter’s modern renderer aiming for predictable performance |
| Skia | Legacy/default fallback path depending on version/platform flags |
| Flags | `--enable-impeller`, manifest metadata, engine switches (version-specific) |
| Debug | DevTools performance, GPU frame times, Impeller-specific issues trackers |
| Art | Custom shaders, `FragmentProgram`, complex blur/saveLayer costs still matter |

## Enablement cheat sheet (version-sensitive)

```bash
flutter --version
# Run with Impeller (example flags — verify for your Flutter SDK)
flutter run --enable-impeller
# Disable when isolating bugs
flutter run --no-enable-impeller
```

```xml
<!-- Android manifest metadata examples have varied by Flutter release; confirm current docs -->
<!-- meta-data android:name="io.flutter.embedding.android.EnableImpeller" android:value="true" /> -->
```

```text
iOS: Impeller often default on recent Flutter iOS; check release notes for your channel
```

## Workflow

### 1. Confirm scope and success criteria

1. Flutter SDK channel/version, target platforms, devices in test matrix.
2. Success: target FPS on critical screens; no unacceptable visual diffs; crash-free GPU path.
3. Define baseline metrics before toggling renderer.

### 2. Inventory current renderer

```bash
flutter doctor -v
# Note whether Impeller enabled in run logs / observatory
```

1. Check project flags in `AndroidManifest.xml`, iOS Info settings, CI build scripts.
2. List screens with heavy effects (blur, backdrop filter, custom paint, video).

### 3. Baseline performance (Skia vs Impeller)

1. Record frame build/raster times on the same device/build mode (profile/release, not debug-only conclusions).
2. Capture screenshots for visual regression of text, shadows, gradients, clips.
3. Note shader jank occurrence rates on first navigation.

### 4. Apply Impeller-focused changes

1. Enable Impeller intentionally per platform in release configs once validated.
2. Fix widgets that regress: simplify `saveLayer`, reduce oversized blurs, prefer efficient compositing.
3. Custom shaders: retest compilation and uniforms under Impeller.
4. Keep a documented **kill switch** (`--no-enable-impeller` or metadata) for emergency rollback.
5. Avoid drawing conclusions from debug mode only.

### 5. Verify with evidence

```bash
flutter run --profile --enable-impeller -d <device>
# Use DevTools Performance: build/raster, jank frames
# Golden/screenshot tests for critical UI if you maintain them
```

| Check | Pass |
| --- | --- |
| FPS on scroll-heavy list | Meets budget |
| Text clarity | No unexpected blur/gamma issues |
| Animations | No new flicker |
| Startup | Acceptable first frames |

### 6. Observe and harden

1. Crash reporting filtered by GPU/renderer tags if available.
2. Track Impeller bugs against Flutter GitHub for your exact version.
3. Re-validate on OS upgrades (Metal/Vulkan driver changes).

### 7. Hand off

1. Document enablement method per platform and Flutter version pin.
2. Record known visual exceptions and owners.
3. Apply `code-quality-standards` for widget fixes.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Measurement | Profile/release on device | Debug-only FPS claims |
| Rollout | Staged + kill switch | Force Impeller all devices untested |
| Fixes | Reduce layer explosion | Random opacity hacks without metrics |
| Versioning | Pin Flutter, read notes | Assume flags eternal |
| Security | N/A primary | Using this skill instead of secure storage review |
| Web | Check if Impeller applies | Confuse with `flutter-wasm-web` |

## Output Checklist

- [ ] Flutter version/channel and devices recorded
- [ ] Current enablement flags inventoried
- [ ] Before/after performance metrics captured
- [ ] Visual regressions checked
- [ ] Kill switch documented
- [ ] Critical screens optimized if needed
- [ ] CI/profile instructions updated
- [ ] `code-quality-standards` applied

## Rules

- Owned apps; evidence from profile/release builds.
- Renderer flags change across Flutter releases—verify against current docs for your pin.
- This skill is graphics/runtime performance, not mobile app auth security.
- Route security reviews to `flutter-security-basics`.

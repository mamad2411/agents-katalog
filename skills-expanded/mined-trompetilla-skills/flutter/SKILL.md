---
name: Flutter
description: Build performant cross-platform apps with Flutter widgets, state management, and platform integration.
metadata: {"clawdbot":{"emoji":"🦋","requires":{"bins":["flutter"]},"os":["linux","darwin","win32"]}}
---

# Flutter Development Rules

## Widget Building
- `const` constructors prevent unnecessary rebuilds — use `const` on every widget that doesn't depend on runtime values
- Split large `build()` methods into smaller widgets, not helper methods — methods rebuild every time, widgets can skip rebuilds
- `ListView.builder` for long lists, never `Column` with `children` — Column loads everything in memory, builder is lazy
- Keys are required when widget identity matters — lists with reordering, state preservation across tree changes
- Avoid `setState` inside `build()` — causes infinite rebuild loop

## State Management
- `setState` is fine for single-widget local state — don't over-engineer simple toggles or form fields
- Lift state up only to lowest common ancestor — higher than necessary causes broader rebuilds
- `ValueNotifier` + `ValueListenableBuilder` is lighter than full state management for simple cases
- Provider/Riverpod: keep providers small and focused — one giant provider defeats selective rebuilding
- Avoid storing derived data in state — compute it in build from source state

## Performance
- `RepaintBoundary` isolates expensive repaints — wrap complex animations or frequently updating widgets
- `const` widgets are cached globally — same `const Text('Hello')` is identical instance across entire app
- Opacity widget is expensive — use `AnimatedOpacity` or `FadeTransition` for animations, or color alpha for static cases
- Images: use `cacheWidth`/`cacheHeight` to decode at display size — full resolution wastes memory
- `flutter run --profile` reveals real performance — debug mode is 10x slower and not representative

## Common Mistakes
- `FutureBuilder` rebuilds on every parent rebuild — cache the Future in `initState`, don't create inline
- `MediaQuery.of(context)` causes rebuild on any media change — use specific queries like `MediaQuery.sizeOf(context)`
- Async gap: check `mounted` before `setState` after await — widget might be disposed
- `TextEditingController` needs disposal — create in `initState`, dispose in `dispose`, never in `build`
- Nested `SingleChildScrollView` with unbounded children fails — wrap inner content with `ConstrainedBox` or use `shrinkWrap`

## Navigation
- Go Router or Navigator 2.0 for deep linking and web — basic Navigator doesn't handle URLs properly
- Pass data via route parameters, not constructor arguments for named routes — survives app restart and URL sharing
- Avoid storing navigation state in global state management — router handles this, duplication causes sync bugs
- `WillPopScope` (or `PopScope` in Flutter 3.16+) to handle back button — confirm before discarding unsaved changes

## Platform Integration
- Method channels are async — can't use in synchronous widget lifecycle methods without `then` or `await`
- Request permissions before using platform features — handle denied state gracefully, don't assume granted
- Platform-specific code goes in separate files with `.android.dart` / `.ios.dart` suffix — conditional imports keep it clean
- Test on real devices — emulators miss permission dialogs, performance characteristics, and sensor behavior

## Build & Release
- `flutter clean` fixes most unexplainable build failures — derived files get corrupted often
- iOS: `pod deintegrate && pod install` when CocoaPods misbehaves — faster than debugging dependency resolution
- Flavors/schemes for environment switching — don't hardcode API URLs, use `--dart-define` or flavor-specific configs
- Obfuscation (`--obfuscate --split-debug-info`) for release builds — protects business logic, requires keeping debug symbols for crash reports
- `flutter build` defaults to release mode — no need for `--release` flag, but `--debug` is needed for debug builds

## Testing
- Widget tests are faster than integration tests — use them for UI logic, save integration for critical flows
- `pumpAndSettle` waits for animations — but hangs on infinite animations, use `pump(duration)` instead
- Mock platform channels with `TestDefaultBinaryMessengerBinding` — real channels fail in tests
- Golden tests catch visual regressions — regenerate with `--update-goldens` when intentional changes happen

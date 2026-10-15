---
name: flutter-startup-gate
description: Use when a Flutter app crashes at startup with a LateInitializationError or when widgets read a field before async init (database open, service wiring) completes. Add an init gate that renders a splash until initialized, an error screen with retry on failure, and guards against double-init.
---

# Flutter startup gate

Stop startup crashes where the UI reads a `late` field before an async `init()` has assigned it. The fix is a **gate** in the root widget: render a splash until `initialized`, an error screen with retry when init fails, and the app shell only after.

## Steps

1. **Confirm the race.** The crash `LateInitializationError: Field 'repo' has not been initialized` (or similar) means a widget read a `late` field in the first frame, before `init()`'s awaits finished. It may pass on a fast host and only crash on slow real devices — check `logcat` for `E/flutter` on-device.
2. **Add an init gate to the root widget** (`app.dart`):
   - While `initializing` → show a splash (logo + spinner + "Opening…").
   - If `error != null` → show an error screen with a **Retry** button (do not crash).
   - Only when `initialized` → show the app shell.
   Completion criterion: every first-frame widget sits behind the gate; none touch `repo`/services before the gate opens.
3. **Guard against double-init.** Add a `_initStarted` flag so `init()` can't run twice (hot reload / retry). Expose `retryInit()` that resets state and re-runs `init()`.
   Completion criterion: tapping Retry re-runs init and reaches the shell without a second manual launch.
4. **Verify.** `flutter analyze` clean; `flutter test` passes; reinstall on the real device and confirm logcat shows no `LateInitializationError` on cold start (see `flutter-device-smoke-test`).

## Reference

- Root cause pattern: `AppState.init()` is async (opens SQLite, wires services, assigns `late` fields); `MaterialApp` builds and screens call `app.repo...` in `build()` before the first await resolves.
- The gate doubles as a user-visible loading state and an error boundary — both needed on slow devices.

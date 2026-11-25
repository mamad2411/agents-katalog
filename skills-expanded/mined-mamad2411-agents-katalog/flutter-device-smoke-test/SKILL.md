---
name: flutter-device-smoke-test
description: Use when testing a Flutter app on a real Android device via adb (install APK, launch, verify UI, check logcat for crashes, verify storage created). Covers wireless adb, run-as data inspection, screenshot capture, and evidence-based checks that the app truly works on-device.
---

# Flutter device smoke test

Verify a Flutter app works on a real Android device, producing an **evidence line** for each claim — a command whose output proves the step happened (a pid, a file, a clean logcat). No assertion without its evidence line.

## Steps

1. **Connect.** `adb devices -l` to list; for a wireless device use `adb connect <ip>:<port>`.
   Completion: your device serial appears and `adb -s <serial> get-state` prints `device`.
2. **Install the APK.** `adb -s <serial> install -r build/app/outputs/flutter-apk/app-debug.apk`.
   Completion: output contains `Success`. A 150MB debug APK over wifi takes minutes — give the command a 300s timeout.
3. **Launch.** `adb -s <serial> shell am start -n <packageId>/.MainActivity`, wait ~5s.
   Completion: `adb -s <serial> shell pidof <packageId>` returns a pid.
4. **Check for crashes.** `adb -s <serial> logcat -d | grep -E 'E/flutter|FATAL|AndroidRuntime|Unhandled|LateInitialization|sqlite' | tail -20`.
   Completion: no `FATAL`/`AndroidRuntime`/`E/flutter` lines from your app (ignore other apps' sqlite logs — scope by package or filter them out).
5. **Verify the UI rendered.** Screenshot: `adb -s <serial> exec-out screencap -p > /tmp/app.png`; confirm `file /tmp/app.png` reports a PNG with device resolution.
   Note: `uiautomator dump` shows **no text** for Flutter apps unless accessibility is enabled — the screenshot, not uiautomator, is the evidence.
6. **Verify storage was created.** Inspect the app's private dir:
   `adb -s <serial> shell run-as <packageId> ls -la app_flutter/` then `find app_flutter/<wikiRoot> -type f`.
   Completion: expected files exist (e.g. `index.sqlite`, `wiki.yaml`). **Quoting trap**: `run-as pkg sh -c '...'` mangles nested quotes through adb — pass one simple command at a time, and inspect `app_flutter/` (path_provider's documents dir) not `files/`.

## Crash-fix loop

When step 4 shows a crash, find the **blame line** in logcat (a `LateInitializationError`, a native-symbol error like `sqlite3_initialize`, etc.), fix the code, rebuild (`flutter build apk --debug`), reinstall, relaunch, and re-verify. Some crashes only reproduce on slow real devices — a clean host test suite is not evidence the device is fine.

## Reference

- **Race on slow devices**: async init (DB open, service wiring) may not finish before the first frame renders → `LateInitializationError: Field 'x' has not been initialized`. Fix with a splash gate — see the `flutter-async-init-gate` skill.
- **Missing native symbol at runtime** (e.g. `sqlite3_initialize`) is a packaging problem — see `flutter-android-build-triage`.
- Device used here: Samsung Galaxy A04, wireless adb `192.168.0.101:33929`.

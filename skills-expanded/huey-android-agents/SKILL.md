# huey-android

Minimal Android app for toggling Hue rooms and zones.

## Commands

Use the Makefile for routine work:

- `make compile` — build debug APK (`app/build/outputs/apk/debug/app-debug.apk`)
- `make build` — alias for `make compile`
- `make test` — run debug unit tests
- `make lint` — run Android lint
- `make verify` — run full Gradle checks
- `make devices` — list connected Android devices
- `make deploy` — build + install debug APK on connected device
- `make deploy DEVICE=<serial>` — target a specific device
- `make uninstall` — uninstall app from connected device
- `make uninstall DEVICE=<serial>` — target a specific device
- `make clean` — clean build artifacts

## Environment

- Java 21 is required for this project (AGP compatibility).
- On macOS, the Makefile auto-resolves Java 21 via `/usr/libexec/java_home -v 21`.
- `adb` (Android platform-tools) is required for deploy/uninstall/device listing.
- If no phone is connected, `make deploy` fails with a clear error so you can retry later.

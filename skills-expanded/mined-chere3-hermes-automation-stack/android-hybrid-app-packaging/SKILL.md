---
name: android-hybrid-app-packaging
description: Package and verify React/Vite or similar web applications as installable Android APKs with Capacitor, including private API connectivity, network policy, signing checks, and device validation.
version: 1.0.0
platforms: [linux]
tags: [android, apk, capacitor, vite, react, gradle, mobile]
---

# Android Hybrid App Packaging

Use this skill when a web application must be delivered as an installable Android APK rather than merely described or hosted.

## User-facing standard

For this user, prefer a directly attachable APK when viable. Preserve Material Design hierarchy, responsive behavior, and information density appropriate for a phone; do not ship a cluttered desktop dashboard inside a WebView. State clearly whether the APK is debug-signed or release-signed and whether it requires Tailscale or another private network.

## Workflow

1. **Choose the runtime architecture before wrapping**
   - A Capacitor APK packages frontend assets, not a Python/Node backend.
   - Decide whether data processing will run in TypeScript on-device or through a reachable backend.
   - If continuous BLE scanning, Android foreground services, Room, WorkManager, Keystore-backed device identity, or precise process/permission lifecycle handling are central requirements, prefer a native Kotlin/Jetpack Compose app rather than forcing the feature through a WebView bridge. The signing, network-boundary, artifact-verification, device-validation, and cleanup rules in this skill still apply; skip Capacitor-specific steps.
   - If using a private backend, bind it only to the intended private interface and document the network prerequisite.
   - Never ship an APK whose frontend still calls relative `/api` unless that API is actually served inside the app.

2. **Align toolchain versions**
   - Keep `@capacitor/core`, `@capacitor/android`, and `@capacitor/cli` on the same major version.
   - Check Node, JDK, Gradle wrapper, Android platform, and build-tools compatibility before the full build.
   - Use an isolated supported JDK via `JAVA_HOME` rather than changing the system default.
   - Reuse an already licensed Android SDK when available; do not accept SDK legal terms on the user's behalf.

3. **Build web assets specifically for mobile**
   - Use a typed build-time API base such as `VITE_API_BASE` and include `/// <reference types="vite/client" />`.
   - Chain build and sync with `&&`; never let `cap sync` copy stale assets after a failed TypeScript build.
   - Run frontend tests and a production build before `npx cap sync android`.
   - Lazy-load heavy charting libraries to keep the initial bundle manageable.

4. **Configure Capacitor**
   - Set a stable reverse-DNS `appId`, human-readable `appName`, and correct `webDir`.
   - Use packaged assets rather than a remote `server.url` unless remote hosting is an explicit product requirement.
   - Configure Android background color and mixed-content behavior only when required.

5. **Constrain private HTTP connectivity**
   - Prefer HTTPS. If a Tailscale-only HTTP API is necessary, do not enable global cleartext traffic.
   - Add an Android `network_security_config.xml` that denies cleartext by default and permits only the exact private host.
   - Reference it from `AndroidManifest.xml` and retain only `INTERNET` unless more permissions are genuinely needed.
   - Backend CORS must allow the exact Capacitor origin (`capacitor://localhost`) and only necessary methods/headers.
   - Verify the API using the same `Origin` header before packaging.

6. **Build the APK**
   - Export `JAVA_HOME`, `ANDROID_HOME`, and `ANDROID_SDK_ROOT` explicitly.
   - Run `./gradlew assembleDebug --no-daemon` for an installable development artifact.
   - For public distribution, create a separately managed release keystore and build a release artifact; never present a debug APK as Play Store ready.

7. **Verify the artifact, not just Gradle output**
   - `apksigner verify --verbose --print-certs APP.apk`
   - `aapt dump badging APP.apk` to confirm package, version, SDK levels, label, and permissions.
   - Inspect the APK ZIP to confirm current web assets and the intended API base are embedded.
   - Inspect the compiled manifest to confirm `networkSecurityConfig` and `INTERNET`.
   - Calculate SHA-256 and file size.
   - If a device is attached, install with `adb install -r` and exercise loading, filtering, rotation, external links, and network loss.
   - If no device is attached, say explicitly that physical runtime validation was not performed.

8. **Operational cleanup**
   - Stop temporary Vite/Uvicorn servers and `adb` daemon.
   - Keep a backend service persistent only when it is part of the APK architecture.
   - Verify that the persistent service is active and restricted to the private interface.
   - Deliver the APK as a native attachment and put install/network instructions at the end.

## Persistent BLE/background collectors

For native collectors that users expect to run continuously:

- Start collection from an explicit user action and persist the enabled state. A visible foreground-service notification is part of the product contract, not an implementation detail.
- Use the exact foreground-service type and modern Bluetooth permissions. Do not hide the notification or use accessibility/device-admin mechanisms to evade lifecycle policy.
- Persist observations locally before upload. Use WorkManager for retryable, idempotent network delivery rather than coupling data durability to the scanner process.
- A boot receiver may restore a previously enabled collector only when Android permits that service type to start from `BOOT_COMPLETED`. Catch background-start denial and expose `requires_intervention` instead of retry loops.
- Never promise literal permanence: force-stop, revoked permissions, Bluetooth-off state and OEM battery policy can stop collection. Represent these as explicit health states and verify them on the physical target device.
- Ask for battery-optimization exemption only when runtime evidence demonstrates that the OEM is killing the collector; do not request broad exemptions preemptively.
- Exercise process death, reboot, Doze, offline queueing, permission revocation, user-stopped foreground service and Bluetooth toggles before calling the app durable.

## Common pitfalls

- Capacitor CLI major differs from Core/Android major.
- `cap sync` runs after a failed frontend build and silently packages stale `dist/` content.
- Gradle runs under a too-new JDK and fails with `Unsupported class file major version`.
- Android SDK environment points at an incomplete SDK while a complete SDK exists elsewhere.
- Capacitor configuration says `cleartext: true`, but the generated manifest still blocks HTTP.
- Global `usesCleartextTraffic=true` is used where an exact-host network policy would suffice.
- The app works in desktop Vite because of its proxy but fails in Android because `/api` points at the WebView origin.
- `set -o pipefail` combined with `aapt ... | head` yields SIGPIPE/141 and skips later verification commands.
- A Gradle `BUILD SUCCESSFUL` is reported without checking signature, embedded assets, API reachability, or installability.

## Verification checklist

- [ ] Capacitor package majors aligned.
- [ ] Supported isolated JDK selected.
- [ ] Frontend tests pass.
- [ ] Backend tests pass.
- [ ] Mobile production build contains the intended API base.
- [ ] `cap sync` ran only after a successful build.
- [ ] Private API responds with exact Capacitor CORS origin.
- [ ] Network security policy is exact-host, deny-by-default.
- [ ] Gradle build succeeds.
- [ ] APK signature verifies.
- [ ] Package metadata and permissions are correct.
- [ ] SHA-256 and size recorded.
- [ ] Device validation completed or its absence disclosed.
- [ ] Continuous collectors expose visible notification and lifecycle health states.
- [ ] Reboot/process-death/Doze/permission-revocation/offline-queue behavior verified on device.
- [ ] Temporary processes cleaned up.

See `references/capacitor-private-api-checklist.md` for a concise command-oriented checklist.

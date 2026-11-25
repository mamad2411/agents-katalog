---
name: mobile-testing
description: Automated Android app testing on an emulator — connect to an AVD, drive the UI (tap/swipe/type/keys/deep links), read the UI/accessibility tree, capture screenshots/recordings and logcat, capture/mock/intercept the app's HTTP(S) traffic in-process (Frida OkHttp hook — no proxy/CA, pinning bypassed) and pin a W3C trace id, and verify app state. Use for testing Android apps, mobile UI flows, login/checkout on Android, or emulator-based verification. Emulator only (no physical devices, no iOS); network capture/mocking needs a rootable emulator image. For web pages use browser-testing; for server APIs use backend-testing.
allowed-tools: Bash(ironbee-android-devtools-cli:*)
---

# Mobile Testing Skill

Automated Android app testing on an emulator using the [Android DevTools CLI](../ironbee-android-devtools-cli/SKILL.md). Drives an AVD over `adb`: connect, act on the UI, read the UI/accessibility tree, capture screenshots/recordings/logcat, and verify.

## When to Use

This skill activates when:
- User asks to test an Android app or mobile UI flow
- User wants to automate taps/swipes/typing on an emulator
- User needs to verify Android app behavior (navigation, forms, login/checkout)
- User wants to capture logcat or app performance during a flow
- User wants to inspect, mock, or intercept the app's HTTP(S) requests, or correlate them to a backend by trace id
- User mentions an AVD, emulator, deep link, or `adb`

Emulator only — no physical devices, no iOS. For web pages use [browser-testing](../browser-testing/SKILL.md); for server APIs use [backend-testing](../backend-testing/SKILL.md).

## Verification model

There is no assert tool. Trigger an action, then read raw observations and judge for yourself. Default to the UI tree (`a11y take-ui-snapshot`) — it is structured, gives stable `ref`s, and is the cheap way to confirm state. Screenshot only for visual-only state or once after a screen change, not after every step.

## Capabilities

### Connect & app lifecycle
```bash
ironbee-android-devtools-cli --json device list-targets
ironbee-android-devtools-cli device connect --serial emulator-5554
ironbee-android-devtools-cli device connect --launch-mode managed --avd-name Pixel_7_API_34
ironbee-android-devtools-cli device launch-app --package-name com.example.app
ironbee-android-devtools-cli device terminate-app --package-name com.example.app
ironbee-android-devtools-cli device set-orientation --orientation landscape
ironbee-android-devtools-cli device disconnect
```

### Read the UI
```bash
ironbee-android-devtools-cli --json a11y take-ui-snapshot
ironbee-android-devtools-cli --json a11y find-element --text "Sign in"
```

### Interact (prefer ref/selector over pixels)
```bash
ironbee-android-devtools-cli interaction tap --ref e5
ironbee-android-devtools-cli interaction tap --text "Sign in"
ironbee-android-devtools-cli interaction input-text --resource-id "com.example.app:id/email" --text "a@b.com"
ironbee-android-devtools-cli interaction scroll --direction down
ironbee-android-devtools-cli interaction swipe --x1 540 --y1 1600 --x2 540 --y2 400
ironbee-android-devtools-cli interaction long-press --ref e9
ironbee-android-devtools-cli interaction press-key --key BACK
ironbee-android-devtools-cli interaction deep-link --uri "myapp://product/42"
```

### Synchronize
```bash
ironbee-android-devtools-cli sync wait-for-network-idle
```

### Capture & observe
```bash
ironbee-android-devtools-cli content take-screenshot --name after-login
ironbee-android-devtools-cli content start-recording
ironbee-android-devtools-cli content stop-recording --name checkout-flow
ironbee-android-devtools-cli --json o11y log-read --tail 200 --level ERROR
ironbee-android-devtools-cli --json o11y get-perf-metrics --package-name com.example.app --activity .MainActivity
```

### Capture / mock app HTTP traffic (Frida OkHttp hook; rootable emulator)
Network capture is **forward-looking** — start it, trigger traffic, then read. The first `get-http-requests` call starts capture; OkHttp-based stacks only (React Native/Expo, Retrofit, `HttpURLConnection`); native/Flutter/Cronet are not covered.
```bash
ironbee-android-devtools-cli --json o11y new-trace-id                 # pin a trace id for backend correlation
ironbee-android-devtools-cli --json o11y get-http-requests            # first call starts capture
ironbee-android-devtools-cli --json o11y get-http-requests --url-pattern "*/api/*" --include-headers --include-bodies
ironbee-android-devtools-cli --json stub mock-http-response --url-glob "https://api.example.com/me" --status 200 --body '{"name":"Alice"}'
ironbee-android-devtools-cli --json stub intercept-http-request --url-glob "https://api.example.com/*" --set-headers '{"X-Test":"1"}'
ironbee-android-devtools-cli --json stub list
ironbee-android-devtools-cli stub clear
```

## Basic Testing Workflow

1. **Connect**: `device list-targets` then `device connect` (attach by serial, or managed by AVD).
2. **Launch**: `device launch-app --package-name`.
3. **Snapshot**: `a11y take-ui-snapshot` to get refs (e1, e2) for stable targeting.
4. **Interact**: tap/input-text/scroll using `--ref` or a selector (`--resource-id`/`--text`/`--content-desc`).
5. **Sync**: `sync wait-for-network-idle` after actions that fetch data.
6. **Verify**: re-read the UI tree (or screenshot for visual-only state).
7. **Document**: report results.

## End-to-End: login flow with logcat correlation

```bash
SESSION="--session-id login"

ironbee-android-devtools-cli $SESSION device connect --serial emulator-5554
ironbee-android-devtools-cli $SESSION device launch-app --package-name com.example.app

# Stream logcat from now on; capture the followId from the output
ironbee-android-devtools-cli $SESSION --json o11y log-follow

# Find fields, type, submit
ironbee-android-devtools-cli $SESSION --json a11y take-ui-snapshot
ironbee-android-devtools-cli $SESSION interaction input-text --resource-id "com.example.app:id/username" --text "alice"
ironbee-android-devtools-cli $SESSION interaction input-text --resource-id "com.example.app:id/password" --text "secret"
ironbee-android-devtools-cli $SESSION interaction tap --text "Sign in"

# Let traffic settle, then verify UI + check for errors in the buffered logs
ironbee-android-devtools-cli $SESSION sync wait-for-network-idle
ironbee-android-devtools-cli $SESSION --json a11y take-ui-snapshot
ironbee-android-devtools-cli $SESSION --json o11y log-get-followed --follow-id <id> --level ERROR

# Cleanup
ironbee-android-devtools-cli $SESSION o11y log-stop-follow --follow-id <id>
ironbee-android-devtools-cli session delete login
```

## End-to-End: deep link into a screen and verify

```bash
SESSION="--session-id deeplink"

ironbee-android-devtools-cli $SESSION device connect --serial emulator-5554
ironbee-android-devtools-cli $SESSION interaction deep-link --uri "myapp://product/42" --package-name com.example.app
ironbee-android-devtools-cli $SESSION sync wait-for-network-idle
ironbee-android-devtools-cli $SESSION --json a11y find-element --text "Add to cart"
```

## Best Practices

1. **Use sessions** (`--session-id`) for multi-step flows — the emulator connection is pinned to the session.
2. **Prefer the UI tree over screenshots** — it is structured, cheaper, and gives stable refs.
3. **Target by ref or selector**, not pixels — pixels break across screen sizes and layout changes.
4. **Wait for network idle** after actions that fetch data, before reading state.
5. **Terminate the app** (`device terminate-app`) to reset state between trigger-and-verify cycles.
6. **Treat emulator perf as comparative only** — `o11y get-perf-metrics` numbers are not real-device representative.
7. **Disconnect**: in `managed` mode `device disconnect` shuts the AVD down; in `attach` mode it leaves it running.
8. **Batch long flows** with `run execute --code "..."` and `callTool()` to cut round-trips (only `callTool` is available — no `page`).

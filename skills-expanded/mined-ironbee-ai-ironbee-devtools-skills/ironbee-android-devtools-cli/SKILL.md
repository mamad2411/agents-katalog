---
name: ironbee-android-devtools-cli
description: CLI for driving an Android emulator (AVD) over adb. Use when the user needs to connect to an emulator (attach to a running one or boot/manage an AVD), tap/swipe/type on the UI, read the UI/accessibility tree, take screenshots or screen recordings, capture logcat, capture HTTP(S) requests in-process (Frida OkHttp hook — no proxy/CA, pinning bypassed), mock/intercept HTTP responses, pin a W3C trace id across app API calls, measure app performance, wait for network idle, or compare a screen against a Figma design. Emulator-only (no physical devices, no on-device tracepoints); network capture/mocking needs a rootable emulator image. Requires daemon; connect a device before other commands. Also covers the creds-gated Jira and Linear issue-tracker domains: fetch/search issues, download attachments, attach evidence, comment, transition/set state, and report verification results back to the tracker.
allowed-tools: Bash(ironbee-android-devtools-cli:*)
---

# IronBee Android DevTools CLI

Command-line interface for driving an Android emulator over a single bridge — `adb`. Part of [IronBee DevTools](https://github.com/ironbee-ai/ironbee-devtools). Collects the same data categories as the other platforms — screenshots, video, logs (logcat), the UI/accessibility tree, and performance metrics — and drives the UI via taps, swipes, key events, text input, and deep links.

It also captures HTTP(S) traffic **in-process via a Frida OkHttp hook** — no proxy, no CA install, certificate pinning bypassed — and can mock or intercept those requests and pin a W3C trace id across the app's API calls. This path covers OkHttp-based stacks (React Native/Expo, Retrofit, Android `HttpURLConnection`) over HTTP/1.1 and HTTP/2; native / Flutter / Cronet are not covered. It provisions `frida-server` on first use, so it needs a **rootable emulator image** (Google APIs or AOSP — not a Play Store image).

Scope: **Android emulator only.** Physical devices and on-device debugging (tracepoints/logpoints/etc.) are out of scope. For browser UIs use [../ironbee-browser-devtools-cli/SKILL.md](../ironbee-browser-devtools-cli/SKILL.md); for Node.js processes use [../ironbee-node-devtools-cli/SKILL.md](../ironbee-node-devtools-cli/SKILL.md); for server APIs use [../ironbee-backend-devtools-cli/SKILL.md](../ironbee-backend-devtools-cli/SKILL.md).

## Installation

```bash
# Install this skill (skills.sh)
npx skills add ironbee-ai/ironbee-devtools-skills

# Install the CLI binary (same package as the rest of IronBee DevTools)
npm install -g @ironbee-ai/devtools
```

Requires **Node.js >= 22.16.0** (`engines.node` in the package): the backend `db` domain's SQLite engine and the `FTS5` scenario-search strategy run on Node's built-in `node:sqlite`, which replaced the last native dependency.


You also need the Android SDK with `adb` (and `emulator` for managed mode). The CLI resolves them from `ANDROID_HOME` / `ANDROID_SDK_ROOT` or the OS-default SDK location (macOS `~/Library/Android/sdk`, Windows `%LOCALAPPDATA%\Android\Sdk`, Linux `~/Android/Sdk`). Override with `ANDROID_ADB_PATH` / `ANDROID_EMULATOR_PATH` if they live elsewhere.

## Port note

All IronBee DevTools CLIs default to daemon port `2020`. To run the Android daemon alongside browser (2020), node (2021), and backend (2022) daemons, start it on its own port and pass `--port` to every Android CLI call:

```bash
PLATFORM=android ironbee-android-devtools-cli daemon start --port 2023
ironbee-android-devtools-cli --port 2023 device list-targets
```

## Quick Start

```bash
# 1. Start daemon (if not running)
ironbee-android-devtools-cli daemon start

# 2. List connectable targets (running emulators + defined AVDs)
ironbee-android-devtools-cli --json device list-targets

# 3. Connect (attach to a running emulator by serial)
ironbee-android-devtools-cli --session-id my-app device connect --serial emulator-5554

# 4. Launch the app under test
ironbee-android-devtools-cli --session-id my-app device launch-app --package-name com.example.app

# 5. Read the UI tree (structured, gives refs)
ironbee-android-devtools-cli --session-id my-app --json a11y take-ui-snapshot

# 6. Tap an element by ref, then re-read to verify
ironbee-android-devtools-cli --session-id my-app interaction tap --ref e5
ironbee-android-devtools-cli --session-id my-app --json a11y take-ui-snapshot
```

## Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `--port <number>` | Daemon server port | `2020` |
| `--session-id <string>` | Session for emulator connection persistence | auto |
| `--json` | Output as JSON (recommended for AI) | `false` |
| `--quiet` | Suppress log messages | `false` |
| `--verbose` | Enable debug output | `false` |
| `--timeout <ms>` | Operation timeout | `30000` |

**AI Agent Recommended:**

```bash
ironbee-android-devtools-cli --json --quiet --session-id "android-session" <command>
```

## Verification model (raw read → trigger → verify)

There is no assert tool. Trigger an action (tap, launch an app, deep link), then read raw observations and decide for yourself. Default to the UI tree (`a11y take-ui-snapshot`) — it is structured, gives stable `ref`s, and is the cheap way to confirm state. **Do NOT screenshot after every action**: `content take-screenshot` is heavy (capture + encode + upload). Take one only when the UI tree is insufficient (visual-only state: rendering, images, layout, custom-drawn views) or once to confirm after a screen change.

Emulator performance numbers are NOT representative of a real device (the emulator runs on the host CPU) — use `o11y get-perf-metrics` comparatively only.

## Tool Domains

| Domain | Description | Reference |
|--------|-------------|-----------|
| device | Connection and lifecycle (connect, disconnect, status, list-targets, launch-app, terminate-app, set-orientation) | [device](./references/device.md) |
| content | Screenshot and screen recording (take-screenshot, start-recording, stop-recording) | [content](./references/content.md) |
| a11y | UI/accessibility tree and element resolution (take-ui-snapshot, find-element) | [a11y](./references/a11y.md) |
| interaction | Tap, swipe, scroll, type, keys, deep links (tap, double-tap, long-press, swipe, scroll, input-text, press-key, deep-link) | [interaction](./references/interaction.md) |
| o11y | Logcat capture, in-process HTTP(S) capture, performance, W3C trace context (log-read, log-follow, log-get-followed, log-stop-follow, get-http-requests, get-perf-metrics, new-trace-id, set-trace-context, get-trace-context, get-trace, get-session-traces) | [o11y](./references/o11y.md) |
| stub | Proxy-free HTTP mocking / request interception via the Frida OkHttp hook (mock-http-response, intercept-http-request, list, clear) | [stub](./references/stub.md) |
| sync | Wait for emulator network idle (wait-for-network-idle) | [sync](./references/sync.md) |
| figma | Compare the current screen against a Figma design (compare-screen-with-design) | [figma](./references/figma.md) |
| execute | Batch tool calls via JavaScript (`run execute`; CLI and MCP). **Note:** only `callTool` is available inside the VM (no `page` binding — that is browser-only). | [execute](./references/execute.md) |
| jira | Jira issue tracker: intake, evidence, outcome, verification report (creds-gated shared domain; writes opt-in) | [jira](./references/jira.md) |
| linear | Linear issue tracker: intake, evidence, outcome, verification report (creds-gated shared domain; writes opt-in) | [linear](./references/linear.md) |

**Jira / Linear** are platform-agnostic shared issue-tracker domains (like scenario/execute) — registered on every platform CLI, but **only when credentials are configured**: jira needs `JIRA_BASE_URL` plus `JIRA_EMAIL` + `JIRA_API_TOKEN` (Cloud) or `JIRA_PAT` (Server/DC); linear needs `LINEAR_API_KEY`. Without creds the `jira` / `linear` subcommand group does not exist. Write tools (add-comment, attach-file, create/update-issue, transition-issue / set-state, link-issue, report-verification) additionally require `JIRA_WRITE_ENABLED=true` / `LINEAR_WRITE_ENABLED=true` (default off ⇒ read-only intake tools only). Close the loop after a verification run: `ironbee-android-devtools-cli jira report-verification --key PROJ-123 --result pass --report "..." --artifacts ./artifacts/evidence.png` (linear: same shape with `--state` instead of `--transition`). See [jira](./references/jira.md) / [linear](./references/linear.md).

**Full `scenario` surface on this CLI.** The Android CLI registers the scenario CRUD subcommands (`scenario-add` / `scenario-update` / `scenario-delete` / `scenario-list` / `scenario-search` / `scenario-recorded-actions`) plus a direct `scenario-run` subcommand under the `default` group — e.g. `ironbee-android-devtools-cli default scenario-run --name <name>` (with `--args` / `--param key=value` / `--timeout-ms`, and `--resume` / `--step-by-step` / `--refresh` for step-based scenarios). `scenario-run` is also reachable from inside `run execute` via `await callTool('scenario-run', { name: '...' })`. See the [scenario](./references/scenario.md) reference. Inside a scenario script only `callTool` is available (no `page` binding — that is browser-only).

## Connection model (one target per session)

Connect with `device connect`. Launch modes:

| Mode | What it does | On disconnect |
|------|--------------|---------------|
| `attach` (default) | Connect to an already-running emulator | Leaves it running |
| `managed` | Boot an AVD on connect | Shuts down the emulator it booted |

Target selection order: explicit `--serial` > the single running emulator > booting `--avd-name` (or `ANDROID_DEFAULT_AVD`). When multiple emulators are running and no serial/avd is given, connect fails and lists targets — enumerate them first with `device list-targets`.

## CLI Management Commands

### Daemon

```bash
ironbee-android-devtools-cli daemon status
ironbee-android-devtools-cli daemon start
ironbee-android-devtools-cli daemon stop
ironbee-android-devtools-cli daemon restart
ironbee-android-devtools-cli daemon info
```

### Session

```bash
ironbee-android-devtools-cli session list
ironbee-android-devtools-cli session info <session-id>
ironbee-android-devtools-cli session delete <session-id>
```

### Tools

```bash
ironbee-android-devtools-cli tools list
ironbee-android-devtools-cli tools search <query>
ironbee-android-devtools-cli tools info <tool-name>
```

### Config

```bash
ironbee-android-devtools-cli config
```

## Android-specific configuration

| Env var | Type | Default | Purpose |
|---------|------|---------|---------|
| `ANDROID_ADB_PATH` | string | (resolved from SDK) | Explicit path to the `adb` binary. |
| `ANDROID_EMULATOR_PATH` | string | (resolved from SDK) | Explicit path to the `emulator` binary (managed mode + AVD listing). |
| `ANDROID_DEFAULT_SERIAL` | string | (unset) | Default emulator serial for `device connect` when none is given. |
| `ANDROID_DEFAULT_AVD` | string | (unset) | Default AVD name to boot in `managed` mode when none is given. |
| `ANDROID_LOG_BUFFER_SIZE` | number | `1000` | Per-follower logcat ring-buffer line cap (`o11y log-follow`). |
| `ANDROID_LOG_REDACT_ENABLE` | boolean | `true` | Redact well-known secrets from logcat before returning lines. |
| `ANDROID_IME_ENABLE` | boolean | `true` | Route `interaction input-text` through an on-device IME (Unicode-safe) instead of adb keystrokes. |
| `ANDROID_FRIDA_SERVER_PATH` | string | (auto-download) | Explicit path to a `frida-server` binary for network capture; omit to let the daemon download/provision it. |
| `ANDROID_HTTP_CAPTURE_BUFFER_SIZE` | number | `1000` | Per-session ring-buffer cap for captured HTTP requests (`o11y get-http-requests`). Legacy fallback: `ANDROID_HTTP_REQUESTS_BUFFER_SIZE`. |
| `ANDROID_HTTP_CAPTURE_BODY_MAX_BYTES` | number | `262144` | Max captured request/response body size in bytes (larger bodies are truncated). Legacy fallback: `ANDROID_HTTP_BODY_MAX_BYTES`. |
| `ANDROID_HTTP_HEADERS_REDACT` | string (csv) | `authorization,cookie,x-api-key` | Header names redacted when `--include-headers` is set. |
| `ANDROID_HTTP_BODY_REDACT_KEYS` | string (csv) | `password,token,secret,…` | JSON body keys redacted recursively when `--include-bodies` is set. |

## Examples

### Trigger-and-verify a login flow

```bash
SESSION="--session-id login"

ironbee-android-devtools-cli $SESSION device connect --serial emulator-5554
ironbee-android-devtools-cli $SESSION device launch-app --package-name com.example.app

# Read the UI tree and find the username field
ironbee-android-devtools-cli $SESSION --json a11y take-ui-snapshot

# Type into fields, then tap login
ironbee-android-devtools-cli $SESSION interaction input-text --resource-id "com.example.app:id/username" --text "alice"
ironbee-android-devtools-cli $SESSION interaction input-text --resource-id "com.example.app:id/password" --text "secret"
ironbee-android-devtools-cli $SESSION interaction tap --text "Sign in"

# Wait for traffic to settle, then re-read to confirm
ironbee-android-devtools-cli $SESSION sync wait-for-network-idle
ironbee-android-devtools-cli $SESSION --json a11y take-ui-snapshot
```

### Correlate a UI action with logcat

```bash
SESSION="--session-id logs"

# Start following logcat, capture the followId
ironbee-android-devtools-cli $SESSION --json o11y log-follow

# Trigger the action
ironbee-android-devtools-cli $SESSION interaction tap --text "Checkout"

# Drain the buffered lines, filtered to errors
ironbee-android-devtools-cli $SESSION --json o11y log-get-followed --follow-id <id> --level ERROR
```

### Capture (and trace-correlate) app HTTP traffic

Network capture is forward-looking — start it, then trigger traffic, then read. Requires a rootable emulator image.

```bash
SESSION="--session-id net"

ironbee-android-devtools-cli $SESSION device connect --serial emulator-5554
ironbee-android-devtools-cli $SESSION device launch-app --package-name com.example.app

# Pin a trace id the backend can later be searched by, then start capture
ironbee-android-devtools-cli $SESSION --json o11y new-trace-id
ironbee-android-devtools-cli $SESSION --json o11y get-http-requests   # first call starts capture

# Trigger traffic in the app, then read what was captured (headers/bodies opt-in)
ironbee-android-devtools-cli $SESSION interaction tap --text "Refresh"
ironbee-android-devtools-cli $SESSION --json o11y get-http-requests --url-pattern "*/api/*" --include-headers --include-bodies
```

### Mock or intercept a response

```bash
# Short-circuit an endpoint with a canned response
ironbee-android-devtools-cli --json stub mock-http-response --url-glob "https://api.example.com/me" --status 200 --body '{"name":"Alice"}'

# Or mutate an outgoing request's headers
ironbee-android-devtools-cli --json stub intercept-http-request --url-glob "https://api.example.com/*" --set-headers '{"X-Test":"1"}'

ironbee-android-devtools-cli --json stub list
ironbee-android-devtools-cli stub clear
```

### Batch with execute

```bash
# Run multiple tool calls in one request — Android exposes only callTool (no `page`)
ironbee-android-devtools-cli run execute --code "await callTool('device_status', {}, true); await callTool('a11y_take-ui-snapshot', {}, true);"
```

## Interactive Mode

```bash
ironbee-android-devtools-cli interactive
```

| Command | Description |
|---------|-------------|
| `help` | Show commands |
| `exit`, `quit` | Exit |
| `device connect` | Connect to an emulator |
| `device status` | Connection status |
| `<domain> <tool>` | Execute tool |

## Shell Completions

```bash
eval "$(ironbee-android-devtools-cli completion bash)"
eval "$(ironbee-android-devtools-cli completion zsh)"
```

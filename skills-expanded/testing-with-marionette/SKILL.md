---
name: "testing-with-marionette"
description: "AI-driven Flutter E2E testing with Marionette (marionette_flutter in the app, marionette_cli or marionette_mcp to drive it). Control running Flutter apps in debug mode for smoke tests, regression checks, exploratory testing, and UI automation. Trigger when the user mentions E2E testing, UI automation, smoke tests, controlling a running Flutter app, VM Service interaction, tapping or entering text in an app, screenshots, log collection, session reports, or testing native dialogs, permissions, or WebViews. Supports named instances, direct VM service URIs, and MCP. Use for troubleshooting flaky UI flows, automating repetitive manual tests, verifying behavior after merges, and AI-agent-driven QA."
metadata:
  last_modified: "2026-11-10"
  package_versions: "marionette_cli 0.7.0, marionette_flutter 0.7.0, marionette_mcp 0.7.0 (verified against the CLI help-ai reference)"
---

# Marionette — AI Agent Reference

Marionette lets an agent drive a Flutter app that runs in debug mode. It has three parts:

| Part | Where | Purpose |
|---|---|---|
| `marionette_flutter` | your app (`dev_dependencies` or `dependencies` with a debug guard) | Exposes the widget tree and actions over the VM service |
| `marionette_cli` | your terminal | Commands such as `tap`, `enter-text`, `take-screenshots` |
| `marionette_mcp` | MCP host (Claude Code, Cursor, Copilot, Gemini CLI) | The same actions as MCP tools, without shell calls |

## 1. Prepare the app

```bash
flutter pub add marionette_flutter
```

```dart
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:marionette_flutter/marionette_flutter.dart';

void main() {
  if (kDebugMode) {
    MarionetteBinding.ensureInitialized(
      const MarionetteConfiguration(enableSessionReports: true), // optional
    );
  } else {
    WidgetsFlutterBinding.ensureInitialized();
  }
  runApp(const MaterialApp(home: Scaffold(body: Center(child: Text('hi')))));
}
```

- Guard the binding with `kDebugMode` so release builds never use it. This snippet was analyzed with `flutter analyze` against `marionette_flutter` 0.7.0.
- Standard Material widgets work without configuration. A custom design system needs `MarionetteConfiguration` (`isInteractiveElement`, `shouldStopTraversalAtElement`, `extractText`). Note: `isInteractiveWidget` and `shouldStopTraversal` are deprecated.
- `enableSessionReports: true` lets each CLI call write a step log (see Session reports below).
- `set-device-config` requires the root widget to be wrapped: `runApp(const MarionetteDeviceConfig(child: MyApp()));`.

## 2. Run the app and connect

1. Run the app in debug mode (`flutter run`) and copy the VM service URI from the console (for example `ws://127.0.0.1:8181/ws`).
2. Choose a connection style:
   - **Named instance (stateful):** `marionette register <name> <uri>`, then `marionette -i <name> <command>`, and `marionette unregister <name>` when done.
   - **Direct URI (stateless):** `marionette --uri <ws-uri> <command>`. Each call opens its own connection. Nothing is stored on disk.

Global options (all commands): `-i, --instance <name>`, `--uri <ws-uri>` (mutually exclusive with `-i`), `--timeout <seconds>` (default 5), `--session <title>`, `--session-dir <path>`.

## 3. Commands

Use `marionette help <command>` for the current options. All commands except `register`, `unregister`, `list`, `doctor`, `mcp`, and `help-ai` need `-i <instance>` or `--uri <ws-uri>`.

### Discovery

- `marionette list`: lists registered instances with URI and registration time.
- `marionette doctor`: checks connectivity of every registered instance. Exit 0 when all are reachable, 1 when any is not.
- `marionette get-interactive-elements [--ancestor-keys <str>] [--compaction compact|none]`: prints one line per interactive element with type, key, identifier, and text. Use the key, identifier, or text as the matcher in later commands.
- `marionette get-logs`: prints the app's collected logs.
- `marionette help-ai`: prints the full CLI reference for AI agents.

### Interaction

Element matchers: `--key <str>` (ValueKey), `--identifier <str>` (Semantics identifier, stable), `--text <str>`, `--type <str>` (widget type name). Pass exactly one primary matcher. `--ancestor-keys <str>` limits the search to the subtree of the named element.

- `tap`: matchers, or `--x <n> --y <n>` for a coordinate tap.
- `secondary-tap`: right mouse button tap, with the same matchers as `tap`. Desktop only. It triggers `onSecondaryTap` (for example context menus).
- `double-tap`, `long-press`, `pinch-zoom`: same matcher rules as `tap`. Their help text is in `marionette help <command>`. They are not described in `help-ai`.
- `enter-text --input <str>`: matches a text field with `--key`, `--identifier`, or `--text`, or uses `--focused` for the focused field. `--input` is required.
- `press-key --key <str> [--modifiers <list>]`: sends a real key event to the focused element. Named keys include `enter`, `tab`, and `escape`. Modifiers are comma-separated (`control`, `shift`, ...). Example: `--key a --modifiers control`. Use it for submit, focus moves, and shortcuts. Use `enter-text` to type text.
- `press-back-button`: Android back or iOS swipe-back.
- `swipe`: matchers plus `--direction left|right|up|down` (required in this mode), `--distance <px>` (default 200). Or give explicit `--start-x --start-y --end-x --end-y`.
- `scroll-to`: scrolls until a matcher is visible.

### Evidence

- `marionette take-screenshots -o <file.png> [--open]`: saves a PNG.
- `marionette record-video [--width <px>] [--height <px>] [--open] [--ffmpeg-path <path>] [--transport auto|tcp|ws] [--frame-port <port>]`: records video. Requires `ffmpeg`. Exit 1 when ffmpeg is missing or recording fails.

### App control

- `marionette hot-reload`: hot reload.
- `marionette hot-restart`: hot restart. Resets app state.
- `marionette set-device-config [--text-scale <n>] [--bold-text true|false] [--platform-brightness light|dark] [--reset]`: simulates device settings. Requires the `MarionetteDeviceConfig` wrapper described above. Without it the command exits 1.

### MCP

- `marionette mcp [--log-file <path>] [--sse-port <port>]`: runs the MCP server over stdio (default) or SSE. Use this when the agent host speaks MCP. The app is still driven through the same VM service.

## 4. Session reports

With `enableSessionReports: true` in the app, every command writes a step to `.marionette/sessions/<title>-<timestamp>/steps.md`. Use `--session <title>` (under about 60 characters) to name the directory and `--session-dir <path>` (or `MARIONETTE_SESSION_DIR`) to change where it is stored.

## 5. Exit codes and error recovery

  0    Success
  1    Runtime error (connection failed, command failed, app unreachable, ffmpeg missing)
  64   Usage error (missing arguments, invalid options)

If a command fails with a connection error, the app may have stopped.

- **Named instance:** run `marionette doctor`, then `marionette unregister <name>` to remove stale entries. Re-run `flutter run` and register the new URI.
- **Direct URI:** check that the URI is still correct and the app is running. Re-run `flutter run` if needed.

## 6. Constraints

- Debug mode only. Keep the `kDebugMode` guard so the binding never ships.
- Prefer `--key` or `--identifier` over `--text` and coordinates. Text changes with locale, and coordinates change with layout.
- Use `press-key` for keyboard events and `enter-text` for typing. They behave differently.
- Do not rely on `set-device-config` unless the app wraps its root in `MarionetteDeviceConfig`.
- For a custom design system, configure `MarionetteConfiguration` before you start testing. Otherwise the agent cannot see your custom buttons.

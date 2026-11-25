---
name: flutter-skill
description: "Automate and test Flutter applications — launch apps, inspect widgets, tap elements, enter text, scroll, swipe, take screenshots, validate state, and debug via Dart VM Service Protocol. Use when the user wants to run Flutter app tests, automate Flutter UI interactions, inspect widget trees, debug a running Flutter app, or perform gesture-based testing."
---

# Flutter Skill

Control running Flutter applications for testing, debugging, and automation. Connects AI agents to Flutter apps via the Dart VM Service Protocol, exposing tools for UI inspection, gestures, state validation, screenshots, and log access.

## Installation

### Option 1: npx (Recommended)
```json
{
  "mcpServers": {
    "flutter-skill": {
      "command": "npx",
      "args": ["flutter-skill"]
    }
  }
}
```

### Option 2: Global Install
```bash
dart pub global activate flutter_skill
```

```json
{
  "mcpServers": {
    "flutter-skill": {
      "command": "flutter_skill",
      "args": ["server"]
    }
  }
}
```

## Key Tools

| Category | Tools | Purpose |
|----------|-------|---------|
| **Connection** | `launch_app`, `connect_app` | Start or attach to a Flutter app |
| **Inspection** | `inspect`, `get_widget_tree`, `find_by_type` | Discover UI elements and widget structure |
| **Interaction** | `tap`, `enter_text`, `swipe`, `scroll_to`, `long_press`, `drag` | Perform gestures and input |
| **Validation** | `wait_for_element`, `wait_for_gone`, `get_text_value`, `get_checkbox_state` | Assert UI state |
| **Screenshots** | `screenshot`, `screenshot_element` | Capture visual state |
| **Navigation** | `go_back`, `get_current_route`, `get_navigation_stack` | Control and inspect navigation |
| **Debug** | `get_logs`, `get_errors`, `hot_reload`, `get_performance` | Diagnose issues |

## Workflow

### Core Testing Loop

```
launch_app(project_path: "/path/to/app")
  → screenshot()
  → inspect()
  → tap(key: "element_key") / enter_text(key: "field_key", text: "value")
  → screenshot()
  → verify with wait_for_element / get_text_value
```

### Example: Login Flow

```
launch_app(project_path: "/path/to/app")
screenshot()
inspect()
enter_text(key: "email_field", text: "user@example.com")
enter_text(key: "password_field", text: "password123")
tap(key: "login_button")
wait_for_element(key: "home_screen", timeout: 5000)
screenshot()
```

**If `wait_for_element` times out:** Call `screenshot()` to see the current state, then `get_errors()` to check for crashes or failed network requests.

### Example: Debug a Running App

```
connect_app(uri: "ws://127.0.0.1:50000/ws")
get_errors()
get_logs()
screenshot()
inspect()
```

## Validation Checkpoints

- **After `launch_app()`**: Verify a VM Service URI was returned. If not, check that Flutter is installed and the app compiles.
- **After `inspect()`**: Confirm interactive elements are returned. If empty, the app may still be loading — call `screenshot()` and retry.
- **After gestures** (`tap`, `enter_text`, `swipe`): Call `screenshot()` to confirm the UI updated as expected.
- **After navigation**: Use `wait_for_element(key: "target")` with a timeout. On timeout, call `get_errors()` to diagnose.

## Element Targeting Priority

1. **`key:`** (most reliable) — widget key set by the developer via `ValueKey`
2. **`text:`** — visible text content (breaks if text changes)
3. **`type:`** — widget type via `find_by_type` (may match multiple elements)

For reliable targeting, apps should use `ValueKey` on interactive elements:
```dart
ElevatedButton(
  key: const ValueKey('submit_button'),
  onPressed: _submit,
  child: const Text('Submit'),
)
```

## Links

- [GitHub Repository](https://github.com/ai-dashboad/flutter-skill)
- [pub.dev Package](https://pub.dev/packages/flutter_skill)
- [npm Package](https://www.npmjs.com/package/flutter-skill)

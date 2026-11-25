# AI Agent Workflow Guide for WeChat DevTools MCP

This guide helps AI agents (Claude, Cursor, Windsurf) effectively use the WeChat DevTools MCP server.

The server supports **two project types**, auto-detected from `project.config.json`:

- `compileType: "miniprogram"` → **mini-program** (pages + DOM)
- `compileType: "game"` → **mini-game** (canvas, no pages/DOM)

## Getting Started

### Step 1: Establish Connection

```json
// Use 'launch' to open a project (auto-detects type):
{
  "name": "launch",
  "arguments": {
    "projectPath": "/absolute/path/to/your/project",
    "cdpEndpoint": "ws://127.0.0.1:9421/<id>"   // optional, mini-game deep debug
  }
}

// Or 'connect' to attach to an already running DevTools:
{
  "name": "connect",
  "arguments": {
    "wsEndpoint": "ws://localhost:9420",
    "projectPath": "/absolute/path/to/your/project"
  }
}
```

### Step 2: Wait for Readiness

After launching:
- **Mini-program**: use `wait_ready` or `check_health` until `compilationStatus: "ready"`.
- **Mini-game**: readiness is detected via `GameGlobal` runtime liveness (NOT pages). `check_health` shows `compilationStatus: "game_running"` and `projectType: "game"`.

### Step 3: Detect Project Type

Always check `projectType` from `check_health` (or `get_project_type`) before choosing tools:

```json
{ "name": "check_health" }
// Response includes: connected, projectType, engineType, pageReady, cdpConnected, tips
```

- `projectType: "program"` → use page/DOM tools.
- `projectType: "game"` → use `evaluate`, `call_wx_method`, `game_*`, `game_touch`, `screenshot`.

> **Tool masking**: `ListTools` auto-hides mini-program-only tools (navigate, get_element, tap_element, …) when connected to a mini-game, and hides mini-game-only tools when connected to a mini-program. You won't see irrelevant tools.

## For Mini-Programs (`projectType: "program"`)
Use: `get_page_data`, `get_element`, `tap_element`, `navigate_to`, etc.

## For Mini-Games (`projectType: "game"`)
Use: `evaluate`, `call_wx_method`, `game_get_info`, `game_touch`, `game_canvas_screenshot`,
`game_get_fps`, `game_webgl_debug`, `game_get_network_logs`, `game_export_vconsole`, `screenshot`.
**Avoid**: `get_page_data`, `get_element`, `tap_element`, `navigate_to` — these require pages and will be rejected.

### Canvas Touch (core mini-game capability)
```json
{ "name": "game_touch", "arguments": { "x": 200, "y": 350, "type": "tap" } }
```
Simulates a real touch at canvas coordinates via CDP `Input.dispatchTouchEvent` (bypasses
"user gesture required" limits), falling back to invoking `wx.onTouchStart/End` callbacks.

## Debug Loop

### After Every Code Change (both types)

```
1. check_health           → verify no compilation/runtime errors, confirm projectType
2. Get recent logs:       → get_console_logs(level: "error")
3. Fix any errors found   → edit/write files
4. Re-check               → check_health
```

### UI / Runtime Verification

```
Mini-program:
1. navigate_to(url)       → go to target page
2. get_page_data()        → inspect state
3. get_element(selector)  → inspect UI
4. screenshot()           → visual check

Mini-game:
1. game_get_info()        → runtime info
2. game_touch(x,y)        → interact on canvas
3. game_get_fps()         → frame rate
4. game_canvas_screenshot()→ visual check
5. game_export_vconsole() → full logs for troubleshooting
```

### Cloud Function Debugging (both types)
```
1. call_cloud_function(name, data)  → invoke
2. get_console_logs()               → check logs
3. cloud_functions_deploy(env, names) → deploy after fixes
```

## Common Pitfalls

| Mistake | Correct Approach |
|---------|------------------|
| Using page tools on a game | Use `evaluate` / `game_touch` / `screenshot` instead |
| Assuming `currentPage()` exists for games | Games have no pages; readiness uses `GameGlobal` liveness |
| Not waiting for compilation | Use `wait_ready` after `launch` |
| Forgetting `check_health` after edits | Run `check_health` after EVERY write/edit |
| Hardcoding paths | Use absolute paths for `projectPath` |
| Touch not registering in game | Ensure the game registered `wx.onTouchStart` (entered interactive screen) before `game_touch` |
| CDP not connected | Manually `set_cdp_endpoint` with the game's `webSocketDebuggerUrl`; otherwise evaluate fallback is used |

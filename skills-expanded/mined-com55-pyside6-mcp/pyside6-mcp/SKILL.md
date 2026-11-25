---
name: pyside6-mcp
description: >
  How to use the pyside6-mcp MCP server to see, control, and debug a running PySide6/Qt Python
  desktop app — like Playwright but for GUI. Use this skill whenever the user wants to inspect or
  interact with their PySide6 app visually: take a screenshot, click a button, type into a field,
  read logs, inspect widget state, or launch the app. Trigger for any PySide6 or PyQt
  project where the user asks about UI behavior, wants to reproduce a bug visually, or says things
  like "screenshot", "click the button", "debug GUI", "inspect widget", "launch app", "see the UI".
---

# pyside6-mcp — Playwright for PySide6

## Overview

`pyside6-mcp` lets the agent see and control a running PySide6 app via an HTTP bridge injected into the app process. No source code changes required.

```
Agent → MCP tools → pyside6-mcp server → HTTP bridge (ephemeral port, keyed by pid) → PySide6 app
```

> **Never edit the user's source code to add `install_bridge()`.**
> Start the app with `launch_app()` instead — it injects the bridge automatically by
> monkey-patching `QApplication` (zero code modification). `install_bridge()` is only a
> fallback for when the user insists on running the app themselves, outside this server.

## Prerequisites

Only the MCP server config in the client — **no install in the target app**.
The target project must already use PySide6 and be runnable via `uv run` in its directory.

## Standard Workflow

### 1. Launch the app (if not already running)

**Required:** `cwd` (absolute project root).  
**Optional:** `script` (entry `.py` relative to cwd), `app_args`, `timeout`.

Returns `{pid}` — the Qt app process. Do **not** pass `port=`.
Omit `pid` on later tools to target this app; pass `pid=` when several apps are running. Call `list_apps()` to see pids.

| Entry location | Call |
|----------------|------|
| `main.py` at project root | `launch_app(cwd="/abs/project")` |
| other name at root, e.g. `app.py` | `launch_app(cwd="/abs/project", script="app.py")` |
| in subfolder, e.g. `backend/gui.py` | `launch_app(cwd="/abs/project", script="backend/gui.py")` |

`cwd` is always the project root (where `pyproject.toml` lives), **not** the folder containing the `.py` file.

If unsure, call `get_launch_help()` first or list the project root before launching.

```
launch_app(cwd="/absolute/path/to/your-project")
launch_app(cwd="/absolute/path/to/your-project", script="src/run.py", app_args=["--verbose"], timeout=60)
```

Do not pass `command=` or shell strings. Do not add pyside6-mcp to the target `pyproject.toml`.
Do not pass `port=` — the server binds an ephemeral localhost port and keys the session by pid.

`launch_app` waits until the UI is ready (visible window + quiet for 500 ms) before returning — all other tools work immediately after. Default `timeout` is 45 seconds. If it returns `"UI not ready"`, the process is left running for inspection — call `get_app_status()` / `get_app_output()`.

If the user already launched the app manually (with `python -m pyside6_mcp main.py`), skip this step or use `wait_until_ready()` instead.

### 1b. Several apps at once

One MCP server can run many apps. `launch_app` returns `{pid}` of the **Qt app process**, not the `uv` wrapper.

```
launch_app(cwd="/abs/project-a", script="app.py")
launch_app(cwd="/abs/project-b", script="examples/test_app.py")
list_apps()                 # [{pid}, {pid}, ...]
screenshot(pid=111)         # required when more than one is running
get_widget_tree(pid=222)
stop_app(pid=111)
```

Omit `pid` only when a single app is running, or to target the last launched app. If tools error with "Multiple apps running", call `list_apps()` and pass `pid=`.

### 2. Orient yourself — always do both first

```
screenshot()        # see current UI state (captures active/modal window)
get_widget_tree()   # full hierarchy with IDs
```

Widget IDs from the tree are used in all other tools.

### 2b. After UI-changing actions

```
wait_for_idle()     # wait for layout/paint to settle
screenshot()        # then capture
```

### 3. Find a widget

```python
find_widget(text="Apply")              # by label/button text
find_widget(class_name="QPushButton")  # by Qt class
find_widget(object_name="submitBtn")   # by objectName set in code
```

### 4. Interact

```python
click(widget_id="4")                   # click widget center
click(widget_id="4", x=10, y=5)       # click at offset within widget
type_text("hello", widget_id="1")      # focus + type
press_key("enter")                     # named key
scroll(dy=-3, widget_id="2")          # scroll up
```

### 5. Verify

```python
screenshot()            # see result
get_widget_info("4")    # check properties/state
get_logs(n=20)          # check Python logging records from the app
get_app_output(n=50)    # check raw stdout/stderr (prints, tracebacks)
```

---

## Tool Reference

| Tool | What it does |
|------|-------------|
| `launch_app(cwd, script?, app_args?, timeout)` | Spawn app + wait for UI readiness (returns `{pid}`, default timeout 45 s) |
| `list_apps()` | Pids of apps this server launched |
| `get_launch_help()` | How to set cwd / script / app_args |
| `wait_until_ready(timeout, quiet_ms, pid?)` | Wait for UI readiness on an already-running app |
| `wait_for_idle(timeout, quiet_ms, pid?)` | Wait until UI quiet after an action (before screenshot) |
| `get_app_status(pid?)` | Process + bridge health; detects likely modal blocks |
| `stop_app(pid?)` | Stop a previously launched app |
| `screenshot(widget_id?, pid?)` | Capture window or specific widget (modal/active-window aware) |
| `get_widget_tree(pid?)` | Full widget hierarchy as JSON with IDs |
| `get_widget_info(widget_id, pid?)` | Detailed properties of one widget |
| `get_app_state(pid?)` | Active window, focus widget, screen info |
| `find_widget(class_name?, object_name?, text?, visible?, pid?)` | Search widgets |
| `click(widget_id?, x?, y?, button?, pid?)` | Mouse click |
| `double_click(widget_id, x?, y?, pid?)` | Double click |
| `type_text(text, widget_id?, pid?)` | Keyboard input |
| `press_key(key, pid?)` | Named key: `enter`, `escape`, `tab`, `up`/`down`/`left`/`right`, `f5`, or any character |
| `scroll(dy, widget_id?, dx?, pid?)` | Scroll (dy > 0 = down, dy < 0 = up) |
| `list_actions(pid?)` | List QAction menu/toolbar items with name, text, shortcut |
| `trigger_action(name?, text?, pid?)` | Trigger a QAction directly without clicking menus |
| `get_logs(n?, pid?)` | Recent Python `logging` records via the bridge (default 50) |
| `get_app_output(n?, pid?)` | Raw stdout/stderr of the launched app: `print()`, tracebacks, Qt warnings (default 200 lines) |
| `eval_python(code, pid?)` | Execute Python inside the app process |

### `eval_python` context

```python
app      # QApplication.instance()
widgets  # dict: widget_id → QWidget
```

Examples:
```python
eval_python("app.activeWindow().windowTitle()")
eval_python("widgets['3'].model().rowCount()")
eval_python("widgets['5'].isChecked()")
```

---

## Common Patterns

### Debug why a button does nothing

```
screenshot()                     # state before
find_widget(text="Submit")       # get widget ID
click(widget_id="X")
screenshot()                     # state after
get_logs()                       # did the handler fire?
```

### Inspect widget state without interacting

```
get_widget_tree()                        # check enabled/visible for all
eval_python("widgets['X'].styleSheet()") # check CSS
eval_python("widgets['X'].isEnabled()")  # check specific property
```

### Fill a form and submit

```
find_widget(class_name="QLineEdit")   # find input fields
type_text("value1", widget_id="1")
press_key("tab")
type_text("value2", widget_id="2")
click(widget_id="submit_id")
screenshot()
```

---

## Gotchas

- **Several apps on one MCP server** — `launch_app` returns `{pid}` (Qt process, not `uv`). `list_apps()` lists them. Omit `pid` to target the last launched app; pass `pid=` to pick one
- **Never pass `port=` or `command=`** — those are gone from the agent API. Do not `uv add pyside6-mcp` in the target project
- **Widget IDs reset on every restart** — always call `get_widget_tree()` again after `launch_app`
- **Bridge must be running** — if tools return a connection error, call `launch_app` first
- **Qt operations run on the main thread** — the bridge marshals automatically, but if the app is hung, tools will timeout after 5 s
- **Modal dialogs block the main thread** — `QDialog.exec()` / `QMessageBox` run a nested event loop; tools that marshal to the main thread will time out. Use `trigger_action()` / `list_actions()` to drive menus without opening modals, and `get_app_status()` to confirm a modal block
- **After UI-changing actions** — call `wait_for_idle()` before `screenshot()` so layout/paint has settled
- **`eval_python` runs real code in the app process** — use for inspection only, not production state changes
- **`get_logs` vs `get_app_output`** — `get_logs` returns Python `logging` records via the bridge; `get_app_output` returns the raw stdout/stderr (`print()`, uncaught tracebacks). If the app crashes on startup, use `get_app_output` — it reads from a file and works even when the bridge never came up (only for apps started via `launch_app`)

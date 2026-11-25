---
name: vision-control
description: Launch, focus, inspect, and automate desktop applications deterministically via ShellMind Vision MCP (AT-SPI2 D-Bus actions first, exact OCR coordinates second, with mandatory post-action verification).
---
# ShellMind Vision Control

Automate desktop applications reliably without mouse guessing or blind retries.

## Workflow

1. **Discover or Launch:** Use `list_windows` / `focused_window` first; if the target app is not open, call `launch_app({"app": "<name>"})`. Respect IDE built-in browser isolation unless the user explicitly asks for a host browser.
2. **Prefer AT-SPI2 D-Bus Over Mouse Input:** Call `deep_atspi_tree({"app_query": "<app>", "max_depth": 28, "interactive_only": true})` and invoke buttons or inputs directly via `atspi_invoke_node({"node_path": "..."})` without hijacking the physical cursor.
3. **Fallback to Exact Coordinates Only When Needed:** If a canvas/webview lacks AT-SPI2 nodes, get exact `(center.x, center.y)` from `screenshot_and_ocr` or `find_text_in_image`, then call `click`, `type_text`, or `press_key`.
4. **Verify State After Action:** Always confirm the UI transitioned as expected using `screenshot_and_ocr` or `deep_atspi_tree` before moving to the next step.

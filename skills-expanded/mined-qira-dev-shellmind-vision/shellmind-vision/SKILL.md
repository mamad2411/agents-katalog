---
name: shellmind-vision
description: Mandatory skill for deterministic desktop UI inspection, application launching, on-demand 123-language OCR provisioning, silent in-memory window/desktop screenshot analysis, batch image OCR, SVG structural parsing, and direct AT-SPI2 D-Bus automation via ShellMind Vision on http://127.0.0.1:39200/mcp.
---
# ShellMind Vision — Deterministic Vision & Desktop Automation Skill

Use the local `ShellMind Vision` engine (`http://127.0.0.1:39200/mcp` or `node ~/.local/share/shellmind-vision/mcp-stdio.mjs`) to deterministically launch, inspect, and control desktop applications, windows, images, screenshots, and SVG files without relying on Vision LLM guessing.

---

## 1. Core Operating Principles

1. **Zero Vision LLM Guessing:** Never estimate pixel coordinates or guess small terminal/UI text using internal Vision LLM capabilities. Always rely on `ShellMind Vision` tool outputs (`center.x, center.y`, `bbox`, `text`, and `atspi_ground_truth_text`).
2. **Browser Isolation:** When working inside an IDE with a built-in browser view (Antigravity, ZCode, Cursor), use the IDE's internal browser rather than hijacking the user's host OS browsers (Brave, Chrome, Firefox) unless explicitly requested.
3. **In-Memory Zero-Disk Pipeline:** For live windows or desktop state, use `screenshot_and_ocr` rather than saving temporary `.png` files to `/tmp`.

---

## 2. Gate 0: Just-In-Time Language Onboarding (123+ Languages)

On a fresh clone, only English (`eng`) is pre-installed so the repository stays lightweight (~40 MB).
1. Call `ensure_language` with `{"language": "list"}` to inspect currently installed OCR models.
2. If the user's conversation or target screen uses another language (e.g., Bengali `"ben"`, Japanese `"jpn"`, Spanish `"spa"`, Arabic `"ara"`, Hindi `"hin"`, French `"fra"`, German `"deu"`, Simplified Chinese `"chi_sim"`, Korean `"kor"`, Russian `"rus"`, Portuguese `"por"`):
   - Immediately call `ensure_language({"language": "<3-letter-code>"})`.
   - The quantized fast model (~1–2 MB) downloads and activates in under 1 second with zero daemon restart required.

---

## 3. Tool Selection & Parameter Reference (27 Tools)

| Task | Tool Name | Key Parameters & Usage Notes |
| :--- | :--- | :--- |
| **Check / Add OCR Language** | `ensure_language` | `{"language": "list"}` or `{"language": "ben"}` (supports 123+ ISO 639-2 codes or `"all"`). |
| **Launch or Focus App** | `launch_app` | `{"app": "zcode"}` (or `"antigravity"`, `"obsidian"`, `"dolphin"`, `"vlc"`). Injects Wayland/XWayland/D-Bus & accessibility flags, waits for rendered window, and reuses existing window if already open. |
| **Live Window / Screen OCR + OS Truth Fusion** | `screenshot_and_ocr` | `{"window_id": 12345}` (or `{}` for full screen, or `{"app_id": "zcode"}`). Runs 100% in RAM, applies 3x3 Laplacian Unsharp Mask, and fuses live 28-level `AT-SPI2` OS labels (`atspi_ground_truth_text`, `atspi_node_path`). |
| **Single or Batch Image File OCR** | `inspect_image_ocr` | Single file: `{"file_path": "/abs/path.png"}`. Batch mode: `{"file_paths": ["/path/1.png", "/path/2.png"]}`. Pass `"detect_ui_boxes": false` for text-only tasks to minimize payload size. |
| **Locate Specific String in Image** | `find_text_in_image` | `{"file_path": "/abs/path.png", "query_text": "Submit"}` -> returns matching blocks with exact `(center.x, center.y)` click coordinates. |
| **Parse SVG File or Markup** | `inspect_svg` | `{"file_path_or_xml": "/path/file.svg"}` (or raw `<svg>...</svg>` string) -> Pure-Rust XML/DOM parser returning `viewBox`, `<text>` nodes, shapes, and exact `bbox`/`center`. |
| **Walk Live Accessibility Tree** | `deep_atspi_tree` | `{"app_query": "zcode", "max_depth": 28, "interactive_only": true}` -> returns structured OS accessibility nodes with `node_path`, `role`, `name`, `actions`, and `bounds`. |
| **Direct No-Mouse D-Bus Action** | `atspi_invoke_node` | `{"node_path": "16/0/0/2"}` (or `{"node_path": "...", "set_text": "hello"}`) -> clicks buttons or populates inputs directly over D-Bus without moving the physical mouse cursor. |
| **Window Discovery & Management** | `list_windows`, `focused_window`, `activate_window`, `move_window`, `resize_window` | Discover `window_id`, `pid`, `app_id`, `title`, and `bounds`, or focus/reposition windows via the GNOME Shell Wayland extension. |
| **Pointer & Keyboard Input** | `click`, `perform_action`, `set_value`, `type_text`, `press_key`, `scroll`, `drag` | Execute bounded desktop input using exact `(x, y)` coordinates or semantic selectors. |

---

## 4. Verification & Error Handling

1. **Check `ok` and `isError`:** Always verify `ok: true` and `isError: false` before using tool output. If an image is unreadable or fails validation, `inspect_image_ocr` returns `ok: false, error_code: "VISION_ENGINE_FAILED", isError: true`.
2. **Verify State After Actions:** After calling `click`, `atspi_invoke_node`, `type_text`, or `launch_app`, confirm the resulting UI transition via `screenshot_and_ocr` or `deep_atspi_tree`.

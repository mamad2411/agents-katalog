---
name: vision-inspect
description: Deterministically inspect screenshots, live desktop windows, batch images, or SVG files using ShellMind Vision MCP (123-language AVX2 OCR + AT-SPI2 ground truth + pure-Rust SVG DOM parser) instead of guessing pixels or text.
---
# ShellMind Vision Inspect

Inspect visual UI state, images, and SVGs deterministically with zero pixel or text hallucination.

## Workflow

1. **Gate 0 (Language Check):** If the target UI or image contains non-English text (e.g. `ben`, `jpn`, `ara`, `hin`, `chi_sim`), call `ensure_language({"language": "list"})` and provision missing models via `ensure_language({"language": "<code>"})` (< 1s, zero restart).
2. **Choose the Deterministic Tool:**
   - **Live window or desktop:** Call `screenshot_and_ocr` (`{}` for full screen or `{"window_id": ...}` / `{"app_id": ...}`) for in-memory OCR fused with 28-level AT-SPI2 ground truth.
   - **Image file(s) on disk:** Call `inspect_image_ocr` (`{"file_path": "/abs/path.png"}` or `{"file_paths": [...]}`). Pass `"detect_ui_boxes": false` for text-only extraction.
   - **Find exact button/label coordinates:** Call `find_text_in_image({"file_path": "/abs/path.png", "query_text": "Submit"})` to get exact `(center.x, center.y)`.
   - **SVG file or markup:** Call `inspect_svg({"file_path_or_xml": "/abs/path.svg"})` for `viewBox`, `<text>`, and exact bounding boxes.
3. **Verify Output:** Always check `ok: true` and `isError: false`. Never treat `VISION_ENGINE_FAILED` as an empty screen.

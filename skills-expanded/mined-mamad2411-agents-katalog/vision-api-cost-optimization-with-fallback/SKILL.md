---
name: vision-api-cost-optimization-with-fallback
description: Cascade of cheaper-to-more-expensive techniques for extracting info from GUIs — window titles first, local OCR second, scoped screenshots only when nothing else works.
category: computer-vision
version: 1.0.0
tags: [computer-vision, cost-optimization, gui-automation, ocr, screenshots]
source_type: extracted-from-git
source_url: https://github.com/lsdefine/GenericAgent.git
source_ref: main
source_commit: ec34b7e1c0f11fbb9709680ccfe313187a1b942b
source_project: GenericAgent
source_path: memory/vision_sop.md
imported_at: 2026-04-18T00:00:00Z
confidence: high
version_origin: extracted
---

# Vision-API cost optimization with fallback cascade

When an agent needs to "see" a GUI, naive use of a vision LLM is expensive and unreliable. This skill prescribes a four-level fallback cascade that defers the vision API to last resort, with strict rules on *what* gets captured when you do reach the API.

## When to use

Any agent that interacts with native desktop apps, browser UIs, or game clients where getting text / state out of the interface is on the critical path.

## The cascade (cheapest → most expensive)

1. **Window-title enumeration.** Before anything else, call the OS window API (on Windows: `pygetwindow`) to list window titles and confirm the target window is present and focused. Many "what app is open / what chat is selected" questions resolve here for zero API cost.
2. **Local OCR.** If a pure text region is needed, run local OCR on the captured region (e.g., the project ships its own `ocr_utils.py`). Tesseract / PaddleOCR / EasyOCR are comparable off-the-shelf options. No tokens, works offline.
3. **Scoped screenshot → vision API.** Only if (1) and (2) can't answer, *and* then with strict scoping rules (see next section).
4. **Full-page / canvas base64.** Reserved for captchas or dynamic canvas content that OCR can't read. Extract via `canvas.toDataURL()` when the source is a browser canvas.

## Hard rules when you do reach the vision API

**Never full-screen.** Always scope the capture to the target window:

```python
import win32gui
from PIL import ImageGrab

hwnd = win32gui.FindWindow(None, target_title)
left, top, right, bottom = win32gui.GetWindowRect(hwnd)
img = ImageGrab.grab(bbox=(left, top, right, bottom))
```

If the relevant region is smaller than the window (title bar, a specific panel), scope it further. Cropping happens *before* the API call, not inside the prompt.

**Verify the window exists first.** If `pygetwindow`/enumeration can't find it, do not screenshot a "best guess" region — stop and report. A screenshot of the wrong window is worse than no screenshot.

**Control the payload size.** Most vision APIs accept a `max_pixels` budget. Default to ~1.4M pixels (roughly 1080p) and auto-downscale anything larger. Very large images waste tokens without improving accuracy on UI extraction.

**Prompt is cheap, image is expensive.** Ask very specific questions ("Return the text in the blue button"), not open-ended ones ("Describe this image"). Specific prompts allow the model to allocate attention efficiently and keep token costs predictable.

## Minimal contract

```python
def ask_vision(
    image_input,              # path | PIL Image
    prompt: str | None = None,
    timeout: int = 60,
    max_pixels: int = 1_440_000,
) -> str:
    """
    Return model text on success, 'Error: ...' string on failure.
    Never throws — failure is returned as a sentinel so the caller can
    layer its own retry/backoff logic.
    """
```

## Retry, don't swallow

Vision API calls will hit transient 503 / timeouts. The SDK-level call should NOT auto-retry silently because different callers want different retry policies (a batch job can afford 8x backoff; a user-facing query cannot wait 30s). Expose the error as a string sentinel; callers wrap in exponential backoff as needed.

## Anti-patterns

- "I'll just screenshot the whole desktop and let the model figure it out." Wastes tokens, leaks PII from other apps, makes OCR worse.
- Hardcoding a model or endpoint inside the vision helper. Configs drift; keep it swappable.
- Using vision to read data that is trivially available via OS APIs (window title, foreground PID, clipboard).
- Calling the vision API inside a tight loop with no retry/backoff — one blip of network weather takes the whole automation down.

## Implementation checklist

- [ ] Confirm `pygetwindow` / equivalent window-enumeration library is installed.
- [ ] Set up a local OCR helper and unit-test it against your target apps' text regions.
- [ ] Wrap the vision API in a thin function with a timeout and max-pixels knob.
- [ ] Document the fallback order in a project SOP so future callers don't skip straight to vision.
- [ ] Add a per-call cost log (pixels in, tokens out) so you can see regression when someone starts full-screening.

---

Adapted from GenericAgent's `vision_sop.md`. Principles generalized; library names are examples, not prescriptions.

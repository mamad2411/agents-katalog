---
name: screenshot-text-extraction
description: Extract text from a visible image or Windows screen pixels with Win+Shift+T Text Extractor/Snipping Tool and copy it to the clipboard, or author a reusable ADH Robot RPA that performs that flow. Use immediately whenever a task requires reading text from an image, screenshot, image/document preview, or screen region, even before the source image is visible.
---

# Screenshot Text Extraction

Use the parent ADH skill and follow its shell-first boundary. Use shell or ordinary code for every step that does not require visible desktop state. Use host-managed `run_python` only for the Windows Text Extractor's visible UI steps during interactive exploration; for reusable RPA author Robot source with the matching `ADHLibrary` keywords and run it through `validate_rpa` / `run_rpa`. After ADH clicks the semantic copy control, return to shell and read the copied text with Windows PowerShell `Get-Clipboard -Raw`. Do not launch a GUI editor to obtain data that shell can read directly.

Load this subskill before app discovery, app launch, dependency selection, or
`init_rpa`. Do not postpone it until an image has been opened. Do not search for
or install OCR packages as a substitute for the Windows Text Extractor workflow
unless the user explicitly requests a different implementation.

## Workflow

1. Focus the source window. Remove or dismiss popups that overlap the target
   region, because Windows OCR extracts every visible layer inside the box.
2. Observe the source with a screenshot and choose the smallest rectangle that
   fully contains the desired text. The rectangle is in current window-screenshot
   pixels; never reuse one from an earlier observation.
3. Resolve the containing display with `get_display(window=source)` and convert
   the rectangle with `project_to_desktop`. Do not add virtual-screen origins or
   apply DPI scaling yourself. Projection rejects a region crossing displays.
4. Invoke `press_global_key("Win+Shift+T", expected_foreground=source)`, wait
   briefly with bounded `time.sleep()`, then capture that display with
   `observe_desktop`.
5. Drag the projected rectangle through `drag_desktop`. Wait briefly for OCR.
6. Call `list_windows()` again. The overlay may start as a desktop-only surface
   and then expose a stable Snipping Tool `WindowRef` plus UIA controls.
7. Observe Snipping Tool candidates and require exactly one enabled button named `复制所有文本` or `Copy all text`. Click that semantic button. Do not guess a small overlay coordinate when a semantic control exists.
8. Verify the overlay closes, then leave the ADH action path and run `Get-Clipboard -Raw` through the host shell. Keep the returned text in memory for parsing or verification. Do not launch Notepad or another scratch editor merely to paste and read the result.

## Reference pattern

Replace `target_rect` with a rectangle derived from the fresh source screenshot.
Keep discovery, projection, shortcut, drag, overlay rediscovery, and selection
in one cell while no model judgment is needed.

```python
import time
from adh.sdk import Rect

source = computer.get_window(app="msedge.exe")
computer.focus_window(source)
source_state = computer.observe(
    source,
    include_screenshot=True,
    include_tree=True,
)

# Derive this from source_state's current screenshot, not from an old run.
target_rect = Rect(x=240, y=160, width=900, height=650)
display = computer.get_display(window=source)
desktop_region = computer.project_to_desktop(source_state, target_rect)

computer.press_global_key("Win+Shift+T", expected_foreground=source)
time.sleep(0.5)
desktop = computer.observe_desktop(display)
rect = desktop_region.rect
computer.drag_desktop(
    desktop,
    start=(rect.x, rect.y),
    end=(rect.x + rect.width - 1, rect.y + rect.height - 1),
)
time.sleep(1.0)

overlay_windows = [
    item
    for item in computer.list_windows()
    if item.app.casefold() == "snippingtool.exe"
]
copy_candidates = []
for overlay_window in overlay_windows:
    state = computer.observe(
        overlay_window,
        include_screenshot=False,
        include_tree=True,
    )
    for item in state.elements:
        if (
            item.role == "button"
            and item.name in {"复制所有文本", "Copy all text"}
            and "disabled" not in item.states
        ):
            copy_candidates.append((overlay_window, state, item.element_index))

if len(copy_candidates) != 1:
    raise RuntimeError(
        f"expected exactly one Copy all text button, found {len(copy_candidates)}"
    )

overlay_window, overlay_state, element_index = copy_candidates[0]
computer.click(overlay_window, element=overlay_state.element(element_index))
time.sleep(0.3)
remaining = [
    item.title
    for item in computer.list_windows()
    if item.app.casefold() == "snippingtool.exe"
]
emit({"copied": True, "remaining_snipping_tool_windows": remaining})
```

After the cell reports a successful semantic copy, read the text with the host shell:

```powershell
Get-Clipboard -Raw
```

Do not print the value again or persist it unless the user's task authorizes that destination.

## Recovery

- If the shortcut has no visible effect, re-observe the source and confirm it is
  still foreground before retrying once.
- If the drag captures unrelated text, close the overlay, remove the occlusion,
  take a fresh source screenshot, and calculate a tighter rectangle.
- If no Snipping Tool window appears immediately after the drag, wait briefly
  and enumerate windows again; do not keep using a stale desktop observation.
- If multiple copy buttons appear, inspect the candidate window titles and trees
  and refine the window selection. Never select the first arbitrary candidate.
- If the overlay exposes no stable window after a bounded retry, stop and report
  the observed windows and desktop state rather than guessing a coordinate.
- If `Get-Clipboard -Raw` returns empty text, confirm that the semantic copy action succeeded and retry the OCR overlay once from a fresh source observation. Do not fall back to a scratch editor.

The clipboard result belongs to the user. Do not emit, paste, or persist
sensitive extracted text unless the user's task authorizes that destination.

## Reusable Robot RPA

Prove one image end to end before building loops or a full challenge. The Robot task must select and foreground the intended source application, observe the actual image, derive the OCR rectangle from that current run, invoke the overlay, rediscover its window, click `Copy all text`, read the clipboard through PowerShell `Get-Clipboard -Raw`, and verify or parse the returned text. Do not treat successful process launch or window selection as proof that the target content is foreground.

Use these `ADHLibrary` equivalents in agent-authored Robot source:

- `list_windows` -> `List Windows`; `focus_window` -> `Focus Window`.
- `observe` -> `Observe Window`; `get_display` -> `Get Display`.
- `project_to_desktop` -> `Project To Desktop`.
- `press_global_key` -> `Press Global Key`.
- `observe_desktop` -> `Observe Desktop`; `drag_desktop` -> `Drag Desktop`.

Use Robot Framework's standard `Process` Library for the shell step; it is available in the fixed ADH Robot runtime:

```robot
*** Settings ***
Library    Process

*** Keywords ***
Read Extracted Text
    ${clipboard}=    Run Process    powershell.exe    -NoProfile    -NonInteractive    -Command    Get-Clipboard -Raw
    Should Be Equal As Integers    ${clipboard.rc}    0
    Should Not Be Empty    ${clipboard.stdout}
    RETURN    ${clipboard.stdout}
```

Keep `Get-Clipboard -Raw` in one Robot argument cell after `-Command`. `Run Process` captures stdout on the result object. Do not use `shell=True`, open a PowerShell window, or persist clipboard text to an intermediate file. Apply the host confirmation policy to consequential shell operations exactly as for other code.

The agent may write a pure Python helper to calculate a `Rect` from current observation geometry or task-specific image bounds. It must not perform desktop input, call an OCR or native clipboard API, or persist coordinates discovered during exploration. After the shortcut and after the drag, use `List Windows` again: the overlay can change from a desktop-only surface into a stable Snipping Tool window. Focus and observe the new window before selecting its semantic control.

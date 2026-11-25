---
name: prefer-second-monitor
description: Place task-owned Windows application windows on a secondary display when available and practical.
---

# Prefer a secondary display

Use the application's own monitor or window-position option when possible.
Inspect current display topology; prefer a non-primary display, or the display
the user named. Single-monitor systems use the available screen without a pause.

If needed, use [the placement helper](scripts/place_process_windows.ps1) on
Windows with the exact process ID launched for this task. Establish ownership
from the launch record and current process identity before using -Apply.
Run without -Apply first to inspect the proposed display and window handles.
Pass -DeviceName explicitly when a particular display is required; its default
is the first non-primary screen sorted by device name.

The helper preserves size and z-order and requests no activation. It positions
windows relative to the working area's origin but does not guarantee DPI-aware
fitting, centering, or containment of oversized windows. Inspect the actual
result, especially with mixed DPI, portrait displays, or negative coordinates.
A zero window_count means no window was placed, regardless of the status label.

Keep a window on the primary screen when capture, input, fullscreen, a modal
parent, or tool limitations make secondary placement unreliable. Preserve
unrelated user windows and all display settings. Move only task-owned windows.
Headless processes have no placement requirement; placement itself is not
evidence that the application works.

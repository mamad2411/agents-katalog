---
name: linux-file-upload-dialog
description: Operate native GTK and Qt file chooser dialogs on Linux after clicking a web upload button.
version: 0.1.0
when:
  keywords: [upload, attach file, choose file, file chooser, gtk, linux dialog]
---
# Linux file upload dialog

Clicking a web "Choose file" or "Upload" button on Linux opens a native GTK or Qt file chooser outside the browser page.

1. Click the upload button with `browser_click`. Do not look for the native dialog inside `browser_snapshot`.
2. Switch to desktop tools: run `desktop_get_state` and locate the window titled "Open", "Open Files", "Choose File", or "Select File".
3. Press `ctrl+l` with `desktop_key` to reveal and focus the GTK/Qt Location text entry bar (if it is not already visible in the accessibility tree).
4. Run `desktop_get_state` again to find the Location text field, then enter the full file path via `desktop_set_value` (or click the field and use `desktop_type`).
5. Press `Return` with `desktop_key` or click the "Open" button.
6. Return to the browser and run `browser_snapshot` to verify the selected file name appears next to the upload control.

Notes:
- Always pass an absolute path (for example `/home/user/Documents/report.pdf`).
- If the dialog is for saving a file ("Save As"), verify the target directory and filename before confirming.
- Confirm with the user before uploading any file they did not explicitly name.

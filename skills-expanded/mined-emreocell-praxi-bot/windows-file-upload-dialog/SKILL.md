---
name: windows-file-upload-dialog
description: Handle the native Windows "Open" file picker that appears after clicking an upload button.
version: 0.1.0
when:
  keywords: [upload, attach file, choose file, file picker, browse]
---
# Windows file upload dialog

Clicking a "Choose file" / "Upload" button opens a native Open dialog outside the page.

1. Click the upload button with `browser_click`. Do not look for the dialog in the page snapshot.
2. Switch to desktop tools: `desktop_get_state` and find the window titled "Open" (or "Select file", "Upload").
3. Find the "File name" edit box and fill it with the full path via `desktop_set_value` (for example `C:\Users\me\Documents\report.pdf`). If set_value fails, click the box and use `desktop_type`.
4. Press Enter with `desktop_key` or click the "Open" button.
5. Return to the browser: `browser_snapshot` and check that the file name is shown next to the input.

Notes:
- Paths with spaces work unquoted in the File name box.
- If a plain file input is visible in the snapshot, prefer setting it directly when a tool supports it; the dialog is the fallback.
- Confirm with the user before uploading any file they did not name.

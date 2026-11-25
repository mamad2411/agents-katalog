---
name: danikuse-desktop
description: Operate the Windows desktop with a visible cursor. Use when the user invokes /danikuse-desktop or asks to operate a desktop application, click or type in a program, or do something "on my computer" outside a browser.
---

# /danikuse-desktop — computer with cursor

CLI: `danikuse pc <agent-desktop args>` (`launch`, `snapshot`, `click`, `type`, `set-value`, `get`, `press`, `screenshot`, `list-windows`, `close-app`). Every result is one JSON object.

1. Work visibly: the user watches the cursor. Never focus or type into a window that holds the user's own unsaved work; if an app is already open with user content, stop and use a safe file or a disposable app instead.
2. Target selection first (the OpenAI computer-use rule): list windows, filter to exactly one returned window, and act only on that handle. Never guess a window from a title you invented. If the filter gives 0 or 2+, stop and narrow it.
3. Observe → one action → refresh: element refs are valid only for the snapshot that produced them. After any action that may change the tree, re-snapshot before the next action. Check the focused element before typing; if a type or click fails, the outcome is unknown — re-observe, never blind-retry.
2. Prefer `set-value` for text fields: it writes through the accessibility seam and verifies the value. Physical `type --headed` needs the window in the foreground; if focus is denied, report it plainly instead of retrying blindly.
3. Done when a fresh snapshot or `get` confirms the target state on screen, not when the click was sent.
4. Confirm Mode default: sending, paying, publishing, deleting in desktop apps waits for the user's word.

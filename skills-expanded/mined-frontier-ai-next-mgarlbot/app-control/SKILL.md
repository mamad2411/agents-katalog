---
name: app_control
description: Open, close, and control applications on the computer
triggers: [open, launch, close, quit, app, application, notepad, textedit, browser, safari, chrome, cursor, vscode, terminal, finder, calculator, открой, запусти, приложение, терминал]
tools: [shell]
platform: macos
---

## Application control (macOS)

Use shell and AppleScript to launch and control apps.

### Open by app name

```
open -a "TextEdit"
open -a "Safari"
open -a "Calculator"
open -a "Cursor"
open -a "Terminal"
open -a "Finder"
open -a "Notes"
```

### Open a file

Default app:

```
open /path/to/file.txt
```

Specific app:

```
open -a "TextEdit" /path/to/file.txt
```

URL:

```
open "https://example.com"
```

### Editor with content

```
echo "content here" > /tmp/tempfile.txt && open -a "TextEdit" /tmp/tempfile.txt
```

### Projects / folders

Open folder in Cursor:

```
open -a "Cursor" /path/to/project
```

Open in Finder:

```
open /path/to/folder
```

### Quit

```
osascript -e 'quit app "TextEdit"'
```

### Is it running?

```
pgrep -x "TextEdit" && echo "Running" || echo "Not running"
```

### AppleScript (advanced)

Type into frontmost app:

```
osascript -e 'tell application "System Events" to keystroke "Hello World"'
```

Shortcut:

```
osascript -e 'tell application "System Events" to keystroke "s" using command down'
```

Bring to front:

```
osascript -e 'tell application "TextEdit" to activate'
```

### Rules

1. On macOS, “notepad” → **TextEdit** unless the user names another app.
2. After `open`, confirm success when practical (e.g. `pgrep`).
3. Prefer **write a temp file and open it** over long keystroke typing.
4. Use `osascript` only when needed; it is fragile under focus changes.
5. After launching an app, a short `sleep 1` before UI automation can help.
6. For “open notepad and write X”: write `X` to a file, open in TextEdit.

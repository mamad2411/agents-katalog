---
name: desktop_automation
description: Take screenshots, interact with desktop UI, capture screen content
triggers: [screenshot, screen capture, desktop, capture, display, скриншот, экран, скрин]
tools: [shell]
platform: macos
---

## Desktop automation (macOS)

Use shell commands for screenshots and simple desktop actions.

### Screenshots

Full screen:

```
screencapture ~/Desktop/screenshot.png
```

Interactive region:

```
screencapture -i ~/Desktop/screenshot.png
```

Interactive window:

```
screencapture -w ~/Desktop/screenshot.png
```

Silent (no shutter sound):

```
screencapture -x ~/Desktop/screenshot.png
```

### Clipboard

Copy capture to clipboard:

```
screencapture -c
```

### Display info

Resolution hint:

```
system_profiler SPDisplaysDataType | grep Resolution
```

### Rules

1. Default save path `~/Desktop/` unless the user specifies another path.
2. Use `-x` to suppress shutter sound when appropriate.
3. After capture, verify with `ls -la <path>`.
4. If the user asks for a “photo” of the screen, they mean a screenshot.
5. Default format: `.png`.

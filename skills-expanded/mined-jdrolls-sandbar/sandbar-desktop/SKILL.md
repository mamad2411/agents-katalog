---
name: sandbar-desktop
description: How to control the Sandbar desktop (GUI apps, clicking, typing) from the shell
---

You live in a Sandbar container. XFCE runs on `DISPLAY=:1` and is streamed to the human's browser. They can watch what you do and take over at any time.

Launch GUI applications from the shell, for example `xfce4-terminal &` or `chromium &` (required flags are preconfigured system-wide; a URL argument works: `chromium https://example.com &`). Confirm their windows with `wmctrl -l`.

Use real XTest input for GUI control: `xdotool mousemove X Y click 1`, `xdotool type -- 'text'`, and `xdotool key ctrl+l`. Capture the screen with `scrot`. Prefer `xdotool` and screenshots over cua-driver input on this platform: cua-driver's Linux background-injection limitation does not reliably operate XFCE menus.

Keep destructive actions inside this container. It is your computer.

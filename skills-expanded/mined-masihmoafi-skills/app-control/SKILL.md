---
name: app-control
description: "Drive a desktop Electron app (Elpis desktop, ChatGPT, Claude) as its user does, through its Chromium DevTools port: see, read, click, type. Use to try, test or compare app features first-hand. The Elpis TUI uses tmux instead."
---

# App control

`appctl.py` drives an Electron app through its DevTools port, so you see and use the real window.

```bash
A="python3 -I <this skill folder>/appctl.py"
$A launch elpis               # starts the app with its debug port (elpis 9336, chatgpt 9334)
$A see elpis                  # what the user sees, as text: roles, names, values
$A shot elpis                 # screenshot; open the printed PNG with Read to look at it
$A click elpis "role:button=New chat"   # = whole name, ~= part of one; also text=, label=, css=, xy=
$A type elpis "hello"; $A key elpis Enter
$A eval elpis "document.title"
```

- Look before and after each action: `see` for exact names, `shot` for layout and colour.
- An app started without its debug port must be restarted through `launch`, which closes its open window.
- While an app runs with its debug port, any local program can control it. Close it when done.
- Terminal apps (the Elpis TUI): `tmux new-session -d`, `tmux send-keys`, `tmux capture-pane -p`.

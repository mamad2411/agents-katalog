---
name: tmux-workspace
description: Generate tmuxinator YAML configs and tmux.conf for multi-project terminal workspaces. Use this skill whenever the user wants to set up tmux, tmuxinator, manage multiple projects in terminal panes, create a dev workspace layout, or mentions anything about terminal multiplexing, session management, or running multiple projects side by side. Also trigger when users say things like "set up my projects", "I want all my repos open", "terminal layout", or "workspace setup".
---

# tmux-workspace

Set up a complete tmux + tmuxinator workspace for managing multiple projects in a single terminal session.

## What this skill produces

1. **tmuxinator YAML** (`~/.config/tmuxinator/<name>.yml`) — defines windows, panes, and startup commands
2. **tmux.conf** (`~/.tmux.conf`) — visual improvements and sane defaults

## Step 1: Gather project info

Ask the user for:
- **Project paths** — which directories to include (or auto-detect from current directory)
- **Workspace name** — used as tmuxinator config name and tmux session name
- **Startup commands** (optional) — what to run in each pane (e.g., `claude --continue`, `python train.py`, a plain shell)
- **Monitor pane** (optional) — whether to add a monitoring window (nvidia-smi, htop, log tailing)

If the user doesn't specify, use sensible defaults: one pane per project with a plain shell, tiled layout, and a monitor window with `nvidia-smi` if the machine has a GPU.

## Step 2: Generate tmuxinator config

Create `~/.config/tmuxinator/<name>.yml`. Make sure the directory exists first (`mkdir -p ~/.config/tmuxinator`).

Structure rules:
- Each project gets **one pane** inside a single `projects` window, using `tiled` layout
- Use `cd <path> && <command>` syntax for pane commands (tmuxinator does NOT support `root` at the pane level — only at window level)
- If all panes share the same root, set it at the window level instead
- Optional second window for monitoring tools

Example output:

```yaml
name: research
root: ~/proj

windows:
  - projects:
      layout: tiled
      panes:
        - cd ~/proj/project-a && claude --continue
        - cd ~/proj/project-b && claude --continue
        - cd ~/proj/project-c

  - monitor:
      panes:
        - watch -n2 nvidia-smi
```

## Step 3: Generate tmux.conf

Write `~/.tmux.conf` with these sections. If the file already exists, ask the user before overwriting.

### True color support
Fixes the common issue where colors inside tmux look different from the regular terminal.

```
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",xterm-256color:RGB"
```

### Visual pane borders
Makes pane separation obvious. Active pane gets a bright border with the current path displayed.

```
set -g pane-border-style "fg=colour240"
set -g pane-active-border-style "fg=colour51,bold"
set -g pane-border-status top
set -g pane-border-format " #[fg=colour51]#{pane_index}: #{pane_current_path} #[default]"
```

### Prefix key indicator
Shows in the status bar when `Ctrl+b` is pressed — solves "did I press it?" confusion.

```
set -g status-style "bg=colour235,fg=colour248"
set -g status-left "#{?client_prefix,#[bg=colour202]#[fg=colour232] ^B PRESSED ,#[bg=colour238]#[fg=colour248] NORMAL } "
set -g status-left-length 20
set -g status-right " #S | %H:%M "
set -g window-status-current-style "bg=colour51,fg=colour232,bold"
```

### Essentials

```
set -g mouse on
set -g base-index 1
setw -g pane-base-index 1
set -sg escape-time 10
```

## Step 4: Print usage instructions

After generating both files, tell the user:

```
# Start the workspace
tmuxinator start <name>

# Detach (keeps session running): Ctrl+b d
# Reattach: tmux attach
# Stop everything: tmux kill-server

# Navigate panes:
#   Ctrl+b o        — next pane
#   Ctrl+b ↑↓←→    — directional
#   Ctrl+b q <num>  — by number
# Switch windows:
#   Ctrl+b n/p      — next/prev
#   Ctrl+b 0-9      — by number
```

## Common pitfalls to watch for

- **tmux.conf not loading after edit**: `tmux kill-server` then restart. `kill-session` is NOT enough — the server process caches the config. Alternatively, reload inside tmux with `Ctrl+b :source ~/.tmux.conf`.
- **`source ~/.tmux.conf` in bash**: This is a tmux config, not a bash script. It can only be loaded by tmux itself.
- **Pane-level `root` in tmuxinator**: Not supported. Use `cd <path> && <cmd>` instead.
- **tmuxinator not installed**: `gem install tmuxinator` or `sudo apt install tmuxinator`.

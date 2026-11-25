---
name: tmux-mastery
description: Comprehensive tmux skill covering process management, session/window orchestration, and ricing (visual customization). Use when managing tmux sessions, running dev servers, setting up floating panes, configuring status bars, installing plugins via TPM, or when the user asks about tmux, tmux-sessionx, tmux-floax, catppuccin tmux theme, or making tmux look good.
---

# tmux Mastery

Covers two domains: **process management** (running/monitoring processes) and **ricing** (visual customization and UX plugins).

---

## Process Management

### Interactive Shell Pattern

Always use `send-keys` - never inline commands in `new-session`. This ensures PATH, direnv, and shell init run correctly.

```bash
# WRONG
tmux new-session -d -s myapp -n main 'npm run dev'

# CORRECT
tmux new-session -d -s myapp -n main
tmux send-keys -t myapp:main 'npm run dev' Enter
```

### Session Naming

Derive from git root:

```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)
```

Use **windows**, not separate sessions, for multiple processes in one project.

### Idempotent Start

```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)

if ! tmux has-session -t "$SESSION" 2>/dev/null; then
  tmux new-session -d -s "$SESSION" -n server
  tmux send-keys -t "$SESSION:server" 'npm run dev' Enter
else
  echo "Session $SESSION already exists"
fi
```

### Multiple Processes (Windows)

```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)

tmux new-session -d -s "$SESSION" -n server
tmux send-keys -t "$SESSION:server" 'npm run dev' Enter

tmux new-window -t "$SESSION" -n tests
tmux send-keys -t "$SESSION:tests" 'npm run test:watch' Enter

tmux new-window -t "$SESSION" -n logs
tmux send-keys -t "$SESSION:logs" 'tail -f logs/app.log' Enter
```

### Monitoring Output

```bash
# Last 50 lines from a window
tmux capture-pane -p -t "$SESSION:server" -S -50

# Check for errors
tmux capture-pane -p -t "$SESSION" -S -100 | rg -i "error|fail|exception"

# Poll until ready
for i in {1..30}; do
  tmux capture-pane -p -t "$SESSION:server" -S -20 | rg -q "listening|ready" && break
  sleep 1
done
```

### Lifecycle Commands

```bash
tmux ls                                      # list sessions
tmux list-windows -t "$SESSION"              # list windows
tmux kill-session -t "$SESSION"             # kill session
tmux send-keys -t "$SESSION:server" C-c     # send Ctrl+C
```

### Isolation Rules

- **Never** `tmux kill-server`
- **Never** kill sessions not matching current project
- **Always** verify session name before destructive ops

### When to Use tmux

| Scenario | Use tmux? |
|---|---|
| Dev server / file watcher | Yes |
| Long-running background process | Yes |
| One-shot build (`npm run build`) | No |
| Quick command (<10s) | No |
| Need stdout directly in conversation | No |

---

## Ricing - Visual Customization

### Plugin Manager (TPM)

Install TPM first:

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

Add to `~/.config/tmux/tmux.conf` (or `~/.tmux.conf`):

```conf
set -g @plugin 'tmux-plugins/tpm'
run '~/.tmux/plugins/tpm/tpm'
```

Install plugins: `prefix + I` | Reload: `prefix + r` | Update: `prefix + U`

### Essential Base Settings (omerxx-style)

```conf
set-option -g default-terminal 'screen-256color'
set-option -g terminal-overrides ',xterm-256color:RGB'

set -g prefix ^A                   # Ctrl+A prefix (like screen)
set -g base-index 1                # windows start at 1
set -g detach-on-destroy off       # don't exit tmux when closing a session
set -g escape-time 0               # zero escape time delay
set -g history-limit 1000000       # large scrollback
set -g renumber-windows on         # auto-renumber after close
set -g set-clipboard on            # use system clipboard
set -g status-position top         # status bar at top (macOS style)

setw -g mode-keys vi               # vi keys in copy mode
set -g pane-active-border-style 'fg=magenta,bg=default'
set -g pane-border-style 'fg=brightblack,bg=default'
```

### Catppuccin Theme

```conf
set -g @plugin 'omerxx/catppuccin-tmux'   # omerxx fork with extras

# Window styling
set -g @catppuccin_window_left_separator ""
set -g @catppuccin_window_right_separator " "
set -g @catppuccin_window_middle_separator " █"
set -g @catppuccin_window_number_position "right"
set -g @catppuccin_window_default_fill "number"
set -g @catppuccin_window_default_text "#W"
set -g @catppuccin_window_current_fill "number"
set -g @catppuccin_window_current_text "#W#{?window_zoomed_flag,(),}"

# Status bar modules
set -g @catppuccin_status_modules_right "directory"
set -g @catppuccin_status_modules_left "session"
set -g @catppuccin_status_left_separator " "
set -g @catppuccin_status_right_separator " "
set -g @catppuccin_status_fill "icon"
set -g @catppuccin_status_connect_separator "no"
set -g @catppuccin_directory_text "#{b:pane_current_path}"
```

### tmux-sessionx - Fuzzy Session Manager

```conf
set -g @plugin 'omerxx/tmux-sessionx'

set -g @sessionx-bind 'o'                        # launch with prefix+o
set -g @sessionx-auto-accept 'off'
set -g @sessionx-window-height '85%'
set -g @sessionx-window-width '75%'
set -g @sessionx-zoxide-mode 'on'               # requires zoxide
set -g @sessionx-filter-current 'false'
set -g @sessionx-custom-paths '~/projects'       # always-visible paths
set -g @sessionx-custom-paths-subdirectories 'false'
set -g @sessionx-git-branch 'on'                # show git branch next to session
```

Key bindings inside sessionx:
- `alt+backspace` - delete session
- `Ctrl-r` - rename session
- `Ctrl-w` - switch to window mode
- `Ctrl-e` - expand PWD for local dirs
- `Ctrl-x` - browse `~/.config` or custom path
- `?` - toggle preview

### tmux-floax - Floating Scratch Pane

```conf
set -g @plugin 'omerxx/tmux-floax'

set -g @floax-bind 'p'              # prefix+p to toggle
set -g @floax-bind-menu 'P'         # prefix+P for resize/fullscreen menu
set -g @floax-width '80%'
set -g @floax-height '80%'
set -g @floax-border-color 'magenta'
set -g @floax-text-color 'blue'
set -g @floax-change-path 'true'    # float follows session path
# set -g @floax-session-name 'scratch'   # default session name
```

Floating pane menu options: size down/up, fullscreen, reset, embed.

### Full Recommended Plugin Stack

```conf
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-yank'
set -g @plugin 'tmux-plugins/tmux-resurrect'    # save/restore sessions
set -g @plugin 'tmux-plugins/tmux-continuum'    # auto-save
set -g @plugin 'fcsonline/tmux-thumbs'          # hint-based copy
set -g @plugin 'sainnhe/tmux-fzf'
set -g @plugin 'wfxr/tmux-fzf-url'
set -g @plugin 'omerxx/catppuccin-tmux'
set -g @plugin 'omerxx/tmux-sessionx'
set -g @plugin 'omerxx/tmux-floax'

# Session persistence
set -g @continuum-restore 'on'
set -g @resurrect-strategy-nvim 'session'

run '~/.tmux/plugins/tpm/tpm'
```

### Minimal Config Quickstart

For a clean starting config:

```conf
# ~/.config/tmux/tmux.conf
source-file ~/.config/tmux/tmux.reset.conf   # optional keybind resets

set-option -g default-terminal 'screen-256color'
set-option -g terminal-overrides ',xterm-256color:RGB'

set -g prefix ^A
set -g base-index 1
set -g detach-on-destroy off
set -g escape-time 0
set -g history-limit 1000000
set -g renumber-windows on
set -g set-clipboard on
set -g status-position top
setw -g mode-keys vi

set -g pane-active-border-style 'fg=magenta,bg=default'
set -g pane-border-style 'fg=brightblack,bg=default'

set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'omerxx/catppuccin-tmux'
set -g @plugin 'omerxx/tmux-sessionx'
set -g @plugin 'omerxx/tmux-floax'

set -g @sessionx-bind 'o'
set -g @floax-bind 'p'
set -g @floax-border-color 'magenta'

run '~/.tmux/plugins/tpm/tpm'
```

---

## Additional Resources

- For detailed sessionx key rebinding options, see the [tmux-sessionx README](https://github.com/omerxx/tmux-sessionx)
- For floax menu/sizing options, see the [tmux-floax README](https://github.com/omerxx/tmux-floax)
- Reference dotfiles: [omerxx/dotfiles](https://github.com/omerxx/dotfiles)

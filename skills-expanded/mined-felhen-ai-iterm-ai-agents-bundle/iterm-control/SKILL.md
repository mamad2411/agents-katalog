---
name: iterm-control
description: "Control iTerm from an agent: inspect windows/tabs/sessions, focus targets, create tabs/windows/splits/2x2 grids, close scoped targets safely, set iTerm badges, send commands to panes, run health checks, and take screenshots. Use when the user asks to manage iTerm panes, tabs, windows, badges, layouts, or agent sessions inside iTerm."
---

# iTerm Control

Use this skill to control iTerm topology and pane state through the bundled CLI.
Prefer the CLI over hand-written AppleScript.

## Quick Start

```bash
skills/iterm-control/scripts/iterm-control identify
skills/iterm-control/scripts/iterm-control health
skills/iterm-control/scripts/iterm-control list
skills/iterm-control/scripts/iterm-control focus --target session:<id>
skills/iterm-control/scripts/iterm-control badge --target caller --text "Regi"
skills/iterm-control/scripts/iterm-control tab --target caller --command "zsh -lc 'cd \"$PWD\" && exec codex'"
skills/iterm-control/scripts/iterm-control window --target caller --command "zsh -lc 'cd \"$PWD\" && exec codex'"
skills/iterm-control/scripts/iterm-control split --target caller --direction right --command "zsh -lc 'cd \"$PWD\" && exec codex'"
skills/iterm-control/scripts/iterm-control grid --target caller --rows 2 --cols 2 --command "zsh -lc 'cd \"$PWD\" && exec codex'"
skills/iterm-control/scripts/iterm-control screenshot --output /tmp/iterm-check.png
```

When installed locally, the same script is usually available at:

```bash
~/.agents/skills/iterm-control/scripts/iterm-control
~/.claude/skills/iterm-control/scripts/iterm-control
~/.codex/skills/iterm-control/scripts/iterm-control
```

## Targeting

Use explicit targets for mutating actions:

- `caller`: the terminal that invoked the agent, matched by TTY when possible.
- `current`: iTerm's current session in the current window.
- `session:<id>`: exact iTerm session id from `list` or `identify`.
- `tty:<path>`: exact TTY path, for example `tty:/dev/ttys003`.

If `caller` cannot be matched because the agent runtime is not attached to a TTY,
the CLI falls back to iTerm's current session and reports `caller-fallback-current`
in JSON. Treat that as user-visible focus and verify before destructive actions.

## Common Tasks

Create a right split and start a command:

```bash
iterm-control split --target caller --direction right --command "zsh -lc 'cd /path/to/repo && exec codex'"
```

Create a new tab in the caller/current window and start a command:

```bash
iterm-control tab --target caller --command "zsh -lc 'cd /path/to/repo && exec codex'"
```

Create a 2x2 grid while preserving the caller pane:

```bash
iterm-control grid --target caller --rows 2 --cols 2 --command "zsh -lc 'cd /path/to/repo && exec codex'"
```

Set a badge without typing into the shell:

```bash
iterm-control badge --target session:<id> --text "worker-1"
```

Send a command to a pane:

```bash
iterm-control send --target tty:/dev/ttys005 --text "git status"
```

Validate layout visually:

```bash
iterm-control screenshot --output /tmp/iterm-layout.png
```

Focus an existing pane or tab:

```bash
iterm-control focus --target session:<id>
```

Open a new window for a separate worker:

```bash
iterm-control window --target caller --command "zsh -lc 'cd /path/to/repo && exec codex'"
```

Close a known temporary tab or window after validation:

```bash
iterm-control close --target session:<id> --scope tab --force
iterm-control close --target session:<id> --scope window --force
```

## Rules

- Inspect with `identify` or `list` before mutating layout.
- Use `health` when diagnosing targeting, fallback, or session readiness.
- Prefer `session:<id>` or `tty:<path>` after the first lookup.
- For tabs, use `tab`; it creates the new tab in the same iTerm window as the target session.
- For separate contexts, use `window`; it creates a new iTerm window with the target profile by default.
- For focus changes, use `focus`; it selects the target window, tab, and session.
- For closing, use an explicit `session:<id>` or `tty:<path>` target. Pass `--force` only when the target scope is intentionally current or not at a shell prompt.
- Do not use `send` for a pane running a full-screen TUI unless the user asked.
- For badges, use `badge`; it writes the OSC 1337 sequence directly to the target TTY.
- For screenshots, report the output path and inspect the image when visual proof matters.
- Do not edit iTerm preferences or profiles from this skill.

## References

- [references/recipes.md](references/recipes.md) has common layouts and command examples.
- [references/applescript.md](references/applescript.md) documents the iTerm mechanisms wrapped by the CLI.

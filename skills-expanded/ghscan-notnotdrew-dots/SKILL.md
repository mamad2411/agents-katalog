---
name: help-me-use-herdr
description: >-
  Helps Drew use Herdr as a human: setup, keybindings, plugins, sidebar,
  panels, and local config. Use when he asks how to do something in Herdr,
  what a prefix chord does, which plugin owns a key, or how to get around
  the TUI. Not for controlling another pane from inside Herdr (that is
  `herdr --skill`) and not for spinning up a worktree workspace
  (starting-herdr-work).
---

# Help me use Herdr

Herdr ships two agent-facing docs. They are different jobs:

| Source | Job |
| --- | --- |
| https://herdr.dev/agent-guide.md | Teach / set up / troubleshoot Herdr for a human |
| `herdr --skill` | Control Herdr from inside a pane (`HERDR_ENV=1`) |

This skill is the first job, plus Drew's local overlay. Fetch the agent
guide before answering generic Herdr questions. Do not use `herdr --skill`
or the installed `herdr` skill for "how do I …" questions.

## Drew's overlay (read after the guide)

The agent guide describes defaults. Drew's setup overrides several of them.

1. `~/dots/herdr/keybindings.md` — curated keys worth using, plus a dated
   log of recently added or discussed bindings. Opened in the TUI by
   `prefix+u` (`herdr-help`).
2. `~/dots/herdr/config.toml` — live `[keys]` and `[[keys.command]]`. This
   is the authority for what is actually bound.

`prefix+?` is Herdr's full live keymap. Point him there for exhaustive
lists. Do not paste it.

## When keys change

If this conversation adds, moves, or discusses a binding he should remember:

- Update `~/dots/herdr/keybindings.md` in the matching section.
- Add a dated line under **Recently added or discussed**.
- Reload with `herdr server reload-config` after `config.toml` edits. Do
  not tell him to press `prefix+shift+r`; that key is worktrunk, not reload.

Keep the file a shortlist. "Use these often" is muscle memory, not every
plugin action.

## Local traps (override the guide)

- iTerm's Option key is Normal, so `alt` chords (including the guide's
  `ctrl+alt` prefix-free set) often never reach Herdr. Prefer prefix
  chords or modified arrows (`ctrl+shift+up/down`).
- There is no navigate-mode surface for the Agents panel. `prefix+w` is
  spaces only; agents step with `ctrl+shift+up` / `ctrl+shift+down`.
- `prefix+o` is Herdr's `open_notification_target`. Annotate open is
  `prefix+d`.
- Plugin actions error if the plugin is missing from `herdr plugin list`.
  Reinstall rather than deleting the binding unless he asks.

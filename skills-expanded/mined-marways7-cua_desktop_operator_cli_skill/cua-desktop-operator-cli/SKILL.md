---
name: cua_desktop_operator_cli_skill
description: Windows desktop operation skill for shell-capable AI agents. Use when the agent can run local shell or terminal commands, inspect screenshot file paths, and needs to launch apps, focus windows, click, type, use reusable desktop macros, or run an observe-plan-act-verify loop through the local desktop_operator_cli JSON interface.
---

# CUA Desktop Operator CLI Skill

Use this skill when the user wants desktop control on Windows and the current agent can execute local commands and read JSON and image artifacts.

## What this skill expects

- A local Python runtime with the desktop operator dependencies installed.
- The agent can execute `python -m desktop_operator_cli ...` or `.\scripts\run_cli_command.ps1 ...`.
- The agent can inspect screenshot paths returned by `observe`.
- Temporary artifacts should be cleaned after task success unless the user asked to keep them.

If the runtime is not ready:

1. Run `scripts/setup_runtime.ps1`.
2. Verify `python -m desktop_operator_cli observe` returns JSON.

## Core workflow

Use this loop for almost every GUI task:

1. Run `python -m desktop_operator_cli observe`.
2. Inspect the screenshot, active window, visible windows, and optional cropped window image.
3. Choose the smallest next step.
4. Prefer the highest-signal command that fits:
   - `focus-window` before keyboard input
   - `click-relative` before absolute clicks
   - `uia-*` when a stable control is visible in UIA
   - `run-macro` when the action pattern is reusable
5. After each mutating action, run `observe` or `validate-state`.
6. Repeat until the success condition is visible.
7. If the task is complete and the user did not ask to keep screenshots, logs, or debug traces, run `cleanup-artifacts`.

## Command selection order

Use commands in this order unless the task clearly needs something else:

1. `observe`
2. `find-window` or `list-windows`
3. `focus-window`
4. `run-macro` for stable repeated flows
5. `click-relative` / `uia-click`
6. `paste-text` for Chinese or mixed-language text
7. `type-text` only for short plain text
8. `validate-state`

## Action policy

- Keep actions small and reversible.
- Prefer one to three commands before observing again.
- Use `wait` when the UI is loading instead of stacking blind clicks.
- Use `match-index` whenever multiple similar windows exist.
- Use `run-macro --macro-id __catalog__` to inspect the built-in macro catalog.
- Clean temporary artifacts after successful completion unless the user explicitly asked to retain them.

## Safety policy

- Do not run destructive OS actions unless the user explicitly asked for them.
- Validate focus before typing or pressing submit keys.
- If a click misses once, re-observe before trying again.
- If UIA lookup is slow or empty, return to screenshot-driven interaction.

## References

- CLI command details: `references/cli-command-catalog.md`
- Shell-agent setup: `references/shell-agent-setup.md`
- Interaction patterns: `references/interaction-patterns.md`
- Macro catalog: `references/macro-catalog.md`
- Failure recovery: `references/failure-recovery.md`
- Cross-agent notes: `references/compatibility.md`

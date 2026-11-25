---
name: cross-app-thread-launch
description: >-
  Launch a new agent thread in another app's desktop UI with its prompt already submitted, and
  return a deep link that opens it. Lets Claude Code start a thread in the Codex desktop app, Codex
  start one in the Claude desktop app, either start one in T3 Code, or prefill a ChatGPT web chat.
  Use when asked to "launch a thread in Codex/Claude/T3", "hand this to Codex", "start a Claude
  session for this", "kick off a thread in the other app", or to fan work out across agent apps.
  macOS only.
---

# Cross-app thread launch

Start a visible thread in Claude Code, Codex, T3 Code or ChatGPT from whichever agent you are
running in, and get back a link that opens it in that app's desktop UI.

```bash
<skill-dir>/scripts/launch_thread.py <claude|codex|t3|chatgpt> \
  --cwd <project folder> [--title "<title>"] [--model <model>] "<prompt>"
```

`<skill-dir>` is wherever this skill is installed (for example `~/.claude/skills/cross-app-thread-launch`
or `~/.codex/skills/cross-app-thread-launch`).

Pass `-` as the prompt to read a long brief from stdin (heredoc). The last three lines it prints
are `Thread: <id>`, `Open: <url>` and `Run: <run folder>`. Put the `Open:` link in your reply as a
clickable link. A non-zero exit means nothing launched. Say that plainly, and never report a launch
that didn't happen.

## Picking the app

- **The user named one:** use it.
- **The host app has its own native launch tool** (for example a desktop app's start-session tool,
  or T3's `t3_thread_launch` MCP tool when you are already inside T3): prefer that for same-app
  launches. Use this script for cross-app launches.
- **No app named:** T3 Code if installed, since it fronts both Claude and Codex
  (`--provider claudeAgent` or `--provider codex`). Otherwise the other agent's app.
- **"ChatGPT":** if the user means the Codex desktop app, use `codex` (its link scheme is
  `codex://`). If they mean a ChatGPT web chat, use `chatgpt`. That route only prefills
  `chatgpt.com/?q=`. ChatGPT blocks auto-submit, so the user has to press Enter; say so.

## What each route does

| App | Launch | Link | Opens |
|---|---|---|---|
| `claude` | `claude -p --session-id <uuid> --name <title> --permission-mode acceptEdits`, detached | `claude://resume?session=<uuid>` | When the run finishes (opening mid-run makes the desktop start a second process on the same session) |
| `codex` | `codex exec --json -C <dir> -s workspace-write`, detached; title set afterwards with app-server `thread/name/set` | `codex://threads/<id>` | When the run finishes (the desktop doesn't watch exec threads) |
| `t3` | `~/.t3/bin/t3 thread start <dir> - --json --title ...`; adds the T3 project first if missing; opens T3 Code if its server is down | `t3code://threads/<environment-id>/<thread-id>` | Immediately |
| `chatgpt` | Opens `https://chatgpt.com/?q=<prompt>` | the same URL | Immediately, prefilled and not sent |

Useful flags: `--model`, `--mode` (Claude permission mode), `--sandbox` (Codex: `read-only` for
investigations), `--provider` / `--worktree <base>` / `--branch` (T3), `--no-open`.
T3 threads use the project's default permission mode; there is no flag for it.

Environment: `THREAD_LAUNCH_HOME` moves the run folders; `T3CODE_HOME` and `T3_APP_NAME` point at
a non-default T3 install.

## Writing the prompt

The new thread has none of this conversation's context. Give it the task, essential context,
scope, success criteria, and any real boundaries. Preserve relevant local work and project rules.
Avoid generic checklists and repeated safety boilerplate. For work that spans more than one short
step, ask for a brief plan, updates at meaningful milestones or blockers, and a final recap of
what changed, what was checked, and what remains. Launching several threads: use one script call
per thread and return every `Open:` link.

## After launching

- Starting a thread is not the same as finishing the work. Report it as launched (or running),
  not done.
- Each run folder (`~/.local/state/cross-app-thread-launch/runs/<timestamp>__<app>-<slug>/`) holds
  `launch.log`, the agent's own `receipt.jsonl`, and `manifest.json`. `latest` next to `runs/`
  points at the newest one. Read the receipt to check how a Claude or Codex run ended.
- Follow-ups: Claude `claude -p "<next>" --resume <uuid>`; Codex `codex exec resume <id> "<next>"`;
  T3 `t3 thread --help` (or the T3 MCP `t3_thread_send`).

Route evidence, gotchas and what was not verified: `references/routes.md`.

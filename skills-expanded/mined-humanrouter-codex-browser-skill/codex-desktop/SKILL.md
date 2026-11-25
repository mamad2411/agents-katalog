---
name: codex-desktop
description: Hand a browser task to the Codex DESKTOP APP and get the answer back automatically, with no human copy-paste relay. Use when a browser task needs Codex's Chrome control (your harness's own browser tools are blocked, limited, or you specifically want Codex to do it), e.g. "have codex do this in the browser", "send this to the codex app", "codex browser task". NOT for code questions/second opinions. This is specifically for steering the Codex app's browser/computer-use from another agent.
---

# Codex Desktop Bridge

Send a task to the **Codex desktop app** (which has working Chrome browser
control) and block until its final answer comes back. Replaces the manual
workflow of copying a prompt into the Codex app and pasting the result back
into your primary agent.

## Why this exists

- `codex exec` / `codex app-server` CANNOT use the Chrome plugin from the CLI:
  browser backends report `[]` / `Browser is not available: chrome`. Upstream
  bug openai/codex#26820. The native browser pipe is only injected into
  app-spawned sessions.
- The desktop app's sessions DO have Chrome control. All sessions (app and
  CLI) write rollout JSONL to `~/.codex/sessions/YYYY/MM/DD/`, ending in a
  `task_complete` event carrying `last_agent_message`. The bridge drives the
  app UI via System Events and tails those files.
- **If the upstream issue gets fixed, prefer plain `codex exec` again** (test:
  ask it to list browser backends).

## When to use

1. Browser work your harness can do itself → use your harness's own browser
   tooling first.
2. Browser work that needs a logged-in Chrome + Codex's plugin, or that your
   agent refuses / can't do for privacy reasons, or when you explicitly want
   Codex to run it → THIS skill.
3. Code review / second opinion / research → a plain `codex exec` call, not
   this.

## Usage

```bash
node ~/.claude/skills/codex-desktop/scripts/codex-app-task.mjs \
  --prompt "..." [--timeout 900] [--no-refocus]
# or --prompt-file /path/task.md for long prompts
```

- Prints `SESSION: <rollout file>` then `ANSWER:` + Codex's final message on
  stdout. Progress notes go to stderr.
- Exit codes: 0 ok · 2 prompt never reached a session (send failed) · 3 Codex
  didn't finish before timeout (inspect/tail the session file, it keeps
  running in the app) · 4 bad args / osascript failure.
- For long tasks (browser flows routinely take minutes), run it in the
  background with a generous `--timeout`, then continue when it completes.

## Prompt-writing rules

- Make the prompt fully self-contained: Codex has none of your agent's context.
  Include URLs, exact steps, credential-location hints, and the desired output
  format ("reply with ... as plain text").
- Say explicitly "using your Chrome browser control plugin" for browser tasks.
- State read-only vs allowed-to-modify explicitly.
- The script appends a tracking nonce line to the prompt; that's how it finds
  the right session, and it makes concurrent bridge calls safe.

## Requirements / caveats

- macOS. The Codex desktop app should be RUNNING. If it isn't:
  `open -a Codex && sleep 10` first (activate will launch it, but the File menu
  needs time to exist).
- Needs Accessibility permission for the terminal host running the script.
- Steals focus for ~2 s while it pastes into a New Chat (File → New Chat), then
  tries to refocus the previous app (`--no-refocus` to skip). Focus-return is
  best-effort and app/process-name specific. See the README's focus section.
- Uses the clipboard for the paste; the previous clipboard text is restored a
  few seconds after sending.
- The Codex app runs tasks with whatever approval settings you've configured.
  If approvals are off, tasks run unattended, so prefer read-only phrasing
  unless changes are intended.

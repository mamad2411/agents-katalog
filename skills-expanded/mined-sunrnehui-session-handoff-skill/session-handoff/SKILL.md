---
name: session-handoff
description: Find, inspect, and export prior AI coding-agent conversation sessions into handoff Markdown using `continues`. Use when the user asks to find another account's thread, another window's conversation history, previous Codex or Claude session, context inheritance, session handoff, resume interrupted work, recover from rate limits, transfer context between Codex/Claude/Gemini/Cursor, or says phrases like "找另外一个线程", "另一个账号的对话记录", "交接", "上下文继承", "额度不足继续", "handoff", "resume session", or "continue another thread".
---

# Session Handoff

## Purpose

Create a durable handoff file from local AI coding-agent session history so another account, window, or tool can continue without relying on chat UI context.

Use the installed `continues` CLI first. It reads local session files read-only and writes Markdown handoff files.

## Workflow

1. Confirm the tool exists:
   ```bash
   command -v continues && continues --version
   ```
   If missing, explain that `continues` must be installed before this skill can operate.

2. Decide the source:
   - User says Codex / 当前 Codex / 官方账号 Codex / API 账号 Codex: use `codex`.
   - User says Claude / Claude Code: use `claude`.
   - User does not specify: list both Codex and Claude candidates, then choose the most plausible recent one from cwd, summary, and timestamp.

3. List candidates before exporting:
   ```bash
   continues list --source codex -n 10
   continues list --source claude -n 10
   ```
   Prefer the latest session from the same project directory unless the user names a project, topic, or tool.

4. Export a handoff file with the bundled script. Resolve `<skill-dir>` as the directory containing this `SKILL.md`. By default it writes to `~/Documents/Codex-Handoffs/` so the file is easy to find:
   ```bash
   python3 <skill-dir>/scripts/handoff.py --source codex
   ```
   Useful variants:
   ```bash
   python3 <skill-dir>/scripts/handoff.py --source claude
   python3 <skill-dir>/scripts/handoff.py --id <session-id> --preset full
   python3 <skill-dir>/scripts/handoff.py --source codex --query "my project" --preset standard
   python3 <skill-dir>/scripts/handoff.py --source codex --query "app launch failure" --preset standard
   python3 <skill-dir>/scripts/handoff.py --source codex --out-dir ~/Desktop
   ```

   The script validates the exported Markdown before reporting success. Required checks include session id, Session Overview, Current State, Recent Conversation, and Session Origin. It also requires at least one useful detail section: Tool Activity or Files Modified.

   The script searches up to 2000 recent indexed sessions by default so older but relevant threads can be found by query.

5. Give the user:
   - the selected session id,
   - source tool,
   - cwd / project,
   - updated time,
   - handoff file path,
   - exact prompt to paste into the new account/window.

## Same-Tool Account Switch

For Codex official-account to Codex API-account handoff, do not rely on `continues resume <id> --in codex`. `continues` treats same-tool resume as native resume, while cross-account Codex needs a portable handoff document.

Use:
```bash
continues inspect <session-id> --preset standard --write-md ~/Documents/Codex-Handoffs/<name>.md
```

Then tell the new session:
```text
请先读取 <handoff.md>，按里面的 Current State、Recent Conversation、Tool Activity、Files Modified（如果有）、Session Origin 继续任务。不要从头开始。
```

## Cross-Tool Transfer

When the target is a different tool, the direct command may work:
```bash
continues resume <session-id> --in claude
continues resume <session-id> --in codex
continues resume <session-id> --in gemini
```

If the user wants inspection or account switching rather than launching a new tool, export Markdown instead.

## Preset Choice

- `minimal`: urgent low-token handoff.
- `standard`: default.
- `verbose`: complex debugging or multi-file work.
- `full`: high-risk long task where losing context is worse than a larger file.

## Default Output Location

Write handoff files to:

```text
~/Documents/Codex-Handoffs/
```

Use `--out-dir <path>` only when the user asks for another location.

## Guardrails

- Treat session export as local read-only recovery. Do not delete, edit, or compact raw session files.
- Do not paste long handoff contents into the chat unless the user asks; provide the file path and concise summary.
- If multiple sessions match, show the top candidates and explain which one was selected.
- If sensitive credentials appear possible, prefer handing off by file path instead of quoting raw contents.

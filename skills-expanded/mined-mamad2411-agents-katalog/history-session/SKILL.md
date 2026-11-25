---
name: history-session
description: "Display historical Claude Code sessions for the current directory, letting users decide whether to --resume a previous session. Reads sessions-index.json and .jsonl files from ~/.claude/projects/. Use when user types /history-session or says '历史会话', 'history session', '查看历史', '看看历史会话'."
---

# history-session

Display historical Claude Code sessions for the current directory so the user can decide whether to `--resume` one.

## Trigger

Use this skill when the user types:
- `/history-session`
- "历史会话"、"history session"、"查看历史"、"看看历史会话"

## Steps

**Step 1: Run the lookup script**

```bash
python3 ~/.claude/skills/history-session/scripts/history_session.py "$PWD"
```

**Step 2: Display results**

- If output is `NO_SESSIONS`: reply "当前目录没有历史会话记录。"
- Otherwise, display under the heading `📋 历史会话（当前目录）`, outputting the script result **exactly as-is** — do not reformat, do not convert to a table, do not omit any lines.

Each session is two lines: the first shows the summary, the second shows the `claude --resume` command. Both lines must be shown.

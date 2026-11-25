---
name: session-handoff
description: Keep long Claude Code sessions from eating usage limits. `write` builds a HANDOFF.md from the session log (files edited, commands run, recent requests, last todo list, git status and recent commits, secrets redacted) with sections Claude fills in (goal, done, decisions, open problems, next steps), so the user can /clear and continue in a cheap fresh session. `meter` is a Stop hook that warns the user when the context passes ~150k tokens. Use when a session is long or drifting, when the user says "write a handoff", "summarize where we are", "I need to restart", or when context warnings appear.
---

# session-handoff

`scripts/handoff.mjs` is zero-dependency Node 22+ and reads the local logs in `~/.claude/projects/`.

Every message in a session re-sends the whole context. At 300k+ tokens even "thanks" costs as much as reading a book, and the claude-token-audit skill usually shows a few long sessions eating most of the usage. A good handoff plus `/clear` resets that to a few thousand tokens.

## Writing a handoff (when the user asks, or the meter fires)
1. `node handoff.mjs write` (in the project folder). It picks this session automatically, even with several Claude Code windows open. `--session <id-prefix>` or `--transcript <file>` choose explicitly; `--out` changes the file name.
2. Open `HANDOFF.md` and replace every `<!-- CLAUDE: … -->` placeholder from your knowledge of the session. Be short and concrete: real file names, exact error messages, commands that worked, what the user explicitly decided or rejected. Don't pad. The "Facts from the session log" section is already filled.
3. Tell the user: **run `/clear`, then say "Read HANDOFF.md and continue"**. Remind them HANDOFF.md is a working note (the script warns if it isn't gitignored).

Secrets in commands and prompts (API keys, tokens, `PASSWORD=…`, credentialed URLs) are replaced with `[redacted]` in the facts section. Still read it before sharing.

## Context meter (Stop hook)
If you installed the binay-skills plugin, the meter is already on (it ships in the plugin's `hooks/hooks.json`); turn it off with `"env": { "BINAY_SKILLS_HOOKS_OFF": "session-handoff" }`. Without the plugin, ask the user before adding it:
```json
{ "hooks": { "Stop": [ { "hooks": [ { "type": "command", "command": "node \"/ABSOLUTE/PATH/session-handoff/scripts/handoff.mjs\" meter" } ] } ] } }
```
After each reply it reads the tail of the transcript. Once context passes 150k tokens it shows the user one line suggesting a handoff or `/compact`, then again every +50k (`HANDOFF_WARN_TOKENS`, `HANDOFF_STEP_TOKENS`). Silent otherwise, and it fails open.

`node handoff.mjs status` prints the current context size.

## Limits
- The facts come from the log. The *why* comes from Claude filling the sections, so the handoff is only as good as that summary. Write it before the context is so long that early details are fuzzy.
- `/compact` is the built-in alternative when you want to stay in the same session. A handoff file survives across sessions, machines and teammates.

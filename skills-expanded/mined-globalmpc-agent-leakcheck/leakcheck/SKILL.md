---
description: Scan this machine for what coding agents (Claude Code, Codex, Cursor, Gemini CLI) can reach, such as .env files, plaintext tokens, loose SSH key permissions and risky approval modes. Use when the user asks to run agent-leakcheck, audit agent security or check for leaked secrets.
allowed-tools: Bash(npx -y @globalmpc/agent-leakcheck@latest --json)
---

Run `npx -y @globalmpc/agent-leakcheck@latest --json` and read the JSON from stdout.

Then tell the user, in plain words:
1. The grade and score.
2. Each failing check: what it means, which agent, and the `fix` text from the output.
3. Info and warning rows (for example secret-looking env var names) in one short list.

Rules:
- Never run `--fix` or `--share` unless the user explicitly asks for it in this conversation. If they ask for `--fix`, show the planned changes first and wait for a clear yes.
- Never print, guess or ask for secret values. The tool only reports names and paths.
- Do not edit config files yourself to apply fixes; give the fix text and let the user decide.
- If `npx` is missing or the command fails, show the error as is and stop.

---
name: setup-doctor
description: Check a lean-agents install and propose exact fixes. Use when the user asks if lean-agents works, a tool seems missing, or something stopped loading after an update.
---

# setup-doctor

1. Run the doctor. It changes nothing:
   `curl -fsSL https://github.com/estebanmr99/lean-agents/releases/latest/download/install.sh | bash -s -- --doctor`
2. Read the table. Keep only lines marked `error`, `missing` or `changed`.
3. For each line, say what it means in one sentence and give the exact fix:
   - `changed` on a file you did not edit, or `i-have-adhd skill`: an update reset it. Fix: run the same command with `--update`.
   - `missing` on a binary: name the install command from `docs/manual-install.md`.
   - `error` on an MCP server or plugin: run the agent's own list command (`claude mcp list`, `copilot mcp list`, `agy mcp list`, `opencode debug config`) and quote the line that shows why.
4. Ask before running any fix. Never edit a file marked `managed by lean-agents` by hand: `--update` rewrites it.
5. Report what passed, what you fixed and what still needs the user, such as logging in.

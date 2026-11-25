---
name: cf
description: >
  Use when switching AI coding tools (Claude Code, Codex, Cursor, OpenCode, Copilot CLI, Gemini CLI) due to rate limits,
  cost optimization, or model capability gaps. Triggers on "/cf save", "/cf load", "/cf status", "/cf diff",
  "/cf validate" commands. Also use when the user mentions losing context, repeating work across tools,
  session migration, context transfer, or needing to save/restore conversation state between coding agents.
license: MIT
compatibility: >
  Requires Bash to run Python scripts in scripts/. Requires Read, Glob, Grep to discover
  session files on disk. Works on Linux, macOS, and Windows.
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
metadata:
  audience: developers
  workflow: session-migration
---

# ContextFlow — /cf

Save and load session context across AI coding tools. Provides five slash commands:

- `/cf save` — persist current session to `.session-bridge/`
- `/cf load <id>` — restore a saved session's context
- `/cf status` — list saved snapshots
- `/cf diff <id1> [<id2>]` — compare two snapshots
- `/cf validate <id>` — validate a snapshot against the USF schema

## Save

User says `/cf save`. Execute `scripts/cf-save.py` with Bash.

**Workflow checklist — track progress:**
- [ ] Detect current tool
- [ ] Extract session data from tool storage
- [ ] Capture git file state
- [ ] Redact secrets
- [ ] Write USF + summary to `.session-bridge/`
- [ ] Auto-add `.session-bridge/` to `.gitignore`
- [ ] Run `/cf validate` on the saved snapshot

After the script finishes, read `session.summary.md` and relay key info to the user. Then run `/cf validate` to confirm the output is valid — if validation fails, investigate and re-save.

No LLM used by the script. Works during rate limits. Direct run:
```
python3 scripts/cf-save.py    # macOS/Linux
py scripts/cf-save.py         # Windows (Bash or PowerShell)
```

**Flags:** `--label`, `--session-id`, `--tool`, `--project-dir`, `--global`, `--no-cleanup`

## Load

User says `/cf load <snapshot-id>` (or `/cf load latest`).

**Workflow checklist — track progress:**
- [ ] Execute `scripts/cf-load.py` to read the snapshot
- [ ] Read `session.summary.md` for quick orientation
- [ ] Analyze USF — reclassify tool calls, summarize decisions, identify next steps
- [ ] Present findings and continue the work

**Important:** The script itself does not use an LLM — it generates a markdown context document. The *agent* (you) uses LLM reasoning to analyze the output and continue the task.

**Compatible tools:** Bash, Read, Edit, Write, Glob, Grep, FileEdit, Replace — available in every tool. Pass through unchanged.

**Incompatible tools:** ClaudeCode, Skill, Terminal, Message — tool-specific. Translate each into a human-readable summary of what it accomplished. The effects are visible in file state.

## Status

User says `/cf status`. Execute `scripts/cf-status.py` with Bash.

Lists all snapshots in `.session-bridge/` with size, age, tool, and message count.

## Diff

User says `/cf diff <id1> [<id2>]`. If `<id2>` omitted, compare against latest. Execute `scripts/cf-diff.py` with Bash.

Compares two snapshots at the field level: source metadata, file state, conversation length, decisions, intent.

## Validate

User says `/cf validate <id>`. Execute `scripts/cf-validate.py` with Bash.

Validates against `schemas/usf-schema.json` dynamically. Reports missing fields, type mismatches, and warnings.

## Retention

Save script automatically removes snapshots older than 30 days. Pass `--no-cleanup` to skip.

## Universal Session Format (USF)

Five layers: `source` (tool/model), `snapshot` (metadata), `file_state` (git), `conversation` (messages), `tool_calls` (compatible/incompatible), `decisions` (choices), `current_intent` (task state).

- **Schema:** `schemas/usf-schema.json` — full type definitions, required fields, enums
- **Field guide:** `references/usf-guide.md` — per-field docs, extraction notes, privacy redaction details
- **Tool sources:** `references/tool-sessions.md` — session file locations per tool, read when save fails

## Privacy

The save script redacts:
- API key/secret/token assignment patterns
- OpenAI-style keys (`sk-...`), GitHub tokens (`ghp_`/`gho_`/`ghs_`), AWS keys (`AKIA...`)
- JWT tokens (`eyJ...`)
- PEM private key headers

## Installation

Clone the repo and link it into the tool's skills directory.

### OpenCode
```bash
# Unix
ln -s "$(pwd)/context-flow" ~/.config/opencode/skills/cf

# Windows (Admin PowerShell)
New-Item -ItemType Junction -Path "$env:USERPROFILE\.config\opencode\skills\cf" -Target "$pwd\context-flow"
```

### Claude Code
```bash
ln -s "$(pwd)/context-flow" /path/to/project/.claude/skills/cf
```

### Any tool
Copy or link the repo root into the tool's configured skills path.

## Examples

**Rate-limit switch:**
User hits a rate limit in Claude Code → `/cf save` → opens Codex → `/cf load latest` → continues without re-explaining.

**Cost optimization:**
User finishes design in Claude Opus → `/cf save --label design-review` → switches to cheaper model → `/cf load design-review` → implements based on saved decisions.

**Same-tool model switch:**
User does `/cf save` → switches model in same tool → `/cf load latest` → identifies incompatible tool calls and continues.

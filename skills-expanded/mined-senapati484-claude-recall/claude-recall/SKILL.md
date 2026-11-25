---
name: claude-recall
description: >
  Always-on Claude Code skill that bridges Claude with an Obsidian vault for persistent
  project memory. Automatically loads relevant context nodes from mindmap.json before every
  prompt (UserPromptSubmit hook) and saves structured session notes to the vault on exit
  (Stop hook). Zero manual invocation — hooks fire automatically.

  Context is AUTO-GENERATED using the claude CLI. Claude analyzes
  transcripts and project files to populate mindmap.json with stack, architecture decisions,
  gotchas, and current state. Users never need to manually edit.

  The /recall command lets users trigger on-demand context updates from the terminal.
  MCP tools (recall_get, recall_update_node, recall_session_history, recall_mindmap) let
  Claude fetch deeper context mid-session.

  Storage: <vault>/claude-recall/projects/<project-slug>/mindmap.json (JSON graph)
  and sessions/YYYY-MM-DD_HH-MM.md (session notes). Project slug is derived from
  the directory Claude Code was launched in.

  Install from GitHub (one command):
    curl -fsSL https://raw.githubusercontent.com/senapati484/claude-recall/main/install.sh | bash

  Requires: Python 3.8+, Obsidian, Claude Code CLI in PATH. API keys are optional fallbacks.

  Consult this skill for: install help, Obsidian vault path issues, hooks not firing,
  context not loading, sessions not saving, editing context.md, vault folder structure,
  slug mapping questions, config options, uninstalling, /recall commands.
---

# claude-recall

Obsidian-backed persistent memory for Claude Code. Install once, works on every session.
**All context is auto-generated** using a local LLM — no manual Obsidian editing required.

## Session Model

A **session = one terminal session** (open terminal → close terminal or `/exit`).
This is NOT per-prompt. The session marker at `~/.claude/.recall_<session_id>` prevents
context re-injection after the first prompt of a session.

```
Terminal session opens → UserPromptSubmit fires → context loaded ONCE
Terminal session continues → UserPromptSubmit fires → SKIPPED (marker exists)
Terminal session closes → Stop hook fires → session note written, context updated
```

## How It Works

```
Session start   →  load_context.py    →  keyword match  →  inject 2-3 relevant nodes
Tool use       →  post_tool_use.py   →  mark_files_stale() on Edit/Write/Create
Session end    →  save_context.py    →  claude CLI → update mindmap.json nodes
/recall query  →  MCP server recall_get() → return relevant context nodes
```

Both hooks run via Claude Code hooks in `~/.claude/settings.json`. No invocation needed.
The `/recall` command is invoked directly by the user during a Claude session.
MCP tools are available for Claude to call mid-session for deeper context.

### Hook Events
- **UserPromptSubmit**: Injects relevant context nodes based on current prompt keywords
- **PostToolUse**: Marks mindmap nodes stale when files are edited (Edit, Write, MultiEdit, Create)
- **Stop**: Analyzes full transcript via claude CLI, updates mindmap.json, writes session note

## LLM Model

## LLM Model

claude-recall natively uses **claude CLI** — meaning it inherits your Claude Code auth.
API keys are only used as fallback.

- Backend 1 (Primary): `claude` CLI backend
- Backend 2: `ANTHROPIC_API_KEY` (haiku-4-5)
- Backend 3: NVIDIA NIM
- If missing all: gracefully falls back to regex-based context extraction
- LLM is used for:
  - Session summarization (what was done, decisions, next steps, files_and_roles)
  - Project context generation (via /recall update)
  - Re-summarizing stale nodes after file edits
  - MCP tool responses for deeper context queries

---

## /recall Command

To manually refresh project context during a session, **type the full command**:
```
/Users/sayansenapati/.claude/skills/claude-recall/scripts/recall_update.py update
```

Or from any project directory, run:
```
python3 ~/.claude/skills/claude-recall/scripts/recall_update.py update
```

Available actions:
- `update` — Scan project with LLM and regenerate context.md
- `status` — Show current context.md content
- `reset` — Delete context.md and regenerate from scratch

**Note**: `/recall` is not a native Claude Code command. You must use the full path above.
The hint shown in Claude's context will remind you of this each session.

## Quick Reference

| What you type | What happens |
|---|---|
| Full path above | Runs /recall update — LLM regenerates context.md |
| (context loads automatically) | Happens on first prompt of every session |

---

## Auto-Context Generation

Claude automatically generates and updates `context.md` content:

- **On first session load**: Analyzes transcript + scans project files to auto-populate context
- **On every session end**: LLM analyzes full transcript → merges new learnings into context.md
- **On `/recall update`**: LLM scans filesystem for stack, structure, and README → updates context.md

### Auto-marker system
Auto-generated content is wrapped in markers:
```markdown
## Stack
<!-- auto:stack:start -->
Next.js 16 · Tailwind CSS · TypeScript
<!-- auto:stack:end -->
```

- **Inside markers**: Managed by claude-recall, updated automatically
- **Outside markers**: User-owned, NEVER modified by auto-updates

---

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/senapati484/claude-recall/main/install.sh | bash
```

The installer:
1. Checks Python 3 + Claude Code are present
2. Asks for your Obsidian vault path (once — saved to `~/.claude/claude-recall.json`)
3. Clones the repo to `~/.claude/skills/claude-recall/`
4. Installs `anthropic` and `fastmcp` via pip
5. Checks for `claude` CLI and optional API keys
6. Registers `UserPromptSubmit`, `Stop`, and `PostToolUse` hooks + MCP server in `~/.claude/settings.json`
7. Creates `<vault>/claude-recall/` folder structure

**Then restart Claude Code.**

---

## Obsidian Vault Structure

```
<your-vault>/
└── claude-recall/
    ├── _index.md                    ← deduplicated project table (auto-updated)
    └── projects/
        └── <project-slug>/
            ├── context.md           ← auto-populated + user can edit
            └── sessions/
                └── YYYY-MM-DD_HH-MM.md   ← auto-written on exit
```

**`context.md`** is the permanent memory file — auto-populated with project stack,
architecture decisions, gotchas, and current state. Users can add their own notes
outside the auto-markers. Claude reads it before your first message every session.

**`_index.md`** shows each project ONCE with accumulated stats:
```
| Project | Directory | Sessions | Total Turns | Last Active |
|---------|-----------|----------|-------------|-------------|
| setu    | `/home/.../setu` | 5 | 127 | 2025-01-16 14:07 |
```

**Project slug** is derived from the directory you launched `claude` in:
`/home/sayan/projects/setu` → `setu`, `/home/sayan/client/acme` → `client-acme`

---

## Scripts

- `scripts/load_context.py` — `UserPromptSubmit` hook. Fires on every prompt.
  - Injects 2-3 relevant context nodes based on keyword matching
  - Auto-generates mindmap.json on first load if missing
  - Loads relevant nodes + last session summary → stdout for Claude
  - Starts MCP server process for recall tools
- `scripts/save_context.py` — `Stop` hook. Fires on exit.
  - Parses full transcript (all messages, tool calls, errors, file ops)
  - Generates structured summary (summary, decisions, files_and_roles, keywords) via LLM
  - Updates mindmap.json nodes with session learnings
  - Writes context.md (Obsidian-readable) from mindmap
  - Writes session note to sessions/YYYY-MM-DD_HH-MM.md
  - Updates _index.md
- `scripts/summarize.py` — LLM summarizer.
  - Automatically routes to claude CLI or Anthropic/NIM APIs
  - Returns structured JSON: summary, decisions, files_and_roles, next_steps, keywords
  - Falls back to regex if LLMs unavailable
- `scripts/mindmap.py` — Mindmap storage + retrieval.
  - load_mindmap(), save_mindmap(), get_relevant_nodes()
  - upsert_node(), mark_files_stale(), build_initial_mindmap_from_stack()
  - mindmap_to_context_md() for Obsidian viewing
- `scripts/mcp_server.py` — FastMCP server.
  - Exposes recall_get(), recall_update_node(), recall_session_history(), recall_mindmap()
  - Claude can call these mid-session for deeper context
- `scripts/post_tool_use.py` — `PostToolUse` hook.
  - Marks mindmap nodes stale when files are edited (Edit, Write, MultiEdit, Create)
- `scripts/recall_update.py` — `/recall` command.
  - `update`: Build initial mindmap from filesystem + README
  - `status`: Show mindmap as tree with stale indicators
  - `query`: Search mindmap for relevant nodes
  - `reset`: Delete and regenerate mindmap.json
- `scripts/utils.py` — shared helpers:
  - `llm_available()` — checks for claude CLI or API keys
  - `get_anthropic_client()` — cached Anthropic client
  - `merge_auto_section()` — preserves user content outside auto-markers
  - `detect_project_stack()` — scans package.json, requirements.txt, etc.

---

## Config (`~/.claude/claude-recall.json`)

```json
{
  "vault_path": "/path/to/your/vault",
  "vault_folder": "claude-recall",
  "max_context_tokens": 400,
  "include_recent_sessions": 2,
  "save_sessions": true,
  "load_on_every_prompt": true,
  "use_claude_api": true
}
```

| Key | Default | Description |
|---|---|---|
| `vault_path` | required | Absolute path to your Obsidian vault |
| `vault_folder` | `claude-recall` | Folder name created inside the vault |
| `max_context_tokens` | `400` | Token budget for injected context (~1.6K chars) |
| `include_recent_sessions` | `2` | How many past session notes to load |
| `load_on_every_prompt` | `true` | Reload relevant context on every prompt |
| `use_claude_api` | `true` | Use Claude API for summarization |

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Context not loading | Check hooks in `~/.claude/settings.json`; restart Claude Code |
| "Vault not found" error | Check vault_path in config; verify drive is mounted |
| Sessions not saving | Verify vault is writable; check `save_sessions: true` in config |
| Wrong project loaded | Launch `claude` from the correct project directory |
| Mindmap is empty | Run `/recall update` to populate from filesystem |
| "claude CLI: not found" | Install Claude Code and ensure it's in your PATH |
| Hook errors | Run `echo '{"cwd":"'$(pwd)'","session_id":"t"}' \| python3 ~/.claude/skills/claude-recall/scripts/load_context.py` |
| Re-install / update | Re-run the `curl` install command — detects existing install |

---

## When Helping the User

- **First-time setup**: walk through install → vault path → restart → test with a prompt
- **Context not appearing**: check hook registration → run load script manually → open vault
- **Editing context**: guide to `<vault>/claude-recall/projects/<slug>/context.md` in Obsidian
  - Auto-generated sections are inside `<!-- auto:*:start/end -->` markers
  - User can add their own content anywhere outside markers
- **LLM model missing**: explain auto-download or manual download from HuggingFace
- **Token savings**: explain that pre-loaded context avoids repeated codebase discovery
- **/recall commands**: run `recall_update.py` when user asks for context refresh

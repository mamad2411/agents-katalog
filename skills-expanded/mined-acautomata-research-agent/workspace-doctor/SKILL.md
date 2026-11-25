---
name: workspace-doctor
description: >
  Create, validate, update, and sync OpenClaw agent workspaces. Handles the full lifecycle:
  scaffolding new workspaces with all required files (SOUL.md, AGENTS.md, IDENTITY.md, USER.md,
  TOOLS.md, MEMORY.md, HEARTBEAT.md, DREAMS.md), updating individual workspace files while
  preserving existing conventions, validating consistency between workspace directories and
  openclaw.json registration, and syncing agent configs. Use this skill whenever the user
  mentions workspaces, agent setup, subagent creation, workspace files (SOUL/AGENTS/IDENTITY/etc),
  workspace validation, or any task that involves creating or modifying agent workspace directories.
  Also use when the user says "add a new agent", "set up workspace", "check workspaces",
  "fix workspace", "sync agent config", or mentions workspace-maintenance tasks — even if they
  don't explicitly say "workspace-doctor".
---

# Workspace Doctor

You maintain OpenClaw agent workspaces — the `workspace-<agentId>/` directories that define each agent's identity, behavior, and tools.

This skill covers four operations: **create** (scaffold a new workspace), **update** (modify individual files), **validate** (check consistency), and **sync** (align openclaw.json with workspace reality).

## Understanding the Workspace System

Each OpenClaw agent owns a workspace directory containing Markdown files that shape its behavior. The main agent lives in `workspace/`; sub-agents live in `workspace-<agentId>/` where `<agentId>` matches the `id` field in `openclaw.json` → `agents.list[]`.

Agents are registered in `openclaw.json` under `agents.list`:
```json
{ "id": "agent-id", "name": "Display Name", "workspace": "~/.openclaw/workspace-agent-id" }
```

Sub-agents must also be listed in `agents.defaults.subagents.allowAgents`.

## Operation 1: Create — Scaffold a New Workspace

When the user wants to add a new agent, you create the workspace directory and all required files, then register the agent in `openclaw.json`.

### Step 1: Gather Requirements

Ask the user (if not already specified):
1. **Agent ID** — kebab-case identifier (e.g. `paper-review`, `autoresearch`). This becomes the directory name.
2. **Agent name** — human-readable display name
3. **Role** — one-phrase description of what this agent does (the single-responsibility principle: can you describe it in one verb phrase?)
4. **Is it a sub-agent?** — most new agents are sub-agents spawned by the main agent via `sessions_spawn`. Only the main agent uses `workspace/` without a suffix.
5. **Any special tools or wiki access needed?** — determines if sandbox binds are needed.

### Step 2: Create the Workspace Directory

```bash
mkdir -p workspace-<agentId>
```

### Step 3: Create Each Workspace File

Write each file following the conventions documented in `references/file-templates.md`. The key conventions:

**SOUL.md** — The agent's persona, personality, and boundaries. This is NOT a job description — it's who the agent *is*. Every workspace SOUL.md follows this pattern:
```markdown
# SOUL.md - 你是谁

_你是 [Agent Name]，不是 [what it's not]。_

## 身份
[One-line role description with personality]

## 核心
[4-6 behavioral principles, each with a bold summary + one-line explanation]

## 风格
[Communication style bullets]

## 边界
[What the agent will NOT do]

---
_[Closing line]. 操作手册见 AGENTS.md。_
```

**AGENTS.md** — Operating procedures and task workflows. This IS the job description. Structure:
```markdown
# AGENTS.md — [Agent Role Description]

## 会话启动
[What to read on session start]

## 核心职责
[Primary responsibilities]

## 任务流程
[Step-by-step workflows for each task type]

## 产出规范
[Output format requirements]
```

**IDENTITY.md** — Agent's name, appearance, vibe, emoji. Sub-agents can have simpler entries than the main agent.

**USER.md** — Who the agent's user is. For sub-agents, this is often the main agent that spawns them.

**TOOLS.md** — Environment-specific tool notes. Read `references/file-templates.md` for the standard template.

**MEMORY.md** — Starts as an empty structure: `# Long-Term Memory\n\n_(Promoted content will appear here)_`

**HEARTBEAT.md** — Default template:
```markdown
# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.
# Add tasks below when you want the agent to check something periodically.
```

**DREAMS.md** — Starts empty: `# Dream Diary\n\n<!-- openclaw:dreaming:diary:start -->\n<!-- openclaw:dreaming:diary:end -->`

### Step 4: Register in openclaw.json

Add an entry to `agents.list`:
```json
{
  "id": "<agentId>",
  "name": "<Display Name>",
  "workspace": "~/.openclaw/workspace-<agentId>"
}
```

If it's a sub-agent, add the ID to `agents.defaults.subagents.allowAgents`.

If the agent needs read access to shared wiki or other agent outputs, add volume binds to `agents.defaults.sandbox.docker.binds`.

### Step 5: Update .gitignore

Add runtime-state exclusions for the new workspace if needed (e.g., `workspace-<agentId>/memory/`, `workspace-<agentId>/state/`).

## Operation 2: Update — Modify Workspace Files

When updating an existing workspace file, follow these rules:

1. **Read before writing.** Always read the current file first to understand existing conventions, language (Chinese vs English), and formatting patterns.

2. **Match existing style.** If SOUL.md uses Chinese headers, keep Chinese headers. If AGENTS.md uses tables for routing, use tables. Don't reformat.

3. **Preserve what works.** Only change what the user asked to change. Don't "improve" adjacent content, comments, or formatting.

4. **File-specific update guidance:**

| File | Update with care because... |
|------|---------------------------|
| SOUL.md | Defines the agent's core identity. Changes here affect all behavior. Keep the 身份/核心/风格/边界 structure. |
| AGENTS.md | Contains routing logic and workflows. Changes must be consistent with openclaw.json agent list. |
| IDENTITY.md | Cosmetic only. Safe to update freely. |
| USER.md | Grows organically. Add new user context at the end. |
| TOOLS.md | Environment-specific. Verify tool names and paths against actual setup. |
| MEMORY.md | Append-only in general. Only prune with explicit user instruction. |
| HEARTBEAT.md | Should stay minimal to avoid token burn on heartbeat runs. |
| DREAMS.md | Auto-generated by dreaming system. Don't edit manually unless asked. |

## Operation 3: Validate — Check Workspace Consistency

Run a full consistency check when the user asks to "validate workspaces", "check consistency", or when you suspect drift between config and filesystem.

### Checklist

Run through these checks for every registered agent:

1. **Directory exists** — Does `workspace-<agentId>/` exist for every `agents.list[].id`?
2. **All required files present** — SOUL.md, AGENTS.md, IDENTITY.md, USER.md, TOOLS.md, MEMORY.md, HEARTBEAT.md must exist. DREAMS.md is optional but recommended.
3. **No orphan workspaces** — Does every `workspace-*/` directory have a matching `agents.list[]` entry?
4. **Workspace path matches** — Does `agents.list[].workspace` resolve to the actual directory?
5. **allowAgents sync** — Is every sub-agent in `agents.list[]` also in `agents.defaults.subagents.allowAgents`?
6. **File structure valid** — SOUL.md has 身份/核心/风格/边界 sections; AGENTS.md has 会话启动/核心职责 sections.
7. **No secrets in files** — Grep for API keys, tokens, passwords in workspace files.
8. **Sandbox binds reference real directories** — Every bind in `agents.defaults.sandbox.docker.binds` maps to an existing path.

Report results as a table:

| Check | Agent | Status | Detail |
|-------|-------|--------|--------|
| Directory exists | main | ✅ | workspace/ present |
| ... | ... | ... | ... |

## Operation 4: Sync — Align Config with Reality

When filesystem and openclaw.json have drifted apart:

1. **Read openclaw.json** — extract `agents.list` and `agents.defaults.subagents.allowAgents`.
2. **Scan workspace directories** — glob for `workspace*/` at the repo root.
3. **Compute diff** — find mismatches between the two.
4. **Propose fixes** — for each mismatch, suggest the specific edit needed:
   - Missing registration → add `agents.list` entry
   - Missing allowAgents entry → add to array
   - Orphan directory → either register it or flag for deletion
   - Wrong workspace path → fix the path in openclaw.json
5. **Apply only after confirmation** — config changes affect running agents.

## Important Conventions

- **Language**: Main agent workspace files use Chinese. Sub-agent SOUL.md files mix Chinese headers with English/Chinese body. Match the existing pattern of the workspace you're editing.
- **Single responsibility**: Each sub-agent should be describable in one verb phrase. If an agent grows beyond that, flag it for splitting.
- **Wiki access**: Sub-agents that need wiki access require explicit sandbox volume binds. Check `agents.defaults.sandbox.docker.binds` when creating new agents.
- **Skills placement**: Sub-agent skills go in `workspace-<agentId>/skills/<skill-name>/SKILL.md`. Main agent skills go in `.claude/skills/<skill-name>/SKILL.md`.
- **.gitignore**: Runtime state (memory/, state/, .dreams/, *.sqlite, logs/) is gitignored. Configuration files (SOUL.md, AGENTS.md, etc.) and skills are tracked.

## Quick Reference

```
# Validate all workspaces
"check workspace consistency"

# Create a new sub-agent
"create a workspace for the translation agent"

# Update a specific file
"update the autoresearch agent's SOUL.md to be more concise"

# Sync config
"sync openclaw.json with workspace directories"
```

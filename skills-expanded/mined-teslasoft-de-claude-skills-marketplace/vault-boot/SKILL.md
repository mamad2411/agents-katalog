---
name: vault-boot
description: |
  Load vault context for role sessions (developer, architect, researcher, etc.).
  Replaces 10+ sequential tool calls with 2 parallel batches. Use at session start
  or after context recovery. Not for Nikola (/dashboard) or Cowork (/cowork).
  Includes agent team preparation for orchestration-first workflows and context
  packet detection for self-contained session handoff.
triggers:
  - vault boot
  - vault context
  - load vault
  - session start
  - was steht an
negative_triggers:
  - dashboard
  - cowork
  - nikola
version: 3.7.0
author: Christian Kusmanow / Claude
last_updated: 2026-06-17
review_status: reviewed
reviewed_at: "2026-02-17T11:30:00.000Z"
---

# Vault Boot — Generic Session Loader

Loads vault context for role sessions (developer, architect, researcher, e2e-tester,
doc-specialist, housekeeper). Replaces 10+ sequential tool calls with 2 parallel batches.
Supports context packet-driven sessions for orchestration-first workflows.

## When to Use

- **Role session start**: After `/role <name>` when vault context is needed
- **Context recovery**: After context window rotation or long pause
- **Orientation**: When user asks "was steht an?" outside Nikola/Cowork
- **Worktree session start**: After opening a session in a worktree — detects context packet automatically

## When NOT to Use

- **Nikola sessions**: Use `/dashboard` (Jarvis-powered, 7 modes including Orchestrate)
- **Cowork sessions**: Use `/cowork` (delegation-focused, .memory-based)
- Mid-session when context is already loaded
- For Jarvis-specific commands (use `/jarvis` skill)

## Complementary Tools

| Tool | Actor | Use |
|------|-------|-----|
| `/vault` (this) | Role sessions | Generic vault context loader |
| `/dashboard` | Nikola (Claude Code) | Interactive command center, orchestration |
| `/cowork` | Cowork (Claude Desktop) | Delegation-focused briefing, decisions |
| `00_Dashboard/dashboard.html` | Human (browser) | Visual Kanban, zero AI cost |

## Procedure

### Step 0 — Context Packet Detection

Before loading generic vault context, check if this session has a context packet:

1. Check working directory — if inside `.worktrees/{name}/`, this is a worktree session
2. If in a worktree, look for a matching context packet:
   - Extract work-item-id from worktree name (e.g., `.worktrees/s86-p1-catalog/` → `s86-p1`)
   - Check `coordination/context-packets/{id}.md` (case-insensitive match)
   - Also check `coordination/context-packets/` for any packet with `worktree_path` matching current worktree
3. If a context packet is found:
   - **Read the packet** — it contains everything needed: identity, objective, tasks, policies, relevant files
   - **Skip Steps 1-4** — the packet replaces generic vault loading
   - **Jump to Step 5a (Context Packet Briefing)** instead of the generic briefing

**If no context packet found:** Continue with Steps 1-4 (generic vault boot).

### Step 1 — Parallel Core Load

Fire ALL of these in one parallel batch (Obsidian MCP or direct reads):

| # | File | Purpose |
|---|------|---------|
| 1 | `TASKS.md` | Active/waiting/someday tasks |
| 2 | `PROJECT_STATE.md` | Goal status, active projects, KRs, constraints |
| 3 | `AGENTS.md` | Vault conventions, PARA structure, edit rules |
| 4 | `coordination/harness-control.md` | Thread control, active threads |
| 5 | `coordination/improvement-queue.md` | Pending improvements |
| 6 | `coordination/policies/policies.index.yaml` | Active policy catalog |

6 parallel calls in a single message — replaces 6 sequential round-trips.

### Step 2 — Parallel Extended Load

After Step 1, fire these in parallel:

| # | Call | Purpose |
|---|------|---------|
| 7 | List `coordination/threads/` | Active thread specs |
| 8 | List `coordination/agent-state/` | Agent state files |
| 9 | List `00_Inbox/` | Inbox item count |
| 10 | List `coordination/context-packets/` | Active context packets (for team awareness) |

### Step 3 — Service Check (optional)

If drone is likely running (Claude Code session), check health:

```bash
pnpm health
```

Skip in environments where drone is unavailable (Cowork, standalone).

### Step 4 — Agent Team Preparation

After loading vault context, prepare for orchestration-first workflows:

**4a. Check for active worktrees:**

```bash
ls -d .worktrees/*/ 2>/dev/null
```

If worktrees exist, gather their status:

| Worktree | Branch | Status | Relevance |
|----------|--------|--------|-----------|
| [name] | [branch] | [clean/dirty] | [related to current role?] |

**4b. Check for pending context packets:**

Scan `coordination/context-packets/*.md` frontmatter for `status: pending` or `status: active`.
List packets relevant to the current role (matching `role:` field in packet frontmatter).

**4c. Check for team specs:**

Read `coordination/dashboard-sessions.json` for active team compositions.
If a team is active and this role is part of it, note the team context.

**4d. Render team awareness section:**

```markdown
### Agent Team Status
- **Active worktrees:** [N] ([names])
- **My context packets:** [list of packets assigned to this role]
- **Team:** [team-name or "none"]
- **Dispatch queue:** [N] pending items
```

This section gives every role session awareness of the broader orchestration context
without requiring Nikola-level orchestration access.

### Step 5 — Render Status Briefing

```markdown
## Vault Status — {date}

**Goal Q1 2026:** {goal_description}
| KR | Status | Project |
|----|--------|---------|
| {kr} | {status} | {project_link} |

**Active Tasks:** {bullet list from TASKS.md}
**Blocked:** {list with reasons}
**Inbox:** {N} items
**Threads:** {N} active
**Context Packets:** {N} active, {N} pending
**Services:** {drone: up/down, rc_watcher: up/down, plugin: up/down}
```

### Step 5a — Context Packet Briefing (alternative to Step 5)

When a context packet is detected in Step 0, render this instead of the generic briefing:

```markdown
## Context Packet Session — {work_item_id}

**Role:** {role} | **Autonomy:** {autonomy_level} | **Model:** {model}
**Worktree:** {worktree_path} | **Branch:** {branch}
**Objective:** {objective from packet}
**Expires:** {expires timestamp}

### Task Progress
| # | Task | Status | Commit |
|---|------|--------|--------|
| {N} | {task} | {status} | {commit or "-"} |

### Relevant Files
{list from packet}

### Policies
{list from packet}

### How to Start
1. Verify worktree: `git status`
2. Begin next pending task
3. After each task: commit + update this packet's task table
```

**Key difference:** This briefing is self-contained — no vault-wide context loading needed.
The executor can start working immediately from the packet alone.

### Step 6 — Session Handoff Support

When a session completes work (all tasks done or session ending), produce a self-contained
context packet update for handoff:

**6a. On task completion within a context packet session:**

Update the packet's task table via direct file edit:
- Set task `status: done`
- Set task `commit: {hash}` with the commit that completed the task
- If all tasks done: set packet frontmatter `status: done`

**6b. On session end (any session with uncommitted progress):**

Generate a handoff summary for the next session:

```markdown
### Session Handoff — {date} {time}
**Session:** {session_id or "ad-hoc"}
**Role:** {role}
**Branch:** {branch}
**Commits this session:** {list of commit hashes + messages}
**Work completed:** {summary of what was done}
**Work remaining:** {summary of what's left}
**Blockers:** {any blockers encountered}
**Files modified:** {list of files changed}
```

This handoff is written to:
- The context packet (if one exists) — appended to `## Session Log` section
- The agent-state file — updated with current_task and next_tasks

### Step 7 — Ready Prompt

End in user's language (German for Christian):

> Kontext geladen. Womit moechtest du weitermachen?

Surface P0/P1 alerts prominently before the ready prompt if they exist.

**For context packet sessions**, use a targeted ready prompt:

> Kontext-Paket geladen ({work_item_id}). Naechste Aufgabe: {next_pending_task}

## MCP Integration

The vault-boot skill supports **three data sources** with automatic fallback:

1. **Obsidian MCP** (preferred for live vault): Uses `obsidian_get_file_contents` when Obsidian is running — provides live view of current vault state
2. **Vault MCP** (preferred for automation): Uses `vault_read`, `vault_list` via vault-mcp server with dual-transport support:
   - **HTTP** (port 3838): Available in Claude Code sessions; requires `pnpm mcp:bg` to start the server
   - **Stdio** (WSL bun): Available in Claude Desktop sessions via `coordination/vault-mcp/src/stdio.ts`; automatically configured in `claude_desktop_config.json`
3. **Direct filesystem** (fallback): Standard Read/Glob tools with absolute paths

**Note for Cowork sessions:** Claude Desktop uses stdio transport — no HTTP server startup needed. The stdio connection is independent and automatically configured.

**Server health verification:** Use `server_health` MCP tool to verify vault-mcp server availability before attempting vault operations. This is particularly useful in Cowork sessions running in Claude Desktop (Hyper-V VM) where filesystem access is unavailable.

## Fallback Strategy

1. **Try context packet first**: If in a worktree, check for matching packet (Step 0)
2. **Try Obsidian MCP**: `obsidian_get_file_contents` calls (requires Obsidian running)
3. **Try Vault MCP**: `vault_read` calls via vault-mcp server (port 3838, filesystem-based, no Obsidian needed)
4. **Fall back to direct reads**: Read from vault root with 10s timeout
5. **Partial boot**: Render what loaded, note missing sections
6. **Never block**: Partial briefing > no briefing

## Performance Target

2 tool-call turns (parallel batches) + 1 rendering turn. Target: < 15 seconds.
Context packet sessions: 1 tool-call turn + 1 rendering turn. Target: < 5 seconds.

## Vault Structure Reference

- **PARA**: 00_Inbox, 10_Goals, 20_Projects, 30_Areas, 40_Resources, 50_Collab, 60_Science, 70_Skills, 90_Archive
- **Language**: Goal/project names German, technical content English
- **Scripts**: Use `pnpm <script>` commands (VOP-001), see package.json
- **Services**: drone (3737), vault-mcp (3838), rc_watcher (27141), plugin (esbuild watch)
- **Context Packets**: `coordination/context-packets/{id}.md` — self-contained work item context
- **Worktrees**: `.worktrees/{name}/` — isolated execution environments

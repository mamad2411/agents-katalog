---
name: orc-session
description: "Use when starting an agent session on an ORC-backed project, resuming after compaction, recording significant actions, or ending a work unit. Foundational ORC workflow: call context() first, record events, snapshot before compaction, restore after."
allowed-tools: mcp__orc__skill_read mcp__orc__audit_list mcp__orc__memory_list mcp__orc__memory_read mcp__orc__memory_create mcp__orc__memory_update mcp__orc__memory_history mcp__orc__kb_search mcp__orc__kb_read mcp__orc__kb_comment mcp__orc__context mcp__orc__session_event mcp__orc__session_snapshot mcp__orc__session_restore mcp__orc__session_log mcp__orc__tool_search mcp__orc__tool_describe mcp__orc__tool_invoke
---

# ORC Session Workflow

ORC is a local-first orchestration hub - a shared SQLite brain that all agents read/write. Sessions ensure continuity across context compactions and agent restarts.

## Why

Context windows are finite. When compaction happens, everything you learned vanishes unless recorded. ORC sessions capture events as they happen and compress them into a restorable snapshot.

---

## Workflow

### 1. Start - Always call `context()` first

Returns a compact overview: active tasks, the project's top memories by priority (`name [pN] - description`), last session summary. Read relevant memories with `memory_read`. Pass `project` to scope (e.g. `"orc"`), or omit for the default.

- **Empty response**: No saved context. Inspect current project instructions and the assigned task; do not invent rules or duplicate existing tasks.
- **Resuming after compaction**: Use your supplied session ID to call `session_restore`, then refresh the task, feedback and relevant memory and KB context.

### 2. Discover available workflows

Use `skill_list` to see available skills. Use `skill_read` to load specific skill content when you need a structured workflow (e.g. for code review, planning, or bug fixes).

Memory changes record the agent's native session when the MCP server can see it (stdio MCP and the CLI read `ORC_SESSION_ID` or `CLAUDE_CODE_SESSION_ID`; HTTP MCP cannot). Note the names of memories you create or update for the end-of-session review. See `orc-memory` for what belongs in a memory.

### 3. Record events as you work

Call `session_event` after anything worth surviving compaction. Events are deduplicated automatically.

**What to record:**

- File edits (type: `file`) - after Write/Edit
- Task transitions (type: `task`) - when status changes
- Conventions (type: `rule`) - when you establish "always do X"
- Architectural choices (type: `decision`) - when choosing between options
- Git operations (type: `git`) - commits, pushes, branches
- Failures (type: `error`) - tool errors, failed commands

Rules and decisions get highest priority in snapshots and future `context()` calls.

### 4. Snapshot before compaction

`session_snapshot` builds a priority-tiered XML blob (<=2KB). Claude Code's `PreCompact` hook calls this automatically. Cursor/Gemini agents should call it manually when context is near limit.

### 5. Log completed work

At the end of a task or work block, load `orc-memory-review` with `skill_read` and follow its review steps inline before calling `session_log` with a summary. Use ordinary `search` / `kb_search` for lessons as needed; normal `skill_read` returns edited instructions in the selected project. It auto-derives touched files and task changes from your session events, and lists memories changed in this session.

---

## Agent Setup

**Claude Code** - hooks handle events, snapshots, and restore automatically. See `hooks/` directory and `hooks/claude-code/settings.json` for the hook configuration.

**Other clients** - hook support varies. Use explicit session tools when lifecycle events are not automatically recorded. Use the session ID supplied by ORC; native sessions need a unique ID per work unit.

**Agent Loop Workers** - sessions are managed automatically by the task loop. Workers call `context()` at start and the loop handles lifecycle.

### MCP connection modes

The ORC MCP server (`<orc-host>/mcp` over HTTP, or `orc mcp` over stdio) has two modes:

- **Full** (default; `/mcp` or `orc mcp`) - every ORC tool is listed and called by name, e.g. `memory_list`.
- **Meta** (`/mcp?mode=meta` or `orc mcp --mode meta`) - lists only three tools, which keeps a large
  tool list out of your context:
  - `tool_search({ query })` - find tools by intent ("create task", "search the kb"). Omit the
    query to get every tool grouped by toolset; use that when you do not know what exists.
  - `tool_describe({ name })` - full description and JSON input schema of one tool.
  - `tool_invoke({ name, arguments })` - run it. Arguments are validated like a direct call.

In meta mode, every tool named in ORC skills (`context`, `memory_list`, `kb_search`, ...) is reached
through `tool_invoke`: describe it once if you are unsure of its arguments, then invoke it. An
unknown name returns `Unknown tool`; search instead of guessing.

The server decides which tools exist; ORC agent runtimes pre-approve every tool on the `orc` server
(permission rule `mcp__orc`). To give an agent or package a narrower ORC surface, point its MCP
config (`mcp.json`) at a different URL rather than adding per-tool allow lists.

---

## CLI Fallbacks

For operations not in MCP (delete, advanced queries):

```bash
orc session list              # List sessions
orc session show <id>         # Show session details
orc flow status <id>          # Inspect a managed task; the flow owns status
orc project add <name>        # Create a project
orc project update <name>     # Update project details
orc job add <name> --command "..." # Create a job
```

---

## Common Mistakes

| Mistake                        | Fix                                                        |
| ------------------------------ | ---------------------------------------------------------- |
| Skipping `context()` at start  | Always call it first - you'll duplicate work or miss rules |
| Using `context()` as a search  | Use `memory_list({ q })` for targeted lookups              |
| Not recording decisions        | Decisions lost on compaction = re-making the same choices  |
| One giant `session_log` at end | Log per work unit so partial progress is preserved         |

---

## Related

- **orc-tasks** skill - task lifecycle, HITL review, agent loop patterns
- **orc-memory** skill - what belongs in a memory and how to write one
- Built-in skills: use `skill_list` to discover available workflows, `skill_read` to load them

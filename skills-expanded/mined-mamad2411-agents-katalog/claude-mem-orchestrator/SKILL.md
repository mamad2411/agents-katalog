---
name: claude-mem-orchestrator
description: "Orchestrates claude-mem persistent memory for maximum session context. Use at conversation start to load relevant past work, when the user says 'what did we do last time', 'load context', 'recall', 'remember', 'search memory', 'what do you know about this project', or when starting work on a project that has prior sessions. Also use when the user wants to save important decisions, search past sessions, or generate project history reports."
---

# Claude-Mem Orchestrator

claude-mem v12 — persistent cross-session memory via MCP tools on port 37777.

**Plugin location:** `~/.claude/plugins/cache/thedotmack/claude-mem/12.0.1/`

## Core Principle

Memory is automatic — hooks capture everything. The orchestrator's job is **retrieval and routing**: load the right context at the right time, and route memory queries to the right tool. Keep token usage lean by always filtering before fetching.

---

## Step 0: Orient — Check Memory Health

Before anything, verify claude-mem is running:

1. Check if `<claude-mem-context>` blocks appeared in this session (auto-injected on session start)
2. If not, check worker health:

```bash
curl -s http://localhost:37777/health
```

If the worker is down:
```bash
# Start it (uses bun runtime)
node "$HOME/.claude/plugins/cache/thedotmack/claude-mem/12.0.1/scripts/bun-runner.js" \
     "$HOME/.claude/plugins/cache/thedotmack/claude-mem/12.0.1/scripts/worker-service.cjs" start
```

If port 37777 is stuck (stale socket from crashed process):
- Wait 1-2 minutes for OS to release, then retry
- Or restart the terminal / VS Code window

Once healthy, show:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MEM  |  Worker: [healthy / down]
     |  Project: [detected project name]
     |  Context: [auto-injected / manual load needed]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 1: Assess Intent & Route

| User signal | Action |
|-------------|--------|
| Starting a new session on a known project | **Auto-context** — search + fetch recent work (Route A) |
| "What did we do last time?" / "recall" | **Memory search** — targeted query (Route B) |
| "Save this decision" / "remember that..." | **Save memory** — store important context (Route C) |
| "What's the project history?" | **Timeline report** — use `/timeline-report` skill |
| "Search code structurally" | **Smart explore** — use `/smart-explore` skill |
| "Create a plan with memory context" | Route to `/make-plan` skill |
| "Execute a plan" | Route to `/do` skill |

---

## Route A: Auto-Context Load (Session Start)

Use this when starting work on a project with prior sessions. Goal: get the user productive in under 30 seconds with full context.

### Step 1: Search recent project work

```
search(query="recent work", limit=20, project="<project-name>", type="observations", orderBy="date_desc")
```

Also search for the specific area of work if known:
```
search(query="<topic from user's first message>", limit=10, project="<project-name>")
```

### Step 2: Get timeline context around the most recent session

```
timeline(query="latest session", depth_before=5, depth_after=0, project="<project-name>")
```

### Step 3: Fetch full details for the most relevant items

Review titles from search results. Pick the 3-5 most relevant IDs. Discard the rest.

```
get_observations(ids=[<selected IDs>], orderBy="date_desc")
```

### Step 4: Summarize to the user

Present a brief status:
- What was last worked on and when
- Key decisions made
- Any open items or blockers from last session
- Suggested next steps

---

## Route B: Memory Search (Targeted Query)

When the user asks about specific past work.

**Always follow the 3-layer pattern — never fetch without filtering first:**

1. **Search** — get compact index (~50-100 tokens/result)
   ```
   search(query="<user's question>", limit=20, project="<project>")
   ```

2. **Timeline** — get chronological context around interesting results
   ```
   timeline(anchor=<best_match_id>, depth_before=3, depth_after=3)
   ```

3. **Fetch** — get full details only for filtered IDs (~500-1000 tokens each)
   ```
   get_observations(ids=[<selected>])
   ```

**Present results as a narrative**, not raw data. Connect the dots between observations to tell the user what happened and why.

---

## Route C: Save Important Context

When the user explicitly wants to preserve a decision, insight, or context for future sessions.

```
save_memory(
  text="<structured summary of what to remember>",
  title="<concise title>",
  project="<project-name>"
)
```

**What's worth saving manually** (hooks capture most things automatically):
- Architectural decisions and their rationale
- "We tried X and it failed because Y" — failure context
- User preferences discovered during conversation
- External knowledge not in the codebase (e.g., "the API changed in v3")

**What NOT to save** (hooks already capture these):
- Tool usage and file reads (PostToolUse hook)
- Session summaries (Stop hook)
- Code changes (captured via git + observation hooks)

---

## Troubleshooting

### Worker won't start
```bash
# Check logs
cat ~/.claude-mem/logs/claude-mem-$(date +%Y-%m-%d).log | tail -20

# Check if port is in use
netstat -ano | grep 37777    # Windows
lsof -i :37777               # macOS/Linux
```

### MCP tools not available
- In VS Code: run `Developer: Reload Window` (Ctrl+Shift+P)
- Check plugin is enabled: `~/.claude/settings.json` should have `"claude-mem@thedotmack": true`
- Verify MCP server config exists: `~/.claude/plugins/cache/thedotmack/claude-mem/12.0.1/.mcp.json`

### No context auto-injected
- Worker must be running BEFORE session starts
- Check `~/.claude-mem/claude-mem.db` exists and has data
- Start worker manually, then open a new conversation

### VS Code extension vs CLI
claude-mem works identically in both — same hooks, same MCP server, same worker on port 37777. If MCP tools appear in CLI but not in VS Code extension panel, this is a known VS Code extension issue — use `Developer: Reload Window` or run `claude` from the integrated terminal as fallback.

---

## Anti-patterns to Flag

- **Fetching all observations without filtering** — always search first, then fetch by ID. 10x token savings.
- **Ignoring auto-injected context** — check for `<claude-mem-context>` blocks before doing manual searches.
- **Saving redundant memories** — hooks capture tool usage and sessions automatically. Only manually save decisions and insights.
- **Searching without project filter** — always pass `project` parameter to avoid cross-project noise.

---

## Focus Recovery

If the conversation drifts from memory-related tasks:
> "Memory context is loaded. Ready to work — what's the task?"

The orchestrator's job is to get context loaded fast, then get out of the way.

---
name: onboard
description: First-time Loom setup for a new repository. Runs loom analyze, installs MCP config, and shows what was indexed.
argument-hint: "[repo-path]"
allowed-tools:
  - mcp__loom__graph_stats
  - mcp__loom__god_nodes
  - mcp__loom__suggest_questions
  - mcp__loom__get_savings
  - Bash
  - Read
  - Glob
---

# Onboard — First-Time Loom Setup

Set up Loom for a repository and orient to the codebase.

## Steps

### 1. Check if already indexed

Call `graph_stats()` — if total node count > 0, Loom is already indexed. Jump to Step 4.

### 2. Index the repository

```bash
loom analyze .
```

This runs tree-sitter over all Python/TypeScript/JavaScript/Java files and builds `~/.loom/projects/{repo-name}.db` (or `~/.loom/loom.db` if not in a git repo). Typically 5–30 seconds for a 500-file repo.

If the user provides a path argument, use that instead of `.`.

### 3. Install MCP config (first time only)

```bash
loom install
```

This writes the MCP server config to the appropriate tool config file (Claude Code, Cursor, Windsurf, or Codex), and installs a post-commit git hook for incremental sync.

### 4. Check what was indexed

Call `graph_stats()` — shows node and edge counts by kind.

### 5. Find entry points

Call `god_nodes(limit=10)` — shows the most-called functions. These are the best starting points for understanding the codebase.

### 6. Surface investigation priorities

Call `suggest_questions(limit=7)` — surfaces dead code, undocumented hot functions, bridge nodes, and low-cohesion clusters worth looking at.

### 7. Report to user

Show:
- Node count by kind (functions, classes, files, methods)
- Top 5 most-called functions (entry points)
- Top 3 suggested questions to investigate
- Confirm MCP server is registered (loom in mcpServers)

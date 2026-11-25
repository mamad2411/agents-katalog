---
name: connect
description: "Set up MCP server — create/update .mcp.json and verify connection"
category: setup
tags: [mcp, server, endpoint, config]
depends-on: []
input: "MCP endpoint URL or default"
output: ".mcp.json configuration + connection verification"
token-estimate: 2000
parallel-safe: false
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-sonnet-4-6
context: fork
agent: general-purpose
---

# Connect

Set up the CCS MCP server connection for the current project.

## Steps

### 1. Detect existing config
Check if `.mcp.json` exists in project root. If `ccs` entry already exists and is valid → skip to step 4 (verify).

### 2. Create or merge .mcp.json
**If no `.mcp.json`:** Create with CCS entry:
```json
{ "mcpServers": { "ccs": { "type": "http", "url": "https://skills.thinqmesh.com/api/mcp" } } }
```

**If `.mcp.json` exists but no `ccs` entry:** Read, parse, add `ccs` to existing `mcpServers`, write back.

**NEVER overwrite or remove existing MCP server entries.**

### 3. Ask connection preference
- **Remote (default):** `https://skills.thinqmesh.com/api/mcp`
- **Local:** Update config to `{ "command": "npx", "args": ["-y", "@jason.today/webmcp@latest", "--mcp"] }`

### 4. Verify connection
For HTTP: `curl -s https://skills.thinqmesh.com/api/mcp` — check response includes server name and tools. If fails → suggest troubleshooting.

### 5. Check .gitignore
- `.mcp.json` should NOT be in `.gitignore` (commit for team)
- `.claude/settings.local.json` SHOULD be in `.gitignore`

### 6. Report
Output: server name, transport type, endpoint, status, tools available, other servers preserved. Suggest → `/ccs-init` to index codebase.

### 7. Log to `.ccs/task.md`
If `.ccs/task.md` exists, append entry using template at `.claude/skills/_ccs/templates/task-template.md`.

## Rules
- Never overwrite existing MCP server entries — only add/update `ccs`
- This is project-level config (`.mcp.json`), not global (`~/.claude/settings.json`)
- After connect → suggest `/ccs-init`

## Refs
- MCP config: `.mcp.json`
- Task template: `.claude/skills/_ccs/templates/task-template.md`
- Strategy: `.claude/skills/_ccs/references/context-strategies.md`

---
*codebase-context-skill v2.0.0*

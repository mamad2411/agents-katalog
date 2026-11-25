---
name: init
description: "Index the codebase using the CCS engine — builds dependency graph, symbol index, and project summary in milliseconds"
category: context
tags: [index, scan, setup, architecture]
depends-on: []
input: "codebase root directory"
output: ".ccs/index.json — full codebase index with symbols, graph, conventions"
token-estimate: 500
parallel-safe: false
argument-hint: "[--rebuild]"
user-invocable: true
allowed-tools: Read, Bash, AskUserQuestion
model: claude-sonnet-4-6
context: inline
agent: general-purpose
---

# Init — Engine-Powered Indexing

Index the codebase using the CCS TypeScript engine. Zero AI exploration — the engine does all the work programmatically.

## Engine Output (injected automatically)

!`ccs index 2>&1 || node "$HOME/.claude/skills/_ccs/engine/cli.js" index 2>&1 || npx codebase-context-skill index 2>&1 || echo "CCS engine not found. Run: npm install -g codebase-context-skill"`

## After Indexing

!`ccs summary 2>/dev/null || node "$HOME/.claude/skills/_ccs/engine/cli.js" summary 2>/dev/null`

## What to Tell the User

Report the engine output above. The index is now at `.ccs/index.json`. Explain:
- **Files indexed**, total lines, directories, tech stack
- **Key files** (S/A rank) — these are the most-imported, most-central files
- **Architecture** detected and conventions found
- **Next steps**: Just start working. The engine automatically:
  - Injects relevant context on every query (UserPromptSubmit hook)
  - Updates the index when files change (PostToolUse hook)
  - Provides project summary at session start (SessionStart hook)

Available commands:
- `ccs search <query>` — search files and symbols (instant, zero tokens)
- `ccs context <query>` — build precise context blob
- `ccs graph <file>` — show dependency graph for a file
- `ccs stats` — index statistics
- `ccs watch` — auto-update index on file changes

---
*codebase-context-skill v2.0.0*

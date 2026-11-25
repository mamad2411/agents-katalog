---
name: SDLC Plugin Setup
description: >
  One-command setup for AI-SDLC IDE Plugin. Installs dependencies, creates env,
  bootstraps .sdlc/, wires Claude Code commands, Cursor MCP, and validates everything.
tags: [setup, install, configure, onboarding]
triggerPhrases:
  - "set up"
  - "setup"
  - "install"
  - "configure"
  - "onboard"
  - "get started"
  - "initialize"
  - "init"
  - "bootstrap"
  - "first time"
  - "how to start"
---

# /project:setup

**One-command SDLC Plugin Setup**

Works in: Claude Code, Cursor IDE, CLI terminal

## When to Trigger

User says anything like:
- "set up the SDLC plugin"
- "install the plugin"
- "configure SDLC"
- "how do I get started"
- "initialize the project"
- "first time setup"
- "bootstrap everything"

## What To Do

### Step 1: Check if already set up

```
Check if these exist:
  - plugins/ide-plugin/node_modules/@modelcontextprotocol/sdk/ → deps installed?
  - plugins/ide-plugin/env/.env → env configured?
  - .sdlc/memory/ → project structure bootstrapped?
  - .claude/commands/project.md → commands wired?

If ALL exist → tell user "Already set up! Try /project:prd-review AB#123"
If SOME missing → run setup for missing parts only
If NONE exist → full setup
```

### Step 2: Run setup

Execute this command in the terminal:
```bash
cd plugins/ide-plugin && npm install --production && node scripts/setup.js
```

### Step 3: Check ADO_PAT

After setup, check `plugins/ide-plugin/env/.env`:
- If ADO_PAT is empty → ask user to provide it
- If ADO_PAT is set → test connection

### Step 4: Confirm working

Show user:
```
✅ Setup complete!

What's ready:
  • 16 slash commands (/project:prd-review, /project:grooming, etc.)
  • 5 MCP tools (list-work-items, get-work-item, create-work-item, update-work-item, post-comment)
  • NL routing (just describe what you need in plain English)
  • Memory system (.sdlc/memory/)

Try it:
  • /project:prd-review AB#12345
  • "Review the PRD for AB#12345 from backend perspective"
  • "Create a master story for multi-language signup"
```

### Step 5: If ADO_PAT needed

Ask user interactively:
```
To connect to Azure DevOps, I need your Personal Access Token.

Get it: Azure DevOps → User Settings → Personal Access Tokens → New Token
Scopes: Work Items (Read & Write), Code (Read)

Paste your token (I'll save it to env/.env):
```

Then write it to `plugins/ide-plugin/env/.env` as `ADO_PAT=<token>`.

## CLI Mode

```bash
# From repo root
cd plugins/ide-plugin && npm run setup

# Or directly
./plugins/ide-plugin/setup.sh
```

## Verification

After setup, validate:
1. `node --check plugins/ide-plugin/mcp/ado-server.js` → syntax OK
2. Send MCP initialize handshake → get response
3. `ls .claude/commands/project*.md` → 16+ files
4. `cat .cursor/mcp.json` → has ado-plugin entry
5. `ls .sdlc/memory/` → directory exists

## Model & Token Budget
- **Model Tier:** Haiku (simple file operations)
- Input: ~200 tokens
- Output: ~500 tokens

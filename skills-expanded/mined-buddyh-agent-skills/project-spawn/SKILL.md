---
name: project-spawn
description: Spawn a new Claude Code or Codex session in a project directory with context handoff. This skill should be used when discussion shifts to a different project/repo and the user wants to work on it in a dedicated session. Creates a handoff document with relevant context from the current conversation, then launches a new tmux session ready to continue.
---

# Project Spawn

## Overview

Transfer context from the current conversation to a new session in a different project directory. This enables seamless context handoff when pivoting from a general session to focused project work.

## Platform Support

- **Claude Code**: `claude` CLI
- **Codex**: `codex` CLI

The handoff workflow is identical on both platforms.

## Workflow

### Step 1: Resolve Target Project

Determine the target project directory:

1. **If explicit path/name provided**: Use directly
2. **If project name provided**: Search for matching directories in common locations (`~/repos/`, `~/projects/`, etc.)
3. **If no target specified**: Detect from recent conversation context or ask the user

### Step 1b: Handle Non-Existent Directory

If target directory doesn't exist, ask user:

> "Directory `<path>` doesn't exist. Want me to create it?"
> - Create folder only
> - Create folder + init git repo
> - Create folder + init git + create GitHub repo (public)
> - Create folder + init git + create GitHub repo (private)
> - Cancel

Create as requested before proceeding to Step 2.

### Step 2: Extract Relevant Context

Analyze the last 5-10 messages for content relevant to the target project:

- Tasks or work items discussed
- Specific files, scripts, or features mentioned
- Decisions made or questions raised
- Any errors or issues identified
- Uncommitted changes noted

Focus only on information relevant to the target project, not the entire conversation.

### Step 3: Create Handoff Document

Write `PROJECT_HANDOFF.md` to the target project directory:

```markdown
# Project Handoff - [DATE] [TIME]

## Context
[Why this handoff is happening - what triggered the pivot]

## Discussion Summary
[Relevant context extracted from conversation]

## Specific Tasks/Questions
- [Actionable items identified]

## Files/Areas Mentioned
- [Specific files or code areas referenced]

## Suggested Starting Point
[What to do first in this session]
```

### Step 4: Launch Session

```bash
~/.claude/skills/project-spawn/scripts/spawn_session.sh "<project-path>" "<session-name>" [--agent claude|codex]
```

**Options:**
| Flag | Description |
|------|-------------|
| `--agent claude\|codex` | Which AI agent to launch (default: auto-detect from environment) |

The script will:
1. Create a new tmux session named after the project
2. Change to the project directory
3. Start the AI agent with initial prompt to read the handoff

**Platform-specific launch commands:**
- **Claude Code**: `claude`
- **Codex**: `codex`

### Step 5: Confirm to User

Report:
```
Spawned: <session-name>
Directory: <project-path>
Handoff: PROJECT_HANDOFF.md created

To attach: tmux attach -t <session-name>
```

## Quick Reference

**Invocation**: `/spawn <project-name-or-path>` or `/spawn` (auto-detect)

**Session naming**: Uses repo folder name (e.g., `my-project`)

**Handoff location**: `<project-dir>/PROJECT_HANDOFF.md`

**Examples:**
```bash
# Spawn with auto-detected agent
/spawn my-project

# Use Codex instead of Claude
/spawn my-project --agent codex
```

## Setup

```bash
chmod +x ~/.claude/skills/project-spawn/scripts/*.sh
```

## Resources

### scripts/
- `spawn_session.sh` - Creates tmux session and launches AI agent with handoff context

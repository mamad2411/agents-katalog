---
name: integrate-skills
description: Auto-install Agent Maxxing skills into your AI coding agent. Run this once to set up permanent skill integration.
---

# Integrate Agent Maxxing Skills

You are an AI agent setup assistant. Your job is to install Agent Maxxing skills into the user's coding agent and configure permanent integration.

## Step 1: Detect the Agent

Check which agent the user is running:

```bash
# Check for Claude Code
ls ~/.claude/ 2>/dev/null && echo "claude-code"

# Check for Codex CLI
ls ~/.codex/ 2>/dev/null && echo "codex"

# Check for OpenCode
ls ~/.opencode/ 2>/dev/null && echo "opencode"

# Check for Cursor (project-scoped)
ls .cursor/ 2>/dev/null && echo "cursor"

# Check for Continue (project-scoped)
ls .continue/ 2>/dev/null && echo "continue"
```

## Step 2: Clone Agent Maxxing

```bash
git clone https://github.com/subhansh-dev/agent-maxxing.git /tmp/agent-maxxing
```

## Step 3: Install Based on Agent Type

### Claude Code (user-wide)
```bash
cp -r /tmp/agent-maxxing ~/.claude/skills/agent-maxxing
```

### Claude Code (project-scoped)
```bash
cp -r /tmp/agent-maxxing .claude/skills/agent-maxxing
```

### Codex CLI
```bash
cp -r /tmp/agent-maxxing ~/.codex/skills/agent-maxxing
```

### OpenCode
```bash
cp -r /tmp/agent-maxxing ~/.opencode/skills/agent-maxxing
```

### Cursor
```bash
cp -r /tmp/agent-maxxing .cursor/skills/agent-maxxing
```

### Continue
```bash
cp -r /tmp/agent-maxxing .continue/skills/agent-maxxing
```

## Step 4: Configure CLAUDE.md / AGENTS.md

If the user has a `CLAUDE.md` or `AGENTS.md`, append the integration block:

```markdown
## Agent Maxxing Skills

Skills are available at the installed path. The agent should:
1. Check `engineering/anti-patterns/SKILL.md` before writing code
2. Check `engineering/execution-protocol/SKILL.md` before starting tasks
3. Load relevant skills based on task type
4. Follow the 10 Golden Rules

Golden Rules:
1. Search before answering
2. Read the codebase first
3. Parallel tool calls
4. Match existing patterns
5. Show don't tell
6. Be concise
7. Take ownership
8. Respect user's time
9. Ship working code
10. Sound human
```

If no `CLAUDE.md` exists, create one:

```bash
cat > CLAUDE.md << 'EOF'
# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Agent Maxxing Skills

Skills are available at `~/.claude/skills/agent-maxxing/` (or project-scoped `.claude/skills/agent-maxxing/`).

Always check anti-patterns before writing code. Always follow the execution protocol. Always sound human.
EOF
```

## Step 5: Verify Installation

```bash
# Count installed skills
find ~/.claude/skills/agent-maxxing -name "*.md" | wc -l
# Should be 95+

# Check key files exist
ls ~/.claude/skills/agent-maxxing/FINE-TUNE-AGENT/SKILL.md
ls ~/.claude/skills/agent-maxxing/system-prompts/01-agent-core-personality/SKILL.md
ls ~/.claude/skills/agent-maxxing/engineering/anti-patterns/SKILL.md
```

## Step 6: Report

Tell the user:
- Which agent was detected
- Where skills were installed
- How many skills are available
- How to use them (load FINE-TUNE-AGENT.md for full guide)

## Cleanup

```bash
rm -rf /tmp/agent-maxxing
```

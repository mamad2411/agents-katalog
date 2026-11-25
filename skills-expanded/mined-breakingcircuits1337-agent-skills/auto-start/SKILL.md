---
name: auto-start
description: Use at session start to automatically load memory and suggest relevant skills based on the task. Triggers: session start, new conversation, first message.
---

# Auto-Start

Automatically runs at session initialization to load memory and prepare relevant skills.

## When to Use

- At the very start of every session
- When a new conversation begins
- When the user provides their first message

## What It Does

### 1. Load Memory
```bash
python3 /home/bc/bin/memory.py
```

This loads all 7 memory files:
- CLAUDE.md (long-term)
- SOUL.md (values)
- USER.md (user context)
- TOOLS.md (available tools)
- AGENTS.md (instructions)
- MEDIUM_TERM.md (cross-session)
- SHORT_TERM.md (current session)

### 2. Analyze Task

After loading memory, analyze the user's request to identify relevant skills:

| Task Type | Suggested Skills |
|-----------|------------------|
| Creating code/features | test-driven-development, writing-skills |
| Debugging | systematic-debugging |
| Planning | brainstorming, writing-plans |
| Reviewing code | receiving-code-review, requesting-code-review |
| Multiple tasks | dispatching-parallel-agents |
| Finishing work | finishing-a-development-branch, verification-before-completion |

### 3. Apply Skills

Load and apply the most relevant skills before proceeding.

## Memory Reminder

The agent should ALWAYS remember:
- **ALWAYS run `python3 /home/bc/bin/memory.py` BEFORE making decisions**
- Check LONG-TERM, MEDIUM-TERM, and SHORT-TERM for context
- Use skills when 1% chance they apply
- NEVER delete skills - always create new ones

## Key Locations

| Item | Location |
|------|----------|
| Memory loader | `/home/bc/bin/memory.py` |
| Consolidated skills | `/home/bc/skills/all/` |
| Skills index | `/home/bc/skills/all/SKILLS_INDEX.md` |
| Homunculus | `/home/bc/.claude/homunculus/` |

## Quick Commands

```bash
# Load memory
python3 /home/bc/bin/memory.py

# List all skills
ls /home/bc/skills/all/

# Check SHORT_TERM for active tasks
cat /home/bc/SHORT_TERM.md
```

## Integration

This skill is designed to work with OpenCode's skill system. It should be invoked automatically at session start.

## Skills to Consider

Based on memory loaded:
- **update-report** - For documenting changes
- **brainstorming** - For creative work
- **test-driven-development** - For implementation
- **systematic-debugging** - For bug fixes
- **receiving-code-review** - For handling feedback
- **verification-before-completion** - Before finishing work

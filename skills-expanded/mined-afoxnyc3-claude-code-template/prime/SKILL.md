---
name: prime
description: Load project context - reads CLAUDE.md and hierarchical context
allowed-tools: Bash, Read, Glob
---

# Prime Command

Read and internalize project context files to understand the project.

## Instructions

Read these files in order:

1. **CLAUDE.md** - Project overview and hierarchical structure pointers
2. **README.md** - Project setup and quick start
3. **docs/ARCHITECTURE.md** - Detailed architecture decisions (if exists)

Claude Code also auto-loads:
- `.claude/rules/*.md` - Project-wide rules (code standards, self-review, parallel workflow)
- Component-specific `CLAUDE.md` files when working in those directories

## Context Discovery

The project uses hierarchical context:

```
CLAUDE.md                    # Universal context (~90 lines)
├── .claude/rules/           # Auto-loaded project rules
│   ├── 01-code-standards.md
│   ├── 02-self-review.md
│   └── 03-parallel-workflow.md
├── [component]/CLAUDE.md    # Component-specific context
└── knowledge/               # Domain expertise (referenced via @)
```

## Context Output

After reading, summarize:

```markdown
## Project Context Loaded

**Project**: {{PROJECT_NAME}} - [one-line description]

**Architecture**: [key components]

**Current Focus**: [based on recent activity from git log]

Ready to assist with [domain area].
```

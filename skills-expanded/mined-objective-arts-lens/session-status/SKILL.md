---
name: session-status
description: Show what Claude Code primitives are active in this session
---

# Session Status Check

When invoked, analyze and report the current session state.

## Instructions

1. **Identify the project** from the working directory
2. **List active primitives** by checking what's loaded
3. **Show auto-invoke rules** from CLAUDE.md
4. **Flag any issues** (missing skills, broken references)

## Output Format

```
┌─ Session Status ─────────────────────────────────────────┐
│ Project: [project name] ([project type])                 │
│ Profile: [if detected]                                   │
│                                                          │
│ SKILLS AVAILABLE                                         │
│   [icon] [skill name] ([token estimate]) - [source]      │
│   ...                                                    │
│                                                          │
│ AUTO-INVOKE RULES (from CLAUDE.md)                       │
│   [context] → [action]                                   │
│   ...                                                    │
│                                                          │
│ COMMANDS AVAILABLE                                       │
│   /[command] - [description]                             │
│   ...                                                    │
│                                                          │
│ MCP SERVERS                                              │
│   [server name] - [status]                               │
│   ...                                                    │
│                                                          │
│ ISSUES                                                   │
│   ⚠ [warning description]                               │
│   ...                                                    │
└──────────────────────────────────────────────────────────┘
```

## How to Gather Information

1. **Project detection**: Read current working directory, check for package.json, go.mod, etc.

2. **Skills**: Check both locations:
   - Global: `~/.claude/skills/`
   - Project: `./.claude/skills/`

3. **Auto-invoke rules**: Parse CLAUDE.md for tables with "Context" and "Action" columns

4. **Commands**: Check both locations:
   - Global: `~/.claude/commands/`
   - Project: `./.claude/commands/`

5. **Token estimates**: ~4 chars per token, read each skill file

6. **Issues to detect**:
   - Skill referenced in CLAUDE.md but not found
   - Broken symlinks
   - Duplicate skill names (project vs global)

## Example Output

```
┌─ Session Status ─────────────────────────────────────────┐
│ Project: d3-smr (D3 Visualization)                       │
│ Profile: d3-development                                  │
│                                                          │
│ SKILLS AVAILABLE                                         │
│   ⚡ d3 (1.2k) - project/.claude/skills                   │
│   ⚡ react-state (890) - project/.claude/skills           │
│   ⚡ typescript (1.1k) - project/.claude/skills           │
│   🔒 security-mindset (1.4k) - ~/.claude/skills         │
│   🔒 owasp (1.6k) - ~/.claude/skills                    │
│   📐 devlens (3.8k) - ~/.claude/skills                  │
│                                                          │
│ AUTO-INVOKE RULES                                        │
│   D3.js or visualization → /d3                           │
│   React/JSX/TSX files → /react-state                     │
│   Auth, login, passwords → /security-mindset             │
│   SQL, user input, APIs → /owasp                         │
│                                                          │
│ COMMANDS AVAILABLE                                       │
│   /session-status - This command                                 │
│   /viz/* - D3 visualization commands                     │
│                                                          │
│ MCP SERVERS                                              │
│   linear - enabled                                       │
│   sequential-thinking - enabled                          │
│                                                          │
│ ISSUES                                                   │
│   ✓ No issues detected                                  │
└──────────────────────────────────────────────────────────┘
```

## Icons

- ⚡ Canon/domain skill
- 🔒 Security skill
- 📐 Meta/methodology skill
- 🔧 Utility skill
- ⚠ Warning
- ✓ OK

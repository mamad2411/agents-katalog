---
name: easyskillz-register
description: Add a new AI tool to the project and wire all existing skills to it.
---
# easyskillz-register

Add a new AI tool to the project and wire all existing skills to it.

## When to Use This Skill

Use this skill when:
- User installs a new AI tool (e.g., adds Windsurf after using Claude)
- User wants to enable easyskillz for an additional tool
- User says "add Cursor support" or "enable skills for Codex"
- A new AI tool is detected but not registered in the config

## What This Skill Does

Runs `easyskillz register <tool>` which:
1. Adds the tool to `.easyskillz/easyskillz.json` config
2. Wires ALL existing skills to the new tool
3. Creates symlinks/stubs in the tool's skills directory
4. Updates the tool's instruction file with easyskillz info

## Instructions

**Step 1: Check supported tools**

Supported tools:
- `claude` - Claude Code
- `codex` - Codex
- `cursor` - Cursor
- `windsurf` - Windsurf
- `windsurf-workflows` - Windsurf Workflows
- `copilot` - GitHub Copilot
- `gemini` - Gemini CLI

**Step 2: Run register command**
```bash
easyskillz register <tool>
```

Example:
```bash
easyskillz register cursor
```

**Step 3: Verify**

Check that:
- Tool is added to `.easyskillz/easyskillz.json`
- Skills are wired to the tool's directory (e.g., `.cursor/skills/`)
- Tool's instruction file is updated (e.g., `AGENTS.md`)

## Expected Output

```
  ✓ Registered Cursor
  ✓ Wired skill "review-pr" → Cursor
  ✓ Wired skill "commit-msg" → Cursor
  ✓ Wired skill "debug-api" → Cursor
  ✓ Updated AGENTS.md

Cursor registered. 3 skill(s) wired.
```

## Example Workflow

```bash
# User: "I just installed Cursor, can you add it to easyskillz?"

# You run:
easyskillz register cursor

# Output:
#   ✓ Registered Cursor
#   ✓ Wired skill "review-pr" → Cursor
#   ✓ Wired skill "commit-msg" → Cursor
#   ✓ Updated AGENTS.md
#
# Cursor registered. 2 skill(s) wired.

# Now all existing skills are available in Cursor!
```

## What Gets Updated

**1. Config file** (`.easyskillz/easyskillz.json`)
```json
{
  "tools": ["claude", "cursor"],  // ← cursor added
  "linkStrategy": "symlink",
  "manageDocs": true,
  "docsStrategy": "unified",
  "gitignoreStrategy": "full"
}
```

**2. Tool's skills directory**
```
.cursor/skills/
  review-pr/     ← symlink to .easyskillz/skills/review-pr
  commit-msg/    ← symlink to .easyskillz/skills/commit-msg
```

**3. Tool's instruction file** (e.g., `AGENTS.md`)
```markdown
<!-- easyskillz-managed -->
## easyskillz — Skill Management
...
<!-- /easyskillz-managed -->
```

**4. .gitignore** (if gitignore strategy is set)
```gitignore
.cursor/          # ← added
.cursor/config.json  # ← added (if conflict-only strategy)
```

## Supported Tools

| Tool | Skills Dir | Instruction File |
|------|------------|------------------|
| Claude Code | `.claude/skills/` | `CLAUDE.md` |
| Codex | `.codex/skills/` | `AGENTS.md` |
| Cursor | `.cursor/skills/` | `AGENTS.md` |
| Windsurf | `.windsurf/skills/` | `AGENTS.md` |
| Windsurf Workflows | `.windsurf/workflows/` | `AGENTS.md` |
| GitHub Copilot | `.github/skills/` | `.github/copilot-instructions.md` |
| Gemini CLI | `.gemini/skills/` | `GEMINI.md` |

## Troubleshooting

**Tool already registered?**
- The command will tell you and skip registration
- Skills are still checked and wired if missing

**Unknown tool error?**
- Check the list of supported tools above
- Make sure you spelled the tool name correctly
- Tool names are lowercase: `cursor`, not `Cursor`

**Skills not showing up in the new tool?**
- Make sure the tool is actually installed
- Check that symlinks were created in the tool's directory
- Try running `easyskillz sync` to re-wire

## When NOT to Use This

**Don't use register for:**
- Initial setup → Use **easyskillz-setup** instead
- Creating skills → Use **easyskillz-add** instead
- Tools that aren't supported → Request support in GitHub issues

## Related Skills

- **easyskillz-setup** - Set up easyskillz after cloning
- **easyskillz-add** - Create a new skill
- **easyskillz-reference** - Full easyskillz documentation

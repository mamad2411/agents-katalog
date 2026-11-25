---
name: easyskillz-setup
description: Set up easyskillz after cloning a repository or on a new machine.
---
# easyskillz-setup

Set up easyskillz after cloning a repository or on a new machine.

## When to Use This Skill

Use this skill when:
- You just cloned a repository that uses easyskillz
- You're on a new machine and need to wire skills to your AI tools
- Skills aren't showing up in your AI tools
- You see a message like "Run `easyskillz sync` after cloning"
- You want to initialize easyskillz in a project

## What This Skill Does

Runs `easyskillz sync` which:
1. Detects which AI tools you have installed (Claude, Cursor, Codex, etc.)
2. Reads the project's easyskillz configuration
3. Creates symlinks from tool directories to `.easyskillz/skills/`
4. Wires all existing skills to your tools
5. Optionally manages instruction files (CLAUDE.md, AGENTS.md, etc.)
6. Optionally configures .gitignore

## Instructions

**Step 1: Run sync**
```bash
easyskillz sync
```

**Step 2: Answer prompts (first time only)**

If this is your first time running sync in this repo, you'll be asked:

1. **Instruction file management?** [Y/n]
   - `Y` = Centralize instruction files in `.easyskillz/docs/`
   - `n` = Leave instruction files as-is
   
2. **Strategy?** [1/2] (if you chose Y)
   - `1` = Unified (one INSTRUCTION.md for all tools)
   - `2` = Tool-specific (separate files per tool)

3. **Gitignore strategy?** [1/2/3]
   - `1` = Full (gitignore all tool files) ← **Recommended**
   - `2` = Conflict-only (gitignore config files only)
   - `3` = None (manual management)

**Step 3: Verify**

After sync completes, verify skills are wired:
- Check `.claude/skills/` (if using Claude)
- Check `.cursor/skills/` (if using Cursor)
- Skills should appear in your AI tool's skill list

## Expected Output

```
Scanning for AI tools...
  ✓ Claude Code      (.claude/skills)
  ✓ Cursor           (.cursor/skills)
  
Reading config (.easyskillz/easyskillz.json)...
  Registered: claude, cursor
  Strategy:   symlink

Testing symlink support...
  ✓ symlinks work

Plan:
  [ wire ]      .claude/skills/review-pr  →  .easyskillz/skills/review-pr
  [ wire ]      .cursor/skills/review-pr  →  .easyskillz/skills/review-pr

Proceed? [Y/n] Y

  ✓ Wired review-pr → Claude Code
  ✓ Wired review-pr → Cursor

Done. 2 tool(s) wired via symlink.
```

## Troubleshooting

**Skills not showing up?**
- Make sure you're in the project root directory
- Check that `.easyskillz/skills/` exists and has skill folders
- Try running `easyskillz sync` again

**Symlinks not working?**
- On Windows, you may need to run as administrator
- easyskillz will fall back to stub files automatically

**No tools detected?**
- Make sure you have at least one AI tool installed
- Check that the tool has created its config file (e.g., `.claude/settings.json`)

## Related Skills

- **easyskillz-add** - Create a new skill
- **easyskillz-register** - Add a new AI tool to the project
- **easyskillz-reference** - Full easyskillz documentation

---
name: skill-scoped-permission-suggestions
description: "Suggest the narrowest permission scope by mapping a file path to its enclosing skill directory before prompting the user."
metadata:
  author: ychampion
---

# SKILL: Skill-Scoped Permission Suggestions
**Domain:** safety-worktrees  
**Trigger:** Apply this when Claude is asking for filesystem permission that can be narrowed to a single skill directory.
**Source Pattern:** Distilled from reviewed repo-safety, packaging, and worktree-management patterns.

## Core Method
Leverage the skill path parser to detect when a target file resides inside `.claude/skills/<skill-name>` (project or global). Once matched, compute a gitignore-style prefix such as `/.claude/skills/<skill-name>/**` and offer that as the minimal scope for the permission prompt. This keeps the permission dialogue focused on the skill under edit and prevents giving blanket access to the entire `.claude` tree.

## Key Rules
- Normalize paths and compare lowercased versions so the detection works on both Windows and Unix filesystems.
- Reject skill names that contain `.` or traversal segments before suggesting scopes to avoid leaking overlapping directories.
- Always prefer `/.claude/skills/<name>/**` or `~/.claude/skills/<name>/**` over `/.claude/**` whenever the file sits inside a skill.
- When normalization finds no skill directory, fall back to the default wider scope instead of fabricating a useless pattern.

## Example Application
When editing `skills/my-skill/SKILL.md`, call this method before showing the permission prompt so you can recommend granting `/.claude/skills/my-skill/**` instead of the entire `.claude` directory.

## Anti-Patterns (What NOT to do)
- Do not re-prompt with the same wide scope if the normalized path already resolves to a skill — that defeats the purpose of scoped access.
- Don’t rely on raw casing or unnormalized separators; mismatched case would generate invalid patterns and quietly fall through.

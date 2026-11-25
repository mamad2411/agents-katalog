---
name: agents-md-writer
description: Create or update project-level AGENTS.md and CLAUDE.md guidance that maps real skills to project tasks without replacing native skill discovery. Use for cross-tool workspace instructions, scoped routing, and preserving existing project rules.
---

# Workspace Guidance Writer

Keep project instructions accurate without forcing every skill to load for every task.

1. Read existing guidance at the workspace and relevant parent/subproject levels. Preserve unrelated rules and user edits.
2. Inventory relevant skill locations, real folders, shared targets, missing entries, and name collisions. Do not read account settings or access files.
3. Distinguish discovery from project routing:
   - Codex discovers repository/user `.agents/skills` folders and supports linked skill folders. [Official guidance](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills), checked 2026-10-14.
   - Claude Code discovers project/personal `.claude/skills` folders. [Official guidance](https://code.claude.com/docs/en/skills), checked 2026-10-14.
   - Inspect compatibility locations already in use; do not move or duplicate skills automatically.
4. Propose a small task-specific map using verified workspace-relative references. Avoid blanket claims that a tool cannot discover skills.
5. Show the intended diff before replacing substantive instructions. Update only requested files. A short CLAUDE.md pointer can be useful if it preserves existing load order, but is not mandatory.
6. Verify referenced files exist and confirm routing/discovery with the target tool after its supported refresh. File existence alone is not integration success.

## Example structure

```markdown
# Project guidance

## Scope

These rules apply to this project. Preserve more specific subproject instructions.

## Skill routing

- For release preparation, use the installed safety-review skill when available.
- For a local-only reference, read the verified relative path listed here.

## Project constraints

Record actual project requirements and authorization boundaries.
```

Do not paste private profiles, inventories, source registries, or access configuration into public instructions. Do not replace, relink, or install skills as a side effect of writing guidance.

Return the diff, unresolved references/conflicts, and discovery checks performed or pending.

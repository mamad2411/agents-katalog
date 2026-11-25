---
name: dotvibe-migration
description: Use when the user asks to call or use dotvibe, export memories, import old Mac memories, migrate AI coding memory, restore Claude Code memory, move Claude Code/Codex CLI/OpenCode settings, apply or create a .vibe recipe, or says Chinese phrases such as 调用 dotvibe, 导出记忆, 导入旧 Mac 记忆, 迁移 AI coding 记忆, 恢复 Claude Code memory, vibe recipe.
---

# dotvibe Migration

Guide users through dotvibe migrations as a choice-driven assistant. The user should be able to use simple natural language such as `调用 dotvibe 导出记忆` or `调用 dotvibe 导入旧 Mac 的记忆，备份在 <path>`; do not require them to name this skill or provide dotvibe commands.

## Start Here

1. Read `references/intents.md` and classify the user's natural-language intent.
2. Run `dotvibe agent doctor --json` before any export/import/setup/write workflow.
3. For source Mac export, read `references/source-export.md`.
4. For destination Mac import, read `references/destination-import.md`.
5. If `import-plan` reports `project_relocations`, or the user mentions a changed username/home path, missing project checkout, clone, repo mismatch, or loading old project memory, read `references/project-relocation.md`.
6. If project memory conflicts exist, a stage directory exists, or the user asks to review/merge memory, read `references/memory-merge.md`.
7. For risky actions, recipe apply, installer commands, overwrites, or lint overrides, read `references/safety.md`.
8. For validating the skill behavior itself, read `references/testing.md`.

## Natural Language Entrypoints

These prompts should trigger the standard flow without asking the user to restate commands:

- `调用 dotvibe 导出记忆`
- `调用 dotvibe 导入旧 Mac 的记忆，备份在 ~/Downloads/dotvibe.tar.gz`
- `帮我备份这台 Mac 上的 Claude Code / Codex / OpenCode 记忆`
- `帮我把旧 Mac 的 AI coding 记忆恢复到这台新 Mac`
- `帮我导出一个可以分享给团队的 vibe recipe`
- `帮我应用这个 .vibe recipe`
- `新 Mac 用户名变了，帮我加载旧项目 memory`

## Rules

- Ask choice-style questions; avoid open-ended command prompts.
- Do not ask users to choose raw flags when the skill can translate choices into dotvibe commands.
- Always run a JSON plan or dry-run before writing.
- Before direct full-archive imports or `--force`, require either a fresh destination-side backup or a staging workspace the user has reviewed.
- Never use `--force`, `--yes`, setup installs, `git clone`, recipe apply, or direct import writes without explicit user confirmation.
- Prefer `dotvibe import --stage` for existing project memory.
- If per-project relocation safety conflicts with a top-level `safe-to-import` recommendation, choose the safer per-project path.
- Do not paste secrets or full private memory into chat unless the user explicitly asks after a warning.
- After any write, summarize the result and show recovery instructions. Recipe apply creates rollback records; full archive import currently requires the pre-import backup, staged local copies, or manual recovery.

## Common Entrypoints

- Source Mac export: `dotvibe agent doctor --json`, `dotvibe agent inventory --json`, then `dotvibe agent export-plan --json`.
- Destination Mac import: `dotvibe agent doctor --json`, `dotvibe agent import-plan <archive> --json`, then `dotvibe import <archive> --stage --stage-dir <dir>` when review is needed.
- Shareable setup: use `dotvibe recipe inspect/lint/diff/apply` and rollback guidance.

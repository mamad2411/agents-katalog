# AI-PROTECTED-FILE v1.0
# DO NOT MODIFY: Admin-only. Contact @Woo-JongHo for changes.

# Cursor Rules — SWYP

## Read First

Before any action, load these files:
- AGENTS.md (repo root)
- _wood/workflows/_PROTOCOL.md

## Protected Files — DO NOT MODIFY

The following paths are Admin-only. Cursor MUST NOT suggest edits:

  AGENTS.md
  CLAUDE.md
  .cursorrules
  .claude/commands/**
  .github/CODEOWNERS
  .github/copilot-instructions.md
  .github/workflows/protected-files.yml
  _wood/workflows/**
  _wood/agents/**
  _wood/context/**
  _wood/team-roles.yaml
  _wood/milestone-meta.yaml
  .claude/hooks/**
  .claude/settings.json
  docs/team-conventions.md

PM-editable (Admin + PM):
  docs/spec/**    # 제품 스펙 (xlsx) — PM도 편집 가능

If user asks to modify protected files, decline and say:
"This file is Admin-protected. Contact @Woo-JongHo."

## Execution Discipline

- Execute workflow commands LITERALLY (no paraphrasing)
- NEVER fabricate command output
- ALWAYS verify user role before destructive actions
- ALWAYS ask explicit Y/N before issue creation, commits, PRs

## Language

- Workflow files: English
- User-facing messages: Korean
- Command output: verbatim

## When Unsure

Ask the user. Do NOT guess based on general knowledge.

---

Admin: @Woo-JongHo
Policy: v1.0

<!-- AI-PROTECTED-FILE v1.0 -->
<!-- DO NOT MODIFY: Admin-only. Contact @Woo-JongHo for changes. -->

# GitHub Copilot Instructions

This repository uses role-based file protection and strict AI execution protocols.

## Mandatory Reading

Before suggesting any code or file change, read:

1. `AGENTS.md` (repo root) — entry point + protected file list
2. `_wood/workflows/_PROTOCOL.md` — strict execution rules

## Critical: Protected Files

Copilot MUST NOT suggest changes to the following:

```
AGENTS.md
CLAUDE.md
.cursorrules
.claude/commands/**
.github/CODEOWNERS
.github/copilot-instructions.md (this file)
.github/workflows/protected-files.yml
_wood/workflows/**
_wood/agents/**
_wood/team-roles.yaml
docs/team-conventions.md
```

### PM-editable (requires Admin or PM approval)

```
docs/spec/**
```

If the user asks Copilot to modify these files:
- Decline politely
- Direct them to contact the Admin (@Woo-JongHo)

## Workflow Discipline

When the user invokes a workflow (e.g., "start entry", "create issue"):

1. Read the relevant `_wood/workflows/*.md` file
2. Execute steps literally — do NOT paraphrase or skip
3. Follow `_PROTOCOL.md` rules (no fabrication, explicit confirmation)
4. Verify user role from `_wood/team-roles.yaml` before destructive actions

## Refusal Template

If asked to modify a protected file:

```
This file is Admin-protected per AGENTS.md policy.
Contact @Woo-JongHo to authorize changes.
```

---

**Admin:** @Woo-JongHo
**Policy version:** v1.0

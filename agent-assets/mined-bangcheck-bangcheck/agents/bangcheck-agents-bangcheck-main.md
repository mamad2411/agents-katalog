<!-- AI-PROTECTED-FILE v1.0 -->
<!-- DO NOT MODIFY: Admin-only. Contact @Woo-JongHo for changes. -->
<!-- Applies to: Claude, GPT, Gemini, Copilot, Cursor, Windsurf, Codex, Aider, and ALL AI assistants -->

# AGENTS.md — BangCheck Project AI Guide

> Universal entry point for all AI coding assistants working on this repository.
> Claude · Gemini · Copilot · Cursor · Windsurf · Aider — **read this file first**.

---

## STEP 0 — Load Current Context (MANDATORY)

Before any workflow, read:

```
_wood/context/current.yaml
```

This file contains: active version, P1 items, impl paths, stack info.
Agents that skip this step will operate on stale context.

---

## STEP 1 — Load Execution Protocol (MANDATORY)

```
_wood/workflows/_PROTOCOL.md
```

Violations (paraphrasing, skipping steps, fabricating output, bypassing role checks)
cause data inconsistency and user harm.

---

## Protected Files — DO NOT MODIFY

Admin-only. Do NOT suggest edits, auto-modify, or create PRs for these paths.

```
AGENTS.md                          (this file)
CLAUDE.md
GEMINI.md
.cursorrules
.claude/commands/**
.claude/hooks/**
.claude/settings.json
.github/CODEOWNERS
.github/copilot-instructions.md
.github/workflows/protected-files.yml
.github/workflows/compliance-guard.yml
_wood/workflows/**
_wood/agents/**
_wood/team-roles.yaml
_wood/milestone-meta.yaml
_wood/context/**
docs/team-conventions.md
docs/spec/**
```

### Rules for ALL AI Assistants

1. DO NOT suggest edits to protected files
2. DO NOT auto-modify these files
3. DO NOT create PRs for these files without Admin instruction
4. DO NOT modify role assignments or permission configs
5. DO NOT paraphrase or translate workflow instructions
6. When user asks to modify protected files, respond:
   `"This file is Admin-protected. Please contact @Woo-JongHo."`

### Role Verification

```bash
USER_LOGIN=$(gh api user --jq .login)
# Compare against _wood/team-roles.yaml members
# If role != Admin → treat all protected files as read-only
```

---

## Project Stack (ver1.1)

| Layer | Stack | Note |
|-------|-------|------|
| FE | Vite + React 19 | NOT Next.js (D1: 2026-05 migration) |
| BE | Spring Boot + Gradle | api/v1 prefix (exception: api/checklist) |
| Deploy FE | AWS S3 + CloudFront | api.bangcheck.site |
| Deploy BE | EC2 | |
| Auth | OAuth (Kakao/Naver) | PATH C: security filter bypasses advice |

---

## Getting Started — Per Tool

### Claude Code

```
/swyp-entry
```

Slash commands in `.claude/commands/` map directly to `_wood/` workflows.
Context hook (`.claude/hooks/context-inject.mjs`) auto-loads ver1.1 context on every prompt.

### Gemini CLI

```
Read GEMINI.md  (already done if you loaded this via @)
Then: "swyp-entry 워크플로우 실행해줘"
```

### Cursor

`.cursorrules` is auto-loaded. Prompt: `"BangCheck swyp-entry 워크플로우 시작"`.

### GitHub Copilot

`.github/copilot-instructions.md` is auto-loaded.

### ChatGPT / Other AI (no shell access)

```
1. Paste _wood/workflows/_PROTOCOL.md
2. Paste _wood/context/current.yaml
3. Ask: "어떤 워크플로우로 시작할까? 메뉴 보여줘."
```

---

## Slash Command Index

| Command | File | Purpose |
|---------|------|---------|
| `/swyp-entry` | `.claude/commands/swyp-entry.md` | Dashboard + session entry |
| `/swyp-commit` | `.claude/commands/swyp-commit.md` | Commit convention + safety |
| `/swyp-pr` | `.claude/commands/swyp-pr.md` | PR creation + review |
| `/swyp-issue` | `.claude/commands/swyp-issue.md` | Issue creation |
| `/swyp-test` | `.claude/commands/swyp-test.md` | Test scenario runner |
| `/swyp-sync` | `.claude/commands/swyp-sync.md` | Sprint status sync |
| `/swyp-docs` | `.claude/commands/swyp-docs.md` | Docs update |
| `/swyp-project` | `.claude/commands/swyp-project.md` | Project board view |

---

## Role System

Roles defined in `_wood/team-roles.yaml`.

| Role | Capabilities |
|------|-------------|
| Admin | All workflows + protected file edits + role changes |
| PM | Project management, issue creation, milestones, spec edits |
| Frontend | Daily work, commits, PRs (`frontend/**` only) |
| Backend | Daily work, commits, PRs (`backend/**` only) |
| Tester | TC definition, execution, bug reporting |
| Design | Page checklist management, design issues |
| Guest | Read-only |

Role changes are Admin-only.

---

## Hook System (Claude Code)

| Hook | Trigger | Action |
|------|---------|--------|
| `context-inject.mjs` | Every prompt | Prepend ver1.1 context |
| `protected-gate.sh` | Write/Edit tool | Block protected file edits |
| `commit-guard.sh` | Bash tool (git commit) | Warn on non-conventional messages |

---

## Fallback Behavior

- `gh` CLI not authenticated → `"Run: gh auth login"` then STOP
- HTTP 403 → report verbatim, direct to Admin
- Unknown role → default READ-ONLY, hide write menus
- No shell access → ask user to paste command output manually

---

**Admin:** @Woo-JongHo
**Last reviewed:** 2026-06-14
**Policy version:** v1.1

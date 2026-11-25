---
name: kratos-memory
description: "Persistent memory system for AI coding agents. Use this PROACTIVELY — do not wait to be asked. At session start, check what Kratos remembers about the current project. During work, save bug fixes, architecture decisions, how things work, and lessons learned. At session end, save a summary if significant work was done. Triggers: any coding session, any project work, when the user explains something important, after fixing bugs, after making decisions, when onboarding to a codebase, when the user says 'remember', 'save this', 'what do you know about', or asks about prior context."
---

# Kratos Memory

Persistent memory across sessions for any AI coding agent. Save what matters, recall it later. Local SQLite, zero network calls, 40ms per command.

## Setup Check

Before using any command, verify kratos-memory is installed AND working:

```bash
kratos-memory status
```

**If command not found** — install it:
```bash
npm install -g kratos-memory
```

**If status fails with a native module error** (e.g. `NODE_MODULE_VERSION` mismatch) — reinstall:
```bash
npm uninstall -g kratos-memory && npm install -g kratos-memory
```

**If npm is unavailable**, use npx (slower but works without install):
```bash
npx kratos-memory@latest status
```

Only proceed once `status` runs successfully. If it shows project info and memory stats, the setup is healthy.

## Two Memory Scopes

Kratos has two memory layers. Use the right one:

**Project memory** (default) — isolated per project. Architecture decisions, repo-specific patterns, project config, file structures. Only visible when working in that project.

**Global memory** (`--global` flag) — shared across ALL projects. Reusable bug fixes, tool gotchas, workflow patterns, general engineering lessons. Visible from any project.

Add `--global` or `-g` to any command to use global memory:
```bash
kratos-memory save "..." --global     # save to global
kratos-memory search "..." --global   # search global
kratos-memory recent --global         # recent global memories
```

## Session Start — Always Do This

At the beginning of every session, load project context:

```bash
kratos-memory summary
```

This shows pinned rules, key decisions, topics, and recent activity. If working on a specific area, search for it:

```bash
kratos-memory ask "How does [area] work?"
```

Use this context to avoid re-asking the user things they already explained in prior sessions.

## When to Save — Proactive Triggers

Save immediately when any of these happen. Do not ask permission — just save.

**After fixing a bug — save BOTH project and global:**
```bash
# Project: what was fixed in this repo
kratos-memory save "Fixed [what] — root cause was [why]. Changed [file] to [how]." --tags bug,fix --importance 4 --paths path/to/file.ts

# Global: the reusable lesson (only if the fix applies beyond this project)
kratos-memory save "If you encounter [symptom], the cause is usually [root cause]. Fix: [general solution]." --tags bug,fix --importance 4 --global
```

**After the user explains how something works:**
```bash
kratos-memory save "[What they explained]" --tags architecture --importance 4 --paths relevant/file.ts
```

**After making a design or architecture decision:**
```bash
kratos-memory save "Chose [X] over [Y] because [reason]." --tags decision,architecture --importance 5
```

**After discovering infrastructure/deployment details:**
```bash
kratos-memory save "[Service] hosted on [platform]. [Details]." --tags infrastructure --importance 4
```

**When the user sets a rule ("never do X", "always do Y"):**
```bash
kratos-memory save "[The rule]" --tags rules --importance 5
```
Then pin it so it always surfaces first:
```bash
kratos-memory pin <id>
```

**After discovering a tool gotcha or workflow pattern (GLOBAL):**
```bash
kratos-memory save "npm rebuild better-sqlite3 reports success but doesn't build. Use npm run build-release instead." --tags tooling,gotcha --importance 4 --global
```

**After completing significant work:**
```bash
kratos-memory save "Session: [what was done]. Key changes: [list]. Files: [list]." --tags session --importance 3
```

## Core Commands — Quick Reference

| Command | Use |
|---------|-----|
| `save "<text>" --tags X --importance N` | Store a memory |
| `save "<text>" --global` | Store a global memory (shared across all projects) |
| `search "<query>"` | Find by keyword |
| `search "<query>" --global` | Search global memories |
| `ask "<question>"` | Natural language query |
| `recent` | Latest memories |
| `get <id>` | Full memory details |
| `update <id> "<text>"` | Edit without delete/re-save |
| `forget <id>` | Delete |
| `pin <id>` | Pin — always surfaces first |
| `summary` | Project brief |
| `export` | Dump all as JSON |
| `status` | Dashboard |
| `scan "<text>"` | Check for secrets/PII |

Add `--global` / `-g` to any read/write command to use global scope.

For full command reference with all options, see [references/api_reference.md](references/api_reference.md).

## Saving Best Practices

- **Be specific** — "Auth uses JWT RS256 with httpOnly refresh tokens" not "we use JWT"
- **Include file paths** — `--paths src/auth.ts` helps future agents find the code
- **Include the WHY** — "Chose X because Y" is more valuable than "Using X"
- **Use consistent tags** — `bug`, `fix`, `architecture`, `decision`, `security`, `database`, `api`, `frontend`, `backend`, `infrastructure`, `performance`, `rules`
- **Scan before saving sensitive text** — `kratos-memory scan "<text>"` detects API keys, passwords, PII
- **Pin critical rules** — anything that should never be forgotten

## When to Save Global vs Project

**Save to GLOBAL (`--global`) when:**
- The lesson applies to ANY project (not just this one)
- You fixed a bug caused by a tool/library/platform behavior
- You discovered a workflow pattern (e.g., "Codex needs --write flag")
- The user shares a general preference that should apply everywhere

**Save to PROJECT (default) when:**
- It's about THIS repo's architecture, patterns, or config
- It's about specific files, endpoints, or schemas in this project
- It's a project-specific rule or convention

**When stuck on a bug — search both:**
```bash
kratos-memory search "the error message"           # check this project first
kratos-memory search "the error message" --global   # then check global lessons
```

## What NOT to Save

- Code that's already in the repo (that's what git is for)
- Temporary debugging notes
- Obvious language/framework knowledge Claude already has
- Duplicate information — search first, update if exists
- Routine edits to global memory (don't save "edited button.tsx" globally)

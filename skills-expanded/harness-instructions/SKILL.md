---
name: harness-instructions
description: >-
  Writes a short AGENTS.md the agent actually reads — rules, startup flow, and
  verification commands. Use when instructions are too long, missing, or the
  agent keeps asking the same project questions.
---

# Harness Instructions

## What this does for you

- **Stop re-explaining the project** — the agent reads AGENTS.md first
- **Short rules that stick** — ~100 lines at the root, details in `docs/`
- **Copy-paste verification** — commands the agent can run, not vague prose

The repository is the single source of truth (Lesson 03). Instructions should be a **map**, not a manual (Lesson 04).

## Principles

1. **~100 lines max** in root `AGENTS.md` / `CLAUDE.md`
2. **Progressive disclosure**: link to `docs/` for detail
3. **Constrain, don't micromanage**: executable invariants, not implementation steps
4. **Copy-pasteable commands**: verification as code blocks, not prose

## Recommended structure

```markdown
# AGENTS.md

## Purpose (1 line)
[What the project does]

## Stack
[Language, framework, key versions]

## Startup flow
1. pwd
2. Read progress.md
3. Read feature_list.json → pick highest-priority unfinished feature
4. git log --oneline -5
5. ./init.sh

## Verification commands
- Tests: `...`
- Lint: `...`
- Type-check: `...`
- Full: `./init.sh`

## Invariant rules
- One feature at a time
- Do not mark done without evidence
- Do not change verification rules during implementation

## Definition of done
[Brief checklist]

## Detailed documentation
- Architecture: docs/architecture.md
- Conventions: docs/conventions.md
- API: docs/api.md

## End of session
[5 closing steps]
```

## Anti-patterns

| Bad | Good |
|-----|------|
| 500 lines in AGENTS.md | 80 lines + docs/ |
| "Follow best practices" | "All APIs use OAuth 2.0" |
| Project history | Current commands and rules |
| Duplicate full README | Link to README |

## Workflow

1. Read the project: stack, package.json scripts, directory structure
2. Identify what the agent must know **before** writing code
3. Write a short AGENTS.md with routing to docs/
4. Create docs/ only for what does not fit in the map
5. Validate: can a new agent start using only these files?

## Related skills

- `harness-repo-knowledge` — `docs/REPO_MAP.md` for where code lives

## Templates

- [templates/agents.md](../../templates/agents.md)

## Course reference

- Lesson 03: The repository as a system of record
- Lesson 04: Why a giant instruction file fails
- Project 02: Agent-legible workspace

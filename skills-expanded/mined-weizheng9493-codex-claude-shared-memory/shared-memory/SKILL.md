---
name: shared-memory
description: Cross-agent shared memory for Codex, Claude, and compatible skill runtimes. Use when the user wants multiple AI agents to share durable context, technical decisions, project notes, long-term facts, preferences, or a portable file-backed memory protocol that both Codex and Claude can install and use.
---

# Shared Memory

## Overview

Use this skill to coordinate work across Codex and Claude through a shared local file store. The default memory directory is `~/Documents/ai-shared-memory/`; set `AI_MEMORY_DIR` only when the user explicitly wants a different location.

The bundled `scripts/memory.sh` CLI writes structured Markdown entries, maintains `memory-index.yml`, and can create compact snapshots so either agent can read what the other agent already learned, decided, or completed.

## Memory CLI

Use the script bundled with this skill:

```bash
scripts/memory.sh <command> [args...]
```

If the skill is installed with `scripts/install.sh`, a stable copy of the CLI is also placed at:

```bash
~/Documents/ai-shared-memory/scripts/memory.sh
```

Set `AGENT_NAME` before writing so memory entries show their source:

```bash
AGENT_NAME=codex scripts/memory.sh today
AGENT_NAME=claude scripts/memory.sh today
```

## Start Of Work

At the start of each meaningful conversation or task, read shared context before acting:

```bash
export AGENT_NAME=codex   # or claude
scripts/memory.sh today --tail 20
scripts/memory.sh recent 5
```

If the user names a project, repository, or workspace, also read its project memory:

```bash
scripts/memory.sh project <project-name>
```

When memory volume is small, it is acceptable to read broader context with `today`, `index`, or `fact user-prefs`. When memory volume becomes expensive, prefer `today --tail 20`, `recent 5`, `today --summary`, and `project <name>`.

When using prior memory in a user-facing answer, cite it inline as `(来源: mem-xxx, codex)` or `(来源: mem-xxx, claude)`. If another agent already made a relevant decision, mention it so work does not repeat unnecessarily.

## End Of Work

After completing substantial work, write only durable information. Before writing, ask whether a future Codex or Claude run would avoid repeated explanation or mistakes by seeing this memory.

```bash
scripts/memory.sh log "Completed <work summary>."
scripts/memory.sh decide <topic> "<title>" "<decision and rationale>"
scripts/memory.sh context <project> "<project context update>"
scripts/memory.sh context --replace <project> "<current project context>"
scripts/memory.sh fact user-prefs "<stable user preference or long-term fact>"
```

Choose the narrowest command:

- `log`: completed work that another agent should know happened.
- `decide`: technical or product decisions and why they were chosen.
- `context`: repository, product, architecture, dependency, or workflow state. Use `context --replace` when the entry represents the current state rather than a historical update.
- `fact`: stable user preferences, long-lived constraints, or durable facts.

Use simple slug keys for `<topic>`, `<project>`, and `<category>`: letters, numbers, `.`, `_`, and `-` only. Do not include path separators.

Do not record temporary debug output, pure search results, routine failures, low-value intermediate steps, unconfirmed guesses, expired information, or casual chat. Do not record sensitive private information unless the user explicitly asks and the information is necessary; summarize it when possible.

## Commands

Writing:

```bash
scripts/memory.sh log <message>
scripts/memory.sh decide <topic> <title> <body>
scripts/memory.sh context [--replace] <project> <content>
scripts/memory.sh fact <category> <content>
```

Reading:

```bash
scripts/memory.sh today [--tail N] [--summary] [--json]
scripts/memory.sh recent [n] [--json]
scripts/memory.sh project <project-name>
scripts/memory.sh search [--all] <query>
scripts/memory.sh list decisions|contexts|facts|logs|snapshots|projects
scripts/memory.sh index
```

Maintenance:

```bash
scripts/memory.sh snapshot [--force] [--recent N]
scripts/memory.sh archive
scripts/memory.sh delete <id>
scripts/memory.sh version
```

## Installation

This folder is a complete skill. To install it for both agents from a cloned copy, run:

```bash
bash scripts/install.sh --both
```

The installer copies this folder into:

- Codex: `${CODEX_HOME:-$HOME/.codex}/skills/shared-memory`
- Claude: `${CLAUDE_HOME:-$HOME/.claude}/skills/shared-memory`

The installer also initializes `~/Documents/ai-shared-memory/` and copies the CLI to `~/Documents/ai-shared-memory/scripts/memory.sh`. It does not overwrite global instruction files. If a runtime does not auto-load skills, manually reference this `SKILL.md` or copy the folder to that runtime's user skill directory.

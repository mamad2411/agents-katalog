---
name: meta-docs
description: "A frontmatter-first docs workflow that separates metadata search from body reads. Keywords: docs, frontmatter, metadata, search."
argument-hint: "[search|read|update|create] [options]"
---

# Meta Docs

## Objective

- Separate metadata search from body reads to minimize context usage.
- Keep the docs knowledge base consistent with structured updates and logs.

## Directory and Metadata Rules

- All documents live under `docs/`. Directory structure is not enforced.
- Avoid `docs/{TYPE}` as a convention; do not create directories purely by type.
- Classification is defined by the `type` metadata (single string).
- Recommended types: `design`, `spec`, `guide`, `log`, `reference`, `decision`, `research`, `meeting`, `incident`, `runbook`, `roadmap`, `report`, `checklist`, `retro`, `note`

Every document must include YAML frontmatter:

```yaml
---
title: "Document title"
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "name <email>"
editors: ["name <email>"]
type: "design"
tags: ["ai", "troubleshooting", "gitlab"]
history:
  - "YYYY-MM-DD name <email>: initial entry"
  - "YYYY-MM-DD name <email>: change summary"
---
```

- `author`/`editors` should use Git user info (`user.name`, `user.email`). If unavailable, fall back to the system username.

## Prerequisites

This skill assumes `uv` for execution.

```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Recommended execution style:

```bash
uv run --project skills/meta-docs skills/meta-docs/doc_manager.py <command> [options]
```

Use `--root` when the project root differs from the current working directory. You can place `--root` before or after the subcommand.

## Mandatory Behavior Rules

1. Context discipline: never use `cat`, `grep`, or `find` to locate docs; always run `search` first.
2. Selective reads: choose the minimal set of files from search results and read only those.
3. Active maintenance: after code or architecture changes, always call `update`.
4. Error capitalization: after resolving complex bugs, create a troubleshooting log with `create`.

## Commands

### 1) search

- Input: `--tags "keyword"`, `--type "design"`, `--dir "path"` (optional)
- Behavior: parse only YAML frontmatter and output matching docs as a JSON array

Example:

```bash
uv run --project skills/meta-docs skills/meta-docs/doc_manager.py search --tags "ai troubleshooting" --type "incident" --dir "team"
```

### 2) read

- Input: `--path "docs/target.md"`
- Behavior: return only the document body (frontmatter excluded)

Example:

```bash
uv run --project skills/meta-docs skills/meta-docs/doc_manager.py read --path "docs/20260312-meta-docs-intro.md"
```

### 3) update

- Input: `--path "..." --log "change summary"`
- Behavior: update `updated`, append `history` as `YYYY-MM-DD name <email>: log`
- If `author` is missing, it is auto-filled with the current editor
- The current editor is appended to `editors`

Example:

```bash
uv run --project skills/meta-docs skills/meta-docs/doc_manager.py update --path "docs/20260312-meta-docs-intro.md" --log "architecture updates"
```

### 4) create

- Input: `--title "..." --tags "..." --content "..." [--type "log"]`
- Behavior: create `YYYYMMDD-{TITLE}.md` under `docs/` (type defaults to `log`, override with `--type`)
- Title rule: use English titles so filename slugs stay within lowercase a-z, digits, `-`, and `_`
- `author`/`editors` prefer Git user info and fall back to system username

Example:

```bash
uv run --project skills/meta-docs skills/meta-docs/doc_manager.py create --title "redis-timeout" --tags "infra troubleshooting" --content "Root cause and fix" --type "incident"
```

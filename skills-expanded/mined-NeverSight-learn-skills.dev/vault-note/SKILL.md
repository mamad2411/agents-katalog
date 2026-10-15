---
name: vault-note
description: Read, write, and search notes in the shared Obsidian vault across all AI tools.
triggers:
  - Obsidian
  - vault
  - OBSIDIAN_VAULT_PATH
  - ".md note"
---

# Vault Note

Access the shared Obsidian vault for reading and writing knowledge notes.

## Vault Path

Read from `OBSIDIAN_VAULT_PATH` env var. Default paths:
- macOS/Linux: `~/Documents/Obsidian Vault/`
- Windows: `%USERPROFILE%/Documents/Obsidian Vault/`

Resolve the env var before passing to file tools — they don't expand shell variables.

## Operations

**Always start with the MOC index.** Before reading or searching individual notes, read `知识库 MOC.md` first. It contains a curated index of all vault notes organized by topic — faster than full-text search.

- **Read MOC**: `read_file` with vault path + `/知识库 MOC.md`
- **Read note**: `read_file` with full path (from MOC wikilinks)
- **Search**: `search_files` with `target: "content"` or `target: "files"` + `*.md` glob
- **Write**: `write_file` with full path. After writing, update MOC.

## Directory Convention

- `基础设施/` — Infrastructure & deployment
- `踩坑记录/` — Bugs & fixes
- `技术笔记/` — Technical knowledge
- `项目/` — Project notes

## Language Convention

Skills (SKILL.md) → **English** (reader is AI, more precise, fewer tokens)
Vault notes (.md in Obsidian) → **中文** (reader is human, user's native language)

## Rules

- `[[Note Name]]` for cross-references
- **Never include company sensitive info** — no business code, access keys, secrets, unreleased requirements, internal URLs, or proprietary configs. Use `***` placeholder or generic descriptions.

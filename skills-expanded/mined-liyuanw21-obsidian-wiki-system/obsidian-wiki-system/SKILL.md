---
name: obsidian-wiki-system
description: Initialize or maintain a reusable Obsidian wiki knowledge iteration system with raw inbox, wiki pages, source/concept/synthesis/project templates, workflows, prompts, indexes, logs, and AGENTS.md rules. Use in Codex, OpenCode, or any agent that can read skill folders when the user wants to create a new Obsidian vault, replicate this Routine wiki pattern, scaffold a personal knowledge base, or turn raw notes into an iterative wiki.
---

# Obsidian Wiki System

Use this skill to scaffold or maintain an Obsidian vault that follows the `raw -> wiki -> index/log` knowledge iteration loop.

This folder is agent-portable: use the same `SKILL.md`, `references/`, and `assets/` in Codex, OpenCode, or another agent skill system that can access local files.

## Scaffold Workflow

1. Inspect the target folder first. Preserve any existing user notes.
2. Read `references/language.md` and choose the vault language from the user's request, existing notes, or locale.
3. Read `references/structure.md` for the directory model and required files.
4. Copy the selected template into the target vault:
   - Chinese: `assets/vault-template-zh/`.
   - English: `assets/vault-template-en/`.
   - Other languages: copy the closest template and localize user-facing prose.
5. Replace placeholders:
   - `{{date}}` with the current local date.
   - `{{vault_name}}` with the target folder name unless the user provides a name.
6. If target files already exist, merge conservatively instead of overwriting. Ask before replacing meaningful content.
7. Configure Obsidian templates and daily notes if `.obsidian/` exists or the user wants Obsidian-native setup.
8. Tell the user to start from the localized entry page, such as `首页.md` or `Home.md`.

## Maintenance Workflow

1. Read the vault `AGENTS.md`, localized entry page such as `首页.md` or `Home.md`, `wiki/index.md`, and `ops/workflows.md`.
2. For new materials, put originals in `raw/inbox/` and create processed pages in `wiki/sources/`.
3. Extract durable ideas into `wiki/concepts/`, questions into `wiki/questions/`, projects into `wiki/projects/`, and cross-source conclusions into `wiki/syntheses/`.
4. Update `wiki/index.md` for important new pages.
5. Update `wiki/log.md` after structure changes, major pages, or agent-stack changes.
6. Use `ops/prompts/ingest-source.md`, `query-wiki.md`, and `lint-wiki.md` as reusable operating prompts.

## Boundaries

- `raw/` may be messy; `wiki/` should become increasingly clear.
- Do not turn unsupported excerpts into facts. Mark uncertain points as `待验证`.
- Prefer `[[wikilinks]]` for internal vault pages.
- Keep source pages traceable: every important claim should link back to a source or be labeled as inference.
- Do not install unrelated plugins, MCPs, or external tools unless the user asks.

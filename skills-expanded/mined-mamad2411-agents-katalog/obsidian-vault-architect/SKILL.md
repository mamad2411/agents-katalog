---
name: obsidian-vault-architect
description: Designs and enforces folder structure, naming conventions, and template standards for Obsidian vaults.
category: obsidian
tags: [obsidian, vault, structure, templates, conventions]
agents: [opencode, freebuff, antigravity, codex]
---

# obsidian-vault-architect

## Purpose

Establishes and maintains the structural backbone of an Obsidian vault. Defines folder hierarchy, naming conventions, MOC (Map of Content) placement, template files, and tag taxonomy. Ensures consistent vault architecture across all domain-specific skills that write to Obsidian.

## Invocation

**OpenCode / Codex:** `Invoke obsidian-vault-architect`
**Freebuff:** `/skill obsidian-vault-architect`

## Workflow Steps

1. **Audit:** Survey current vault structure and identify inconsistencies.
2. **Design:** Propose folder hierarchy (Inbox, Projects, Areas, Resources, Archive — PARA or custom).
3. **Templates:** Create note templates for each domain (music, homelab, daily log).
4. **Tag taxonomy:** Define canonical tag set and document in `META/tags.md`.
5. **MOC:** Create or update index MOC notes for each top-level domain.
6. **Enforce:** Apply naming conventions to existing notes via rename batch.

## Inputs

- Current vault root path and existing folder structure
- Target organizational system preference (PARA, Zettelkasten, custom)
- Domain list to cover (music, homelab, projects, daily notes, etc.)

## Outputs

- Proposed folder hierarchy document
- Template files for each domain
- `META/tags.md` with canonical tag taxonomy
- MOC notes per top-level domain
- Rename/move batch plan for existing notes (user must confirm before execution)

## Safety

- Never delete notes; only rename or move with user confirmation.
- Always backup vault before structural changes.
- Log all changes to a vault-change-log note.

## Failure Modes

- Large vault with thousands of notes — chunk rename operations into batches; do not run all at once.
- Conflicting naming conventions from existing notes — surface conflicts to user before resolving.
- Vault backup unavailable — halt structural changes and prompt user to back up first.

## References

- [Obsidian Help](https://help.obsidian.md/)
- [PARA Method](https://fortelabs.com/blog/para/)

## Companion Skills

- `obsidian-homelab-logbook`, `obsidian-music-journal`, `homelab-logbook`

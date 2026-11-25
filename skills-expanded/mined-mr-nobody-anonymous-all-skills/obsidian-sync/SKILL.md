---
name: obsidian-sync
description: Plan and verify safe synchronization between an Obsidian vault and a working directory.
category: productivity
aliases:
- obsidian
- vault
- notes
- sync
- markdown-sync
triggers:
- Sync my Obsidian
- Mirror notes to Obsidian
- Update my vault
- Copy today's journal to Obsidian
keywords:
- obsidian
- vault
- notes
- sync
- markdown
- daily
- journal
- knowledge
- base
dependencies:
- optional:obsidian
risk: medium
version: 1.0.0
source: custom
enabled: true
capabilities:
- obsidian-sync
- productivity
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- notes
- obsidian
- productivity
- sync
- vault
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Obsidian Sync

## Purpose
Keep an Obsidian vault on disk in sync with a working folder of notes, daily logs,
inbox items, and TODOs produced by other skills (`daily-journal`, `unlazy`,
`adhd-task-breakdown`, etc.). The skill preserves frontmatter, internal links, and
the user's tagging conventions, and it never silently overwrites a note that has
changed on both sides.

## When to Use
- The user has a vault path and a working folder path
- A new note was just created in the working folder and needs to land in the vault
- A daily journal was generated and should be appended to the vault
- The user changed a note in the vault and wants the change reflected elsewhere

## When NOT to Use
- The user does not have an Obsidian vault (no action — exit)
- The vault is encrypted with a passphrase that has not been provided
- The user wants notes deleted from the vault (this skill never deletes)

## Capabilities
- Copy new files from the working folder into the vault under the right path
- Preserve YAML frontmatter exactly; never rewrite it
- Convert relative links (`[[Note]]`) only when the target is in a different folder
- Detect conflicts (file changed on both sides since last sync) and ask the user
- Maintain a `.sync-state.json` with checksums and last-seen mtimes
- Dry-run mode: report what would happen, change nothing

## Inputs
- `--vault PATH`  — the Obsidian vault root
- `--source PATH` — the working folder
- `--dry-run`     — show what would change, change nothing
- `--strategy merge|mirror|new-only` (default: `merge`)

## Workflow
1. **Load `.sync-state.json`** from the vault. If absent, do a full scan.
2. **Walk the source folder** and compute checksums.
3. **Compare** with the vault. Three buckets: `new`, `updated-source`, `conflict`.
4. **For `new`**: copy file into the vault, preserving relative path.
5. **For `updated-source`**: copy over the vault copy; record new checksum.
6. **For `conflict`**: write both versions to `<vault>/.conflicts/<ts>/` and ask the user.
7. **For files only in the vault**: leave alone (mirror strategy would copy them out).
8. **Write `.sync-state.json`**.

## Tools
- Filesystem copy / checksum (`sha256sum`, `Get-FileHash`, `shasum`)
- YAML parser (preserve order, do not re-serialize unless changed)
- Optional: `git` for a pre-sync safety commit in the vault

## Examples
**User:** "Sync today's journal into my vault."
**Response:** Vault: `~/Notes`. Source: `~/Working/2026-02-09.md`. Result: copied
under `daily/`. No conflicts.

**User:** "Mirror my project folder into Obsidian."
**Response:** Strategy: `mirror`. 12 new notes, 3 updated, 1 conflict
(`projects/alpha.md` changed in both). Conflict saved to `~/Notes/.conflicts/...`.

## Safety
- Never delete files from the vault
- Never overwrite a vault file that has changed locally without asking
- Always write conflicts to a separate folder, never in place
- Prefer `git commit` inside the vault before any change

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical productivity category.

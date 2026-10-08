---
name: import-claude-skills
description: Import and adapt skills from Claude Code style repositories into Codex. Use when Codex needs to inspect a third-party skills repo, identify folders that contain reusable SKILL.md-based workflows, copy compatible skills into `~/.codex/skills`, or warn about Claude-specific files and assumptions before porting.
---

# Import Claude Skills

Inspect Claude Code style skill repositories locally and port only the useful, compatible skill folders into Codex.

## Quick Start

1. Confirm the source is available on disk. Prefer a local clone or an extracted ZIP over copying from scattered web pages.
2. Run `scripts/list_claude_skills.py <repo-path>` to discover candidate skill folders and their trigger descriptions.
3. Read only the source `SKILL.md` files that match the user's request.
4. Check for Claude-specific assumptions before importing:
   - slash commands or command palettes
   - hooks or agent orchestration not available in Codex
   - hard-coded paths for `.claude/`
   - MCP/tooling requirements that are not present locally
5. Import a selected skill with `scripts/import_skill.py <source-skill-dir>`.
6. Open the copied skill and tighten the description, paths, and workflow so it feels native to Codex.

## Decide What To Port

Prefer skills that are mostly:

- procedural guidance in `SKILL.md`
- portable scripts in `scripts/`
- reference docs in `references/`
- templates or examples in `assets/`

Treat these as adaptation work, not copy-paste:

- skills that rely on Claude-specific commands or UI affordances
- skills that assume a different home directory layout
- skills that depend on remote installers or shell aliases
- giant "meta" repos where only a few folders are relevant to the user

If the repository is `everything-claude-code`, read [ecc-porting-notes.md](./references/ecc-porting-notes.md) before choosing a target skill.

## Import Workflow

### 1. Discover

Run:

```powershell
python scripts/list_claude_skills.py <repo-path>
```

Use the output to shortlist only the skills that match the user request.

### 2. Inspect

Open the shortlisted source `SKILL.md` files and look for:

- trigger language worth preserving
- scripts or references that should come along
- repo-specific instructions that should be rewritten or dropped

Do not bulk-load every source file in a large skills repo.

### 3. Copy

Run:

```powershell
python scripts/import_skill.py <source-skill-dir>
```

The importer copies only the common skill payload:

- `SKILL.md`
- `agents/`
- `scripts/`
- `references/`
- `assets/`

It skips common repo clutter such as `README.md`, install notes, and changelogs.

### 4. Adapt

After copying, update the imported skill so it is usable in Codex:

- rewrite Claude-specific wording
- update destination paths and examples
- remove instructions that depend on unavailable tools
- keep the frontmatter description explicit about when the skill should trigger

### 5. Validate

Run the Codex validator from the `skill-creator` system skill:

```powershell
python C:\Users\nd851\.codex\skills\.system\skill-creator\scripts\quick_validate.py <imported-skill-path>
```

Fix any reported issues before considering the import complete.

## Defaults

- Default destination root: `C:\Users\nd851\.codex\skills`
- Default import mode: copy into a new folder matching the source skill name
- Default behavior: fail rather than overwrite unless `--force` is passed to the importer

## Notes

- Prefer creating one clean Codex skill over mirroring an entire external repo.
- If the user provides only a GitHub URL, first turn it into a local checkout or extracted archive before using the scripts.
- Keep imported skills lean. Delete source files that are not needed by the Codex-facing workflow.

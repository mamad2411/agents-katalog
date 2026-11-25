---
name: claude-to-cursor-skill
description: Use this skill when converting Claude Code / Anthropic agent skills into Cursor Agent Skills, including the full skills directory tree (SKILL.md, references/, scripts/, assets/, examples/), not just the markdown entry file.
license: MIT
compatibility: Cursor Agent Skills, Claude Code skills, Codex-compatible SKILL.md packages
allowed-tools: Read Write Edit Bash Glob Grep
metadata:
  author: SixScripts
  version: 0.1.0
---

# Claude → Cursor Skill Converter

Convert a Claude skill package into a Cursor skill package while preserving **every file** in the skills directory.

## Overview

Claude and Cursor both use a `SKILL.md` entrypoint plus optional `references/`, `scripts/`, and related assets. This skill remaps Claude install roots (`.claude/skills`, plugin skill caches, `upstream/` overlays) into Cursor roots (`.cursor/skills` or `~/.cursor/skills`) and normalizes frontmatter for Cursor discovery.

## Activation

Activate when the user asks to:

- convert Claude skills to Cursor skills
- migrate `.claude/skills` into `.cursor/skills`
- port a Claude plugin skill (including `upstream/` trees) into a Cursor project skill
- keep scripts, references, assets, and examples intact during migration

## Required Inputs

- Source path to a Claude skill directory (must contain `SKILL.md` or `upstream/SKILL.md`)
- Destination root: project (`.cursor/skills`) or personal (`~/.cursor/skills`)
- Optional skill rename (defaults to source frontmatter `name` or directory name)

## Workflow

1. Locate the source skill root (directory containing `SKILL.md`, or Claude plugin layout with `upstream/`).
2. Inventory the **entire** directory tree — do not stop at `SKILL.md`.
3. Run `scripts/convert_claude_to_cursor.py` with CLI flags to copy and rewrite the package.
4. Run `scripts/validate_cursor_skill.py` on the output.
5. Report copied paths, frontmatter changes, and any skipped/unsafe files.
6. Read `references/claude-skill-format.md` if|when the source uses Claude plugin overlays (`upstream/`, `overlay.yaml`).
7. Read `references/cursor-skill-format.md` if|when Cursor frontmatter or install location is unclear.

## Output Contract

Emit a Cursor skill directory:

```text
.cursor/skills/<slug>/
  SKILL.md
  references/…     # preserved when present
  scripts/…        # preserved when present
  assets/…         # preserved when present
  examples/…       # preserved when present
  <other files>    # preserved unless unsafe
```

Also return a short conversion report: source → dest, file count, frontmatter keys kept/dropped, validation status.

## Available Scripts

- `scripts/convert_claude_to_cursor.py` — recursive copy + Cursor frontmatter rewrite
- `scripts/validate_cursor_skill.py` — verifies SKILL.md + directory integrity

Both scripts take CLI flags only (no interactive prompts).

## References

- Read `references/REFERENCE.md` if|when choosing which detailed reference to load next.
- Read `references/claude-skill-format.md` if|when parsing Claude / plugin skill layouts.
- Read `references/cursor-skill-format.md` if|when writing Cursor-compatible frontmatter and install paths.
- Read `references/conversion-rules.md` if|when deciding which files or metadata to keep, rewrite, or drop.

## Safety and Permissions

- Copy only within the requested source and destination roots.
- Reject path traversal (`..`), absolute escapes outside the destination root, and shell-metacharacter paths.
- Never copy secrets (`.env`, credential files) unless the user explicitly asks.
- Prefer project `.cursor/skills/` over `~/.cursor/skills-cursor/` (Cursor-managed builtins — do not write there).

## Failure Handling

- Missing `SKILL.md`: fail with a clear error and list candidate paths checked.
- Invalid YAML frontmatter: keep body, rewrite a minimal Cursor frontmatter from directory name + description heuristics, and warn.
- Destination exists: require `--force` to overwrite; otherwise abort.
- Validation failure: leave files in place and print actionable errors.

## Gotchas

- Claude plugin skills may nest content under `upstream/`; prefer overlay `SKILL.md` at the skill root when present, then merge `upstream/` files that are not overridden.
- Cursor descriptions should be third-person and include trigger terms; Claude descriptions often already work — keep them unless empty.
- Marketplace full-package validation (this repo) is stricter than Cursor runtime; converter output targets Cursor, not marketplace publish, unless the user asks to also wrap as a marketplace package.
- Binary assets must be copied byte-for-byte; do not UTF-8 re-encode them.

## Examples

### Convert a project Claude skill into a project Cursor skill

```bash
python3 scripts/convert_claude_to_cursor.py \
  --source .claude/skills/my-skill \
  --dest-root .cursor/skills \
  --force
```

### Convert a Claude plugin skill cache entry

```bash
python3 scripts/convert_claude_to_cursor.py \
  --source ~/.claude/plugins/cache/.../skills/nextjs \
  --dest-root .cursor/skills \
  --name nextjs \
  --force
```

See `examples/sample-claude-skill/` and the expected Cursor output in `examples/sample-cursor-skill/`.

## Validation

After conversion, run:

```bash
python3 scripts/validate_cursor_skill.py --path .cursor/skills/<slug>
```

Expect: `SKILL.md` present, valid `name`/`description`, and a non-empty file inventory that includes every copied relative path.

## Compatibility

- **Source:** Claude Code skills (`.claude/skills`), Claude plugin skill packages, portable `SKILL.md` directories
- **Target:** Cursor Agent Skills (`.cursor/skills`, `~/.cursor/skills`)
- **Hosts:** Codex / Claude / VS Code marketplace packaging is out of scope unless re-published through this app’s builder

---
name: codex-skillhub-package-conversion
description: Use when the user asks to turn a local skill bundle into "codex 可以安装的格式", package it cleanly, or install it into ~/.codex/skills. Best for SkillHub-style exports with manifest.json, zipped child skills, or mixed metadata.
argument-hint: "[source-bundle-path] [install|package-only]"
disable-model-invocation: true
user-invocable: false
allowed-tools:
  - Bash
  - Read
  - Grep
  - Edit
  - Write
---

# Codex SkillHub package conversion

## When to use

Use this when:
1. The source bundle is a local skill export that is not directly installable by Codex.
2. The user asks for "codex 可以安装的格式", a packaged `.skill` output, or a direct install into `~/.codex/skills/`.
3. The bundle contains multiple specialist skills and benefits from a top-level router skill.

Do not use this when:
1. The source is already a valid Codex skill directory with a clean `SKILL.md`.
2. The task is only to explain what an existing installed skill does.
3. The user wants a repo-local skill for one project rather than a converted external bundle.

## Inputs / context to gather

1. Confirm the source path from `$ARGUMENTS` or the user request.
2. Inspect the bundle shape first:
   - `manifest.json`
   - `skillsets/*.md`
   - zipped child skills
   - existing `SKILL.md`
3. Decide the output mode:
   - `install`: validate, package if useful, and copy to `~/.codex/skills/`
   - `package-only`: leave a converted bundle folder and optional `.skill` archives
4. Check whether the bundle should keep all child skills or only a focused subset.

## Procedure

1. Inventory the source bundle.
   - Find `manifest.json`, `skillsets/`, archives, and any existing `SKILL.md`.
   - Identify the natural router name and the child skill list.
2. Expand to Codex directory shape.
   - Create one directory per installed skill.
   - Ensure each child skill has `SKILL.md`.
   - Add `agents/openai.yaml` only when it improves discoverability or the bundle already uses that presentation layer.
3. Normalize frontmatter before any packaging.
   - Keep required top-level fields like `name` and `description`.
   - Move SkillHub-only presentation fields such as `label`, `homepage`, `category`, `version`, `model`, or `keywords` under `metadata` or remove them from top level.
   - Quote descriptions that contain YAML-breaking colons.
   - Align each `name` with the directory name, using lowercase kebab-case where needed.
4. Add a router skill when the bundle is multi-skill.
   - The router should describe when to use the bundle and how to route to each child skill.
   - Keep the router small and task-oriented.
5. Validate early.
   - Run `quick_validate.py` on the converted skills.
   - If the bundle contains Python resources, run a lightweight syntax pass such as `python3 -m compileall` and then remove `__pycache__`.
6. Package correctly.
   - Run `python3 -m scripts.package_skill` from the `skill-creator` project root, not as a loose script from an arbitrary directory.
   - Verify the archive layout is `skill-name/SKILL.md`.
7. Install only if requested.
   - Copy validated skill directories into `~/.codex/skills/`.
   - Keep the converted bundle folder separate so the user can delete it later if they want.
8. Explain the result.
   - Summarize what the router skill does.
   - List the child skills and their main triggers in plain language.

## Efficiency plan

1. Start by fixing frontmatter and names; that catches most install failures early.
2. Reuse one conversion pattern across sibling bundles instead of redesigning each one.
3. Create the router once the child set is stable; do not rewrite it after every file tweak.
4. Stop after validation plus the requested install/package output is proven.

## Pitfalls and fixes

- Codex rejects the skill even though the body looks fine
  - Likely cause: invalid frontmatter or non-Codex top-level keys.
  - Fix: keep top-level frontmatter minimal and move extra metadata under `metadata`.
- `package_skill.py` cannot import its helpers
  - Likely cause: it was run from the wrong working directory.
  - Fix: run `python3 -m scripts.package_skill` from the `skill-creator` root.
- The converted bundle is bloated with unrelated generic skills
  - Likely cause: the source export mixed core domain skills with broad extras.
  - Fix: keep only the domain core plus the router when that matches the user’s goal.
- Python resource bundles look dirty after validation
  - Likely cause: `compileall` left `__pycache__`.
  - Fix: delete `__pycache__` before final packaging.
- The user still asks what the installed bundle can do
  - Likely cause: the run stopped at file conversion.
  - Fix: always end with a router-plus-children capability summary.

## Verification checklist

1. Every installed skill directory has a valid `SKILL.md`.
2. Top-level frontmatter is Codex-compatible and names match folders.
3. Multi-skill bundles have a clear router skill.
4. Validation passed before packaging or install.
5. If packaging was requested, the archives contain `skill-name/SKILL.md`.
6. If install was requested, the validated skills exist under `~/.codex/skills/`.
7. The final handoff explains what the router and child skills do.

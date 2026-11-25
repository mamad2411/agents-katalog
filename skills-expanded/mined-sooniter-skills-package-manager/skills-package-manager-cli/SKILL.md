---
name: skills-package-manager-cli
description: Help users work in repositories that use skills-package-manager. Use when requests mention `skills.json`, `selfSkill`, `npx skills-package-manager init`, `add`, `install`, `update`, skill specifiers, install directories like `.agents/skills`, or linked skill directories like `.claude/skills`
---

# skills-package-manager

Use this skill for repositories that already use `skills-package-manager`, or when a user needs help understanding and editing its manifest and CLI workflow.

## Core Model

- `skills.json` is the source of truth.
  It declares which skills a repo wants, the pinned git commits or npm versions to use, where to materialize skills, where to link them, and whether to include the bundled helper skill.
- Installed directories such as `.agents/skills` and linked directories such as `.claude/skills` are outputs.
  They are produced from `skills.json`; they are not canonical config.

## What `selfSkill` Means

- `selfSkill: true` adds the bundled `skills-package-manager-cli` skill during install.
- The bundled skill is injected at runtime. It should not be added manually under `skills` unless there is a very specific reason.

## Command Guide

1. `npx skills-package-manager init`
   - Creates `skills.json`.
   - `npx skills-package-manager init --yes` writes the default manifest immediately.

2. `npx skills-package-manager add <specifier> [--skill <name>...]`
   - Adds a skill to `skills.json`.
   - Resolves remote git/npm inputs into pinned specifiers in the manifest.
   - GitHub shorthand, GitHub URL, and GitHub tree URL inputs are written back as `github:owner/repo#<commit>&path:<path>`.
   - Compatible with common `npx skills add` flags: `-s/--skill` can repeat, `-l/--list` lists without installing, `--all` selects all skills and all known project agents, `-a/--agent` can repeat, and `--copy` is accepted as a no-op compatibility flag.
   - Installs it into `installDir` and links it into each `linkTarget`.

3. `npx skills-package-manager install`
   - Resolves and installs everything declared in `skills.json`.
   - Does not write a separate lock file.

4. `npx skills-package-manager update [skill...]`
   - Updates git skills to the latest `main` commit and npm skills to the registry `latest` version.
   - Writes updated pins back to `skills.json` only after install succeeds.
   - Skips `link:`, `local:`, and `file:` skills.

## How To Triage User Questions

1. If the user wants to change which skills a repo uses:
   Edit `skills.json`, then run `npx skills-package-manager install`.

2. If the user wants newer remote skills:
   Run `npx skills-package-manager update` or update the pinned specifier in `skills.json`.

3. If the user says a skill is missing in their agent:
   Check `installDir`, `linkTargets`, generated skill directories, and symlinks.

4. If the user is confused about `selfSkill`:
   Explain that it enables the bundled `skills-package-manager-cli` helper skill, not an arbitrary repo-local skill.

## Specifier Reminders

- `github:owner/repo#commit&path:/skills/name` points to a pinned GitHub skill.
- `link:./path/to/skill-dir` points to a local skill directory and is symlinked into `installDir`.
- `local:*` keeps an existing user-owned skill at `${installDir}/${skillName}` in place.
- `local:./path/to/existing-skill-dir` keeps an existing user-owned skill directory in place.
- `file:./pkg.tgz&path:/skills/name` points to a packaged tarball plus skill path.
- `npm:@scope/pkg@1.0.0&path:/skills/name` resolves a package from the configured registry.

## Validation Checklist

- Keep `manifest`, `installDir`, `linkTargets`, `skills`, and `specifier` terminology exact.
- Treat `skills.json` as the only user-maintained config file.
- If you change this bundled skill inside the `skills-package-manager` repo, revalidate the skill folder.

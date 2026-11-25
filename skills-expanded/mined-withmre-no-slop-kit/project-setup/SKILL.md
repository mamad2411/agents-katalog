---
name: project-setup
description: Create or update the current project's CLAUDE.md from my template, filled only with what the repository actually contains. Use when I ask to set up or initialize a project's CLAUDE.md.
disable-model-invocation: true
---

# Project setup

1. Read `template.md` in this skill's folder.
2. Gather facts cheaply. List the root, read `package.json` (or `pyproject.toml`, `composer.json`, `go.mod`), detect the package manager from the lockfile name without reading it, glance at framework, test and lint config files, and the first lines of the README. Don't read source files unless a section needs it.
3. Fill only what you verified. Commands: copy the exact script names. Add a quiet flag only after checking the tool supports it (`--help`). Anything unknown becomes `[À FOURNIR : ...]`.
4. Delete the template sections that don't apply. Target under 60 lines.
5. If a CLAUDE.md already exists, keep its content, fit it into the template structure and show me the diff. Never drop one of my lines without asking.
6. Write `CLAUDE.md` at the project root. Reply with the list of `[À FOURNIR]` markers, nothing else.

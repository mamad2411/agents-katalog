---
name: dangaiden-project-overview
description: Generate a concise overview of the current project — structure, purpose, recent activity, and open questions. Use when the user asks "what is this repo?", "give me an overview", or "what's going on in this project?".
argument-hint: "[focus area, e.g. 'backend' or 'recent changes']"
allowed-tools: Bash(git*) Bash(ls*) Bash(wc*) Read Grep Glob
---

# Project Overview

Produce a concise, human-readable summary of this project for someone new to the codebase.

## Steps

1. **Identity**: Read `README.md` (if present) for the stated purpose. If absent, infer from directory names and key files.

2. **Structure**: List top-level directories and files. Note the dominant language(s) and any obvious architecture layers (frontend, backend, infra, tests, docs).

3. **Recent activity**: Run `git log --oneline -10` to show the last 10 commits. Summarize what areas have been changing.

4. **Open work**: Look for `TODO`, `FIXME`, or `HACK` comments with `grep -r "TODO\|FIXME\|HACK" --include="*.md" .` and note how many exist.

5. **Key entry points**: Identify the main entrypoint files (e.g. `main.*`, `index.*`, `app.*`, `Makefile`, `package.json`, `Cargo.toml`).

If `$ARGUMENTS` is provided, focus the overview on that area or topic instead of the whole project.

## Output format

- **Purpose**: one sentence
- **Stack**: languages, frameworks, key dependencies
- **Structure**: bullet list of top-level dirs with one-line descriptions
- **Recent activity**: what's been changing (based on git log)
- **Entry points**: files to start reading
- **Open items**: count of TODOs/FIXMEs, any that look urgent

Keep the output under 30 lines. Prioritize clarity over completeness.

---
name: pbip-scaffold
description: Initialize a Power BI PBIP project repository with best-practice .gitignore, data dictionary, changelog, and README. Use when the user says "set up this Power BI project", "scaffold PBIP", "initialize PBIP repo", "create PBIP config", or when you detect a PBIP project without proper git setup. Also triggers on /pbip-scaffold.
argument-hint: [project-path]
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob]
---

# /pbip-scaffold

Set up a Power BI PBIP project directory with all the scaffolding needed for clean version control and documentation.

Arguments: $ARGUMENTS

If no path is provided, use the current working directory. If a path is given, use that.

## Step 1: Find the PBIP project

Look for `.pbip` files in the target directory:
```bash
find <target-dir> -maxdepth 2 -name "*.pbip" 2>/dev/null
```

If none found, tell the user this doesn't appear to be a PBIP project. If multiple found, list them and ask which one to scaffold (or do all).

The project root is the directory containing the `.pbip` file.

## Step 2: Create .gitignore

Read `references/gitignore-template.md` for the comprehensive template. Write it to `<project-root>/.gitignore`.

If a `.gitignore` already exists, merge the PBIP-specific patterns into it rather than overwriting. Check each pattern — only add what's missing.

## Step 3: Check for tracked .pbi/ files

If git is already initialized, check if `.pbi/` cache files are tracked:
```bash
git ls-files --cached '**/.pbi/*' 2>/dev/null
```

If any are tracked, warn the user and offer to remove them from tracking:
```bash
git rm --cached -r '**/.pbi/' 2>/dev/null
```

This removes them from git without deleting the local files.

## Step 4: Create CHANGELOG.md

If `CHANGELOG.md` doesn't exist, create it with this template:

```markdown
# Changelog

All notable changes to this Power BI project are documented here.
Format: append-only, grouped by date and session.

---
```

## Step 5: Generate initial data-dictionary.md

If `.SemanticModel/definition/tables/` exists with `.tmdl` files, generate an initial data dictionary. Follow the same process as the `data-dictionary` skill:
- Parse all table TMDL files
- Extract tables, columns, measures, relationships
- Skip `LocalDateTable_*` and `DateTableTemplate_*`
- Write to `data-dictionary.md`

If no TMDL files exist yet, create an empty template:

```markdown
# Data Dictionary

*Auto-generated from TMDL model definitions. Run `/data-dictionary` to refresh.*

No semantic model found yet. This file will be populated when TMDL files are added.
```

## Step 6: Create README.md

If `README.md` doesn't exist, create one with:

```markdown
# <Project Name>

Power BI PBIP project.

## Structure

See `references/folder-structure.md` in the newna-powerbi plugin for what each directory contains.

## Files

- `data-dictionary.md` — Auto-maintained model dictionary (tables, columns, measures, relationships)
- `CHANGELOG.md` — Append-only history of model changes

## Development

This project uses the newna-powerbi Claude Code plugin for automated:
- Cache cleanup (`.pbi/` files are never committed)
- Data dictionary updates after model changes
- Changelog entries at natural stopping points
```

Replace `<Project Name>` with the name from the `.pbip` file.

## Step 7: Initialize git

Delegate to the `git-autopilot` skill from the `newna-mcp` plugin. It will:
- Initialize git if not already done
- Set user identity
- Make an initial commit

## Step 8: Report

Tell the user what was created/updated:
- .gitignore (new or updated)
- CHANGELOG.md
- data-dictionary.md
- README.md
- Whether any .pbi/ files were untracked
- Git status

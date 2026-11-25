---
name: biolab-project
description: "Use when listing projects, viewing project details by slug, or delegating to a project-specific skill (e.g. biolab-tashan). Do not invent project commands — follow the target project's skill."
metadata:
  requires:
    bins: ["biolab"]
  cliHelp: "biolab project --help"
---

# Biolab Project Workflows

**Before starting, read `../biolab-shared/SKILL.md` for auth, safety, and OpenAPI rules.**

This skill covers generic project administration. For project-specific workflows (germplasm, planting, etc.), use the corresponding `biolab-<project>` skill.

## Project Administration

```bash
biolab projects list -f json
biolab projects get <PROJECT_ID> -f json
biolab projects create '<JSON>' -f json
biolab projects update <PROJECT_ID> '<JSON>' -f json
biolab projects delete <PROJECT_ID> -f json
```

## Project by Slug

```bash
biolab project <SLUG> info -f json
```

Use the `slug` field from `projects list` to identify the project, then check its dedicated skill (e.g. `biolab-tashan`) for available workflow commands.

## Rules

- Do not invent commands — check `biolab project <SLUG> --help` or the project-specific skill.
- Prefer `-f json` for machine-parsable output.
- Confirm before creating, updating, or deleting project records.
- For project-specific workflows (germplasm, planting, etc.), delegate to the corresponding `biolab-<project>` skill.

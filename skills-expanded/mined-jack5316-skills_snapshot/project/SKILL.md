---
name: project
description: Track ongoing personal projects in the Obsidian vault. Use when user asks to create a project, track projects, list projects, log project progress, or /project.
---

# Project Tracking Skill

Creates and tracks personal projects in `01 - Projects/`. Uses the vault's Project Note structure: Desired Outcome, Why This Matters, Next Actions, Tasks, Log. Links to [[AI Projects MOC]].

## Usage

```bash
# Create new project
python3 _scripts/project_track.py create "Project Name" [--desc "Brief description"] [--due YYYY-MM-DD]

# List active projects
python3 _scripts/project_track.py list [--all]

# Log progress to existing project
python3 _scripts/project_track.py log "Project Name" "What you did"
```

- **create**: Creates a project note. AI fleshes out Desired Outcome, Why This Matters, Next Actions from the description.
- **list**: Lists projects in `01 - Projects/`. Use `--all` to include inactive.
- **log**: Appends a dated log entry to an existing project (partial name match).

## Output

New projects go to `01 - Projects/{Project Name}.md` with:

- **Desired Outcome** — What "done" looks like (AI-generated)
- **Why This Matters** — Motivation (AI-generated)
- **Next Actions** — Initial steps (AI-generated)
- **Tasks** — High-level tasks
- **Resources & Links** — References
- **Log** — Dated progress entries
- **Related** — Link to [[AI Projects MOC]]

Uses `[[wikilinks]]` for Obsidian interconnection. YAML frontmatter: `status`, `due`, `tags`.

## Agent workflow

When user says "/project" or "track this project" or "create project":

1. **Create**: Run `create` with project name and optional description
2. **List**: Run `list` to show active projects
3. **Log**: Run `log` with project name and progress note

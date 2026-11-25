---
description: "GitLab Scrum management - create/manage issues, labels, milestones, and boards. Use when user says: create issue, list issues, move issue, add label, scrum, kanban, backlog, or task tracking."
---

# GitLab Scrum

Manage GitLab issues, labels, milestones, and boards via `glab` CLI for Scrum/Kanban workflows.

## Prerequisites

```bash
which glab  # Must be installed
glab auth status  # Must be authenticated
```

## Quick Reference

### Issues

```bash
# Create issue
glab issue create --title "Title" --description "Body" --label "To Do" --milestone "Sprint Name"

# List issues
glab issue list                          # Open issues
glab issue list --milestone "Sprint X"   # By sprint
glab issue list --label "Doing"          # By status
glab issue list --assignee @me           # My issues

# Update issue
glab issue update <ID> --label "Doing" --unlabel "To Do"  # Move on board
glab issue update <ID> --assignee "username"                # Assign
glab issue update <ID> --milestone "Sprint X"               # Set sprint

# Close / reopen
glab issue close <ID>
glab issue reopen <ID>

# Comment
glab issue note <ID> --message "Comment text"

# View
glab issue view <ID>
glab issue view <ID> --web  # Open in browser
```

### Labels (Board Columns)

```bash
# Scrum labels (create once)
glab label create --name "To Do" --color "#F0AD4E"
glab label create --name "Doing" --color "#5CB85C"
glab label create --name "Review" --color "#0033CC"
glab label create --name "Done" --color "#69D100"

# List labels
glab label list
```

### Milestones (Sprints)

```bash
# Create sprint
glab milestone create --project <project-path> --title "Sprint 2026-W13" \
  --description "Goals..." --due-date "2026-03-28"

# List sprints
glab milestone list --project <project-path>

# Close sprint
glab api "projects/<encoded-path>/milestones/<ID>" --method PUT --field "state_event=close"
```

NOTE: `--project` flag is REQUIRED for milestone commands. Get project path from `git remote get-url origin`, strip the hostname and .git suffix. Example: `iclass/mdm/node-mdm-go`

### Boards (via API)

```bash
# Boards require glab api (no native CLI commands)
PROJECT_PATH=$(git remote get-url origin | sed -E 's|.*://[^/]+/||;s|\.git$||' | sed 's|/|%2F|g')

# Create board
glab api "projects/${PROJECT_PATH}/boards" --method POST --field "name=Scrum Board"

# List boards
glab api "projects/${PROJECT_PATH}/boards"

# Add label list to board (need label ID from `glab label list`)
glab api "projects/${PROJECT_PATH}/boards/<BOARD_ID>/lists" --method POST --field "label_id=<LABEL_ID>"
```

### Wiki

```bash
PROJECT_PATH=$(git remote get-url origin | sed -E 's|.*://[^/]+/||;s|\.git$||' | sed 's|/|%2F|g')

# Create wiki page
glab api "projects/${PROJECT_PATH}/wikis" --method POST \
  --field "title=Page Title" \
  --field "content=# Markdown content"

# List wiki pages
glab api "projects/${PROJECT_PATH}/wikis"

# Update wiki page
glab api "projects/${PROJECT_PATH}/wikis/<slug>" --method PUT \
  --field "content=# Updated content"

# Delete wiki page
glab api "projects/${PROJECT_PATH}/wikis/<slug>" --method DELETE
```

## Scrum Workflow

### Moving issues across board:
1. **To Do** → **Doing**: `glab issue update <ID> --label "Doing" --unlabel "To Do"`
2. **Doing** → **Review**: `glab issue update <ID> --label "Review" --unlabel "Doing"`
3. **Review** → **Done**: `glab issue update <ID> --label "Done" --unlabel "Review"` then `glab issue close <ID>`

### Creating a full sprint:
1. Create milestone (sprint)
2. Create issues with `--milestone` and `--label "To Do"`
3. Move issues through labels as work progresses
4. Close milestone when sprint ends

## Error Handling

- If `glab` not found: tell user to install via `brew install glab`
- If not authenticated: tell user to run `glab auth login`
- If not in git repo: tell user to `cd` to a git repo
- Milestone commands need `--project` flag
- Labels use `--name` flag (not positional argument)
- Wiki and boards use `glab api` with URL-encoded project path

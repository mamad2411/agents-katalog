---
description: "Manage GitLab issue boards - create boards, add columns, move issues between columns. Use when user says: board, kanban, move issue, board setup, columns."
---

# GitLab Board Management

Create and manage issue boards via `glab api`.

## Setup Board

Boards use `glab api` (no native CLI). Always get the project path first:

```bash
PROJECT_PATH=$(git remote get-url origin | sed -E 's|.*://[^/]+/||;s|\.git$||' | sed 's|/|%2F|g')
```

### Create Scrum Labels

```bash
glab label create --name "To Do" --color "#F0AD4E" --description "Backlog / ready for work"
glab label create --name "Doing" --color "#5CB85C" --description "In progress"
glab label create --name "Review" --color "#0033CC" --description "In code review"
glab label create --name "Done" --color "#69D100" --description "Completed"
```

### Create Board

```bash
glab api "projects/${PROJECT_PATH}/boards" --method POST --field "name=Scrum Board"
```

### Add Label Columns to Board

Get label IDs first:
```bash
glab label list
```

Then add each label as a board list:
```bash
BOARD_ID=<from board creation>
glab api "projects/${PROJECT_PATH}/boards/${BOARD_ID}/lists" --method POST --field "label_id=<TO_DO_ID>"
glab api "projects/${PROJECT_PATH}/boards/${BOARD_ID}/lists" --method POST --field "label_id=<DOING_ID>"
glab api "projects/${PROJECT_PATH}/boards/${BOARD_ID}/lists" --method POST --field "label_id=<REVIEW_ID>"
glab api "projects/${PROJECT_PATH}/boards/${BOARD_ID}/lists" --method POST --field "label_id=<DONE_ID>"
```

## View Board

```bash
# List boards
glab api "projects/${PROJECT_PATH}/boards" | python3 -c "
import sys,json
for b in json.load(sys.stdin):
    print(f'Board: {b[\"name\"]} (ID: {b[\"id\"]})')
    for l in b.get('lists',[]):
        label = l.get('label',{})
        print(f'  [{l[\"position\"]}] {label.get(\"name\",\"?\")} (list_id: {l[\"id\"]})')
"

# View board in browser
glab repo view --web  # then navigate to Issues > Boards
```

## Move Issues on Board

Moving an issue between columns = swapping labels:

```bash
# To Do → Doing
glab issue update <ID> --label "Doing" --unlabel "To Do"

# Doing → Review
glab issue update <ID> --label "Review" --unlabel "Doing"

# Review → Done
glab issue update <ID> --label "Done" --unlabel "Review"
glab issue close <ID>
```

## Board Summary

```bash
PROJECT_PATH=$(git remote get-url origin | sed -E 's|.*://[^/]+/||;s|\.git$||' | sed 's|/|%2F|g')
for label in "To Do" "Doing" "Review" "Done"; do
  count=$(glab api "projects/${PROJECT_PATH}/issues?labels=${label}&state=opened&per_page=100" 2>/dev/null | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo 0)
  printf "%-10s %s issues\n" "$label" "$count"
done
```

## Delete Board

```bash
glab api "projects/${PROJECT_PATH}/boards/${BOARD_ID}" --method DELETE
```

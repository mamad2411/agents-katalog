---
description: "Plan and manage GitLab sprints - create sprint milestones, populate with issues from backlog, track progress, close sprints. Use when user says: sprint, sprint planning, new sprint, close sprint, sprint review."
---

# GitLab Sprint Management

Create, plan, and manage sprints using GitLab milestones.

## Sprint Planning

When the user asks to plan a sprint:

1. **Get project path** (required for milestones):
```bash
PROJECT_SLUG=$(git remote get-url origin | sed -E 's|.*://[^/]+/||;s|\.git$||')
```

2. **Create the sprint milestone**:
```bash
glab milestone create --project "$PROJECT_SLUG" \
  --title "Sprint YYYY-WNN" \
  --description "Sprint goals:\n- Goal 1\n- Goal 2" \
  --due-date "YYYY-MM-DD"
```

3. **Create sprint issues** with milestone:
```bash
glab issue create --title "Task title" \
  --description "Description" \
  --label "To Do" \
  --milestone "Sprint YYYY-WNN"
```

4. **Create sprint wiki page** for notes/retrospective:
```bash
PROJECT_PATH=$(echo "$PROJECT_SLUG" | sed 's|/|%2F|g')
glab api "projects/${PROJECT_PATH}/wikis" --method POST \
  --field "title=Sprint-YYYY-WNN" \
  --field "content=# Sprint YYYY-WNN\n\n## Goals\n- [ ] Goal 1\n\n## Notes\n\n## Retrospective\n"
```

## Sprint Progress

```bash
# All sprint issues
glab issue list --milestone "Sprint YYYY-WNN"

# Sprint issues by status
glab issue list --milestone "Sprint YYYY-WNN" --label "To Do"
glab issue list --milestone "Sprint YYYY-WNN" --label "Doing"
glab issue list --milestone "Sprint YYYY-WNN" --label "Done"

# Count (via API)
PROJECT_PATH=$(git remote get-url origin | sed -E 's|.*://[^/]+/||;s|\.git$||' | sed 's|/|%2F|g')
glab api "projects/${PROJECT_PATH}/milestones?title=Sprint+YYYY-WNN" | python3 -c "
import sys,json
ms = json.load(sys.stdin)
if ms:
    m = ms[0]
    print(f'Sprint: {m[\"title\"]}')
    print(f'Due: {m.get(\"due_date\",\"not set\")}')
    print(f'State: {m[\"state\"]}')
"
```

## Close Sprint

```bash
# Close all done issues
glab issue list --milestone "Sprint YYYY-WNN" --label "Done" | grep '#' | awk '{print $1}' | sed 's/#//' | while read id; do
  glab issue close "$id"
done

# Close milestone
PROJECT_PATH=$(git remote get-url origin | sed -E 's|.*://[^/]+/||;s|\.git$||' | sed 's|/|%2F|g')
MILESTONE_ID=$(glab api "projects/${PROJECT_PATH}/milestones?title=Sprint+YYYY-WNN" | python3 -c "import sys,json; ms=json.load(sys.stdin); print(ms[0]['id'] if ms else '')")
glab api "projects/${PROJECT_PATH}/milestones/${MILESTONE_ID}" --method PUT --field "state_event=close"

# Move unfinished issues to next sprint
glab issue list --milestone "Sprint YYYY-WNN" --opened | grep '#' | awk '{print $1}' | sed 's/#//' | while read id; do
  glab issue update "$id" --milestone "Sprint YYYY-WNN+1"
done
```

## Sprint Naming Convention

Use ISO week format: `Sprint YYYY-WNN` (e.g., `Sprint 2026-W13`)
- 1-week sprints: `Sprint 2026-W13`
- 2-week sprints: `Sprint 2026-W13-W14`

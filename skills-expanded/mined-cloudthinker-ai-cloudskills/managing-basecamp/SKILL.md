---
name: managing-basecamp
description: |
  Use when working with Basecamp — basecamp project management covering
  projects, to-do lists, messages, schedules, and team activity. Use when
  auditing Basecamp usage, managing to-dos and message boards, analyzing project
  activity, or reviewing team workload across Basecamp projects.
connection_type: basecamp
preload: false
---

# Managing Basecamp

Basecamp project management analysis via the Basecamp REST API.

## Discovery Phase

```bash
#!/bin/bash
BC_BASE="https://3.basecampapi.com/$BASECAMP_ACCOUNT_ID"

echo "=== Current User ==="
curl -s -H "Authorization: Bearer $BASECAMP_TOKEN" \
  "https://launchpad.37signals.com/authorization.json" \
  | jq '{identity: .identity, accounts: [.accounts[] | {id, name, product}]}'

echo ""
echo "=== Projects ==="
curl -s -H "Authorization: Bearer $BASECAMP_TOKEN" \
  "$BC_BASE/projects.json" \
  | jq -r '.[] | "\(.id)\t\(.name[0:30])\t\(.status)\t\(.updated_at[0:10])"' | column -t

echo ""
echo "=== People ==="
curl -s -H "Authorization: Bearer $BASECAMP_TOKEN" \
  "$BC_BASE/people.json" \
  | jq -r '.[] | "\(.id)\t\(.name)\t\(.email_address)\t\(.admin)"' | column -t | head -20

echo ""
echo "=== Project Tools (first project) ==="
FIRST_PROJECT=$(curl -s -H "Authorization: Bearer $BASECAMP_TOKEN" \
  "$BC_BASE/projects.json" | jq -r '.[0].id')
curl -s -H "Authorization: Bearer $BASECAMP_TOKEN" \
  "$BC_BASE/projects/$FIRST_PROJECT.json" \
  | jq -r '.dock[] | "\(.name)\t\(.title)\tenabled=\(.enabled)"' | column -t
```

## Analysis Phase

```bash
#!/bin/bash
BC_BASE="https://3.basecampapi.com/$BASECAMP_ACCOUNT_ID"
PROJECT_ID="${1:?Project ID required}"

echo "=== To-Do Lists ==="
TODOSET_ID=$(curl -s -H "Authorization: Bearer $BASECAMP_TOKEN" \
  "$BC_BASE/projects/$PROJECT_ID.json" | jq -r '.dock[] | select(.name == "todoset") | .id')
curl -s -H "Authorization: Bearer $BASECAMP_TOKEN" \
  "$BC_BASE/buckets/$PROJECT_ID/todosets/$TODOSET_ID/todolists.json" \
  | jq -r '.[] | "\(.id)\t\(.title[0:30])\tcompleted=\(.completed_ratio)"' | column -t

echo ""
echo "=== Recent Messages ==="
MSGBOARD_ID=$(curl -s -H "Authorization: Bearer $BASECAMP_TOKEN" \
  "$BC_BASE/projects/$PROJECT_ID.json" | jq -r '.dock[] | select(.name == "message_board") | .id')
curl -s -H "Authorization: Bearer $BASECAMP_TOKEN" \
  "$BC_BASE/buckets/$PROJECT_ID/message_boards/$MSGBOARD_ID/messages.json" \
  | jq -r '.[:10][] | "\(.created_at[0:10])\t\(.creator.name)\t\(.subject[0:40])"' | column -t

echo ""
echo "=== Upcoming Schedule Entries ==="
SCHEDULE_ID=$(curl -s -H "Authorization: Bearer $BASECAMP_TOKEN" \
  "$BC_BASE/projects/$PROJECT_ID.json" | jq -r '.dock[] | select(.name == "schedule") | .id')
curl -s -H "Authorization: Bearer $BASECAMP_TOKEN" \
  "$BC_BASE/buckets/$PROJECT_ID/schedules/$SCHEDULE_ID/entries.json" \
  | jq -r '.[:10][] | "\(.starts_at[0:10])\t\(.title[0:30])\t\(.creator.name)"' | column -t

echo ""
echo "=== Campfire (recent chat) ==="
CAMPFIRE_ID=$(curl -s -H "Authorization: Bearer $BASECAMP_TOKEN" \
  "$BC_BASE/projects/$PROJECT_ID.json" | jq -r '.dock[] | select(.name == "chat") | .id')
curl -s -H "Authorization: Bearer $BASECAMP_TOKEN" \
  "$BC_BASE/buckets/$PROJECT_ID/chats/$CAMPFIRE_ID/lines.json" \
  | jq -r '.[-10:][] | "\(.created_at[0:16])\t\(.creator.name)\t\(.content[0:50])"' | column -t
```

## Output Format

```
BASECAMP PROJECT HEALTH: [project_name]
Status:        [status]
People:        [count]
Last Updated:  [date]

TO-DO LISTS
List                 Completed  Total
[title]              [n]        [n]

RECENT ACTIVITY
Date         Author       Type      Subject
[date]       [name]       message   [subject]
[date]       [name]       todo      [title]

SCHEDULE
Date         Event
[date]       [title]
```

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |


---
name: managing-height
description: |
  Use when working with Height — height.app project management covering tasks,
  lists, workspaces, and team activity analytics. Use when auditing Height
  workspace usage, managing tasks and lists, analyzing team workload, or
  reviewing project progress across a Height workspace.
connection_type: height
preload: false
---

# Managing Height

Height workspace management and analytics via the Height REST API.

## Discovery Phase

```bash
#!/bin/bash
HEIGHT_BASE="https://api.height.app"

echo "=== Workspace Info ==="
curl -s -H "Authorization: api-key $HEIGHT_API_KEY" \
  "$HEIGHT_BASE/workspace" | jq '{id, name, url}'

echo ""
echo "=== Lists ==="
curl -s -H "Authorization: api-key $HEIGHT_API_KEY" \
  "$HEIGHT_BASE/lists" \
  | jq -r '.list[] | "\(.id)\t\(.name[0:30])\t\(.type)\t\(.archivedAt // "active")"' | column -t

echo ""
echo "=== Users ==="
curl -s -H "Authorization: api-key $HEIGHT_API_KEY" \
  "$HEIGHT_BASE/users" \
  | jq -r '.list[] | "\(.id)\t\(.username)\t\(.email)\t\(.state)"' | column -t

echo ""
echo "=== Field Templates ==="
curl -s -H "Authorization: api-key $HEIGHT_API_KEY" \
  "$HEIGHT_BASE/fieldTemplates" \
  | jq -r '.list[]? | "\(.id)\t\(.name)\t\(.type)"' | column -t | head -15
```

## Analysis Phase

```bash
#!/bin/bash
HEIGHT_BASE="https://api.height.app"
LIST_ID="${1:?List ID required}"

echo "=== List Tasks ==="
curl -s -H "Authorization: api-key $HEIGHT_API_KEY" \
  "$HEIGHT_BASE/lists/$LIST_ID/tasks" \
  | jq -r '.list[] | "\(.index)\t\(.name[0:40])\t\(.status)\t\(.assigneesIds | length) assignees"' | column -t | head -25

echo ""
echo "=== Task Status Distribution ==="
curl -s -H "Authorization: api-key $HEIGHT_API_KEY" \
  "$HEIGHT_BASE/lists/$LIST_ID/tasks" \
  | jq '[.list[].status] | group_by(.) | map({status: .[0], count: length}) | sort_by(-.count)[]'

echo ""
echo "=== Unassigned Tasks ==="
curl -s -H "Authorization: api-key $HEIGHT_API_KEY" \
  "$HEIGHT_BASE/lists/$LIST_ID/tasks" \
  | jq '[.list[] | select(.assigneesIds | length == 0)] | {unassigned: length, tasks: [.[:5][] | {name: .name[0:40], status}]}'

echo ""
echo "=== Recent Activity ==="
curl -s -H "Authorization: api-key $HEIGHT_API_KEY" \
  "$HEIGHT_BASE/activities?listId=$LIST_ID" \
  | jq -r '.list[:10][] | "\(.createdAt[0:16])\t\(.type)\t\(.user.username // "system")"' | column -t
```

## Output Format

```
HEIGHT WORKSPACE HEALTH
Workspace:     [name]
Total Lists:   [count] ([active] active)
Total Users:   [count]

LIST HEALTH: [list_name]
Total Tasks:   [count]
Unassigned:    [count]

STATUS DISTRIBUTION
Status         Count   Pct
backLog        [n]     [pct]%
inProgress     [n]     [pct]%
done           [n]     [pct]%
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


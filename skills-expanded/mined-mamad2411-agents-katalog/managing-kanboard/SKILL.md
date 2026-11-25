---
name: managing-kanboard
description: |
  Use when working with Kanboard — kanboard project management covering
  projects, tasks, columns, swimlanes, and productivity analytics. Use when
  auditing Kanboard usage, managing tasks and projects, analyzing workflow
  throughput, or reviewing board health across a Kanboard instance.
connection_type: kanboard
preload: false
---

# Managing Kanboard

Kanboard project management analysis via the Kanboard JSON-RPC API.

## Discovery Phase

```bash
#!/bin/bash
KANBOARD_BASE="${KANBOARD_URL}/jsonrpc.php"

kb_rpc() {
  local method="$1"
  local params="${2:-{}}"
  curl -s -u "$KANBOARD_USER:$KANBOARD_TOKEN" \
    -H "Content-Type: application/json" \
    -X POST "$KANBOARD_BASE" \
    -d "{\"jsonrpc\": \"2.0\", \"method\": \"$method\", \"id\": 1, \"params\": $params}"
}

echo "=== Current User ==="
kb_rpc "getMe" | jq '.result | {id, username, name, email, role}'

echo ""
echo "=== Projects ==="
kb_rpc "getAllProjects" \
  | jq -r '.result[] | "\(.id)\t\(.name[0:30])\t\(.is_active)\tlast_modified=\(.last_modified)"' | column -t

echo ""
PROJECT_ID="${1:?Project ID required}"
echo "=== Columns ==="
kb_rpc "getColumns" "{\"project_id\": $PROJECT_ID}" \
  | jq -r '.result[] | "\(.id)\t\(.title)\tposition=\(.position)\ttask_limit=\(.task_limit)"' | column -t

echo ""
echo "=== Swimlanes ==="
kb_rpc "getActiveSwimlanes" "{\"project_id\": $PROJECT_ID}" \
  | jq -r '.result[] | "\(.id)\t\(.name)"' | column -t

echo ""
echo "=== Categories ==="
kb_rpc "getAllCategories" "{\"project_id\": $PROJECT_ID}" \
  | jq -r '.result[]? | "\(.id)\t\(.name)"' | column -t

echo ""
echo "=== Project Members ==="
kb_rpc "getProjectUsers" "{\"project_id\": $PROJECT_ID}" \
  | jq -r '.result | to_entries[] | "\(.key)\t\(.value)"' | column -t
```

## Analysis Phase

```bash
#!/bin/bash
KANBOARD_BASE="${KANBOARD_URL}/jsonrpc.php"
PROJECT_ID="${1:?Project ID required}"

kb_rpc() {
  curl -s -u "$KANBOARD_USER:$KANBOARD_TOKEN" \
    -H "Content-Type: application/json" \
    -X POST "$KANBOARD_BASE" \
    -d "{\"jsonrpc\": \"2.0\", \"method\": \"$1\", \"id\": 1, \"params\": ${2:-{}}}"
}

echo "=== Tasks by Column ==="
kb_rpc "getAllTasks" "{\"project_id\": $PROJECT_ID, \"status_id\": 1}" \
  | jq '[.result[] | .column_name] | group_by(.) | map({column: .[0], count: length}) | sort_by(-.count)[]'

echo ""
echo "=== Open Tasks ==="
kb_rpc "getAllTasks" "{\"project_id\": $PROJECT_ID, \"status_id\": 1}" \
  | jq -r '.result[:20][] | "\(.id)\t\(.title[0:35])\t\(.column_name)\t\(.assignee_name // "unassigned")\t\(.color_id)"' | column -t

echo ""
echo "=== Overdue Tasks ==="
kb_rpc "getOverdueTasks" \
  | jq -r '.result[] | select(.project_id == '$PROJECT_ID') | "\(.id)\t\(.title[0:35])\tdue=\(.date_due)\t\(.assignee_name // "unassigned")"' | column -t

echo ""
echo "=== Task Statistics ==="
OPEN=$(kb_rpc "getAllTasks" "{\"project_id\": $PROJECT_ID, \"status_id\": 1}" | jq '.result | length')
CLOSED=$(kb_rpc "getAllTasks" "{\"project_id\": $PROJECT_ID, \"status_id\": 0}" | jq '.result | length')
echo "Open: $OPEN  Closed: $CLOSED  Close Rate: $(echo "scale=1; $CLOSED * 100 / ($OPEN + $CLOSED)" | bc)%"

echo ""
echo "=== Unassigned Tasks ==="
kb_rpc "getAllTasks" "{\"project_id\": $PROJECT_ID, \"status_id\": 1}" \
  | jq '[.result[] | select(.owner_id == "0" or .owner_id == 0)] | {unassigned: length}'
```

## Output Format

```
KANBOARD PROJECT HEALTH: [project_name]
Open Tasks:      [count]
Closed Tasks:    [count]
Close Rate:      [pct]%
Overdue:         [count]

COLUMN DISTRIBUTION
Column           Tasks  WIP Limit
Backlog          [n]    [limit]
Ready            [n]    [limit]
Work in Progress [n]    [limit]
Done             [n]    [limit]

HEALTH INDICATORS
Unassigned Tasks:   [count]
Overdue Tasks:      [count]
Over WIP Limit:     [count] columns
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


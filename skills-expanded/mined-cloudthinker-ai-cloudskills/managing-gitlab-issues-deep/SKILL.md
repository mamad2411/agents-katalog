---
name: managing-gitlab-issues-deep
description: |
  Use when working with Gitlab Issues Deep — deep GitLab Issues management
  covering issue tracking, label analytics, milestone progress, assignee
  workload, and issue lifecycle metrics. Use when performing deep audits of
  GitLab Issues, analyzing issue resolution times, reviewing board health, or
  assessing contributor workload across GitLab projects.
connection_type: gitlab
preload: false
---

# Managing GitLab Issues (Deep)

Deep GitLab Issues analysis covering lifecycle metrics, board health, and contributor workload via the GitLab REST API.

## Discovery Phase

```bash
#!/bin/bash
GITLAB_BASE="${GITLAB_URL:-https://gitlab.com}/api/v4"
PROJECT_ID="${1:?Project ID or URL-encoded path required}"

echo "=== Project Info ==="
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_BASE/projects/$PROJECT_ID" \
  | jq '{id, path_with_namespace, open_issues_count, default_branch}'

echo ""
echo "=== Open Issues (latest 25) ==="
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_BASE/projects/$PROJECT_ID/issues?state=opened&per_page=25&order_by=updated_at" \
  | jq -r '.[] | "#\(.iid)\t\(.title[0:40])\t\(.author.username)\t\(.labels | join(","))\t\(.assignees | map(.username) | join(",") // "unassigned")"' \
  | column -t

echo ""
echo "=== Labels ==="
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_BASE/projects/$PROJECT_ID/labels?per_page=30" \
  | jq -r '.[] | "\(.name)\t\(.open_issues_count) open\t\(.closed_issues_count) closed"' | column -t

echo ""
echo "=== Milestones ==="
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_BASE/projects/$PROJECT_ID/milestones?state=active&per_page=10" \
  | jq -r '.[] | "\(.title[0:30])\topen=\(.open_issues_count // 0)\tclosed=\(.closed_issues_count // 0)\tdue=\(.due_date // "none")"' | column -t

echo ""
echo "=== Issue Boards ==="
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_BASE/projects/$PROJECT_ID/boards?per_page=5" \
  | jq -r '.[] | "\(.id)\t\(.name // "default")\tlists=\(.lists | length)"'
```

## Analysis Phase

```bash
#!/bin/bash
GITLAB_BASE="${GITLAB_URL:-https://gitlab.com}/api/v4"
PROJECT_ID="${1:?Project ID required}"

echo "=== Issue Statistics ==="
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_BASE/projects/$PROJECT_ID/issues_statistics" \
  | jq '.statistics.counts'

echo ""
echo "=== Unassigned Open Issues ==="
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_BASE/projects/$PROJECT_ID/issues?state=opened&assignee_id=None&per_page=1" \
  -I | grep -i 'x-total:' | awk '{print "Unassigned open:", $2}'

echo ""
echo "=== Issues by Label ==="
for LABEL in bug feature documentation; do
  COUNT=$(curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB_BASE/projects/$PROJECT_ID/issues?state=opened&labels=$LABEL&per_page=1" \
    -I | grep -i 'x-total:' | awk '{print $2}')
  echo -e "$LABEL\t${COUNT:-0} open"
done | column -t

echo ""
echo "=== Overdue Issues ==="
TODAY=$(date +%Y-%m-%d)
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_BASE/projects/$PROJECT_ID/issues?state=opened&due_date=overdue&per_page=10" \
  | jq -r '.[] | "#\(.iid)\t\(.title[0:40])\tdue=\(.due_date)\t\(.assignees | map(.username) | join(",") // "unassigned")"' | column -t

echo ""
echo "=== Recent Closed Issues (last 7 days) ==="
SINCE=$(date -v-7d -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d "-7 days" +%Y-%m-%dT%H:%M:%SZ)
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_BASE/projects/$PROJECT_ID/issues?state=closed&updated_after=$SINCE&per_page=15" \
  | jq -r '.[] | "#\(.iid)\t\(.title[0:40])\tclosed=\(.closed_at[0:10])"' | column -t
```

## Output Format

```
GITLAB ISSUES DEEP HEALTH: [project_path]
Open Issues:       [count]
Closed Issues:     [count]
Close Rate:        [pct]%
Unassigned Open:   [count]
Overdue:           [count]

ISSUES BY LABEL
Label              Open    Closed
bug                [n]     [n]
feature            [n]     [n]

MILESTONE PROGRESS
Milestone          Open  Closed  Due        Progress
[title]            [n]   [n]     [date]     [pct]%

BOARD HEALTH
Board              Lists  Issues
[name]             [n]    [n]
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


---
name: managing-github-issues-deep
description: |
  Use when working with Github Issues Deep — deep GitHub Issues management
  covering issue tracking, label analytics, milestone progress, assignee
  workload, and issue lifecycle metrics. Use when performing deep audits of
  GitHub Issues, analyzing issue resolution times, reviewing label health, or
  assessing contributor workload across GitHub repositories.
connection_type: github
preload: false
---

# Managing GitHub Issues (Deep)

Deep GitHub Issues analysis covering lifecycle metrics, label health, and contributor workload via the GitHub REST API.

## Discovery Phase

```bash
#!/bin/bash
GH_BASE="https://api.github.com"
OWNER="${1:?Owner/org required}"
REPO="${2:?Repo name required}"

echo "=== Repository Info ==="
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "$GH_BASE/repos/$OWNER/$REPO" \
  | jq '{full_name, open_issues_count, has_issues, default_branch}'

echo ""
echo "=== Open Issues (latest 25) ==="
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "$GH_BASE/repos/$OWNER/$REPO/issues?state=open&per_page=25&sort=updated" \
  | jq -r '.[] | select(.pull_request == null) | "\(. | "#\(.number)")\t\(.title[0:40])\t\(.user.login)\t\(.labels | map(.name) | join(","))\t\(.assignees | map(.login) | join(",") // "unassigned")"' \
  | column -t

echo ""
echo "=== Labels ==="
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "$GH_BASE/repos/$OWNER/$REPO/labels?per_page=50" \
  | jq -r '.[] | "\(.name)\t\(.description // "no description")"' | column -t

echo ""
echo "=== Milestones ==="
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "$GH_BASE/repos/$OWNER/$REPO/milestones?state=open&per_page=10" \
  | jq -r '.[] | "\(.title[0:30])\topen=\(.open_issues)\tclosed=\(.closed_issues)\tdue=\(.due_on[0:10] // "none")"' | column -t
```

## Analysis Phase

```bash
#!/bin/bash
GH_BASE="https://api.github.com"
OWNER="${1:?Owner required}"
REPO="${2:?Repo required}"

echo "=== Issue Counts ==="
OPEN=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "$GH_BASE/repos/$OWNER/$REPO/issues?state=open&per_page=1" -I | grep -i 'link:' | grep -o 'page=[0-9]*' | tail -1 | cut -d= -f2)
CLOSED=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "$GH_BASE/search/issues?q=repo:$OWNER/$REPO+type:issue+is:closed" | jq '.total_count')
echo "Open: ${OPEN:-N/A}  Closed: ${CLOSED:-N/A}"

echo ""
echo "=== Issues by Label ==="
for LABEL in bug enhancement "good first issue" documentation; do
  COUNT=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
    "$GH_BASE/search/issues?q=repo:$OWNER/$REPO+type:issue+is:open+label:\"$LABEL\"" | jq '.total_count')
  echo -e "$LABEL\t$COUNT open"
done | column -t

echo ""
echo "=== Unassigned Open Issues ==="
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "$GH_BASE/search/issues?q=repo:$OWNER/$REPO+type:issue+is:open+no:assignee" \
  | jq '{unassigned_open: .total_count}'

echo ""
echo "=== Stale Issues (no update in 90 days) ==="
STALE_DATE=$(date -v-90d +%Y-%m-%d 2>/dev/null || date -d "-90 days" +%Y-%m-%d)
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "$GH_BASE/search/issues?q=repo:$OWNER/$REPO+type:issue+is:open+updated:<$STALE_DATE&per_page=10" \
  | jq -r '.items[:10][] | "#\(.number)\t\(.title[0:40])\tupdated=\(.updated_at[0:10])"' | column -t

echo ""
echo "=== Top Issue Contributors ==="
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "$GH_BASE/repos/$OWNER/$REPO/issues?state=all&per_page=100&sort=created" \
  | jq -r '[.[] | select(.pull_request == null) | .user.login] | group_by(.) | map({user: .[0], count: length}) | sort_by(-.count)[:10][] | "\(.user)\t\(.count) issues"' | column -t
```

## Output Format

```
GITHUB ISSUES DEEP HEALTH: [owner/repo]
Open Issues:       [count]
Closed Issues:     [count]
Close Rate:        [pct]%
Unassigned Open:   [count]
Stale (90d+):      [count]

ISSUES BY LABEL
Label              Open    Closed
bug                [n]     [n]
enhancement        [n]     [n]

MILESTONE PROGRESS
Milestone          Open  Closed  Due        Progress
[title]            [n]   [n]     [date]     [pct]%

TOP CONTRIBUTORS
User               Issues Created
[login]            [count]
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


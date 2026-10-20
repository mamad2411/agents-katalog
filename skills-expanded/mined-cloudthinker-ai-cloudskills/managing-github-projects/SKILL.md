---
name: managing-github-projects
description: |
  Use when working with Github Projects — gitHub Projects (v2) management
  covering project boards, views, items, custom fields, and workflow analytics.
  Use when auditing GitHub Projects usage, managing project items and fields,
  analyzing project progress, or reviewing board health across GitHub Projects.
connection_type: github
preload: false
---

# Managing GitHub Projects

GitHub Projects (v2) management and analytics via the GitHub GraphQL API.

## Discovery Phase

```bash
#!/bin/bash
GH_GQL="https://api.github.com/graphql"

gql() {
  curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Content-Type: application/json" \
    -X POST "$GH_GQL" -d "{\"query\": $(echo "$1" | jq -Rs .)}"
}

echo "=== Current User ==="
gql '{ viewer { login name } }' | jq '.data.viewer'

echo ""
OWNER="${1:?Owner/org required}"
echo "=== Organization Projects ==="
gql "{
  organization(login: \"$OWNER\") {
    projectsV2(first: 20) {
      nodes { id number title closed updatedAt }
    }
  }
}" | jq -r '.data.organization.projectsV2.nodes[] | "\(.number)\t\(.title[0:35])\t\(if .closed then "closed" else "open" end)\t\(.updatedAt[0:10])"' | column -t

echo ""
echo "=== User Projects ==="
gql "{
  viewer {
    projectsV2(first: 10) {
      nodes { id number title closed updatedAt }
    }
  }
}" | jq -r '.data.viewer.projectsV2.nodes[]? | "\(.number)\t\(.title[0:35])\t\(if .closed then "closed" else "open" end)\t\(.updatedAt[0:10])"' | column -t
```

## Analysis Phase

```bash
#!/bin/bash
GH_GQL="https://api.github.com/graphql"
OWNER="${1:?Owner required}"
PROJECT_NUM="${2:?Project number required}"

gql() {
  curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Content-Type: application/json" \
    -X POST "$GH_GQL" -d "{\"query\": $(echo "$1" | jq -Rs .)}"
}

echo "=== Project Details ==="
gql "{
  organization(login: \"$OWNER\") {
    projectV2(number: $PROJECT_NUM) {
      title updatedAt
      items(first: 50) {
        totalCount
        nodes {
          type
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2SingleSelectField { name } } }
              ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2Field { name } } }
            }
          }
          content {
            ... on Issue { title state number }
            ... on PullRequest { title state number }
            ... on DraftIssue { title }
          }
        }
      }
      fields(first: 20) {
        nodes {
          ... on ProjectV2Field { name dataType }
          ... on ProjectV2SingleSelectField { name options { name } }
          ... on ProjectV2IterationField { name }
        }
      }
    }
  }
}" | jq '{
  title: .data.organization.projectV2.title,
  total_items: .data.organization.projectV2.items.totalCount,
  fields: [.data.organization.projectV2.fields.nodes[] | .name],
  items: [.data.organization.projectV2.items.nodes[:15][] | {
    type: .type,
    title: .content.title,
    state: .content.state,
    status: [.fieldValues.nodes[] | select(.field.name == "Status") | .name] | first
  }]
}'

echo ""
echo "=== Status Distribution ==="
gql "{
  organization(login: \"$OWNER\") {
    projectV2(number: $PROJECT_NUM) {
      items(first: 100) {
        nodes {
          fieldValues(first: 5) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2SingleSelectField { name } } }
            }
          }
        }
      }
    }
  }
}" | jq '[.data.organization.projectV2.items.nodes[].fieldValues.nodes[] | select(.field.name == "Status") | .name] | group_by(.) | map({status: .[0], count: length}) | sort_by(-.count)[]'
```

## Output Format

```
GITHUB PROJECT HEALTH: [title]
Owner:          [owner]
Total Items:    [count]
Custom Fields:  [list]

STATUS DISTRIBUTION
Status           Count   Pct
Todo             [n]     [pct]%
In Progress      [n]     [pct]%
Done             [n]     [pct]%

ITEMS
#     Title                State    Status
[n]   [title]              open     In Progress
[n]   [title]              closed   Done
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


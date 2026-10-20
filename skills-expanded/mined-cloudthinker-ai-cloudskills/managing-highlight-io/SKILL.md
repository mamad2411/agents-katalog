---
name: managing-highlight-io
description: |
  Use when working with Highlight Io — highlight.io full-stack observability
  platform for session replay, error monitoring, log management, and tracing.
  Covers error tracking, log querying, session analysis, trace investigation,
  and alert management. Use when investigating frontend errors, analyzing user
  sessions, searching application logs, or managing Highlight.io alert
  configurations.
connection_type: highlight-io
preload: false
---

# Highlight.io Monitoring Skill

Query, analyze, and manage Highlight.io observability data using the Highlight.io GraphQL API.

## API Overview

Highlight.io uses a GraphQL API at `https://pri.highlight.io`.

### Core Helper Function

```bash
#!/bin/bash

hl_gql() {
    local query="$1"
    curl -s -X POST "https://pri.highlight.io" \
        -H "Authorization: Bearer $HIGHLIGHT_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"query\": $(echo "$query" | jq -Rs .)}"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover projects and resource types before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Projects ==="
hl_gql '{
    projects {
        id name
    }
}' | jq -r '.data.projects[] | "\(.id)\t\(.name)"' | head -15

echo ""
echo "=== Error Groups (Recent) ==="
hl_gql '{
    error_groups(project_id: "'"$HIGHLIGHT_PROJECT_ID"'", count: 20, params: {date_range: {start_date: "'"$(date -d '24 hours ago' -Iseconds)"'", end_date: "'"$(date -Iseconds)"'"}}) {
        error_groups {
            id type event state
            structured_stack_trace { fileName lineNumber }
        }
        totalCount
    }
}' | jq -r '"Total errors: \(.data.error_groups.totalCount)\n" + (.data.error_groups.error_groups[] | "\(.id)\t\(.state)\t\(.event[0:60])")' | head -20

echo ""
echo "=== Alerts ==="
hl_gql '{
    alerts(project_id: "'"$HIGHLIGHT_PROJECT_ID"'") {
        id name type disabled
    }
}' | jq -r '.data.alerts[] | "\(.id)\t\(.disabled)\t\(.type)\t\(.name)"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Error Frequency (last 24h) ==="
hl_gql '{
    error_groups(project_id: "'"$HIGHLIGHT_PROJECT_ID"'", count: 15, params: {date_range: {start_date: "'"$(date -d '24 hours ago' -Iseconds)"'", end_date: "'"$(date -Iseconds)"'"}}) {
        error_groups { id event environments frequency }
    }
}' | jq -r '.data.error_groups.error_groups[] | "\(.frequency)\t\(.environments[0] // "unknown")\t\(.event[0:70])"' | sort -rn | head -15

echo ""
echo "=== Recent Logs ==="
hl_gql '{
    logs(project_id: "'"$HIGHLIGHT_PROJECT_ID"'", params: {date_range: {start_date: "'"$(date -d '1 hour ago' -Iseconds)"'", end_date: "'"$(date -Iseconds)"'"}, query: "level:error"}, count: 15) {
        edges {
            node { timestamp message level serviceName }
        }
    }
}' | jq -r '.data.logs.edges[] | "\(.node.timestamp[0:19])\t\(.node.level)\t\(.node.serviceName // "unknown")\t\(.node.message[0:60])"' | head -15

echo ""
echo "=== Session Count ==="
hl_gql '{
    sessions_count(project_id: "'"$HIGHLIGHT_PROJECT_ID"'", params: {date_range: {start_date: "'"$(date -d '24 hours ago' -Iseconds)"'", end_date: "'"$(date -Iseconds)"'"}})
}' | jq -r '"Sessions (24h): \(.data.sessions_count)"'
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `count` parameter in queries and `head` in output
- Use error_groups for aggregated error views before drilling into individual errors
- Filter logs with query parameter at API level

## Output Format

Present results as a structured report:
```
Managing Highlight Io Report
════════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

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


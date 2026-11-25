---
name: managing-fortify
description: |
  Use when working with Fortify — micro Focus Fortify application security
  testing for static analysis (SAST), dynamic analysis (DAST), and software
  security assurance. Covers SSC project management, scan result analysis, issue
  tracking, audit workflows, and report generation. Use when reviewing Fortify
  scan results, analyzing application vulnerabilities, managing audit trails, or
  tracking security issue remediation across projects.
connection_type: fortify
preload: false
---

# Fortify SSC Management Skill

Manage and analyze Fortify Software Security Center projects, issues, scan results, and audit workflows.

## API Conventions

### Authentication
All API calls use `Authorization: FortifyToken $FORTIFY_TOKEN` -- injected automatically. Never hardcode tokens.

### Base URL
`https://$FORTIFY_HOST/ssc/api/v1`

### Core Helper Function

```bash
#!/bin/bash

fortify_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    local base="https://${FORTIFY_HOST}/ssc/api/v1"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: FortifyToken $FORTIFY_TOKEN" \
            -H "Content-Type: application/json" \
            "${base}${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: FortifyToken $FORTIFY_TOKEN" \
            -H "Content-Type: application/json" \
            "${base}${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Never dump full API responses

## Discovery Phase

```bash
#!/bin/bash
echo "=== Project Versions ==="
fortify_api GET "/projectVersions?limit=100" \
    | jq '{total: .count, versions: [.data[:10][] | {project: .project.name, version: .name, active: .active}]}'

echo ""
echo "=== Scan Status ==="
fortify_api GET "/projectVersions?limit=10&orderby=currentAnalysisDatetime%20desc" \
    | jq -r '.data[] | "\(.currentAnalysisDatetime[0:16] // "Never")\t\(.project.name[0:25])\t\(.name)"' | column -t
```

## Analysis Phase

### Issue Overview

```bash
#!/bin/bash
VERSION_ID="${1:?Project version ID required}"

echo "=== Issue Summary ==="
fortify_api GET "/projectVersions/${VERSION_ID}/issueGroups?groupingtype=FOLDER&filterset=a243b195-0a59-3f8b-1403-d55b7a7d78e6" \
    | jq -r '.data[] | "\(.cleanName)\t\(.totalCount)\tvisible:\(.visibleCount)"' | column -t

echo ""
echo "=== Critical/High Issues ==="
fortify_api GET "/projectVersions/${VERSION_ID}/issues?limit=20&filter=friority:Critical,High&orderby=friority" \
    | jq -r '.data[] | "\(.friority)\t\(.issueName[0:30])\t\(.primaryLocation[0:40])\tline:\(.lineNumber)"' \
    | column -t | head -20

echo ""
echo "=== Issues by Category ==="
fortify_api GET "/projectVersions/${VERSION_ID}/issueGroups?groupingtype=CATEGORY" \
    | jq -r '.data[] | "\(.totalCount)\t\(.cleanName[0:50])"' | sort -rn | head -15 | column -t
```

### Audit Status

```bash
#!/bin/bash
VERSION_ID="${1:?Project version ID required}"

echo "=== Audit Progress ==="
fortify_api GET "/projectVersions/${VERSION_ID}/issues?limit=500&filter=audited:false" \
    | jq '"Unaudited issues: \(.count)"' -r

fortify_api GET "/projectVersions/${VERSION_ID}/issues?limit=500&filter=audited:true" \
    | jq '"Audited issues: \(.count)"' -r

echo ""
echo "=== Issues by Analysis Tag ==="
fortify_api GET "/projectVersions/${VERSION_ID}/issueGroups?groupingtype=ANALYSIS" \
    | jq -r '.data[] | "\(.cleanName)\t\(.totalCount)"' | column -t
```

### Scan History

```bash
#!/bin/bash
VERSION_ID="${1:?Project version ID required}"

echo "=== Scan Artifacts ==="
fortify_api GET "/projectVersions/${VERSION_ID}/artifacts?limit=10&orderby=uploadDate%20desc" \
    | jq -r '.data[] | "\(.uploadDate[0:16])\t\(.status)\t\(.artifactType)\tsize:\(.fileSize)"' | column -t

echo ""
echo "=== Performance Indicators ==="
fortify_api GET "/projectVersions/${VERSION_ID}/performanceIndicatorHistories" \
    | jq -r '.data[:5][] | "\(.performanceIndicator.name)\tvalue:\(.value)"' | column -t
```

## Output Format

Present results as a structured report:
```
Managing Fortify Report
═══════════════════════
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

## Common Pitfalls

- **Token types**: FortifyToken (unified) vs Basic auth -- check SSC version for supported methods
- **Filterset IDs**: Issue queries require filterset UUID -- default varies by SSC installation
- **Friority vs severity**: Fortify uses "friority" (Fortify Priority) combining impact and likelihood
- **Project version scope**: All issue queries are scoped to a project version ID
- **Pagination**: Use `limit` and `start` parameters -- check `.count` for total
- **Large FPR files**: Scan artifacts can be very large -- do not download full FPR via API

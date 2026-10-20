---
name: managing-burp-suite
description: |
  Use when working with Burp Suite — portSwigger Burp Suite Enterprise Edition
  for automated dynamic application security testing (DAST). Covers scan
  management, vulnerability findings, site configuration, scan scheduling, and
  issue reporting. Use when reviewing DAST scan results, analyzing web
  application vulnerabilities, managing scan schedules, or tracking remediation
  of web security issues.
connection_type: burp-suite
preload: false
---

# Burp Suite Enterprise Management Skill

Manage and analyze Burp Suite Enterprise scans, findings, sites, and scan configurations.

## API Conventions

### Authentication
All API calls use `Authorization: $BURP_API_KEY` -- injected automatically. Never hardcode keys.

### Base URL
`https://$BURP_HOST/api-$BURP_API_VERSION`

### Core Helper Function

```bash
#!/bin/bash

burp_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    local base="https://${BURP_HOST}/api-${BURP_API_VERSION:-v1}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: $BURP_API_KEY" \
            -H "Content-Type: application/json" \
            "${base}${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: $BURP_API_KEY" \
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
echo "=== Sites ==="
burp_api GET "/sites" \
    | jq '{total_sites: (.data | length), sites: [.data[:10][] | {id: .id, name: .name, url: .scope.included_urls[0]}]}'

echo ""
echo "=== Scan Configurations ==="
burp_api GET "/scan_configurations" \
    | jq -r '.data[:10][] | "\(.id)\t\(.name)"' | column -t

echo ""
echo "=== Agent Status ==="
burp_api GET "/agents" \
    | jq -r '.data[] | "\(.name)\t\(.state)\t\(.max_concurrent_scans) max scans"' | column -t | head -10
```

## Analysis Phase

### Scan Results Overview

```bash
#!/bin/bash
echo "=== Recent Scans ==="
burp_api GET "/scans?sort_by=start&sort_order=desc&limit=15" \
    | jq -r '.data[] | "\(.start[0:16])\t\(.status)\t\(.site_name[0:30])\tissues:\(.issue_counts.total // 0)"' \
    | column -t

echo ""
echo "=== Scans by Status ==="
for status in succeeded running failed queued; do
    COUNT=$(burp_api GET "/scans?status=${status}&limit=1" | jq '.total // 0')
    echo "$status: $COUNT"
done
```

### Vulnerability Findings

```bash
#!/bin/bash
SCAN_ID="${1:-}"

if [ -n "$SCAN_ID" ]; then
    echo "=== Scan Issues ==="
    burp_api GET "/scans/${SCAN_ID}/issues" \
        | jq -r '.data[] | "\(.severity)\t\(.confidence)\t\(.type_index)\t\(.path[0:40])\t\(.name[0:40])"' \
        | column -t | head -20
else
    echo "=== All High/Critical Issues (recent scans) ==="
    burp_api GET "/scans?sort_by=start&sort_order=desc&limit=5" \
        | jq -r '.data[].id' | while read SCAN; do
        burp_api GET "/scans/${SCAN}/issues?severity=high,critical" \
            | jq -r --arg scan "$SCAN" '.data[] | "\(.severity)\t\(.name[0:40])\tscan:\($scan)"'
    done | column -t | head -20
fi

echo ""
echo "=== Issue Types Summary ==="
burp_api GET "/issue_definitions" \
    | jq -r '.data[:15][] | "\(.type_index)\t\(.name[0:50])"' | column -t
```

### Site Scan History

```bash
#!/bin/bash
SITE_ID="${1:?Site ID required}"

echo "=== Site Scan History ==="
burp_api GET "/sites/${SITE_ID}/scans?sort_by=start&sort_order=desc&limit=10" \
    | jq -r '.data[] | "\(.start[0:16])\t\(.status)\tduration:\(.duration_in_seconds // 0)s\tissues:\(.issue_counts.total // 0)"' \
    | column -t

echo ""
echo "=== Scan Schedule ==="
burp_api GET "/sites/${SITE_ID}/schedules" \
    | jq -r '.data[] | "\(.id)\t\(.recurrence_rule)\t\(.scan_configuration_ids | join(","))"' | column -t
```

## Output Format

Present results as a structured report:
```
Managing Burp Suite Report
══════════════════════════
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

- **GraphQL vs REST**: Newer versions use GraphQL API -- check your Enterprise Edition version
- **Scan agents**: Scans run on agents -- ensure agents are healthy before scheduling
- **Issue deduplication**: Same issue may appear across scans -- use `type_index` + `path` for dedup
- **Scan duration**: DAST scans can take hours -- poll status rather than waiting
- **Self-signed certs**: On-prem installs may use self-signed certs -- add `-k` to curl if needed

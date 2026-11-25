---
name: managing-black-duck
description: |
  Use when working with Black Duck — synopsys Black Duck software composition
  analysis for open-source risk management, vulnerability detection, and license
  compliance. Covers project scanning, BOM component analysis, vulnerability
  tracking, license risk assessment, and policy management. Use when reviewing
  SCA scan results, analyzing open-source component risks, tracking license
  compliance, or managing Black Duck project configurations.
connection_type: black-duck
preload: false
---

# Black Duck Management Skill

Manage and analyze Black Duck projects, BOM components, vulnerabilities, and license compliance.

## API Conventions

### Authentication
All API calls use `Authorization: Bearer $BLACKDUCK_TOKEN` -- injected automatically. Never hardcode tokens.

### Base URL
`https://$BLACKDUCK_HOST/api`

### Core Helper Function

```bash
#!/bin/bash

bd_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $BLACKDUCK_TOKEN" \
            -H "Content-Type: application/json" \
            -H "Accept: application/vnd.blackducksoftware.user-4+json" \
            "https://${BLACKDUCK_HOST}/api${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $BLACKDUCK_TOKEN" \
            -H "Content-Type: application/json" \
            -H "Accept: application/vnd.blackducksoftware.user-4+json" \
            "https://${BLACKDUCK_HOST}/api${endpoint}"
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
echo "=== Projects ==="
bd_api GET "/projects?limit=100" \
    | jq '{total_projects: (.totalCount), items: [.items[:10][] | {name: .name, updatedAt: .updatedAt[0:10]}]}'

echo ""
echo "=== Code Locations ==="
bd_api GET "/codelocations?limit=1" \
    | jq '"Total code locations: \(.totalCount)"' -r

echo ""
echo "=== Policy Status ==="
bd_api GET "/policy-rules?limit=50" \
    | jq '{total_rules: .totalCount, enabled: ([.items[] | select(.enabled == true)] | length)}'
```

## Analysis Phase

### Vulnerability Overview

```bash
#!/bin/bash
echo "=== Vulnerability Summary Across Projects ==="
bd_api GET "/vulnerability-reports?limit=10" \
    | jq -r '.items[] | "\(.source)\t\(.severity)\t\(.vulnerabilityName)\t\(.componentName[0:30])\tv\(.componentVersionName)"' \
    | column -t | head -20

echo ""
echo "=== Projects with Critical Vulnerabilities ==="
bd_api GET "/projects?limit=50" | jq -r '.items[].name' | while read PROJECT; do
    VERSIONS_URL=$(bd_api GET "/projects?q=name:${PROJECT}&limit=1" | jq -r '.items[0]._meta.links[] | select(.rel == "versions") | .href')
    if [ -n "$VERSIONS_URL" ]; then
        VULN_COUNT=$(curl -s -H "Authorization: Bearer $BLACKDUCK_TOKEN" -H "Accept: application/vnd.blackducksoftware.user-4+json" "${VERSIONS_URL}?limit=1" | jq '[.items[0].securityRiskProfile.counts[] | select(.countType == "CRITICAL") | .count] | add // 0')
        [ "$VULN_COUNT" -gt 0 ] 2>/dev/null && echo "$VULN_COUNT\t$PROJECT"
    fi
done | sort -rn | head -15 | column -t
```

### BOM Component Analysis

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"
VERSION_ID="${2:?Version ID required}"

echo "=== BOM Components ==="
bd_api GET "/projects/${PROJECT_ID}/versions/${VERSION_ID}/components?limit=20&sort=securityRiskProfile" \
    | jq -r '.items[] | "\(.componentName[0:30])\tv\(.componentVersionName)\t\(.securityRiskProfile.counts | map(select(.countType == "CRITICAL" or .countType == "HIGH")) | map("\(.countType):\(.count)") | join(" "))"' \
    | column -t | head -20

echo ""
echo "=== License Risk ==="
bd_api GET "/projects/${PROJECT_ID}/versions/${VERSION_ID}/components?limit=50" \
    | jq -r '.items[] | select(.licenseRiskProfile.counts[] | select(.countType == "HIGH" and .count > 0)) | "\(.componentName[0:30])\t\(.licenses[0].licenseName // "Unknown")"' | head -10 | column -t
```

### Policy Violations

```bash
#!/bin/bash
echo "=== Policy Violations ==="
bd_api GET "/projects?limit=50" | jq -r '.items[] | select(.projectLevelAdjustments == true or true) | .name' | head -10 | while read PROJECT; do
    STATUS=$(bd_api GET "/projects?q=name:${PROJECT}&limit=1" | jq -r '.items[0]._meta.links[] | select(.rel == "versions") | .href')
    echo "$PROJECT"
done

echo ""
echo "=== Enabled Policies ==="
bd_api GET "/policy-rules?limit=20&filter=policyRuleEnabled:true" \
    | jq -r '.items[] | "\(.name[0:40])\tseverity:\(.severity)\t\(.description[0:40])"' | column -t | head -15
```

## Output Format

Present results as a structured report:
```
Managing Black Duck Report
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

- **HATEOAS API**: Navigate via `_meta.links` -- URLs are not predictable, follow link relations
- **Accept header versioning**: Different media types for different resources -- check docs for correct version
- **Token refresh**: Bearer tokens expire -- re-authenticate via `/tokens/authenticate`
- **Pagination**: Use `limit` and `offset` -- check `totalCount` in response
- **Project/version hierarchy**: Projects have versions, versions have BOM components -- always scope to version

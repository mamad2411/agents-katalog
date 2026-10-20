---
name: managing-finout
description: |
  Use when working with Finout — finout cloud cost management and MegaBill
  analysis platform. Covers cost allocation, MegaBill analysis, virtual tagging,
  showback reports, cost anomaly detection, and cross-provider spend
  optimization. Use when unifying cloud billing, creating virtual cost
  allocation tags, or generating showback/chargeback reports.
connection_type: finout
preload: false
---

# Finout Management Skill

Manage cloud cost allocation and MegaBill analysis with Finout.

## MANDATORY: Discovery-First Pattern

**Always list connected accounts and cost centers before querying MegaBill data.**

### Phase 1: Discovery

```bash
#!/bin/bash

finout_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" -H "Authorization: Bearer $FINOUT_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.finout.io/v1/${endpoint}" -d "$data"
    else
        curl -s -X "$method" -H "Authorization: Bearer $FINOUT_API_TOKEN" \
            "https://api.finout.io/v1/${endpoint}"
    fi
}

echo "=== Finout Account Status ==="
finout_api GET "account" | jq '{
    name: .name,
    connectedProviders: .connectedProviders,
    dataStatus: .dataStatus
}'

echo ""
echo "=== Connected Cloud Accounts ==="
finout_api GET "integrations" | jq -r '
    .items[] | "\(.id)\t\(.provider)\t\(.name)\t\(.status)"
' | column -t

echo ""
echo "=== Cost Centers ==="
finout_api GET "cost-centers" | jq -r '
    .items[] | "\(.id)\t\(.name)\tOwner: \(.owner // "unassigned")"
' | column -t | head -15
```

## Core Helper Functions

```bash
#!/bin/bash

finout_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" -H "Authorization: Bearer $FINOUT_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.finout.io/v1/${endpoint}" -d "$data"
    else
        curl -s -X "$method" -H "Authorization: Bearer $FINOUT_API_TOKEN" \
            "https://api.finout.io/v1/${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use jq to extract cost summaries from MegaBill responses
- Round costs to 2 decimal places

## Common Operations

### MegaBill Analysis

```bash
#!/bin/bash
PERIOD="${1:-monthly}"

echo "=== MegaBill Summary ==="
finout_api POST "megabill/query" '{"period": "'$PERIOD'", "groupBy": ["provider"]}' | jq -r '
    .data[] | "\(.provider)\t$\(.totalCost | . * 100 | round / 100)\tChange: \(.changePercent | . * 100 | round / 100)%"
' | sort -t'$' -k2 -rn | column -t

echo ""
echo "=== Top Services by Cost ==="
finout_api POST "megabill/query" '{"period": "'$PERIOD'", "groupBy": ["service"], "limit": 20}' | jq -r '
    .data[] | "\(.service)\t$\(.totalCost | . * 100 | round / 100)\t\(.provider)"
' | sort -t'$' -k2 -rn | column -t | head -20
```

### Virtual Tagging

```bash
#!/bin/bash
echo "=== Virtual Tags ==="
finout_api GET "virtual-tags" | jq -r '
    .items[] | "\(.id)\t\(.name)\tRules: \(.rules | length)\tCoverage: \(.coverage // "unknown")"
' | column -t | head -20

echo ""
echo "=== Untagged Cost Analysis ==="
finout_api POST "megabill/query" '{"period": "monthly", "groupBy": ["virtual-tag:team"], "filter": {"virtual-tag:team": "untagged"}}' | jq '{
    untaggedCost: .data[0].totalCost,
    percentOfTotal: .data[0].percentOfTotal
}'

echo ""
echo "=== Tag Coverage by Provider ==="
finout_api GET "virtual-tags/coverage" | jq -r '
    .items[] | "\(.provider)\tTagged: \(.taggedPercent | . * 100 | round / 100)%\tUntagged Cost: $\(.untaggedCost | . * 100 | round / 100)"
' | column -t
```

### Showback Reports

```bash
#!/bin/bash
COST_CENTER="${1:-}"

echo "=== Showback Report ==="
if [ -n "$COST_CENTER" ]; then
    finout_api GET "showback/reports?costCenter=${COST_CENTER}" | jq -r '
        .items[] | "\(.costCenter)\t\(.period)\t$\(.totalCost | . * 100 | round / 100)\tServices: \(.serviceCount)"
    ' | column -t | head -15
else
    finout_api GET "showback/reports" | jq -r '
        .items[] | "\(.costCenter)\t\(.period)\t$\(.totalCost | . * 100 | round / 100)"
    ' | sort -t'$' -k3 -rn | column -t | head -20
fi
```

### Cost Allocation

```bash
#!/bin/bash
echo "=== Cost Allocation by Team ==="
finout_api POST "megabill/query" '{"period": "monthly", "groupBy": ["virtual-tag:team"]}' | jq -r '
    .data[] | "\(.team // "unallocated")\t$\(.totalCost | . * 100 | round / 100)\t\(.percentOfTotal | . * 100 | round / 100)%"
' | sort -t'$' -k2 -rn | column -t | head -20

echo ""
echo "=== Cost by Environment ==="
finout_api POST "megabill/query" '{"period": "monthly", "groupBy": ["virtual-tag:environment"]}' | jq -r '
    .data[] | "\(.environment // "untagged")\t$\(.totalCost | . * 100 | round / 100)"
' | sort -t'$' -k2 -rn | column -t
```

### Cost Anomaly Detection

```bash
#!/bin/bash
echo "=== Recent Cost Anomalies ==="
finout_api GET "anomalies?days=7" | jq -r '
    .items[] |
    "\(.detectedAt[0:10])\t\(.service)\t\(.provider)\tExpected: $\(.expectedCost | . * 100 | round / 100)\tActual: $\(.actualCost | . * 100 | round / 100)\tDeviation: \(.deviationPercent | round)%"
' | sort -r | column -t | head -15

echo ""
echo "=== Anomaly Alert Rules ==="
finout_api GET "anomalies/rules" | jq -r '
    .items[] | "\(.name)\tThreshold: \(.thresholdPercent)%\tScope: \(.scope)\tEnabled: \(.enabled)"
' | column -t | head -10
```

## Safety Rules
- **Read-only operations**: Finout queries do not modify infrastructure or billing
- **Virtual tag caution**: Virtual tags affect cost attribution reports -- validate rules before applying
- **API token scope**: Ensure token has appropriate read permissions for all needed accounts
- **Report accuracy**: Cross-reference Finout data with native cloud billing for audits

## Output Format

Present results as a structured report:
```
Managing Finout Report
══════════════════════
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
- **Data ingestion delay**: New cloud accounts need 24-72 hours for full MegaBill data
- **Virtual tag conflicts**: Overlapping virtual tag rules can double-count costs
- **Currency normalization**: Multi-currency accounts need exchange rate configuration
- **Shared resources**: Shared infrastructure (NAT gateways, load balancers) needs explicit allocation rules
- **Historical data**: Virtual tag changes do not retroactively update historical reports
- **API rate limits**: Bulk MegaBill queries may hit rate limits -- use pagination for large datasets

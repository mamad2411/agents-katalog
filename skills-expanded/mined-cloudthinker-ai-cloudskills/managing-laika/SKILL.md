---
name: managing-laika
description: |
  Use when working with Laika — laika compliance platform for SOC 2, ISO 27001,
  HIPAA, and other security framework management. Covers control monitoring,
  policy management, evidence workflows, vendor assessment, and employee
  compliance tracking. Use when reviewing compliance status, managing security
  policies, tracking evidence collection workflows, assessing vendor risk, or
  monitoring employee security compliance.
connection_type: laika
preload: false
---

# Laika Management Skill

Manage and analyze Laika compliance controls, policies, evidence, vendors, and employee compliance.

## API Conventions

### Authentication
All API calls use `Authorization: Bearer $LAIKA_API_TOKEN` -- injected automatically. Never hardcode tokens.

### Base URL
`https://api.heylaika.com/v1`

### Core Helper Function

```bash
#!/bin/bash

laika_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $LAIKA_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.heylaika.com/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $LAIKA_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.heylaika.com/v1${endpoint}"
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
echo "=== Frameworks ==="
laika_api GET "/frameworks" \
    | jq -r '.data[] | "\(.id)\t\(.name)\t\(.status)"' | column -t | head -10

echo ""
echo "=== Controls Summary ==="
laika_api GET "/controls?limit=1" \
    | jq '"Total controls: \(.meta.total // "N/A")"' -r

echo ""
echo "=== Integrations ==="
laika_api GET "/integrations" \
    | jq -r '.data[] | "\(.name)\t\(.status)\t\(.type)"' | column -t | head -10
```

## Analysis Phase

### Control Status

```bash
#!/bin/bash
echo "=== Controls by Status ==="
CONTROLS=$(laika_api GET "/controls?limit=200")
echo "$CONTROLS" | jq '{
    total: (.data | length),
    passing: ([.data[] | select(.status == "passing")] | length),
    failing: ([.data[] | select(.status == "failing")] | length),
    needs_attention: ([.data[] | select(.status == "needs_attention")] | length),
    not_started: ([.data[] | select(.status == "not_started")] | length)
}'

echo ""
echo "=== Failing Controls ==="
echo "$CONTROLS" | jq -r '.data[] | select(.status == "failing") | "\(.status)\t\(.name[0:45])\t\(.framework[0:15])\towner:\(.owner[0:20] // "Unassigned")"' \
    | column -t | head -15

echo ""
echo "=== Controls Needing Attention ==="
echo "$CONTROLS" | jq -r '.data[] | select(.status == "needs_attention") | "\(.name[0:50])\treason:\(.attentionReason[0:30] // "N/A")"' \
    | column -t | head -10
```

### Policy Management

```bash
#!/bin/bash
echo "=== Policies ==="
laika_api GET "/policies?limit=100" \
    | jq -r '.data[] | "\(.status)\t\(.name[0:40])\tversion:\(.version // 1)\tupdated:\(.updatedAt[0:10] // "N/A")"' \
    | sort | column -t | head -20

echo ""
echo "=== Policy Acknowledgments ==="
laika_api GET "/policies?limit=100" \
    | jq -r '.data[] | select(.acknowledgmentRequired == true) | "\(.name[0:35])\tacknowledged:\(.acknowledgedCount // 0)/\(.totalEmployees // 0)\t\(if .acknowledgedCount == .totalEmployees then "COMPLETE" else "PENDING" end)"' \
    | column -t | head -10

echo ""
echo "=== Policies Due for Review ==="
laika_api GET "/policies?limit=50&reviewDue=true" \
    | jq -r '.data[] | "\(.name[0:40])\tlastReview:\(.lastReviewDate[0:10] // "Never")\tdue:\(.nextReviewDate[0:10] // "N/A")"' | column -t
```

### Evidence Workflows

```bash
#!/bin/bash
echo "=== Evidence Status ==="
laika_api GET "/evidence?limit=200" \
    | jq '{
        total: (.data | length),
        approved: ([.data[] | select(.status == "approved")] | length),
        pending_review: ([.data[] | select(.status == "pending_review")] | length),
        needs_upload: ([.data[] | select(.status == "needs_upload")] | length),
        expired: ([.data[] | select(.status == "expired")] | length)
    }'

echo ""
echo "=== Evidence Needing Upload ==="
laika_api GET "/evidence?limit=50&status=needs_upload" \
    | jq -r '.data[] | "\(.controlName[0:30])\t\(.name[0:35])\tassignee:\(.assignee[0:20] // "Unassigned")"' \
    | column -t | head -15
```

### Vendor Assessment

```bash
#!/bin/bash
echo "=== Vendor Risk ==="
laika_api GET "/vendors?limit=100" \
    | jq -r '[.data[].riskLevel] | group_by(.) | map({risk: .[0], count: length}) | sort_by(.count) | reverse | .[] | "\(.risk): \(.count)"'

echo ""
echo "=== Vendors Pending Review ==="
laika_api GET "/vendors?limit=50&reviewStatus=pending" \
    | jq -r '.data[] | "\(.name[0:25])\t\(.riskLevel)\t\(.category[0:20])\tlastReview:\(.lastReviewDate[0:10] // "Never")"' \
    | column -t | head -10

echo ""
echo "=== Vendor Questionnaire Status ==="
laika_api GET "/vendors?limit=50" \
    | jq -r '.data[] | select(.questionnaireStatus != null) | "\(.name[0:25])\t\(.questionnaireStatus)\tsent:\(.questionnaireSentDate[0:10] // "N/A")"' | column -t | head -10
```

### Employee Compliance

```bash
#!/bin/bash
echo "=== Employee Compliance ==="
laika_api GET "/employees?limit=200" \
    | jq '{
        total: (.data | length),
        compliant: ([.data[] | select(.complianceStatus == "compliant")] | length),
        non_compliant: ([.data[] | select(.complianceStatus == "non_compliant")] | length)
    }'

echo ""
echo "=== Non-Compliant Employees ==="
laika_api GET "/employees?limit=50&complianceStatus=non_compliant" \
    | jq -r '.data[] | "\(.name)\t\(.email[0:30])\tissues:\(.outstandingItems | length)"' \
    | column -t | head -15
```

## Output Format

Present results as a structured report:
```
Managing Laika Report
═════════════════════
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

- **Workflow-based evidence**: Evidence follows approval workflows -- check pending reviews
- **Policy versioning**: Policies have versions -- acknowledgments are per-version
- **Pagination**: Use `limit` and `offset` -- check `meta.total`
- **Rate limits**: Check response headers for rate limiting
- **Vendor questionnaires**: Vendors may have pending security questionnaires that need follow-up
- **Integration dependencies**: Control status depends on connected integrations being healthy

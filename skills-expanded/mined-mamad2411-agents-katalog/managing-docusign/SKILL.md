---
name: managing-docusign
description: |
  Use when working with Docusign — docuSign eSignature platform management
  covering envelopes, templates, users, signing workflows, and account
  analytics. Use when monitoring envelope status, analyzing signing completion
  rates, reviewing template usage, managing DocuSign users and permissions, or
  troubleshooting document signing workflows.
connection_type: docusign
preload: false
---

# DocuSign Management Skill

Manage and analyze DocuSign eSignature resources including envelopes, templates, and account health.

## API Conventions

### Authentication
All API calls use Bearer OAuth token, injected automatically.

### Base URL
`https://{base_uri}/restapi/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID`

### Core Helper Function

```bash
#!/bin/bash

docusign_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $DOCUSIGN_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            "${DOCUSIGN_BASE_URI}/restapi/v2.1/accounts/${DOCUSIGN_ACCOUNT_ID}${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $DOCUSIGN_ACCESS_TOKEN" \
            "${DOCUSIGN_BASE_URI}/restapi/v2.1/accounts/${DOCUSIGN_ACCOUNT_ID}${endpoint}"
    fi
}
```

## Output Rules
- Target ≤50 lines per script output
- Use `jq` to extract only needed fields
- Never dump full API responses

## Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Account Info ==="
docusign_api GET "" | jq '{account_name: .accountName, plan: .planName, billing_period_end: .billingPeriodEndDate}'

echo ""
echo "=== Recent Envelopes ==="
docusign_api GET "/envelopes?from_date=$(date -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)&count=20&order_by=last_modified&order=desc" \
    | jq -r '.envelopes[] | "\(.envelopeId[0:12])\t\(.status)\t\(.emailSubject[0:40])\t\(.statusChangedDateTime[0:10])"' \
    | column -t | head -20

echo ""
echo "=== Templates ==="
docusign_api GET "/templates?count=20" \
    | jq -r '.envelopeTemplates[] | "\(.templateId[0:12])\t\(.name[0:40])\t\(.lastModifiedDateTime[0:10])"' \
    | column -t | head -15

echo ""
echo "=== Users ==="
docusign_api GET "/users?count=20" \
    | jq -r '.users[] | "\(.userId[0:12])\t\(.userName)\t\(.userStatus)\t\(.email)"' \
    | column -t | head -15
```

## Phase 2: Analysis

### Envelope Health

```bash
#!/bin/bash
echo "=== Envelope Status Summary (last 30 days) ==="
docusign_api GET "/envelopes?from_date=$(date -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)&count=100" \
    | jq -r '.envelopes[] | .status' | sort | uniq -c | sort -rn

echo ""
echo "=== Pending/Sent Envelopes (awaiting signature) ==="
docusign_api GET "/envelopes?from_date=$(date -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)&status=sent&count=20" \
    | jq -r '.envelopes[] | "\(.envelopeId[0:12])\t\(.emailSubject[0:40])\t\(.sentDateTime[0:10])\t\(.recipients.signers | length) signers"' \
    | head -15

echo ""
echo "=== Voided/Declined Envelopes ==="
docusign_api GET "/envelopes?from_date=$(date -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)&status=voided,declined&count=20" \
    | jq -r '.envelopes[] | "\(.envelopeId[0:12])\t\(.status)\t\(.emailSubject[0:40])\t\(.voidedReason // "no reason")"' \
    | head -10
```

### Signing Analytics

```bash
#!/bin/bash
echo "=== Completion Rate (last 30 days) ==="
ALL=$(docusign_api GET "/envelopes?from_date=$(date -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)&count=1" | jq '.totalSetSize // 0')
COMPLETED=$(docusign_api GET "/envelopes?from_date=$(date -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)&status=completed&count=1" | jq '.totalSetSize // 0')
echo "Total: $ALL  Completed: $COMPLETED  Rate: $(echo "scale=1; $COMPLETED * 100 / $ALL" | bc)%"

echo ""
echo "=== Template Usage ==="
docusign_api GET "/templates?count=50" \
    | jq -r '.envelopeTemplates[] | "\(.name[0:40])\t\(.shared)\tfolders:\(.folderIds | length)"' \
    | head -15

echo ""
echo "=== Envelopes Per Day (last 7 days) ==="
docusign_api GET "/envelopes?from_date=$(date -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)&count=200" \
    | jq -r '.envelopes[] | .statusChangedDateTime[0:10]' | sort | uniq -c | sort -k2
```

## Output Format

```
=== Account: <name> | Plan: <plan> ===

--- Envelope Summary (30d) ---
completed: <n>  sent: <n>  voided: <n>  declined: <n>
Completion Rate: <n>%

--- Pending Signatures ---
<subject>  <sent_date>  <signers> signers

--- Templates ---
Total: <n>  Most Used: <template_name>
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

## Common Pitfalls
- **Date format**: Use ISO 8601 with timezone for `from_date` parameter
- **Envelope statuses**: `created`, `sent`, `delivered`, `signed`, `completed`, `declined`, `voided`
- **Rate limits**: 1000 requests/hour per account; batch operations when possible
- **Pagination**: Use `count` and `start_position`; check `totalSetSize` for total

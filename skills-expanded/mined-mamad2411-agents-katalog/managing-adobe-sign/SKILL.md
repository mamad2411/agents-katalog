---
name: managing-adobe-sign
description: |
  Use when working with Adobe Sign — adobe Acrobat Sign (formerly Adobe Sign)
  eSignature platform management covering agreements, templates, workflows,
  users, and audit trails. Use when monitoring agreement status, analyzing
  signing completion rates, reviewing workflow performance, managing Adobe Sign
  users, or auditing document signing activity.
connection_type: adobe-sign
preload: false
---

# Adobe Sign Management Skill

Manage and analyze Adobe Acrobat Sign resources including agreements, templates, workflows, and users.

## API Conventions

### Authentication
All API calls use Bearer OAuth token or Integration Key, injected automatically.

### Base URL
`https://api.na1.adobesign.com/api/rest/v6` (region varies)

### Core Helper Function

```bash
#!/bin/bash

adobesign_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $ADOBE_SIGN_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            "${ADOBE_SIGN_BASE_URI}/api/rest/v6${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $ADOBE_SIGN_ACCESS_TOKEN" \
            "${ADOBE_SIGN_BASE_URI}/api/rest/v6${endpoint}"
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
echo "=== Current User Info ==="
adobesign_api GET "/users/me" \
    | jq '{email: .email, firstName: .firstName, lastName: .lastName, accountType: .accountType, status: .status}'

echo ""
echo "=== Recent Agreements ==="
adobesign_api GET "/agreements?pageSize=20" \
    | jq -r '.userAgreementList[] | "\(.id[0:16])\t\(.status)\t\(.name[0:40])\t\(.displayDate[0:10])"' \
    | column -t | head -20

echo ""
echo "=== Library Templates ==="
adobesign_api GET "/libraryDocuments?pageSize=20" \
    | jq -r '.libraryDocumentList[] | "\(.id[0:16])\t\(.name[0:40])\t\(.modifiedDate[0:10])"' \
    | column -t | head -15

echo ""
echo "=== Workflows ==="
adobesign_api GET "/workflows?pageSize=20" \
    | jq -r '.userWorkflowList[] | "\(.id[0:16])\t\(.displayName[0:40])\t\(.status)\t\(.scope)"' \
    | head -15
```

## Phase 2: Analysis

### Agreement Health

```bash
#!/bin/bash
echo "=== Agreement Status Summary ==="
adobesign_api GET "/agreements?pageSize=100" \
    | jq -r '.userAgreementList[] | .status' | sort | uniq -c | sort -rn

echo ""
echo "=== Agreements Awaiting Signature ==="
adobesign_api GET "/agreements?pageSize=20" \
    | jq -r '.userAgreementList[] | select(.status == "OUT_FOR_SIGNATURE") | "\(.id[0:16])\t\(.name[0:40])\t\(.displayDate[0:10])"' \
    | head -15

echo ""
echo "=== Cancelled/Expired Agreements ==="
adobesign_api GET "/agreements?pageSize=50" \
    | jq -r '.userAgreementList[] | select(.status == "CANCELLED" or .status == "EXPIRED") | "\(.id[0:16])\t\(.status)\t\(.name[0:40])"' \
    | head -10
```

### User & Audit Analytics

```bash
#!/bin/bash
echo "=== Account Users ==="
adobesign_api GET "/users?pageSize=20" \
    | jq -r '.userInfoList[] | "\(.id[0:16])\t\(.email)\t\(.status)\t\(.accountType)"' \
    | column -t | head -15

echo ""
echo "=== Agreement Audit Events (sample) ==="
AGREEMENT_ID=$(adobesign_api GET "/agreements?pageSize=1" | jq -r '.userAgreementList[0].id')
if [ -n "$AGREEMENT_ID" ] && [ "$AGREEMENT_ID" != "null" ]; then
    adobesign_api GET "/agreements/${AGREEMENT_ID}/events" \
        | jq -r '.events[] | "\(.date[0:16])\t\(.type)\t\(.participantEmail // "system")\t\(.description[0:40])"' \
        | head -15
fi
```

## Output Format

```
=== Account: <email> | Type: <type> ===

--- Agreement Summary ---
SIGNED: <n>  OUT_FOR_SIGNATURE: <n>  CANCELLED: <n>  EXPIRED: <n>

--- Awaiting Signature ---
<name>  <date>

--- Users ---
Total: <n>  Active: <n>
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
- **Regional base URL**: API URL varies by region (na1, na2, eu1, jp1, au1, in1)
- **Agreement statuses**: `SIGNED`, `OUT_FOR_SIGNATURE`, `WAITING_FOR_MY_SIGNATURE`, `DRAFT`, `CANCELLED`, `EXPIRED`
- **Pagination**: Use `pageSize` and cursor-based pagination; check `page.nextCursor`
- **Rate limits**: 600 requests/5 minutes for standard accounts
- **OAuth scopes**: Different operations require specific scopes (agreement_read, agreement_write, etc.)

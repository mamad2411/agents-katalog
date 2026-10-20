---
name: managing-hellosign
description: |
  Use when working with Hellosign — helloSign (Dropbox Sign) eSignature platform
  management covering signature requests, templates, teams, and account
  analytics. Use when monitoring signature request status, analyzing completion
  rates, reviewing template usage, managing team members, or troubleshooting
  HelloSign signing workflows.
connection_type: hellosign
preload: false
---

# HelloSign Management Skill

Manage and analyze HelloSign (Dropbox Sign) eSignature resources including signature requests and templates.

## API Conventions

### Authentication
All API calls use Basic Auth with API key, injected automatically.

### Base URL
`https://api.hellosign.com/v3`

### Core Helper Function

```bash
#!/bin/bash

hellosign_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -u "$HELLOSIGN_API_KEY:" \
            -H "Content-Type: application/json" \
            "https://api.hellosign.com/v3${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -u "$HELLOSIGN_API_KEY:" \
            "https://api.hellosign.com/v3${endpoint}"
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
hellosign_api GET "/account" \
    | jq '.account | {account_id: .account_id, email: .email_address, is_paid_hs: .is_paid_hs, quota: .quotas}'

echo ""
echo "=== Recent Signature Requests ==="
hellosign_api GET "/signature_request/list?page_size=20" \
    | jq -r '.signature_requests[] | "\(.signature_request_id[0:12])\t\(.title[0:40])\t\(.is_complete)\t\(.created_at | strftime("%Y-%m-%d"))"' \
    | column -t | head -20

echo ""
echo "=== Templates ==="
hellosign_api GET "/template/list?page_size=20" \
    | jq -r '.templates[] | "\(.template_id[0:12])\t\(.title[0:40])\t\(.signer_roles | length) roles"' \
    | column -t | head -15
```

## Phase 2: Analysis

### Signature Request Health

```bash
#!/bin/bash
echo "=== Completion Summary ==="
hellosign_api GET "/signature_request/list?page_size=100" \
    | jq '{
        total: (.signature_requests | length),
        completed: [.signature_requests[] | select(.is_complete == true)] | length,
        pending: [.signature_requests[] | select(.is_complete == false and .is_declined == false)] | length,
        declined: [.signature_requests[] | select(.is_declined == true)] | length
    }'

echo ""
echo "=== Pending Signatures ==="
hellosign_api GET "/signature_request/list?page_size=20" \
    | jq -r '.signature_requests[] | select(.is_complete == false) | "\(.signature_request_id[0:12])\t\(.title[0:40])\t\(.signatures | map(select(.status_code == "awaiting_signature")) | length) awaiting"' \
    | head -15

echo ""
echo "=== Signer Status Details ==="
hellosign_api GET "/signature_request/list?page_size=20" \
    | jq -r '.signature_requests[] | select(.is_complete == false) | .signatures[] | "\(.signature_id[0:12])\t\(.signer_email_address)\t\(.status_code)\t\(.signed_at // "not signed")"' \
    | head -15
```

### Account Quota & Usage

```bash
#!/bin/bash
echo "=== API Quota ==="
hellosign_api GET "/account" \
    | jq '.account.quotas | {templates_left: .templates_left, api_signature_requests_left: .api_signature_requests_left, documents_left: .documents_left}'

echo ""
echo "=== Team Info ==="
hellosign_api GET "/team" \
    | jq '.team | {name: .name, accounts: [.accounts[].email_address]}'

echo ""
echo "=== Requests Per Day (recent) ==="
hellosign_api GET "/signature_request/list?page_size=100" \
    | jq -r '.signature_requests[] | .created_at | strftime("%Y-%m-%d")' | sort | uniq -c | sort -k2 | tail -7
```

## Output Format

```
=== Account: <email> | Plan: <paid|free> ===
Quota: <n> requests left, <n> templates left

--- Signature Requests ---
Total: <n>  Completed: <n>  Pending: <n>  Declined: <n>

--- Pending Signatures ---
<title>  <n> awaiting signature

--- Templates ---
Total: <n>
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
- **Auth format**: Basic auth with API key as username, empty password (note trailing colon)
- **Timestamps**: Unix epoch seconds in responses — use `strftime` for formatting
- **Pagination**: Use `page` and `page_size` (max 100); check `num_pages` in `list_info`
- **Rate limits**: 25 requests/minute for free, higher for paid plans
- **Status codes**: Signer statuses are `awaiting_signature`, `signed`, `declined`

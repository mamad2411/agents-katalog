---
name: managing-clerk
description: |
  Use when working with Clerk — clerk authentication and user management
  platform covering users, sessions, organizations, invitations, and sign-in
  methods. Use when analyzing user growth, monitoring authentication health,
  reviewing organization membership, managing Clerk users, or auditing sign-in
  patterns.
connection_type: clerk
preload: false
---

# Clerk Management Skill

Manage and analyze Clerk authentication resources including users, organizations, and sessions.

## API Conventions

### Authentication
All API calls use Bearer secret key, injected automatically.

### Base URL
`https://api.clerk.com/v1`

### Core Helper Function

```bash
#!/bin/bash

clerk_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $CLERK_SECRET_KEY" \
            -H "Content-Type: application/json" \
            "https://api.clerk.com/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $CLERK_SECRET_KEY" \
            "https://api.clerk.com/v1${endpoint}"
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
echo "=== User Count ==="
clerk_api GET "/users/count" | jq '{total_users: .total_count}'

echo ""
echo "=== Recent Users ==="
clerk_api GET "/users?limit=20&order_by=-created_at" \
    | jq -r '.[] | "\(.id[0:16])\t\(.email_addresses[0].email_address // "no-email")\t\(.created_at | . / 1000 | strftime("%Y-%m-%d"))"' \
    | column -t | head -20

echo ""
echo "=== Organizations ==="
clerk_api GET "/organizations?limit=20" \
    | jq -r '.data[] | "\(.id[0:16])\t\(.name)\t\(.members_count) members\t\(.created_at | . / 1000 | strftime("%Y-%m-%d"))"' \
    | column -t | head -15

echo ""
echo "=== Active Sessions ==="
clerk_api GET "/sessions?status=active&limit=20" \
    | jq -r '.data[] | "\(.id[0:16])\t\(.user_id[0:16])\t\(.status)\t\(.last_active_at | . / 1000 | strftime("%Y-%m-%d %H:%M"))"' \
    | head -15
```

## Phase 2: Analysis

### User Health

```bash
#!/bin/bash
echo "=== User Growth (sign-up method) ==="
clerk_api GET "/users?limit=200&order_by=-created_at" \
    | jq -r '[.[] | .external_accounts[0].provider // "email"] | group_by(.) | map({(.[0]): length}) | add'

echo ""
echo "=== Users Without Verified Email ==="
clerk_api GET "/users?limit=100" \
    | jq -r '[.[] | select(.email_addresses | all(.verification.status != "verified"))] | length | "Unverified emails: \(.)"'

echo ""
echo "=== Users with 2FA Enabled ==="
clerk_api GET "/users?limit=200" \
    | jq -r '[.[] | select(.two_factor_enabled == true)] | length | "2FA enabled: \(.)"'

echo ""
echo "=== Banned/Locked Users ==="
clerk_api GET "/users?limit=200" \
    | jq -r '[.[] | select(.banned == true or .locked == true)] | length | "Banned/Locked: \(.)"'
```

### Organization Analytics

```bash
#!/bin/bash
echo "=== Organization Summary ==="
clerk_api GET "/organizations?limit=50" \
    | jq '{
        total_orgs: (.data | length),
        total_members: (.data | map(.members_count) | add),
        avg_members: (.data | map(.members_count) | if length > 0 then add / length | floor else 0 end)
    }'

echo ""
echo "=== Largest Organizations ==="
clerk_api GET "/organizations?limit=50&order_by=-members_count" \
    | jq -r '.data[] | "\(.name)\t\(.members_count) members\t\(.pending_invitations_count) pending"' \
    | head -10

echo ""
echo "=== Pending Invitations ==="
clerk_api GET "/invitations?status=pending&limit=20" \
    | jq -r '.data[] | "\(.email_address)\t\(.status)\t\(.created_at | . / 1000 | strftime("%Y-%m-%d"))"' \
    | head -15
```

## Output Format

```
=== Clerk Instance ===
Total Users: <n>  Organizations: <n>

--- Auth Health ---
2FA Enabled: <n>  Unverified: <n>  Banned: <n>

--- Sign-up Methods ---
email: <n>  google: <n>  github: <n>

--- Organizations ---
Total: <n>  Avg Members: <n>  Pending Invites: <n>
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
- **Timestamps**: Clerk uses Unix milliseconds, not seconds — divide by 1000 for date conversion
- **Pagination**: Use `limit` and `offset`; check response array length for more pages
- **Rate limits**: 20 requests/10 seconds for backend API
- **User IDs**: Prefixed with `user_`, org IDs with `org_`

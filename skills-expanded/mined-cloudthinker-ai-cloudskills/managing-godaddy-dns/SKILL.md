---
name: managing-godaddy-dns
description: |
  Use when working with Godaddy Dns — goDaddy DNS management covering domain DNS
  records, zone configuration, domain availability, registration details, and
  forwarding rules. Use when managing GoDaddy-hosted DNS records, checking
  domain registration status, configuring DNS forwarding, or auditing DNS
  configuration across GoDaddy domains.
connection_type: godaddy
preload: false
---

# GoDaddy DNS Skill

Manage GoDaddy DNS records, domain registrations, forwarding, and zone configuration.

## Core Helper Functions

```bash
#!/bin/bash

GD_API="https://api.godaddy.com/v1"

gd_api() {
    local endpoint="$1"
    shift
    curl -s -H "Authorization: sso-key $GODADDY_API_KEY:$GODADDY_API_SECRET" \
         -H "Content-Type: application/json" \
         "$GD_API/$endpoint" "$@"
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Domains ==="
gd_api "domains?limit=100&statuses=ACTIVE" | jq -r '
    .[] | "\(.domainId)\t\(.domain)\t\(.status)\t\(.expires[:10])\t\(.renewAuto)\t\(.locked)"
' | column -t | head -20

echo ""
echo "=== Domain Name Servers ==="
for DOMAIN in $(gd_api "domains?limit=20&statuses=ACTIVE" | jq -r '.[].domain'); do
    NS=$(gd_api "domains/$DOMAIN" | jq -r '.nameServers | join(", ")')
    echo "$DOMAIN: $NS"
done | head -15

echo ""
echo "=== Domains Expiring Soon ==="
gd_api "domains?limit=100&statuses=ACTIVE" | jq -r '
    [.[] | select(.expires < (now + 2592000 | todate))] |
    sort_by(.expires) | .[] | "\(.domain)\t\(.expires[:10])\t\(.renewAuto)"
' | column -t | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
DOMAIN="${1:?Domain name required}"

echo "=== DNS Records ==="
gd_api "domains/$DOMAIN/records" | jq -r '
    .[] | "\(.type)\t\(.name)\t\(.data[:60])\t\(.ttl)s\t\(.priority // "")"
' | sort | column -t | head -30

echo ""
echo "=== Record Type Summary ==="
gd_api "domains/$DOMAIN/records" | jq -r '
    group_by(.type) | .[] | "\(.[0].type): \(length) records"
'

echo ""
echo "=== Domain Details ==="
gd_api "domains/$DOMAIN" | jq '{
    domain, status, expires: .expires[:10],
    renewAuto, renewDeadline: .renewDeadline[:10],
    locked, privacy, transferProtected,
    nameServers, contactRegistrant: .contactRegistrant.email
}'

echo ""
echo "=== Forwarding Rules ==="
gd_api "domains/$DOMAIN/forwarding" | jq -r '
    .[] | "\(.fqdn)\t\(.url)\t\(.type)\t\(.mask)"
' | column -t 2>/dev/null | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use jq to parse GoDaddy API JSON responses
- Sort DNS records by type for readability

## Safety Rules
- **Read-only by default**: Use GET endpoints for inspection
- **Never delete DNS records** without explicit confirmation
- **Domain lock status**: Changing lock can expose domain to unauthorized transfers
- **Privacy settings**: Disabling WHOIS privacy exposes registrant contact info

## Output Format

Present results as a structured report:
```
Managing Godaddy Dns Report
═══════════════════════════
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
- **API key format**: Uses `sso-key API_KEY:API_SECRET` authorization header
- **Record replacement**: PUT replaces ALL records of a type; use PATCH for individual updates
- **TTL minimum**: GoDaddy enforces minimum TTL of 600 seconds for some plans
- **OTE vs Production**: Test environment (ote-godaddy.com) vs production (godaddy.com)
- **Rate limits**: 60 requests per minute for most endpoints

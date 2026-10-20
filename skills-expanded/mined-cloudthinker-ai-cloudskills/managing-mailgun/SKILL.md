---
name: managing-mailgun
description: |
  Use when working with Mailgun — mailgun email service management including
  domain configuration, sending statistics, deliverability monitoring, bounce
  and complaint tracking, route management, and mailing list administration.
  Covers domain health, DNS verification, reputation scoring, and event log
  analysis.
connection_type: mailgun
preload: false
---

# Mailgun Management Skill

Monitor and manage Mailgun email sending infrastructure and deliverability.

## MANDATORY: Discovery-First Pattern

**Always discover domains and their verification status before querying stats.**

### Phase 1: Discovery

```bash
#!/bin/bash
MG_API="https://api.mailgun.net/v3"
AUTH="api:${MAILGUN_API_KEY}"

echo "=== Domains ==="
curl -s -u "$AUTH" "$MG_API/domains" | \
  jq -r '.items[] | "\(.name) | State: \(.state) | Type: \(.type) | Created: \(.created_at)"'

echo ""
echo "=== Domain Verification ==="
for domain in $(curl -s -u "$AUTH" "$MG_API/domains" | jq -r '.items[].name'); do
  status=$(curl -s -u "$AUTH" "$MG_API/domains/$domain" | \
    jq -r '"SPF: \(.sending_dns_records[] | select(.record_type=="TXT" and (.name | contains("spf"))) | .valid // "missing") | DKIM: \(.sending_dns_records[] | select(.record_type=="TXT" and (.name | contains("domainkey"))) | .valid // "missing")"' 2>/dev/null)
  echo "$domain | $status"
done

echo ""
echo "=== IPs ==="
curl -s -u "$AUTH" "$MG_API/ips" | \
  jq -r '.items[] | "\(.ip) | Dedicated: \(.dedicated) | Pool: \(.pool_id)"'

echo ""
echo "=== Routes ==="
curl -s -u "$AUTH" "$MG_API/routes" | \
  jq -r '.items[] | "\(.expression) -> \(.actions[0]) | Priority: \(.priority)"'
```

**Phase 1 outputs:** Domain list, DNS verification, IPs, routes

### Phase 2: Analysis

```bash
#!/bin/bash
DOMAIN="${1:-$MAILGUN_DOMAIN}"

echo "=== Sending Stats (7 days) ==="
curl -s -u "$AUTH" "$MG_API/$DOMAIN/stats/total?event=accepted&event=delivered&event=failed&event=opened&event=clicked&duration=7d" | \
  jq -r '.stats[] | "\(.time): Sent=\(.accepted.total) Del=\(.delivered.total) Fail=\(.failed.total.total) Open=\(.opened.total)"'

echo ""
echo "=== Bounce Rate ==="
curl -s -u "$AUTH" "$MG_API/$DOMAIN/bounces?limit=5" | \
  jq -r '.items[] | "\(.address) | Code: \(.code) | Error: \(.error[:60])"'

echo ""
echo "=== Complaints ==="
curl -s -u "$AUTH" "$MG_API/$DOMAIN/complaints?limit=5" | \
  jq -r '.items[] | "\(.address) | Date: \(.created_at)"'

echo ""
echo "=== Suppressions Summary ==="
bounces=$(curl -s -u "$AUTH" "$MG_API/$DOMAIN/bounces" | jq '.total_count')
complaints=$(curl -s -u "$AUTH" "$MG_API/$DOMAIN/complaints" | jq '.total_count')
unsubs=$(curl -s -u "$AUTH" "$MG_API/$DOMAIN/unsubscribes" | jq '.total_count')
echo "Bounces: $bounces | Complaints: $complaints | Unsubscribes: $unsubs"
```

## Output Format

```
MAILGUN STATUS
==============
Domain: {domain} ({state})
DNS: SPF={status} DKIM={status}
7-Day Stats: Sent={count} Delivered={count} Failed={count}
Delivery Rate: {percent}%
Open Rate: {percent}%
Suppressions: {bounces} bounces, {complaints} complaints
Issues: {list_of_warnings}
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

- **EU vs US region**: EU domains use api.eu.mailgun.net — check domain settings
- **DNS propagation**: SPF/DKIM changes take up to 48h — verify before flagging
- **Rate limits**: 300 requests/minute for free tier — batch stat queries
- **Suppression lists**: Mailgun auto-suppresses bounced addresses — check before diagnosing delivery failures

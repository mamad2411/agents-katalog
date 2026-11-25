---
name: managing-convertkit
description: |
  Use when working with Convertkit — convertKit (Kit) creator marketing platform
  management including subscriber management, forms, sequences, broadcasts,
  tags, and automation rules. Covers subscriber growth, email deliverability,
  sequence performance, and form conversion tracking.
connection_type: convertkit
preload: false
---

# ConvertKit Management Skill

Monitor and manage ConvertKit email marketing for creators.

## MANDATORY: Discovery-First Pattern

**Always discover account info and subscriber count before querying forms or sequences.**

### Phase 1: Discovery

```bash
#!/bin/bash
CK_API="https://api.convertkit.com/v3"
API_SECRET="${CONVERTKIT_API_SECRET}"

echo "=== Account Info ==="
curl -s "$CK_API/account?api_secret=$API_SECRET" | \
  jq -r '"Name: \(.name)\nPlan: \(.plan_name)\nSubscribers: \(.total_subscribers)"'

echo ""
echo "=== Forms ==="
curl -s "$CK_API/forms?api_secret=$API_SECRET" | \
  jq -r '.forms[] | "\(.name) | ID: \(.id) | Type: \(.type) | Subscribers: \(.total_subscriptions) | Created: \(.created_at)"'

echo ""
echo "=== Sequences ==="
curl -s "$CK_API/sequences?api_secret=$API_SECRET" | \
  jq -r '.courses[] | "\(.name) | ID: \(.id) | Subscribers: \(.total_subscriptions) | Created: \(.created_at)"'

echo ""
echo "=== Tags ==="
curl -s "$CK_API/tags?api_secret=$API_SECRET" | \
  jq -r '.tags[] | "\(.name) | ID: \(.id) | Created: \(.created_at)"' | head -20
```

**Phase 1 outputs:** Account plan, forms, sequences, tags

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Subscriber Growth (recent) ==="
curl -s "$CK_API/subscribers?api_secret=$API_SECRET&sort_order=desc&per_page=5" | \
  jq -r '.subscribers[] | "\(.email_address) | State: \(.state) | Created: \(.created_at)"'

echo ""
echo "=== Subscriber States ==="
total=$(curl -s "$CK_API/subscribers?api_secret=$API_SECRET" | jq '.total_subscribers')
echo "Total subscribers: $total"

echo ""
echo "=== Broadcasts (recent) ==="
curl -s "$CK_API/broadcasts?api_secret=$API_SECRET" | \
  jq -r '.broadcasts[:10] | .[] | "\(.subject) | Status: \(.status) | Sent: \(.sent_at // "not sent")"'

echo ""
echo "=== Automations ==="
curl -s "$CK_API/automations?api_secret=$API_SECRET" | \
  jq -r '.automations[] | "\(.name) | Status: \(.status) | Subscribers: \(.subscriber_count)"' | head -10

echo ""
echo "=== Form Conversion Rates ==="
curl -s "$CK_API/forms?api_secret=$API_SECRET" | \
  jq -r '.forms[] | "\(.name): \(.total_subscriptions) subs from \(.total_unique_visitors // "N/A") visitors"'
```

## Output Format

```
CONVERTKIT STATUS
=================
Account: {name} ({plan})
Total Subscribers: {count}
Forms: {count} | Sequences: {count} | Tags: {count}
Recent Broadcasts: {count}
Active Automations: {count}
Top Form: {name} ({conversions} conversions)
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

- **API key vs API secret**: Most endpoints need api_secret, not api_key
- **Subscriber states**: active, cancelled, bounced, complained — filter accordingly
- **Rate limits**: 120 requests/minute — batch subscriber queries
- **Sequences vs Automations**: Sequences are linear email series; automations are rule-based workflows

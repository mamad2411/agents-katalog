---
name: managing-klaviyo
description: |
  Use when working with Klaviyo — klaviyo marketing automation platform
  management including email and SMS campaigns, flows, lists, segments, metrics,
  and revenue attribution. Covers deliverability monitoring, flow performance,
  list growth, and A/B testing results.
connection_type: klaviyo
preload: false
---

# Klaviyo Management Skill

Monitor and manage Klaviyo email and SMS marketing automation.

## MANDATORY: Discovery-First Pattern

**Always discover account metrics and lists before querying campaign or flow data.**

### Phase 1: Discovery

```bash
#!/bin/bash
KL_API="https://a.klaviyo.com/api"
AUTH="Authorization: Klaviyo-API-Key ${KLAVIYO_API_KEY}"
REV="revision: 2024-10-15"

echo "=== Account Info ==="
curl -s -H "$AUTH" -H "$REV" "$KL_API/accounts/" | \
  jq -r '.data[] | "ID: \(.id)\nIndustry: \(.attributes.industry)\nTimezone: \(.attributes.timezone)"'

echo ""
echo "=== Lists ==="
curl -s -H "$AUTH" -H "$REV" "$KL_API/lists/" | \
  jq -r '.data[] | "\(.attributes.name) | ID: \(.id) | Created: \(.attributes.created)"'

echo ""
echo "=== Segments ==="
curl -s -H "$AUTH" -H "$REV" "$KL_API/segments/" | \
  jq -r '.data[] | "\(.attributes.name) | ID: \(.id) | Created: \(.attributes.created)"'

echo ""
echo "=== Flows ==="
curl -s -H "$AUTH" -H "$REV" "$KL_API/flows/" | \
  jq -r '.data[] | "\(.attributes.name) | Status: \(.attributes.status) | Created: \(.attributes.created)"'

echo ""
echo "=== Active Metrics ==="
curl -s -H "$AUTH" -H "$REV" "$KL_API/metrics/" | \
  jq -r '.data[:10] | .[] | "\(.attributes.name) | Integration: \(.attributes.integration.name // "custom")"'
```

**Phase 1 outputs:** Account info, lists, segments, flows, metrics

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Recent Campaigns ==="
curl -s -H "$AUTH" -H "$REV" "$KL_API/campaigns/?filter=equals(messages.channel,'email')&sort=-created_at" | \
  jq -r '.data[:10] | .[] | "\(.attributes.name) | Status: \(.attributes.status) | Sent: \(.attributes.send_time // "draft")"'

echo ""
echo "=== Flow Performance ==="
for flow_id in $(curl -s -H "$AUTH" -H "$REV" "$KL_API/flows/" | jq -r '.data[:5] | .[].id'); do
  name=$(curl -s -H "$AUTH" -H "$REV" "$KL_API/flows/$flow_id/" | jq -r '.data.attributes.name')
  echo "$name (ID: $flow_id) | Status: $(curl -s -H "$AUTH" -H "$REV" "$KL_API/flows/$flow_id/" | jq -r '.data.attributes.status')"
done

echo ""
echo "=== List Profiles Count ==="
for list_id in $(curl -s -H "$AUTH" -H "$REV" "$KL_API/lists/" | jq -r '.data[:5] | .[].id'); do
  name=$(curl -s -H "$AUTH" -H "$REV" "$KL_API/lists/$list_id/" | jq -r '.data.attributes.name')
  echo "$name | ID: $list_id"
done

echo ""
echo "=== Suppressed Profiles ==="
curl -s -H "$AUTH" -H "$REV" "$KL_API/profiles/?filter=equals(subscriptions.email.marketing.suppression.reason,'HARD_BOUNCE')&page[size]=1" | \
  jq -r '"Hard bounces in suppression: check total via pagination"'
```

## Output Format

```
KLAVIYO STATUS
==============
Account: {id} ({industry})
Lists: {count} | Segments: {count}
Active Flows: {count}/{total}
Recent Campaigns: {count}
Tracked Metrics: {count}
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

- **API revision header**: Klaviyo requires a revision date header — always include it
- **Rate limits**: 75 requests/second for most endpoints — use bulk endpoints for profiles
- **Flows vs Campaigns**: Flows are automated triggers; campaigns are one-time sends
- **Pagination**: All list endpoints are paginated — check `links.next` for more data

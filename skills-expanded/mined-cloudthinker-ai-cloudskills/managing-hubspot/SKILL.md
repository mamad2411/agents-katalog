---
name: managing-hubspot
description: |
  Use when working with Hubspot — hubSpot CRM and marketing platform management
  including contacts, companies, deals, tickets, pipelines, email campaigns,
  workflows, forms, and analytics. Covers pipeline health, deal velocity,
  contact engagement, marketing performance, and integration monitoring via the
  HubSpot API.
connection_type: hubspot
preload: false
---

# HubSpot Management Skill

Monitor and manage HubSpot CRM, marketing, and sales operations.

## MANDATORY: Discovery-First Pattern

**Always discover account info and object schemas before querying CRM data.**

### Phase 1: Discovery

```bash
#!/bin/bash
HS_API="https://api.hubapi.com"
AUTH="Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}"

echo "=== Account Info ==="
curl -s -H "$AUTH" "$HS_API/account-info/v3/details" | \
  jq -r '"Portal ID: \(.portalId)\nCompany: \(.companyName // "N/A")\nTimezone: \(.timeZone)\nCurrency: \(.companyCurrency)"'

echo ""
echo "=== CRM Object Counts ==="
for obj in contacts companies deals tickets; do
  count=$(curl -s -H "$AUTH" "$HS_API/crm/v3/objects/$obj?limit=1" | jq '.total // 0')
  echo "$obj: $count"
done

echo ""
echo "=== Deal Pipelines ==="
curl -s -H "$AUTH" "$HS_API/crm/v3/pipelines/deals" | \
  jq -r '.results[] | "\(.label) | ID: \(.id) | Stages: \(.stages | length)"'

echo ""
echo "=== Ticket Pipelines ==="
curl -s -H "$AUTH" "$HS_API/crm/v3/pipelines/tickets" | \
  jq -r '.results[] | "\(.label) | ID: \(.id) | Stages: \(.stages | length)"'

echo ""
echo "=== Workflows ==="
curl -s -H "$AUTH" "$HS_API/automation/v4/flows" | \
  jq -r '.results[:10] | .[] | "\(.name) | Enabled: \(.enabled) | Type: \(.type)"' 2>/dev/null || echo "Check workflows via dashboard"
```

**Phase 1 outputs:** Account info, object counts, pipelines, workflows

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Deal Pipeline Summary ==="
curl -s -H "$AUTH" "$HS_API/crm/v3/objects/deals?limit=100&properties=dealstage,amount,pipeline" | \
  jq -r '[.results[] | {stage: .properties.dealstage, amount: (.properties.amount // "0" | tonumber)}] | group_by(.stage) | map({stage: .[0].stage, count: length, total: [.[].amount] | add}) | .[] | "\(.stage): \(.count) deals (\(.total))"'

echo ""
echo "=== Recent Contacts (last 7 days) ==="
curl -s -H "$AUTH" "$HS_API/crm/v3/objects/contacts?limit=1&sorts=-createdate&filterGroups=[{\"filters\":[{\"propertyName\":\"createdate\",\"operator\":\"GTE\",\"value\":\"$(date -v-7d +%s000 2>/dev/null || date -d '7 days ago' +%s000)\"}]}]" | \
  jq -r '"New Contacts (7d): \(.total // "N/A")"' 2>/dev/null

echo ""
echo "=== Email Campaign Performance ==="
curl -s -H "$AUTH" "$HS_API/marketing/v3/emails/statistics?limit=5&orderBy=-sendDate" | \
  jq -r '.results[:5] | .[] | "\(.name[:40]) | Sent: \(.counters.sent) | Opens: \(.counters.open) | Clicks: \(.counters.click)"' 2>/dev/null || echo "Check marketing email stats via dashboard"

echo ""
echo "=== Forms ==="
curl -s -H "$AUTH" "$HS_API/marketing/v3/forms" | \
  jq -r '.results[:10] | .[] | "\(.name) | Type: \(.formType) | Submissions: \(.submissions // "N/A")"' 2>/dev/null

echo ""
echo "=== Integration Health ==="
curl -s -H "$AUTH" "$HS_API/integrations/v1/me" | \
  jq -r '"App ID: \(.appId // "direct token")\nScopes: \(.scopes // [] | join(", "))"' 2>/dev/null
```

## Output Format

```
HUBSPOT STATUS
==============
Portal: {id} ({company})
Contacts: {count} | Companies: {count}
Deals: {count} | Tickets: {count}
Deal Pipelines: {count}
Pipeline Value: {total_amount}
Active Workflows: {count}
New Contacts (7d): {count}
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

- **Rate limits**: 100 requests per 10 seconds for OAuth apps — use batch endpoints
- **API versions**: CRM v3 is current — v1/v2 endpoints are deprecated
- **Property limits**: Only 10 properties returned by default — specify properties parameter
- **Associations**: Objects are linked via associations API — separate from object queries
- **OAuth scopes**: Each API endpoint requires specific scopes — check token permissions

---
name: managing-close-crm
description: |
  Use when working with Close Crm — close CRM management including leads,
  contacts, opportunities, activities, sequences, smart views, and custom
  fields. Covers pipeline velocity, calling metrics, email outreach performance,
  sequence engagement, and team productivity analysis.
connection_type: close-crm
preload: false
---

# Close CRM Management Skill

Monitor and manage Close CRM sales operations and outreach.

## MANDATORY: Discovery-First Pattern

**Always discover organization structure and pipelines before querying leads or activities.**

### Phase 1: Discovery

```bash
#!/bin/bash
CLOSE_API="https://api.close.com/api/v1"
AUTH="-u ${CLOSE_API_KEY}:"

echo "=== Organization Info ==="
curl -s $AUTH "$CLOSE_API/me/" | \
  jq -r '"Org: \(.organizations[0].name)\nUser: \(.first_name) \(.last_name)\nEmail: \(.email)\nRole: \(.role)"'

echo ""
echo "=== Pipelines ==="
curl -s $AUTH "$CLOSE_API/pipeline/" | \
  jq -r '.data[] | "\(.name) | ID: \(.id) | Statuses: \(.statuses | length)"'

echo ""
echo "=== Pipeline Statuses ==="
curl -s $AUTH "$CLOSE_API/pipeline/" | \
  jq -r '.data[].statuses[] | "\(.label) | Type: \(.type) | Pipeline: \(.pipeline_name // "default")"'

echo ""
echo "=== Users ==="
curl -s $AUTH "$CLOSE_API/user/" | \
  jq -r '.data[] | "\(.first_name) \(.last_name) | Email: \(.email) | Role: \(.role)"'

echo ""
echo "=== Sequences ==="
curl -s $AUTH "$CLOSE_API/sequence/" | \
  jq -r '.data[] | "\(.name) | Status: \(.status) | Steps: \(.steps | length) | Enrolled: \(.subscription_count)"'
```

**Phase 1 outputs:** Org info, pipelines, users, sequences

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Lead Summary ==="
curl -s $AUTH "$CLOSE_API/report/lead/status/" | \
  jq -r '.data[] | "\(.status_label): \(.count) leads (\(.revenue // 0) revenue)"' 2>/dev/null || \
curl -s $AUTH "$CLOSE_API/lead/?_limit=1" | \
  jq -r '"Total Leads: \(.total_results)"'

echo ""
echo "=== Opportunity Pipeline ==="
curl -s $AUTH "$CLOSE_API/opportunity/?_limit=200&status_type=active" | \
  jq -r '"Open Opportunities: \(.total_results)\nTotal Value: \([.data[].value // 0] | add // 0)"'

echo ""
echo "=== Activity Summary (7 days) ==="
curl -s $AUTH "$CLOSE_API/report/activity/?" | \
  jq -r '"Calls: \(.calls_made // 0)\nEmails Sent: \(.emails_sent // 0)\nSMS Sent: \(.sms_sent // 0)\nMeetings: \(.meetings_completed // 0)"' 2>/dev/null || echo "Check activity report via dashboard"

echo ""
echo "=== Sequence Performance ==="
curl -s $AUTH "$CLOSE_API/sequence/" | \
  jq -r '.data[:5] | .[] | "\(.name) | Active: \(.active_subscription_count) | Completed: \(.completed_subscription_count) | Bounced: \(.bounced_subscription_count)"'

echo ""
echo "=== Smart Views ==="
curl -s $AUTH "$CLOSE_API/saved_search/?_limit=10" | \
  jq -r '.data[] | "\(.name) | Type: \(.type) | Shared: \(.is_shared)"'
```

## Output Format

```
CLOSE CRM STATUS
================
Org: {name} | Users: {count}
Leads: {count} | Open Opportunities: {count}
Pipeline Value: {amount}
7-Day Activity: {calls} calls, {emails} emails
Active Sequences: {count} ({enrolled} enrolled)
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

- **API key auth**: Close uses basic auth with API key as username — no password needed
- **Rate limits**: 600 requests/minute — monitor X-Rate-Limit headers
- **Lead vs Contact vs Opportunity**: Leads contain contacts; opportunities are deal tracking
- **Custom fields**: Use field IDs (custom.cf_xxx) not labels in API queries

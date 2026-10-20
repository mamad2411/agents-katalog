---
name: managing-mailchimp
description: |
  Use when working with Mailchimp — mailchimp email marketing platform
  management including audience lists, campaigns, automations, templates, and
  analytics. Covers list health, campaign performance, subscriber engagement,
  bounce and unsubscribe rates, and A/B test results.
connection_type: mailchimp
preload: false
---

# Mailchimp Management Skill

Monitor and manage Mailchimp email marketing campaigns and audiences.

## MANDATORY: Discovery-First Pattern

**Always discover audiences and account info before querying campaign data.**

### Phase 1: Discovery

```bash
#!/bin/bash
MC_API="https://${MAILCHIMP_DC}.api.mailchimp.com/3.0"
AUTH="anystring:${MAILCHIMP_API_KEY}"

echo "=== Account Info ==="
curl -s -u "$AUTH" "$MC_API/" | \
  jq -r '"Name: \(.account_name)\nEmail: \(.email)\nPlan: \(.pricing_plan_type)\nContacts: \(.total_subscribers)"'

echo ""
echo "=== Audiences (Lists) ==="
curl -s -u "$AUTH" "$MC_API/lists?count=20" | \
  jq -r '.lists[] | "\(.name) | ID: \(.id) | Members: \(.stats.member_count) | Unsub Rate: \(.stats.unsubscribe_count)/\(.stats.member_count)"'

echo ""
echo "=== Recent Campaigns ==="
curl -s -u "$AUTH" "$MC_API/campaigns?count=10&sort_field=send_time&sort_dir=DESC" | \
  jq -r '.campaigns[] | "\(.settings.title) | Status: \(.status) | Sent: \(.send_time // "draft")"'

echo ""
echo "=== Automations ==="
curl -s -u "$AUTH" "$MC_API/automations?count=20" | \
  jq -r '.automations[] | "\(.settings.title) | Status: \(.status) | Emails: \(.emails_sent)"'
```

**Phase 1 outputs:** Account plan, audiences, campaigns, automations

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Campaign Performance (last 10 sent) ==="
curl -s -u "$AUTH" "$MC_API/campaigns?count=10&status=sent&sort_field=send_time&sort_dir=DESC" | \
  jq -r '.campaigns[] | "\(.settings.title) | Opens: \(.report_summary.open_rate*100 | floor)% | Clicks: \(.report_summary.click_rate*100 | floor)% | Unsubs: \(.report_summary.unsubscribed)"'

echo ""
echo "=== Audience Growth (last 30 days) ==="
LIST_ID=$(curl -s -u "$AUTH" "$MC_API/lists?count=1" | jq -r '.lists[0].id')
curl -s -u "$AUTH" "$MC_API/lists/$LIST_ID/growth-history?count=30&sort_field=month&sort_dir=DESC" | \
  jq -r '.history[:5] | .[] | "\(.month): Subs=\(.subscribed) Unsubs=\(.unsubscribed) Cleaned=\(.cleaned)"'

echo ""
echo "=== Bounce Summary ==="
curl -s -u "$AUTH" "$MC_API/lists/$LIST_ID" | \
  jq -r '"Hard Bounces: \(.stats.hard_bounce_count) (\(.stats.hard_bounce_count * 100 / (.stats.member_count + 1) | floor)%)\nSoft Bounces: \(.stats.soft_bounce_count)\nCleaned: \(.stats.cleaned_count)"'

echo ""
echo "=== Top Performing Links ==="
CAMPAIGN_ID=$(curl -s -u "$AUTH" "$MC_API/campaigns?count=1&status=sent&sort_field=send_time&sort_dir=DESC" | jq -r '.campaigns[0].id')
curl -s -u "$AUTH" "$MC_API/reports/$CAMPAIGN_ID/click-details" | \
  jq -r '.urls_clicked[:5] | .[] | "\(.url[:50]) | Clicks: \(.total_clicks) | Unique: \(.unique_clicks)"'
```

## Output Format

```
MAILCHIMP STATUS
================
Account: {name} ({plan})
Total Contacts: {count}
Audiences: {count}
Avg Open Rate: {percent}% | Avg Click Rate: {percent}%
Bounces: {hard} hard, {soft} soft
Automations: {active}/{total} active
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

- **Data center prefix**: API key suffix determines DC (e.g., us21) — must match in URL
- **Rate limits**: 10 concurrent connections max — serialize requests
- **Audience vs Segment**: Audiences are top-level lists; segments are filtered subsets
- **Archived campaigns**: Archived campaigns don't appear in default queries — add status filter

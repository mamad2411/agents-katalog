---
name: analytics-audit
description: "Audit analytics implementations for tracking gaps and data quality issues."
category: data
tags: [analytics,tracking,data-quality,measurement]
complexity: intermediate
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Analytics Auditor

## Purpose
Ensure business decisions are based on complete, accurate analytics data.

## Audit Checklist

### Coverage Audit
```javascript
// Required events for SaaS product
const REQUIRED_EVENTS = [
  // Acquisition
  'page_view', 'utm_click', 'sign_up', 'sign_in',
  // Activation
  'onboarding_step_started', 'onboarding_step_completed', 'activation_event',
  // Engagement
  'feature_used', 'session_started', 'search_performed',
  // Revenue
  'upgrade_clicked', 'checkout_started', 'payment_completed', 'subscription_cancelled',
  // Retention
  'return_visit', 'notification_clicked',
];
```

### Data Quality SQL
```sql
-- Check for event volume anomalies
SELECT
  DATE(created_at) AS date,
  event_name,
  COUNT(*) AS count,
  LAG(COUNT(*)) OVER (PARTITION BY event_name ORDER BY DATE(created_at)) AS prev_day,
  ROUND((COUNT(*) - LAG(COUNT(*)) OVER (PARTITION BY event_name ORDER BY DATE(created_at)))::numeric
        / NULLIF(LAG(COUNT(*)) OVER (PARTITION BY event_name ORDER BY DATE(created_at)), 0) * 100, 1) AS pct_change
FROM analytics_events
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY 1, 2
HAVING ABS(pct_change) > 50  -- Flag 50%+ day-over-day swings
ORDER BY 1 DESC, ABS(pct_change) DESC;

-- Missing user properties
SELECT COUNT(*) FILTER (WHERE user_id IS NULL) / COUNT(*)::float AS pct_anonymous
FROM analytics_events
WHERE event_name = 'purchase_completed';
```

## Outputs
1. Analytics coverage report
2. Data quality test queries
3. Implementation gap priority list
4. Analytics governance documentation
5. Data validation CI tests
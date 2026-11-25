---
name: digital-advertising
description: "Manage digital advertising campaigns across Meta Ads, Google Ads, LinkedIn Ads, and TikTok Ads using their APIs. Covers campaign creation, budget management, audience targeting, performance analytics, and AI-powered optimization."
license: Apache 2.0
tags: ["digital-advertising", "meta-ads", "google-ads", "linkedin-ads", "tiktok-ads", "ppc", "adtech", "marketing"]
difficulty: intermediate
time_to_master: "10-16 weeks"
version: "1.0.0"
---

# Digital Advertising Operations

## Overview

Digital advertising platforms (Meta, Google, LinkedIn, TikTok) offer APIs that enable programmatic campaign management — creating ads, adjusting budgets, targeting audiences, and analyzing performance. AI agents with access to these APIs can optimize spend, generate ad variants, and provide real-time ROAS insights. This skill covers the major ad platform APIs and automation patterns.

## When to Use This Skill

- Building MCP servers for ad campaign management
- Automating cross-platform ad spend optimization
- Creating AI-powered ad copy generation and A/B testing
- Implementing budget pacing and automated bid strategies
- Building unified ad performance dashboards

## Core Concepts

### Platform API Comparison

| Platform | API | Auth | Spend Share | Best For |
|----------|-----|------|------------|----------|
| Google Ads | REST v16 | OAuth 2.0 | 28% digital | Search, YouTube, Display |
| Meta Ads | Marketing API v19 | System User Token | 22% digital | Social, Instagram, audience targeting |
| LinkedIn Ads | Marketing API | OAuth 2.0 | B2B dominant | B2B targeting by title/company |
| TikTok Ads | Marketing API | Access Token | Fastest growing | Gen Z/Millennial, video |

### Campaign Hierarchy

```
Ad Account
  └── Campaign (objective: awareness/traffic/conversions)
        └── Ad Set / Ad Group (targeting, budget, schedule)
              └── Ad / Creative (copy, image/video, CTA)
```

### Key Metrics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| CTR (Click-Through Rate) | Clicks / Impressions | 1-3% (search), 0.5-1.5% (social) |
| CPC (Cost Per Click) | Spend / Clicks | $0.50-$5.00 |
| CPM (Cost Per Mille) | (Spend / Impressions) × 1000 | $5-$30 |
| ROAS (Return on Ad Spend) | Revenue / Ad Spend | 3-5x |
| CPA (Cost Per Acquisition) | Spend / Conversions | Industry-dependent |
| Frequency | Impressions / Reach | < 3 per week |

## Implementation Guide

### Meta (Facebook/Instagram) Ads API

```typescript
// Create a campaign
const campaign = await fetch(
  `https://graph.facebook.com/v19.0/act_${adAccountId}/campaigns`,
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: "Q2 Product Launch",
      objective: "OUTCOME_SALES",
      status: "PAUSED",
      special_ad_categories: [],
      access_token: META_TOKEN,
    }),
  }
);

// Get campaign performance
const insights = await fetch(
  `https://graph.facebook.com/v19.0/${campaignId}/insights?` +
  new URLSearchParams({
    fields: "campaign_name,spend,impressions,clicks,ctr,cpc,actions,cost_per_action_type",
    date_preset: "last_7d",
    access_token: META_TOKEN,
  })
);
```

### Google Ads API

```python
from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_storage("google-ads.yaml")
ga_service = client.get_service("GoogleAdsService")

# Query campaign performance
query = """
    SELECT
        campaign.name,
        campaign.status,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.cost_per_conversion
    FROM campaign
    WHERE segments.date DURING LAST_7_DAYS
        AND campaign.status = 'ENABLED'
    ORDER BY metrics.cost_micros DESC
    LIMIT 20
"""

response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
for row in response:
    cost = row.metrics.cost_micros / 1_000_000
    print(f"{row.campaign.name}: ${cost:.2f} spend, {row.metrics.clicks} clicks, "
          f"{row.metrics.conversions:.0f} conversions")
```

### Cross-Platform MCP Server

```typescript
server.tool(
  "get_ad_performance",
  "Get ad performance metrics across all platforms for a date range",
  {
    platform: z.enum(["meta", "google", "linkedin", "tiktok", "all"]),
    dateRange: z.enum(["today", "yesterday", "last_7d", "last_30d", "this_month"]),
    metric: z.enum(["spend", "impressions", "clicks", "conversions", "roas"]).optional(),
  },
  async ({ platform, dateRange, metric }) => {
    const platforms = platform === "all"
      ? ["meta", "google", "linkedin", "tiktok"]
      : [platform];

    const results = await Promise.all(
      platforms.map(p => getPerformance(p, dateRange))
    );

    const combined = results.flat();
    const totalSpend = combined.reduce((s, r) => s + r.spend, 0);
    const totalRevenue = combined.reduce((s, r) => s + r.revenue, 0);

    return {
      content: [{
        type: "text",
        text: `Ad Performance (${dateRange}):\n` +
          `Total Spend: $${totalSpend.toLocaleString()}\n` +
          `Total Revenue: $${totalRevenue.toLocaleString()}\n` +
          `Blended ROAS: ${(totalRevenue / totalSpend).toFixed(2)}x\n\n` +
          combined.map(r =>
            `${r.platform} | ${r.campaign}: $${r.spend} spend, ${r.clicks} clicks, ` +
            `${r.conversions} conv, ${r.roas.toFixed(2)}x ROAS`
          ).join("\n"),
      }],
    };
  }
);

server.tool(
  "adjust_campaign_budget",
  "Adjust budget for a campaign (requires approval for increases > 20%)",
  {
    platform: z.enum(["meta", "google", "linkedin", "tiktok"]),
    campaignId: z.string(),
    newDailyBudget: z.number().describe("New daily budget in dollars"),
    reason: z.string(),
  },
  async ({ platform, campaignId, newDailyBudget, reason }) => {
    const current = await getCampaignBudget(platform, campaignId);
    const changePercent = ((newDailyBudget - current) / current) * 100;

    if (changePercent > 20) {
      return {
        content: [{
          type: "text",
          text: `⚠️ Budget increase of ${changePercent.toFixed(0)}% requires manager approval.\n` +
            `Current: $${current}/day → Proposed: $${newDailyBudget}/day\nReason: ${reason}`,
        }],
      };
    }

    await updateBudget(platform, campaignId, newDailyBudget);
    return {
      content: [{
        type: "text",
        text: `Budget updated: $${current}/day → $${newDailyBudget}/day (${changePercent > 0 ? "+" : ""}${changePercent.toFixed(0)}%)`,
      }],
    };
  }
);
```

## Budget Pacing Algorithm

```python
def check_budget_pacing(campaign, today):
    """Check if campaign spend is on pace with budget."""
    days_in_period = (campaign.end_date - campaign.start_date).days
    days_elapsed = (today - campaign.start_date).days
    expected_spend_pct = days_elapsed / days_in_period
    actual_spend_pct = campaign.spend_to_date / campaign.total_budget

    pace = actual_spend_pct / expected_spend_pct if expected_spend_pct > 0 else 0

    if pace > 1.15:
        return {"status": "overpacing", "action": "reduce_daily_budget", "pace": pace}
    elif pace < 0.85:
        return {"status": "underpacing", "action": "increase_daily_budget", "pace": pace}
    else:
        return {"status": "on_pace", "action": "maintain", "pace": pace}
```

## Best Practices

1. **Start campaigns PAUSED** — review before activating to avoid budget waste
2. **Use conversion APIs alongside pixels** — server-side tracking improves attribution
3. **Set frequency caps** — prevent ad fatigue (< 3 impressions/user/week)
4. **Automate budget pacing** — catch overspend/underspend before it impacts results
5. **A/B test creatives** — always run 3-5 ad variants per ad set
6. **Require approval for budget changes > 20%** — protect against runaway spend

## Resources

- [Meta Marketing API](https://developers.facebook.com/docs/marketing-apis/)
- [Google Ads API](https://developers.google.com/google-ads/api/docs/start)
- [LinkedIn Marketing API](https://learn.microsoft.com/en-us/linkedin/marketing/)
- [TikTok Marketing API](https://business-api.tiktok.com/portal/docs)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |

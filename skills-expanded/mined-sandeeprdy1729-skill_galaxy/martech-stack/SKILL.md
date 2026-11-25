---
name: martech-stack
description: "Integrate and automate marketing technology stacks including email marketing, analytics, CDP, attribution, and campaign orchestration across platforms like Mailchimp, Segment, Mixpanel, and Braze."
license: Apache 2.0
tags: ["martech", "marketing-automation", "email-marketing", "analytics", "cdp", "segment", "attribution"]
difficulty: intermediate
time_to_master: "10-16 weeks"
version: "1.0.0"
---

# MarTech Stack Integration

## Overview

The modern marketing technology (MarTech) stack comprises 10-30 tools spanning email, analytics, customer data platforms (CDPs), attribution, push notifications, and campaign orchestration. AI agents that can operate across this stack enable unified customer journeys, automated campaign optimization, and real-time personalization. This skill covers the key MarTech APIs and integration patterns.

## When to Use This Skill

- Building unified marketing automation with AI-powered orchestration
- Integrating Customer Data Platforms (CDPs) with campaign tools
- Automating email marketing workflows and A/B testing
- Implementing cross-channel attribution modeling
- Creating MCP servers for marketing operations

## Core Concepts

### MarTech Stack Architecture

```
                    ┌─────────────┐
                    │   CDP       │  (Segment, mParticle)
                    │  Unified    │
                    │  Customer   │
                    │  Profile    │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
    │   Email   │   │  In-App   │   │   Ads     │
    │ Mailchimp │   │  Braze    │   │ Meta/     │
    │ SendGrid  │   │ OneSignal │   │ Google    │
    └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Analytics  │  (Mixpanel, Amplitude, GA4)
                    │  Attribution│  (AppsFlyer, Branch)
                    └─────────────┘
```

### Key MarTech Categories

| Category | Purpose | Key Players | API Quality |
|----------|---------|-------------|-------------|
| CDP | Unified customer profiles | Segment, mParticle | Excellent |
| Email | Campaigns, transactional | Mailchimp, SendGrid, Klaviyo | Good |
| Product Analytics | User behavior tracking | Mixpanel, Amplitude, PostHog | Good |
| Push/In-App | Mobile engagement | Braze, OneSignal | Good |
| Attribution | Channel attribution | AppsFlyer, Branch, Triple Whale | Moderate |
| A/B Testing | Experimentation | LaunchDarkly, Statsig, Optimizely | Good |

## Implementation Guide

### Segment CDP Integration

```typescript
import Analytics from "@segment/analytics-node";

const analytics = new Analytics({ writeKey: process.env.SEGMENT_WRITE_KEY });

// Track user events
analytics.track({
  userId: "user_123",
  event: "Purchase Completed",
  properties: {
    orderId: "ORD-456",
    revenue: 99.99,
    currency: "USD",
    products: [
      { id: "SKU-001", name: "Pro Plan", price: 99.99 },
    ],
  },
});

// Identify user with traits
analytics.identify({
  userId: "user_123",
  traits: {
    email: "user@example.com",
    plan: "pro",
    company: "Acme Corp",
    lifecycleStage: "customer",
    ltv: 1199.88,
  },
});
```

### Email Marketing (Mailchimp)

```typescript
import mailchimp from "@mailchimp/mailchimp_marketing";

mailchimp.setConfig({ apiKey: process.env.MAILCHIMP_API_KEY, server: "us1" });

// Create and send a campaign
async function createCampaign(listId, subject, htmlContent) {
  const campaign = await mailchimp.campaigns.create({
    type: "regular",
    recipients: { list_id: listId },
    settings: {
      subject_line: subject,
      from_name: "Your Brand",
      reply_to: "hello@yourbrand.com",
    },
  });

  await mailchimp.campaigns.setContent(campaign.id, { html: htmlContent });

  // Send immediately or schedule
  await mailchimp.campaigns.send(campaign.id);
  return campaign;
}

// Get campaign performance
async function getCampaignReport(campaignId) {
  const report = await mailchimp.reports.getCampaignReport(campaignId);
  return {
    sent: report.emails_sent,
    opens: report.opens.unique_opens,
    openRate: report.opens.open_rate,
    clicks: report.clicks.unique_clicks,
    clickRate: report.clicks.click_rate,
    unsubscribes: report.unsubscribed,
    bounces: report.bounces.hard_bounces + report.bounces.soft_bounces,
  };
}
```

### Marketing Analytics MCP Server

```typescript
server.tool(
  "get_campaign_analytics",
  "Get performance metrics for marketing campaigns across channels",
  {
    channel: z.enum(["email", "push", "sms", "in-app", "all"]),
    period: z.enum(["last_7d", "last_30d", "last_90d"]),
  },
  async ({ channel, period }) => {
    const campaigns = await getCampaigns(channel, period);

    const summary = campaigns.map(c => ({
      name: c.name,
      channel: c.channel,
      sent: c.sent,
      delivered: c.delivered,
      opened: c.opened,
      clicked: c.clicked,
      converted: c.converted,
      revenue: c.revenue,
    }));

    const totals = {
      sent: summary.reduce((s, c) => s + c.sent, 0),
      revenue: summary.reduce((s, c) => s + c.revenue, 0),
    };

    return {
      content: [{
        type: "text",
        text: `Marketing Performance (${period}):\n` +
          `Total Sent: ${totals.sent.toLocaleString()} | Revenue: $${totals.revenue.toLocaleString()}\n\n` +
          summary.map(c =>
            `${c.name} (${c.channel}): ${c.sent} sent → ${c.opened} opened (${(c.opened/c.sent*100).toFixed(1)}%) → ${c.converted} converted → $${c.revenue}`
          ).join("\n"),
      }],
    };
  }
);
```

### Cross-Channel Customer Journey

```python
class CustomerJourney:
    """Track and orchestrate cross-channel customer touchpoints."""

    def get_journey(self, user_id):
        touchpoints = self.cdp.get_events(user_id, last_days=90)

        return {
            "user_id": user_id,
            "first_touch": touchpoints[0] if touchpoints else None,
            "last_touch": touchpoints[-1] if touchpoints else None,
            "total_touchpoints": len(touchpoints),
            "channels_used": list(set(t.channel for t in touchpoints)),
            "journey_stage": self.classify_stage(touchpoints),
            "next_best_action": self.recommend_action(touchpoints),
        }

    def recommend_action(self, touchpoints):
        """AI-powered next best action recommendation."""
        recent = touchpoints[-5:]
        if not recent:
            return {"action": "welcome_email", "channel": "email"}

        channels_used = set(t.channel for t in recent)
        if "email" in channels_used and "push" not in channels_used:
            return {"action": "push_notification", "channel": "push"}
        if any(t.event == "pricing_page_view" for t in recent):
            return {"action": "sales_outreach", "channel": "email", "priority": "high"}

        return {"action": "nurture_content", "channel": "email"}
```

## Best Practices

1. **CDP as the hub** — route all customer data through a CDP, not point-to-point
2. **Event naming conventions** — use consistent `Object Action` format (e.g., "Order Completed")
3. **Respect consent** — check opt-in status before every outbound touchpoint
4. **Deduplicate contacts** — merge profiles across channels using email/phone as keys
5. **Attribution windows** — set clear attribution windows (7-day click, 1-day view)
6. **A/B test everything** — subject lines, send times, content, and CTAs

## Resources

- [Segment Documentation](https://segment.com/docs/)
- [Mailchimp API](https://mailchimp.com/developer/)
- [Mixpanel API Reference](https://developer.mixpanel.com/)
- [Braze API Guide](https://www.braze.com/docs/api/)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |

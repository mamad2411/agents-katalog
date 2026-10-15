---
name: publisher-analytics
description: Pull performance data across connected accounts. Content audit, engagement report, and growth trends using Zernio post data and Instagram Insights.
requires:
  env:
    - ZERNIO_API_KEY
compatibility: Accounts must be connected via Zernio and have at least 7 days of posting data.
homepage: https://github.com/tfcbot/agent-video-team
source: https://github.com/tfcbot/agent-video-team
---

# Publisher — Analytics

Pull performance data across connected accounts and generate reports. Zernio provides post-level data via its API. For detailed engagement metrics (reach, impressions, follower demographics), the user should also reference Instagram Insights directly.

Base URL: `https://zernio.com/api/v1`
Auth header: `Authorization: Bearer $ZERNIO_API_KEY`

## Data Sources

**Zernio API** — post history, scheduling status, and platform-level metrics returned with post data:

```
GET /posts
Authorization: Bearer $ZERNIO_API_KEY
```

**Instagram Insights** — for detailed analytics (reach, impressions, follower growth, demographics), direct the user to check Instagram's native Insights in the app or Creator Studio.

## Report Types

### Content Audit

1. Pull post data from Zernio.
2. Filter for published posts and cross-reference with Instagram Insights.
3. Rank content by engagement (views, likes, shares, comments).
4. Identify patterns in top-performing content.
5. Flag underperforming content and recommend what to stop doing.

**Output:** Ranked list of posts with performance data and pattern analysis.

### Engagement Report

1. Pull the post list from Zernio for publishing history.
2. Ask the user for key metrics from Instagram Insights per account.
3. Report post frequency vs. target, engagement trends, posting gaps.
4. Compare accounts if running multiple channels.

**Output:** Per-account health dashboard with trends over time.

### Growth Trends

1. Pull post history from Zernio for the reporting period.
2. Combine with Instagram Insights data.
3. Calculate follower growth rate, view trends, engagement trend, best day of week.
4. Project next 30 days based on current trajectory.

**Output:** Growth summary with trajectory projection and recommended adjustments.

## Key Behaviors

- **Run a content audit after the first 7 days.** Earlier data is too noisy.
- **Engagement reports weekly. Growth trends monthly.**
- **Always compare against the channel strategy.**
- **If engagement is declining**, recommend format or hook changes before scaling back.
- **Don't over-index on follower count.** Profile visits and link clicks matter more.
- **Zernio provides post history.** For deep metrics, Instagram Insights is primary.

---
name: matomo-track
description: "Track web analytics and user behavior using Matomo at {{MATOMO_HOST}}:{{MATOMO_PORT}}."
metadata:
  openclaw:
    emoji: "📊"
---

# Matomo Analytics

Matomo is available at `http://{{MATOMO_HOST}}:{{MATOMO_PORT}}` within the Docker network.

## Track a Page View

```bash
curl "http://{{MATOMO_HOST}}:{{MATOMO_PORT}}/matomo.php?idsite=1&rec=1&action_name=Home&url=https://example.com"
```

## Query Reports

```bash
curl "http://{{MATOMO_HOST}}:{{MATOMO_PORT}}/index.php?module=API&method=VisitsSummary.get&idSite=1&period=day&date=today&format=JSON&token_auth=$MATOMO_TOKEN"
```

## Tips for AI Agents

- Matomo provides privacy-focused analytics as a Google Analytics alternative.
- Use the Reporting API to extract visitor data, page views, and conversions.
- Supports custom dimensions, events, and goal tracking.

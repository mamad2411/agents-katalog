---
name: filevine-data-connector
description: Skill for integrating and connecting data with Filevine using APIs and webhooks
---

# Filevine Data Connector Skill

## Overview
This skill assists users in connecting Filevine to external data sources, BI tools (like Power BI, Tableau), or custom internal applications. It focuses on the Filevine API v2, Webhooks, and data synchronization patterns.

## API Best Practices
1. **Authentication**: Use proper OAuth 2.0 or API key management based on the endpoint requirements.
2. **Rate Limiting**: Always account for Filevine's rate limits (usually ~5 requests per second). Implement retry logic with exponential backoff.
3. **Pagination**: Correctly handle paginated responses (offset/limit) to ensure all data is retrieved.
4. **Efficient Fetching**: Only request the fields and relations you actually need to reduce payload size and response time.

## Webhooks
- Use webhooks for real-time updates (e.g., Project Created, Phase Changed, Task Completed).
- Ensure your endpoint can handle duplicate deliveries and out-of-order events.
- Respond with a 2xx status quickly; perform heavy processing asynchronously.

## BI Tool Integration
- Recommend using automated ETL processes (e.g., via Domo, Fivetran, or custom scripts) to pull data into a data warehouse before connecting BI tools, rather than querying the live API directly from the BI dashboard.

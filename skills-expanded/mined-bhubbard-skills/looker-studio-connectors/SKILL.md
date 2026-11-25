---
name: looker-studio-connectors
description: "Guidelines for developing Looker Studio (formerly Data Studio) Community Connectors using Google Apps Script."
---

# Looker Studio Community Connectors

Looker Studio allows developers to build **Community Connectors** using Google Apps Script to fetch data from any internet-accessible API and bring it directly into Looker Studio reports.

## Core Functions

Every Community Connector must implement the following core Google Apps Script functions:

### 1. `getAuthType()`
Defines the authentication method required by the third-party service (e.g., `NONE`, `KEY`, `USER_PASS`, `OAUTH2`).

### 2. `getConfig()`
Defines the user-facing configuration options presented when a user adds the connector to a report (e.g., text inputs, dropdowns for selecting an account or date range).

### 3. `getSchema(request)`
Defines the schema (the list of fields/columns) returned by the connector. You must define whether each field is a `DIMENSION` or a `METRIC`, as well as its data type (e.g., `STRING`, `NUMBER`, `BOOLEAN`).

### 4. `getData(request)`
The core execution function. Looker Studio calls this function when a chart loads.
*   **Input:** Receives a request object containing the user's `configParams`, the `dateRange`, and the specific `fields` the chart requires.
*   **Execution:** You must fetch the data from your external API, parse it, and map it *exactly* to the requested fields.
*   **Output:** Returns an object containing the matching `schema` and the `rows` of data.

## Best Practices

*   **Caching:** Always implement `CacheService` to cache API responses and avoid hitting external rate limits, since Looker Studio will call `getData()` frequently as users interact with the dashboard.
*   **Semantic Types:** Use Looker Studio's semantic types (e.g., `YEAR_MONTH_DAY` or `CURRENCY_USD`) in `getSchema()` so data formats correctly out of the box.

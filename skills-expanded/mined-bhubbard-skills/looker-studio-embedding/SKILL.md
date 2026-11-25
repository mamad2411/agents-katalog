---
name: looker-studio-embedding
description: "Guidelines for embedding Looker Studio reports and utilizing the Linking API."
---

# Looker Studio Embedding and Linking

## 1. Iframe Embedding

Looker Studio reports can be embedded into standard HTML pages, intranets, or custom web apps using an iframe. 

**Requirements:**
*   Embedding must be explicitly enabled in the report settings (`File -> Embed report`).
*   Data access is controlled by the data source credentials. If the data source uses "Viewer's Credentials", the user viewing the iframe must be logged into a Google account with access to the underlying data.

## 2. The Linking API

The Linking API allows you to programmatically configure a Looker Studio report via a URL string. 

### Use Case
You can build a URL in your application that links to Looker Studio. When the user clicks it, Looker Studio will open a pre-configured report with specific filter values or specific connector configurations applied.

### URL Structure

You send a JSON-encoded, URL-encoded object as a query parameter. 

```javascript
const config = {
  "ds0.connectorConfig.account_id": "12345",
  "ds0.connectorConfig.date_range": "LAST_30_DAYS"
};

const encodedConfig = encodeURIComponent(JSON.stringify(config));
const url = `https://lookerstudio.google.com/reporting/create?c.reportId=YOUR_REPORT_ID&r.reportName=Custom+Report&ds.ds0.connectorName=YOUR_CONNECTOR_NAME&ds.ds0.config=${encodedConfig}`;
```

This is highly useful for SaaS platforms that want to generate isolated, templated dashboards for their clients with a single click.

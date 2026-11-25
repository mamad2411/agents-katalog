---
name: salesforce-integration
description: "Build integrations with Salesforce CRM using REST/SOAP APIs, Bulk API, and the MCP protocol. Covers authentication, SOQL queries, record management, webhook processing, and real-time sync patterns."
license: Apache 2.0
tags: ["salesforce", "crm", "api-integration", "soql", "enterprise", "mcp", "sales-automation"]
difficulty: intermediate
time_to_master: "8-14 weeks"
version: "1.0.0"
---

# Salesforce Integration

## Overview

Salesforce is the dominant CRM platform with 150K+ enterprise customers. Building integrations enables AI agents to query leads, update opportunities, manage contacts, and automate sales workflows. This skill covers the APIs, authentication flows, data model, and integration patterns needed to connect any system to Salesforce.

## When to Use This Skill

- Building MCP servers that expose Salesforce data to AI agents
- Automating lead scoring, opportunity updates, or pipeline reviews
- Syncing Salesforce data with marketing platforms or data warehouses
- Creating custom dashboards that pull from Salesforce
- Implementing Salesforce webhooks for real-time event handling

## Core Concepts

### Salesforce API Landscape

| API | Use Case | Data Volume | Format |
|-----|----------|-------------|--------|
| REST API | CRUD, queries, metadata | Single records | JSON |
| SOAP API | Complex operations, legacy | Single records | XML |
| Bulk API 2.0 | Mass data operations | 10K-100M records | CSV/JSON |
| Streaming API | Real-time events | Event stream | Bayeux |
| Metadata API | Config/deploy customizations | Schema changes | XML |
| Composite API | Multiple operations in one call | Up to 25 subrequests | JSON |

### Authentication: OAuth 2.0 Web Server Flow

```
┌──────────┐     ┌───────────────┐     ┌────────────┐
│  Client  │────►│ Salesforce    │────►│  Callback  │
│  App     │     │ Auth Endpoint │     │  URL       │
└──────────┘     └───────────────┘     └─────┬──────┘
                                             │auth code
                                             ▼
                                      ┌────────────┐
                                      │ Token       │
                                      │ Endpoint    │
                                      └─────┬──────┘
                                            │access_token
                                            │refresh_token
                                            ▼
                                      ┌────────────┐
                                      │ API Calls  │
                                      └────────────┘
```

### SOQL (Salesforce Object Query Language)

```sql
-- Find high-value open opportunities closing this quarter
SELECT Id, Name, Amount, StageName, CloseDate, Account.Name
FROM Opportunity
WHERE StageName != 'Closed Won'
  AND StageName != 'Closed Lost'
  AND Amount > 50000
  AND CloseDate = THIS_QUARTER
ORDER BY Amount DESC
LIMIT 20

-- Get contacts with recent activities
SELECT Id, Name, Email, Account.Name,
  (SELECT Subject, ActivityDate FROM ActivityHistories ORDER BY ActivityDate DESC LIMIT 5)
FROM Contact
WHERE Account.Industry = 'Technology'
  AND LastActivityDate = LAST_N_DAYS:30
```

## Implementation Guide

### MCP Server for Salesforce

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({ name: "salesforce-mcp", version: "1.0.0" });

// Tool: Search Salesforce records
server.tool(
  "search_salesforce",
  "Search Salesforce records using SOQL",
  {
    object: z.enum(["Account", "Contact", "Opportunity", "Lead", "Case"]),
    query: z.string().describe("Natural language search query"),
    limit: z.number().default(10),
  },
  async ({ object, query, limit }) => {
    const soql = buildSOQL(object, query, limit);
    const results = await sfClient.query(soql);

    return {
      content: [{
        type: "text",
        text: formatResults(results.records),
      }],
    };
  }
);

// Tool: Update a record
server.tool(
  "update_salesforce_record",
  "Update fields on a Salesforce record",
  {
    object: z.string(),
    recordId: z.string(),
    fields: z.record(z.unknown()).describe("Fields to update"),
  },
  async ({ object, recordId, fields }) => {
    await sfClient.sobject(object).update({ Id: recordId, ...fields });
    return {
      content: [{ type: "text", text: `Updated ${object} ${recordId}` }],
    };
  }
);
```

### Authentication Setup

```typescript
import jsforce from "jsforce";

// OAuth 2.0 with refresh token (recommended for production)
const oauth2 = new jsforce.OAuth2({
  clientId: process.env.SF_CLIENT_ID,
  clientSecret: process.env.SF_CLIENT_SECRET,
  redirectUri: process.env.SF_REDIRECT_URI,
});

const conn = new jsforce.Connection({ oauth2 });

// Auto-refresh expired tokens
conn.on("refresh", (accessToken) => {
  console.log("Token refreshed");
  // Store new access token securely
});

await conn.login(process.env.SF_USERNAME, process.env.SF_PASSWORD + process.env.SF_SECURITY_TOKEN);
```

### Bulk Data Operations

```typescript
async function bulkUpsertAccounts(records) {
  const job = conn.bulk.createJob("Account", "upsert", {
    extIdField: "External_Id__c",
    concurrencyMode: "Parallel",
  });

  const batch = job.createBatch();
  batch.execute(records);

  return new Promise((resolve, reject) => {
    batch.on("response", (results) => {
      const success = results.filter(r => r.success).length;
      const failed = results.filter(r => !r.success).length;
      resolve({ success, failed, errors: results.filter(r => !r.success) });
    });
    batch.on("error", reject);
  });
}
```

### Real-Time Events with Platform Events

```typescript
// Subscribe to Salesforce Platform Events
const channel = "/event/Order_Placed__e";
const replayId = -1; // -1 = new events only

conn.streaming.topic(channel).subscribe((message) => {
  console.log("Event received:", message);
  // Process: sync to warehouse, trigger fulfillment, etc.
});
```

## Common Integration Patterns

### Lead-to-Opportunity Pipeline Sync

```
Marketing Platform ──► Salesforce Lead ──► Qualify ──► Opportunity
                         │                                │
                         ▼                                ▼
                    Lead Scoring              Pipeline Dashboard
                    (AI-powered)              (Revenue Forecast)
```

### Data Warehouse Sync

```
Salesforce ──Bulk API──► Staging ──Transform──► Data Warehouse
                           │                        │
                      Incremental              Analytics/BI
                      (LastModifiedDate)       Dashboards
```

## Best Practices

1. **Use Bulk API for 200+ records** — REST API has a 100-record composite limit
2. **Always handle token refresh** — access tokens expire every 2 hours
3. **Respect API limits** — monitor daily API call consumption (varies by edition)
4. **Use Compound Fields wisely** — Address, Name are compound; query sub-fields directly
5. **Implement retry with backoff** for `REQUEST_LIMIT_EXCEEDED` errors
6. **Query selectively** — never `SELECT *`; specify only needed fields

## Resources

- [Salesforce REST API Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)
- [jsforce Library](https://jsforce.github.io/)
- [SOQL Reference](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |

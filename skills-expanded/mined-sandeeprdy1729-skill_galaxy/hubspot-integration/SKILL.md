---
name: hubspot-integration
description: "Build integrations with HubSpot CRM, Marketing Hub, and Sales Hub using REST APIs and webhooks. Covers contacts, deals, pipelines, email automation, and MCP server patterns for AI-driven CRM workflows."
license: Apache 2.0
tags: ["hubspot", "crm", "marketing-automation", "api-integration", "sales", "mcp"]
difficulty: intermediate
time_to_master: "6-10 weeks"
version: "1.0.0"
---

# HubSpot Integration

## Overview

HubSpot serves 200K+ customers across its CRM, Marketing, Sales, and Service Hubs. Unlike Salesforce's enterprise complexity, HubSpot offers a developer-friendly REST API with generous free-tier access, making it the most accessible CRM integration target. This skill covers authentication, core API operations, webhook handling, and AI agent integration patterns.

## When to Use This Skill

- Building CRM-connected AI agents for sales or marketing automation
- Syncing contacts, deals, and activities between HubSpot and other systems
- Automating lead nurturing workflows with AI-powered personalization
- Creating MCP servers that expose HubSpot data to Claude or other LLMs
- Implementing real-time deal pipeline analytics

## Core Concepts

### HubSpot API Structure

| Hub | Key Objects | API Endpoints |
|-----|------------|---------------|
| CRM | Contacts, Companies, Deals, Tickets | `/crm/v3/objects/{objectType}` |
| Marketing | Emails, Forms, Lists | `/marketing/v3/` |
| Sales | Meetings, Calls, Tasks, Quotes | `/crm/v3/objects/` |
| CMS | Pages, Blog posts, Files | `/cms/v3/` |

### Authentication

HubSpot supports two auth methods:

| Method | Use Case | Token Lifetime |
|--------|----------|---------------|
| Private App Token | Server-to-server, internal tools | No expiry (revokable) |
| OAuth 2.0 | Multi-tenant apps, marketplace | 30 min (refresh available) |

### Object Model

```
Company (1) ──► (N) Contacts
    │                   │
    │                   ▼
    │              (N) Deals ──► Pipeline Stages
    │                   │
    ▼                   ▼
Activities         Line Items
(Calls, Emails,    (Products,
 Meetings, Notes)   Quoted prices)
```

## Implementation Guide

### Basic API Operations

```typescript
import { Client } from "@hubspot/api-client";

const hubspot = new Client({ accessToken: process.env.HUBSPOT_TOKEN });

// Search contacts
const searchResponse = await hubspot.crm.contacts.searchApi.doSearch({
  filterGroups: [{
    filters: [{
      propertyName: "lifecyclestage",
      operator: "EQ",
      value: "lead",
    }],
  }],
  sorts: [{ propertyName: "createdate", direction: "DESCENDING" }],
  properties: ["firstname", "lastname", "email", "company", "lifecyclestage"],
  limit: 20,
});

// Create a deal
const deal = await hubspot.crm.deals.basicApi.create({
  properties: {
    dealname: "Acme Corp - Enterprise Plan",
    pipeline: "default",
    dealstage: "qualifiedtobuy",
    amount: "45000",
    closedate: "2026-06-30",
  },
  associations: [{
    to: { id: contactId },
    types: [{ associationCategory: "HUBSPOT_DEFINED", associationTypeId: 3 }],
  }],
});
```

### MCP Server for HubSpot

```typescript
server.tool(
  "search_hubspot_contacts",
  "Search HubSpot contacts by name, email, company, or lifecycle stage",
  {
    query: z.string().describe("Search term"),
    lifecycleStage: z.enum(["subscriber", "lead", "marketingqualifiedlead",
      "salesqualifiedlead", "opportunity", "customer"]).optional(),
    limit: z.number().default(10),
  },
  async ({ query, lifecycleStage, limit }) => {
    const filters = [{ propertyName: "hs_searchable_calculated_phone_number_country_code", operator: "HAS_PROPERTY" }];
    // Build filters from query and lifecycleStage
    const results = await hubspot.crm.contacts.searchApi.doSearch({
      query,
      filterGroups: lifecycleStage ? [{
        filters: [{ propertyName: "lifecyclestage", operator: "EQ", value: lifecycleStage }],
      }] : [],
      properties: ["firstname", "lastname", "email", "company", "lifecyclestage", "hs_lead_status"],
      limit,
    });

    return {
      content: [{
        type: "text",
        text: results.results.map(c => 
          `${c.properties.firstname} ${c.properties.lastname} | ${c.properties.email} | ${c.properties.company} | Stage: ${c.properties.lifecyclestage}`
        ).join("\n"),
      }],
    };
  }
);

server.tool(
  "get_deal_pipeline",
  "Get deals in a pipeline stage with amounts and close dates",
  {
    stage: z.string().describe("Pipeline stage name"),
    minAmount: z.number().optional(),
  },
  async ({ stage, minAmount }) => {
    const filters = [
      { propertyName: "dealstage", operator: "EQ", value: stage },
    ];
    if (minAmount) {
      filters.push({ propertyName: "amount", operator: "GTE", value: String(minAmount) });
    }

    const results = await hubspot.crm.deals.searchApi.doSearch({
      filterGroups: [{ filters }],
      properties: ["dealname", "amount", "dealstage", "closedate", "pipeline"],
      sorts: [{ propertyName: "amount", direction: "DESCENDING" }],
      limit: 20,
    });

    const total = results.results.reduce((sum, d) => sum + Number(d.properties.amount || 0), 0);
    return {
      content: [{
        type: "text",
        text: `Pipeline Stage: ${stage} | ${results.total} deals | Total: $${total.toLocaleString()}\n\n` +
          results.results.map(d =>
            `- ${d.properties.dealname}: $${Number(d.properties.amount).toLocaleString()} (Close: ${d.properties.closedate})`
          ).join("\n"),
      }],
    };
  }
);
```

### Webhook Processing

```typescript
import crypto from "crypto";

function verifyHubSpotWebhook(req, clientSecret) {
  const signature = req.headers["x-hubspot-signature-v3"];
  const timestamp = req.headers["x-hubspot-request-timestamp"];

  // Reject if timestamp > 5 minutes old
  if (Date.now() - Number(timestamp) > 300000) return false;

  const sourceString = `${req.method}${req.url}${JSON.stringify(req.body)}${timestamp}`;
  const hash = crypto.createHmac("sha256", clientSecret).update(sourceString).digest("base64");
  return crypto.timingSafeEqual(Buffer.from(hash), Buffer.from(signature));
}
```

## Rate Limits

| Tier | Limit | Burst |
|------|-------|-------|
| Free | 100 calls/10 sec | 110 |
| Starter | 100 calls/10 sec | 110 |
| Professional | 150 calls/10 sec | 160 |
| Enterprise | 200 calls/10 sec | 200 |

**Daily limit:** 250,000 calls for free/starter; 500,000 for pro/enterprise.

## Best Practices

1. **Use the official Node.js client** (`@hubspot/api-client`) over raw HTTP
2. **Batch API calls** — use `/batch/read` and `/batch/create` for multiple records
3. **Implement retry logic** for 429 (rate limit) responses with `Retry-After` header
4. **Use search API over list** — search supports filters, sorting, and pagination efficiently
5. **Subscribe to webhooks** for real-time sync instead of polling
6. **Cache property definitions** — custom properties rarely change; fetch once and cache

## Resources

- [HubSpot API Documentation](https://developers.hubspot.com/docs/api/overview)
- [HubSpot Node.js Client](https://github.com/HubSpot/hubspot-api-nodejs)
- [HubSpot Developer Portal](https://developers.hubspot.com/)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |

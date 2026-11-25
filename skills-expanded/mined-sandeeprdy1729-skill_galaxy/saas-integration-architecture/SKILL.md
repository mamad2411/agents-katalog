---
name: saas-integration-architecture
description: "Design and build robust SaaS-to-SaaS integrations including API gateway patterns, webhook management, data transformation, sync strategies, and iPaaS alternatives for connecting enterprise applications."
license: Apache 2.0
tags: ["saas", "integration", "api-gateway", "webhooks", "etl", "ipaas", "middleware", "enterprise"]
difficulty: advanced
time_to_master: "12-20 weeks"
version: "1.0.0"
---

# SaaS Integration Architecture

## Overview

Modern businesses use 100-300 SaaS applications that need to exchange data reliably. SaaS integration architecture covers the patterns, protocols, and infrastructure needed to connect these applications — from simple webhook handlers to complex bidirectional sync engines. As AI agents gain the ability to operate across SaaS tools, robust integration architecture becomes critical.

## When to Use This Skill

- Designing integration layers between multiple SaaS applications
- Building custom connectors when iPaaS tools are insufficient
- Implementing real-time bidirectional data sync
- Creating API gateways for unified access to multiple SaaS APIs
- Handling webhook management at scale (receiving, validating, processing)

## Core Concepts

### Integration Patterns

```
Point-to-Point          Hub-and-Spoke           Event-Driven
┌───┐   ┌───┐          ┌───┐                   ┌───┐
│ A │───│ B │          │ A │──┐                 │ A │──publish──┐
└───┘   └───┘          └───┘  │  ┌───────┐     └───┘           │
  │       │              │    ├──│  Hub  │──┐                   ▼
  │       │            ┌───┐  │  │(iPaaS)│  │  ┌───┐     ┌──────────┐
  └───────┘            │ B │──┘  └───────┘  ├──│ B │     │  Event   │
┌───┐   ┌───┐          └───┘              │  └───┘     │  Bus     │
│ C │───│ D │          ┌───┐              │  ┌───┐     └──────────┘
└───┘   └───┘          │ C │──────────────┘  │ C │           │
                       └───┘                 └───┘     subscribe
O(n²) connections      Centralized           │
                       management            ▼
                                        ┌───────┐
                                        │Process│
                                        └───────┘
```

### Sync Strategies

| Strategy | Latency | Complexity | Best For |
|----------|---------|------------|----------|
| **Polling** | Minutes | Low | Low-volume, simple |
| **Webhooks** | Seconds | Medium | Event-driven updates |
| **Change Data Capture** | Sub-second | High | Database-level sync |
| **Bidirectional Sync** | Seconds | Very High | Two-way data flow |
| **Batch ETL** | Hours | Medium | Analytics, reporting |

### Data Transformation Pipeline

```
Source API                 Transform               Target API
─────────                  ─────────               ──────────
{ "first_name": "Jane",   ┌──────────┐           { "name": {
  "last_name": "Doe",     │  Map     │             "first": "Jane",
  "email": "j@co.com",    │  Filter  │             "last": "Doe"
  "company": "Acme",   ──►│  Enrich  │──►         },
  "created": "2026-01-15" │  Validate│             "email": "j@co.com",
}                          └──────────┘             "org": "Acme",
                                                    "source": "crm",
                                                    "imported": "2026-03-31"
                                                  }
```

## Implementation Guide

### Webhook Management at Scale

```typescript
import crypto from "crypto";
import { Queue } from "bullmq";

const webhookQueue = new Queue("webhooks", { connection: redisConnection });

// Receive and queue webhooks (fast response)
app.post("/webhooks/:source", async (req, res) => {
  const { source } = req.params;

  // 1. Verify signature
  if (!verifyWebhookSignature(source, req)) {
    return res.status(401).send("Invalid signature");
  }

  // 2. Queue for async processing (respond fast)
  await webhookQueue.add(source, {
    source,
    headers: req.headers,
    body: req.body,
    receivedAt: Date.now(),
  }, {
    attempts: 3,
    backoff: { type: "exponential", delay: 5000 },
  });

  // 3. Respond immediately (most platforms require < 5s)
  res.status(200).send("OK");
});

// Process webhooks asynchronously
const worker = new Worker("webhooks", async (job) => {
  const { source, body } = job.data;

  switch (source) {
    case "stripe":
      await handleStripeEvent(body);
      break;
    case "hubspot":
      await handleHubSpotEvent(body);
      break;
    case "shopify":
      await handleShopifyEvent(body);
      break;
  }
}, { connection: redisConnection });

function verifyWebhookSignature(source, req) {
  const secrets = {
    stripe: process.env.STRIPE_WEBHOOK_SECRET,
    hubspot: process.env.HUBSPOT_CLIENT_SECRET,
    shopify: process.env.SHOPIFY_WEBHOOK_SECRET,
  };

  // Each platform has different signature verification
  switch (source) {
    case "stripe":
      return stripe.webhooks.constructEvent(req.rawBody, req.headers["stripe-signature"], secrets.stripe);
    case "shopify":
      const hmac = crypto.createHmac("sha256", secrets.shopify).update(req.rawBody).digest("base64");
      return crypto.timingSafeEqual(Buffer.from(hmac), Buffer.from(req.headers["x-shopify-hmac-sha256"]));
    default:
      return false;
  }
}
```

### Bidirectional Sync Engine

```python
class BidirectionalSync:
    """Sync records between two SaaS systems with conflict resolution."""

    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.sync_state = SyncStateStore()

    async def sync(self, object_type):
        # Get changes from both sides since last sync
        last_sync = self.sync_state.get_last_sync(object_type)

        source_changes = await self.source.get_changes(object_type, since=last_sync)
        target_changes = await self.target.get_changes(object_type, since=last_sync)

        # Detect conflicts (same record changed in both)
        conflicts = self.detect_conflicts(source_changes, target_changes)

        # Apply non-conflicting changes
        for change in source_changes:
            if change.record_id not in conflicts:
                await self.target.apply_change(change)

        for change in target_changes:
            if change.record_id not in conflicts:
                await self.source.apply_change(change)

        # Resolve conflicts (last-write-wins or manual)
        for conflict in conflicts:
            resolved = self.resolve_conflict(conflict)
            await self.source.apply_change(resolved)
            await self.target.apply_change(resolved)

        self.sync_state.update_last_sync(object_type, datetime.utcnow())

    def resolve_conflict(self, conflict):
        """Last-write-wins conflict resolution."""
        if conflict.source_modified > conflict.target_modified:
            return conflict.source_version
        return conflict.target_version
```

### Data Mapping Framework

```typescript
interface FieldMapping {
  source: string;       // Source field path (dot notation)
  target: string;       // Target field path
  transform?: (value: any) => any;
  required?: boolean;
  default?: any;
}

class DataMapper {
  constructor(private mappings: FieldMapping[]) {}

  map(sourceRecord: Record<string, any>): Record<string, any> {
    const result: Record<string, any> = {};

    for (const mapping of this.mappings) {
      let value = this.getNestedValue(sourceRecord, mapping.source);

      if (value === undefined) {
        if (mapping.required) throw new Error(`Missing required field: ${mapping.source}`);
        value = mapping.default;
      }

      if (mapping.transform && value !== undefined) {
        value = mapping.transform(value);
      }

      if (value !== undefined) {
        this.setNestedValue(result, mapping.target, value);
      }
    }

    return result;
  }
}

// Example: Map HubSpot contacts to Salesforce leads
const hubspotToSalesforce = new DataMapper([
  { source: "properties.firstname", target: "FirstName" },
  { source: "properties.lastname", target: "LastName", required: true },
  { source: "properties.email", target: "Email", required: true },
  { source: "properties.company", target: "Company" },
  { source: "properties.phone", target: "Phone" },
  {
    source: "properties.lifecyclestage",
    target: "Status",
    transform: (stage) => ({
      subscriber: "Open",
      lead: "Open",
      marketingqualifiedlead: "Working",
      salesqualifiedlead: "Working",
      opportunity: "Qualified",
      customer: "Converted",
    }[stage] || "Open"),
  },
]);
```

### Rate Limiting and Retry

```typescript
class RateLimitedClient {
  private queue: PQueue;

  constructor(private maxPerSecond: number) {
    this.queue = new PQueue({
      concurrency: maxPerSecond,
      interval: 1000,
      intervalCap: maxPerSecond,
    });
  }

  async request(config: RequestConfig): Promise<Response> {
    return this.queue.add(async () => {
      for (let attempt = 0; attempt < 3; attempt++) {
        try {
          const response = await fetch(config.url, config);
          if (response.status === 429) {
            const retryAfter = parseInt(response.headers.get("Retry-After") || "5");
            await sleep(retryAfter * 1000);
            continue;
          }
          return response;
        } catch (error) {
          if (attempt === 2) throw error;
          await sleep(Math.pow(2, attempt) * 1000);
        }
      }
    });
  }
}
```

## Best Practices

1. **Idempotent operations** — use external IDs to prevent duplicate records on retry
2. **Queue webhook processing** — respond to webhooks immediately, process async
3. **Verify all webhook signatures** — never trust unverified webhook payloads
4. **Implement circuit breakers** — stop syncing if error rate exceeds threshold
5. **Log every transformation** — maintain audit trail of data changes
6. **Handle pagination** — never assume APIs return complete datasets
7. **Map fields explicitly** — never auto-map; field names differ across platforms

## Resources

- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/)
- [Zapier vs Custom Integration Guide](https://zapier.com/blog/build-vs-buy-integrations/)
- [BullMQ (Queue Library)](https://docs.bullmq.io/)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |

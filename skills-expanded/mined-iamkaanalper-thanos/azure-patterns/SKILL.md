---
name: azure-patterns
description: Azure Functions, Cosmos DB modeling, Service Bus patterns, Bicep templates. Grok-native with Production Contract, hooks, compound, palace.
when-to-use: When building Azure/serverless or Cosmos-heavy features, especially with backend-dev, devops, or azure-expert agent. Pair for migrations or new services.
---

# Azure Patterns (Grok Port)

Production patterns for Azure Functions, Cosmos DB, Service Bus, and Bicep IaC. Grok-native port with full Production Contract enforcement, hooks integration, compound self-improvement, palace memory, and two-pass claim-verification.

## Azure Functions (v4 Node/TypeScript + triggers)
```ts
import { app, HttpRequest, HttpResponseInit, InvocationContext } from '@azure/functions';

app.http('getOrder', {
  methods: ['GET'],
  authLevel: 'function',
  route: 'orders/{orderId}',
  handler: async (request: HttpRequest, context: InvocationContext): Promise<HttpResponseInit> => {
    const orderId = request.params.orderId;
    context.log(`Processing order: ${orderId}`);
    try {
      const order = await orderService.getById(orderId);
      if (!order) return { status: 404, jsonBody: { error: 'Order not found' } };
      return { status: 200, jsonBody: order };
    } catch (error) {
      context.error('Failed to get order', error);
      return { status: 500, jsonBody: { error: 'Internal server error' } };
    }
  },
});

// Service Bus trigger with retry / poison handling
app.serviceBusTopic('processOrderEvent', {
  topicName: 'order-events',
  subscriptionName: 'order-processor',
  connection: 'ServiceBusConnection',
  handler: async (message, context) => {
    // idempotency + dead-letter on repeated poison
  },
});
```

## Cosmos DB Modeling (partition + indexing)
- Choose partition key for high-cardinality + even distribution (e.g. userId or /tenantId + /userId composite).
- Avoid cross-partition queries in hot paths; use change feed for denormalization.
- Indexing policy: exclude large arrays/blobs by default; include only queried paths.
- Soft deletes + TTL for GDPR "right to be forgotten" cascades.

Example container:
```json
{
  "id": "orders",
  "partitionKey": { "paths": ["/userId"], "kind": "Hash" },
  "indexingPolicy": {
    "indexingMode": "consistent",
    "includedPaths": [{ "path": "/*" }],
    "excludedPaths": [{ "path": "/largePayload/*" }]
  }
}
```

## Service Bus Patterns (exactly-once, sessions, dead-letter)
- Use MessageId + dedup for idempotency.
- Sessions for ordered processing per aggregate.
- Dead-letter queue + poison count handling; move to "manual review" topic after N retries.
- Prefetch + batching for throughput.

## Bicep / ARM IaC Best Practices
- Modules for every reusable component (vnet, sql, func app).
- Use parameters + secureString for secrets (never hardcode).
- Tagging strategy: environment, costCenter, owner, managedBy=terraform-or-bicep.
- State: use remote backend (storage account + SAS or managed identity).
- Drift detection in CI via `az deployment group what-if`.

## Grok Integration (Production Contract)
- Primary: azure-expert + backend-dev + devops.
- Fire on_infra_change / on_db_change / on_api_feature when Azure resources, Cosmos containers, or Service Bus topics are added/changed.
- Pre-Flight (mandatory): "Partition key chosen? Cross-partition query risk? Secret injection via Key Vault? Retry + DLQ strategy? Cost guardrails (budgets/alerts)?"
- Ledger: every infra mutation, schema change, or connection string rotation recorded with task_id + diff.
- Handoff: Bicep diff, partition key rationale, throughput estimate, secret ref (no values), rollback (previous slot or ARM template), observability (App Insights queries).
- Friction + compound: "Cold start latency on consumption plan broke p95" or "Cosmos RU burst from missing composite index" → compound to preflight rules, linter policies, or skill defaults.
- Palace: "Chose Cosmos + Service Bus sessions for this bounded context because ordering per tenant required; rejected Event Grid because no sessions".
- Claim-verification: Two-pass required. Hypothesize from grep "Cosmos container" → read_file actual bicep / ARM / portal export → "container 'orders' with partition /userId exists at infra/cosmos.bicep:42 ✓VERIFIED". Never claim "partition safe" or "idempotent" without reading the real definition.
- Pair with: aws-patterns (multi-cloud), sast-patterns (secret scanning in IaC), gdpr-compliance (data residency + erasure in Cosmos), test-enforcement (infra + contract tests), caching-patterns (Cosmos point reads as cache).

## When to Activate
- New Azure Function, Cosmos container, Service Bus topic, or Bicep module.
- Swarm Phase 2 (infra/backend) and Phase 3 review.
- Before any deploy that touches Azure resources or data plane.
- PRs with .bicep, azure-pipelines, or Functions code.
- Cost or compliance reviews (shipper + verifier + compliance-expert).

## Quick Commands
- Deploy: az deployment group create --template-file main.bicep ...
- What-if: az deployment group what-if ...
- Cosmos: az cosmosdb sql container create ...
- Logs: az monitor app-insights query ...

See .grok/skills/aws-patterns/SKILL.md, kubernetes-patterns, backend-patterns, api-patterns, preflight, memory-palace + layered-recall (for prior Azure decisions), compound-learnings.

Production Contract: ledger + structured handoff + preflight + friction capture on every non-trivial Azure change. Always use least-privilege + Key Vault refs. Verify actual deployed state, not just code.

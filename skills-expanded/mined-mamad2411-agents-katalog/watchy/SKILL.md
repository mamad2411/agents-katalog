---
name: watchy
description: >-
  Integrate AWS Lambda projects with Watchy — capture errors with criticality
  and business context, then query them via MCP for production-aware debugging.
  Use when a user wants to: track Lambda errors, set up error reporting for
  serverless apps, connect their project to Watchy, enable production-aware
  coding with AI agents, or instrument Lambda handlers. Triggers include:
  "set up watchy", "capture Lambda errors", "error tracking for Lambda",
  "instrument my handlers", "connect to watchy", "production-aware debugging".
---

# Watchy

Integrate your AWS Lambda project with [Watchy](https://watchy.dev) — the operational graph for serverless teams.

**What this skill does:**
1. Helps you **capture errors** from Lambda handlers with criticality levels and business context
2. Errors flow into Watchy's operational graph (Stack -> Lambda -> API Endpoint)
3. AI agents **query real errors** via Watchy's MCP server — stack traces, not just metric counts

**No npm packages required.** You generate a small service file (~120 lines) using plain `fetch()`.

## How to Use This Skill (Agent Workflow)

**Do NOT just generate code immediately.** Follow this interactive workflow to help the developer capture the right errors with the right context and criticality.

Link: references/agent-workflow.md

## Two Parts

### Part 1: Capture (this skill)

The agent analyzes your codebase, asks what matters, and generates error capture code tailored to your handlers — with per-handler criticality and business context.

```typescript
import { wrapHandler, captureError } from './lib/watchy';

// Auto-catch with criticality + context extraction
export const handler = wrapHandler(async (event, context) => {
  const order = await createOrder(event.body);
  return { statusCode: 200, body: JSON.stringify(order) };
}, {
  criticality: 'critical',
  contextExtractor: (event) => ({ orderId: event.body?.orderId, userId: event.body?.userId }),
});

// Manual capture in existing catch blocks
catch (err) {
  captureError(err, context, {
    criticality: 'critical',
    context: { orderId, amount, currency },
  });
  throw err;
}
```

### Part 2: Query (MCP)

Once errors flow into Watchy, AI agents query them via the MCP `search_errors` tool:

```
Agent: "What errors happened in the last 24 hours?"
→ MCP search_errors returns: real stack traces, criticality, business context, linked to your operational graph

Agent: "Show me critical errors in the payments stack"
→ MCP returns: TimeoutError in processPayment, 47 occurrences, context: { orderId, amount }
```

To set up MCP, see the `watchy-mcp-setup` skill.

## Prerequisites

- A Watchy account with at least one connected AWS account
- A Watchy API key with `write:errors` scope (Settings -> API Keys)
- `WATCHY_API_KEY` environment variable set on your Lambda functions

## Criticality Levels

Every captured error has a criticality level that determines how it's prioritized:

| Level | When to use | Examples |
|---|---|---|
| `critical` | Revenue impact, data loss, security breach | Payment processing, data mutations, auth failures |
| `high` | User-facing failures, SLA violations | API responses, form submissions, file uploads |
| `medium` | Degraded experience, retryable failures | Cache misses, slow queries, partial feature failure |
| `low` | Background tasks, non-blocking operations | Analytics, notifications, cleanup jobs |

## Context — The Flexible Bag

Every error carries a `context` object — free-form JSON where you pack whatever makes debugging useful. The agent suggests context fields based on what each handler does.

```typescript
// Payment handler → pack business data
{ orderId, userId, amount, currency, paymentProvider: 'stripe' }

// Auth handler → pack identity data
{ userId, authMethod: 'oauth', provider: 'google' }

// Background job → pack progress data
{ batchId, processedCount: 47, totalCount: 100, retryable: true }
```

## References

- **Interactive workflow** (step-by-step for agents): references/agent-workflow.md
- **API specification** (endpoint, schemas, rate limits): references/api-reference.md
- **Code patterns** (complete service file + integration patterns): references/lambda-patterns.md

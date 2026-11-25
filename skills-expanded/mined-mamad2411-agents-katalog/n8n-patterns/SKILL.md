---
name: n8n-patterns
description: N8N workflow patterns and node reference. Use when building, debugging, or optimizing n8n workflows. Covers node cheat sheet, common workflow patterns, ecommerce integrations, error handling, and best practices.
license: Internal
metadata:
  author: trngthnh369
  version: "1.0.0"
---

# N8N Patterns

> **⚠️ IMPORTANT (2026-04-21):** `n8n-mcp` server is NOT installed. For live workflow manipulation use `n8nctl` CLI (see `n8nctl` skill), or REST via `$N8N_HOST` + `$N8N_API_KEY` as fallback.

Quick reference for building n8n workflows.

## Node Cheat Sheet

### Trigger Nodes
| Node | Use When | Key Config |
|------|----------|------------|
| **Webhook** | External service calls your workflow | Method, Path, Auth (Header/Basic), Response Mode |
| **Schedule** | Time-based automation | Cron expression or interval |
| **n8n Trigger** | React to n8n events | Workflow activated/error/updated |
| **Email Trigger (IMAP)** | New email arrives | Mailbox, folder, unseen only |

### Core Logic Nodes
| Node | Use When | Key Config |
|------|----------|------------|
| **IF** | Binary branching | Condition (string/number/boolean/date) |
| **Switch** | Multi-way branching | Rules or expression matching |
| **Merge** | Combine data from branches | Mode: Append/Keep Key Matches/Combine |
| **Loop Over Items** | Process items one-by-one | Batch size (use for rate-limited APIs) |
| **Wait** | Pause/resume workflow | Duration, webhook resume, or specific time |
| **Code** | Custom JS/Python logic | Language, run once vs per item |

### Data Nodes
| Node | Use When | Key Config |
|------|----------|------------|
| **HTTP Request** | Call any REST API | Method, URL, Auth, Body, Pagination |
| **Set** | Transform/rename fields | Assignments (keep only set fields option) |
| **Aggregate** | Summarize items → 1 item | Operation: concatenate, count, sum, etc. |
| **Split Out** | 1 item → many items | Field to split, include other fields |
| **Sort** | Order items | Field, direction |
| **Limit** | Trim item count | Max items |
| **Remove Duplicates** | Deduplicate | Compare field |
| **Date & Time** | Parse/format dates | Operation, format, timezone |

### Output Nodes
| Node | Use When | Key Config |
|------|----------|------------|
| **Respond to Webhook** | Return data to caller | Response code, body, headers |
| **Send Email** | SMTP email delivery | To, Subject, Body (HTML/text) |
| **Slack/Discord/Telegram** | Chat notifications | Channel, message format |

## Common Workflow Patterns

### Pattern 1: Webhook → Process → Respond
```
Webhook → Set (extract fields) → HTTP Request (external API) → Respond to Webhook
```
Use for: API proxy, form submissions, payment callbacks.

### Pattern 2: Schedule → Fetch → Notify
```
Schedule → HTTP Request (fetch data) → IF (condition) → Slack/Email (notify)
```
Use for: monitoring, daily reports, stock alerts.

### Pattern 3: Webhook → Queue → Batch Process
```
Webhook → Respond to Webhook (202 Accepted) → Wait (batch window) → Aggregate → Process
```
Use for: high-volume webhooks, batch operations.

### Pattern 4: Error → Retry → Alert
```
[Main Flow] → Error Trigger → Wait (exponential backoff) → [Retry Main] → IF (max retries) → Slack (alert)
```
Use for: unreliable APIs, network issues.

### Pattern 5: Pagination Loop
```
Loop Over Items → HTTP Request (page N) → IF (has next page) → [back to Loop] / [exit]
```
Config HTTP Request pagination: `Response Contains Next URL` or `Offset-based`.

## Ecommerce Integration Patterns

### Product Sync (Platform A → Platform B)
```
Schedule (hourly)
  → HTTP Request (fetch products from A, paginated)
  → Code (transform A format → B format)
  → Loop Over Items (batch 50, respect rate limits)
    → HTTP Request (upsert to B)
  → IF (any errors)
    → Slack (error report)
```

### Order Webhook Processing
```
Webhook (order.created from platform)
  → Set (normalize order fields)
  → HTTP Request (check inventory)
  → IF (in stock)
    → HTTP Request (confirm order on platform)
    → HTTP Request (create fulfillment)
  → ELSE
    → HTTP Request (cancel/hold order)
    → Email (notify ops team)
```

### Price/Inventory Sync
```
Schedule (every 15min)
  → HTTP Request (fetch inventory from ERP/source)
  → Merge (match with platform products by SKU)
  → IF (qty or price changed)
    → Loop Over Items
      → HTTP Request (update platform)
```

## HTTP Request Tips

### Authentication patterns
```
# Header Auth (Haravan, Shopify)
Header: X-Shopify-Access-Token = {{$credentials.token}}

# Query Param Signing (Shopee, Lazada, TikTok)
# Use Code node to generate signature, then pass in HTTP Request
URL: {{$json.signed_url}}

# OAuth2 (most platforms)
Use n8n's built-in OAuth2 credential type
```

### Pagination
- **Cursor-based**: Set pagination to "Response Contains Next URL", extract from `next` field
- **Offset-based**: Use Loop, increment offset by page_size each iteration
- **Page number**: Use Loop, increment page param

### Rate Limiting
- Use `Loop Over Items` with batch size matching API limits
- Add `Wait` node (1-2s) between batches
- Check response headers for `X-RateLimit-Remaining`

## Error Handling Best Practices

1. **Always set Error Workflow** on production workflows
2. Use **retry on fail** (Settings tab) for HTTP Request nodes: 3 retries, 1s wait
3. **Dead letter pattern**: Failed items → separate workflow or database table for manual review
4. Log errors with context: workflow name, node name, item index, error message
5. Set **timeout** on Wait nodes to prevent zombie executions

## n8n Expressions Quick Reference

```javascript
// Access input data
{{ $json.fieldName }}
{{ $json['nested.field'] }}

// Previous node data  
{{ $('NodeName').item.json.field }}

// All items from node
{{ $('NodeName').all() }}

// Current item index
{{ $itemIndex }}

// Environment variable
{{ $env.MY_VAR }}

// Date/time
{{ $now.toISO() }}
{{ $today.format('yyyy-MM-dd') }}

// Conditional
{{ $json.status === 'active' ? 'yes' : 'no' }}
```

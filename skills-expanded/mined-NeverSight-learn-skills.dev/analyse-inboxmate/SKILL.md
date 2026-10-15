---
name: analyse-inboxmate
description: Reference guide for understanding the InboxMate ecosystem - architecture, repos, pipeline, CRM states, metrics, and how to query each system. Use when starting any InboxMate-related work.
---

# InboxMate Ecosystem Reference

Use this skill to understand the InboxMate product, its architecture, outreach pipeline, and how to query data across systems.

## Architecture

InboxMate is a module (`chatwidget`) within the **AgentHub** platform — a full-stack Nuxt 3 + Supabase + Socket.IO SaaS.

### Repos & Key Files

| Repo | Purpose | Key Files |
|---|---|---|
| **agenthub** | Full-stack app (InboxMate + AgentHub) | `server/api/mcp.post.ts` (demo MCP), `app/pages/demo.vue` (demo page), `server/utils/scraping.ts` (Tavily/Firecrawl), `server/utils/subscriptionUtils.ts` (tiers), `app/components/InboxMatePricingModal.vue` |
| **notification-service** | Email drafts, templates, funnel analytics | `src/routes/drafts.ts` (draft CRUD), `src/routes/stats.ts` + `frontend/pages/funnel.vue` (funnel) |
| **psquared-websites** | Marketing sites | `apps/inboxmate/` (inboxmate.psquared.dev), `apps/psquared/` (psquared.dev) |
| **psquared-skills** | Pipeline skills | `skills/` directory |

### URLs

| Service | URL |
|---|---|
| InboxMate app | `app.psquared.dev` (chatwidget module) |
| Demo pages | `demo.inboxmate.psquared.dev/?id=<demoId>` |
| Marketing site | `inboxmate.psquared.dev` |
| Company site | `psquared.dev` |
| Notification admin | `notifications.psquared.dev/drafts` |
| CRM | `crm.psquared.dev` |
| Analytics | `ackee.psquared.dev` |

## Demo Pipeline

```
/find-leads [N]          → CRM companies + people (German B2B, UWG-compliant)
  ↓
/inboxmate-batch-demo    → Demos created, opportunities at SCREENING/PENDING_REVIEW
  ↓
/review-demos            → demoStatus: OK_TO_SEND or NEEDS_FIX
  ↓
/fix-demos               → Fixes applied, reset to PENDING_REVIEW
  ↓
/plan-campaign           → CRM campaign created, opportunities linked with shared deadline
  ↓
/setup-email-drafts      → Email drafts at notifications.psquared.dev/drafts
  ↓
Human review + send      → demoStatus: SENT, outreachSentAt timestamped
  ↓
/check-outreach-status   → Follow-up drafts created (5+ days after send)
  ↓
/check-demo-analytics    → Pipeline health report (Ackee + CRM)
  ↓
/refurbish-demos         → Upgrade knowledge for campaign demos (clear + re-scrape via MCP)
```

## CRM State Machine (Twenty CRM)

### Opportunity.demoStatus
| Status | Meaning |
|---|---|
| `PENDING_REVIEW` | Demo built, awaiting QA |
| `OK_TO_SEND` | QA passed, ready for outreach |
| `NEEDS_FIX` | QA failed, needs corrections |
| `SENT` | Initial outreach email sent |
| `FOLLOW_UP_SENT` | Follow-up email sent |
| `SKIP_FAULTY_WEBSITE` | Website unreachable/broken |
| `SKIP_IRRELEVANT` | Company not a fit |
| `SKIPPED` | Generic skip |
| `DISQUALIFIED` | Permanently excluded |

### Opportunity.stage
| Stage | Meaning |
|---|---|
| `NEW` | Fresh lead, no outreach |
| `SCREENING` | Outreach phase |
| `MEETING` | Responded / call scheduled |
| `PROPOSAL` | Quoted or decision-maker demo |
| `CUSTOMER` | Paying customer |

### Campaign Structure
Campaigns group opportunities into sendable batches with shared `offerExpiresAt` and `offerText`. Created by `/plan-campaign`, consumed by `/setup-email-drafts`.

## How to Query Each System

### CRM (Twenty) — GraphQL
- **Endpoint**: `https://crm.psquared.dev/graphql`
- **Auth**: `Authorization: Bearer $PSQUARED_CRM_TOKEN`
- **Key objects**: `companies`, `people`, `opportunities`, `campaigns`, `tasks`, `notes`

Example — list opportunities in a campaign:
```graphql
query {
  opportunities(filter: { campaignId: { eq: "CAMPAIGN_ID" } }) {
    edges { node { id name stage demoStatus demoUrl } }
  }
}
```

### Supabase (AgentHub DB)
- **Project**: `fevtfywriufbqnvbgyrm`
- **Tool**: `mcp__plugin_supabase_supabase__execute_sql`
- **Key tables**: `demo_pages`, `agents`, `knowledge`, `knowledge_bucket_items`, `knowledge_bucket_chunks`, `chats`, `messages`, `accounts`

Example — find chats on demo agents:
```sql
SELECT dp.company_name, c.id as chat_id, c.created_at,
  (SELECT count(*) FROM messages m WHERE m.chat_id = c.id) as msg_count
FROM demo_pages dp
JOIN chats c ON c.agent_id = dp.agent_id
ORDER BY c.created_at DESC
```

### Ackee Analytics — GraphQL
- **Endpoint**: `https://ackee.psquared.dev/api`
- **Auth**: `Authorization: Bearer $ACKEE_TOKEN`
- **Demo domain ID**: `4bdddc8c-11d9-4d7e-ab94-aeb7866f0bb2`
- **CTA event ID**: `0f037f1c-c2c0-4205-b90d-3cb9bf66f9c2`

Example — get demo page views:
```graphql
query {
  domain(id: "4bdddc8c-11d9-4d7e-ab94-aeb7866f0bb2") {
    statistics { views(interval: MONTHLY, type: UNIQUE) { count } }
    facts { viewsMonth viewsToday activeVisitors }
  }
}
```

### Notification Service — REST
- **Base URL**: `https://notifications.psquared.dev`
- **Auth (admin)**: `Authorization: Bearer $BEARER_TOKEN`
- **Auth (drafts only)**: `Authorization: Bearer $EMAIL_DRAFT_ONLY_BEARER`

Key endpoints:
- `GET /drafts?status=SENT&pageSize=50` — list sent emails
- `GET /drafts/:id` — read full email (html_body, variables, subject)
- `POST /drafts/create` — create draft from template
- `POST /drafts/send` — send drafts `{ draftIds: [...] }`
- `GET /stats/funnel` — full conversion funnel data
- `GET /drafts/campaigns` — list CRM campaigns with draft counts

### InboxMate MCP — JSON-RPC
- **Endpoint**: `https://app.psquared.dev/api/mcp`
- **Auth**: `Authorization: Bearer $NUXT_MCP_DEMO_TOKEN`
- **Protocol**: JSON-RPC 2.0

Key tools:
- `clear_bucket` — remove all items from a knowledge bucket
- `scrape_and_build_knowledge` — scrape URLs via Tavily, create knowledge items with real sourceUrls
- `create_agent`, `update_prompt`, `update_widget_style`, `publish_agent`
- `create_knowledge_bucket`, `add_to_bucket`, `set_knowledge`
- `create_demo_page`, `update_demo_page`, `list_demos`, `get_demo`
- `list_bucket_items`, `list_knowledge`, `get_knowledge`

## Key Metrics

| Metric | Source | How to check |
|---|---|---|
| Demo page views | Ackee | Query demo domain statistics |
| CTA clicks | Ackee | Query CTA event |
| Emails sent | Notification service | `GET /drafts?status=SENT` |
| Chat interactions | Supabase | `chats` JOIN `demo_pages` on `agent_id` |
| Pipeline funnel | Notification service | `GET /stats/funnel` |
| Hot leads | CRM | Opportunities with stage > SCREENING |
| Campaign status | CRM + Notification service | Campaigns + draft counts per campaign |

## Environment Variables

All in `/Users/martinpammesberger/Documents/psquared/claude-overlord-folder/.env`:

| Variable | Service |
|---|---|
| `PSQUARED_CRM_TOKEN` | Twenty CRM GraphQL |
| `NUXT_MCP_DEMO_TOKEN` | InboxMate MCP endpoint |
| `NUXT_TAVILY_SEARCH_API_KEY` | Tavily web scraping |
| `EMAIL_DRAFT_ONLY_BEARER` | Notification service (draft creation) |
| `NOTIFICATIONS_SERVICE_BEARER_TOKEN` | Notification service (admin) |
| `ACKEE_TOKEN` | Ackee analytics |

## Pricing Tiers

**Note:** If prices change, this table must be updated. The `/price-change` skill handles pricing updates across all touchpoints — make sure this file is included in the update list.

| Tier | Monthly | Yearly | Demo Discount (yearly) |
|---|---|---|---|
| Starter | €59 | €49/mo | — |
| Pro | €129 | €107/mo | -33% → €86/mo |
| Business | €399 | €331/mo | -50% → €199/mo |

All plans include 14-day free trial, no credit card required.

## Knowledge System

Agents use RAG (vector search) over knowledge buckets:
- Each bucket contains knowledge items (text entries with `sourceUrl`)
- Items are chunked and embedded for vector similarity search
- When the agent's `searchKnowledge` tool is called, it returns matching chunks WITH their `sourceUrl`
- The widget UI shows sources as clickable links in citations

To upgrade knowledge quality: `clear_bucket` → `scrape_and_build_knowledge` with real page URLs → `publish_agent`

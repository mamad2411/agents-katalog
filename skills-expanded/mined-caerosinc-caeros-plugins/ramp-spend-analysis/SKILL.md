---
name: ramp-spend-analysis
description: Read-only reporting and analysis patterns over Ramp spend data, transactions, categories, receipts and memo hygiene, and the MCP load-and-query workflow. Use when analyzing corporate spend rather than integrating systems.
---

# Ramp Spend Analysis (Read-Only)

Everything here is reporting: read scopes only (`transactions:read`,
`reimbursements:read`, `business:read`, `users:read`). Analysis never
initiates payments, transfers, or card changes; findings go to humans who
act inside Ramp.

## Two ways to get the data

1. **Developer API**: pull `GET /transactions` windows with
   `from_date`/`to_date` and aggregate yourself (see `ramp-api`).
2. **Official MCP server** (this plugin ships it, `https://mcp.ramp.com/mcp`,
   OAuth sign-in): built for exactly this. Its tools follow a
   load-then-query pattern: `load_spend_export`, `load_cards`,
   `load_limits`, `load_users`, `load_departments`, `load_vendors`,
   `load_memos`, `load_entities`, `load_locations`,
   `load_purchase_orders` pull data into an ephemeral in-memory SQL
   database, then `execute_query` runs SQL over it. `get_ramp_categories`
   gives the category taxonomy; `get_current_user` shows whose access you
   inherit. Access mirrors the signed-in user's Ramp role, and company-wide
   data generally needs admin access; actions are recorded in Ramp's audit
   log.

MCP workflow: load only the tables and date range needed, query with SQL,
clear tables between unrelated questions to stay under context limits.

## Analyses that pay off

- **Spend by merchant / category / department**: group transaction amounts
  by `merchant_name`, Ramp category (via `get_ramp_categories` mapping),
  and department; compare month over month to catch drift.
- **Top-vendor concentration**: rank vendors by trailing-quarter spend;
  flag vendors that crossed a threshold for contract review.
- **Duplicate and anomaly screens**: same merchant + amount + date across
  cardholders; amounts just under approval thresholds; sudden first-time
  merchants with large charges. Report candidates, never auto-act.
- **Subscription creep**: recurring same-merchant monthly charges across
  many cards; consolidate under one owner.
- **Policy hygiene**: transactions missing receipts or memos
  (`load_memos` joins help here); stale limits vs actual usage
  (`load_limits`); reimbursements pending too long.
- **Budget burn**: department spend vs limit/spend-program allocations,
  projected to period end.

## Reporting discipline

- State the window and data cut time on every report; Ramp data changes as
  transactions settle and get coded.
- Reconcile totals against a second pull before publishing numbers; partial
  pagination is the classic silent error (walk `page.next` to the end).
- Amount fields are usually integer cents; divide once, at the display
  layer, and confirm units against the OpenAPI spec.
- Respect data minimization: aggregate where possible, avoid exporting
  cardholder-level detail unless the question requires it, and never pull
  card numbers (`cards:read_vault` stays off for analysis).
- Large datasets: keep result sets aggregated in SQL (GROUP BY in
  `execute_query`) instead of streaming raw rows into the conversation.

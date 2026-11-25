---
name: homepage-takeover
description: "Use when the user asks for a homepage takeover, roadblock, or 100% SOV sponsorship on the homepage — an ad ops fixed-flight campaign template deployed via OrbiAds (MCP or CLI). Example queries: 'book a homepage takeover for Renault next week', 'roadblock the homepage May 4-10'."
version: 1.0.0
author: Example Agency
license: MIT
metadata:
  group: examples
  tags: [orbiads, gam, adops, sponsorship, example]
  related_skills: [orbiads]
---

# Homepage Takeover — Custom Agency Skill (Worked Example)

This skill encodes our agency's house template for deploying a **homepage takeover** (HPTO): a fixed-flight sponsorship campaign that targets all homepage ad units, achieves 100% share of voice, and pairs every line item with companion roadblock creatives. It is a worked example for [`docs/custom-skills/README.md`](../../README.md) demonstrating how to write a custom skill on top of OrbiAds.

---

## House Conventions

| Parameter | Value |
|---|---|
| Line item type | `SPONSORSHIP` |
| Priority | `4` (GAM sponsorship priority) |
| Delivery goal type | `PERCENTAGE` |
| Goal percentage | `100` (100% SOV) |
| Creative strategy | Roadblock: all sizes served together, same flight |
| Naming pattern | `{Brand} — HPTO — {StartDate}` (e.g. `Renault — HPTO — 20260615`) |
| Flight | Fixed start + end date, no auto-extension |
| Targeting | Ad unit: homepage root + all children; device: ALL |

---

## Procedure

Follow these phases in order. Each maps to a step in [`workflow.yaml`](workflow.yaml).

### Phase 1 — Auth & Context Intake

Derive tenant and network from auth tools — never hardcode them.

| Step | MCP | CLI |
|---|---|---|
| Confirm connected user | `check_credentials` (standalone auth tool) | `orbiads auth status` |
| Get tenant ID | `get_my_tenant_id` (standalone auth tool) | `orbiads auth status` |

**Gate:** refuse to proceed if credentials are missing or GAM connection is not active.

---

### Phase 2 — Inventory Discovery

List homepage ad units and confirm sizes before building any payload.

| Step | MCP | CLI |
|---|---|---|
| List homepage ad units | `targeting(action="list_ad_units")` | `orbiads inventory ad-units` |
| List sizes on those units | `inventory(action="list_ad_unit_sizes")` | `orbiads inventory sizes` |
| List existing placements | `placements(action="list_placements")` | `orbiads inventory placements` |

Collect all `adUnitId` values whose path contains `homepage` (or whatever the tenant's root slug is). Confirm sizes — you will need them to match creative dimensions exactly.

---

### Phase 3 — Availability Forecast

Run a prospective forecast before creating anything. This is a validation gate.

| Step | MCP | CLI |
|---|---|---|
| Prospective forecast | `reporting(action="get_prospective_delivery_forecast")` | `orbiads reporting forecast prospective` |
| Standalone forecast (optional, per size) | `reporting(action="get_standalone_forecast")` | `orbiads reporting forecast standalone` |

**Gate:** present forecast results to the user. If available impressions < 95% of goal, stop and advise flight date adjustment. Do not proceed to writes until the user confirms the forecast is acceptable.

---

### Phase 4 — Advertiser & Order

Find or create the advertiser, then create the order.

| Step | MCP | CLI |
|---|---|---|
| Find/create advertiser | `find_or_create_advertiser` (PARITY: FULL) | `orbiads advertisers find-or-create` |
| Create order (dry_run first) | `orders(action="create", dry_run=true)` then with token | `orbiads orders create` |

Name the order: `{Brand} — HPTO — {StartDate}` per house convention above.

**Preview gate:** show the `ExecutionPlan` (mutations, estimatedCost, currentBalance) and require explicit user confirmation before executing.

---

### Phase 5 — Line Items

Create one sponsorship line item per ad unit group (or one per size if the network requires it).

| Step | MCP | CLI |
|---|---|---|
| Create line item batch (dry_run first) | `campaign(action="create_line_items_batch", dry_run=true)` then with token | MCP-only (no CLI equivalent for `campaign.create_line_items_batch`) |
| Or create individually | `line_items(action="create", dry_run=true)` then with token | `orbiads campaigns add-line-items` |
| Verify targeting setup | `line_items(action="verify")` | `orbiads line-items verify` |

Key payload fields:
```json
{
  "lineItemType": "SPONSORSHIP",
  "priority": 4,
  "deliveryRateType": "AS_FAST_AS_POSSIBLE",
  "goal": { "goalType": "PERCENTAGE", "percentage": 100 },
  "startDateTime": "...",
  "endDateTime": "..."
}
```

**Preview gate:** confirm every line item write individually (each token is scoped to a single payload; do not re-use across line items).

---

### Phase 6 — Creative Upload & Association

Upload roadblock creatives and associate them with the line items.

| Step | MCP | CLI |
|---|---|---|
| Upload image creative (per size) | `creative_assets(action="create_image")` | `orbiads creatives upload-images` |
| Associate creative to line item | `creatives(action="associate_creative")` | `orbiads campaigns attach-creatives` |
| Scan compliance | `creative_qa(action="scan_creative_compliance")` | `orbiads creative-qa scan-compliance` |
| Validate SSL | `creative_qa(action="validate_creative_ssl")` | `orbiads creative-qa validate-ssl` |

For HTML5 creatives use `creative_assets(action="create_html5")` / `orbiads creatives upload-html5`.

**QA gate:** `scan_creative_compliance` and `validate_creative_ssl` must both pass (no blockers) before the deploy step. Do not proceed to deploy if either returns errors.

---

### Phase 7 — Deploy

Execute the campaign pipeline.

| Step | MCP | CLI |
|---|---|---|
| Plan deployment | `campaign(action="plan_deployment")` | `orbiads campaigns plan-deployment` |
| Deploy (dry_run first, then with token) | `campaign(action="deploy", dry_run=true)` then with token | `orbiads campaigns deploy` |

**Preview gate:** show the full `ExecutionPlan` from `plan_deployment` (all mutations, credit cost). Get explicit user confirmation before calling `deploy` with the `confirmation_token`.

---

### Phase 8 — Post-Deploy Delivery Check

Confirm GAM has accepted the line items and delivery is starting.

| Step | MCP | CLI |
|---|---|---|
| Check delivery status | `reporting(action="check_delivery_status")` | `orbiads reporting delivery-status` |
| Delivery forecast per line item | `reporting(action="get_delivery_forecast_by_line_item")` | `orbiads reporting forecast-line-item` |
| Check underdelivery alerts | `reporting(action="check_underdelivery_alerts")` | `orbiads reporting alerts-underdelivery` |

---

## Gotchas

1. **Creative sizes must match the line item's creative placeholders exactly.** List sizes with `inventory(action="list_ad_unit_sizes")` first. Size mismatch is the #1 API error: the line item stays stuck in `NEEDS_CREATIVES` and never delivers.

2. **SPONSORSHIP requires `goal.goalType=PERCENTAGE` and `goal.percentage` must be set.** Omitting the `percentage` field or sending `goalType=IMPRESSIONS` for a SPONSORSHIP line item returns a GAM validation error. This type only accepts percentage delivery goals.

3. **Run the forecast before creating anything.** Forecasts are free reads; priority-4 sponsorships compete for the same guaranteed homepage inventory, so creating line items without forecasting can book over an already-sold flight and create delivery conflicts you only discover after the writes are paid.

4. **`confirmation_token` expires in 5 minutes.** If the user takes more than 5 minutes to confirm a preview, the token is stale. Re-run the dry_run to get a fresh token. Any payload change between dry_run and execute returns `IDEMPOTENCY_KEY_MISMATCH` — the server validates a SHA-256 of the full payload.

5. **REST delivery reports do not work on GAM test networks.** The REST Interactive Reports API returns SERVER_ERROR on test networks, so the Phase 8 delivery checks need a production network. Forecasts (Phase 3) are unaffected. This is a GAM API limitation, not an OrbiAds bug.

---

## Safety Contract

- **Derive tenant and network from auth tools.** Call the standalone `check_credentials` or `get_my_tenant_id` auth tools before any action. Never hardcode a `tenantId` or `networkCode`.
- **Reads are free.** Call `list_ad_units`, `list_ad_unit_sizes`, `list_placements`, `get_prospective_delivery_forecast`, and `scan_creative_compliance` liberally — they cost 0 credits.
- **Every write requires preview → confirmation_token → execute.** Call with `dry_run=true` first, show the `ExecutionPlan`, get explicit user confirmation, then re-call with the same payload + `confirmation_token`. Token TTL is 5 minutes.
- **Never bypass `billing_guard`.** The server enforces this; client-side bypasses are not possible. Quote the credit cost before every write: "This will consume N credits. You have M remaining. Proceed?"
- **Max 2 write retries.** GAM SOAP is not idempotent. If a write fails twice, surface the error code (`CONFIRMATION_REQUIRED`, `IDEMPOTENCY_KEY_MISMATCH`, etc.) and stop. Do not loop.
- **Same rules apply on CLI.** The CLI routes through the same backend `billing_guard` and confirmation token pipeline. `--dry-run` on CLI commands triggers the same preview flow.

---

Fixed orchestration: see [`workflow.yaml`](workflow.yaml).

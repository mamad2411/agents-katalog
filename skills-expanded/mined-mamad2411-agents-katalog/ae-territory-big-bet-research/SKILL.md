---
name: ae-territory-big-bet-research
description: Run a full AE territory overview and big bet research workflow. Collects consumption, pipeline, WAU, contracts, ASQ, PS, Genie/Lakebase, and activity depth signals from Logfood and Salesforce to identify 3–5 high-growth "big bet" accounts, model the quarterly target gap, and produce a Google Doc briefing with executive summary + Slack delivery. Use when asked to run a territory overview, identify big bet accounts, prepare AE research, analyse an AE's territory, or prepare for a QBR or territory planning session.
---

# AE Territory Overview and Big Bet Research

**Execution order:** Phase 1 → Phase 2 → Phase 3 → **[Phase 4 ‖ Phase 5 in parallel]** → Phase 6.

---

## ⚠️ Pre-execution: AE identification

If no AE was specified, **stop and ask:** *"Which Account Executive should I run this for? Provide full name and/or Databricks email."* Set `[AE Name]` and `[AE Email]` as variables substituted into every prompt, query, and heading.

**Account scope gate (end of Phase 1, Step 1):** Count total accounts. If **≥ 20**, restrict all subsequent phases to consuming accounts only (`total_consumption_dollars > 0` in either of the last two quarters). Zero-consumption accounts get a single footnote in Phase 6 ("X accounts with zero consumption excluded — separate greenfield review recommended"). Under 20 → include all.

---

## Scope and data sources

> **Strategy:** Load `fe-internal-tools:genie-rooms` first — primary interface for all exploratory and aggregation queries. Fall back to direct SQL (`--profile=logfood`) only when Genie lacks field-level precision (blocker fields, days-in-stage math, burst-date calculations, exact UCO stage filtering).

**Skills to load:** `fe-internal-tools:genie-rooms` (first), `logfood-querier`, `salesforce-actions`, `databricks-org`, `uco-consumption-analysis`. Always apply region filter (e.g. `FEPhysicalRegion__c = 'EMEA'`) to avoid cross-regional leakage.

**Auth:** Load `databricks-authentication` and `salesforce-authentication` before any queries.

### Territory scoping
- **Genie (primary):** Call Global Genie with `--profile=logfood`. Ask: *"Show all accounts where [AE name / email] is the Account Executive."* Use the result as the **active (consuming) account subset** (Genie is usage-scoped, ~29-day window). Validate count; use for exploratory ranking and quick territory check. *Experiment: Genie returns usage-based list; sufficient for many Phase 1 steps.*
- **SQL fallback (full territory):** When the **full SFDC territory list** is required (e.g. scope gate count ≥20, or UCO/contract coverage across all assigned accounts), use `main.sfdc_bronze.accountteammember` (latest `processDate`), `UserId = <AE SFDC Id>`, `TeamMemberRole = 'Account Executive'`; also `Account.OwnerId = <AE Id>`. Resolve AE's SFDC ID via `main.sfdc_bronze.user` filtered by email. Persist full account ID + name list.

### Consumption data
- **Genie:** *"Rank [AE name]'s accounts by total consumption $ in [quarter] and QoQ vs prior quarter"* / *"Show monthly consumption by SKU for [Account] over 9 months"*
- **Direct SQL:** `main.gtm_gold.account_consumption_quarterly` (QoQ), `account_consumption_monthly` (MoM / partial-quarter pro-rating), `main.fin_live_gold.paid_usage_metering` (SKU granularity — group by `sfdc_account_id`, `sku`/`product_type`, month).

### Use case pipeline (UCO)
- **Genie:** *"Show active use cases for [AE name]'s accounts grouped by stage (U1–U6) with monthly DBU targets"*
- **Direct SQL (primary for U2–U5 detail):** Query `UseCase__c` via Salesforce CLI (`sf data query`) or `main.sfdc_bronze.usecase__c` (latest `processDate`). Filter: `Stages__c IN ('U1','U2','U3','U4','U5','U6')` — the `Active__c` boolean is unreliable in Logfood (often false even for active UCOs); use stage filter instead.

  **Required fields** — confirmed actual Salesforce field names (verified via `sf sobject describe UseCase__c`):

  | Field | Purpose |
  |---|---|
  | `Name`, `Account__c`, `Account__r.Name` | Identity |
  | `Stages__c` | Stage (U1–U6) |
  | `TotalDBUs__c` | Monthly Total DBUs |
  | `MonthlyTotalDollarDBUs__c` | Monthly Total $DBUs — **use this for pipeline ranking** |
  | `Implementation_Status__c` | Manual health flag (Green/Yellow/Red) — treat as **secondary signal only** |
  | `Implementation_Notes__c` | Onboarding Plan — primary real-progress signal |
  | `NextSteps__c` | Next Steps text — primary real-progress signal |
  | `Demand_Plan_Next_Steps__c` | Demand Plan next steps — supplement |
  | `LastNextStepsModifiedDate__c` | Staleness of next steps — critical freshness indicator |
  | `Last_Stage_Modified_Date__c` | When stage last changed |
  | `CurrentStageDaysCount__c` | Days in stage (pre-calculated) |
  | `LastModifiedDate` | Fallback for days-in-stage |
  | `Blockers__c` | Blocker picklist |
  | `Blocker_Comments__c` | Blocker detail text |
  | `Implementation_Start_Date__c` | Target onboarding start |
  | `Full_Production_Date__c` | Target go-live / production date |
  | `UseCaseInPlan__c` | In demand plan? |
  | `Description__c` | Business problem description |
  | `Lifecycle_Stage__c` | Lifecycle status |

- **Days-in-stage:** use `CurrentStageDaysCount__c` (pre-calculated); fallback: `DATEDIFF(CURRENT_DATE(), COALESCE(Last_Stage_Modified_Date__c, LastModifiedDate))`. Labels: **Green** (<90d), **Yellow** (90–180d), **Red** (>180d).

- **⚠️ UCO momentum read — go beyond the health flag.** `Implementation_Status__c` (Green/Yellow/Red) is self-reported and frequently stale or over-optimistic. **For every U2–U5 UCO, synthesize a true momentum assessment from three signals combined:**
  1. **`NextSteps__c` text** — are next steps concrete and specific ("deploy to prod by March 5", "schedule kickoff") or vague/absent ("TBD", null)? Flag language indicating risk: *"waiting for", "blocked by", "on hold", "no response", "pending approval", "paused"*. Flag language indicating momentum: *"completed", "deploying", "in progress", "next meeting scheduled", "testing"*.
  2. **`Implementation_Notes__c` (Onboarding Plan)** — does the plan describe active delivery milestones, or is it a stale copy-paste from U2 with no updates? A U4/U5 UCO that still has only an initial scoping statement in the onboarding plan is de facto stalled.
  3. **`LastNextStepsModifiedDate__c`** — if >60 days since last update, flag as **stale** regardless of the health flag. A "Green" UCO with next steps last updated 90+ days ago is not Green.
  - **Synthesize into one label per UCO:** `ACTIVE` (concrete next steps, fresh, momentum language), `DRIFTING` (vague or partially stale), `STALLED` (no concrete next steps, or >60d stale, or blocker language — regardless of health flag), or `AT-RISK` (explicit blocker or risk language found).
  - **This label overrides the health flag in all analysis.** A "Green" health flag with a STALLED momentum read = treated as stalled.

- **Adoption maturity tiers:** Tier 1 = JOBS/DLT only; Tier 2 = SQL Warehouse + BI UCOs; Tier 3 = ALL_PURPOSE + MODEL_SERVING + FMA + ML/GenAI UCOs; Tier 4 = multi-SKU breadth + Unity Catalog / data products.

### Commit contracts and burst dates
- **Primary:** `main.fin_live_gold.consolidated_active_contracts` (validated SOT). **Critical:** filter by `sfdc_account_id` (NOT `account_id` — that column does not exist in this table). The commitment amount is in `workload_commitment` (double) — there is no `contract_type` column. Key columns: `sfdc_account_id`, `sfdc_account_name`, `workload_commitment`, `complimentary_usage`, `paid_usage`, `platform`, `order_start_date`, `order_end_date`.
```sql
SELECT sfdc_account_id, sfdc_account_name, workload_commitment,
       paid_usage, platform, order_start_date, order_end_date
FROM main.fin_live_gold.consolidated_active_contracts
WHERE sfdc_account_id IN (<territory_account_ids>)
ORDER BY workload_commitment DESC
```
- **Fallback:** `main.sfdc_bronze.opportunity` (`StageName = 'Closed Won'`) or `main.sfdc_bronze.contract` — use `sf sobject describe Contract` to validate field names first.
- **ACV** = `workload_commitment / contract_years` (contract_years = DATEDIFF(order_end_date, order_start_date) / 365.0).
- **Burst date = order_start_date + (workload_commitment / annualized_run_rate) years** (annualized_run_rate = current quarter consumption × 4; pro-rate partials). Run rate > ACV → burst before contract end (upsell opportunity); run rate << ACV → adoption risk (under-commit). No contract row → flag PAYG.

### ASQ / Specialist requests
> **Primary source is Logfood** (`main.sfdc_bronze.approvalrequest__c` — confirmed present). Fall back to Salesforce API only after 2–3 failed Logfood attempts. The Salesforce object is `ApprovalRequest__c` (NOT `ASQ__c` — that name will 404).

**Step 1 — Logfood (primary):**
```sql
SELECT
    Name,                  -- AR number, e.g. AR-000110329
    Request_Type__c,       -- "Specialist SA (SSA) Request" | "Shared Technical Services" | "Scaled SAs Support Request" | "PS Ops"
    Status__c,             -- New | In Progress | On Hold | Complete | Rejected
    Support_Type__c,       -- e.g. "Unblock New Workloads", "ML & GenAI", "Win an Evaluation"
    Urgency__c,            -- Low | Normal | High | Critical
    Start_Date__c,
    End_Date__c,
    Account_Name__c,       -- pre-joined account name (no lookup needed)
    CreatedDate,
    Account__c
FROM main.sfdc_bronze.approvalrequest__c
WHERE Account__c IN (<territory_account_ids>)
  AND processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.approvalrequest__c)
ORDER BY CreatedDate DESC
```
> **Note:** `Account_Owner__c` in this table is an HTML anchor (`<a href="/005...">Name</a>`), not a plain string. Do not filter by it — use `Account__c IN (...)` with the pre-resolved territory account IDs instead.

**Step 2 — Salesforce API fallback** (use only if Logfood query fails or returns 0 rows after retrying):
```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')
sf data query --target-org "$SF_TARGET_ORG" -q "
  SELECT Id, Name, RecordType.Name, Request_Type__c, Status__c, Support_Type__c,
         Urgency__c, Start_Date__c, End_Date__c, Account__r.Name, CreatedDate
  FROM ApprovalRequest__c
  WHERE Account__c IN ('<id1>','<id2>',...)
  ORDER BY CreatedDate DESC
  LIMIT 50"
```
> Key `RecordType.Name` values: `Account Resource Request` (SSA requests), `Shared Technical Services` (STS), `Scaled SAs Support`, `PS Ops / Partner Ops`.

**Step 3 — Genie (last resort):** *"Show specialist / SSA engagement history for [Account Name]."*

- **CHECK:** Flag open ASQs (`Status__c IN ('New','In Progress','On Hold')`); flag zero-history accounts as under-invested in SA coverage; note `Support_Type__c` patterns (e.g. multiple "Unblock New Workloads" = repeated friction).

### Partner engagements and PS projects
> Partner data is most reliably found in UCO text fields; PS data is rarely in sfdc_bronze — default to API.
- **Partners:** Scan UCO `Description__c`, `Implementation_Notes__c`, `Next_Steps__c` for mentions. Also check `main.sfdc_bronze.opportunity` for `Partner__c` / `Partner_Account__c`. API fallback: `SELECT ... FROM PartnerEngagement__c WHERE Account__c IN (...)` if object exists.
- **PS:** API primary: `SELECT Id, Name, Account__r.Name, Status__c, Type__c, Start_Date__c, End_Date__c FROM PSEngagement__c WHERE Account__c IN (...)`. Validate: `sf sobject describe PSEngagement__c`. Fallback: UCO description text.
- **CHECK:** Flag big bet accounts with no partner as co-sell opportunities; flag where PS could accelerate a stalled UCO (U3→U5); note PS–consumption correlation where observable.

### Genie and Lakebase usage (FY27 priority)
- **Genie:** `product_type = 'GENIE'` or `sku LIKE '%GENIE%'` / `'%AI_BI%'` in `paid_usage_metering`. Fallback: `main.data_product_features.genie_usage` or UCO text.
- **Lakebase:** `product_type = 'LAKEBASE'` or `sku LIKE '%LAKEBASE%'` / `'%POSTGRES%'`. Fallback: UCO text or `databricks lakebase list --profile=logfood`.
- **FMA / Model Serving:** `product_type IN ('FOUNDATION_MODEL_API', 'MODEL_SERVING', 'AI_GATEWAY')` — AI maturity proxy.
- **Genie (aggregation):** *"Which of [AE name]'s accounts have Genie, Lakebase, AI, or Model Serving usage?"*
- **CHECK:** Per account: Genie (Y/N + $), Lakebase (Y/N + instances), FMA (Y/N). **Zero Genie + zero Lakebase = FY27 whitespace target.** Both active → elevates toward Tier 4.

### Active users / WAU and activity depth
- **Primary:** `main.gtm_gold.account_active_users_quarterly` — pull current + prior fiscal quarter per territory account. Derive `<current_q>` using `../../resources/fiscal_calendar.py` (`fiscal_year_quarter_str` field); the filter value format is `"FY'27 Q1"` (string with apostrophe).
```sql
SELECT account_id, wau_t7d, wau_t7d_prior_quarter, fiscal_year_quarter
FROM main.gtm_gold.account_active_users_quarterly
WHERE account_id IN (<territory_account_ids>)
  AND fiscal_year_quarter = '<current_fiscal_year_quarter_str>'  -- e.g. "FY'27 Q1"
ORDER BY wau_t7d DESC
```
  Compute: `wau_qoq_pct = (current_wau - prior_wau) / NULLIF(prior_wau, 0) * 100`. Labels: Rising (>+10%), Flat (±10%), Declining (<–10%).
- **Genie:** *"Show quarterly WAU for [AE name]'s accounts comparing current to prior quarter."*
- Rising WAU QoQ = expanding user base (leading indicator). Flat/declining on high-consumption account = adoption risk.
- **Activity depth (secondary):** `main.gtm_gold.account_activity_measures` — `DESCRIBE` first to discover columns; extract active days, session counts, feature engagement, distinct users. Use as an additional secondary metric of account activity in Phase 3 scoring.

### Industry outcome maps
Reference [Databricks Industry Outcome Maps (2025)](https://home.databricks.com/sales/industry-2025/) in Phases 4 and 6. If gated, search Glean for "industry outcome map [vertical]". Extract: recommended use cases, expected business outcomes, Databricks SKU mapping.

---

## Phase 1: Territory scoping and baseline data

1. **Resolve accounts** — **Genie first:** Ask Global Genie (*"Show all accounts where [AE name / email] is the Account Executive"*, `--profile=logfood`) and use the returned list as the active-territory set for downstream steps. When full territory count is needed for the **scope gate** (≥20 → restrict to consuming only), or when Phase 2/3/6 require every assigned account, **fallback:** lookup AE in `sfdc_bronze.user`; get full account list from `accountteammember`. Persist IDs. **Apply scope gate.**
2. **Top consuming accounts** — Genie: *"Top accounts for [AE Name] by $ this quarter and last."* Fallback: `account_consumption_quarterly`. Output: ranked top 10–15 with name, $, DBUs, region.
3. **Consumption trends by SKU** — Genie: *"QoQ SKU consumption trend for [AE Name]'s accounts over 3 quarters."* Fallback: `paid_usage_metering` grouped by account, SKU, month.
4. **UCO pipeline (full momentum read — text fields required)**
   - Query `UseCase__c` for all territory accounts using `Stages__c IN ('U1','U2','U3','U4','U5','U6')` (not `Active__c = true` — that filter is unreliable in Logfood). Pull all fields listed in the UCO scope section, **including `NextSteps__c`, `Implementation_Notes__c`, `LastNextStepsModifiedDate__c`**.
   - **Momentum read (mandatory):** For every U2–U5 UCO, read `NextSteps__c` + `Implementation_Notes__c` + `LastNextStepsModifiedDate__c` and assign a momentum label: `ACTIVE`, `DRIFTING`, `STALLED`, or `AT-RISK` per the UCO scope section rules. This label is the primary progress signal — it **overrides** `Implementation_Status__c` if they conflict.
   - **Blocker analysis:** flag `Blockers__c` populated or blocker language in `NextSteps__c` / `Blocker_Comments__c`. **Blocked U5 UCOs are a direct risk to the big bet thesis.**
   - **Days-in-stage flags:** Green (<90d), Yellow (90–180d), Red (>180d). Red on U2/U3/U4 = stalled; on U5 = go-live delay.
   - **Adoption maturity:** assign Tier 1–4 per account.
5. **ASQ / partner / PS** — Run queries per scope section. Note specialist history, partner linkage, PS–consumption correlation.
6. **Contracts and burst dates** — Query `consolidated_active_contracts`; compute burst date per account; flag burst-before-end (upsell) and under-commit (adoption risk).
7. **Genie + Lakebase heatmap** — Genie: *"Which accounts have Genie or Lakebase usage?"* Enrich with `paid_usage_metering`. Produce heatmap: green (both), yellow (one), red (neither = FY27 whitespace target).
8. **WAU + activity depth** — Query `account_active_users_quarterly` (current + prior quarter); compute QoQ %; flag rising/flat/declining. Also query `account_activity_measures` for engagement enrichment.

**Deliverable:** Territory overview — (1) top consuming accounts, (2) UCO pipeline with tier/blockers/days-in-stage, (3) SKU trends, (4) ASQ/PS/partner summary, (5) contract + burst analysis, (6) Genie/Lakebase heatmap, (7) WAU QoQ + activity depth.

---

## Phase 2: Internal risk and red flag assessment

> Run directly after Phase 1, before Phase 3. Risk data prevents anchoring the big bet shortlist on growth signals alone.

For every territory account, document:
- **Internal red flags:** open ASQ or escalation; active UCO blockers (especially U5 in Q1/Q2); stalled UCOs (U2/U3/U4 >180d Red, 90–180d Yellow; U5 >90d Yellow); declining QoQ consumption; under-commit; missing SA coverage; contract renewal <6 months with no expansion plan.
- **External red flags (5-min scan per account):** "[Company] layoffs / restructuring / Snowflake / Fabric."
- **Output:** Risk summary table — account name, red flag type + severity, stalled UCO count, open ASQ count, consumption trend, contract status. Feeds Phase 3 scoring.

---

## Phase 3: Identify big bet accounts

> Run after Phase 1 + Phase 2. Upside lens (Phase 1) + downside lens (Phase 2) = balanced shortlist.

**Scoring dimensions** — primary signals drive selection; secondary are tiebreakers; risk filter applied last:
- **(Primary) Consumption growth:** QoQ % from `account_consumption_quarterly` (target >50% QoQ or strong monthly ramp)
- **(Primary) Pipeline size + timing:** sum of `Monthly_DBUs__c` from U3/U4/U5; weight U5 go-lives in current quarter highest
- **(Primary) WAU growth:** QoQ WAU % from `account_active_users_quarterly`; rising = upweight even if current consumption is moderate
- **(Primary) Active commitment:** commit size, burst proximity, under-commit flag
- **(Secondary) Activity depth:** `account_activity_measures` metrics — active days, session depth, feature engagement; use as tiebreaker
- **(Secondary) Adoption maturity gap:** Tier 1–2 with high consumption has more expansion headroom
- **(Secondary) Genie + Lakebase whitespace:** neither active = higher FY27 priority
- **(Risk filter) Phase 2 register:** downweight/exclude multiple Red-flag stalled UCOs, active U5 blockers, declining QoQ, near-term renewal with no expansion plan. Flag "conditional bets" (e.g. "big bet if blocker resolved by [date]").

**Steps:**
1. Genie: *"Show QoQ growth, pipeline size, and WAU trend for all [AE Name]'s accounts — which have the strongest growth momentum?"* Supplement with direct SQL for burst-date and maturity tier scoring.
2. Compute per account: current + prior quarter consumption, QoQ %; UCOs in U3/U4/U5 with `Monthly_DBUs__c`.
3. Score and rank using dimensions above. Shortlist **3–5 accounts**.
4. **Document explicit selection rationale per account (3–5 sentences):** why selected (specific data points), key risk acknowledged (Phase 2 ref), FY27 angle (Genie/Lakebase), why not excluded despite flags, and why other high-scorers were excluded.

**Deliverable:** Shortlist — account name, consumption, pipeline, maturity tier, ASQ/PS/partner, contract/burst, WAU QoQ %, activity depth signals, explicit rationale, risk register filtered to shortlisted accounts.

---

## Phase 4: External research per big bet account

> **Parallelise:** Launch Phase 4 and Phase 5 concurrently (separate agents) immediately after Phase 3 using `dispatching-parallel-agents`. Both must complete before Phase 6 begins.

For each shortlisted account (3–5):
1. **Corporate website** — homepage + about/data/technology/careers pages. Extract: industry, size, strategic priorities, data-driven initiatives.
2. **Hiring signals** — "[Company] data engineer / analytics / ML jobs." Note volume and role types as a data capability investment signal.
3. **Competitor + platform usage** — "[Company] Snowflake / Fabric / data warehouse / Databricks." Use job postings, press, case studies to infer platform coexistence or displacement risk.
4. **Data strategy synthesis** — centralised vs federated, cloud maturity, CDO/analytics leadership mentions.
5. **Outcome map use case ideation** — fetch [industry outcome map](https://home.databricks.com/sales/industry-2025/) for the account's vertical. Using the account's data strategy, strategic priorities, and hiring signals gathered in steps 1–4 as a lens, identify **3–5 use cases the account is NOT currently pursuing** that they would likely find compelling based on what you now know about their business direction. Do NOT limit suggestions to gaps in the existing UCO portfolio — treat the current UCOs as background context only. For each suggested use case: use case name (from outcome map), why this specific company would care about it (grounded in their stated priorities, industry position, or hiring signals), expected business outcome, Databricks SKU fit, and adoption maturity pre-requisite. **CHECK:** match use case complexity to the account's maturity tier — don't suggest Tier 4 use cases for Tier 1 accounts; suggest the next logical capability step.

**Deliverable:** Per-account brief (1–2 pages) — corp overview, hiring signals, competitor/platform signals, data strategy, outcome map use cases, risk factors, why 30% QoQ is plausible.

---

## Phase 5: Quarterly target gap analysis

> **Parallelise** with Phase 4. Needs only Phase 1 data + Phase 3 shortlist.

**Fiscal context:** Derive `<current_fiscal_quarter>` and `<current_fiscal_year>` from today's date using the shared utility at `../../resources/fiscal_calendar.py`. Run `python3 ../../resources/fiscal_calendar.py` to get a JSON object with `fiscal_year` (int), `fiscal_quarter` (int), and `fiscal_year_quarter_str` (e.g. `"FY'27 Q1"`). Use integer values for `rpt_individual_obt_gtm` and the string value for `account_active_users_quarterly`. Databricks fiscal year starts Feb 1 — FY27 = Feb 2026–Jan 2027.

**Step 1 — Establish target and forecasts.** Query `main.gtm_gold.rpt_individual_obt_gtm`:
```sql
SELECT user_email, fiscal_quarter, fiscal_year, 
    target_dbu_dollars,                      -- the AE's quarterly target (SOT) — what they are measured against
    submitted_my_call,                       -- the AE's own forecast for the current quarter — what they think they will land
    forecast_straight_line_t28d_quarterly    -- DS data-science linear prediction (trailing 28d consumption trend)
FROM main.gtm_gold.rpt_individual_obt_gtm
WHERE user_email = '[AE Email]'
  AND fiscal_quarter = <current_fiscal_quarter>   -- integer from databricks_fiscal_context()
  AND fiscal_year = <current_fiscal_year>         -- integer from databricks_fiscal_context()
LIMIT 1
```
**Column meanings:**
- `target_dbu_dollars` — the official quarterly **target** the AE is measured against. This is the SOT number for gap labelling.
- `submitted_my_call` — the AE's own **forecast** of where they expect to land this quarter. Compare against both `target_dbu_dollars` (are they calling above/below target?) and `forecast_straight_line_t28d_quarterly` (does their call agree with the DS trend?).
- `forecast_straight_line_t28d_quarterly` — the **data science forecast** extrapolated from the trailing 28-day consumption trend. The most objective momentum signal.

**Target fallback:** If `target_dbu_dollars` is NULL (known Logfood gap for some EMEA AEs): run-rate fallback = current partial quarter consumption × (90 / days elapsed); ask AE for target directly; note fallback in Section 3.5.

**Step 2 — Weighted pipeline contribution.** U5 UCOs with go-live in current quarter: `Monthly_DBUs__c × (remaining weeks / 13)` × confidence (Green=80%, Yellow=40%, Red=10%). U4 UCOs with current-quarter onboarding target: same formula × 30%. Sum → weighted uplift. Add to DS forecast → **projected quarter-end**. Gap labels: **On track** (≥95% target), **At risk** (75–95%), **Material gap** (<75%).

**Step 3 — Three-way comparison.** Lay out all three numbers side by side and draw an explicit conclusion:

| Signal | Value | Meaning |
|--------|-------|---------|
| `target_dbu_dollars` | $X | Official quarterly target — the bar to hit |
| `submitted_my_call` | $Y | AE's own forecast — their confidence in closing the quarter |
| `forecast_straight_line_t28d_quarterly` | $Z | DS trend-based prediction — objective momentum signal |

- **AE vs Target:** Is `submitted_my_call` above or below `target_dbu_dollars`? If below, the AE themselves is not calling a beat — flag immediately.
- **AE vs DS:** If `submitted_my_call` and `forecast_straight_line_t28d_quarterly` diverge >10%, flag: AE is either overly optimistic (call > DS) or overly pessimistic (call < DS). Use the more conservative number for gap labelling.
- **DS vs Target:** Is the DS trend alone enough to hit target, or is pipeline uplift required?
- Supplement with MoM growth rate from `account_consumption_monthly` (last 3 months) and WAU trend from Phase 1. State whether organic momentum alone closes the gap.

**Step 4 — Acceleration ideation (if At risk or Material gap).** Options grounded in Phases 1–3 data only:
- UCO pull-forwards (U4/U5 with solvable blockers in <2 weeks)
- New SKU activations (single-SKU accounts where UCOs mention additional workloads)
- Commit/burst conversations (accounts approaching burst that could sign expansion this quarter)
- Genie/Lakebase fast activations (Tier 2+ SQL accounts, zero Genie/Lakebase)
- PS-accelerated go-lives (UCOs where PS compresses U3→U5 by 4–6 weeks)

Output per option: `| Option | Account | UCO / SKU | Est. uplift ($) | Effort | Owner | Confidence |`

> **CHECK:** No generic suggestions — every option grounded in data. If on track, state clearly; do not manufacture a gap.

**Deliverable:** Gap verdict (on track / at risk / material gap), projected vs target, momentum summary, acceleration table (if gap exists).

---

## Phase 6: Final deliverable

> Write as an **AE research assistant briefing** for [AE Name]. Tone: direct, opinionated, actionable — not a data dump. State conclusions backed by data. Avoid hedging.

**Format:** Single Google Doc via `google-docs` skill — H1 sections, H2 accounts, H3 sub-topics. Tables for Section 2 and Section 3. Use `internal-jargon` skill for Databricks terminology.

### Section 0: Executive Summary *(one-page scannable — no prose paragraphs)*
- **Opening line:** Territory headline (account count, total $ consumption, QoQ %, active UCO count).
- **Big bet table** (one row per account): Account | Potential Score (`Very High / High / Medium-High`) | Qualification summary | Top use cases driving the bet (2–3 use cases).
  - **Qualification summary** must be a 1–2 sentence narrative that explains *why* this account is a big bet in plain business language — not a raw data list. Embed the key metrics as evidence within the narrative. Example: *"Fastest-growing account in the territory (+72% QoQ) with two high-value AI use cases ramping to production in Q1, and a large SQL analytics user base that hasn't yet adopted Genie or Model Serving — strong platform expansion headroom."* Avoid formats like "+72% QoQ, 3 U5 UCOs, Tier 2→3 gap" as standalone bullet points.
- **Quarterly target status:** Bold verdict — *"ON TRACK"* or *"MATERIAL GAP — $Z shortfall."* Follow with a three-line breakdown: (1) Target: `target_dbu_dollars` = $X. (2) AE forecast (`submitted_my_call`) = $Y — above/below target by Z%. (3) DS forecast (`forecast_straight_line_t28d_quarterly`) = $W — above/below target by Z%. Note any divergence between AE and DS forecasts. Include key go-lives factored in and top 2 acceleration options (if gap).
- **Territory-wide callouts** (3–5 bullets): burst-risk accounts, Genie/Lakebase whitespace clusters, stalled UCOs needing immediate attention.
- **One action per big bet** (max one line each): highest-leverage action [AE Name] should take in the next 30 days.

### Section 1: Big Bet Account Briefs *(one subsection per account)*

Per account, include all of the following subsections in order:

1. **Why this is a big bet** — 2–3 sentences with specific data points (consumption $, WAU QoQ, contract ACV, top UCO stage).
2. **Consumption snapshot** — 3-month $+DBUs, SKUs ranked by spend, Genie/Lakebase status, WAU QoQ trend from `account_active_users_quarterly`. Present as a small table.
3. **Contract details** — ACV (= `workload_commitment / contract_years`), TCV (`workload_commitment`), platform, `order_start_date` / `order_end_date`, burst date, over/under-commit flag. PAYG if no contract row found.
4. **UCO progress** — Per UCO: stage, days-in-stage flag (Green/Yellow/Red), blocker (if any), verdict. Table format.
5. **PS / ASQ / specialist history** — Count and summarise all `approvalrequest__c` records: total ARs, open ARs (flag stale "In Progress"), most recent SSA/STS/Scaled SA types, pattern notes (e.g. repeated "Unblock New Workloads" = repeated friction). Flag accounts with zero ASQ history as under-invested.
6. **External company overview** *(from Phase 4 internet research — required, not optional)*:
   - **Company profile:** industry, headquarters, revenue/size, ownership (public/private/PE), recent M&A or restructuring.
   - **Strategic priorities:** key initiatives from annual report, press, or CEO statements — especially data, AI, digital transformation, or cloud mentions.
   - **Hiring signals:** data/ML/analytics/cloud open roles — volume and seniority as investment proxy.
   - **Competitive / platform signals:** evidence of Snowflake, Fabric, Redshift, or other platform usage from job postings, press, or case studies.
   - **Data strategy synthesis:** centralised vs federated, cloud maturity, CDO/CDAO/analytics leadership.
   - Keep this subsection to 5–8 bullet points — dense signal, not prose paragraphs.
7. **Risks** — bullet per risk with severity (High/Medium/Low) and one-line mitigation.
8. **3–5 outcome-map use case suggestions** — use cases the account is **NOT currently pursuing** but would likely find compelling based on their external data strategy and business direction (from Phase 4). Per suggestion: use case name (from outcome map), why *this specific company* would care (grounded in their stated priorities, industry position, or hiring signals), expected business outcome, Databricks SKU fit, adoption maturity pre-requisite. Match complexity to maturity tier.

### Section 1.5: Top U2–U5 Pipeline — Upside Potential & Risk Assessment *(mandatory default)*

> This section appears in **every** deliverable, not just when explicitly requested. It is the bridge between the Big Bet briefs (Section 1) and the territory overview (Section 2) — it makes the full active pipeline visible and gives the AE a ranked action list.

**Scope:** All active UCOs in stages U2–U5 across the entire territory, sorted by `MonthlyTotalDollarDBUs__c` descending. Include the top 10 (or all if fewer than 10 exist).

**Summary ranking table** (one row per UCO):

| Rank | Account | Use Case | Stage | Monthly $ | Days in Stage | Health Flag | **Momentum Read** | Upside | Risk |
|---|---|---|---|---|---|---|---|---|---|
| 1 | … | … | U2 | $X | 30d GREEN | Green | ACTIVE | Very High | Low |

- **Momentum Read** column: the synthesized label (`ACTIVE / DRIFTING / STALLED / AT-RISK`) derived from `NextSteps__c` + `Implementation_Notes__c` + `LastNextStepsModifiedDate__c` — not the raw health flag.
- **Upside** label: `Very High / High / Medium / Low` — reflects combined $ potential, stage proximity to go-live, and ACTIVE momentum.
- **Risk** label: `Low / Medium / High` — reflects STALLED/AT-RISK momentum, days-in-stage Red flag, blocker presence, or parallel resource contention.

**Per-UCO narrative** (3–5 bullets each — focus on the two or three highest-$ UCOs; compress lower-value ones):

For each UCO, address:
1. **Upside case** — why this UCO converts and what it means for the quarter ($ uplift, new SKU, platform expansion). Ground in actual consumption trend and account context.
2. **What the next steps / onboarding plan actually say** — quote or paraphrase key language from `NextSteps__c` and `Implementation_Notes__c`. If stale (>60d), say so explicitly. A UCO with no concrete next steps is not on track regardless of the Green flag.
3. **Specific risk** — what could prevent this UCO from going live this quarter: resource contention, technical complexity, procurement, stakeholder gap, or explicit blocker.
4. **Recommended action** — one concrete step the AE or SA should take in the next 2 weeks to preserve or accelerate the UCO.

> **CHECK:** Do not summarise by health flag alone. If `Implementation_Status__c = Green` but `NextSteps__c` is null or 90+ days stale, the momentum read must be `STALLED` and the narrative must reflect that. Honest assessment over optimistic label acceptance.

### Section 2: Territory Overview — Rest of Territory
All non-big-bet accounts sorted by tier potential (highest first). Per-account table: account name | tier potential label (`High / Medium / Watch / Stable`) | last-quarter $ | QoQ trend (↑/↔/↓) | maturity tier | active UCOs (count + top stage) | main risk flag | Genie (Y/N) | Lakebase (Y/N). Plus 2–3 trend highlights and a risk watch list.

### Section 3: Actionable Next Steps
Table per recommendation: **Account | Action | Owner (AE/SA/Specialist/Partner) | Timeline | Expected outcome.** Cover: UCO stage progression, blocker resolution, new use case initiation, PS/ASQ engagement, partner co-sell, contract/renewal actions. **Every zero-Genie / zero-Lakebase account must have a specific activation step.**

### Section 3.5: Quarterly Target Gap Analysis
- **Verdict:** bold one-liner (On track / At risk / Material gap) with shortfall amount if applicable.
- **Three-way breakdown table** (from Phase 5 Step 3):

| | Value | vs Target |
|-|-------|-----------|
| **Target** (`target_dbu_dollars`) | $X | — |
| **AE forecast** (`submitted_my_call`) | $Y | +/- Z% |
| **DS forecast** (`forecast_straight_line_t28d_quarterly`) | $W | +/- Z% |
| **Projected (DS + weighted pipeline)** | $V | +/- Z% |

- **Divergence flag:** If AE forecast and DS forecast differ >10%, call it out explicitly — note which is more conservative and why.
- **Momentum signal:** MoM growth rate (last 3 months) + WAU trend direction.
- **Acceleration options table** (only if gap): sorted by uplift descending — account, action, $ uplift, effort (Low/Med/High), owner.
- **If on track:** state clearly; do not manufacture urgency.
> **CHECK:** `target_dbu_dollars` = official target (SOT). `submitted_my_call` = AE's forecast — always compare against target AND DS forecast. If `target_dbu_dollars` is NULL, note fallback used. All three numbers must appear in the section.

### Section 4: Questions for [AE Name]
Sharp, account-specific questions (no generic ones) — each anchored to a named account and a concrete data signal. Themes: growth potential unlocking, use case acceleration, risk/retention signals, FY27 product conversations, partner/PS leverage, contract/commitment posture.

### Slack delivery
After Google Doc is created, send a Slack DM to the **vibe profile owner** (load `vibe-profile` skill; use `slack_handle` from `~/.vibe/profile`). Message: Section 0 content formatted for Slack + `Full research doc: <Google Doc URL>`. If handle unresolvable, print message text to console and note the gap.

---

## Checkpoint appendix

| Phase | Checkpoint | Verify |
| ----- | ---------- | ------ |
| 1.4 | UCO stage filter | `Stages__c IN ('U1','U2','U3','U4','U5','U6')` used — NOT `Active__c = true` (unreliable in Logfood) |
| 1.4 | UCO text fields retrieved | `NextSteps__c`, `Implementation_Notes__c`, `Demand_Plan_Next_Steps__c`, `LastNextStepsModifiedDate__c` pulled for every U2–U5 UCO |
| 1.4 | Momentum read completed | Every U2–U5 UCO assigned `ACTIVE / DRIFTING / STALLED / AT-RISK` label from text fields + staleness — NOT from health flag alone |
| 1.4 | Health flag conflicts flagged | Any UCO where momentum read contradicts `Implementation_Status__c` (e.g. Green + STALLED) explicitly called out |
| 1.4 | Next steps staleness checked | Any UCO with `LastNextStepsModifiedDate__c` > 60 days ago flagged as stale regardless of health flag |
| 1.4 | Blocker fields on every UCO | `Blockers__c` / `Blocker_Comments__c` inspected; blocker language in `NextSteps__c` also scanned; blocked UCOs flagged |
| 1.4 | Days-in-stage flags | `CurrentStageDaysCount__c` used (fallback: DATEDIFF); Green/Yellow/Red assigned; stalled UCOs listed |
| 1.4 | Adoption maturity tier per account | Tier 1–4 assigned from SKU + UCO mix |
| 1.5 | ASQ history | `main.sfdc_bronze.approvalrequest__c` queried with `processDate` filter (primary); if 0 rows → Salesforce API `ApprovalRequest__c` used as fallback (not `ASQ__c`); open ASQs flagged; zero-history accounts flagged |
| 1.5 | Partner engagements | Query ran; partner-linked accounts documented |
| 1.5 | PS projects | Query ran; PS–consumption correlation noted |
| 1.6 | Contracts + burst dates | `main.fin_live_gold.consolidated_active_contracts` queried using `sfdc_account_id IN (...)` (NOT `account_id`); `workload_commitment` used for ACV — no `contract_type` column exists; burst date computed; over/under-commit flagged; PAYG accounts noted |
| 1.7 | Genie usage per account | paid_usage_metering queried; Y/N + $ + trend per account |
| 1.7 | Lakebase usage per account | paid_usage_metering queried; Y/N + instances + trend per account |
| 1.7 | Genie + Lakebase heatmap | Green/Yellow/Red per account; FY27 whitespace targets identified |
| 1.8 | WAU QoQ per account | `account_active_users_quarterly` queried (current + prior); QoQ %; Rising/Flat/Declining; `account_activity_measures` enrichment extracted |
| 2 | Risk summary table | Internal red flags, stalled UCO count, ASQ count, consumption trend, contract status per account |
| 2 | Phase 2 before Phase 3 | Risk register complete and available as Phase 3 input |
| 3 | Scoring dimensions applied | Maturity tier, burst proximity, WAU QoQ, activity depth, Genie/Lakebase whitespace all factored in |
| 3 | Risk-adjusted scoring | Phase 2 register applied; Red-flag accounts downweighted/excluded; conditional bets flagged |
| 3 | Explicit selection rationale | Each shortlisted account has: growth driver, risk acknowledged, FY27 angle, why-not-excluded; excluded high-scorers briefly noted |
| 4 | Outcome map use cases | 3–5 use cases per big bet that the account is NOT currently pursuing; grounded in their data strategy + Phase 4 business insights; maturity-compatible |
| 5 | Phase 5 launched in parallel with Phase 4 | Separate agent started after Phase 3; Phase 1 + Phase 3 context passed |
| 5 | Target + forecasts retrieved | `target_dbu_dollars` (quarterly target, SOT), `submitted_my_call` (AE's forecast), `forecast_straight_line_t28d_quarterly` (DS forecast) all retrieved from `rpt_individual_obt_gtm`; three-way comparison completed; divergence flagged if AE vs DS >10%; fallback noted if target is NULL |
| 5 | Weighted pipeline modelled | U5 + U4 UCOs weighted; gap labelled On track / At risk / Material gap |
| 5 | Momentum check | DS vs AE forecast divergence flagged; MoM rate + WAU trend stated |
| 5 | Acceleration options | If gap: grounded options table; if on track: stated clearly |
| 6.0 | Executive summary | Territory headline; target verdict; big bet table; callouts; one action per bet |
| 6.1 | Big bet briefs | Each has all 8 subsections: rationale, consumption snapshot, contract (ACV + burst), UCO progress (with momentum read labels), PS/ASQ history, **external company overview from internet research**, risks, outcome-map use cases |
| 6.1.5 | Top U2–U5 pipeline section present | Section 1.5 included; top 10 UCOs ranked by `MonthlyTotalDollarDBUs__c`; momentum read labels shown; per-UCO narrative quotes/paraphrases `NextSteps__c` + `Implementation_Notes__c`; stale UCOs called out |
| 6.2 | Territory overview | All non-big-bet accounts ranked; per-account table; highlights + risk watch list |
| 6.3 | Next steps | Account + action + owner + timeline + outcome per row; Genie/Lakebase activation for every zero-usage account |
| 6.3.5 | Gap analysis section | Verdict + forecast + momentum; acceleration table if gap; numbers tie to Phase 5; quota source stated |
| 6.4 | AE questions | Account-specific and data-anchored; all 6 themes covered |
| 6.5 | Slack DM sent | Section 0 + Google Doc link delivered; confirmation or fallback text printed |

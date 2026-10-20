---
name: ae-biweekly-review
description: Prepare bi-weekly business review prep for Account Executives. Scans the current user's calendar for upcoming "2by2" or "b2b" meetings, runs use-case and consumption-focused research per AE (Genie, Logfood, Salesforce), produces a Google Doc per AE and sends a summary to the review owner on Slack. User-agnostic: works for any manager; uses vibe profile for identity and territory. Use when asked to prepare 2by2/b2b reviews, run bi-weekly AE reviews, or prep for business review meetings.
---

# Bi-weekly AE Business Review Skill

**Purpose:** Lightweight, recurring research for bi-weekly "2by2" / "b2b" business review meetings. Focus on use cases (sentiment, progress, onboarding hygiene), consumption trends (2-week delta, new SKUs), and adoption (WAU, new workspaces). Output: territory change summary, use case review with discussion questions, pipeline sufficiency, and Slack + Google Doc delivery.

**Execution order:** Phase 0 (user + calendar) -> Phase 1 (snapshot load) -> Phase 2 (data collection) -> Phase 3 (analysis) -> Phase 4 (output) -> Phase 5 (persist + deliver).

**Usage (any manager):**
- **With calendar:** Run on a Monday (or any day). The skill uses *your* vibe profile and *your* Google Calendar. It finds events containing "2by2" or "b2b" in the next 7 days, maps attendees to AEs from your profile's territory, and runs research for those AEs. Output is sent to *you* (Slack DM if configured, else printed).
- **Single AE (no calendar):** Say e.g. "Run bi-weekly review for Joscha Beutel" or "Prepare 2by2 prep for benjamin.zhou@databricks.com". The skill runs for that AE only and delivers to you.
- **First-time / no territory in profile:** If your vibe profile has no territory or account_executives, the skill will ask which AE(s) to run for. You can still use it for one or more AEs by name/email.

---

## User-agnostic setup: Review owner and paths

**Who is the "review owner"?** The person running this skill (the manager preparing the reviews). All deliverables are for them.

1. **Load vibe profile.** Read `~/.vibe/profile` (or use `vibe-profile` skill). From it set:
   - `[Review Owner Name]` = `user.name`
   - `[Review Owner Email]` = `user.email`
   - `[Review Owner Slack]` = `user.slack_handle` or Slack user ID for DM delivery (if present).

2. **If no vibe profile or missing user:** Ask the user to provide their name and email for "review owner", and where to send output (e.g. "I'll print the summary; for Slack delivery, add your Slack handle to vibe profile or specify it now").

3. **Snapshot base path (per-owner, so multiple managers don't overwrite):**
   - `[Snapshot Base]` = `~/.vibe/cache/ae-biweekly-reviews/{owner_safe}/`
   - `owner_safe` = `[Review Owner Email]` with `@` replaced by `_at_` (e.g. `k.halozhyn_at_databricks.com`).
   - Per-AE snapshot dir: `[Snapshot Base]{ae_email_safe}/` (same: email with `@` -> `_at_`).
   - Files: `snapshot_{YYYY-MM-DD}.json`, and symlink or copy `latest_snapshot.json`.
   - This location is consistent with the vibe-standard cache directory. Safe to delete at any time — next run treats a missing snapshot as a first run.

4. **Slack delivery:** Send DM to `[Review Owner Slack]`. If not set, output the message to the console and note: "Slack not in vibe profile; add slack_handle for DM delivery."

---

## Phase 0: Calendar scan and AE identification

**Goal:** Find which AEs have upcoming 2by2/b2b meetings this week so we only run research for them.

1. **Calendar search (current user's calendar).**
   - Use `google-calendar` skill. Get context first: `gcal_builder.py get-context`.
   - Search the **primary calendar** (the authenticated user = review owner) for events in the **next 7 days** where the event **summary** or **description** contains `2by2` OR `b2b` (case-insensitive).
   - Implementation: List events in next 7 days, filter client-side by summary/description containing "2by2" or "b2b", or use Calendar API `q=2by2` and `q=b2b` and merge results.

2. **Extract attendees.** For each matching event, collect attendee emails (and optionally the event date/time for ordering).

3. **Map attendees -> AEs.**
   - If vibe profile has `territory` with nested `account_executives` (each with `name`, `email`), build a list of AE emails. Match attendee emails to this list. Each matched attendee = one AE with an upcoming review. **Note:** The profile's account list per AE is for display/calendar only -- never use it for territory or UCO data extraction (see Phase 2).
   - If the profile has no territory / account_executives, **do not assume AEs.** Ask: "No territory in vibe profile. Which AE(s) should I prepare reviews for? Provide full name and/or email, or say 'all' and list them."
   - **Manual override:** If the user explicitly said "run bi-weekly review for [AE name/email]", use that AE (or those AEs) and skip calendar-based discovery.

4. **Result:** Ordered list of `[AE Name]`, `[AE Email]` with upcoming 2by2/b2b in the next 7 days. If the list is empty (no matching events and no manual AE), exit gracefully: "No 2by2/b2b meetings found in the next 7 days and no AE specified. Specify an AE to run a one-off review, or run again when meetings are scheduled."

---

## Phase 1: Load prior snapshot (per AE)

- For each AE, set `[AE Email Safe]` = `[AE Email]` with `@` -> `_at_`.
- Path: `[Snapshot Base][AE Email Safe]/latest_snapshot.json`.
- If the file exists, load it. Snapshot should contain: UCO stages/momentum/dates, consumption totals by SKU, WAU, new workspaces list, and a timestamp.
- If it does not exist, treat as first run: no prior snapshot; all "deltas" and "changes since last review" will be N/A or "baseline".

---

## Phase 2: Data collection (per AE)

**Skills to load:** `genie-rooms` (first), `logfood-querier`, `salesforce-actions`, `databricks-authentication`, `salesforce-authentication`. Apply region filter where relevant (e.g. `FEPhysicalRegion__c = 'EMEA'`) to avoid cross-region leakage.

**Fiscal context from today's date (use for all quarter-scoped data):** Compute once at the start of Phase 2 from the **run date** (today) using the shared fiscal calendar utility.

> **Shared resource:** `../../resources/fiscal_calendar.py` (single source for all fe-manager skills). Run directly (`python3 ../../resources/fiscal_calendar.py`) for JSON output, or import the function in Python. See file docstring for SQL format notes.

Run at the start of Phase 2:
```python
import subprocess, json
ctx = json.loads(subprocess.run(
    ["python3", "../../resources/fiscal_calendar.py"],
    capture_output=True, text=True
).stdout)
# OR if running from an absolute path:
# import sys; sys.path.insert(0, os.path.expanduser("~/.vibe/marketplace/plugins/fe-manager/resources"))
# from fiscal_calendar import databricks_fiscal_context; ctx = databricks_fiscal_context()
# Produces: fiscal_year, fiscal_quarter, fiscal_year_quarter_str ("FY'27 Q1"),
#           quarter_start, quarter_end, prior_fiscal_year, prior_fiscal_quarter,
#           next_fiscal_year, next_fiscal_quarter
```

Set from `ctx`:
- **[Current Date]** = today's date (YYYY-MM-DD).
- **[Current Fiscal Year]** = `ctx["fiscal_year"]`, **[Current Fiscal Quarter]** = `ctx["fiscal_quarter"]`.
- **[Current Quarter Date Range]** = `ctx["quarter_start"]` to `ctx["quarter_end"]`. Use this to identify UCOs whose `Implementation_Start_Date__c` or `Full_Production_Date__c` falls within this range.
- **[Next Fiscal Quarter / Year]** = `ctx["next_fiscal_quarter"]` / `ctx["next_fiscal_year"]`. Derive **[Next Quarter Date Range]** by calling `databricks_fiscal_context()` with the first day of the next quarter.
- **[Prior Fiscal Quarter / Year]** = `ctx["prior_fiscal_quarter"]` / `ctx["prior_fiscal_year"]`.
- Use `ctx["fiscal_year_quarter_str"]` (e.g. `"FY'27 Q1"`) as the string filter value in `account_active_users_quarterly`. Use `ctx["fiscal_year"]` and `ctx["fiscal_quarter"]` as integers in `rpt_individual_obt_gtm`.
- In all narrative and output, label quarters explicitly (e.g. "FY27 Q1 (Feb–Apr 2026)") so the review is unambiguous.

**Territory account list for this AE (mandatory -- do not use vibe profile):** The vibe profile may list only a subset of accounts (e.g. "key" or "active" accounts). For UCO, consumption, WAU, and workspace data you **must** resolve the full territory from Salesforce/Logfood.

1. **Resolve AE Salesforce User Id:** Query `main.sfdc_bronze.user` (latest `processDate`), filter by `Email = '[AE Email]'`. Persist `[AE SFDC User Id]`.
2. **Full territory from Logfood (primary):** Query `main.sfdc_bronze.accountteammember` (latest `processDate`) JOIN `main.sfdc_bronze.account` (latest `processDate`) ON `atm.AccountId = a.Id`, WHERE `atm.UserId = '[AE SFDC User Id]'` AND `atm.TeamMemberRole IN ('Account Executive', 'Additional AE', 'Secondary AE')`. Select DISTINCT `a.Id`, `a.Name`. This returns all accounts where the AE is on the team in an AE role.
3. **Optional -- include owned accounts:** UNION with `main.sfdc_bronze.account` WHERE `OwnerId = '[AE SFDC User Id]'` (same processDate filter) to include accounts owned by but not on the team (if any). Use distinct account IDs.
4. **Persist** the full list as `territory_account_ids` and `territory_account_names` for all Phase 2 queries (UCO, consumption, WAU, new workspaces, targets). Validate count: if the number seems low (e.g. fewer than 10 for an enterprise AE), re-check User Id and TeamMemberRole values.

**UCO extraction:** Use the same `territory_account_ids` from step 2-3. Filter UCO by `Account__c IN (territory_account_ids)` and `Stages__c IN ('U1','U2','U3','U4','U5','U6')`. Do not use vibe profile account list for UCO or consumption.

### 2a. UCO pipeline (GTM Use Case Genie FIRST, Logfood SQL as fallback)

**Primary source: GTM Use Case Genie (`go/gtm_uco_genie`, room 13).** Use the genie-rooms skill to query this room with natural language. It is optimized for UCO stage, size ($DBUs), pipe gen, and progression data and should be attempted before any direct SQL query. Example commands:

```bash
# Step 1: Get full UCO list for the AE's territory
python3 resources/genie_rooms.py --room gtm_uco_genie ask \
  "Show all use cases for AE email [AE Email] in stages U1 through U6. Include: use case name, account name, stage, days in stage, implementation status color, implementation start date, full production date, monthly DBU dollars, and whether it is in plan."

# Step 2: Get at-risk and current-quarter UCOs
python3 resources/genie_rooms.py --room gtm_uco_genie ask \
  "For AE [AE Email], which use cases in U1-U5 have implementation start date or production date between [Current Quarter Start] and [Current Quarter End]? Show stage, days in stage, implementation status, and monthly DBU dollars."

# Step 3 (optional follow-up): Stage distribution summary
python3 resources/genie_rooms.py --room gtm_uco_genie follow-up <conversation-id> \
  "Summarize by stage (U1 through U6) — count and total monthly DBU dollars."
```

Collect from Genie: UCO name, account name, stage, days-in-stage, implementation status color, implementation start date, full production date, monthly DBU $, in-plan flag. Persist as the UCO list.

**Fallback and enrichment: Logfood SQL (mandatory for deep notes read).** The Genie does not reliably return free-text fields (NextSteps__c, Implementation_Notes__c, Blocker_Comments__c, Demand_Plan_Next_Steps__c). After getting the structured list from Genie, run a targeted SQL query to retrieve the notes for the non-U6 UCOs only — these are needed for Phase 3a's deep read.

```sql
SELECT
  uc.Name, uc.Account__c, a.Name AS AccountName,
  uc.Stages__c, uc.Implementation_Status__c,
  uc.NextSteps__c, uc.Implementation_Notes__c,
  uc.Demand_Plan_Next_Steps__c, uc.Blocker_Comments__c,
  uc.Last_Stage_Modified_Date__c, uc.CurrentStageDaysCount__c,
  uc.Implementation_Start_Date__c, uc.Full_Production_Date__c,
  uc.MonthlyTotalDollarDBUs__c, uc.LastModifiedDate
FROM main.sfdc_bronze.usecase__c uc
LEFT JOIN main.sfdc_bronze.account a
  ON uc.Account__c = a.Id
  AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
WHERE uc.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
  AND uc.Account__c IN (<territory_account_ids>)
  AND uc.Stages__c IN ('U1','U2','U3','U4','U5')
```

Merge the Genie results (structured pipeline data) with the SQL results (notes and text fields) by UCO name + account. If the Genie query fails or times out, fall back to querying Logfood SQL directly for all fields.

- **Momentum read (every U2-U5 UCO):** Read the notes fields from SQL to assign: `ACTIVE`, `DRIFTING`, `STALLED`, `AT-RISK`. This overrides the Genie's implementation status color (see Phase 3a Step 1).
- **Days-in-stage:** Use CurrentStageDaysCount__c from Genie or SQL; else DATEDIFF(CURRENT_DATE(), COALESCE(Last_Stage_Modified_Date__c, LastModifiedDate)). Green (<90d), Yellow (90-180d), Red (>180d).
- **Historical diff:** Optionally ask the Genie a follow-up: "Which of these use cases changed stage in the last 14 days?" If not available, query usecase__c for processDate approx 14 days ago to detect changes.

### 2b. Consumption trends (Logfood)

- **Source:** `main.fin_live_gold.paid_usage_metering`. Filter: `sfdc_account_id IN (territory_account_ids)`, `paying_status = 'PAYING_STATUS_PAYING'`. Add `record_type = 'RECORD_TYPE_ORIGINAL'` only if the column exists in your environment.
- **Queries:** Group by `sfdc_account_id`, `sfdc_account_name`, `product_type` (or `sku`), and week (e.g. DATE_TRUNC('week', date)) for the last 4 weeks. Compute total usage_dollars per week.
- **Deltas:** 2-week-over-2-week (last 14 days vs prior 14 days) for territory total and per-account. Flag new SKUs: product_type/sku present in last 2 weeks and absent in the 2 weeks before. Flag growth >20% or decline >10%.

### 2c. WAU and adoption (Logfood)

- **Source:** `main.gtm_gold.account_active_users_quarterly`.

**Schema notes (verified 2026-02-23 — do not guess column names):**
- `account_id` (STRING) — this IS the Salesforce account ID (same values as `sfdc_account_id` in PUM). Use `account_id IN (territory_account_ids)` directly.
- `fiscal_year_quarter` (STRING) — format is `"FY'27 Q1"` (with apostrophe, space before Q). NOT integers. Example values: `"FY'27 Q1"`, `"FY'26 Q4"`.
- `wau_t7d` (BIGINT) — weekly active users, current quarter.
- `wau_t7d_prior_quarter` (BIGINT) — WAU from the prior quarter (already pre-computed; no need to pull two rows and compute yourself).
- `mau_t28d` / `mau_t28d_prior_quarter` — monthly active users, current and prior quarter.
- No `account_name` column — to get account names, join with a name map from PUM or the territory account list you already built.

**Correct query:**

```sql
SELECT
  account_id,
  fiscal_year_quarter,
  wau_t7d,
  wau_t7d_prior_quarter,
  ROUND(
    (wau_t7d - wau_t7d_prior_quarter) * 100.0 / NULLIF(wau_t7d_prior_quarter, 0),
    1
  ) AS wau_qoq_pct
FROM main.gtm_gold.account_active_users_quarterly
WHERE account_id IN (<territory_account_ids>)
  AND fiscal_year_quarter = 'FY''[YY] Q[Q]'   -- e.g. "FY'27 Q1"
ORDER BY wau_t7d DESC
```

To build the `fiscal_year_quarter` string: take `[Current Fiscal Year]` (e.g. 27) and `[Current Fiscal Quarter]` (e.g. 1), then construct `"FY'27 Q1"`. In SQL use `CONCAT("FY'", [FY], " Q", [FQ])` or just hardcode the string.

- Compute QoQ change using `wau_qoq_pct`; label: Rising (>+10%), Flat (±10%), Declining (<-10%).
- Accounts with `wau_t7d = 0` and `wau_t7d_prior_quarter = 0` — no active users (prospect or inactive).
- **Do not attempt to join on `sfdc_account_id`** — that column does not exist in this table. `account_id` is already the SFDC ID.

### 2d. New workspaces

**Source 2 (SFDC) -- workspaces created in last 14 days:**

```sql
SELECT w.Name, w.Status__c, w.CreatedDate, a.Name AS account_name
FROM main.sfdc_bronze.workspace__c w
JOIN main.sfdc_bronze.account a ON w.Account__c = a.Id
WHERE w.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.workspace__c)
  AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
  AND w.Account__c IN (<territory_account_ids>)
  AND w.CreatedDate >= DATEADD(DAY, -14, CURRENT_DATE())
```

**Source 3 (consumption) -- workspaces first consuming in last 14 days:**

```sql
WITH recent AS (
  SELECT DISTINCT sfdc_workspace_id, sfdc_workspace_name, sfdc_account_name
  FROM main.fin_live_gold.paid_usage_metering
  WHERE sfdc_account_id IN (<territory_account_ids>)
    AND date >= DATEADD(DAY, -14, CURRENT_DATE())
    AND paying_status = 'PAYING_STATUS_PAYING'
),
prior AS (
  SELECT DISTINCT sfdc_workspace_id
  FROM main.fin_live_gold.paid_usage_metering
  WHERE sfdc_account_id IN (<territory_account_ids>)
    AND date BETWEEN DATEADD(DAY, -28, CURRENT_DATE()) AND DATEADD(DAY, -14, CURRENT_DATE())
    AND paying_status = 'PAYING_STATUS_PAYING'
)
SELECT r.* FROM recent r
LEFT JOIN prior p ON r.sfdc_workspace_id = p.sfdc_workspace_id
WHERE p.sfdc_workspace_id IS NULL
```

Combine: new SFDC workspaces + workspaces that just started consuming. Enrich with account name, tier, region where available.

### 2e. Target and forecast (Logfood)

- **Source:** `main.gtm_gold.rpt_individual_obt_gtm`. Filter: `user_email = '[AE Email]'` AND `fiscal_quarter = [Current Fiscal Quarter]` AND `fiscal_year = [Current Fiscal Year]` (from today's date fiscal context). Columns: target_dbu_dollars, submitted_my_call, forecast_straight_line_t28d_quarterly.
- Use for pipeline sufficiency: compare target vs AE forecast vs DS forecast; weight U4/U5 pipeline to project quarter-end. In output, label as "FY[Current Fiscal Year] Q[Current Fiscal Quarter] ([Current Quarter Date Range])".

### 2f. Consuming accounts with no U1-U5 use cases (gap for current and next quarter)

- **Purpose:** Identify accounts that have consumption but no active use case (U1-U5) in the system, for current quarter and next quarter planning.
- **Consuming accounts:** From 2b (consumption), take distinct `sfdc_account_id` (and account name) where there is paid consumption in the last 4 weeks. Persist as `consuming_account_ids`.
- **Accounts with at least one U1-U5 UCO:** From 2a (UCO extraction), take distinct `Account__c` where `Stages__c IN ('U1','U2','U3','U4','U5')`. U6-only accounts count as "no active UCO" for this check. Persist as `accounts_with_u1_u5_uco`.
- **Gap:** `consuming_accounts_no_u1_u5 = consuming_account_ids` minus `accounts_with_u1_u5_uco`. These are accounts we are getting revenue from but have no U1-U5 use case in the system.
- **Persist** the list (account Id, account name, and optionally last 4-week consumption $) for Phase 3 and output.

### 2g. Account behavioral signals (optional)

**Run this step only if the user explicitly requests signals** (e.g. "include signals", "run signals analysis", "add platform health", "include behavioral patterns").

Invoke the `ae-accounts-signals` skill, passing:
- `territory_account_ids` and `territory_account_names` already resolved in Phase 2 steps 1–4 above.
- The logfood Databricks CLI profile name.

The `ae-accounts-signals` skill will run five data-collection phases (workspace security flags, centralized system tables, new workspaces, WAU trends, feature-level adoption) and return a structured per-account signals report. Store the output as `[AE signals output]` for inclusion in Phase 4 Section 6.

**Important:** when invoking `ae-accounts-signals` from this skill, do NOT have it create its own Google Doc — the signals output will be embedded in the biweekly review doc (Section 6). The ae-accounts-signals skill skips its Phase 6 doc creation when called as a sub-skill from ae-biweekly-review.

---

## Phase 3: Analysis engine (per AE)

### 3a. UCO deep assessment (current and next quarter, excluding U6)

**Scope:** All UCOs with Stages__c IN ('U1','U2','U3','U4','U5'). Exclude U6 (live). For each UCO, read the **actual text** of NextSteps__c, Implementation_Notes__c, Demand_Plan_Next_Steps__c, and Blocker_Comments__c. Do **not** rely solely on Implementation_Status__c color -- the color is often stale or optimistic; the notes are the ground truth.

**Step 1 -- Deep read per UCO.** For each non-U6 UCO, extract from the notes:
- **Last meaningful update date:** Most recent dated entry in NextSteps__c or Implementation_Notes__c.
- **Actual next action and owner:** Is there a specific next step with a date? Who owns it -- AE, SA, customer, partner?
- **Real blockers:** Read Blocker_Comments__c AND any blocker language buried in notes (e.g. "waiting for", "delayed", "on hold", "no resources", "deprioritized", "champion left", "no budget", "C-Level awareness needed").
- **Implementation plan agreed?** Is there a concrete milestone or date in Implementation_Notes__c, or is it vague / still TBD?
- **Momentum signal** -- assign one of:
  - `ACTIVE`: Concrete action taken in last 14 days with clear owner and specific next step.
  - `DRIFTING`: Last meaningful action 15-60 days ago, or next steps are vague ("next checkin", "no update"), no concrete milestone.
  - `STALLED`: Last update >60 days ago, or notes explicitly say "no update" repeatedly, or tech win date passed with no stage move.
  - `AT-RISK`: Explicit blocker present -- resource shortage, champion departure, competitive threat, explicitly deprioritized by customer or AE, implementation date already passed without U6, C-Level awareness not secured for U4+, or partner contract/signing delay blocking start.

**Step 2 -- Quarter relevance classification.** Using Implementation_Start_Date__c and Full_Production_Date__c:
- **Current quarter ([Current Quarter Date Range]):** A UCO is current-quarter-relevant if Implementation_Start_Date__c or Full_Production_Date__c falls within [Current Quarter Date Range], OR if the UCO is U4/U5 (actively onboarding). Flag OVERDUE if impl/production date has already passed without moving to U6.
- **Next quarter ([Next Quarter Date Range]):** A UCO is next-quarter-relevant if Implementation_Start_Date__c or Full_Production_Date__c falls within [Next Quarter Date Range], OR if current momentum suggests it can realistically reach U4+ by next quarter start.

**Step 3 -- Action classification.** Classify each current- or next-quarter UCO as:
- **[RED] Action needed this week/next:** AT-RISK or STALLED with current-quarter relevance; OR a concrete, actionable blocker that AE/Databricks can address right now (provide API docs, schedule exec intro, complete nomination, confirm partner engagement, send architecture guidance).
- **[YELLOW] Watch -- push in next 2 weeks:** DRIFTING with next-quarter relevance; or scheduled next step that has not yet been confirmed or acted on.
- **[GREEN] On track:** ACTIVE with a concrete upcoming milestone and no open blockers.
- **[PARKED]:** Explicitly deprioritized by customer or AE; dates are H2 or later; no Q1/Q2 relevance. Do not surface in the primary output tables.

**Step 4 -- Produce two focused output tables** (see Phase 4 Section 2 format):
- **Table A -- Current quarter, action needed ([RED] and [YELLOW] only):** Focus on UCOs with current-quarter implementation or production dates. Include the specific blocker or action from the notes. Omit [GREEN] on-track unless they are at a critical milestone this week. Omit [PARKED] entirely.
- **Table B -- Next quarter pipeline in build ([YELLOW] and [RED]):** UCOs that need groundwork laid THIS quarter to land next quarter. For each, state what must happen now. Omit [PARKED] and [GREEN] on-track that need no attention.

**Hygiene flags (always append after the two tables, as a separate list):**
- U4/U5 UCOs where Full_Production_Date__c is in the past and stage is still U4/U5 (overdue).
- U4/U5 UCOs with no Implementation_Notes__c or notes older than 30 days (stale onboarding record).
- U3 UCOs where NextSteps__c was last updated >60 days ago (stalled tech win -- consider close or reset).
- Any UCO where CurrentStageDaysCount__c >180 days (Red zone -- recommend stage reset or close).
- U3/U4 UCOs where Implementation_Status__c = Green but the notes reveal a blocker (color-note mismatch -- fix the color).

### 3b. Consumption trend summary

- Territory total: 2-week trend (up/down/flat) and %.
- Top 5 account movers (up and down).
- New SKU list.
- **Consuming accounts with no U1-U5 use cases (current and next quarter):** Use the gap list from 2f. For each account in `consuming_accounts_no_u1_u5`, we have consumption but no active pipeline/onboarding UCO (U1-U5) in the system. Recommend: create a UCO or document why no UCO is needed (e.g. renewal-only, non-strategic). Call this out in Section 2 and Section 3 (questions for the meeting).

### 3c. Pipeline sufficiency

- Current quarter (FY[Current Fiscal Year] Q[Current Fiscal Quarter]): target vs submitted_my_call vs forecast_straight_line_t28d_quarterly; weighted U4+U5 contribution. Verdict: ON TRACK / AT RISK / MATERIAL GAP.
- Next quarter: Enough U1-U3 pipeline for next quarter target?

### 3d. Diff vs last review

- UCO stage changes, consumption deltas, WAU movement, new workspaces, new risks or resolved risks (from snapshot comparison).

---

## Phase 4: Output generation

Produce the following sections (for Google Doc and for Slack summary).

**Section 1 -- Territory changes since last review (~2 weeks)**
Consumption trend; new SKUs; WAU changes; UCO stage movements; new workspaces (created or first consuming).

**Section 2 -- Use case review (non-U6 only)**

Lead with two action-focused tables from Phase 3a:

*Table A: Current quarter -- needs action or watch ([RED] and [YELLOW])*
Columns: UCO Name | Account | Stage | Days-in-stage | Impl/Prod Date | Monthly $ | Action tag | Specific action or blocker (from notes)

*Table B: Next quarter pipeline -- attention needed now ([YELLOW] and [RED])*
Columns: UCO Name | Account | Stage | Impl/Prod Date | Monthly $ | Action tag | What must happen this quarter to keep on track

*Hygiene flags:* List from Phase 3a Step 4, with specific UCO names and recommended fix.

*Consuming accounts with no U1-U5 UCOs:* List from 2f with account name and consumption $; recommended action: create UCO or document why not.

**Section 3 -- Questions for the meeting**
5-8 account-specific, data-anchored questions. Derived directly from the [RED] action items and hygiene flags in Section 2. Each question should reference a specific UCO, date, or data point. Include at least one question per consuming account with no U1-U5 UCO.

**Section 4 -- Pipeline sufficiency**
Target vs AE vs DS forecast for FY[Current Fiscal Year] Q[Current Fiscal Quarter] ([Current Quarter Date Range]); next quarter pipeline health; bold verdict (ON TRACK / AT RISK / MATERIAL GAP).

**Section 5 -- Other trends**
Adoption (WAU, new workspaces); consumption anomalies; contract/burst alerts if applicable.

**Section 6 -- Platform health signals (only if Phase 2g was run)**
Insert the full `ae-accounts-signals` output (`[AE signals output]`) here. This includes per-account Green (positive momentum) and Red/Orange (worst practices / risks) signals, plus the territory summary table.

In the **Slack DM**, include a 2–3 line condensed version: the top 2 positive signals and top 2 risks across the territory, then link to the Google Doc for the full signals report.

---

## Phase 5: Persistence, doc creation, Slack delivery

1. **Save snapshot.** Ensure directory exists: `[Snapshot Base][AE Email Safe]/` (e.g. `mkdir -p`). Write current state to `snapshot_{YYYY-MM-DD}.json` in that directory. Update `latest_snapshot.json` (copy or symlink) in the same directory. Include: UCO list with stage/momentum/dates, consumption by SKU/account, WAU, new workspaces, timestamp.

   **Retention cleanup (run immediately after writing the new snapshot):** Bi-weekly cadence accumulates files quickly. Keep storage bounded:

   ```bash
   SNAP_DIR="${HOME}/.vibe/cache/ae-biweekly-reviews/[owner_safe]/[AE Email Safe]"

   # Remove snapshots older than 90 days
   find "$SNAP_DIR" -name "snapshot_*.json" -mtime +90 -delete

   # Keep at most 6 dated snapshots (retain newest; 6 ≈ 3 months of history)
   ls -t "$SNAP_DIR"/snapshot_*.json 2>/dev/null | tail -n +7 | xargs rm -f
   # latest_snapshot.json is never deleted by the above (name doesn't match snapshot_*.json)
   ```

   If a previous snapshot is deleted, note in console output: "Pruned old snapshots for [AE Name]; [N] retained." The skill always treats a missing snapshot as a first run — safe to clear the directory manually at any time.

2. **Google Doc.** Use `google-docs` skill (markdown-first): create doc titled "Bi-weekly Review: [AE Name] - [date]". Paste Sections 1-5 in markdown, then convert to Google Doc. Share/link as needed for the review owner.

3. **Slack.** Send a DM to `[Review Owner Slack]` with: (a) which AE, (b) Section 1 summary (territory changes), (c) Section 3 (questions for the meeting), (d) link to the Google Doc. If Slack is not set, print this to the console and note that Slack can be added to vibe profile for future DMs.

---

## Data sources reference

| Data | Source |
|------|--------|
| UCO pipeline (structured) | GTM Use Case Genie (`go/gtm_uco_genie`, room 13) -- stage, size, dates, status, pipe gen, progression |
| UCO pipeline (text/notes) | `main.sfdc_bronze.usecase__c` -- NextSteps__c, Implementation_Notes__c, Blocker_Comments__c (fallback for all fields if Genie unavailable) |
| Consumption | `main.fin_live_gold.paid_usage_metering` (by account, SKU, workspace, date) |
| WAU | `main.gtm_gold.account_active_users_quarterly` — filter: `account_id IN (territory_account_ids)` (`account_id` IS the SFDC ID, same values as sfdc_account_id in PUM) AND `fiscal_year_quarter = "FY'27 Q1"` (string with apostrophe + space before Q, e.g. `"FY'27 Q1"`, `"FY'26 Q4"`). Key columns: `wau_t7d` (current), `wau_t7d_prior_quarter` (prior quarter pre-joined). No `sfdc_account_id` or `account_name` columns exist — do not use them. |
| New workspaces (created) | `main.sfdc_bronze.workspace__c` (CreatedDate, Account__c) |
| New workspaces (first consumption) | `main.fin_live_gold.paid_usage_metering` (sfdc_workspace_id, date window diff) |
| Workspace metadata | `main.certified.workspaces_latest` (enrichment) |
| Workspace security flags + Databricks UUIDs (signals) | `main.certified.workspaces_latest` — `salesforce_account_id` → `account_id` (Databricks UUID), security flags: `is_public_access_enabled`, `is_no_public_ip_enabled`, `is_identity_federation_enabled`, `feature_tier`. Used by `ae-accounts-signals` Phase 1. |
| Compute/query/job patterns (signals) | `main.centralized_system_tables.*` — filter by `account_id` (Databricks UUID from workspaces_latest, NOT SFDC ID). Tables: `compute_clusters`, `compute_warehouses`, `query_history`, `lakeflow_job_run_timeline`, `lakeflow_jobs`. Used by `ae-accounts-signals` Phase 2. |
| New workspaces first-consuming (signals) | `main.fin_live_gold.paid_usage_metering` — 28d vs prior 28d by `sfdc_workspace_id` to find net-new consuming workspaces. Used by `ae-accounts-signals` Phase 3. |
| WAU trends QoQ (signals) | `main.gtm_gold.account_active_users_quarterly` — same schema as 2c. Rising (>+10%), Flat (±10%), Declining (<-10%). Used by `ae-accounts-signals` Phase 3. |
| Feature-level adoption (signals) | `main.data_product_features.account_metrics` — t28d columns: `genie_num_events_t28d`, `databricks_assistant_num_users_t28d`, `lakeview_num_users_t28d`, `mlflow_num_api_calls_t28d`, `dlt_dbus_t28d`, `apps_dbus_t28d`, `scim_num_api_calls_t28d`. Filter by `salesforce_account_id` (not `sfdc_account_id`). Used by `ae-accounts-signals` Phase 4. |
| Targets/forecasts | `main.gtm_gold.rpt_individual_obt_gtm` |
| Territory accounts | **Logfood only:** resolve `main.sfdc_bronze.user` (Id by email) then `main.sfdc_bronze.accountteammember` (UserId, TeamMemberRole IN ('Account Executive','Additional AE','Secondary AE')) + optional account.OwnerId. Do not use vibe profile account list. |
| Calendar | Google Calendar (primary, current user) |
| Identity / territory | `~/.vibe/profile` (user, optional territory.account_executives) |

---

## Checklist (per run)

- [ ] Review owner set from vibe profile (or user input); snapshot path uses owner-safe folder.
- [ ] Calendar searched for 2by2/b2b in next 7 days; AEs resolved from attendees or manual list.
- [ ] Territory account IDs resolved per AE; region filter applied where relevant.
- [ ] Fiscal context computed: FY = Databricks Feb 1 start; fiscal_year and fiscal_quarter derived from today's date; [Current Quarter Date Range] and [Next Quarter Date Range] computed.
- [ ] UCO data: GTM Use Case Genie (go/gtm_uco_genie) queried first for structured pipeline data (stage, size, dates, status); Logfood SQL run second for text fields (NextSteps__c, Implementation_Notes__c, Blocker_Comments__c) on U1-U5 UCOs only; results merged. If Genie unavailable, full SQL fallback used.
- [ ] Deep read applied per non-U6 UCO from the notes fields; momentum assigned from notes not color.
- [ ] Two output tables produced: Table A (current quarter action needed) and Table B (next quarter pipeline); hygiene flags listed.
- [ ] Consuming accounts with no U1-U5 UCO (2f): gap computed and included in Section 2 and Section 3.
- [ ] New workspaces: SFDC CreatedDate + PUM first-consumption query both run.
- [ ] Snapshot saved under [Snapshot Base][AE Email Safe]/; Slack DM sent to review owner (or output printed if no Slack).
- [ ] Snapshot retention cleanup ran: files >90 days old removed; at most 6 dated snapshots per AE retained. Storage location: `~/.vibe/cache/ae-biweekly-reviews/{owner_safe}/` — safe to delete this directory entirely at any time; next run treats missing snapshot as first run.

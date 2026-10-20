---
name: dsa-business-overview
description: Generate the monthly DSA Business Update as an editable Google Doc and polished HTML Gmail draft. Queries UCO pipeline, subscription activity, FTE capacity, live use cases, risks, and formats into a newsletter-style document for leadership. Phase 1 creates an editable Google Doc (single master doc with monthly sections). Phase 2 converts the edited content to a rich HTML email draft. Works for any DSA manager. Use when someone says business overview, monthly overview, team overview, leadership report, DSA update, DSA newsletter, business update.
user-invocable: true
---

# DSA Business Update Generator

Generate a polished monthly DSA Business Update for any DSA manager. Phase 1 creates an editable Google Doc; Phase 2 converts to a rich HTML Gmail draft. All data is queried deterministically from Logfood — every metric has an exact SQL definition so results are consistent and reproducible for any manager.

**Reference Format**: [DSA Business Update — INSWAM](https://docs.google.com/document/d/1ZDSksSA_ufYQim5vLhUxKyRr7dn7JEchR1IL5VjEIZ8/edit)

## When to Use This Skill

- Generate the monthly DSA Business Update document for any DSA manager's team
- Create a team-level UCO pipeline summary for leadership
- Produce a formatted newsletter with live use cases, risks, subscription activity
- Prepare for monthly DSA team review meetings

## Prerequisites

Before running this skill, ensure the following are authenticated:
1. **Databricks** — Run `/databricks-authentication` (for Logfood queries)
2. **Google** — Run `/google-auth` (for Google Doc editing + Gmail draft)
3. **Salesforce** — Run `/salesforce-authentication` (for UCO details and contacts)

## Required Information

The skill needs: **which DSA manager's team** to generate the overview for. Provided as: $ARGUMENTS

If no manager name is provided, ask:
> "Which DSA manager's team should I generate the Business Update for? Please provide their name."

## Reference Files

- **`resources/DSA_LT_QUERIES.md`** — SQL query templates for all team-level data
- **`resources/BUSINESS_OVERVIEW_TEMPLATE.md`** — Google Doc markdown template and heading hierarchy rules (Phase 1)
- **`resources/EMAIL_TEMPLATE.html`** — HTML email structure, inline CSS patterns, and color palette (Phase 2)

---

## Step 0: Identify Manager and Discover Team

**Goal**: Find the manager's team roster and determine the vertical/team context.

### Query Team Roster

Use the manager name to find all DSAs on their team:

```sql
SELECT dsa AS name, email, hire_date, dsa_manager, bu, sales_subregion_level_1, cost_center, title_curated
FROM main.field_dsa.dsa_roster_curr
WHERE LOWER(dsa_manager) LIKE '%{manager_name}%'
ORDER BY dsa
```

Execute via `databricks api post /api/2.0/sql/statements/ --profile=logfood`.

### Determine Vertical/Team Context

From the roster results:
- **`sales_subregion_level_1`** or **`bu`** → Use as the vertical/team identifier in the document title (e.g., "INSWAM", "Enterprise West", etc.)
- If mixed, use the most common value or ask the user for a label

### Build Working Variables

From the roster query, extract and store:
- `dsa_names`: List of full names (e.g., `['Richa Sethi', 'Patrick Chan', ...]`)
- `dsa_emails`: List of emails
- `manager_name`: Full manager name
- `vertical_label`: Team/vertical identifier for the document title
- `dsa_count`: Number of DSAs on team
- `account_names`: Will be populated from assignment data

---

## Step 1: Determine Report Month and Compute Date Variables

Before querying data, compute all date variables for the report:

```
report_month        = The month being reported (e.g., February 2026)
month_start         = First day of report month (e.g., 2026-02-01)
month_end           = First day of next month (e.g., 2026-03-01)  — used as exclusive upper bound
fy_start            = February 1 of current FY (e.g., 2026-02-01 for FY27)
quarter_start       = First day of current fiscal quarter
quarter_end         = Last day of current fiscal quarter
quarter_num         = Q1/Q2/Q3/Q4
quarter_months      = e.g., "Feb–Apr 2026"
is_quarter_end      = True if report_month is the last month of a fiscal quarter (Apr, Jul, Oct, Jan)
projection_snapshot = The earliest projection_month_end_date >= month_end in rpt_use_case_pipeline_monthly
```

**Fiscal Calendar**: FY starts Feb 1. Q1=Feb–Apr, Q2=May–Jul, Q3=Aug–Oct, Q4=Nov–Jan.

---

## Step 2: Parallel Data Collection

Launch **two sub-agents simultaneously** to gather data in parallel. Pass `dsa_names`, `manager_name`, and all date variables.

### Agent 1: Pipeline Analyst (`fe-dsa-lt:pipeline-analyst`)

The agent will query `main.gtm_gold.rpt_use_case_pipeline_monthly` using the nearest `projection_month_end_date` snapshot.

**CRITICAL: UCO-Level DSA Attribution — SFDC Only (No Account-Level Fallback)**

The `dsa` column on `rpt_use_case_pipeline_monthly` is the **account-level** DSA, NOT the UCO-level DSA. In multi-DSA accounts this misattributes use cases. **Only include UCOs where the SFDC `DSA__c` field directly resolves to a team member.** Do NOT fall back to the account-level `p.dsa` column — this inflates pipeline numbers with UCOs not actually owned by a DSA.

1. Join `rpt_use_case_pipeline_monthly p` → `main.sfdc_bronze.usecase__c u` (on `p.usecase_id = u.Id`)
2. Left join → `main.sfdc_bronze.user usr` (on `u.DSA__c = usr.Id`) to resolve the SFDC User ID to a name
3. Apply strict filter: only include UCOs where `usr.Name IN ({team_dsa_list})`

```sql
WITH resolved AS (
  SELECT p.*, usr.Name AS sfdc_dsa_name,
    CASE
      WHEN usr.Name IS NOT NULL AND usr.Name IN ({team_dsa_list}) THEN usr.Name
      ELSE NULL
    END AS effective_dsa
  FROM main.gtm_gold.rpt_use_case_pipeline_monthly p
  JOIN main.sfdc_bronze.usecase__c u ON p.usecase_id = u.Id
    AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
  LEFT JOIN main.sfdc_bronze.user usr ON u.DSA__c = usr.Id
    AND usr.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
  WHERE p.projection_month_flag = true
    AND p.projection_month_end_date = (SELECT MIN(projection_month_end_date)
        FROM main.gtm_gold.rpt_use_case_pipeline_monthly WHERE projection_month_flag = true)
)
SELECT * FROM resolved WHERE effective_dsa IS NOT NULL
```

Use `effective_dsa` as the DSA name in all pipeline queries below. Replace `p.dsa IN ({team_dsa_names})` with the CTE + `WHERE effective_dsa IS NOT NULL`.

Queries (all using the resolved CTE above):
1. U6 UCOs where `target_live_date >= month_start AND target_live_date < month_end` → **"went live this month"**
2. U6 UCOs where `target_live_date >= fy_start` → **FY-to-date live** (summary stats only)
3. All U5 UCOs → **active pipeline**
4. U5 UCOs where `target_live_date >= quarter_start AND target_live_date <= quarter_end` → **Q{X} at stake**
5. U5 UCOs ranked by `estimated_quarterly_dollar_dbus DESC`, top 5 → **Top 5 Onboarding**
6. U5 UCOs where `implementation_status IN ('Yellow', 'Red')` → **Risks & Blockers**

### Agent 2: Capacity Calculator (`fe-dsa-lt:capacity-calculator`)

The agent queries **two tables** — `dsa_bandwidth_table` for capacity totals, and `dsa_project_assignment_outcomes` for subscription detail:

1. **Total Deployed Capacity** — Query `main.field_dsa.dsa_bandwidth_table WHERE LOWER(dsa_manager) LIKE '%{manager_name}%'`. Extract per-DSA FTE from `bandwidth_bar_html` using regex. Count ASSIGNMENT accounts from `account_dsa_accounts_html`. This is the **authoritative source** for FTE/DSA/account totals (same table the DSA Operations Dashboard uses). **Do NOT sum `fte_req_current` from `dsa_project_assignment_outcomes`** — that table has overlapping subscription rows that double-count.
2. **Active account list** — Extract account names with `ASSIGNMENT` status from `account_dsa_accounts_html` in the bandwidth table. This gives the correct active account count.
3. **Subscription detail** — Query `main.field_dsa.dsa_project_assignment_outcomes` using `LATERAL VIEW EXPLODE(project_assignments) t AS pa` and `snapshot_date = MAX(snapshot_date)` for per-subscription detail (tier, type, dates). Use for the DSA Subscriptions table but NOT for FTE totals.
4. Previous expired subscriptions (`fte_req_current = 0`) for same accounts → **Net New FTE** calculation (only count incremental FTE: new subscription FTE minus previous subscription FTE)
5. Tier upgrade detection → annotate Type as "Renewal (upgraded from {old_tier})"
6. Transition detection → same account, different DSAs with overlapping/consecutive subscriptions → **Account Transitions**
7. `dsa_engagement_type = 'Invested DSA'` assignments → **Investment DSAs**

**Wait for both agents to complete before proceeding.**

---

## Step 2a: Compile Executive Snapshot

Using results from both agents, compute these **exact** metrics:

| Metric | Exact Computation |
|--------|-------------------|
| Use Cases Live This Month | Count of U6 UCOs where `target_live_date >= month_start AND target_live_date < month_end`. ARR = `SUM(estimated_quarterly_dollar_dbus) * 4`. Description also shows FY-to-date: count + ARR of U6 where `target_live_date >= fy_start`. |
| Active Onboarding Pipeline (U5) | Count + ARR of all U5 UCOs in the projection snapshot. ARR = `SUM(estimated_quarterly_dollar_dbus) * 4` |
| Q{X} ARR at Stake ({quarter_months}) | ARR of U5 UCOs where `target_live_date >= quarter_start AND target_live_date <= quarter_end` |
| New Subscriptions This Month | Split display: "{new_account_count} new accounts + {renewal_count} renewals · +{net_new_fte} FTE (net new)" (see Step 6 for new vs renewal and net new FTE logic) |
| Total Deployed Capacity | From `dsa_bandwidth_table`: `SUM(total_fte)` FTE · `COUNT(dsa)` DSAs · count of ASSIGNMENT accounts from `account_dsa_accounts_html`. **Do NOT use `dsa_project_assignment_outcomes`** — it double-counts due to overlapping subscription rows. |

**Quarter-end behavior**: On quarter-end months (Apr, Jul, Oct, Jan), append a quarter summary row: "Q{X} Total: {count} live · ${ARR} ARR"

---

## Step 3: Compile Use Cases Live This Month

**Filter**: U6 UCOs where `target_live_date >= month_start AND target_live_date < month_end`

Show **up to 5** rows ranked by ARR descending. If fewer went live, show all.

For each row: Account, Use Case name (hyperlinked to SFDC via `link_sfdc_usecase` if available), ARR (`estimated_quarterly_dollar_dbus * 4`), DSA (full name as-is from data).

**Description line above the table**: "{count} use cases reached production in {Month} — generating ${ARR} in new ARR. FY-to-date: {fy_count} live · ${fy_arr} ARR."

---

## Step 4: Compile Top 5 Onboarding Use Cases

From **all U5 UCOs** (not just this month), rank by `estimated_quarterly_dollar_dbus` DESC. Take the **top 5**.

For each, build a **numbered narrative entry** (NOT a table row):

```
**1. {Account} — {Use Case Name}**
${ARR} ARR · {target_month} · {DSA_name} · Status: {display_status}
{1-2 sentence narrative}
```

**Status display mapping** (source → display):
- `Green` → `On Track`
- `Yellow` → `At Risk`
- `Red` → `Red`
- `NULL` → `Not Set`

**To build the narrative**, use:
- `demand_plan_next_steps` — Latest next steps from Salesforce
- `implementation_status` — mapped to display status
- `num_of_blockers` — Number of active blockers
- `days_in_stage` — Time in current stage
- `target_live_date` vs today — Is it past due?

If `demand_plan_next_steps` is empty or generic, write a brief context sentence based on the data (e.g., "Migration in progress. No blockers reported.").

---

## Step 5: Compile Risks & Blockers

**Filter**: U5 UCOs only where `implementation_status IN ('Yellow', 'Red')`.

**Limit to top 5 by ARR descending.** This keeps the newsletter concise. If more than 5 exist, mention the overflow count (e.g., "5 of 8 at-risk use cases shown — ranked by ARR").

Build **numbered narrative cards** (NOT a table) — each risk gets its own block with Plan to Green, Key Risk/Blocker, and Engaged fields.

**Status display**: `Yellow` → "At Risk" (amber color), `Red` → "Red" (red color).

Sort by ARR descending, take top 5.

If no risks, write: "No critical risks or blockers this period."

---

## Step 6: Compile Subscription Activity

### Step 6.0: Deduplicate Against Prior Month's Email

**CRITICAL**: Before compiling subscription activity, **search Gmail for the previous month's business update email** (subject: `DSA InsWAM Business Update - {prior_month} {year}`) and read its content. Only include events that happened **in the current report month** — do NOT repeat subscriptions, transitions, or new logos already reported in a prior month's email.

- **Subscriptions**: If a subscription was already listed in a prior month's email (even if it's in the same fiscal quarter), exclude it from this month.
- **Transitions**: Same rule — only include transitions with effective dates in the current month.
- **New Logos**: Same rule — only new logos that started this month.
- **Executive Snapshot**: If all Q1 subscription activity was already reported in prior months, the "New Subscriptions This Month" row should say "None — all Q1 activity reported in {prior_month}".
- **Capacity Snapshot**: Always include — this reflects current state, not a one-time event.
- **Pipeline / Risks / Top 5**: Always include — these reflect current state and are updated monthly.

The Logfood queries return quarter-level data, but the email must be scoped to the **current month only** by diffing against what the prior email already covered.

### Step 6.1: Query Assignment Data

All assignment data comes from `main.field_dsa.dsa_project_assignment_outcomes` using `LATERAL VIEW EXPLODE(project_assignments) t AS pa` to access DSA-level detail. Use the **latest snapshot** (`snapshot_date = MAX(snapshot_date)`).

### Query Active Team Subscriptions

```sql
SELECT account_name,
       pa.assignment_resource_user_name AS dsa_name,
       project_service_tier AS tier,
       subscription_hours_weekly_current AS hours,
       fte_req_current AS fte,
       project_start_date, project_end_date,
       conversion_type, inferred_outcome, dsa_engagement_type
FROM main.field_dsa.dsa_project_assignment_outcomes
LATERAL VIEW EXPLODE(project_assignments) t AS pa
WHERE pa.assignment_resource_user_name IN ({team_dsa_list})
AND snapshot_date = (SELECT MAX(snapshot_date) FROM main.field_dsa.dsa_project_assignment_outcomes)
AND fte_req_current > 0
ORDER BY fte_req_current DESC, account_name
```

### DSA Subscriptions (New & Renewed Only)

Show only **new logos, renewals, and transitions** — subscriptions that started this fiscal quarter. **Exclude existing/unchanged subscriptions** from prior quarters to keep the update concise. The Total Deployed Capacity row in the Executive Snapshot already reflects the full team allocation including existing subscriptions.

Table columns: Account | DSA | Tier (Xh/wk) | FTE | Type

**Filtering**: Include CURRENT ASSIGNED subscriptions where `assignment_start_date` falls within the current fiscal quarter (>= quarter start date). Exclude subscriptions that started in prior quarters.

**Type determination** (from full assignment history — do NOT use `inferred_outcome`):

The `inferred_outcome` field is at the project level and does not distinguish DSA-level transitions. Instead, classify by comparing each new subscription against the **full assignment history across ALL managers/teams** (not just the current manager's team). Accounts may transition between teams (e.g., from Team A's DSA to Team B's DSA), so prior history must be checked globally.

1. Query using `DSA_LT_QUERIES.md` Section 12, which uses TWO scopes:
   - **Manager-filtered**: identifies new subscriptions this quarter for this manager's team
   - **Global (unfiltered)**: checks ALL prior DSA assignments at each account across ALL managers
2. For each new subscription (account A, DSA D, starting this quarter):
   - `account_has_prior` = any DSA assignment at account A with start_date before quarter_start, **across ALL managers**
   - `same_dsa_prior` = any assignment at account A by DSA D with start_date before quarter_start, **across ALL managers**

   Classification:
   - **NOT account_has_prior** → **New Logo** (no DSA has ever been assigned to this account)
   - **same_dsa_prior** → **Renewal** (same DSA renewing at same account)
   - **account_has_prior AND NOT same_dsa_prior** → **Transition** (account had a different DSA before — possibly from a different manager's team)

For tier upgrades on renewals, annotate: `"Renewal (upgraded from {old_tier})"` — detected when the current hours are higher than the most recent prior subscription's hours for the same DSA+account.

**Transition handling**: Transitions appear in **both** the DSA Subscriptions table (new DSA row, typed as the engagement type) AND the Account Transitions sub-section. In the subscription table, do NOT label transitions as "Renewal" — omit them from the subscription table entirely and only show them in Account Transitions.

**Tier classification** (from `subscription_hours_weekly`):
- `>= 32` → `Platinum (32h/wk)` = 1.0 FTE
- `>= 16` → `Gold (16h/wk)` = 0.5 FTE
- `< 16` → `Silver (Xh/wk)` = 0.25 FTE (show actual hours)

Sort by FTE descending, then account name.

### Net New FTE Calculation

**Only count incremental FTE** — the delta between the new subscription and any previous subscription for the same account+DSA.

For each new subscription:
- **New Logo**: net new = full current FTE (no prior subscription to offset)
- **Renewal, same tier**: net new = 0 (no change in capacity)
- **Renewal, tier upgrade**: net new = current FTE - previous FTE (e.g., Gold 0.5 → Platinum 1.0 = +0.5)
- **Renewal, tier downgrade**: net new = 0 (don't show negative)
- **Transition**: net new = new DSA FTE - prior DSA FTE at same account (may be 0 if same tier, positive if upgrade)

Total net new FTE goes in the Executive Snapshot `New Subscriptions This Month` row.

### Total Deployed Capacity

**Use `dsa_bandwidth_table` — NOT `dsa_project_assignment_outcomes`.** The bandwidth table is the authoritative source (same as the DSA Operations Dashboard). The outcomes table has overlapping subscription rows per account that inflate FTE totals when summed.

**Per-DSA FTE:**

```sql
SELECT
  dsa,
  CAST(regexp_extract(bandwidth_bar_html, 'font-weight:600;">([0-9.]+)<', 1) AS DOUBLE) AS total_fte,
  capacity_flag
FROM main.field_dsa.dsa_bandwidth_table
WHERE LOWER(dsa_manager) LIKE '%{manager_name}%'
ORDER BY total_fte DESC
```

**Active account count** — extract from `account_dsa_accounts_html` by counting entries with `ASSIGNMENT` status (green badges). Each `<span>` with `color:#137333` and text containing `ASSIGNMENT` is one active account.

**Compute totals:**
- `total_fte` = SUM of per-DSA FTE from the query above
- `dsa_count` = COUNT of rows from the query above
- `active_accounts` = COUNT of distinct ASSIGNMENT accounts across all DSAs

Use these actuals in the Executive Snapshot `Total Deployed Capacity` row.

### Pipeline Opportunities

Subscriptions in pipeline (not yet active). If none: "No pipeline opportunities this period."

### Investment DSAs

**Filter**: `dsa_engagement_type = 'Invested DSA'` (exact value — not 'Investment').

**Always show this section.** If no results, display: "No investment DSA engagements this period."

Table columns: Account | DSA | Status | Notes

### Account Transitions

Transitions are detected during subscription classification (see above). A **Transition** occurs when a new subscription this quarter is at an account that previously had a different DSA from this team, and the current DSA has no prior history at that account.

Detect by: for each new subscription classified as "Transition", the prior DSA is the most recent `HISTORICAL` or ending `CURRENT ASSIGNED` DSA at that account (different from the new DSA).

Table columns: Account | Previous DSA | New DSA | Effective (month year)

The effective date should be the **report month** (not the project start date, which may be earlier due to subscription timing).

If no transitions: "No account transitions this period."

### DSA Name Display

**Use names exactly as they appear in the data** (full legal names from `assignment_resource_user_name` and `dsa` columns). Do NOT use nicknames. The manager can edit names in the Google Doc phase if desired.

---

## Step 7: Build Output (Google Doc → HTML Email)

The output is a **two-phase workflow**: first a Google Doc for easy editing, then a rich HTML email for sending. This lets the manager add/remove rows, tweak narratives, and fix details in a familiar editor before producing the polished email.

### Phase 1: Google Doc (for editing)

The business update uses a **single master Google Doc per team** with each month as a separate section (page break + heading). This creates a running history navigable via the document outline sidebar.

#### Step 7a: Find or Create Master Doc

Search Google Drive for an existing master doc:

```bash
TOKEN=$(python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token)
curl -s "https://www.googleapis.com/drive/v3/files?q=name='DSA Business Update — {Vertical}'&mimeType='application/vnd.google-apps.document'&fields=files(id,name)" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

If found, use that `doc_id`. If not found, the first run will create it in Step 7b.

#### Step 7b: Write Markdown

**Load `resources/BUSINESS_OVERVIEW_TEMPLATE.md`** for the content structure.

Write the month's content as markdown to `/tmp/claude/dsa_business_update.md`.

**HEADING STRUCTURE** (important for document outline navigation):
- **H1** (`#`): Doc title — `DSA Business Update — {Vertical/Team}` (only for new docs)
- **H2** (`##`): Month heading — `{Month Year}  |  {Manager Name}, DSA Team Lead`
- **H3** (`###`): Section headings — Executive Snapshot, Use Cases Live, Top N, Risks, Subscription Activity

If appending to an existing doc, **omit the H1 title** — only include the H2 month heading and below.

**CONTENT SECTIONS** under the month heading:
1. **Personal intro**: 2-3 sentences, newsletter tone, reference key headline numbers (this month's live count + FY total)
2. **### Executive Snapshot**: Clean 2-column metrics table (5 rows, monthly focus)
3. **### Use Cases Live This Month**: Table (up to 5 by ARR) with intro sentence showing month count + FY-to-date
4. **### Top 5 Onboarding Use Cases — Going Live Q{X}**: Numbered bold items with narrative per UCO
5. **### Risks & Blockers**: Compact table — U5 only, Yellow/Red status only
6. **### {Month} Subscription Activity**: Sub-sections: DSA Subscriptions, Pipeline Opportunities, Investment DSAs, Account Transitions
7. **(Quarter-end only) ### Q{X} Summary**: Appended section with quarter totals when report month = Apr/Jul/Oct/Jan

### Required Sections & Empty-State Rules — MANDATORY

**Every monthly update MUST include ALL of the following sections and sub-sections, even when they have no data.** This keeps the report structure consistent month-over-month so readers always know where to find each category. Never drop a section because it's empty — use the prescribed empty-state text instead.

| # | Section | Empty-State Text |
|---|---------|-----------------|
| 1 | Personal intro | *(never empty — always write 2-3 sentences)* |
| 2 | Executive Snapshot | *(never empty — always has 5 metric rows)* |
| 3 | Use Cases Live This Month | "No use cases reached production in {Month}. FY-to-date: {N} live ({$X} ARR)." |
| 4 | Top 5 Onboarding Use Cases | "No DSA-attributed U5 onboarding use cases in pipeline." |
| 5 | Risks & Blockers | "No at-risk or red use cases this month." |
| 6a | DSA Subscriptions | "No new subscriptions in {Month}." If all Q1 activity was in prior months: "No new subscriptions in {Month}. All Q1 activity ({N} new + {M} renewals, +{X} FTE) was reported in the {Prior Month} update." |
| 6b | Pipeline Opportunities | "No pipeline opportunities this period." |
| 6c | Investment DSAs | "No investment DSA engagements this period." If former invested DSAs transitioned to paid, add: "{Names} were previously Invested DSAs — both have transitioned to Paid DSA assignments." |
| 6d | Account Transitions | "No new account transitions in {Month}." If transitions were reported in a prior month, add: "Transitions reported in the {Prior Month} update: {Account} ({Old DSA} → {New DSA})." |
| 7 | Capacity Snapshot | *(never empty — always shows full team table + available capacity + expiring soon)* |

**Validation checklist** — Before finalizing the Google Doc or HTML email, verify:
- [ ] All 7 top-level sections present (intro, snapshot, live, top 5, risks, subscription activity, capacity)
- [ ] All 4 subscription sub-sections present (DSA Subscriptions, Pipeline, Investment DSAs, Transitions)
- [ ] Empty sections use the exact empty-state text from the table above (not omitted)
- [ ] No data from prior months repeated (Step 6.0 deduplication applied)
- [ ] Executive Snapshot "New Subscriptions This Month" reflects only THIS month (not cumulative quarter)
- [ ] Capacity Snapshot reflects current state (always included regardless of deduplication)

#### Step 7c: Add to Google Doc

**First run (no existing doc):**
```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/claude/dsa_business_update.md \
  --title "DSA Business Update — {Vertical/Team}"
```

**Subsequent months (existing doc):**
Insert a page break at the end of the doc, then append the new month's content:

```bash
# 1. Insert page break at end of document
TOKEN=$(python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token)
# Get document length
DOC_LEN=$(curl -s "https://docs.googleapis.com/v1/documents/{doc_id}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['body']['content'][-1]['endIndex']-1)")
# Insert page break
curl -s -X POST "https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d "{\"requests\":[{\"insertPageBreak\":{\"location\":{\"index\":$DOC_LEN}}}]}"

# 2. Append new month's content
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/claude/dsa_business_update.md \
  --doc-id "{doc_id}"
```

Save the `doc_id` for Phase 2.

#### Step 7d: Present for Editing

Tell the user:
- Here is the Google Doc — the new month's section has been added
- Use the **document outline** (View → Show outline) to navigate between months
- Edit tables, narratives, statuses freely — add/remove rows, fix details
- **When done, say "create the email" or "ready to send"**

### Phase 2: HTML Email (for sending)

**Triggered when the user says** "create the email", "send it", "convert to email", "ready to send", or similar.

#### Step 7e: Read the Edited Google Doc

Read the Google Doc content using the Google Docs API. **Read only the current month's section** — find the H2 heading matching `{Month Year}` and extract everything until the next H2 or end of document.

The user may have:
- Added or removed table rows
- Changed narratives or status text
- Reordered items
- Fixed names, ARR amounts, or dates

Extract the edited content by section (Business Snapshot, Live UCOs, Top N, Risks, Subscription Activity).

#### Step 7f: Generate Styled HTML

**Load `resources/EMAIL_TEMPLATE.html`** for the exact HTML structure, inline CSS patterns, and color palette.

Convert the edited Google Doc content into a rich HTML email body. Write to `/tmp/claude/dsa_business_update.html`.

**HTML STYLING RULES** (all inline CSS — Gmail strips `<style>` blocks):

**Layout elements:**
- Title: `<h1 style="font-size:22px;color:rgb(26,26,26);font-family:Arial,sans-serif">`
- Intro callout: `<div style="background:rgb(250,250,250);border-left:4px solid rgb(231,76,60);padding:14px 18px;margin:20px 0px;font-size:14px;color:rgb(51,51,51)">`
- Section headers: `<h2 style="font-size:17px;color:rgb(44,62,80);border-bottom:2px solid rgb(231,76,60);padding-bottom:6px;margin-top:32px;font-family:Arial,sans-serif">`
- Section dividers: `<hr style="border-top-style:solid;border-top-color:rgb(224,224,224);margin:28px 0px">`
- Section notes: `<p style="font-style:italic;color:rgb(102,102,102);font-size:13px;margin-bottom:12px">`
- Sub-headings: `<div style="font-size:14px;color:rgb(44,62,80);margin:20px 0px 8px"><strong>...</strong></div>`

**Table styling:**
- Table: `style="width:780px;border-collapse:collapse;margin:14px 0px 20px;font-size:13px"`
- Header cells: `style="background:rgb(44,62,80);color:rgb(255,255,255);text-align:left;padding:8px 10px;font-size:12px;text-transform:uppercase;letter-spacing:0.3px"`
- Data cells: `style="padding:8px 10px;border-bottom:1px solid rgb(233,236,239)"`
- Alternating rows: add `style="background:rgb(248,249,250)"` on odd `<tr>` elements

**Top N cards** (NOT a table — use `<div>` cards):
- Normal card: `<div style="background:rgb(248,249,250);border-left:4px solid rgb(52,152,219);padding:12px 16px;margin:10px 0px;border-radius:0px 4px 4px 0px;font-size:14px">`
- At Risk / Red card: same but `border-left:4px solid rgb(231,76,60)`
- Card title: `<p style="font-weight:700;margin:0px 0px 4px">`
- Card meta: `<p style="font-size:12px;color:rgb(102,102,102);margin:0px 0px 6px">` with `<span style="margin-right:12px">` for each field
- Card body: `<p style="font-size:13px;color:rgb(68,68,68);margin:0px">`

**Status color map** (inline CSS on `<span>` elements):
- On Track: `color:rgb(39,174,96);font-weight:600`
- At Risk / Yellow: `color:rgb(243,156,18);font-weight:600`
- Red: `color:rgb(231,76,60);font-weight:600`
- Not Set: `color:rgb(149,165,166);font-weight:600`
- Active (Investment DSAs): `color:rgb(39,174,96);font-weight:600`

**Card border color rules:**
- At Risk or Red status → red left border `rgb(231,76,60)`
- All other statuses → blue left border `rgb(52,152,219)`

#### Step 7g: Create Gmail Draft

```bash
cd ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail
HTML_BODY=$(cat /tmp/claude/dsa_business_update.html)
python3 resources/gmail_builder.py create-draft \
  --to "{recipient_emails}" \
  --subject "DSA {Vertical} Business Update - {Month} {Year}" \
  --html "$HTML_BODY"
```

Ask the manager who the recipients (To) and CC should be. If unknown, create the draft with the manager's own email as To.

#### Step 7h: Confirm

Tell the user:
- A Gmail draft has been created with the polished HTML formatting
- They can find it in their Gmail Drafts folder
- Review once more and hit Send

---

## Domain Rules

### Tier Classification
- **Platinum**: >= 32 hours/week = 1.0 FTE
- **Gold**: >= 16 hours/week = 0.5 FTE
- **Silver**: < 16 hours/week = 0.25 FTE

### Databricks Fiscal Year
- FY starts **February 1**
- Q1: Feb – Apr, Q2: May – Jul, Q3: Aug – Oct, Q4: Nov – Jan
- FY designation: FY27 runs Feb 2026 – Jan 2027

### ARR Calculation
- `ARR = estimated_quarterly_dollar_dbus * 4` (column is already in dollar terms)

### Health Status Mapping (Source → Display)
| Source Value | Display | Email Color |
|---|---|---|
| `Green` | On Track | `rgb(39,174,96)` |
| `Yellow` | At Risk | `rgb(243,156,18)` |
| `Red` | Red | `rgb(231,76,60)` |
| `NULL` | Not Set | `rgb(149,165,166)` |

### Investment DSA Identification
- Filter: `dsa_engagement_type = 'Invested DSA'` (exact string match)
- NOT 'Investment' — the actual column value is 'Invested DSA'

### UCO Stage Names
| Stage | Name |
|-------|------|
| 1 | U1 - Validating |
| 2 | U2 - Scoping |
| 3 | U3 - Evaluating |
| 4 | U4 - Confirming |
| 5 | U5 - Onboarding |
| 6 | U6 - Live |

---

## Error Handling

| Issue | Resolution |
|-------|------------|
| No team members found | Ask user for manager name or DSA list |
| Logfood timeout | Retry once after 30s. If still fails, report partial results |
| No UCO data | Report empty pipeline — may indicate data lag |
| Google auth expired | Run `/google-auth` |
| No bandwidth data | Skip capacity metrics, note in doc |
| Partial data | Generate doc with available data, note missing sections |

---

## Common Pitfalls

### Pitfall #1: Querying DSAs One at a Time
**Problem**: N+1 query pattern — one query per DSA is slow
**Solution**: Always use `IN` clauses to query all DSAs in a single statement

### Pitfall #2: Wrong FY Calendar
**Problem**: Using calendar year instead of Databricks FY (starts Feb 1)
**Solution**: FY start = February 1. Current quarter = compute from current month

### Pitfall #3: Mixing Up ARR vs Quarterly DBUs
**Problem**: Reporting `estimated_quarterly_dbus` as ARR
**Solution**: ARR = estimated_quarterly_dbus * 4

### Pitfall #4: Table Format for Top N Section
**Problem**: Using a table for the Top N onboarding section
**Solution**: Use numbered list with narrative per UCO — this is a newsletter, not a spreadsheet

### Pitfall #5: Missing Personal Intro
**Problem**: Starting directly with the Executive Snapshot
**Solution**: Always include a 2-3 sentence personal greeting and context paragraph

### Pitfall #6: Using "Live This FY" Instead of "Live This Month"
**Problem**: Showing all U6 UCOs since FY start (179 UCOs!) instead of just this month's new live UCOs
**Solution**: Filter `target_live_date >= month_start AND target_live_date < month_end`. Show FY-to-date totals in the description text only.

### Pitfall #7: DSA Nickname Mismatch
**Problem**: Using nicknames (Muju, Ray) that don't match data column values (Mujahid Ali Mohammed, Raymond Rosalez)
**Solution**: Always use names exactly as they appear in the `dsa` or `assignment_resource_user_name` columns. Names are consistent across pipeline, assignment, and roster tables.

### Pitfall #8: Wrong Investment DSA Filter
**Problem**: Filtering `dsa_engagement_type LIKE '%Investment%'` — returns no results
**Solution**: The exact value is `'Invested DSA'` (not "Investment"). Use exact match: `dsa_engagement_type = 'Invested DSA'`

### Pitfall #9: Using estimated_quarterly_dbus Instead of estimated_quarterly_dollar_dbus
**Problem**: Column name confusion — `estimated_quarterly_dbus` (raw DBUs) vs `estimated_quarterly_dollar_dbus` (dollar amount)
**Solution**: Always use `estimated_quarterly_dollar_dbus * 4` for ARR. This column is already in dollar terms.

### Pitfall #10: Snapshot Comparison for Live Detection
**Problem**: Trying to compare monthly snapshots in `rpt_use_case_pipeline_monthly` — the table only has future projections, no historical state
**Solution**: Use `target_live_date` to determine when UCOs went live. The field uses clean first-of-month values (e.g., 2026-02-01).

### Pitfall #11: Account-Level vs UCO-Level DSA Attribution
**Problem**: The `dsa` column on `rpt_use_case_pipeline_monthly` is the **account-level** DSA, not the UCO-level DSA. Filtering `p.dsa IN (team_names)` misattributes use cases in multi-DSA accounts (e.g., State Street DMC showed Mujahid as pipeline DSA but the actual UCO-level DSA was Mohan Matthews). Falling back to account-level DSA inflates pipeline numbers with UCOs not truly owned by the team.
**Solution**: Join to `main.sfdc_bronze.usecase__c` (on `usecase_id`) and resolve `DSA__c` via `main.sfdc_bronze.user` to get the UCO-level DSA. **Only include UCOs where `usr.Name IN (team_names)`.** Do NOT fall back to `p.dsa` (account-level). Accept that metrics will be smaller but more accurate. See the CTE pattern in Step 2 Agent 1.

### Pitfall #12: Manager Name Format Mismatch
**Problem**: Using short name (e.g., "Amit Jha") when the roster stores full legal name ("Amit Kumar Jha")
**Solution**: Use `LOWER(dsa_manager) LIKE '%{partial_name}%'` for the roster lookup, then use the exact full name from the results for all subsequent queries.

### Pitfall #13: Double-Counting FTE from dsa_project_assignment_outcomes
**Problem**: Summing `fte_req_current` from `dsa_project_assignment_outcomes` produces an inflated FTE total (e.g., 11.0 when actual is 9.0). This happens because the table has **multiple overlapping subscription rows per DSA-account pair** (e.g., MetLife has 3 active rows at 0.25 FTE each = 0.75, but the actual deployed FTE is 0.5).
**Solution**: Use `main.field_dsa.dsa_bandwidth_table` for Total Deployed Capacity. This is the same table the DSA Operations Dashboard uses. It correctly de-duplicates and aggregates FTE per DSA. Extract FTE from `bandwidth_bar_html` via regex: `regexp_extract(bandwidth_bar_html, 'font-weight:600;">([0-9.]+)<', 1)`. Use `dsa_project_assignment_outcomes` only for subscription detail (tier, type, dates) — never for FTE totals.

### Pitfall #14: Dropping Empty Sections
**Problem**: When a section has no data (e.g., no new subscriptions, no investment DSAs, no transitions), the section is omitted entirely from the output. This breaks report consistency — readers expect the same structure every month and may think data is missing rather than empty.
**Solution**: **Never drop a section.** Always include all 7 top-level sections and all 4 subscription sub-sections. Use the prescribed empty-state text from the "Required Sections & Empty-State Rules" table (e.g., "No pipeline opportunities this period."). This was caught when the March 2026 report omitted Pipeline Opportunities, Investment DSAs, and Account Transitions because they were empty.

### Pitfall #15: Repeating Prior Month's Subscription Activity
**Problem**: The Logfood query returns all subscriptions starting this fiscal quarter, but some were already reported in a prior month's email. Including them again makes the update look like a copy-paste of last month.
**Solution**: Before compiling subscription activity, **read the prior month's email** (Step 6.0) and exclude any subscriptions, transitions, or new logos that were already reported. The Executive Snapshot "New Subscriptions This Month" row must reflect only THIS month's activity. If nothing is new, say "None — all Q1 activity reported in {Prior Month}."

### Pitfall #16: Hardcoding Team DSA Names
**Problem**: Using a hardcoded list of DSA names from a previous run. Team composition changes (new hires, departures, name corrections).
**Solution**: Always start by querying `main.field_dsa.dsa_roster_curr WHERE LOWER(dsa_manager) LIKE '%{manager_name}%'` to get the current team roster. Use the `dsa` column values exactly as returned — do not guess or abbreviate names.

---

## Related Skills

- `/dsa-capacity-planning` — Detailed FTE allocation analysis
- `/dsa-assignment-sync` — Validate assignments against Salesforce UCO coverage
- `/salesforce-actions` — Salesforce query patterns
- `/logfood-querier` — Logfood query patterns
- `/google-docs` — Google Doc creation (editing phase)
- `/gmail` — Gmail draft creation (sending phase)

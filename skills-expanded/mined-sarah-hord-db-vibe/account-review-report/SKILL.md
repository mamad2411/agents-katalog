---
name: account-review-report
description: Generate comprehensive  account review reports with consumption trends, use case progress, risk analysis, active users, blockers, and Salesforce hygiene. Creates markdown/PDF/Google Doc output with optional Slack/email distribution. Use when asked to create account review, prepare  review, generate account report, or prepare for 1-on-1 with IC.
---

# Account Review Report Generator

Generate comprehensive  account review reports for specific accounts. This report forms the basis for reviews or one-on-one meetings with ICs, covering consumption, use cases, risks, blockers, and data hygiene.

## Dependencies

This skill requires the following plugins to be installed:

- **fe-salesforce-tools** (required) — Salesforce authentication and data access
- **fe-internal-tools** (required) — Logfood queries and internal terminology
- **fe-google-tools** (optional) — Google Doc output and email distribution
- **fe-specialized-agents** (optional, for PDF output) — Markdown-to-PDF converter with Databricks branding

Install with:
```bash
claude plugin install fe-salesforce-tools@fe-vibe fe-internal-tools@fe-vibe fe-google-tools@fe-vibe
```

## Prerequisites

Before running this skill, ensure authentication:

1. **Salesforce** -- Run `/salesforce-authentication`
2. **Logfood** -- Run `databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood`
3. **Google Workspace** (optional, for Google Doc output or email distribution) -- Run `/google-authentication`

## Required Inputs

The skill will prompt for:

1. **Account Name** -- The Salesforce account to analyze (e.g., "Acme Corp")
2. **Lookback Period** -- For Period-over-Period (PoP) changes: `7_days`, `14_days`, `28_days`, `91_days`, or `FQ_Start` (Fiscal Quarter start)
3. **Output Format** -- Markdown (default), PDF (via weasyprint), or Google Doc

Optional (prompted after report generation):
- **Google Drive Folder** -- Target folder ID for Google Doc (if applicable)
- **Additional Format** -- Convert to a second format after initial output
- **Distribution** -- Slack channel/DM or email recipients

---

## Report Structure

The report consists of six sections. No plots or charts in v1 -- all data is presented as narrative text and tables.

### 1. Executive Summary
- **3-4 concise paragraphs** (each ~6 lines max on A4) synthesizing the account's current state, key trends, and critical actions
- **Paragraph 1:** Consumption headline (direction, % change, dollar amounts) and active user engagement headline (DAU/WAU/MAU trends, QoQ comparison). Mention data freshness
- **Paragraph 2:** Pipeline PoP changes -- net $ impact, count of changes, key inflows/outflows by name. Use case stage progressions -- count of advancements, notable launches or stage moves with $ values
- **Paragraph 3:** Risk status (Red/Yellow flag count and $ at risk, grouped by category). Blocker summary (count of blockers, count of affected use cases, total $ at risk, name the highest-impact blocker). Hygiene summary (count of flagged use cases, worst offender by days-in-stage)
### 2. Consumption Trends
- **Opening narrative (2-3 short paragraphs)** describing total consumption across three rolling intervals (7d, 28d, 90d), whether short-term momentum aligns with longer-term trends, and which workspaces drove growth or decline
- **Consumption table** with columns: Workspace Name, Interval, Current Period ($), Prior Period ($), Change ($), Change (%). Rows grouped by entity — "Total Account" first (7d/28d/90d), then top 5 workspaces each with three interval rows
- **Data freshness note:** "Latest consumption data available: [date] ([N] days old)"
- **Source:** Logfood `main.gtm_gold.workspace_sku_consumption_daily`

### 3. Use Case Updates
Combined section covering pipeline changes, stage progressions, and risk flags. Opens with **2-3 short summary paragraphs** highlighting the most critical aspects: net pipeline $ movement, most notable stage progressions, and any Red/Yellow flags requiring immediate action.

#### 3a. PoP Changes
- **Count header:** "N changes detected affecting [quarters] compared to [period] ago:"
- **Bullet list** of each change: use case name as Salesforce link with owner initials in brackets, fiscal quarter in parentheses, "Inflow/Outflow of $X due to [reason]" (reasons: pushed out, went live, lost, progressing into pipeline, shrunk, etc.)
- **"Net Impact:"** closing narrative paragraph summarizing net pipeline $ change across affected quarters and primary drivers
- **Source:** Logfood `main.sfdc_bronze.usecase__c` (current + historical processDate snapshots)

#### 3b. Use Case Progression
- **"Key Highlights"** opening line: count of advancing use cases, combined $ in quarterly DBUs, as-of date
- **Grouped by stage movement type** with bold sub-headers (e.g., "Recent Production Launch (U6):", "N Use Cases Moved to Evaluating (U3):")
- **Each use case:** name as Salesforce link with owner initials, $/quarter, implementation status color, narrative description of current state and next steps
- **"Most Significant Pipeline Movement:"** callout highlighting the highest-value progression
- **Source:** Logfood `main.sfdc_bronze.usecase__c` (U-stage date fields within last 14 days)

#### 3c. Risks
- **"Critical Red-Flagged Use Cases"** subsection (or "No Red-flagged use cases found" if none)
- **"Key Yellow-Flagged Risks by Category"** subsection, grouped by risk type:
  - **Customer Engagement Issues** -- heading with account name and total $ at risk
  - **Product/Feature Gaps** -- heading with account name and total $ at risk
  - **Other** -- heading with account name and total $ at risk
- **Each use case:** name as Salesforce link, stage in parentheses, $/quarter, description of the issue
- **"Remediation:"** sub-line per use case with specific actionable steps, suggested owner, and timeline
- **Source:** Logfood `main.sfdc_bronze.usecase__c` (latest processDate, `implementation_status` Yellow/Red)

### 4. Active User Trends
- **Title includes current FQ:** "Active User Trends - [FQ] (Current Quarter)"
- **Opening narrative (2-3 short paragraphs)** summarizing the key engagement trend (e.g., "demonstrates strong user engagement growth" or "mixed user engagement trends") with current DAU, WAU, MAU counts
- **"Current Quarter Performance"** subsection: QAU count, comparison to prior quarter with absolute change and %, narrative
- **"Growth Trends"** subsection: bullet list of DAU, WAU, MAU each showing: user count, +/- change in users, % change, directional arrow
- **Anomaly detection:** Flag conflicting signals (e.g., DAU up 121% but MAU down 22%) with a note recommending data validation
- **Source:** Logfood `main.gtm_gold.account_active_users_quarterly`

### 5. Blockers Overview
- **Opening narrative (2-3 short paragraphs):** "N use cases in stages U2-U5 are currently blocked, representing $X in quarterly DBU consumption at risk." Name the highest-impact blocker and note compounding risks
- **"All Blockers by Aha Feature"** heading, organized by descending number of blocked use cases
- **Each blocker:** bold name with Aha ID in parentheses, status, "Blocking N use cases:"
- **Sub-bullets:** affected use case names as Salesforce links with stage in parentheses
- **"Key Observations:"** closing paragraph identifying cross-blocker patterns (e.g., multiple blockers hitting the same use case) and recommendations for product engagement
- **Source:** Logfood `main.sfdc_bronze.blocker__c` joined with use cases

### 6. Hygiene
- **Opening narrative (2-3 short paragraphs)** stating total flagged use cases, breaking down by issue type, and highlighting worst offenders
- **Table** with columns: Use Case | Stale Update (>10d) | Stuck in U2 (>60d) | Stuck in U3/U4 (>90d) | On-boarding in past | Go-Live in past | Onboarding Plan Incomplete. The Use Case column includes stage and estimated quarterly DBUs in parentheses (e.g., "Use Case Name (Scoping, $15,000)"). Use flag indicators for boolean columns; for the last column show the missing section names instead of a flag
- **Source:** Logfood `main.sfdc_bronze.usecase__c`

---

## Execution Steps

### Step 0: Load Related Skills

**Proactively load skills into context** before querying:

```
/salesforce-actions
/logfood-querier
/internal-jargon
```

This ensures correct Salesforce schemas, Logfood table references, and internal terminology handling.

### Step 0.5: Pre-flight Validation

**Before proceeding, verify all required dependencies are accessible and authenticated.**

Run these checks sequentially. If any **required** check fails, stop execution and present remediation instructions to the user.

#### 1. Check Required Plugin Access

Verify the skills from Step 0 loaded successfully:

- If `/salesforce-actions` failed to load → Instruct user to install `fe-salesforce-tools` plugin
- If `/logfood-querier` failed to load → Instruct user to install `fe-internal-tools` plugin

#### 2. Check Salesforce Authentication

Run a lightweight probe query to verify SF CLI is authenticated:

```bash
sf data query --target-org "$SF_TARGET_ORG" --query "SELECT Id FROM Account LIMIT 1" --json
```

**If this fails:**
- Instruct user to run `/salesforce-authentication` skill to authenticate

#### 3. Check Logfood Authentication

Test the Databricks CLI profile for Logfood access:

```bash
databricks auth token --profile=logfood 2>/dev/null
```

**If this fails:**
- Instruct user to run: `databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood`

#### 4. Check Optional Google Workspace (Conditional)

**Only run this check if** `OUTPUT_FORMAT` is `google_doc` or if distribution includes email addresses.

Test gcloud CLI authentication:

```bash
gcloud auth print-access-token 2>/dev/null
```

**If this fails:**
- Warn the user that Google Workspace features will be unavailable
- Suggest running `/google-auth` if they need Google Doc output
- **Do NOT block execution** — allow the skill to proceed with markdown/PDF output only

**After all required checks pass, proceed to Step 1.**

### Step 1: Resolve Account and Lookback Period

**1A: Resolve Account (Fuzzy Match → Ultimate Parent)**

Search Salesforce for accounts matching the user's input. Always retrieve multiple candidates and include parent account info for hierarchy resolution:

```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Id, Name, ParentId, Parent.Name FROM Account \
   WHERE Name LIKE '%<ACCOUNT_NAME>%' LIMIT 10" --json
```

**Match handling:**

- **Zero results:** Try alternative spellings, abbreviations, or shorter substrings (e.g., "Deutsche Bahn" → "Deutsche", "DB"). Ask the user to clarify if still no match.
- **Exactly one result:** Present the match to the user and ask for confirmation before proceeding.
- **Multiple results:** Present all matches as a numbered list (showing Name and Parent.Name) and ask the user to pick the correct one.

**1B: Traverse to Ultimate Parent Account**

Once the user confirms an account, check whether it has a `ParentId`. If it does, walk up the hierarchy until you reach the top-level account (where `ParentId IS NULL`):

```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Id, Name, ParentId, Parent.Name FROM Account \
   WHERE Id = '<PARENT_ID>'" --json
```

Repeat until `ParentId` is null. The account with no parent is the **ultimate parent**.

Store the ultimate parent as `ACCOUNT_ID` and `ACCOUNT_NAME`. Inform the user which account is being used:

> "Found **[matched account]** — resolving to ultimate parent account **[ACCOUNT_NAME]** (ID: [ACCOUNT_ID]). All report sections will use this account."

If the matched account has no parent (it is already the ultimate parent), skip the traversal and proceed.

**IMPORTANT:** All subsequent queries in this report MUST use the ultimate parent `ACCOUNT_ID`. This ensures consumption, use cases, blockers, and hygiene data are aggregated at the correct organizational level.

**1C: Convert Lookback Period to Date Range**

Ask the user to provide a look back period, which can be one of the following options: 7, 14, 28, or 91 days, or Fiscal Quarter start.

The user's answer should be one of: `7_days`, `14_days`, `28_days`, `91_days`, or `FQ_Start`. Use the resolved value as the `{PERIOD}` parameter directly in queries—no need to convert to date ranges here.

**1D: Select Output Format**

Ask the user which output format they want for the report:
- **Markdown** (default) -- saved to `/tmp/`
- **PDF** -- Databricks-branded PDF via weasyprint
- **Google Doc** -- created in Google Drive (requires `/google-authentication`)

If the user has already specified the format in their initial prompt, confirm and proceed. Otherwise, explicitly ask. If the user does not have a preference, default to Markdown.

Store the choice as `OUTPUT_FORMAT` (one of `markdown`, `pdf`, `google_doc`).

---

### Step 2: Parallel Data Collection

Execute these queries in parallel using the `field-data-analyst` subagent or by running multiple Logfood queries concurrently.

**2A: Consumption Trends**

Query: `resources/consumption_trends.sql`

**Parameters:** `ACCOUNT_ID`

**Returns:** Rows for three rolling intervals (7d, 28d, 90d), each containing a "Total Account" summary row plus the top 5 workspaces by current consumption:
- `Interval` — window label (`7d`, `28d`, `90d`)
- `Workspace Name` — workspace name or `Total Account` for the account-level aggregate
- `Current Period Consumption ($)` — DBU dollar spend in the current window
- `Prior Period Consumption ($)` — DBU dollar spend in the preceding window of equal length
- `Change ($)` — absolute difference (current minus prior)
- `Change (%)` — percentage change with directional arrow (`↑` / `↓`)
- `Data As Of` — most recent usage date in the dataset

**2B: Use Case PoP Changes**

Query: `resources/usecase_pop_changes.sql`

**Parameters:** `ACCOUNT_ID`, `PERIOD` (one of `1_days`, `7_days`, `14_days`, `28_days`, `91_days`, `FQ Start`)

**Returns:** Use cases with changes in the selected period, filtered to current and next fiscal quarter target-live dates. Only rows where a change occurred (no-change rows excluded).
- `usecase_id`, `usecase_name`, `usecase_link` (pre-built markdown hyperlink — use verbatim in report output), `account_name`
- `target_live_fiscal_year_quarter`, `target_live_fiscal_quarter_start_date`
- `period`, `change_type_label` (e.g. `outflow: went live`, `outflow: lost`), `change_amount`
- `stage_name_ui_latest` vs `stage_name_ui_prior` (e.g. Live ← Onboarding, Lost ← Evaluating)
- `estimated_quarterly_dollar_dbus_latest` vs `estimated_quarterly_dollar_dbus_prior`
- `target_live_date_latest` vs `target_live_date_prior`

**2C: Stage progression during the last 14 days**

Query: `resources/use_case_progress.sql`

**Parameters:** `ACCOUNT_ID`

**Returns:** Use cases where any U-stage date (U1–U6) falls within the last 14 days, with AI-extracted status updates from the free-text `demand_plan_next_steps` field. Ordered by most recent stage change descending.
- `usecase_name`, `usecase_id`, `usecase_link` (pre-built markdown hyperlink — use verbatim in report output), `account_name`
- `stage`, `stage_name_ui` (e.g. Scoping, Evaluating, Confirming, Live)
- `estimated_quarterly_dollar_dbus`, `target_live_date`
- `stage_change` — highest U-stage reached in the 14-day window (e.g. `Moved to U4`)
- `most_recent_stage_change_date` — date of the most recent U-stage transition
- `status_update` — formatted summary combining AI-extracted fields: latest update date, update text, implementation plan agreed (Yes/No/NA), blockers & risks
- `implementation_status` (Green, Yellow, Red)

**2D: Use Cases with Risk Flags**

Query: `resources/usecase_risks.sql`

**Parameters:** `ACCOUNT_ID`

**Returns:** Use cases in stages U1–U5 with `implementation_status` of `Yellow` or `Red` that have non-empty `demand_plan_next_steps`. Each row includes an AI-extracted plain-text summary of blockers and risks (rows where the AI returns "NA" are excluded).
- `usecase_id`, `usecase_name`, `usecase_link` (pre-built markdown hyperlink — use verbatim in report output), `current_stage` (e.g. U3, U5)
- `implementation_status` (Yellow or Red)
- `estimated_quarterly_dollar_dbus`
- `blockers_and_risks` — AI-generated concise paragraph (3–4 sentences) describing blockers, risks, and impediments extracted from the free-text next-steps field

**2E: Active User Trends**

Query: `resources/active_user_trends.sql` (active users section)

**Parameters:** `ACCOUNT_ID`

**Returns:** A single aggregated row for the most recent fiscal quarter, showing active user counts at three cadences (weekly, monthly, quarterly) with period-over-period comparisons.
- `parent_account_name`, `fiscal_quarter_start_date`, `fiscal_year_quarter`
- `wau_t7d`, `wau_t7d_prior_period`, `wau_t7d_change`, `wau_t7d_change_pct` — weekly active users (7-day window) with delta and % change
- `mau_t28d`, `mau_t28d_prior_period`, `mau_t28d_change`, `mau_t28d_change_pct` — monthly active users (28-day window)
- `qau_t91d`, `qau_t91d_prior_period`, `qau_t91d_change`, `qau_t91d_change_pct` — quarterly active users (91-day window)

**2F: Blockers Overview**

Query: `resources/blockers_overview.sql`

**Parameters:** `ACCOUNT_ID`

**Returns:** Blockers linked to U2–U5 use cases, grouped by Aha idea, ordered by number of blocked use cases and consumption impact descending.
- `blocker_name` — Aha idea name (or "No Aha Name" if unlinked)
- `aha_link` — Salesforce link to the Aha idea (or "No Link")
- `num_blocked_usecases` — count of distinct use cases affected
- `total_blocked_quarterly_dbus` — sum of estimated quarterly dollar DBUs across blocked use cases
- `blocked_usecase_names` — array of affected use case names
- `blocked_usecase_ids` — array of corresponding Salesforce use case IDs
- `blocked_usecase_links` — array of pre-built markdown hyperlinks for each blocked use case (use these verbatim in report output instead of constructing links manually)

**2G: Salesforce Hygiene Issues**

Query: `resources/salesforce_hygiene.sql`

**Parameters:** `ACCOUNT_ID`

**Returns:** Use cases in stages U2–U5 that trigger at least one hygiene flag. For U4/U5 use cases, includes AI-assessed implementation plan completeness (checks for Objective, Delivery Model, Milestones & Timeline, Risks & Mitigation).
- `account_name`, `usecase_name`, `usecase_id`, `usecase_link` (pre-built markdown hyperlink — use verbatim in report output), `stage`, `stage_name_ui`
- `days_in_stage`, `target_onboarding_date`, `target_live_date`
- `estimated_quarterly_dollar_dbus`, `account_executive`
- `last_update_date`, `days_since_update`
- `Stale Update (>10d)` — boolean, true if `custom_last_modified_date` is more than 10 days ago
- `Stuck in U2 (>60d)` — boolean, true if U2 for more than 60 days
- `Stuck in U3/U4 (>90d)` — boolean, true if U3 or U4 for more than 90 days
- `Overdue Onboarding` — boolean, true if `target_onboarding_date` is past and use case not yet in U5+
- `Overdue Go-Live (>30d)` — boolean, true if `target_live_date` is more than 30 days past and not yet U6/Lost
- `Incomplete Implementation Plan` — boolean, true if AI finds missing sections in `implementation_notes` (U4/U5 only)
- `Missing Onboarding Plan Sections` — comma-separated list of missing sections (e.g. "Milestones & Timeline, Risks & Mitigation") or null if complete

---

### Step 3: Analysis and Synthesis

**3A: Executive Summary Generation**

Based on data from Steps 2A-2G, synthesize 3-4 concise paragraphs (each ~6 lines max on A4 / ~100 words). Split any content area into two paragraphs if it would otherwise exceed the limit:

- **Paragraph 1:** Consumption headline (direction, % change, dollar amounts) and active user engagement headline (DAU/WAU/MAU trends with QoQ comparison). Mention data freshness
- **Paragraph 2:** Pipeline PoP changes (net $ impact, count of changes, key inflows/outflows by name). Use case stage progressions (count of advancements, notable launches or stage moves with $ values)
- **Paragraph 3:** Risk status (Red/Yellow flag count and $ at risk by category). Blocker summary (count, affected use cases, total $ at risk, name highest-impact blocker). Hygiene summary (flagged use case count, worst offender)
**3B: Risk Deep Dive**

For each use case in Section 3c (risks), read the AI-extracted `blockers_and_risks` field and extract:

- **Root cause:** Why is this use case at risk? (Look for: "waiting for", "delayed", "no resources", "champion left", "budget freeze", "C-Level approval needed")
- **Risk category:** Classify as Customer Engagement Issues, Product/Feature Gaps, or Other
- **Remediation:** What specific action can be taken? (Provide AE, SA, customer action with owner and timeline)

**3C: Blocker Impact Prioritization**

Sort blockers by total consumption impact (sum of blocked use cases' quarterly DBU $) descending. Highlight the top 3 blockers.

---

### Step 4: Generate Report Output

**4A: Create Markdown Report**

Build the markdown report following the section-by-section formatting instructions below. No plots or charts in v1 -- present all data as narrative text and tables.

**Formatting conventions used throughout:**
- Paragraph brevity: Every narrative paragraph in the report must be **no longer than ~6 printed lines on an A4 page** (~100 words). If a paragraph exceeds this, split it into two shorter paragraphs. Prefer short, punchy paragraphs that each make a single point -- this improves scannability in both digital and printed formats
- Dollar values: `$` prefix with comma separators (e.g., `$136,029`)
- Percentage changes: include directional arrows (`↑` for positive, `↓` for negative)
- Use case names: **ALWAYS use the `usecase_link` column from query results verbatim.** Each query returns a pre-built markdown hyperlink (e.g., `[SuccessFactors Data Product](https://databricks.lightning.force.com/lightning/r/UseCase__c/a1B8W00000JkLmNOP/view)`). Prepend owner initials in brackets before the link (e.g., `[AM] {usecase_link}`). For the blockers query, use the `blocked_usecase_links` array entries directly. **NEVER construct Salesforce URLs manually or fabricate record IDs.** This applies to all output formats -- markdown, PDF, and Google Doc
- Implementation status: Green/Yellow/Red throughout

---

#### Report Header

```markdown
# [ACCOUNT_NAME] - Account Progress Report
Date: [CURRENT_DATE] Period: Last [LOOKBACK_PERIOD] Data Source: [GENIE_SPACE_NAME]
```

---

#### Section 1: Executive Summary

Write 3-4 concise paragraphs (each **no longer than ~6 lines on A4 / ~100 words**) followed by a "Recommended Actions" list. The three content areas below map to at least one paragraph each, but split any area into two paragraphs if needed to stay within the brevity limit:

**Bold formatting for key insights:** Within each paragraph, wrap the most important figures, verdicts, and risk callouts in `**bold**` so readers can scan the summary without reading every sentence. Bold the overall account assessment, headline metrics and their directional changes, dollar amounts at risk, and any critical action triggers. Example: "SAP SE demonstrates **stable account performance** with **28-day consumption up 3.2% (+$4,197)**..." / "**4 use cases are blocked**, representing **$405K in quarterly DBUs at risk**".

**Paragraph 1 -- Consumption and User Engagement:**
State the account name and **bold the overall assessment** (e.g., "demonstrates **stable account performance**" or "shows **mixed signals**"). Reference consumption trends across the three intervals — lead with the 28-day change as the primary signal, but note whether 7-day and 90-day trends confirm or contradict it. Bold the headline percentage changes and dollar amounts (e.g., "**28-day consumption grew 3.2% (+$4,197)**, consistent with the 90-day upward trend of 4.5%, while 7-day momentum is flat at +0.3%"). If adding active user trends would push the paragraph beyond ~6 lines, start a new paragraph for user engagement. Summarize active user trends with specific metrics, bolding divergent or notable signals (e.g., "daily and weekly users grew 9.7% and 11.8% respectively, but **quarterly active users declined 1.9% QoQ**"). Mention data freshness.

**Paragraph 2 -- Pipeline and Use Case Movement:**
Summarize PoP changes: **bold the net $ impact and direction** (e.g., "**net pipeline decrease of -$45K**"). Name specific use cases using their `usecase_link` from query results with $ amounts and change reasons (e.g., "{usecase_link} lost ($60K)", "{usecase_link} progressing into pipe ($15K)"). Then cover stage progressions: bold the count of advancing use cases and any notable launches with $ values (e.g., "**3 use cases advanced** this period, including **{usecase_link} launching into production ($72K)**"). Split into two paragraphs (PoP changes / stage progressions) if the combined text exceeds ~6 lines.

**Paragraph 3 -- Risks, Blockers, and Hygiene:**
**Bold the Red/Yellow flag counts and total $ at risk** (e.g., "**2 Red-flagged use cases totaling $134K at risk**") or bold the absence of risk (e.g., "**No Red-flagged use cases were identified**"). Summarize blocker exposure: bold the headline blocker stat (e.g., "**4 use cases blocked by 3 unique Aha features, $405K at risk**") and name the highest-impact blocker with its specifics. Briefly note hygiene: bold the worst offender (e.g., "**[Use Case Name] has been stuck in U2 for 76 days with no update in 23 days**"). Split into two paragraphs (risks+blockers / hygiene) if needed to stay within the brevity limit.

---

#### Section 2: Consumption Trends

**Opening summary (2-3 short paragraphs):** Summarize overall consumption direction across all three comparison windows (7-day, 28-day, 90-day). Call out whether short-term momentum (7d) aligns with longer-term trends (90d) — e.g., "7-day consumption is up 5.2% but the 90-day trend shows a 1.8% decline, suggesting recent growth may be a spike rather than a sustained shift." Name the largest movers among the top workspaces with their individual changes, and highlight any workspace with an outsized swing (>20% in any interval) that warrants attention.

**Consumption table:**

The table includes an `Interval` column and groups rows by entity — `Total Account` first, then each workspace — with separate lines for 7d, 28d, and 90d comparisons. This lets the reader see short-, medium-, and long-term trends at a glance for each entity.

```markdown
| Workspace Name | Interval | Current Period ($) | Prior Period ($) | Change ($) | Change (%) |
|---|---|---|---|---|---|
| **Total Account** | 7d | $19,433 | $18,833 | +$600 | ↑ 3.2% |
| **Total Account** | 28d | $136,029 | $131,832 | +$4,197 | ↑ 3.2% |
| **Total Account** | 90d | $378,250 | $362,010 | +$16,240 | ↑ 4.5% |
| IDA-ADB-Workspace-01 | 7d | $2,356 | $2,576 | -$220 | ↓ 8.5% |
| IDA-ADB-Workspace-01 | 28d | $16,492 | $18,031 | -$1,539 | ↓ 8.5% |
| IDA-ADB-Workspace-01 | 90d | $48,205 | $51,440 | -$3,235 | ↓ 6.3% |
| ... | ... | ... | ... | ... | ... |
```

First three rows are always `Total Account` (7d → 28d → 90d). Follow with the top 5 workspaces by current 28d consumption descending, each with three interval rows. Bold the workspace name only on the `Total Account` rows to visually separate the account-level aggregate.

**Data freshness closing line:** "Latest consumption data available: [DATE] ([N] days old)"

---

#### Section 3: Use Case Updates

**Opening summary (2-3 short paragraphs):** Synthesize the most critical aspects across all three subsections: net pipeline $ movement and direction, the most notable stage progressions (count and highest-value), and any Red/Yellow flags requiring action. This lets the reader grasp the full use case picture before diving into subsections.

##### 3a. PoP Changes

**Count header line:** "N changes detected affecting [FISCAL_QUARTERS] compared to [PERIOD] ago:"

**Bullet list** -- one bullet per change (use the `usecase_link` from query results):
```markdown
- **[OWNER] {usecase_link}** (FY'27 Q1): Outflow of $30,000 due to use case being pushed out to next quarter
- **[OWNER] {usecase_link}** (FY'27 Q2): Inflow of $15,000 due to use case progressing into pipeline
```

**"Net Impact:"** closing paragraph stating the net $ change, whether most changes are inflows or outflows, and naming the primary drivers.

##### 3b. Use Case Progression

**"Key Highlights" opening:** State count of advancing use cases, combined $ in quarterly DBUs, and as-of date. Example: "Six use cases for SAP SE advanced stages in the past 14 days on 2026-03-04, representing a combined $165,000 in estimated quarterly DBUs."

**Group by stage movement type** with bold sub-headers. Always use a hyphenated list for use cases under each sub-header, even when only a single use case is listed:

```markdown
**Recent Production Launch (U6):**
- **[OWNER] {usecase_link}** ($15,000 quarterly): Went live (U6) on [DATE]. [Status] status with [brief narrative].

**Three Use Cases Moved to Evaluating (U3) on [DATE]:**
- **[OWNER] {usecase_link}** ($90,000 quarterly): [Status] status. [Brief narrative of current state.]
- **[OWNER] {usecase_link}** ($15,000 quarterly): [Status] status. [Brief narrative.]
```

Order from highest stage (U6) to lowest (U1). Include implementation status color and a 1-sentence narrative per use case describing what is happening or what comes next.

**"Most Significant Pipeline Movement:"** callout naming the highest-value use case progression with its $ amount and stage.

##### 3c. Risks

**"Critical Red-Flagged Use Cases"** subsection. If none: "No Red-flagged use cases found."

**"Key Yellow-Flagged Risks by Category"** subsection. Group use cases by risk category:

```markdown
**Customer Engagement Issues ([ACCOUNT_NAME] - $78K at risk)**
- **[OWNER] {usecase_link}** (Scoping, $54K/quarter): [Description of the issue -- no response, cancelled, considering alternative, etc.]
  Remediation: [Specific action with suggested owner and timeline.]

**Product/Feature Gaps ([ACCOUNT_NAME] - $60K at risk)**
- **[OWNER] {usecase_link}** (Proving, $60K/quarter): [Description of the gap or delay.]
  Remediation: [Specific action -- schedule workshop, engage specialist, etc.]
```

---

#### Section 4: Active User Trends

**Section title:** "Active User Trends - [FQ] (Current Quarter)"

**Opening summary (2-3 short paragraphs):** Summarize the overall user engagement trajectory — state whether DAU, WAU, and MAU are growing or declining, give the most significant % change, and note the current quarter's QAU compared to the prior quarter. If metrics diverge (e.g., WAU up but QAU down), call out the discrepancy upfront so the reader knows what to watch. Example: "SAP SE demonstrates strong user engagement growth across most metrics, with weekly active users increasing 11.8% quarter-over-quarter to 1,900 users. However, quarterly active users declined 1.9%, suggesting recent gains may not yet reflect in longer-term retention."

**"Current Quarter Performance" subsection:** State QAU count for the current quarter, compare to prior quarter with absolute and % change, and provide a 1-sentence narrative assessment.

**"Growth Trends" subsection:** Bullet list comparing current to prior quarter:
```markdown
- **Daily Active Users (DAU):** 620 users (+55 users, +9.7% growth)
- **Weekly Active Users (WAU):** 1,900 users (+200 users, +11.8% growth)
- **Monthly Active Users (MAU):** 3,422 users (+28 users, +0.8% growth)
```
Include QAU as a separate line if it tells a different story from the shorter-term metrics.

**Anomaly detection:** If DAU/WAU/MAU trends conflict significantly (e.g., one metric up >50% while another is down >10%), add a "Note:" paragraph flagging the discrepancy and recommending data validation.

---

#### Section 5: Blockers Overview

**Opening summary (2-3 short paragraphs):** State the count of blocked use cases (stages U2-U5), total $ in quarterly DBU consumption at risk, and the number of unique Aha blockers. Name the highest-impact blocker (most use cases or highest $ at risk) and note its current status. If one use case is affected by multiple blockers, call that out as a compounding risk. Example: "N use cases are currently blocked, representing $X in quarterly DBU consumption at risk across M unique Aha blockers. The most impactful is [Blocker Name] (DB-I-XXXXX), which alone blocks N use cases worth $Y in quarterly DBUs and remains in [Status] status."

**"All Blockers by Aha Feature"** heading. List blockers in descending order of blocked use case count:

Use the `blocked_usecase_links` array from query results for each blocker's sub-bullets:

```markdown
**Unity Catalog with HANA Data Lake File System (HDLF)** (DB-I-15234) - Status: Under Review - Blocking 4 use cases:
- [AB] {blocked_usecase_links[0]} (U3)
- [AM] {blocked_usecase_links[1]} (U3)
- [MK] {blocked_usecase_links[2]} (U3)
- [MK] {blocked_usecase_links[3]} (U4)

**Account Console - Azure Databricks Account PIM** (DB-I-12987) - Status: Open - Blocking 2 use cases:
- [AM] {blocked_usecase_links[0]} (U3)
- [MK] {blocked_usecase_links[1]} (U4)
```

Each blocker entry: bold name, Aha ID in parentheses, status, blocking count. Sub-bullets list each affected use case with stage in parentheses.

**"Key Observations:"** closing paragraph identifying patterns (e.g., one use case blocked by multiple features, a single feature blocking many use cases) and recommending product team engagement with ETAs.

---

#### Section 6: Hygiene

**Opening summary (2-3 short paragraphs):** State the total count of use cases with at least one hygiene flag, then break down by issue type (stale updates, stuck in stage, overdue milestones, incomplete onboarding plans). Highlight the worst offenders by name with their days-in-stage or days-since-update. If a single use case has multiple flags, call it out as the top priority. Example: "12 use cases exhibit hygiene issues — 9 have incomplete onboarding plans, 7 have stale notes (>10 days), and 4 have been stuck in U2 for over 60 days. [OWNER] {usecase_link} is the most critical: 76 days in U2 with no update in 23 days and onboarding plan missing Milestones & Timeline, Risks & Mitigation."

**Table** with flag indicators. Stage and estimated quarterly DBUs are shown in parentheses in the Use Case column to keep the table compact:

```markdown
| Use Case | Stale Update (>10d) | Stuck in U2 (>60d) | Stuck in U3/U4 (>90d) | On-boarding in past | Go-Live in past | Onboarding Plan Incomplete |
|---|---|---|---|---|---|---|
| [AB] {usecase_link} (Scoping, $15,000) | ✓ | ✓ | — | — | — | Milestones & Timeline, Risks & Mitigation |
```

Use `✓` for flagged and `—` for clean. For the **Onboarding Plan Incomplete** column, show the comma-separated list of missing sections from the `Missing Onboarding Plan Sections` query field (e.g., "Milestones & Timeline, Risks & Mitigation"). Use `—` if the plan is complete (query returns null).

**4B: Save Markdown to File**

Write the report to `/tmp/account_review_[ACCOUNT_NAME]_[DATE].md`.

**4C: Validate Links**

After generating the markdown, scan all Salesforce URLs in the report. Every `UseCase__c/` ID must be a real 15-18 character Salesforce ID that came directly from the `usecase_link` or `blocked_usecase_links` columns in the query results. If any link contains a fabricated or placeholder ID (e.g., sequential patterns like `a1B2C3D4E5`, `a1B2C3D4E6`), replace it with the correct `usecase_link` from the query data. Do NOT proceed to the next step until all links are verified.

---

### Step 5: Convert to Chosen Output Format

Based on the `OUTPUT_FORMAT` selected in Step 1D, convert the markdown report.

**If `OUTPUT_FORMAT` is `markdown`:** No conversion needed — the markdown file from Step 4B is the final output. Present the file path to the user.

**If `OUTPUT_FORMAT` is `pdf`:**

```bash
pip install weasyprint markdown
python3 ~/.claude/plugins/cache/fe-vibe/fe-specialized-agents/*/skills/markdown-to-pdf/resources/markdown_to_pdf.py \
  --input /tmp/account_review_[ACCOUNT_NAME]_[DATE].md \
  --output /tmp/account_review_[ACCOUNT_NAME]_[DATE].pdf
```

This uses the shared `markdown-to-pdf` skill from `fe-specialized-agents`, which applies DM Sans font and the Databricks brand color palette. The co-located `databricks_report.css` is applied automatically. To override, pass `--css /path/to/custom.css`.

Return the PDF path to the user.

**If `OUTPUT_FORMAT` is `google_doc`:**

1. **Convert markdown to Google Doc** using the markdown converter from `fe-google-tools`:

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/account_review_[ACCOUNT_NAME]_[DATE].md \
  --title "Account Review: [ACCOUNT_NAME] ([LOOKBACK_PERIOD])" \
  --font "DM Sans"
```

2. **Move to target folder** (if specified):

Use `google-docs` skill to move the created document to the user's specified Google Drive folder.

3. **Return the Google Doc URL** to the user.

---

### Step 6: Offer Additional Format

After delivering the report in the chosen format, **always** ask the user whether they would also like the report in another format.

**Which formats to offer depends on what was already generated:**

- **If `pdf` was chosen:** Ask: "Would you also like this report as a **Google Doc**?"
- **If `google_doc` was chosen:** Ask: "Would you also like this report as a **PDF**?"
- **If `markdown` was chosen:** Ask: "Would you also like this report as a **PDF**, a **Google Doc**, or both?"

If the user says yes, execute the corresponding conversion from Step 5 (the markdown source file is always available). If the user declines, proceed to Step 7.

---

### Step 7: Offer Distribution

After all format conversions are complete, **always** ask the user whether they would like to distribute the report.

Ask: "Would you like to distribute this report? I can send it via **Slack** (channel or DM) or **Email** (Gmail draft). If yes, to whom?"

If the user declines, the skill is complete.

If the user wants distribution, ask for:
- **Channel:** Slack or Email (or both)
- **Recipients:** Slack channel name / DM handle, or email addresses

Then proceed with the appropriate distribution method below.

**7A: Slack Distribution**

1. Use the `slack` MCP server or `google-chat` skill
2. Send a message with:
   - Account name and review period
   - Executive summary (Section 1)
   - Link to the full report (Google Doc URL or attached PDF)
3. Target: Specified Slack channel or DM

**7B: Email Distribution**

1. Load the Gmail skill: `/gmail`
2. Ensure Google Workspace authentication is complete (`/google-authentication`)
3. Create a draft email (saved to Gmail Drafts for review — **not sent automatically**):

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail/resources/gmail_builder.py \
  create-draft \
  --to "recipient1@example.com,recipient2@example.com" \
  --subject "Account Review: [ACCOUNT_NAME] ([LOOKBACK_PERIOD])" \
  --body "[EXECUTIVE_SUMMARY_TEXT]"
```

If a PDF was generated, attach it:

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail/resources/gmail_builder.py \
  create-draft \
  --to "recipient1@example.com,recipient2@example.com" \
  --subject "Account Review: [ACCOUNT_NAME] ([LOOKBACK_PERIOD])" \
  --body "[EXECUTIVE_SUMMARY_TEXT]" \
  --attach "/tmp/account_review_[ACCOUNT_NAME]_[DATE].pdf"
```

All recipients go into a single draft. If a Google Doc was created, include the Doc URL in the body. After creating the draft, tell the user: "A draft email has been saved to your Gmail Drafts. Please review and send it when ready."

---

## Query Resource Files

All SQL queries are stored in the `resources/` directory:

| File | Purpose |
|------|---------|
| `consumption_trends.sql` | Section 2: Overall and workspace-level consumption with PoP comparison |
| `usecase_pop_changes.sql` | Section 3a: Pipeline inflows/outflows over lookback period |
| `use_case_progress.sql` | Section 3b: Use case stage progressions in last 14 days |
| `usecase_risks.sql` | Section 3c: Red/Yellow use cases with AI-extracted blockers and risks |
| `active_user_trends.sql` | Section 4: DAU/WAU/MAU/QAU trends from `main.gtm_gold.account_active_users_quarterly` |
| `blockers_overview.sql` | Section 5: Active blockers by Aha feature with consumption impact |
| `salesforce_hygiene.sql` | Section 6: Hygiene flags (stale updates, stuck stages, missing plans) |

**Important:** These query files are **templates** with parameter placeholders. Before running, substitute:
- `{ACCOUNT_ID}` → Resolved Salesforce account ID
- `{LOOKBACK_START_DATE}` → Start of current period
- `{LOOKBACK_END_DATE}` → End of current period (usually CURRENT_DATE())
- `{PRIOR_START_DATE}` → Start of prior period
- `{PRIOR_END_DATE}` → End of prior period
- `{FISCAL_YEAR_QUARTER}` → e.g., "FY'27 Q1"

---

## Example Invocations

| Prompt | What Happens |
|--------|-------------|
| "Create account review for Acme Corp, 14 day lookback" | Full report for Acme Corp, comparing last 14 days to prior 14 days |
| "Generate bi-weekly review for Block, output as Google Doc" | Report for Block (14-day default), converted to Google Doc |
| "Account review for Netflix, 28 days, PDF output" | Report for Netflix (28-day lookback), saved as PDF |
| "Prepare for 1-on-1 with IC: Capital One account, FQ start lookback" | Report for Capital One, comparing current FQ to date vs prior FQ |
| "Account review for Stripe, 7 days, send to #account-team on Slack" | Report for Stripe (7-day lookback), posted to Slack channel |

---

## Related Skills

| Skill | When to Use |
|-------|------------|
| `/salesforce-actions` | Update use case fields, create/edit blockers based on report findings |
| `/logfood-querier` | Ad-hoc Logfood queries for deeper consumption or adoption analysis |
| `/uco-updates` | Update UCO NextSteps and health after review meeting |
| `/google-docs` | Manually format or edit the generated Google Doc |
| `/ae-biweekly-review` | Manager-level bi-weekly reviews across multiple AEs (not single account) |

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Account not found in Salesforce | Step 1A already uses fuzzy matching; try shorter substrings, abbreviations, or alternate spellings. Ask the user if still unresolved |
| No use cases returned | Check that use cases exist for this account in Salesforce; verify `Active__c = true` |
| Consumption data missing | Ensure `main.fin_live_gold.paid_usage_metering` is accessible; check account ID matches Salesforce |
| WAU/MAU query returns empty | Verify fiscal year/quarter string format (e.g., "FY'27 Q1" with apostrophe and space) |
| Blocker query fails | Check that blockers are linked to use cases via `UseCase__c` lookup field |
| Google Doc conversion fails | Ensure `fe-google-tools` plugin is installed and `/google-authentication` is complete |
| Email draft creation fails | Ensure `fe-google-tools` plugin is installed and `/google-authentication` is complete. Load the `/gmail` skill for detailed troubleshooting |
| PDF generation fails | Install weasyprint: `pip install weasyprint` |

---

## Notes

- **All queries use `--profile=logfood`** for Logfood/Databricks access.
- **Fiscal calendar:** Use the shared `fiscal_calendar.py` from `fe-manager/resources/` for FQ_Start calculations.
- **Markdown converter:** Always use `markdown_to_gdocs.py` for Google Doc output — do NOT manually construct batch updates.

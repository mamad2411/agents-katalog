---
name: dsa-quarterly-review
description: Generate the QBR — a comprehensive quarterly business review for a DSA manager's team with consolidated metrics, wins & shoutouts, QoQ comparisons, and forward-looking outlook. This is THE default QBR skill. Use this skill when the user says QBR, create the QBR, quarterly review, quarterly business review, quarter review, Q1 review, Q2 review, Q3 review, Q4 review, Q1 QBR, Q2 QBR, Q3 QBR, Q4 QBR, or any QBR request that does NOT mention a specific customer account name. Queries UCO pipeline, subscription activity, FTE capacity, and formats into an executive-level Google Doc and HTML Gmail draft. Works for any DSA manager. Note: for customer-specific account review slide decks, use account-review-deck instead.
user-invocable: true
---

# DSA Quarterly Business Review Generator

Generate a comprehensive quarterly business review for any DSA manager's team. Consolidates a full fiscal quarter (90 days) into an executive-level report with wins/shoutouts, QoQ trends, and a forward-looking next-quarter outlook. Phase 1 creates an editable Google Doc; Phase 2 converts to a rich HTML Gmail draft.

**Based on**: The monthly `dsa-business-overview` skill — same data sources, same agents, same domain rules, but scoped to a full quarter with additional strategic sections.

## When to Use This Skill

- Generate the quarterly DSA business review for any DSA manager's team
- Prepare for quarterly leadership reviews or QBR meetings
- Produce a consolidated view of the quarter: wins, pipeline, risks, capacity, outlook
- Create an executive-level quarterly newsletter for stakeholders

## Prerequisites

Before running this skill, ensure the following are authenticated:
1. **Databricks** — Run `/databricks-authentication` (for Logfood queries)
2. **Google** — Run `/google-auth` (for Google Doc editing + Gmail draft)
3. **Salesforce** — Run `/salesforce-authentication` (for UCO details and contacts)

## Required Information

The skill needs: **which DSA manager's team** and **which quarter** to generate the review for. Provided as: $ARGUMENTS

If no manager name is provided, ask:
> "Which DSA manager's team should I generate the Quarterly Business Review for? Please provide their name."

If no quarter is specified, auto-detect:
- If the current month is the 1st month of a quarter (Feb, May, Aug, Nov), default to the **prior quarter** (just completed)
- Otherwise, default to the **current quarter** (in progress)
- Always confirm with the user: "Generating Q{X} FY{YY} ({quarter_months}) review — is that correct?"

## Reference Files

- **`../dsa-business-overview/resources/DSA_LT_QUERIES.md`** — SQL query templates (shared with monthly skill)
- **`resources/QBR_TEMPLATE.md`** — Google Doc markdown template for quarterly review
- **`resources/QBR_EMAIL_TEMPLATE.html`** — HTML email structure, inline CSS, color palette
- **`../dsa-business-overview/resources/EMAIL_TEMPLATE.html`** — Base color palette reference

---

## Step 0: Identify Manager and Discover Team

Identical to the monthly `dsa-business-overview` skill.

### Query Team Roster

```sql
SELECT dsa AS name, email, hire_date, dsa_manager, bu, sales_subregion_level_1, cost_center, title_curated
FROM main.field_dsa.dsa_roster_curr
WHERE LOWER(dsa_manager) LIKE '%{manager_name}%'
ORDER BY dsa
```

Execute via `databricks api post /api/2.0/sql/statements/ --profile=logfood`.

### Build Working Variables

From the roster query, extract:
- `dsa_names`: List of full names
- `dsa_emails`: List of emails
- `manager_name`: Full manager name
- `vertical_label`: Team/vertical identifier from `sales_subregion_level_1` or `bu`
- `dsa_count`: Number of DSAs on team

---

## Step 1: Compute Quarter Variables

Compute all date variables for the report quarter:

```
report_quarter       = Q1/Q2/Q3/Q4 (user-specified or auto-detected)
quarter_start        = First day of quarter (e.g., 2026-02-01 for Q1 FY27)
quarter_end          = Last day of quarter (e.g., 2026-04-30 for Q1 FY27)
quarter_end_exclusive = First day of next quarter (e.g., 2026-05-01) — used as exclusive upper bound
fy_start             = February 1 of current FY (e.g., 2026-02-01 for FY27)
fy_label             = FY designation (e.g., "FY27")
quarter_label        = e.g., "Q1 FY27"
quarter_months       = e.g., "Feb–Apr 2026"
prior_quarter_start  = First day of prior quarter (for QoQ comparison)
prior_quarter_end    = Last day of prior quarter
next_quarter_start   = First day of next quarter (for outlook)
next_quarter_end     = Last day of next quarter
next_quarter_label   = e.g., "Q2 FY27"
next_quarter_months  = e.g., "May–Jul 2026"
```

**Fiscal Calendar**: FY starts Feb 1. Q1=Feb–Apr, Q2=May–Jul, Q3=Aug–Oct, Q4=Nov–Jan.

| Quarter | Start | End | Months |
|---------|-------|-----|--------|
| Q1 | Feb 1 | Apr 30 | Feb–Apr |
| Q2 | May 1 | Jul 31 | May–Jul |
| Q3 | Aug 1 | Oct 31 | Aug–Oct |
| Q4 | Nov 1 | Jan 31 | Nov–Jan |

---

## Step 2: Parallel Data Collection

Launch **two sub-agents simultaneously** — same agents as the monthly skill, but with **quarter-wide date filters**.

### Agent 1: Pipeline Analyst (`fe-dsa-lt:pipeline-analyst`)

Same query pattern as monthly (see `dsa-business-overview` SKILL.md Step 2), using the `resolved` CTE with UCO-level DSA attribution via SFDC `DSA__c`. **Replace month date filters with quarter date filters:**

1. U6 UCOs where `target_live_date >= quarter_start AND target_live_date < quarter_end_exclusive` → **"went live this quarter"**
2. U6 UCOs where `target_live_date >= fy_start` → **FY-to-date live** (summary stats)
3. All U5 UCOs → **active pipeline** (current state)
4. U5 UCOs where `target_live_date >= next_quarter_start AND target_live_date < next_quarter_end_exclusive` → **next quarter at stake**
5. U5 UCOs ranked by `estimated_quarterly_dollar_dbus DESC`, top 5 → **Top 5 Onboarding** (targeting next quarter)
6. U5 UCOs where `implementation_status IN ('Yellow', 'Red')` → **Risks & Blockers**
7. *(QoQ comparison)* U6 UCOs where `target_live_date >= prior_quarter_start AND target_live_date < prior_quarter_end_exclusive` → **prior quarter live count + ARR** (for delta)

### Agent 2: Capacity Calculator (`fe-dsa-lt:capacity-calculator`)

Same query pattern as monthly. **Replace month/quarter date filters with the report quarter:**

1. **Total Deployed Capacity** — `dsa_bandwidth_table` (current state, authoritative FTE source)
2. **Active account list** — from `account_dsa_accounts_html` ASSIGNMENT badges
3. **All subscriptions starting in quarter** — `dsa_project_assignment_outcomes EXPLODE`, `assignment_start_date >= quarter_start AND < quarter_end_exclusive`
4. Subscription classification via DSA_LT_QUERIES.md Section 12 (New Logo / Renewal / Transition)
5. **Investment DSAs** — `dsa_engagement_type = 'Invested DSA'`
6. **Expiring assignments** — assignments ending within the next quarter (`assignment_end_date >= quarter_end_exclusive AND < next_quarter_end_exclusive`)
7. Per-DSA FTE for capacity snapshot

**Wait for both agents to complete before proceeding.**

---

## Step 3: Executive Snapshot

7-row metrics table (expanded from monthly's 5 rows):

| Metric | Exact Computation |
|--------|-------------------|
| **Use Cases Live This Quarter** | Count + ARR of U6 where `target_live_date >= quarter_start AND < quarter_end_exclusive`. ARR = `SUM(estimated_quarterly_dollar_dbus) * 4`. |
| **FY-to-Date Live** | Count + ARR of U6 where `target_live_date >= fy_start`. If Q1, this equals "This Quarter". |
| **Active Onboarding Pipeline (U5)** | Count + ARR of all current U5 UCOs. |
| **Next Quarter ARR at Stake (Q{X+1})** | ARR of U5 where `target_live_date` in next quarter. |
| **New Subscriptions This Quarter** | "{new_logo_count} new logos + {renewal_count} renewals · +{net_new_fte} FTE (net new)" |
| **Total Deployed Capacity** | From `dsa_bandwidth_table`: FTE · DSAs · Active Accounts |
| **QoQ Delta** | If prior quarter data available: "UCOs: {delta} ({prior} → {current}), ARR: {delta}". If Q1 (first of FY): "First quarter of FY{YY} — no prior quarter comparison." |

---

## Step 4: Quarter Wins & Shoutouts

This is a **new section** not present in the monthly skill. It highlights the quarter's top achievements and recognizes team members.

### Auto-Populated Content

From the pipeline and capacity data, automatically generate:

**Major Wins:**
- Largest ARR UCO gone live this quarter (account, use case, ARR, DSA)
- Total UCOs live count and ARR for the quarter
- Any new logo wins (new accounts landed)
- Any significant tier upgrades

**Team Shoutouts:**
- Top 3 DSAs by UCO go-live count this quarter (name, count)
- DSA with the highest single ARR go-live
- Any DSA who went from 0 to multiple live UCOs (momentum)

### Manager-Editable Placeholders

After auto-populated content, include clearly marked placeholders:

```
**Additional Wins** *(edit below)*
- [Add: customer testimonials, internal recognition, process improvements]

**Personal Shoutouts** *(edit below)*
- [Add: certifications earned, above-and-beyond moments, team milestones, new hire welcome]
```

These placeholders are meant for the manager to fill in during the Google Doc editing phase before the email is generated.

---

## Step 5: Use Cases Live This Quarter

**Filter**: U6 UCOs where `target_live_date >= quarter_start AND target_live_date < quarter_end_exclusive`

Show **up to 10 rows** ranked by ARR descending (expanded from monthly's 5). If more than 10, show top 10 and note the overflow.

Table columns: Account | Use Case | ARR | DSA | Month

The **Month** column shows which month of the quarter the UCO went live (e.g., "Feb", "Mar", "Apr") — this provides month-level granularity within the quarterly view.

**Description line**: "{count} use cases reached production in Q{X} — generating ${ARR} in new ARR. FY-to-date: {fy_count} live · ${fy_arr} ARR."

---

## Step 6: Top 5 Onboarding — Going Live Next Quarter

From **all U5 UCOs** with `target_live_date` in the **next quarter**, rank by `estimated_quarterly_dollar_dbus DESC`. Take top 5.

This section is **forward-looking** — it previews what's coming in Q{X+1}, unlike the monthly skill which shows current quarter pipeline.

Same numbered narrative card format as monthly:

```
**1. {Account} — {Use Case Name}**
${ARR} ARR · {target_month} · {DSA_name} · Status: {display_status}
{1-2 sentence narrative}
```

If no U5 UCOs target next quarter: "No DSA-attributed U5 onboarding use cases targeting Q{X+1} ({next_quarter_months})."

---

## Step 7: Risks & Blockers

Identical to the monthly skill — U5 UCOs where `implementation_status IN ('Yellow', 'Red')`, top 5 by ARR.

Same numbered narrative cards with Plan to Green, Key Risk/Blocker, and Engaged fields.

If none: "No at-risk or red use cases at quarter end."

---

## Step 8: Quarter Subscription Activity

Same 4 sub-sections as monthly, but covering the **full quarter**. No deduplication needed — the quarterly report is the authoritative single view for the entire 90-day period.

### DSA Subscriptions

All new logos and renewals starting in the quarter (`assignment_start_date >= quarter_start AND < quarter_end_exclusive`). Classification uses the same global cross-team history check (DSA_LT_QUERIES.md Section 12).

Table columns: Account | DSA | Tier | FTE | Type | Month

**Month** column shows start month within the quarter.

If none: "No new subscriptions in Q{X}."

### Pipeline Opportunities

Not-yet-active subscriptions. If none: "No pipeline opportunities this period."

### Investment DSAs

Active invested assignments (`dsa_engagement_type = 'Invested DSA'`). Table: Account | DSA | Hours/Wk | End Date

Always shown. If none: "No investment DSA engagements this period."

### Account Transitions

All transitions effective in the quarter. Table: Account | Previous DSA | New DSA | Effective Month

If none: "No account transitions in Q{X}."

---

## Step 9: Next Quarter Outlook

This is a **new section** not present in the monthly skill. It provides forward-looking context for the next quarter.

### Auto-Populated Content

**Expiring Assignments:**
Assignments ending within the next quarter. Table: Account | DSA | Current Tier | End Date

**Pipeline at Stake:**
Total U5 ARR targeting next quarter, count of UCOs, and top 3 by ARR.

**Capacity Forecast:**
- DSAs who will be under-capacity after expirations
- DSAs who are already over-capacity
- Net FTE change expected

### Manager-Editable Placeholder

```
**Strategic Priorities for Q{X+1}** *(edit below)*
- [Add: hiring plans, account focus areas, process improvements, training initiatives]
```

---

## Step 10: Capacity Snapshot

Identical to the monthly skill — current state table from `dsa_bandwidth_table`.

Table columns: DSA | FTE | Status | Accounts

Status: Over Capacity (>1.0 FTE), At Capacity (=1.0), Under Capacity (<1.0)

Below the table:
- **Available capacity**: {X} FTE across {N} under-capacity DSAs
- **Expiring soon**: comma-separated list of assignments ending in next 90 days

---

## Step 11: Build Output (Google Doc → HTML Email)

Same two-phase workflow as the monthly skill.

### Phase 1: Google Doc

**Load `resources/QBR_TEMPLATE.md`** for content structure.

Write markdown to `/tmp/claude/dsa_quarterly_review.md`.

**HEADING STRUCTURE:**
- **H1** (`#`): Doc title — `DSA Quarterly Business Review — {Vertical}` (new docs only)
- **H2** (`##`): Quarter heading — `Q{X} FY{YY} ({quarter_months})  |  {Manager}, DSA Team Lead`
- **H3** (`###`): Section headings

Convert to Google Doc:
```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/claude/dsa_quarterly_review.md \
  --title "DSA Quarterly Business Review — {Vertical}"
```

Present to the manager for editing — especially the Wins & Shoutouts and Strategic Priorities sections.

### Phase 2: HTML Email

**Triggered when the user says** "create the email", "send it", "convert to email", "ready to send".

**Load `resources/QBR_EMAIL_TEMPLATE.html`** for exact HTML structure and inline CSS.

Convert edited Google Doc content to rich HTML. Write to `/tmp/claude/dsa_quarterly_review.html`.

Create Gmail draft:
```bash
cd ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail
python3 resources/gmail_builder.py create-draft \
  --to "{recipient_emails}" \
  --subject "DSA {Vertical} Quarterly Business Review - Q{X} FY{YY}" \
  --html "$(cat /tmp/claude/dsa_quarterly_review.html)"
```

---

## Required Sections & Empty-State Rules — MANDATORY

**Every quarterly review MUST include ALL of the following sections, even when empty.**

| # | Section | Empty-State Text |
|---|---------|-----------------|
| 1 | Intro paragraph | *(never empty — always write 3-4 sentences)* |
| 2 | Executive Snapshot (7 rows) | *(never empty)* |
| 3 | Quarter Wins & Shoutouts | Auto-populated from data + manager placeholders |
| 4 | Use Cases Live This Quarter | "No use cases reached production in Q{X}." |
| 5 | Top 5 Onboarding — Next Quarter | "No DSA-attributed U5 onboarding use cases targeting Q{X+1} ({next_quarter_months})." |
| 6 | Risks & Blockers | "No at-risk or red use cases at quarter end." |
| 7a | DSA Subscriptions | "No new subscriptions in Q{X}." |
| 7b | Pipeline Opportunities | "No pipeline opportunities this period." |
| 7c | Investment DSAs | "No investment DSA engagements this period." |
| 7d | Account Transitions | "No account transitions in Q{X}." |
| 8 | Next Quarter Outlook | Auto-populated from data + manager placeholder |
| 9 | Capacity Snapshot | *(never empty — always full team table)* |

### Validation Checklist

Before finalizing the Google Doc or HTML email, verify:
- [ ] All 9 top-level sections present (intro, snapshot, wins, live, top 5, risks, subscriptions, outlook, capacity)
- [ ] All 4 subscription sub-sections present
- [ ] Empty sections use prescribed empty-state text (not omitted)
- [ ] Executive Snapshot has all 7 rows
- [ ] Wins & Shoutouts has auto-populated content + manager placeholders
- [ ] Next Quarter Outlook has expiring assignments + pipeline + placeholder
- [ ] QoQ delta computed correctly (or first-quarter note)
- [ ] All UCO live dates fall within the report quarter boundaries
- [ ] ARR calculations use `estimated_quarterly_dollar_dbus * 4`

---

## Domain Rules

Same as `dsa-business-overview`:

### Tier Classification
- **Platinum**: >= 32 hours/week = 1.0 FTE
- **Gold**: >= 16 hours/week = 0.5 FTE
- **Silver**: < 16 hours/week = 0.25 FTE

### Databricks Fiscal Year
- FY starts **February 1**
- Q1: Feb–Apr, Q2: May–Jul, Q3: Aug–Oct, Q4: Nov–Jan

### ARR Calculation
- `ARR = estimated_quarterly_dollar_dbus * 4`

### Health Status Mapping
| Source | Display | Color |
|--------|---------|-------|
| Green | On Track | `rgb(39,174,96)` |
| Yellow | At Risk | `rgb(243,156,18)` |
| Red | Red | `rgb(231,76,60)` |
| NULL | Not Set | `rgb(149,165,166)` |

### Investment DSA Identification
- Filter: `dsa_engagement_type = 'Invested DSA'` (exact match)

---

## Common Pitfalls

All pitfalls from the monthly `dsa-business-overview` skill apply here. Additionally:

### Pitfall Q1: Wrong Quarter Boundaries
**Problem**: Using calendar quarters (Jan-Mar) instead of fiscal quarters (Feb-Apr)
**Solution**: Always use fiscal calendar — Q1 starts Feb 1, not Jan 1.

### Pitfall Q2: QoQ Comparison for Q1
**Problem**: Trying to compute QoQ delta for Q1 when Q4 was in the prior FY
**Solution**: Q1 can still compare to Q4 of prior FY. But if no prior quarter data is available (first time running), display "First quarter of FY{YY} — no prior quarter comparison."

### Pitfall Q3: Deduplication Not Needed
**Problem**: Applying the monthly deduplication step (reading prior month's email) to the quarterly report
**Solution**: The quarterly report covers the full quarter — no deduplication is needed. All subscriptions, transitions, and logos within `[quarter_start, quarter_end)` are included.

### Pitfall Q4: Mixing Current and Next Quarter Pipeline
**Problem**: Showing current quarter pipeline instead of next quarter in the "Top 5 Onboarding" section
**Solution**: The quarterly review's Top 5 is **forward-looking** — target next quarter. The current quarter's pipeline is already resolved as "live" or still in progress.

---

## Error Handling

Same as monthly `dsa-business-overview` — retry Logfood once on timeout, report partial results, re-auth as needed.

---

## Related Skills

- `/dsa-business-overview` — Monthly business update (same data sources, monthly scope)
- `/dsa-capacity-planning` — Detailed FTE allocation analysis
- `/dsa-assignment-sync` — Validate assignments against Salesforce
- `/google-docs` — Google Doc creation
- `/gmail` — Gmail draft creation

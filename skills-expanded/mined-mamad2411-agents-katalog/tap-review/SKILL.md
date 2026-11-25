---
name: tap-review
description: Generate a full Technical Account Planning (TAP) review deck and companion Google Doc for a customer account. Clones the FY26 15-slide TAP template, auto-fills data from Logfood, SFDC, and TAP Map output, and marks remaining sections with [TODO] placeholders. Use when asked to "build a TAP deck", "create TAP review", "generate TAP slides", "prep TAP planning", "account planning deck", or "TAP presentation".
user-invocable: true
model: opus
---

# TAP Review Deck Generator

Generate a full Technical Account Planning (TAP) deck and companion Google Doc for a customer account. Clones the FY26 15-slide TAP template, auto-fills quantitative sections from Logfood/SFDC/TAP Map data, and marks strategic sections with `[TODO]` placeholders for human input.

## Quick Start

```
/tap-review <Account Name>
/tap-review <Account Name> --skip-tap-map
```

## Prerequisites

Before running this skill, ensure the following are authenticated:
1. **Salesforce** — run `/salesforce-authentication`
2. **Databricks** — run `/databricks-authentication` (for Logfood queries)
3. **Google** — run `/google-auth` (for Slides + Docs creation)

## Required Information

- **Account Name** (required): Provided as `$ARGUMENTS`
- **`--skip-tap-map`** (optional): Skip running fe-account-tap-map if it was already run recently

If no account name is provided, ask the user for one before proceeding.

## Reference Files

This skill uses resource files for detailed mappings:
- **`resources/TAP_TEMPLATE_MAP.md`** — Slide-by-slide index of all 15 slides, table structures, placeholder text patterns
- **`resources/SECTION_AUTOFILL.md`** — Per-slide data source mapping and auto-fill rules
- **`resources/DOC_TEMPLATE.md`** — Markdown template for the companion Google Doc

Load the relevant resource file when entering each step.

---

## Step 0: Parse Input

1. Extract account name from `$ARGUMENTS`. If `--skip-tap-map` flag is present, note it.
2. Read `~/.vibe/profile` for:
   - SA name (for attribution in the deck)
   - AE name (from team roles)
   - Team info (`team_region`)
3. Sanitize account name for file paths: `ACCOUNT_SLUG = account_name.lower().replace(" ", "_").replace(".", "")`

---

## Step 1: Run fe-account-tap-map (Conditional)

**Skip this step if `--skip-tap-map` was passed.**

Invoke the TAP Map skill to generate TAM sizing, peer benchmarks, competitive analysis, and champion mapping:

```
/fe-account-tap-map <Account Name>
```

After it completes, read the output file:
```
/tmp/claude/<account_slug>_tap_map.md
```

Parse the TAP Map output into structured data:
- **TAM per workload** — 8 workload areas with TAM ranges, confidence
- **Champions** — Executive buyers and champions mapped to workloads
- **Incumbent tools** — Competitive tools per workload area
- **Peer benchmarks** — Comparison table (over/under-indexed)
- **DBRX %** — Penetration percentage per workload
- **Current consumption** — Total and by-SKU breakdown

If the file doesn't exist or parsing fails, log a warning and proceed with reduced data. The deck will have more `[TODO]` sections but still be useful.

---

## Step 2: Collect Additional Data (Parallel)

Data that fe-account-tap-map does NOT provide. Launch TWO `fe-internal-tools:field-data-analyst` agents simultaneously:

### Agent 1 — UCO Pipeline + Consumption Trends (Logfood)

**Logfood profile:** `logfood`

First, find the Salesforce Account ID:
```bash
sf data query --query "SELECT Id, Name FROM Account WHERE Name LIKE '%<Account Name>%' LIMIT 5" --json
```

Then run these queries against Logfood:

**All UCOs for the account (all stages including U6/U7 for history):**
```sql
SELECT
  Usecase_ID, Usecase, Account, UCO_Stage, health_status,
  LEFT(Next_Steps, 300) AS Next_Steps,
  Implementation_Start_Date, Full_Prod_Date,
  Monthly_UCO_Dollar_DBUs, onboard_fy_quarter, golive_fy_quarter,
  days_in_stage, workload_type
FROM main.field_usage_dashboard.uco_data
WHERE account_id = '<SFDC_ACCOUNT_ID>'
ORDER BY Monthly_UCO_Dollar_DBUs DESC
```

**Monthly $DBU consumption trend (18 months):**
```sql
SELECT usage_date, SUM(dbu_dollars) as dbu_dollars
FROM main.gtm_data.c360_consumption_monthly
WHERE account_id = '<SFDC_ACCOUNT_ID>'
AND usage_date >= DATE_ADD(CURRENT_DATE(), -18)
GROUP BY usage_date ORDER BY usage_date
```

**Consumption by SKU (product adoption, 12 months):**
```sql
SELECT sku, SUM(dbu_dollars) as dbu_dollars
FROM main.gtm_data.c360_consumption_monthly
WHERE account_id = '<SFDC_ACCOUNT_ID>'
AND usage_date >= DATE_ADD(CURRENT_DATE(), -12)
GROUP BY sku ORDER BY dbu_dollars DESC
```

Save results to `/tmp/claude/tap_review_<account_slug>_logfood.json`.

### Agent 2 — SFDC Supplementary Data

Pull the following from Salesforce (using `sf data query`):

**Opportunities (pipeline, competitors):**
```bash
sf data query --query "SELECT Id, Name, StageName, Amount, CloseDate, Competitors__c, Type FROM Opportunity WHERE AccountId = '<ACCOUNT_ID>' AND IsClosed = false" --json
```

**ASQs/Specialist Requests:**
```bash
sf data query --query "SELECT Id, Name, Status__c, Request_Type__c, Notes__c FROM ApprovalRequest__c WHERE Account__c = '<ACCOUNT_ID>' ORDER BY CreatedDate DESC LIMIT 20" --json
```

**Blockers:**
```bash
sf data query --query "SELECT Id, Name, Description__c, Status__c, Priority__c FROM Blocker__c WHERE Account__c = '<ACCOUNT_ID>'" --json
```

**Key Contacts (beyond what tap-map identified):**
```bash
sf data query --query "SELECT Id, Name, Title, Email, Department FROM Contact WHERE AccountId = '<ACCOUNT_ID>' ORDER BY LastModifiedDate DESC LIMIT 30" --json
```

Save results to `/tmp/claude/tap_review_<account_slug>_sfdc.json`.

---

## Step 3: Clone TAP Template and Populate Slides

**Load `resources/TAP_TEMPLATE_MAP.md`** for the slide-by-slide mapping.

### 3a: Clone the Template

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-slides/resources/gslides_builder.py \
  copy --pres-id "1epknukOBfeHAjU8fUzbmkRtbZ9v2OEkNwnwpTjLCuhQ" \
  --title "<Account Name> — TAP Review"
```

Capture the new presentation ID from the output.

### 3b: Read Cloned Presentation Structure

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-slides/resources/gslides_builder.py \
  list-slides --pres-id "<NEW_PRES_ID>"
```

This reveals slide IDs (which change on copy). Map them to the template index using `TAP_TEMPLATE_MAP.md`. Verify the cloned deck has **15 slides** matching the expected structure.

### 3c: Global Text Replacement

Replace account-level placeholders across the entire presentation:

```bash
GSLIDES="python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-slides/resources/gslides_builder.py"

# Account name — replace the template placeholder pattern
$GSLIDES replace-text --pres-id "<NEW_PRES_ID>" --find "<Account Name>" --replace "<Actual Account Name>" --match-case

# AE name
$GSLIDES replace-text --pres-id "<NEW_PRES_ID>" --find "<AE Name>" --replace "<Actual AE Name>" --match-case

# Date
$GSLIDES replace-text --pres-id "<NEW_PRES_ID>" --find "<Date>" --replace "$(date +%B\ %Y)" --match-case
```

### 3d: Per-Slide Content Population

**Load `resources/SECTION_AUTOFILL.md`** for the detailed field-by-field mapping.

For each group of slides, populate content based on available data:

**Slides 0-3 (Customer Overview & Strategy):** Replace title fields (account name, AE, date). Fill customer overview table on slide 1 from TAP Map account data. Populate stakeholder table on slide 2 from TAP Map champions + SFDC contacts. Mark slide 3 (Strategic Priorities) as `[TODO: Define strategic priorities and outcome mapping with AE]`.

**Slides 4-6 (TAP Map & AI Platform):** Fill tech stack table on slide 4 by mapping TAP Map incumbent tools to tech layers (BI, ETL, ML/AI, DW, Ingest, Governance, Storage, DB, App, Serving, Sharing). Fill EB/Budget from TAP Map TAM data. Populate AI platform entries on slide 5 from TAP Map AI-related data. Mark slide 6 (AI Use Cases) as `[TODO: ...]`.

**Slides 7-9 (Usage, UCOs & Pipeline):** Fill consumption trend and SKU breakdown on slide 7 from Logfood data. Build full UCO table on slide 8 from Logfood (all stages, sorted by $DBU DESC) with columns: Name, Stage, Days in Stage, $DBU/Qtr, Go-Live. Mark slide 9 (UCO Dependencies) as `[TODO: ...]`.

**Slides 10-11 (SA Assessment & Key Asks):** Pre-fill suggested SA questions on slide 10 based on data patterns (champion gaps, stalled UCOs, low penetration areas). Build Key Asks table on slide 11 from SFDC Blockers + ASQs with columns: Specific Ask, Why, Owner, Next Steps.

**Slides 12-14 (Appendix):** Keep as-is — these are reference slides.

### 3e: Replace Unfilled Placeholders

After all data insertion, scan for any remaining `<Placeholder>` patterns and replace them with `[TODO: ...]` markers so nothing is left as raw template text:

```bash
# Get presentation info to find remaining placeholders
$GSLIDES info --pres-id "<NEW_PRES_ID>"
```

For each remaining placeholder found, replace with a meaningful TODO:
```bash
$GSLIDES replace-text --pres-id "<NEW_PRES_ID>" --find "<PLACEHOLDER>" --replace "[TODO: Add placeholder info]" --match-case
```

---

## Step 4: Generate Companion Google Doc

**Load `resources/DOC_TEMPLATE.md`** for the markdown template.

### 4a: Build the Markdown

Write the companion document to `/tmp/claude/tap_review_<account_slug>.md` using the DOC_TEMPLATE.md structure. Populate all the same data that went into the slides, organized as a readable document with tables.

### 4b: Convert to Google Doc

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/claude/tap_review_<account_slug>.md \
  --title "<Account Name> — TAP Review"
```

---

## Step 5: Present Results

After both deliverables are created, present a summary:

```
TAP Review Complete — <Account Name>

Deliverables:
  - Slides: <Google Slides URL>
  - Doc:    <Google Docs URL>

Auto-populated slides:
  - Slide 0 (Title): Account name, AE, date
  - Slide 1 (Customer Overview): Company info, team RACI
  - Slide 2 (Org Chart): Stakeholder table (layout is manual)
  - Slide 4 (TAP Map): Tech stack with incumbents and EB/Budget
  - Slide 5 (AI Platform): AI tool mapping (partial)
  - Slide 7 (Usage): Consumption trend, SKU breakdown, challenges
  - Slide 8 (UCOs): Full UCO pipeline table
  - Slide 11 (Key Asks): Blockers and ASQs

TODO slides (require human input):
  - Slide 3: Strategic Priorities & Outcome Map
  - Slide 6: Horizontal AI Use Cases
  - Slide 9: UCO Dependency Graph
  - Slide 10: SA Questions (suggestions pre-filled)

Appendix slides (reference, keep as-is):
  - Slides 12-14: Appendix divider + AI Platform Map references

Suggested next steps:
  1. Review the Slides deck and fill [TODO] sections
  2. Arrange stakeholder org chart (slide 2) using the populated table
  3. Define strategic priorities with AE (slide 3)
  4. Run customer AI discovery session for slide 6
  5. Review and customize SA questions (slide 10)
```

---

## Error Handling

| Issue | Resolution |
|---|---|
| TAP Map skill fails | Proceed without TAP Map data; more sections will be [TODO] |
| Account not found in SFDC | Ask user to clarify name, try variations (Inc., Corp., Group) |
| Template clone fails | Check Google auth (`/google-auth`), verify template ID is accessible |
| Logfood timeout | Retry once after 30s (cold start), then proceed with SFDC data only |
| No UCOs found | Note in output; slides 7-9 will be mostly [TODO] |
| No ASQs/Blockers | Note in output; slide 11 will be mostly [TODO] |
| Google auth expired | Run `/google-auth` |
| Slide structure mismatch | If template has changed (not 15 slides), warn user; populate what can be matched |

## Related Skills

- `/fe-account-tap-map` — TAM sizing, peer benchmarks, competitive analysis (used in Step 1)
- `/ae-uco-hygiene` — UCO hygiene audit (may suggest running this skill for flagged accounts)
- `/google-slides` — Google Slides operations
- `/google-docs` — Google Docs operations
- `/fe-architecture-diagram` — Generate architecture diagrams
- `/lucid-diagram` — Generate diagrams for UCO dependency graph (slide 9)

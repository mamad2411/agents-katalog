---
name: ssagent-researcher
description: Researches a new ASQ (Specialist SA Request) end-to-end. Pulls ASQ details from Salesforce, identifies technical problems, researches them via product-question-researcher, queries Databricks consumption via logfood, and synthesises everything into an SSA briefing. Use when asked "research my new ASQ", "brief me on AR-XXXXXXXXX", or "/ssagent-researcher AR-XXXXXXXXX".
argument-hint: "AR-XXXXXXXXX"
user-invocable: true
model: sonnet
---

# ASQ Researcher

Research a Salesforce ASQ end-to-end and produce a structured SSA briefing.

**Usage:** `/ssagent-researcher AR-000098660`

---

## Prerequisites — Auth Checks

Load the profile using `load_profile.py` from `ssagent-sfdc` (returns all keys with defaults applied). Extract `sf_org` and `initials`. If either is `None`, fall back to `fe-salesforce-tools:salesforce-authentication` and the User query pattern from `ssagent-sfdc` Reusable Query Patterns.

Substitute the resolved `sf_org` value as a **literal** into every `<SF_ORG_USERNAME>` placeholder below.

Then run these additional checks (do not continue past a failure):

**1. Google** — invoke `fe-google-tools:google-auth`.

**2. Glean & Logfood MCPs** — invoke `fe-vibe-setup:validate-mcp-access`.

---

## Step 1 — Fetch ASQ from Salesforce (Sequential)

```bash
sf data query --query "SELECT Id, Name, Status__c, Account_Name__c, Account__c, Support_Type__c, AssignmentDate__c, End_Date__c, Request_Description__c, Submit_Comments__c, Request_Status_Notes__c, Additional_Notes_or_Doc_Links__c FROM ApprovalRequest__c WHERE Name = '$ARGUMENTS'" --target-org <SF_ORG_USERNAME> --json
```

Extract and note:
- `Id` — Salesforce record ID, used in all subsequent queries
- `Account__c` — Account ID, used for customer lookups and logfood
- `Account_Name__c`, `Status__c`, `Support_Type__c`, `AssignmentDate__c`, `End_Date__c`
- `Request_Description__c` — read fully, identify **2–5 specific technical problems** and list them explicitly
- `Request_Status_Notes__c` — note the full current value (used when writing back at the end)
- `Additional_Notes_or_Doc_Links__c` — note the full current value (used when writing back at the end)

---

## Step 2 — Fetch Salesforce Context (Parallel)

Run these three queries in parallel (single message, multiple tool calls):

**A. UCOs linked to this ASQ** — two-step (field is `Stages__c`, NOT `Stage__c`):
```bash
sf data query --query "SELECT Id, Use_Case__c FROM Approved_UseCase__c WHERE Approval_Request__c = '<ASQ_SFDC_ID>'" --target-org <SF_ORG_USERNAME> --json

sf data query --query "SELECT Id, Name, Stages__c, Amount__c, MonthlyTotalDollarDBUs__c, ProjectedConsumption__c, Business_Value_Description__c, POCStatus__c, Competitor_Status__c, Customer_Notes__c FROM UseCase__c WHERE Id IN (SELECT Use_Case__c FROM Approved_UseCase__c WHERE Approval_Request__c = '<ASQ_SFDC_ID>')" --target-org <SF_ORG_USERNAME> --json
```

**B. Recent customer ASQs:**
```bash
sf data query --query "SELECT Name, Status__c, Support_Type__c, AssignmentDate__c, End_Date__c, Request_Description__c FROM ApprovalRequest__c WHERE Account__c = '<ACCOUNT_ID>' ORDER BY AssignmentDate__c DESC LIMIT 10" --target-org <SF_ORG_USERNAME> --json
```

**C. Account details:**
```bash
sf data query --query "SELECT Id, Name, BillingCountry, Industry, AnnualRevenue FROM Account WHERE Id = '<ACCOUNT_ID>'" --target-org <SF_ORG_USERNAME> --json
```

---

## Step 3 — Parallel Research Phase

**Before constructing any task prompt below, substitute ALL placeholders in square brackets** with actual values from Steps 1 and 2. Never pass literal bracket placeholders to a subagent.

**Launch all research tasks simultaneously using the Task tool in a single message.**

### Task A — Customer Glean Research

Spawn a `general-purpose` subagent with this prompt:

```
Research the customer "[CUSTOMER_NAME]" (Salesforce Account ID: [ACCOUNT_ID]) across
internal Databricks sources using the mcp__glean__glean_read_api_call tool
(endpoint: "search.query").

Run these searches in parallel (single message, multiple tool calls):

1. General customer search:
   params: {"query": "[CUSTOMER_NAME] Databricks", "page_size": 10,
            "request_options": {"timePeriod": "PAST_YEAR"}}

2. Customer in Drive (docs, presentations):
   params: {"query": "[CUSTOMER_NAME]", "page_size": 8,
            "request_options": {"facetFilters": [{"fieldName": "datasource",
            "values": [{"value": "gdrive", "relationType": "EQUALS"}]}],
            "timePeriod": "PAST_YEAR"}}

3. Customer mentions in Slack:
   params: {"query": "[CUSTOMER_NAME]", "page_size": 8,
            "request_options": {"facetFilters": [{"fieldName": "type",
            "values": [{"value": "conversation", "relationType": "EQUALS"}]}],
            "timePeriod": "PAST_YEAR"}}

After the searches complete, identify the 2–3 most valuable documents in the results.
Read each in full using the mcp__google__google_read_api_call or
mcp__confluence__get_confluence_page_content tool as appropriate.

Extract: key stakeholders, technical context, engagement history, competitive mentions,
and links to all key documents. Return a concise markdown report.
```

### Task B — Consumption via Logfood

Spawn a `general-purpose` subagent with this prompt:

```
Query 12 months of consumption for Salesforce Account ID: [ACCOUNT_ID].

Invoke the `fe-internal-tools:logfood-querier` skill to do this. Pass it the
following request:

  "Query 12 months of monthly consumption from main.fin_live_gold.paid_usage_metering
   for sfdc_account_id = '[ACCOUNT_ID]'. Return month, total DBUs, and total list $
   (list_price * usage_amount), ordered newest first."

Return the monthly table and highlight: total 12m spend, peak month, any sharp
drop-offs or ramp-ups that might be significant for the SSA to understand.
If no rows, note the customer has minimal/no consumption.
```

### Task C — Topic Research (one task per problem)

For **each** technical problem identified in Step 1, spawn a separate `fe-workflows:product-question-researcher` subagent (model: `sonnet`). Run all topic tasks in the same parallel batch as Tasks A and B.

Subagent prompt template per topic:

```
[PROBLEM_TITLE] — for a customer engagement with [CUSTOMER_NAME] ([INDUSTRY], [COUNTRY]).

Context: [PROBLEM_DESCRIPTION]

Research this as a Databricks product question. Focus on:
- What Databricks capabilities address this requirement
- Known limitations or gotchas
- GA vs preview status of relevant features
- Recent changes or roadmap items (flag anything from the last 6 months as [RECENT])
- How similar customers have approached this

IMPORTANT: Do NOT create a Google Doc. Return your findings as a concise markdown
report only — it will be synthesised into a single ASQ briefing document.
```

---

## Step 4 — Synthesise into SSA Briefing

Collect all outputs from Steps 2 and 3, then write the final report.

**Determine the output path:**

Check if the current working directory is an engagement folder (contains `databricks.yml` and a `research/` directory):
```bash
# Use asq_root from profile, default ~/ASQ
ASQ_ROOT="<asq_root from profile or ~/ASQ>"

if [ -f databricks.yml ] && [ -d research ]; then
  OUTPUT_DIR="research"
  echo "Engagement folder detected — writing to research/"
else
  CUSTOMER_SLUG=$(echo "<CUSTOMER_NAME>" | tr '[:upper:] ' '[:lower:]_' | tr -cd 'a-z0-9_')
  DATE=$(date +%Y-%m-%d)
  TOPIC_SLUG="<2-4 word slug>"
  OUTPUT_DIR="${ASQ_ROOT}/${CUSTOMER_SLUG}_${DATE}_${TOPIC_SLUG}/research"
  mkdir -p "$OUTPUT_DIR"
  echo "No engagement folder — writing to $OUTPUT_DIR"
fi
```

Write the full report to `$OUTPUT_DIR/asq_brief.md` using the template below.

**Then create a Google Doc** using `fe-google-tools:google-docs`:
```bash
python3 $(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py) \
  --input "$OUTPUT_DIR/asq_brief.md" \
  --title "ASQ Research: <ASQ-ID> — <Customer Name>"
```

**Then update Salesforce** — show the user what will be written, then use `AskUserQuestion` with options:
- "Approve" (Recommended) — write to Salesforce as shown
- "Edit" — let user modify the values before writing
- "Skip" — do not write to Salesforce

Fields to display:
  - `Additional_Notes_or_Doc_Links__c`: prepend `<GOOGLE_DOC_URL>`
  - `Request_Status_Notes__c`: prepend `<INITIALS> <DATE>: Research brief completed.`

On approval, use `sf_update.py prepend` from `ssagent-sfdc` (read-back verification runs automatically).

Confirm success, then tell the user:
- Local: `$OUTPUT_DIR/asq_brief.md`
- Google Doc: `<GOOGLE_DOC_URL>`
- Salesforce: ASQ updated with doc link and status note

---

## Report Template

```markdown
# ASQ Research: <ASQ-ID> — <Customer Name>
**Date:** <today>  |  **Status:** <status>  |  **Support Type:** <type>  |  **Due:** <end_date>

---

## 1. ASQ Overview
[2–3 sentence summary of what is being asked and why the SSA is needed]

**Partner/SI:** [if mentioned]
**Key internal contacts:** [from ASQ or Glean research]

## 2. Technical Problems
1. ...
2. ...

## 3. Technical Research

### Problem 1: [Title]
[Summary of findings. Mark recent items [RECENT]. Include source URLs.]

### Problem 2: [Title]
[...]

## 4. Customer Context

### Account Profile
**[Customer Name]** | [Country] | [Industry] | Revenue: [if known]

### Engagement History (Glean + SFDC)
[Prior engagements, stakeholders, Slack discussions, Drive documents.]

### Previous ASQs
| ASQ | Date | Type | Topic (summary) |
|-----|------|------|-----------------|
| ... | ...  | ...  | ...             |

### Linked Use Cases
| UCO Name | Stage | Monthly $DBU | Amount | POC Status | Business Value |
|----------|-------|-------------|--------|------------|----------------|
| ...      | ...   | ...         | ...    | ...        | ...            |

## 5. Customer Consumption (Last 12 Months)
| Month | DBUs | List $ |
|-------|------|--------|
| ...   | ...  | ...    |

[Total 12m spend, peak month, trend]

## 6. SSA Briefing — Suggested Focus & Actions

**Top focus areas:**
- ...

**Risks / watch-outs:**
- ...

**Suggested preparation:**
- ...

**Key questions to ask the customer:**
- ...
```

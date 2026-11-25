---
name: create-engagement-report
description: Generate full-draft PS Engagement Reports from customer and/or project name. Delegates context gathering to the engagement-context-collector subagent (Salesforce/FF, Gmail, Google Drive, Slack, Jira, Confluence, Glean, Logfood), then synthesizes everything into a full draft Google Doc following the official PS Engagement Report template. Use when creating engagement reports, ER drafts, or documenting completed PS engagements.
user-invocable: true
---

# PS Engagement Report Generator

This skill produces complete draft PS Engagement Reports. It delegates all data gathering to a specialized subagent, then drives synthesis and Google Doc creation directly — interacting with you at every step to fill gaps and confirm the output location.

## Accepted Inputs

| Input Type | Example | How It's Used |
|------------|---------|---------------|
| Customer + Project | "LogixHealth SQL Server Migration" | Search across all sources |
| FinancialForce Project ID | `PRJ-12345` | Direct FinancialForce lookup |
| SFDC Opportunity ID | `006XXXXXXXXX` | Direct Salesforce lookup |
| Slack Channel | `#logixhealth-migration` | Use as primary Slack source |
| Any combination of the above | — | Each identifier sharpens the search |

## Example Invocations

```
/create-engagement-report LogixHealth SQL Server Migration
/create-engagement-report Nubank BigQuery migration project
/create-engagement-report JPMC CRAM  PRJ-98765
/create-engagement-report Constellation NextGen Data Platform
```

---

## Execution Workflow

Follow these steps in order. Do not skip steps.

---

### Step 1: Read Template Resources

Resolve the resources directory from the marketplace installation and read both reference files before doing anything else:

```bash
RESOURCE_DIR=$(ls -d ~/.claude/plugins/cache/fe-vibe/fe-ps-tools/*/skills/create-engagement-report/resources 2>/dev/null | sort -V | tail -1)
```

Read both files using the Read tool:
- `${RESOURCE_DIR}/ENGAGEMENT_REPORT_TEMPLATE.md` — the full document template; every section must be present in the output
- `${RESOURCE_DIR}/SECTION_GUIDANCE.md` — per-section writing rules, quality criteria, and formatting expectations

Keep this content in mind throughout generation. **Do not proceed without reading both files.**

---

### Step 2: Gather Context via the Collector Subagent

Invoke the `engagement-context-collector` subagent using the Task tool:

```
Task tool with subagent_type='fe-ps-tools:engagement-context-collector' and model='opus'
Prompt: "Gather all available context for a PS Engagement Report.
Customer / Account: {CUSTOMER_NAME}
Project: {PROJECT_NAME}
Additional identifiers provided by user: {any FF Project ID, Opp ID, Slack channel, Google Doc links, Jira tickets provided}"
```

The collector will:
- Interactively prompt the user for optional explicit resource links (Google Docs, Slack channels, Jira tickets, etc.) and confirm the engagement identifiers
- Search Salesforce/FinancialForce, Gmail, Google Drive, Slack, Jira, Confluence, Glean, and Logfood
- Validate its findings with the user mid-way and at the end
- Return a single structured context document

Wait for the collector to finish and return the context document before proceeding.

---

### Step 3: Review Context and Identify Gaps

Carefully read the structured context document returned by the collector. For each template section, assess whether there is sufficient data to write a quality draft or whether a placeholder is needed.

Build a mental map of:
- **Well-sourced sections** — have concrete data, names, metrics, quotes
- **Thin sections** — data exists but is vague or incomplete
- **Empty sections** — nothing found; will need user input or `[To be completed]`

---

### Step 4: Ask the User to Fill Critical Gaps

Use `AskUserQuestion` for **critical missing items only** — things that genuinely cannot be written without input:

- **Author name(s)** — who is writing this report (if not in Salesforce team data)
- **Specific accomplishment metrics** — numbers that were not found in Slack or Logfood (e.g., tables migrated, time saved, cost reduction)
- **Delivery materials link** — URL to project assets in Google Drive (architecture docs, runbooks)
- **Customer quotes** — if none were found in Slack or Gmail
- **Unresolved challenge details** — challenges mentioned without a stated resolution

**Do NOT ask about nice-to-have items.** Use `[To be completed]` placeholders for anything optional. Do not ask for data that the collector already retrieved.

If the user mentions additional sources during this conversation (e.g., "there's also a Confluence page at X" or "check Slack channel #abc"), proceed to Step 5. Otherwise, skip to Step 6.

---

### Step 5: Re-invoke Collector for Additional Sources (if needed)

If the user identifies new sources during Step 4, re-invoke the collector with a targeted prompt:

```
Task tool with subagent_type='fe-ps-tools:engagement-context-collector' and model='opus'
Prompt: "Fetch additional context for the {CUSTOMER_NAME} engagement.
The user has provided the following specific sources to pull:
{list the explicit links or sources the user mentioned}
Focus only on these sources — do not re-search sources already covered."
```

Merge the returned content with the original context document before writing.

---

### Step 6: Generate the Full Report

Write the complete engagement report as a single markdown document. Reference the template structure and section guidance from Step 1 throughout.

Map collected context to sections as follows:

| Section | Primary Sources |
|---------|----------------|
| Customer Name & Project Title | Salesforce/FF |
| Customer Stakeholders | Salesforce Opportunity contacts, Slack, user input |
| Databricks Delivery Team | FF project assignments |
| Partner Delivery Team | FF/Salesforce partner data |
| Databricks Account Team | Salesforce account team (AE, SA, EM) |
| Executive Summary | Synthesize from all sources — 3-4 sentences: who, what, how, impact |
| Project Objectives (The Why) | Salesforce use cases, Google Drive SOW, Slack kickoff discussions |
| Implementation Details (The What) | Slack technical discussions, Google Docs, Gmail |
| Accomplishments / Highlights | Slack milestones, Logfood consumption metrics, Gmail |
| Challenges Faced / Resolved | Slack discussions, Jira ES tickets |
| Potential Next Steps | Salesforce, Slack, user input |
| Internal Metadata Table | FF project (author, FF ID, BU, industry, cloud, dates, use case, partners) |
| Key Learnings / Lessons Learned | Slack retrospectives, Confluence, Gmail |
| Databricks Products Used | Slack, Google Docs, Jira |
| Product Challenges / Gaps | Jira with formatted links: `[ES-XXXXXX](https://databricks.atlassian.net/browse/ES-XXXXXX)` |
| Assets Used to Assist Delivery | Slack, Google Drive, user input |
| Delivery Assets Improvement Opportunities | Slack, user input |
| Customer Quotes | Slack (verbatim), Gmail, user input |

**Formatting rules:**
- Always use the actual company name — never "the customer" or "the client"
- People: `FirstName LastName (Role)` — include title for customer contacts
- All links must be embedded: `[Text](URL)` — no raw URLs in the body
- Numbers: use commas for thousands, include units and time periods
- Missing data: `[To be completed]` — never leave a section header with nothing below it

---

### Step 7: Choose Upload Destination

Before creating the Google Doc, ask the user where to save it using `AskUserQuestion`:

> "Where would you like the engagement report saved?
>
> **Option 1 (default):** 1 - In Draft Engagement Reports (the standard PS ER staging folder)
> **Option 2:** A different Google Drive folder — paste the folder URL or name"

If the user selects the default or doesn't specify, use:
- **Folder ID:** `1ti7npy1OVI4q5QGkubCrKnmHiPQeK8iA`

If the user provides a Google Drive folder URL, extract the folder ID from the URL pattern:
`https://drive.google.com/drive/folders/{FOLDER_ID}`

---

### Step 8: Create the Google Doc and Upload

First, write the report to a temp file:

```bash
cat > /tmp/engagement_report.md << 'EOF'
{the full report markdown generated in Step 6}
EOF
```

Then attempt the following approaches **in order**, moving to the next only if the current one fails:

#### Approach 1 (primary): markdown_to_gdocs.py + Drive API

Resolve the converter and auth scripts from the `fe-google-tools` marketplace installation:

```bash
GDOCS_CONVERTER=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py 2>/dev/null | sort -V | tail -1)
GAUTH=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | sort -V | tail -1)
```

If both scripts resolve successfully:

1. Convert to Google Doc:
```bash
python3 "$GDOCS_CONVERTER" \
  --input /tmp/engagement_report.md \
  --title "[DRAFT] - {CUSTOMER_NAME} - {PROJECT_NAME} - Engagement Report"
```

2. Move to the selected folder (get a fresh token — the converter may have consumed the previous one):
```bash
TOKEN=$(python3 "$GAUTH" token)
DOC_ID="{from converter output}"
FOLDER_ID="{from Step 7}"

curl -s -X PATCH \
  "https://www.googleapis.com/drive/v3/files/${DOC_ID}?addParents=${FOLDER_ID}&removeParents=root&supportsAllDrives=true" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json"
```

#### Approach 2 (fallback): Use an available Google skill or agent

If the scripts in Approach 1 cannot be found or fail, look through all installed skills and agents for one that can handle Google Doc creation or Drive upload. Candidates in priority order:

- **`fe-google-tools:google-docs`** skill — load it and follow its instructions to create the doc from the markdown content
- **`fe-google-tools:google-drive-upload`** skill — use it to upload `/tmp/engagement_report.md` as a Google Doc to the selected folder
- **`fe-google-tools:google-drive`** agent — invoke via Task tool to handle the full creation and placement

Load whichever is available and delegate the upload task to it, passing the temp file path, target title, and folder ID.

#### Approach 3 (last resort): Deliver the markdown

If no Google tools are available or all approaches fail, inform the user clearly:

> "I was unable to create the Google Doc automatically. Here is the full report as markdown — you can paste it into a new Google Doc manually, or let me know which tool to use."

Then output the full report markdown directly in the conversation so the user is never left empty-handed.

---

**On success**, return the document URL to the user:
`https://docs.google.com/document/d/{DOC_ID}/edit`

---

### Step 9: Quality Checklist

Before completing, verify:

- [ ] Read `ENGAGEMENT_REPORT_TEMPLATE.md` and `SECTION_GUIDANCE.md` before writing
- [ ] All 15 template sections are present — none are skipped
- [ ] Customer name used throughout — never "the customer"
- [ ] All team tables have full names and roles (not just titles)
- [ ] Executive summary is 3-4 sentences covering who/what/how/impact
- [ ] At least one specific metric in Accomplishments (number, %, growth rate)
- [ ] Each challenge includes both the problem and the resolution
- [ ] Product challenges reference Jira ticket links
- [ ] All links are embedded — no bare URLs
- [ ] Missing sections use `[To be completed]` — no empty sections
- [ ] Document title: `[DRAFT] - {Customer} - {Project} - Engagement Report`
- [ ] Document is in the folder the user selected

---

## Document Structure Reference

### External-Facing Sections
1. **Customer Name & Project Title**
2. **Team Tables** — Customer Stakeholders, Databricks Delivery Team, Partner Delivery Team, Databricks Account Team
3. **Executive Summary** (table format, 3-4 sentences)
4. **Project Objectives** (The Why)
5. **Implementation Details** (The What)
6. **Accomplishments / Highlights**
7. **Challenges Faced / Resolved**
8. **Potential Next Steps**

### Internal Learnings Section
9. **Metadata Table** — Author, FF Project ID, BU, Industry/Vertical, Project Duration, Primary Use Case, Partners, Delivery Materials link, Cloud
10. **Key Learnings / Lessons Learned**
11. **Databricks Products Used**
12. **Product Challenges / Gaps** (with Jira/Aha links)
13. **Assets Used to Assist with Delivery**
14. **Delivery Assets Improvement Opportunities**
15. **Customer Quotes**

---

## What Makes a Great Engagement Report

1. **Specific, measurable accomplishments** — numbers: tables migrated, % consumption growth, hours saved
2. **Honest challenge documentation** — real obstacles and exactly how they were resolved
3. **Concrete learnings** — actionable insights for future engagements, not generic observations
4. **Product feedback with links** — Jira and Aha references so feedback is trackable
5. **Customer quotes** — direct feedback that validates the engagement value
6. **Clear next steps** — specific follow-on work planned or recommended

---

## Output Folder Structure

```
PS Engagement Reports/
├── 1 - In Draft Engagement Reports     ← default destination
├── 2 - In Review Engagement Reports
└── 3 - Completed Engagement Reports
```

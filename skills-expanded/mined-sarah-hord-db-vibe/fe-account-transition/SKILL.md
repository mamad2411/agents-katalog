---
name: fe-account-transition
description: Create comprehensive account transition documents for new Account Executives and Solution Architects taking over accounts. Gathers data from Salesforce, Logfood, Glean, and JIRA.
user-invocable: true
---

# Account Transition Document Generator

Create comprehensive account transition documents for new Account Executives and Solution Architects taking over an account. These documents provide technical depth on production use cases, evaluation pipelines, and historical context to ensure smooth transitions.

## Prerequisites

Before running this skill, ensure the following are authenticated:
1. **Salesforce** - Run `/salesforce-authentication`
2. **Databricks** - Run `/databricks-authentication`
3. **Google** - Run `/google-auth`

**Python Dependencies for Consumption Visualization:**
The consumption analyzer script requires matplotlib and numpy:
```bash
pip install matplotlib>=3.8.0 numpy>=1.24.0
```

**CRITICAL: Reading Google Docs**
When you need to read any Google Doc URL (docs.google.com), you MUST use the `/google-docs` skill. **NEVER use fetch or WebFetch for Google Docs** - they will fail. The google-docs skill handles authentication and document access properly.

## Required Information

Ask the user for:
1. **Account Name** - The customer account name (e.g., "Block", "Square")
2. **Incoming AE** - Name and email of the new Account Executive
3. **Incoming SA** - Name and email of the new Solution Architect (if changing)
4. **Outgoing Team** - Names of departing team members (AE, SA, CSM if applicable)

## Data Gathering Workflow

### Step 1: Get Salesforce Account ID

```bash
sf data query --query "SELECT Id, Name FROM Account WHERE Name LIKE '%ACCOUNT_NAME%' LIMIT 5" --json
```

Note the Account ID (18-character ID starting with `001`).

### Step 2: Query Use Cases from Salesforce

```bash
sf data query --query "SELECT Id, Name, Stages__c, Implementation_Status__c, Account_Name__c FROM UseCase__c WHERE Account__c = 'ACCOUNT_ID' ORDER BY Stages__c DESC" --json
```

Categorize use cases by stage:
- **U6 (Production)** - Active in production
- **U5 (Onboarding)** - Being deployed
- **U4 (Confirming)** - Approved, awaiting deployment
- **U3 (Evaluating)** - In POC/evaluation
- **U2 (Scoping)** - Requirements being defined
- **U1 (Interest)** - Initial interest expressed
- **Lost/Disqualified** - Not proceeding

### Step 3: Query Consumption Data from Logfood

Use the `logfood-querier` skill to query internal consumption data. This skill uses the `logfood` profile which connects to the logfood workspace (`https://adb-2548836972759138.18.azuredatabricks.net/`).

**Important:** Ensure you are authenticated to the logfood workspace first:
```bash
databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood
```

Then use the `databricks-query` skill with the `logfood` profile:

```sql
-- Monthly consumption by SKU
SELECT
    usage_date,
    sku,
    SUM(dbu_dollars) as dbu_dollars,
    SUM(dbus) as dbus
FROM main.gtm_data.c360_consumption_monthly
WHERE account_id = 'SALESFORCE_ACCOUNT_ID'
AND usage_date >= DATE_ADD(CURRENT_DATE(), -12)
GROUP BY usage_date, sku
ORDER BY usage_date DESC, dbu_dollars DESC

-- Get all workspaces
SELECT DISTINCT
    workspace_id,
    workspace_name
FROM main.gtm_data.c360_consumption_monthly
WHERE account_id = 'SALESFORCE_ACCOUNT_ID'
AND usage_date >= DATE_ADD(CURRENT_DATE(), -3)
ORDER BY workspace_name
```

Execute queries using:
```bash
databricks api post /api/2.0/sql/statements/ --json='{"statement": "<SQL_QUERY>", "warehouse_id": "<WAREHOUSE_ID>", "format":"JSON_ARRAY", "wait_timeout":"50s"}' --profile=logfood
```

### Step 3b: Generate Consumption Trend Visualization

**IMPORTANT:** Always generate consumption trend visualization for accounts with consumption data.

Run the consumption analyzer script:

```bash
# Chart output path defaults to /tmp/consumption_trend_{account_id}.png to prevent collisions
python3 ~/.claude/plugins/cache/fe-vibe/fe-workflows/*/skills/fe-account-transition/resources/consumption_analyzer.py \
  --account-id "SALESFORCE_ACCOUNT_ID" \
  --format json > /tmp/consumption_analysis.json

# Output file will be at /tmp/consumption_trend_SALESFORCE_ACCOUNT_ID.png
```

The script outputs JSON with:
- `chart_path`: Path to generated chart image
- `analysis.velocity`: "Accelerating" | "Steady Growth" | "Plateauing" | "Declining"
- `analysis.avg_mom_growth`: Average month-over-month growth percentage
- `analysis.yoy_growth`: Year-over-year growth (compares current month to same month 12 months ago)
- `analysis.inflection_points`: Months with >30% change (POC launches, new use cases, churn events)
- `analysis.forecast_next_month`: Predicted next month consumption
- `analysis.health`: "Healthy" | "Stable" | "At Risk"

**Why 13 months?** The script analyzes 13 months by default (12-month cycle + 1 for YoY comparison) - this is industry best practice for consumption-based pricing. See [MostlyMetrics: TTM for Usage-Based SaaS](https://www.mostlymetrics.com/p/the-top-metrics-for-usage-based-saas) and [Gainsight: Customer Health Scores](https://www.gainsight.com/blog/customer-health-scores/).

**Parse the analysis:**
```bash
VELOCITY=$(jq -r '.analysis.velocity' /tmp/consumption_analysis.json)
YOY_GROWTH=$(jq -r '.analysis.yoy_growth' /tmp/consumption_analysis.json)
HEALTH=$(jq -r '.analysis.health' /tmp/consumption_analysis.json)
AVG_MOM=$(jq -r '.analysis.avg_mom_growth' /tmp/consumption_analysis.json)
```

**Add to document Section 8 (Consumption Analysis):**

If consumption data exists:
```markdown
### Monthly Consumption Trend (Last 12 Months)

![Consumption Trend](/tmp/consumption_trend_{account_id}.png)

**Trend Analysis:**
- **Velocity:** {VELOCITY}
- **YoY Growth:** {YOY_GROWTH}
- **Health:** {HEALTH}
- **Average MoM Growth:** {AVG_MOM}

**Inflection Points:**
{for each inflection_point}
- **{month}:** {change} — {spend} ({reason if detectable})
{end for}

**Forecast:** Next month estimated at ${forecast_next_month:,.0f}
```

**For zero-consumption accounts** (like Mayo Clinic):
```markdown
### Consumption Analysis

**Current State:** $0/month (trial accounts, PAYG, or early evaluation)

**Growth Potential:** Estimate based on:
- **Data volume:** {PB of data mentioned in discovery}
- **Developer count:** {number of data engineers/scientists}
- **Use case goals:** {e.g., "2,000+ AI agents"}
- **External sharing:** {e.g., "56M patient network via Delta Sharing"}

**Estimated Potential:** ${estimated_monthly_spend}/month at full deployment

**Basis:** Similar customers with comparable scale (reference accounts if available)
```

### Step 4: Search Glean for Documents and Context

Use the Glean MCP to find relevant documents:

```bash
# Search for account documents
mcp-cli call glean/glean_read_api_call '{
  "endpoint": "/search",
  "params": {
    "query": "ACCOUNT_NAME architecture strategy",
    "pageSize": 20
  }
}'

# Search for Slack channels
mcp-cli call glean/glean_read_api_call '{
  "endpoint": "/search",
  "params": {
    "query": "ext-ACCOUNT_NAME OR ext-u-ACCOUNT_NAME slack channel",
    "pageSize": 30
  }
}'

# Search for JIRA tickets
mcp-cli call glean/glean_read_api_call '{
  "endpoint": "/search",
  "params": {
    "query": "ACCOUNT_NAME site:databricks.atlassian.net",
    "pageSize": 20
  }
}'
```

**IMPORTANT: Reading Google Docs from Search Results**

When Glean returns Google Doc URLs (docs.google.com), you MUST use the `google-docs` skill to read them. **NEVER use fetch or WebFetch for Google Docs** - it will fail.

To read a Google Doc:
```
/google-docs
```
Then provide the Google Doc URL when prompted. The skill handles authentication and extracts the document content properly.

### Step 5: Query JIRA for Engineering Escalations

Use the `jira-actions` skill to find ES tickets:

```bash
sf data query --query "SELECT Id, Name, Jira_Ticket_Number__c, Status__c, Priority__c FROM JiraIssue__c WHERE Account__c = 'ACCOUNT_ID' ORDER BY CreatedDate DESC LIMIT 20" --json
```

### Step 6: Get Team Member Emails

For @ mentions to work as person chips, look up email addresses:

```bash
# Search Glean for person
mcp-cli call glean/glean_read_api_call '{
  "endpoint": "/search",
  "params": {
    "query": "PERSON_NAME",
    "datasource": "people"
  }
}'
```

## Document Structure

Create a markdown file with the following sections. The document MUST follow this exact format, especially the header section:

```markdown
# [Account Name] Account Transition Document

**Document Type:** Account Transition

**Prepared For:** @Incoming AE Name (Incoming Account Executive)

**Solution Architect:** @SA Name (Continuing)

**Date:** [Month Day, Year]

**Account Status:** ~$X.XM-$X.XM MRR | [Account Tier]

———

## Executive Summary
Brief overview (2-3 paragraphs) covering:
- Account relationship overview and strategic importance
- Current consumption and growth trajectory
- Key renewal/expansion opportunities
- Top priorities for the incoming team

———

## 1. Account Overview
### Company Profile

| Attribute | Value |
|-----------|-------|
| Industry | Industry |
| Employees | X,XXX |
| Headquarters | City, State |
| Founded | Year |
| Public/Private | Status |

### Business Units
**Unit Name** - Description of what this business unit does

### Key Metrics

| Metric | Value |
|--------|-------|
| Current MRR | $X.XM-$X.XM |
| Renewal Date | Month Year |
| Renewal Amount | $XX.XM |
| Production Use Cases (U6) | XX |
| YoY Growth | ~XXX% |

———

## 2. Databricks Team Contacts

| Role | Name | Status |
|------|------|--------|
| Account Executive | @Name | Incoming |
| Solutions Architect | @Name | Continuing |
| Customer Success Manager | @Name | Continuing |
| Regional Director | @Name | N/A |

———

## 3. [Account Name] Stakeholder Map

### Key Technical Teams
**Team Name** - Brief description of what they do and their relationship with Databricks

### Key Stakeholders
*To be completed by incoming team during introductory meetings*

| Name | Title | Role | Relationship | Notes |
|------|-------|------|--------------|-------|
| | | | | |
| | | | | |
| | | | | |

———

## 4. Production Use Cases (U6) - Selected Highlights

### GenAI & Model Serving

| Use Case | Status | Notes |
|----------|--------|-------|
| [Use Case Name](SALESFORCE_UCO_URL) | **Green** | Brief description |

### Data Platform & Lakehouse

| Use Case | Status | Notes |
|----------|--------|-------|
| [Use Case Name](SALESFORCE_UCO_URL) | **Green** | Brief description |

### ML & Feature Engineering

| Use Case | Status | Notes |
|----------|--------|-------|
| [Use Case Name](SALESFORCE_UCO_URL) | **Yellow** | Brief description |

———

## 5. Active Pipeline Use Cases (U1-U5)

### U5 - Onboarding (X)

| Use Case | Status | Notes |
|----------|--------|-------|
| [Use Case Name](SALESFORCE_UCO_URL) | **Green** | Expected production date |

### U4 - Confirming (X)

| Use Case | Status | Notes |
|----------|--------|-------|
| [Use Case Name](SALESFORCE_UCO_URL) | **Yellow** | Brief description |

### U2 - Scoping (X)

| Use Case | Status | Notes |
|----------|--------|-------|
| [Use Case Name](SALESFORCE_UCO_URL) | **Yellow** | Brief description |

### U1 - Interest (X)

| Use Case | Status | Notes |
|----------|--------|-------|
| [Use Case Name](SALESFORCE_UCO_URL) | **Yellow** | Brief description |

———

## 6. Paused/Lost Use Cases - Key Ones to Re-engage

| Use Case | Reason | Competitor | Re-engagement Opportunity |
|----------|--------|------------|---------------------------|
| [Use Case Name](SALESFORCE_UCO_URL) | Reason lost/paused | Competitor if any | Opportunity to re-engage |

**Key Insight:** Summary of patterns in lost use cases and lessons learned.

———

## 7. Engineering Escalations & Known Issues

### Active Issues

| Ticket | Summary | Priority | Status |
|--------|---------|----------|--------|
| [ES-XXXXX](JIRA_URL) | Brief summary | P1/P2/P3 | Status |

### Recent Resolved Issues

| Ticket | Summary | Resolution |
|--------|---------|------------|
| [ES-XXXXX](JIRA_URL) | Brief summary | How resolved |

### Product Asks & Feature Requests
**Feature Name** - Description and status/ETA if known

———

## 8. Consumption Analysis

### Current Status
| Metric | Value |
|--------|-------|
| Latest Month | {latest_month} |
| Latest Spend | ${latest_spend:,.2f} |
| Trend | {velocity} ({avg_mom_growth} avg MoM) |
| Health | {health_indicator} |

### Monthly Consumption Trend (Last 12 Months)

![Consumption Trend](/tmp/consumption_trend_{account_id}.png)

**Trend Analysis:**
- **Velocity:** {velocity}
- **YoY Growth:** {yoy_growth}
- **Health:** {health}
- **Average MoM Growth:** {avg_mom_growth}

**Inflection Points:**
- **{month}:** {change} — {spend} (POC launch / new use case / etc.)

**Forecast:** Next month estimated at ${forecast_next_month:,.0f}

### Top SKUs (Most Recent Month)

| SKU | Monthly Spend | % of Total |
|-----|---------------|------------|
| SKU Name | $XXX,XXX | XX% |

### Growth Trajectory
**H1 Year:** ~$X.XM/month average
**H2 Year:** ~$X.XM/month average
**YoY Growth:** ~XXX% consumption growth
**Key Driver:** What's driving growth

———

## 9. Key Documents & Resources

### Internal Documents
- [Document Name](URL) - Brief description
- [Document Name](URL) - Brief description

### Slack Channels
**External:**
- #ext-account-name - Customer-facing channel

**Internal:**
- #acct-account-name - Internal coordination
- go/account-support - Support instructions

———

*Document generated by Vibe on [DATE]*
```

## Creating the Google Doc

### Step 1: Save Markdown to Temp File

```bash
cat > /tmp/transition_doc.md << 'CONTENT'
[Your markdown content here]
CONTENT
```

### Step 2: Convert to Google Doc

Use the markdown_to_gdocs.py script from the google-docs skill:

```bash
# Use the markdown_to_gdocs.py script from the google-docs skill
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/transition_doc.md \
  --title "[Account Name] Account Transition Document"
```

This properly handles:
- Heading styles (H1, H2, H3)
- Bold and italic text
- Hyperlinks
- Tables
- Bullet lists

**Note on consumption chart images:** The markdown template references `/tmp/consumption_trend.png` as a local path. When creating the Google Doc, this image needs to be uploaded to Google Drive first. Use the `google-docs` skill's image upload capability or manually upload the chart to Drive and replace the path with the Drive image URL in the final document.

### Step 3: Post-Process for Person Chips and Status Colors

Create and run the post-processing script:

```python
#!/usr/bin/env python3
"""Fix @ mentions and add status colors to transition doc."""

import json
import subprocess
import urllib.request
import time

DOC_ID = "YOUR_DOC_ID"
QUOTA_PROJECT = "gcp-sandbox-field-eng"

# Map of @mentions to emails - CUSTOMIZE THIS
MENTION_TO_EMAIL = {
    "@Person Name": "person.name@databricks.com",
}

# Status colors
STATUS_COLORS = {
    "**Green**": {"red": 0.0, "green": 0.5, "blue": 0.0},
    "**Yellow**": {"red": 0.8, "green": 0.6, "blue": 0.0},
    "**Red**": {"red": 0.8, "green": 0.0, "blue": 0.0},
    "Green": {"red": 0.0, "green": 0.5, "blue": 0.0},
    "Yellow": {"red": 0.8, "green": 0.6, "blue": 0.0},
    "Red": {"red": 0.8, "green": 0.0, "blue": 0.0},
}

def get_token():
    result = subprocess.run(
        ["gcloud", "auth", "application-default", "print-access-token"],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def get_document():
    token = get_token()
    req = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{DOC_ID}",
        headers={"Authorization": f"Bearer {token}", "x-goog-user-project": QUOTA_PROJECT}
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def batch_update(requests):
    if not requests:
        return None
    token = get_token()
    data = json.dumps({"requests": requests}).encode('utf-8')
    req = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{DOC_ID}:batchUpdate",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "x-goog-user-project": QUOTA_PROJECT,
            "Content-Type": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"Error: {error_body}")
        return None

def find_text_in_document(doc, search_text):
    """Find all occurrences of text in document with their positions."""
    occurrences = []

    for element in doc.get('body', {}).get('content', []):
        if 'paragraph' in element:
            for text_elem in element['paragraph'].get('elements', []):
                if 'textRun' in text_elem:
                    content = text_elem['textRun'].get('content', '')
                    start_idx = text_elem['startIndex']

                    pos = 0
                    while True:
                        pos = content.find(search_text, pos)
                        if pos == -1:
                            break
                        occurrences.append({
                            'start': start_idx + pos,
                            'end': start_idx + pos + len(search_text),
                            'text': search_text
                        })
                        pos += 1

        # Also check table cells
        if 'table' in element:
            for row in element['table'].get('tableRows', []):
                for cell in row.get('tableCells', []):
                    for cell_content in cell.get('content', []):
                        if 'paragraph' in cell_content:
                            for text_elem in cell_content['paragraph'].get('elements', []):
                                if 'textRun' in text_elem:
                                    content = text_elem['textRun'].get('content', '')
                                    start_idx = text_elem['startIndex']

                                    pos = 0
                                    while True:
                                        pos = content.find(search_text, pos)
                                        if pos == -1:
                                            break
                                        occurrences.append({
                                            'start': start_idx + pos,
                                            'end': start_idx + pos + len(search_text),
                                            'text': search_text
                                        })
                                        pos += 1

    return occurrences

print("Fetching document...")
doc = get_document()

# Step 1: Apply status colors
print("Applying status colors...")
for status_text, color in STATUS_COLORS.items():
    occurrences = find_text_in_document(doc, status_text)
    if occurrences:
        requests = []
        for occ in occurrences:
            requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": occ['start'], "endIndex": occ['end']},
                    "textStyle": {
                        "foregroundColor": {"color": {"rgbColor": color}},
                        "bold": True
                    },
                    "fields": "foregroundColor,bold"
                }
            })

        for i in range(0, len(requests), 50):
            batch_update(requests[i:i+50])
        print(f"  Applied color to {len(occurrences)} instances of '{status_text}'")

# Re-fetch document after color changes
time.sleep(0.5)
doc = get_document()

# Step 2: Replace @mentions with person chips
print("\nReplacing @mentions with person chips...")

all_mentions = []
for mention_text, email in MENTION_TO_EMAIL.items():
    occurrences = find_text_in_document(doc, mention_text)
    for occ in occurrences:
        occ['email'] = email
        all_mentions.append(occ)

# Sort by start index descending (process in reverse order)
all_mentions.sort(key=lambda x: x['start'], reverse=True)

for mention in all_mentions:
    requests = [
        {
            "deleteContentRange": {
                "range": {
                    "startIndex": mention['start'],
                    "endIndex": mention['end']
                }
            }
        },
        {
            "insertPerson": {
                "personProperties": {
                    "email": mention['email']
                },
                "location": {"index": mention['start']}
            }
        }
    ]

    result = batch_update(requests)
    if result:
        print(f"  Replaced '{mention['text']}' with person chip for {mention['email']}")

    time.sleep(0.2)
    doc = get_document()

print(f"\nDocument updated: https://docs.google.com/document/d/{DOC_ID}/edit")
```

Save this as `/tmp/fix_transition_doc.py`, update `DOC_ID` and `MENTION_TO_EMAIL`, then run:

```bash
python3 /tmp/fix_transition_doc.py
```

## Output

The skill produces a fully formatted Google Doc with:

### Header Section
- Document type, prepared for (with person chip), SA (with person chip), date, account status
- Clear visual separation using horizontal rules (———)

### Content Formatting
- Proper heading hierarchy (H1 for title, H2 for sections, H3 for subsections)
- Clickable hyperlinks for Salesforce UCOs, JIRA tickets, and documents embedded in text
- Interactive person chips for all @ mentions (NOT plain text "@Name")
- Color-coded status indicators (Green/Yellow/Red) with appropriate colors
- Tables with properly formatted columns (no separate "Salesforce Link" column)

### Section Structure
- Executive Summary with account overview
- Account Overview with company profile and key metrics tables
- Single Databricks Team Contacts table with Status column
- Stakeholder Map with Key Technical Teams AND empty stakeholder table
- Production Use Cases (U6) grouped by category
- Active Pipeline Use Cases (U1-U5) with counts in headers
- Paused/Lost Use Cases with re-engagement insights
- Engineering Escalations (active, resolved, product asks)
- Consumption Analysis with trends and top SKUs
- Key Documents & Resources

### Footer
- "Document generated by Vibe on [DATE]" (always include "by Vibe")

Returns document URL to user.

## Tips for Best Results

### Document Header (CRITICAL)
The header section at the top of the document is essential. It MUST include:
- **Document Type:** Account Transition
- **Prepared For:** @Name (Incoming Account Executive) - must be a proper person chip
- **Solution Architect:** @Name (Continuing) - must be a proper person chip
- **Date:** Spelled out (e.g., "January 16, 2026")
- **Account Status:** MRR range and tier (e.g., "~$1.5M-2.2M MRR | Top 25 Account")

Use the horizontal rule (———) to separate major sections for visual clarity.

### Databricks Team Contacts
Use a SINGLE "Databricks Team Contacts" table (NOT separate "Continuing" and "Transition" sections). Include a Status column showing "Incoming", "Continuing", or "Outgoing".

### Stakeholder Map
The Stakeholder section MUST include:
1. **Key Technical Teams** - List the customer's technical teams with brief descriptions
2. **Empty Stakeholder Table** - Include a blank table with headers (Name, Title, Role, Relationship, Notes) for the incoming team to fill out during introductory meetings

### Use Case Tables
Use Case tables should have these columns:
| Use Case | Status | Notes |
- **Use Case**: Name with embedded hyperlink to Salesforce UCO record
- **Status**: Color-coded status (**Green**, **Yellow**, **Red**)
- **Notes**: Brief description or context

Do NOT include a separate "Salesforce Link" column - embed the link in the Use Case name.

### Comprehensive Glean Searches
Search for variations of the account name (e.g., "Block", "Square", "Cash App" for Block Inc.)

### Slack Channel Discovery
Search for patterns like:
- `ext-ACCOUNT`
- `ext-u-ACCOUNT`
- `#databricksXXXX` (account number)

### Use Case Categorization
Group U6 use cases by domain:
- GenAI & Model Serving
- Data Platform & Lakehouse
- ML & Feature Engineering
- ETL & Data Processing
- Analytics & BI

### Status Colors
Use consistent status indicators:
- **Green** - Healthy, on track
- **Yellow** - Needs attention, minor issues
- **Red** - At risk, major issues

### Document Footer
Always end with: `*Document generated by Vibe on [DATE]*` (include "by Vibe").

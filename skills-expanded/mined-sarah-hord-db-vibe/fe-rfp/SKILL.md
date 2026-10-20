---
name: fe-rfp
description: >
  Answer RFP (Request for Proposal) questions using the RFP Response Assistant.
  Use this skill when a user needs help responding to RFPs, vendor questionnaires,
  or technical capability assessments. Handles both product/technical questions and
  security/compliance (SQRC) questions. Supports single questions, batch CSV processing,
  and Google Sheets input (exports sheet to CSV automatically).
  Triggers on: "RFP", "request for proposal", "vendor questionnaire", "rfp response",
  "rfp question", "rfpbot", "rfp-assistant".
user-invocable: true
---

# RFP Response Assistant

This skill answers RFP questions using the Databricks RFP Response Assistant, a RAG-powered agent backed by curated knowledge sources including Databricks docs, product catalogs, blogs, and the SQRC security/compliance knowledge base.

**Announce at start:** "I'm using the fe-rfp skill to answer RFP questions using the RFP Response Assistant."

## Overview

The RFP Assistant classifies each question into one of two paths:

| Path | Trigger | Returns |
|------|---------|---------|
| **Product/Technical** | Feature, capability, architecture questions | Compliance degree, justification, products, source URLs |
| **SQRC** | Security, privacy, compliance, legal questions | SQRC matches with detailed answers and platform-specific details |

**Knowledge sources:**
- Databricks official documentation (AWS, Azure, GCP)
- Databricks product keyword catalog
- Open source docs (Spark, MLflow)
- Databricks blogs (last 2 years)
- SQRC security/compliance knowledge base (go/sqrc)

## Prerequisites

1. **Databricks authentication** - Run `/databricks-authentication` and authenticate with a profile that has access to the **E2 Demo West** workspace (`e2-demo-west.cloud.databricks.com`)
2. **VPN required** - Must be connected to the Databricks VPN
3. **Python 3.10+** - For running the API helper script

## Workflow

### Step 1: Authenticate

Verify you have a valid token for E2 Demo West:

```bash
databricks auth token -p e2-demo-west 2>/dev/null || databricks auth token -p DEFAULT 2>/dev/null
```

If not authenticated, run `/databricks-authentication` first and configure a profile with access to E2 Demo West.

### Step 2: Gather Information

Before calling the API, determine:

1. **The RFP question(s)** - What does the user need answered?
2. **Cloud provider** - `aws`, `azure`, or `gcp`
   - **Always ask the user which cloud the customer uses before processing.** Responses differ by cloud platform (e.g., security features, service names, architecture details), so this matters for accuracy.
   - Do NOT skip this step or default to a cloud. Ask the user explicitly if they haven't specified one.

### Step 3: Call the API

#### Single Question

For a single RFP question:

```bash
python3 resources/rfp_api.py --cloud aws "Does Databricks support role-based access control?"
```

#### Batch Processing from CSV

For multiple questions from a CSV file (must have a `question` column):

```bash
python3 resources/rfp_api.py --cloud azure --csv /path/to/questions.csv --output /tmp/rfp_responses.csv
```

#### Batch Processing from Google Sheets

If the user provides a Google Sheets URL or spreadsheet ID containing RFP questions:

1. **Extract the spreadsheet ID** from the URL. For `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`, the ID is the `SPREADSHEET_ID` portion.

2. **Identify the question column.** Ask the user which column contains the questions, or inspect the sheet headers to find it. Common names: `question`, `Question`, `RFP Question`, etc.

3. **Export the sheet data to CSV** using `gsheets_cli.sh`:

```bash
# Fetch all values from the sheet (adjust range as needed)
GSHEETS_CLI=~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-sheets/resources/gsheets_cli.sh
bash $GSHEETS_CLI get-values SPREADSHEET_ID "Sheet1!A:Z"
```

This returns a JSON array of arrays (rows). The first row is typically headers.

4. **Convert to CSV with a `question` column.** Write a short Python snippet to convert the JSON output to a CSV file that `rfp_api.py` expects:

```bash
bash $GSHEETS_CLI get-values SPREADSHEET_ID "Sheet1!A:Z" | python3 -c "
import csv, json, sys

rows = json.load(sys.stdin)
if not rows:
    print('Error: Sheet is empty', file=sys.stderr)
    sys.exit(1)

headers = [h.strip().lower() for h in rows[0]]

# Find the question column - look for common names
question_col = None
for name in ['question', 'rfp question', 'questions', 'rfp questions']:
    if name in headers:
        question_col = headers.index(name)
        break

if question_col is None:
    print(f'Available columns: {rows[0]}', file=sys.stderr)
    print('Error: No question column found. Specify which column contains the questions.', file=sys.stderr)
    sys.exit(1)

with open('/tmp/rfp_questions.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['question'])
    for row in rows[1:]:
        if question_col < len(row) and row[question_col].strip():
            writer.writerow([row[question_col].strip()])

count = sum(1 for row in rows[1:] if question_col < len(row) and row[question_col].strip())
print(f'Exported {count} questions to /tmp/rfp_questions.csv')
"
```

If the column name doesn't match automatically, adjust `question_col` to the correct index based on the user's input (0-indexed).

5. **Run the RFP API** on the exported CSV:

```bash
python3 resources/rfp_api.py --cloud aws --csv /tmp/rfp_questions.csv --output /tmp/rfp_responses.csv
```

**Google Auth prerequisite:** The user must be authenticated with Google (`/google-auth`) for the Sheets export to work.

#### Batch Processing from Inline Questions

For a few questions provided directly:

```bash
python3 resources/rfp_api.py --cloud aws \
  "Does Databricks support RBAC?" \
  "Describe your encryption at rest capabilities" \
  "What compliance certifications does Databricks hold?"
```

### Step 4: Interpret the Response

The API returns structured JSON. The helper script formats it as readable output.

#### Product/Technical Responses

The response includes:
- **Compliance Degree**: `Full Compliance`, `Partial Compliance`, or `Non-Compliance`
- **Justification**: Detailed explanation with Databricks product references
- **Products**: Official Databricks product names relevant to the answer
- **Sources**: Documentation URLs supporting the response

**Present the response to the user** in a clear format:

```
**Compliance:** Full Compliance

**Response:** Databricks supports role-based access control through Unity Catalog...

**Relevant Products:** Unity Catalog, Databricks SQL, Workspace Administration

**Sources:**
- https://docs.databricks.com/en/security/auth/access-control.html
```

#### SQRC (Security/Compliance) Responses

When the question is security/compliance related, the response includes:
- **Compliance Degree**: `Consult go/sqrc` (indicates human expert review recommended)
- **SQRC Matches**: Up to 3 matching Q&A pairs from the SQRC knowledge base, each with:
  - The matched SQRC question
  - Short and detailed answers
  - Platform-specific details
  - Link to the SQRC entry

**Present SQRC responses** with the matched answers and note that go/sqrc should be consulted for the authoritative response:

```
**Compliance:** Consult go/sqrc

**Best Matching SQRC Entry:**
Q: Is your organization HITRUST Certified?
A: Yes. Databricks has achieved HITRUST CSF certification...

**Source:** https://platform.sec.databricks.com/kb.html?...

> Note: For security/compliance questions, consult go/sqrc for the authoritative answer.
```

### Step 5: Format Output

#### For Single Questions
Present the formatted response directly in the conversation.

#### For Batch/CSV Results
1. The `--output` flag saves results to a CSV file
2. Summarize the results: total questions, compliance breakdown, any SQRC redirects
3. If the user wants a Google Doc, use the markdown converter pattern to create one

#### Creating a Google Doc from Results

If the user wants the RFP responses in a Google Doc:

1. Generate a markdown file from the responses:
```bash
python3 resources/rfp_api.py --cloud aws --csv /path/to/questions.csv --output-markdown /tmp/rfp_responses.md
```

2. Convert to Google Doc using the standard converter:
```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/rfp_responses.md \
  --title "RFP Response - [Customer Name]"
```

## CLI Reference

```bash
# Single question
python3 resources/rfp_api.py "Your RFP question here"

# Single question with cloud filter
python3 resources/rfp_api.py --cloud aws "Your RFP question here"

# Multiple questions
python3 resources/rfp_api.py --cloud azure "Question 1" "Question 2" "Question 3"

# Batch from CSV (must have 'question' column)
python3 resources/rfp_api.py --cloud gcp --csv /path/to/questions.csv --output /tmp/responses.csv

# Batch from CSV with markdown output
python3 resources/rfp_api.py --cloud aws --csv /path/to/questions.csv --output-markdown /tmp/responses.md

# Override Databricks profile
python3 resources/rfp_api.py --profile e2-demo-west "Your question here"

# Raw JSON output (for debugging)
python3 resources/rfp_api.py --raw "Your question here"
```

## Important Notes

1. **VPN required** - The E2 Demo West workspace requires Databricks VPN access
2. **Timeout** - Each question can take up to 150 seconds; batch processing uses parallel requests
3. **SQRC questions** - Security/compliance questions are routed to the SQRC knowledge base; always recommend consulting go/sqrc for authoritative answers
4. **Cloud parameter** - Providing a cloud provider improves response quality by filtering to relevant docs
5. **Rate limits** - The endpoint has scale-to-zero enabled; first request after inactivity may be slower

## Support

- **Slack:** [#rfp-assistant](https://databricks.enterprise.slack.com/archives/C088C94ABDH)
- **Owner:** Nuwan Ganganath M. A. (nuwan.ganganath.m.a@databricks.com)
- **Repo:** https://github.com/databricks-field-eng/rfp-assistant
- **Docs:** [go/rfp-assistant](https://databricks.atlassian.net/wiki/spaces/FE/pages/4671308274/RFP+Response+Assistant+go+rfpbot)

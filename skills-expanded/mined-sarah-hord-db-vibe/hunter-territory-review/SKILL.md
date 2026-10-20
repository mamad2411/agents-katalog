---
name: hunter-territory-review
description: Pull Salesforce state for a FINS hunter territory, read account strategy notes (Google Docs), map each account to the Hunter Playbook stage, and output a current state markdown + Google Doc. Use when an AE/SA pair wants a territory snapshot — account tiers, open opps, UCOs, key contacts, last activity, and recommended next actions per account.
user-invocable: true
---

# Hunter Territory Review

Compiles a full territory current state document for a FINS Hunter AE/SA pair. Pulls live Salesforce data across all territory accounts, reads any external account notes (Google Docs), and maps every account to its Hunter Playbook stage with a concrete next action.

**Output:** A markdown file written to the current working directory AND a Google Doc, both containing:
1. Territory overview summary
2. Scored account table (all accounts)
3. Per-account detail sections (contacts, UCOs, opps, signals)
4. Account notes deep dive (Google Doc sources)
5. Hunter Playbook stage mapping with next actions for each account

---

## Prerequisites

Ensure the following are authenticated before running. If any fail, the skill will prompt you to re-authenticate.

1. **Salesforce** — run `/salesforce-authentication` if needed
2. **Google** — run `/google-auth` if needed
3. **Configuration files** — First run creates user config directory at:
   - `~/.claude/plugins/cache/fe-vibe/fe-fins-hunter/playbook_doc_id.txt` — Google Doc ID for Hunter Playbook (editable)
   - `~/.claude/plugins/cache/fe-vibe/fe-fins-hunter/gdocs_writer_email.txt` — Team member email for shared Writer access (editable)

If you need to use a different playbook source, edit `playbook_doc_id.txt` and restart.

### Configuration Precedence

For inputs that can be saved locally (`gdocs_shared_writer_email`), the skill follows this precedence:

1. **User-provided value** — If passed as an input parameter, use that value
2. **Saved configuration** — If a saved config file exists, read and offer to reuse it (or prompt for change)
3. **Interactive prompt** — If no config file exists, ask the user and save the answer for future runs

This allows users to override saved values on any run while avoiding repetitive prompts.

---

## Required Inputs

Ask the user for the following at the start. Accept all in a single message if provided together.

| Field | Required | Description |
|-------|----------|-------------|
| `ae_name` | Required | Full name of Account Executive (e.g., "Matthew Haynor") |
| `ae_email` | Required | Email of Account Executive (e.g., "matthew.haynor@databricks.com") |
| `sa_name` | Required | Full name of Solutions Architect (e.g., "Anant Asthana") |
| `sa_email` | Required | Email of Solutions Architect (e.g., "anant.asthana@databricks.com") |
| `account_ids` | Yes | List of Salesforce Account IDs (18-char), OR path to Excel/CSV with an `Id` column |
| `account_notes_urls` | Optional | One or more Google Doc URLs containing account strategy notes |
| `output_dir` | Optional | Directory to write the markdown file (defaults to current working directory) |
| `gdocs_shared_writer_email` | Optional | Email of team member to grant Writer access. Precedence: (1) value passed as input, (2) saved in ~/.claude/plugins/cache/fe-vibe/fe-fins-hunter/gdocs_writer_email.txt, (3) prompt user. |

**If the user provides an Excel file path**, extract account IDs by reading the file with Python:
```bash
python3 -c "
import sys
try:
    import openpyxl
    wb = openpyxl.load_workbook('EXCEL_PATH', read_only=True, data_only=True)
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        for row in ws.iter_rows(values_only=True):
            for cell in row:
                val = str(cell) if cell else ''
                if len(val) == 18 and val.startswith('00'):
                    print(val)
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
" 2>/dev/null | sort -u
```

**Shared Writer Email Configuration:**
On first run, ask the user: "What is the email of the team member who should have Writer access to generated Google Docs?" Store the answer in `~/.claude/plugins/cache/fe-vibe/fe-fins-hunter/gdocs_writer_email.txt`. On subsequent runs, read this file and offer to reuse it or change it.

---

## Workflow

### Phase 1: Initialize Configuration Files

On first run, check and initialize user config directory:

**Create config directory if needed:**
```bash
mkdir -p "$HOME/.claude/plugins/cache/fe-vibe/fe-fins-hunter"
```

**Initialize playbook_doc_id.txt if missing:**

⚠️ **Playbook Document Ownership & Access**
- **Document Owner:** Anant Asthana (anant.asthana@databricks.com)
- **Current Doc ID:** 1EBwqCxc1GlIzNh8YanOL0KoMwkSHBv12kojaUoh5V9M (shared with FINS Hunter team)
- **If document becomes inaccessible:** The skill automatically falls back to the committed `HUNTER_PLAYBOOK_STAGES.md` file
- **To override playbook doc ID:** Edit `~/.claude/plugins/cache/fe-vibe/fe-fins-hunter/playbook_doc_id.txt` and paste a new Doc ID
- **To update for new document owner:** Contact Anant Asthana to transfer ownership and update this default ID

```bash
CONFIG_DIR="$HOME/.claude/plugins/cache/fe-vibe/fe-fins-hunter"
PLAYBOOK_ID_FILE="${CONFIG_DIR}/playbook_doc_id.txt"
DEFAULT_PLAYBOOK_ID="1EBwqCxc1GlIzNh8YanOL0KoMwkSHBv12kojaUoh5V9M"

if [ ! -f "$PLAYBOOK_ID_FILE" ]; then
    echo "$DEFAULT_PLAYBOOK_ID" > "$PLAYBOOK_ID_FILE"
    echo "✓ Initialized playbook doc config (can be overridden in ${PLAYBOOK_ID_FILE})"
fi

PLAYBOOK_DOC_ID=$(tr -d '\n' < "$PLAYBOOK_ID_FILE")
echo "✓ Using playbook doc ID from config"
export PLAYBOOK_DOC_ID
```

---

### Phase 2: Authentication Check

```bash
# Check Salesforce
sf org display --json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['result'].get('connectedStatus',''))"

# Check Google
python3 $HOME/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py status 2>/dev/null | grep "Status:"
```

If either is not connected, stop and prompt the user to run the relevant auth skill before continuing.

---

### Phase 3: Prompt for Writer Email (Optional)

Writer email is used to grant document access to the generated Google Doc. The skill can reuse a saved email from a previous run or prompt for a new one.

**Flow:**
- If the user specified `gdocs_shared_writer_email` in inputs, use that directly
- Otherwise, check if a saved writer email exists in `~/.claude/plugins/cache/fe-vibe/fe-fins-hunter/gdocs_writer_email.txt`
- If a saved email exists:
  - Display it to the user
  - Ask to confirm reuse or change it
  - If user chooses to change, prompt for new email and save it
- If no saved email exists:
  - Prompt user for writer email
  - Save it for future runs

The following bash block sets up variables for the skill flow:

```bash
WRITER_EMAIL_FILE="$HOME/.claude/plugins/cache/fe-vibe/fe-fins-hunter/gdocs_writer_email.txt"
SAVED_EMAIL=""

if [ -f "$WRITER_EMAIL_FILE" ]; then
  SAVED_EMAIL=$(tr -d '\n' < "$WRITER_EMAIL_FILE")
fi
```

### Phase 4: Collect AE/SA Information

Validate that AE and SA information has been provided:

```bash
# Map skill inputs (lowercase) to bash variables (uppercase)
# Skill inputs: ae_email, sa_email, ae_name, sa_name
AE_EMAIL="${ae_email}"
SA_EMAIL="${sa_email}"
AE_NAME="${ae_name}"
SA_NAME="${sa_name}"

# Check AE_EMAIL is provided
if [ -z "$AE_EMAIL" ]; then
    echo "❌ AE_EMAIL is required. Please provide the Account Executive email."
    exit 1
fi

# Validate AE email is Databricks-owned
if [[ ! $AE_EMAIL =~ @(databricks\.com|databrickslabs\.com)$ ]]; then
    echo "❌ AE email must be Databricks (@databricks.com or @databrickslabs.com): $AE_EMAIL"
    exit 1
fi

# Check SA_EMAIL is provided
if [ -z "$SA_EMAIL" ]; then
    echo "❌ SA_EMAIL is required. Please provide the Solutions Architect email."
    exit 1
fi

# Validate SA email is Databricks-owned
if [[ ! $SA_EMAIL =~ @(databricks\.com|databrickslabs\.com)$ ]]; then
    echo "❌ SA email must be Databricks (@databricks.com or @databrickslabs.com): $SA_EMAIL"
    exit 1
fi

# Validate names are non-empty
if [ -z "$AE_NAME" ]; then
  echo "❌ Error: AE Name cannot be empty" >&2
  exit 1
fi

if [ -z "$SA_NAME" ]; then
  echo "❌ Error: SA Name cannot be empty" >&2
  exit 1
fi

# Display validation success
echo "✓ AE: ${AE_NAME} (${AE_EMAIL})"
echo "✓ SA: ${SA_NAME} (${SA_EMAIL})"
```

---

### Phase 5: Pull Salesforce Data

Use the `fe-internal-tools:field-data-analyst` agent to run all queries in a single call. Pass all account IDs as a comma-separated list in IN clauses.

**Queries to run** (full templates in `resources/SOQL_TEMPLATES.md`):

1. **Account Summary** — Name, Owner, Type, AnnualRevenue, NumberOfEmployees, BillingCity, BillingState, Description
2. **Open Opportunities** — Name, StageName, Amount, CloseDate, Owner.Name, NextStep (IsClosed = false)
3. **UCOs** — Name, Stages__c, Implementation_Status__c, Use_Case_Description__c, Demand_Plan_Next_Steps__c, LastModifiedDate, CreatedDate
4. **Key Contacts** — Name, Title, Email, Phone, LastActivityDate (ORDER BY LastActivityDate DESC)
5. **Recent Tasks** — Subject, ActivityDate, Description, Owner.Name, Status, Type (LAST_N_DAYS:90)
6. **Recent Events** — Subject, ActivityDate, Owner.Name, Type, DurationInMinutes (LAST_N_DAYS:90)

**Instruct the field-data-analyst agent** to return complete, untruncated results for all queries organized by account. Save raw results to `[output_dir]/[ae_last_name]_territory_sf_raw.json` for reference.

---

### Phase 6: Read Account Notes (Google Docs)

For each URL in `account_notes_urls`:

```bash
TOKEN=$(python3 $HOME/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token)
DOC_ID=$(echo "DOC_URL" | grep -oP '(?<=/d/)[^/]+')
curl -s "https://docs.googleapis.com/v1/documents/${DOC_ID}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  | python3 -c "
import json, sys
try:
    doc = json.load(sys.stdin)
    for elem in doc.get('body',{}).get('content',[]):
        if 'paragraph' in elem:
            for e in elem['paragraph'].get('elements',[]):
                if 'textRun' in e:
                    print(e['textRun'].get('content',''), end='')
except Exception as e:
    print(f'⚠ Could not parse Google Doc response: {e}', file=sys.stderr)
    # Continue gracefully — log error but don't exit (matches error handling table)
"
```

Extract and organize:
- Recent status updates (look for date patterns: `M/D/YY`, `MM/DD/YY`, `Month DD, YYYY`)
- Stakeholder names and titles
- Use case details and blockers
- Next steps

---

### Phase 7: Fetch Hunter Playbook Content

Implementation uses curl with proper validation, falling back to committed reference file if fetch fails.

```bash
# Phase 7: Fetch Hunter Playbook from Google Doc using curl
# Fetch from Google Docs API with fallback to local reference file

# Helper function: use local playbook reference file
# Uses process-specific temp file name to avoid collision if multiple instances run concurrently
use_local_playbook_fallback() {
  PLAYBOOK_REF_FILE=$(find "$HOME/.claude/plugins/cache/fe-vibe/fe-fins-hunter" -name "HUNTER_PLAYBOOK_STAGES.md" -type f | head -1)
  if [ -f "$PLAYBOOK_REF_FILE" ]; then
    cp "$PLAYBOOK_REF_FILE" "/tmp/playbook_content_$$.txt" 2>/dev/null
  else
    echo "⚠ Warning: could not fetch playbook from Google Docs or fallback file" >&2
    exit 1
  fi
}

# Re-read playbook doc ID from config file (env vars don't persist across bash blocks in SKILL.md)
# Each bash block runs in an isolated subprocess, so exports from Phase 1 don't reach Phase 7
CONFIG_DIR="$HOME/.claude/plugins/cache/fe-vibe/fe-fins-hunter"
PLAYBOOK_ID_FILE="${CONFIG_DIR}/playbook_doc_id.txt"
if [ -f "$PLAYBOOK_ID_FILE" ]; then
  PLAYBOOK_DOC_ID=$(tr -d '\n' < "$PLAYBOOK_ID_FILE")
else
  PLAYBOOK_DOC_ID=""
fi

TOKEN=$(python3 $HOME/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token 2>/dev/null)

if [ -n "$TOKEN" ]; then
    curl -s "https://docs.googleapis.com/v1/documents/${PLAYBOOK_DOC_ID}" \
      -H "Authorization: Bearer $TOKEN" \
      -H "x-goog-user-project: gcp-sandbox-field-eng" \
      -o "/tmp/playbook_response_$$.json" 2>/dev/null

    # Validate response
    if python3 -c "
import json, sys
try:
    with open('/tmp/playbook_response_$$.json') as f:
        doc = json.load(f)
    if 'body' in doc and 'content' in doc['body']:
        sys.exit(0)
    else:
        sys.exit(1)
except Exception:
    sys.exit(1)
" 2>/dev/null; then
        # Extract content
        python3 -c "
import json, sys
try:
    with open('/tmp/playbook_response_$$.json') as f:
        doc = json.load(f)
    for elem in doc.get('body',{}).get('content',[]):
        if 'paragraph' in elem:
            for e in elem['paragraph'].get('elements',[]):
                if 'textRun' in e:
                    print(e['textRun'].get('content',''), end='')
except Exception as e:
    print(f'Error extracting playbook content: {e}', file=sys.stderr)
    sys.exit(1)
" > "/tmp/playbook_content_$$.txt"

        if [ -s "/tmp/playbook_content_$$.txt" ]; then
            echo "✓ Fetched Hunter Playbook from Google Doc"
        else
            echo "⚠ Google Doc fetch returned empty content — using local reference"
            use_local_playbook_fallback
        fi
    else
        echo "⚠ Could not fetch Hunter Playbook from Google Doc — using local reference"
        use_local_playbook_fallback
    fi
else
    echo "⚠ Could not authenticate with Google — using local reference"
    use_local_playbook_fallback
fi
```

**Error handling:** If the curl fetch fails for any reason (auth, missing document, API error), the bash script automatically falls back to the committed `HUNTER_PLAYBOOK_STAGES.md` reference file. This ensures the workflow continues without interruption.

---

### Phase 8: Apply Hunter Playbook Stage Classification

Use the fetched playbook content (or fallback reference) to classify each account and determine next actions. Use the classification table at the top of the playbook file to assign:
- The **stage** (Pre-Discovery, Discovery, Workshop/POC, etc.)
- The **recommended next action** (specific, concrete — not generic)
- The **primary tool or resource** from `resources/HUNTER_PLAYBOOK_RESOURCES.md`

---

### Phase 9: Compile Current State Document

Write the markdown output to: `[output_dir]/[ae_last_name]_fy[YY]_territory_current_state_[YYYY-MM-DD].md`

Example: `haynor_fy27_territory_current_state_2026-03-03.md`

Follow the document structure in `resources/OUTPUT_TEMPLATE.md`. Key sections:

1. **Header** — AE, SA, date, total accounts, segment
2. **Territory Overview** — key themes, strategic signals, open pipeline summary
3. **Account Scored Table** — all accounts with tier, score, cloud, employees, open opp, UCO stage, last activity, key signal
4. **Tier 1 Account Details** — full section per account: SF data, key contacts (with emails), UCO history + next steps, recent activity, strategic signal, **recommended action**
5. **Tier 2 Account Details** — same structure, slightly condensed
6. **Tier 3 Account Details** — brief bullets only
7. **Account Notes Deep Dive** — full extracted content from Google Docs, organized by account, filtered to notes from the last 90 days
8. **Cross-Territory Strategic Signals** — competitive displacement opps (Snowflake, Azure, legacy on-prem), dark accounts, high-contact/no-UCO accounts
9. **Hunter Playbook Stage Mapping** — table mapping each account to playbook stage with next action and tools/resources

**IMPORTANT:** Write the markdown to the output directory directly — NOT to `/tmp`. This lets the user view and edit the source file alongside the Google Doc.

---

### Phase 10: Convert to Google Doc

```bash
python3 $HOME/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input "[output_dir]/[filename].md" \
  --title "[AE Last Name] FY[YY] Territory — Current State ([Month YYYY])"
```

Capture the returned `documentId` and `url`.

**Grant Shared Writer Access with Databricks Domain Validation:**

If `gdocs_shared_writer_email` was provided (or loaded from local config):

```bash
TOKEN=$(python3 $HOME/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token)
GDOCS_ID="<document_id_from_markdown_to_gdocs>"
WRITER_EMAIL="<gdocs_shared_writer_email>"

# Validate Databricks domain
if [[ ! $WRITER_EMAIL =~ @(databricks\.com|databrickslabs\.com)$ ]]; then
    echo "❌ Cannot grant permissions to non-Databricks email: $WRITER_EMAIL"
    echo "Writer email must be @databricks.com or @databrickslabs.com"
    exit 1
fi
echo "✓ Email validation passed: $WRITER_EMAIL is Databricks-owned"

# Grant with error handling
HTTP_CODE=$(curl -s -X POST "https://www.googleapis.com/drive/v3/files/${GDOCS_ID}/permissions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d "{
    \"role\": \"writer\",
    \"type\": \"user\",
    \"emailAddress\": \"${WRITER_EMAIL}\"
  }" \
  -w "%{http_code}" -o "/tmp/perms_response_$$.json")

if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ Granted Writer access to $WRITER_EMAIL"
else
    RESPONSE=$(cat "/tmp/perms_response_$$.json")
    echo "⚠ Could not grant Writer access. HTTP $HTTP_CODE"
    echo "Response: $RESPONSE"
fi
```

---

### Phase 11: Confirm Output

Print a clean summary:

```
Territory review complete for [AE_NAME] / [SA_NAME]

Accounts reviewed: [N]
Open opportunities: [N]
Active UCOs: [N]
Accounts with zero SF activity: [N]

Markdown saved: [full path to .md file]
Google Doc: [URL]
Shared with: [SHARED_WRITER_EMAIL] (Writer)
```

---

## Playbook Stage Classification Logic

Use this logic when mapping each account to a playbook stage. Full stage definitions are in `resources/HUNTER_PLAYBOOK_STAGES.md`.

| Condition (check in order) | Stage | Recommended Tool |
|---------------------------|-------|-----------------|
| 0 contacts in SF AND 0 UCOs | **Pre-Discovery** | External research, LinkedIn, add contacts to SF |
| Contacts exist but 0 UCOs AND no recent tasks (90d) | **Discovery** | go/discoveryguides, go/perplexityprompts |
| UCOs exist but all Lost/Disqualified AND no activity in 90d | **Discovery Re-entry** | Re-engage new contact, updated pitch |
| Active tasks/events in 90d OR open UCO U1–U2 | **Discovery (Active)** | go/discoveryguides, go/perplexityprompts |
| UCO at U3 (Evaluating) OR open opportunity at Validate/Qualify | **Workshop / POC** | go/launchaccelerator (Jumpstart), go/sts |
| UCO at U3–U4 with active POC in progress | **POC (In Progress)** | go/launchaccelerator, STS support |
| POC complete OR opportunity at Proposal/Negotiate | **Commit / Proposal** | Ignition Package ($15–25K small), go/proposal (larger) |
| Signed deal / U5–U6 | **Onboarding / Expansion** | CSM handoff, go/expandaccelerator |

---

## Key SOQL Field Notes

- UCO stage field: `Stages__c` — values: `Lost`, `Disqualified`, `Interest (U1)`, `Scoping (U2)`, `Evaluating (U3)`, `Confirming (U4)`, `Onboarding (U5)`, `Producing (U6)`
- UCO next steps: `Demand_Plan_Next_Steps__c`
- UCO description: `Use_Case_Description__c`
- If a field returns an error (not on object), fall back gracefully and note it — do not abort

---

## Error Handling

| Error | Action |
|-------|--------|
| SF not authenticated | Stop, prompt: "Run `/salesforce-authentication` first" |
| Google not authenticated | Stop, prompt: "Run `/google-auth` first" |
| Account ID not found in SF | Note as "Not found in SF" in output, continue |
| Google Doc URL inaccessible | Note as "Could not read [URL]" in output, continue |
| Excel/CSV parse failure | Ask user to paste account IDs directly |
| Playbook Google Doc unavailable | Use committed `HUNTER_PLAYBOOK_STAGES.md`, display "Using local Hunter Playbook reference" |

---

## Example Invocation

```
User: /hunter-territory-review

Agent: Hunter Territory Review

Who is the AE and SA for this territory?
What are the Salesforce account IDs, or do you have an Excel file I should read?
Any Google Doc URLs with account notes?
What is the email of the team member who should have Writer access to the generated Google Doc?

User: AE is Matthew Haynor, SA is Anant Asthana.
      Excel: /Users/anant.asthana/projects/2026_accounts/Haynor FY 27 Territory.xlsx
      Google Doc: https://docs.google.com/document/d/1tJMhvCdwFsOgqx5ADunjMckGkEAsWsUiQjlfGYXoZck/edit
      Shared Writer: ralph.laite@databricks.com

Agent: Checking auth...
       Reading account IDs from Excel...
       Pulling Salesforce data for 16 accounts...
       Reading Citizens Bank Google Doc...
       Fetching Hunter Playbook from Google Doc...
       Compiling current state document...
       Creating Google Doc...
       Granting Writer access...

       Territory review complete for Matthew Haynor / Anant Asthana

       Accounts reviewed: 16
       Open opportunities: 1 (Citizens Bank - POC, Proposal)
       Active UCOs: 2
       Accounts with zero SF activity: 2 (Home Bancshares, NY Commercial Bank)

       Markdown saved: /Users/anant.asthana/projects/2026_accounts/haynor_fy27_territory_current_state_2026-03-03.md
       Google Doc: https://docs.google.com/document/d/...
       Shared with: ralph.laite@databricks.com (Writer)
```

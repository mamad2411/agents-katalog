---
name: lean-sigma-fmea
description: Generates a Lean Six Sigma FMEA (Failure Mode and Effects Analysis) risk table for a data platform process or pipeline. Creates a Google Sheet with Severity/Occurrence/Detection scoring, auto-calculated RPN, and Databricks Well-Architected Framework recommendations. Use when assessing operational risk, preparing for a customer go-live, or hardening a data platform design.
user-invocable: true
---

# FMEA Generator

Produces a **FMEA (Failure Mode and Effects Analysis)** artifact following the DMAIC Improve-phase standard. Takes process steps (from a SIPOC or user input) and generates a prioritized risk table with RPN scores, Databricks-specific failure modes, and Well-Architected Framework remediation guidance.

FMEA answers: **What could go wrong? How bad would it be? How likely? Would we catch it in time?**

The output is a Google Sheet with:
- Full 17-column FMEA table
- Auto-calculated RPN (= Severity × Occurrence × Detection)
- Conditional formatting: Red (RPN ≥ 200), Orange (100–199), Yellow (50–99), Green (<50)
- Severity ≥ 9 items flagged regardless of RPN
- WA pillar tags per failure mode
- Recommended actions with Databricks-specific remediation

---

## Quick Start

User examples that trigger this skill:
```
"Run a FMEA on the data ingestion pipeline"
"FMEA for our Unity Catalog migration"
"What are the failure risks for this process?"
"Risk assessment for the customer's ML pipeline"
"FMEA based on this SIPOC"
```

---

## Workflow

### Phase 1 — Gather Process Steps

**Option A: Use an existing SIPOC**
If the user has run `/lean-sigma-sipoc`, ask for the Google Sheet URL or use the process steps from the current conversation. Read the Process column from the SIPOC sheet.

**Option B: Gather from user**
Ask:
1. What are the main process steps? (4–10 steps)
2. What is the process purpose and criticality?
3. Who are the key stakeholders / customers of this process?
4. Are there any known issues or past incidents?

**Option C: Infer from context**
If a Salesforce account, Slack thread, or prior conversation describes the process, extract the steps from there.

---

### Phase 2 — Generate Failure Modes per Process Step

For each process step, brainstorm failure modes using the taxonomy in `resources/databricks_failure_modes.md`. Apply these principles:

**Rules for identifying failure modes:**
- A failure mode is how the step **fails to deliver its function** (not why it fails — that is the cause)
- Use plain language: "Data not delivered on time", "Schema validation fails", "Model predictions are stale"
- Each step should have 2–5 failure modes (more is fine for high-risk steps)
- Consider both **partial failures** (degraded performance) and **complete failures** (process stops)

**Lean Six Sigma failure categories to probe:**
- Quality failures (wrong data, bad data, missing data)
- Timeliness failures (late, SLA miss, stale)
- Availability failures (process down, service unreachable)
- Security failures (unauthorized access, data exposure)
- Cost failures (runaway spend, wasted compute)
- Governance failures (lineage broken, audit gap, policy violation)

---

### Phase 3 — Score Each Failure Mode

Use the rating scales in `resources/rating_scales.md` to assign:

| Rating | Scale | Description |
|--------|-------|-------------|
| **Severity (S)** | 1–10 | How bad is the impact on the customer/business if this failure occurs? |
| **Occurrence (O)** | 1–10 | How likely is this failure to occur without additional controls? |
| **Detection (D)** | 1–10 | How likely is it that existing controls would NOT detect this failure before it reaches customers? |

**RPN = S × O × D** (Range: 1–1,000)

**Special rule:** Any item with **Severity ≥ 9** requires immediate attention regardless of RPN. Flag these with a "⚠️ HIGH SEV" marker.

**Scoring guidance by WA pillar:**

| WA Pillar | Typical Severity Range | Occurrence Guidance | Detection Guidance |
|-----------|----------------------|--------------------|--------------------|
| GOV (Governance) | 7–10 (compliance risk) | Low if Unity Catalog in place | Often invisible without audit logs |
| OPS (Operational) | 4–7 (process impact) | Moderate | Moderate (depends on monitoring) |
| SEC (Security) | 8–10 (breach risk) | Low-Moderate | Very hard to detect (D=7–10) |
| REL (Reliability) | 5–9 (SLA impact) | Moderate | Moderate (alerting varies) |
| PERF (Performance) | 3–7 (degraded UX) | Moderate-High | Often detected by users |
| COST (Cost) | 3–6 (financial waste) | Moderate | Easy if cost alerts in place |
| INT (Interoperability) | 4–7 (consumer impact) | Low-Moderate | Detected at consumption time |

---

### Phase 4 — Build FMEA Table

#### Standard 17-Column FMEA Schema

| # | Column Name | Description |
|---|------------|-------------|
| 1 | **Process Step** | From SIPOC or user input |
| 2 | **Potential Failure Mode** | How the step fails |
| 3 | **Potential Effect(s) of Failure** | Impact on customers/downstream |
| 4 | **Severity (S)** | 1–10 |
| 5 | **Potential Cause(s) of Failure** | Root cause(s) — why it happens |
| 6 | **Occurrence (O)** | 1–10 |
| 7 | **Current Process Controls** | What's in place today |
| 8 | **Detection (D)** | 1–10 |
| 9 | **RPN** | =S×O×D (formula) |
| 10 | **WA Pillar** | GOV / OPS / SEC / REL / PERF / COST / INT |
| 11 | **Recommended Action** | Databricks-specific remediation |
| 12 | **Responsible Party** | Team or role |
| 13 | **Target Date** | Completion target |
| 14 | **Actions Taken** | What was done |
| 15 | **Revised Severity (S')** | After remediation |
| 16 | **Revised Occurrence (O')** | After remediation |
| 17 | **Revised Detection (D')** | After remediation |
| 18 | **Revised RPN** | =S'×O'×D' (formula) |

---

### Phase 5 — Create Google Sheet

Use the `google-sheets` skill. Authenticate first:

```bash
TOKEN=$(python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token)
```

Create a spreadsheet with **three sheets**:

**Sheet 1: "FMEA"** — Main artifact

Header row formatting:
- Background: `#1A3A5C` (dark navy), white bold 11pt text
- Freeze row 1 — see API pattern below for correct method
- Column widths: Process Step (180), Failure Mode (220), Effects (200), S/O/D (60 each), RPN (70), WA Pillar (100), Recommended Action (250), other columns (160)

Conditional formatting on **RPN column (I)**:
```
≥ 200  → Background: #C62828 (dark red),   text: white   [Critical]
100–199 → Background: #EF6C00 (orange),    text: white   [High]
50–99  → Background: #F9A825 (yellow),     text: black   [Medium]
<50    → Background: #2E7D32 (green),      text: white   [Low]
```

Conditional formatting on **Severity (S) column**:
```
≥ 9    → Background: #880E4F (dark magenta), text: white  [⚠️ Immediate Action]
```

RPN formula in column I (example for row 2):
```
=IF(AND(D2<>"",F2<>"",H2<>""),D2*F2*H2,"")
```

Revised RPN formula in column R (example for row 2):
```
=IF(AND(O2<>"",P2<>"",Q2<>""),O2*P2*Q2,"")
```

**Sheet 2: "RPN Summary"** — Prioritized view

Create a sorted copy of the FMEA filtered to RPN ≥ 50, sorted descending by RPN. Add a bar chart of Top 10 RPN items.

**Sheet 3: "Action Tracker"** — Status dashboard

Columns: Process Step | Failure Mode | RPN | Recommended Action | Owner | Status (Open/In Progress/Closed) | Due Date | Notes

Pre-populate with all items where RPN ≥ 100 or Severity ≥ 9.

#### API patterns (tested and working):

```bash
# 1. Create the spreadsheet with all three sheets
SPREADSHEET=$(curl -s -X POST \
  "https://sheets.googleapis.com/v4/spreadsheets" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {"title": "FMEA - [Process] - [Customer]"},
    "sheets": [
      {"properties": {"title": "FMEA", "index": 0}},
      {"properties": {"title": "RPN Summary", "index": 1}},
      {"properties": {"title": "Action Tracker", "index": 2}}
    ]
  }')
SHEET_ID=$(echo $SPREADSHEET | python3 -c "import sys,json; print(json.load(sys.stdin)['spreadsheetId'])")

# Get tab IDs for all sheets (required for formatting/freeze calls)
SHEETS_META=$(curl -s "https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}?fields=sheets.properties" \
  -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: gcp-sandbox-field-eng")
FMEA_TAB_ID=$(echo $SHEETS_META | python3 -c "
import sys,json; sheets=json.load(sys.stdin)['sheets']
print([s['properties']['sheetId'] for s in sheets if s['properties']['title']=='FMEA'][0])")
SUMMARY_TAB_ID=$(echo $SHEETS_META | python3 -c "
import sys,json; sheets=json.load(sys.stdin)['sheets']
print([s['properties']['sheetId'] for s in sheets if s['properties']['title']=='RPN Summary'][0])")
TRACKER_TAB_ID=$(echo $SHEETS_META | python3 -c "
import sys,json; sheets=json.load(sys.stdin)['sheets']
print([s['properties']['sheetId'] for s in sheets if s['properties']['title']=='Action Tracker'][0])")

# 2. IMPORTANT: Expand secondary sheets before writing — new sheets have a small default
#    row count and writes will fail with an "out of range" error without this step.
curl -s -X POST "https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}:batchUpdate" \
  -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d "{\"requests\": [
    {\"appendDimension\": {\"sheetId\": $SUMMARY_TAB_ID, \"dimension\": \"ROWS\", \"length\": 50}},
    {\"appendDimension\": {\"sheetId\": $TRACKER_TAB_ID, \"dimension\": \"ROWS\", \"length\": 50}}
  ]}"

# 3. Freeze header row on all sheets — use updateSheetProperties, NOT "frozenRowCount" key
curl -s -X POST "https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}:batchUpdate" \
  -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d "{\"requests\": [
    {\"updateSheetProperties\": {
      \"properties\": {\"sheetId\": $FMEA_TAB_ID, \"gridProperties\": {\"frozenRowCount\": 1}},
      \"fields\": \"gridProperties.frozenRowCount\"
    }},
    {\"updateSheetProperties\": {
      \"properties\": {\"sheetId\": $SUMMARY_TAB_ID, \"gridProperties\": {\"frozenRowCount\": 1}},
      \"fields\": \"gridProperties.frozenRowCount\"
    }},
    {\"updateSheetProperties\": {
      \"properties\": {\"sheetId\": $TRACKER_TAB_ID, \"gridProperties\": {\"frozenRowCount\": 1}},
      \"fields\": \"gridProperties.frozenRowCount\"
    }}
  ]}"

# 4. Apply conditional formatting on RPN (col I) and Severity (col D)
#    CRITICAL: When using Python heredocs, use quoted PYEOF and pass shell vars as arguments
#    to prevent shell from expanding $I2 / $D2 formula references to empty strings.
python3 - "$TOKEN" "$SHEET_ID" "$FMEA_TAB_ID" << 'PYEOF'
import json, urllib.request, sys
TOKEN, SHEET_ID, FMEA_TAB_ID = sys.argv[1], sys.argv[2], int(sys.argv[3])
def api(payload):
    req = urllib.request.Request(
        f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}:batchUpdate",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {TOKEN}", "x-goog-user-project": "gcp-sandbox-field-eng", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp: return json.loads(resp.read())
def rgb(h):
    h=h.lstrip('#'); return {"red":int(h[0:2],16)/255,"green":int(h[2:4],16)/255,"blue":int(h[4:6],16)/255}
rpn = {"sheetId":FMEA_TAB_ID,"startRowIndex":1,"endRowIndex":100,"startColumnIndex":8,"endColumnIndex":9}
sev = {"sheetId":FMEA_TAB_ID,"startRowIndex":1,"endRowIndex":100,"startColumnIndex":3,"endColumnIndex":4}
rules = [
    (rpn, "=$I2>=200",           rgb("C62828"), {"red":1,"green":1,"blue":1}),
    (rpn, "=AND($I2>=100,$I2<200)", rgb("EF6C00"), {"red":1,"green":1,"blue":1}),
    (rpn, "=AND($I2>=50,$I2<100)",  rgb("F9A825"), {"red":0,"green":0,"blue":0}),
    (rpn, "=$I2<50",             rgb("2E7D32"), {"red":1,"green":1,"blue":1}),
    (sev, "=$D2>=9",             rgb("880E4F"), {"red":1,"green":1,"blue":1}),
]
reqs = [{"addConditionalFormatRule":{"rule":{"ranges":[rng],"booleanRule":{
    "condition":{"type":"CUSTOM_FORMULA","values":[{"userEnteredValue":f}]},
    "format":{"backgroundColor":bg,"textFormat":{"foregroundColor":fg,"bold":True}}}},"index":i}}
    for i,(rng,f,bg,fg) in enumerate(rules)]
r = api({"requests": reqs})
print("CF rules:", len(r.get("replies",[])))
PYEOF

# 5. Write FMEA header row
curl -s -X POST \
  "https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values:batchUpdate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{
    "valueInputOption": "USER_ENTERED",
    "data": [{
      "range": "FMEA!A1:R1",
      "values": [["Process Step","Potential Failure Mode","Potential Effect(s)","S","Potential Cause(s)","O","Current Controls","D","RPN","WA Pillar","Recommended Action","Responsible Party","Target Date","Actions Taken","S'\''","O'\''","D'\''","Revised RPN"]]
    }]
  }'
```

---

### Phase 6 — Deliver Outputs

1. **Google Sheet URL** — "Here is your FMEA: [link]"
2. **Top risks summary** — Present the top 5 RPN items and any Severity ≥ 9 items:
   ```
   ## Top FMEA Findings

   ⚠️ Critical Items (RPN ≥ 200 or Severity ≥ 9):
   1. [Process Step] — [Failure Mode] — RPN: [N] — [Recommended Action]
   ...

   📊 Risk Distribution:
   - Critical (RPN ≥ 200): N items
   - High (100–199): N items
   - Medium (50–99): N items
   - Low (<50): N items
   ```
3. **WA gap summary** — Which pillars have the most failures:
   - "Security has 4 high-severity items — recommend prioritizing Unity Catalog access control review"
4. **Suggested next steps**:
   - "Run `/lean-sigma-process-map` to visualize the process flow and highlight waste"
   - "Schedule a remediation review with the team for items with RPN ≥ 100"

---

## FMEA → Process Map Handoff

After completing the FMEA, offer to create a process map:

> "Your FMEA identified high-risk steps. Would you like me to create a swimlane process map that visualizes the flow and highlights these risk points? Use `/lean-sigma-process-map` or say 'map this process'."

---

## Resources

- `resources/rating_scales.md` — Complete Severity, Occurrence, Detection 1–10 scale definitions
- `resources/databricks_failure_modes.md` — Pre-built failure mode library organized by WA pillar

---

## Do NOT

- Score Severity, Occurrence, or Detection without justification — briefly note the rationale in the Potential Causes and Effects columns
- Leave RPN ≥ 200 items without a Recommended Action
- Ignore Severity ≥ 9 items even if RPN is low — these always need attention
- Mark Controls as "None" without confirming this with the user — there may be informal controls in place
- Create more than 5 failure modes per process step for a first pass — focus on the most realistic and impactful

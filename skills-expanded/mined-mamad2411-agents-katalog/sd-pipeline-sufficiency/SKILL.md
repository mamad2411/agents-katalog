---
name: sd-pipeline-sufficiency
description: Use when asked "do we have enough pipeline to hit target", "pipeline sufficiency for [director]", "can we make target next quarter", "U2–U5 pipeline coverage", "pipeline check for [director name]", or "pipeline report for [director]". Covers sales director teams with AE-level drill-down, UCO momentum scoring, U1/U2 pipeline accelerators, U5 go-live management, and full FY (current + next 3 quarters) verdict.
---

# SD Pipeline Sufficiency

**Purpose:** Answer *"Does [Sales Director]'s team have enough U2–U5 pipeline to hit consumption targets for the current and next 3 fiscal quarters (full FY view)?"*

**Output:** Google Doc (full report) + Slack DM to director and FE manager with summary + actions.

**Execution order:** Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5

---

## ⚠️ Pre-execution

If no sales director was specified, **stop and ask:** *"Which sales director should I run this for? Provide full name or Databricks email."*

Set `[Director Name]` and `[Director Email]` as variables used throughout. **Multiple directors:** comma-separate — run one full analysis per director, one Google Doc per director.

---

## ⚠️ CRITICAL: Verified schema notes (do not skip)

These were validated against live Logfood data. Deviating from them will cause silent failures.

### rpt_individual_obt_gtm
- **Date filter:** Use `quarter_type = 'Current Qtr'` — **not** fiscal year/quarter columns, not `processDate` (this column does not exist in this table).
- **AE filter:** Use `user_id` — **not** `sfdc_user_id` (does not exist).
- **Target columns:** `target_dbu_dollars` (Qcur), `target_dbu_dollars_quarter_plus_one` (Qnxt1), `target_dbu_dollars_quarter_plus_two` (Qnxt2), `target_dbu_dollars_quarter_plus_three` (Qnxt3).
- **Trajectory:** `forecast_straight_line_t28d_quarterly` — available for current quarter only. Sum across all AEs for team total.
- **Manager filter:** `manager_email = '[director_email]'` — returns direct reports only (correct scope).

### sfdc_bronze.accountteammember
- This is a **historical append table** — one row per record per day. Must filter to latest snapshot with `processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.accountteammember)` or queries return thousands of duplicate rows.
- Use `GROUP BY AccountId, UserId` or `QUALIFY ROW_NUMBER() OVER (PARTITION BY AccountId ORDER BY processDate DESC) = 1` to deduplicate.

### sfdc_bronze.account
- **Account name column:** `DeployableAccountName__c` — the `Name` column does not resolve in Databricks SQL when the table is joined or queried directly. `Headquarter_Business_Name__c` is usually null. `DeployableAccountName__c` is reliable.
- Also a historical table — filter with `processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)` when joining.

### sfdc_bronze.usecase__c
- Also historical — filter with `processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)`.
- **Salesforce relationship syntax (`Account__r.Name`) does not work** — join to account table explicitly.
- `NextSteps__c` is empty for all EMEA UCOs. Use **`Demand_Plan_Next_Steps__c`** as the primary next-steps signal.

### Account→AE mapping for Hunter/Geo AEs
- Hunter AEs may have very few or no entries in `accountteammember` (role = 'Account Executive'). **Fallback:** supplement with `sfdc_bronze.account.OwnerId` to cover all owned accounts.
- Always use latest processDate snapshot for both tables.

---

## Phase 0: Identity & org resolution

### 0a — FE Manager identity

Load `~/.vibe/profile`. Extract:
- `[FE Manager Name]`, `[FE Manager Email]`, `[FE Manager Slack]`

If profile missing → ask for name and email. Skip Slack DM; print to terminal instead.

### 0b — Warehouse selection

**Auth:** Load `fe-internal-tools:databricks-authentication` before any queries. Select a running Databricks SQL warehouse from the logfood profile:

```bash
WAREHOUSE_ID=$(databricks --profile logfood warehouses list --output json | \
  python3 -c "
import json, sys
ws = [w for w in json.load(sys.stdin).get('warehouses', []) if w.get('state') == 'RUNNING']
print(ws[0]['id'] if ws else '')
")
echo "Using warehouse: $WAREHOUSE_ID"
```

Store as `[WAREHOUSE_ID]`. If no warehouse is RUNNING, serverless warehouses start within ~30s once the first query is submitted.

All SQL in this skill runs as:
```python
import subprocess, json

def run_sql(sql, warehouse_id):
    r = subprocess.run(
        ["databricks", "--profile", "logfood", "api", "post",
         "/api/2.0/sql/statements/", "--json",
         json.dumps({"statement": sql, "warehouse_id": warehouse_id,
                     "wait_timeout": "50s", "format": "JSON_ARRAY"})],
        capture_output=True, text=True)
    d = json.loads(r.stdout)
    if d.get('status', {}).get('state') == 'SUCCEEDED':
        cols = [c['name'] for c in d['manifest']['schema']['columns']]
        return cols, d.get('result', {}).get('data_array', [])
    raise RuntimeError(d.get('status', {}).get('error', {}).get('message', str(d)))
```

### 0c — Director SFDC ID

```sql
SELECT Id, Name, Email
FROM main.sfdc_bronze.user
WHERE Name LIKE '%[Director Name]%' AND IsActive = true
ORDER BY processDate DESC LIMIT 5
```

Take the most recent distinct row for the correct person. Store as `[Director SFDC ID]`.

### 0d — AE list (direct reports only)

```sql
SELECT DISTINCT user_id, user_name, user_email
FROM main.gtm_gold.rpt_individual_obt_gtm
WHERE manager_email = '[director_email]'
  AND quarter_type = 'Current Qtr'
ORDER BY user_name
```

Store as `[AE List]` = list of `{user_id, user_name, user_email}`. If empty, fall back to:

```sql
SELECT DISTINCT Id AS user_id, Name AS user_name, Email AS user_email
FROM main.sfdc_bronze.user
WHERE ManagerId = '[Director SFDC ID]' AND IsActive = true
ORDER BY Name
```

---

## Phase 1: Targets & trajectory

**Single query — all 4 quarters at once:**

```sql
SELECT user_id, user_name,
  target_dbu_dollars                   AS target_qcur,
  target_dbu_dollars_quarter_plus_one  AS target_qnxt1,
  target_dbu_dollars_quarter_plus_two  AS target_qnxt2,
  target_dbu_dollars_quarter_plus_three AS target_qnxt3,
  forecast_straight_line_t28d_quarterly AS t28d_qcur,
  submitted_weighted_projection         AS proj_qcur,
  submitted_weighted_projection_quarter_plus_one  AS proj_qnxt1,
  submitted_weighted_projection_quarter_plus_two  AS proj_qnxt2
FROM main.gtm_gold.rpt_individual_obt_gtm
WHERE manager_email = '[director_email]'
  AND quarter_type = 'Current Qtr'
ORDER BY user_name
```

Compute team-level totals by summing across all AEs:
```
team_target_Qcur  = Σ target_qcur
team_target_Qnxt1 = Σ target_qnxt1
team_target_Qnxt2 = Σ target_qnxt2
team_target_Qnxt3 = Σ target_qnxt3
team_t28d_Qcur    = Σ t28d_qcur
```

**Trajectory (5% organic QoQ growth for Qnxt1+):**
```
traj_Qcur  = team_t28d_Qcur
traj_Qnxt1 = traj_Qcur  * 1.05
traj_Qnxt2 = traj_Qnxt1 * 1.05
traj_Qnxt3 = traj_Qnxt2 * 1.05
```

**Quarter date ranges — derived dynamically at runtime:**

Do NOT hardcode fiscal dates. Use the shared fiscal calendar utility:

> **Shared resource:** `../../resources/fiscal_calendar.py` (single source for all fe-manager skills). For the 4-quarter forward view needed by this skill, run with `--quarters`:

```python
import subprocess, json

ctx = json.loads(subprocess.run(
    ["python3", "../../resources/fiscal_calendar.py", "--quarters"],
    capture_output=True, text=True
).stdout)
# Produces: fy_label, q_bounds {'Qcur': (start, end), ...}, q_labels {'Qcur': "FY'27 Q1 (Feb–Apr)", ...}
Q_BOUNDS  = {k: tuple(v) for k, v in ctx["q_bounds"].items()}
Q_LABELS  = ctx["q_labels"]
FY_LABEL  = ctx["fy_label"]
Q_ORDERED = [("Qcur",  *Q_BOUNDS["Qcur"]),  ("Qnxt1", *Q_BOUNDS["Qnxt1"]),
             ("Qnxt2", *Q_BOUNDS["Qnxt2"]), ("Qnxt3", *Q_BOUNDS["Qnxt3"])]
```

Call this once before any pipeline calculations. Use `Q_LABELS['Qcur']` through `Q_LABELS['Qnxt3']` for all report headings, table rows, and Slack messages. Example output for a run in Feb–Apr 2026:

```
fy_label = "FY'27"
q_labels = {'Qcur': "FY'27 Q1 (Feb–Apr)", 'Qnxt1': "FY'27 Q2 (May–Jul)", ...}
q_bounds = {'Qcur': ('2026-02-01', '2026-04-30'), ...}
```

---

## Phase 2: Account & UCO data

### 2a — Account→AE mapping

Build the map in two steps, merging both sources to handle Hunter/Geo AEs.

**Step 1: accountteammember (primary role)**
```sql
SELECT atm.AccountId, atm.UserId, a.DeployableAccountName__c AS account_name
FROM main.sfdc_bronze.accountteammember atm
JOIN main.sfdc_bronze.account a
  ON a.Id = atm.AccountId
  AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
WHERE atm.UserId IN ('[ae_id_1]', '[ae_id_2]', ...)
  AND atm.TeamMemberRole = 'Account Executive'
  AND atm.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.accountteammember)
GROUP BY atm.AccountId, atm.UserId, a.DeployableAccountName__c
ORDER BY a.DeployableAccountName__c
LIMIT 2000
```

**Step 2: Account OwnerId fallback (for Hunter AEs with few ATM entries)**

For each AE separately (to avoid inline byte limit):
```sql
SELECT DISTINCT Id AS AccountId, OwnerId, DeployableAccountName__c AS account_name
FROM main.sfdc_bronze.account
WHERE OwnerId = '[ae_id]'
  AND IsDeleted = false
  AND processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
LIMIT 500
```

Merge both sets — for any AccountId already mapped via Step 1, skip Step 2. Final map: `account_id → {ae_id, ae_name, account_name}`.

> **Note:** If `DeployableAccountName__c` is null, fall back to AccountId as the label and flag for data hygiene. Do not use `Name` or `Headquarter_Business_Name__c` — these do not resolve reliably.

### 2b — UCO pull

First, count distinct UCOs to detect if LIMIT will be hit:
```sql
SELECT COUNT(DISTINCT uc.Id) AS cnt
FROM main.sfdc_bronze.usecase__c uc
WHERE uc.Account__c IN ('[acct_id_1]', '[acct_id_2]', ...)
  AND uc.Stages__c IN ('U1','U2','U3','U4','U5')
  AND uc.IsDeleted = false
  AND uc.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
```

If count ≤ 500: run single query. If > 500: batch accounts into groups of 50 and run separate queries with LIMIT 500 each (should not be needed in practice — most teams have < 300 UCOs total).

**Main UCO query (runs once or per batch):**
```sql
SELECT
  uc.Id, uc.Name, uc.Stages__c, uc.Account__c, uc.OwnerId,
  uc.MonthlyTotalDollarDBUs__c,
  uc.Full_Production_Date__c,
  uc.Implementation_Start_Date__c,
  uc.Demand_Plan_Next_Steps__c,
  uc.CustomLastModifiedDate__c,
  uc.SlippageCount__c,
  uc.CurrentStageDaysCount__c,
  uc.MetricsNotes__c,
  uc.MetricsQuantification__c,
  uc.XDRDecisionProcess__c,
  uc.XDRIdentifiedPainGain__c,
  uc.Compelling_event_Urgency__c,
  uc.Implementation_Notes__c,
  uc.Blockers__c,
  a.DeployableAccountName__c AS account_name
FROM main.sfdc_bronze.usecase__c uc
JOIN main.sfdc_bronze.account a
  ON a.Id = uc.Account__c
  AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
WHERE uc.Account__c IN ('[acct_id_1]', '[acct_id_2]', ...)
  AND uc.Stages__c IN ('U1','U2','U3','U4','U5')
  AND uc.IsDeleted = false
  AND uc.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
ORDER BY uc.Name
LIMIT 500
```

Enrich each UCO with `ae_name` by joining `Account__c` → `[AE Account Map]`.

---

## Phase 3: Classification & pipeline model

### 3a — Python classification script

> **Resource file:** `../../resources/classify_ucos.py` — shared classification module for this skill. Copy it to `/tmp/classify_ucos.py` before running classification, or import directly if running from the plugin directory.

```bash
cp ../../resources/classify_ucos.py /tmp/classify_ucos.py
```

The module exports these functions (see source for full docstrings and scoring breakdown):

```python
from classify_ucos import (
    momentum_label,            # UCO → ACTIVE / DRIFTING / STALLED / AT-RISK / WILL_NOT_HAPPEN
    heat_score,                # U1/U2 → 0-10 acceleration readiness
    u5_heat_score,             # U5 → 0-10 go-live urgency
    estimate_contribution_quarter,  # U1/U2 → Qcur/Qnxt1/Qnxt2/Qnxt3/FY+1
    pull_forward_potential,    # U5 → {planned_q, target_q, opportunity, days_gap}
    quarter_contribution,      # UCO + quarter → weighted $DBU contribution
    will_not_happen_score,     # UCO → 0-N risk score (≥3 = WILL_NOT_HAPPEN)
    CONFIDENCE,                # label → confidence multiplier (ACTIVE=1.0 .. WNH=0.0)
    Q_BOUNDS, Q_LABELS, FY_LABEL, Q_ORDERED,  # fiscal context (auto-loaded)
)
```

**Key scoring rules (for reference — authoritative source is the resource file):**

| Function | Input | Output | Range |
|----------|-------|--------|-------|
| `momentum_label(uco)` | UCO dict | Label string | ACTIVE / DRIFTING / STALLED / AT-RISK / WILL_NOT_HAPPEN |
| `heat_score(uco)` | UCO dict | Float | 0-10 (U1/U2 acceleration readiness) |
| `u5_heat_score(uco)` | UCO dict | Float | 0-10 (U5 go-live urgency) |
| `estimate_contribution_quarter(uco)` | UCO dict | Quarter key | Qcur / Qnxt1 / Qnxt2 / Qnxt3 / FY+1 |
| `pull_forward_potential(uco)` | UCO dict | Dict | {planned_q, target_q, opportunity, days_gap} |
| `quarter_contribution(uco, qk)` | UCO dict + quarter key | Float | Weighted $DBU contribution |

### 3b — Momentum & pipeline summary

For each U2–U5 UCO:
1. Compute `momentum_label(uco)`
2. For each of Qcur–Qnxt3: compute `quarter_contribution(uco, qk)`
3. Aggregate into `uco_pipe = {Qcur: $, Qnxt1: $, Qnxt2: $, Qnxt3: $}`
4. Count labels: ACTIVE / DRIFTING / STALLED / AT-RISK / WILL_NOT_HAPPEN
5. Attribute to AE via `AE Account Map`

For each AE: track `{Qcur_pipe, Qnxt1_pipe, Qnxt2_pipe, Qnxt3_pipe, ACTIVE, DRIFTING, STALLED, AT-RISK, WILL_NOT_HAPPEN, U1_count}`.

### 3c — Verdict per quarter

```
Total(Q) = traj(Q) + uco_pipe(Q)
Gap(Q)   = Total(Q) - target(Q)
Pct(Q)   = Gap(Q) / target(Q) * 100

GREEN  = Pct ≥ -5%
YELLOW = -20% ≤ Pct < -5%
RED    = Pct < -20%
```

Apply for each of Qcur, Qnxt1, Qnxt2, Qnxt3.

### 3d — Acceleration section (U1/U2 + U5) — quarter-aware framing

The two sub-sections have **different temporal orientations**:

- **3e-i (U1/U2)** = **future quarter pipeline builders.** These deals will not contribute to Qcur/Qnxt1 consumption directly — their value is filling Qnxt1/Qnxt2/Qnxt3 gaps. Frame as: "Act now to close the forward pipeline."
- **3e-ii (U5)** = **current and next quarter go-live management.** These are already in onboarding. The question is: will they go live on time (protect Qcur plan), can any Qnxt2-planned ones be pulled into Qnxt1 (upside), and are any at risk of slipping (downside)?

#### 3d-i: U1/U2 — Grouped by Estimated Contribution Quarter

For each U1/U2 UCO:
1. Compute `heat_score(uco)` 
2. Compute `estimate_contribution_quarter(uco)` — uses stage + heat score to estimate go-live timing
3. Group into Qnxt1/Qnxt2/Qnxt3 tables sorted by score ↓, monthly DBU ↓
4. Include SFDC links for all rows

Show per quarter:
- Qnxt1 (hot U2s, score ≥ 8): top 10 — these are the most time-sensitive actions
- Qnxt2 (most U1/U2 deals): top 8
- Qnxt3 (cold U1s): top 6
- One "hottest per AE" summary row (with estimated contribution quarter)

#### 3d-ii: U5 — Grouped by Pull-Forward Opportunity

For each non-WNH U5 UCO:
1. Compute `u5_heat_score(uco)` — reads both NS + `Implementation_Notes__c`
2. Classify using `pull_forward_potential(uco)` — returns one of:
   - `PROTECT_Qcur`: planned Qcur go-live, must stay on track
   - `PULL_TO_Qcur`: planned Qnxt1 but advanced enough to pull into current quarter (strict criteria)
   - `Qnxt1_ON_TRACK`: planned Qnxt1, progressing normally
   - `PULL_TO_Qnxt1`: planned Qnxt2 with strong momentum — upside opportunity
   - `Qnxt2_ON_TRACK`: planned Qnxt2+, standard progress
   - `AT_RISK_OF_SLIP`: signals of slippage regardless of planned quarter
3. Report total $DBU/mo at stake per category

**Display order:**
1. `PROTECT_Qcur` — show all (these are this quarter's revenue)
2. `PULL_TO_Qcur` — show all (immediate upside if any qualify)
3. `Qnxt1_ON_TRACK` — show top 8 (for awareness)
4. `PULL_TO_Qnxt1` — show all (next quarter upside)
5. `AT_RISK_OF_SLIP` — show all as bullet list with flags

For `PROTECT_Qcur` and `PULL_TO_Qnxt1` rows include Impl Notes Signal:
- "✓ struct" = has LATEST STATUS/CURRENT STATUS block in impl notes (actively maintained)
- "✓ notes" = non-empty implementation notes
- "⚠ none" = no impl notes (risk signal — no visibility into actual delivery)

---

## Phase 4: Report output

### 4a — Google Doc

Create a new Google Doc using `google-docs` skill:
```
Title: SD Pipeline Sufficiency — [Director Name] — [YYYY-MM-DD]
```

Write the report as markdown and convert using `markdown_to_gdocs.py --input [file] --doc-id [id]`.

**After creation, share the doc with the director (editor access) using the Drive API:**

```bash
TOKEN=$(python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token)
curl -s -X POST "https://www.googleapis.com/drive/v3/files/[DOC_ID]/permissions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d "{\"role\": \"writer\", \"type\": \"user\", \"emailAddress\": \"[Director Email]\"}"
```

If the share call returns an error, log it and continue — do not block doc delivery or Slack DMs.

**Document structure (6 sections — always in this order):**

Use `q_labels` from `../../resources/fiscal_calendar.py --quarters` for all quarter headings. In the template below, `[Qcur_LABEL]`–`[Qnxt3_LABEL]` = `q_labels['Qcur']`–`q_labels['Qnxt3']` and `[FY_LABEL]` = `fy_label`. **Never write a literal fiscal year or month range.**

```
# SD Pipeline Sufficiency — [Director Name] — [Run Date]
Prepared by: [FE Manager Name] | Run date: [date] | Covers: [FY_LABEL] [Qcur_LABEL] – [Qnxt3_LABEL]
Sources: rpt_individual_obt_gtm · accountteammember · usecase__c (Demand_Plan_Next_Steps__c)

## 1. Executive Summary
Team: [N AEs] | [M accounts] | [P active UCOs U2–U5] | [W WNH excluded] | [U1+U2 accel pool]

| Quarter | Target | Trajectory | UCO Pipeline | Total | Gap | Verdict |
|---------|--------|------------|--------------|-------|-----|---------|
| [Qcur_LABEL]  | $X | $X | $X | $X | $X | 🟢/🟡/🔴 (+X%) |
| [Qnxt1_LABEL] | ...
| [Qnxt2_LABEL] | ...
| [Qnxt3_LABEL] | ...
| [FY_LABEL] Full Year | ...

[Trajectory footnote: [Qcur_LABEL] = T28D straight-line. [Qnxt1_LABEL]–[Qnxt3_LABEL] = Q_prev × 1.05 (5% organic QoQ growth)]
[Momentum distribution: ACTIVE=N | DRIFTING=N | STALLED=N | AT-RISK=N | WNH=N]
[Bottom line narrative: 2–3 sentences on overall health and primary driver of gap or surplus]

## 2. AE-Level Breakdown
[Account attribution method note]
| AE | Accts | [Qcur_LABEL] Pipe | [Qnxt1_LABEL] Pipe | [Qnxt2_LABEL] Pipe | [Qnxt3_LABEL] Pipe | A/D/S/WNH | U1 pool | Flags |
...
[Named observations per rep — 1–2 sentences each, highlight white space, cliffs, high risk]

## 3. Acceleration Candidates
[3a: U1/U2 pipeline builders by target quarter | 3b: U5 go-live management by pull-forward potential]

### 3a. U1 + U2 Pipeline Builders — Targeted by Contribution Quarter
[Framing: these deals do NOT contribute to [Qcur_LABEL]/[Qnxt1_LABEL] directly — act now to fill [Qnxt1_LABEL]/[Qnxt2_LABEL]/[Qnxt3_LABEL] gaps]
[U2 hot (score ≥8) → Qnxt1 (18wks) | U2 normal → Qnxt2 (24wks) | U1 hot → Qnxt2 (24wks) | U1 normal → Qnxt3 (30wks)]

**[Qnxt1_LABEL] Contributors — hot U2 deals | Act now, contributes in ~18 weeks**
| Score | Stage | Account | Use Case | $DBU/mo | AE | Reasoning |
...top 10, sorted score ↓ then monthly ↓...

**[Qnxt2_LABEL] Contributors — primary U1/U2 pipeline build**
| Score | Stage | Account | Use Case | $DBU/mo | AE | Reasoning |
...top 8...

**[Qnxt3_LABEL] Contributors — longer-horizon U1 deals**
| Score | Stage | Account | Use Case | $DBU/mo | AE | Reasoning |
...top 6...

**Hottest Deal Per AE (with estimated contribution quarter)**
| AE | Stage | Est. Quarter | Account | Use Case | $DBU/mo | Action |
...

### 3b. U5 Go-Live Management — Protect [Qcur_LABEL], Pull [Qnxt2_LABEL]→[Qnxt1_LABEL], Flag At-Risk
[Score 0–10 reads both Demand_Plan_Next_Steps__c + Implementation_Notes__c]
[Impl signal: ✓ struct = LATEST STATUS block | ✓ notes = non-empty | ⚠ none = no visibility]

**🟢 Protect [Qcur_LABEL] Go-Lives — $[X]/mo at stake — must not slip**
| Score | Account | Use Case | $DBU/mo | AE | Days@U5 | Impl | Reasoning |
...all PROTECT_Qcur deals...

**🔵 Pull [Qnxt2_LABEL]→[Qnxt1_LABEL] Opportunity — $[X]/mo upside — Qnxt2 go-lives with strong momentum**
| Score | Account | Use Case | $DBU/mo | AE | Days@U5 | Impl | Planned Go-Live | Reasoning |
...all PULL_TO_Qnxt1 deals (if any)...

**⏳ [Qnxt1_LABEL] On-Track — $[X]/mo — progressing toward planned go-live**
| Score | Account | Use Case | $DBU/mo | AE | Days@U5 | Impl | Reasoning |
...top 8 Qnxt1_ON_TRACK deals...

**🔴 At-Risk of Slipping — $[X]/mo threatened — review before quarter ends**
- [Deal] ([Account], [AE], planned [Qtr], $[X]/mo) — [flags: N slips / low heat / long stage / no impl notes]

## 4. WILL NOT HAPPEN & AT-RISK Use Cases
### WILL NOT HAPPEN — Excluded from Pipeline (N UCOs)
[WNH score criteria recap]
| Account | Use Case | Stage | Slips | Days | WNH Score | AE | Latest Next Steps |
...

### AT-RISK — In Pipeline but Endangered (N UCOs)
[Confidence = 0.1]
| Account | Use Case | Stage | Slips | Go-Live Qtr | AE | Latest Next Steps |
...

## 5. Pipeline by Quarter
### [Qcur_LABEL] — Target $X | Total $X | Verdict
### [Qnxt1_LABEL] — ...
### [Qnxt2_LABEL] — ...
### [Qnxt3_LABEL] — ...
[Each section: top UCO contributors with go-live, momentum, AE, effective $ contribution]

## 6. Methodology
[AE scope, account attribution logic, trajectory model, confidence table,
WNH scoring table, contribution formula, heat score breakdown, primary data fields]
```
### 4b — Slack message

Send two DMs via `user-slack` MCP:
1. **To director** (`users.lookupByEmail` → `chat.postMessage`)
2. **To FE manager** (same message or brief confirmation)

**Message structure:**

```
:bar_chart: *Pipeline Sufficiency — [Director Name]'s Team | [FY_LABEL] [Qcur_LABEL] – [Qnxt3_LABEL]*
Full report: <[doc_url]|Google Doc>

---

:[green/yellow/red]: *Headline*
[2–3 sentence summary: overall verdict, primary driver, structural insight about
target growth vs combined trajectory+pipe growth rate QoQ]

```
Quarter              Target    Traj      UCO Pipe   Total     Gap
[Qcur_LABEL]         $XXXk     $XXXk     $XXk       $XXXk     +$XXk (+XX%)  🟢/🟡/🔴
[Qnxt1_LABEL]        $XXXk     $XXXk     $XXk       $XXXk     +$XXk (+XX%)  🟢/🟡/🔴
[Qnxt2_LABEL]        $XXXk     $XXXk     $XXXk      $XXXk     +$XXk (+XX%)  🟢/🟡/🔴
[Qnxt3_LABEL]        $XXXk     $XXXk     $XXXk      $XXXk     +$XXk (+XX%)  🟢/🟡/🔴
FY'XX Full Year      $X.XXM                         $X.XXM    +$XXXk (+XX%) 🟢/🟡/🔴
```
[Right-pad all columns to consistent fixed width for monospace alignment. Use K for thousands, M for millions. NEVER use pipe-style markdown tables in Slack — they do not render. Always wrap the data table in a ``` code block.]

---

:rotating_light: *Risk Flags*
• [Rep name] — [WNH/AT-RISK/STALLED count] [specific deal or pattern]
...

---

:rocket: *Top Actions*

*1. Act now — U1/U2 hot deals building [Qnxt1_LABEL]/[Qnxt2_LABEL] pipeline*
[List top 5–6 U1/U2 deals by contribution quarter: Qnxt1-targeted first, then Qnxt2]
• *[Account]* | <[sfdc_url]|[UCO Name]> — [stage] → [Qnxt1/Qnxt2], $[X]K/mo, [AE] → [action]

*2. Protect [Qcur_LABEL] go-lives — $[X]K/mo at stake this quarter*
[List top 4–5 PROTECT_Qcur deals by value, noting any with impl risk signals]
• *[Account]* | <[sfdc_url]|[UCO Name]> — U5, $[X]K/mo, [AE], go-live [date] → [protect / check impl notes]

*3. Pull [Qnxt2_LABEL]→[Qnxt1_LABEL] upside — $[X]K/mo available if momentum maintained*
[List PULL_TO_Qnxt1 deals (if any)]
• *[Account]* | <[sfdc_url]|[UCO Name]> — U5 [Qnxt2_LABEL]→[Qnxt1_LABEL], $[X]K/mo, [AE] → [accelerate onboarding]

*2–5. [Named, specific, actionable items based on the actual data]*
[Frame actions differently for GREEN teams (maintain lead) vs YELLOW/RED (close gap)]

---
_Run: [date] | Sources: rpt_individual_obt_gtm · sfdc_bronze.usecase__c · accountteammember_
```

Use `with_foot_note: false` to avoid attribution footer.

---

## Phase 5: Cache snapshot

Save to `~/.vibe/cache/sd-pipeline-sufficiency/[director_name_safe]/`:

```json
{
  "run_date": "YYYY-MM-DD",
  "director_name": "...",
  "director_email": "...",
  "ae_count": 0,
  "account_count": 0,
  "uco_count_u2_u5": 0,
  "uco_count_u1": 0,
  "label_counts": {"ACTIVE":0,"DRIFTING":0,"STALLED":0,"AT-RISK":0,"WILL_NOT_HAPPEN":0},
  "targets":    {"Qcur":0,"Qnxt1":0,"Qnxt2":0,"Qnxt3":0,"FY":0},
  "trajectory": {"Qcur":0,"Qnxt1":0,"Qnxt2":0,"Qnxt3":0,"FY":0},
  "uco_pipe":   {"Qcur":0,"Qnxt1":0,"Qnxt2":0,"Qnxt3":0,"FY":0},
  "total":      {"Qcur":0,"Qnxt1":0,"Qnxt2":0,"Qnxt3":0,"FY":0},
  "gap":        {"Qcur":0,"Qnxt1":0,"Qnxt2":0,"Qnxt3":0,"FY":0},
  "verdict":    {"Qcur":"GREEN","Qnxt1":"YELLOW","Qnxt2":"RED","Qnxt3":"YELLOW","FY":"YELLOW"},
  "q_labels":   {"Qcur":"FY'27 Q1 (Feb–Apr)","Qnxt1":"FY'27 Q2 (May–Jul)","Qnxt2":"...","Qnxt3":"..."},
  "google_doc_url": "https://docs.google.com/document/d/..."
}
```

Write both `latest_snapshot.json` and `snapshot_[YYYY-MM-DD].json`.

`[director_name_safe]` = director name lowercased, spaces replaced by underscores (e.g. `tanya_nitzsche`).

---

## Error handling

| Situation | Action |
|-----------|--------|
| Director not found in SFDC | Stop + ask for correct name/email |
| No AEs found in rpt_individual_obt_gtm | Try sfdc_bronze.user ManagerId fallback |
| AEs found but 0 accounts from ATM | Switch to account.OwnerId approach for all AEs |
| UCO query returns 0 rows | Check processDate filter; verify account IDs are valid |
| `Name` column fails on sfdc_bronze.account | Use `DeployableAccountName__c` |
| `Account__r.Name` syntax error | Join to account table explicitly; never use dot-notation |
| t28d = 0 for some AEs | Use non-zero AEs for trajectory; flag zero-t28d AEs separately |
| UCO count > 500 | Batch accounts into groups of 50; merge results |
| Google Doc creation fails | Print markdown to terminal; offer to retry |
| Slack DM fails | Print message to terminal; provide copy-paste text |
| Director has no targets in Q3/Q4 columns | Note as "no Q4 target set"; skip Q3 from model |

---

## Lessons from live runs (do not ignore)

These were validated against multiple EMEA teams (8-AE YELLOW team with ~235 accounts and a 6-AE Geo/Hunter GREEN team with ~358 accounts):

1. **`NextSteps__c` is empty for all EMEA UCOs.** Always use `Demand_Plan_Next_Steps__c`. Never build momentum logic that relies on `NextSteps__c` alone.

2. **Historical tables require `processDate` filtering.** `accountteammember`, `account`, and `usecase__c` each contain one row per record per day. Without `processDate = MAX(processDate)` you get 200–500× more rows than expected and all pagination will be wrong.

3. **`a.Name` does not resolve when querying `sfdc_bronze.account` directly.** Use `DeployableAccountName__c`. If that is null, fall back to AccountId as the display label.

4. **Salesforce relationship syntax (`Account__r.Name`) is not supported in Logfood SQL.** Always join the account table explicitly.

5. **Hunter/Geo AEs have very few accountteammember records.** The `account.OwnerId` fallback is essential for teams like these. Always merge both sources.

6. **`rpt_individual_obt_gtm` has no `processDate` or `sfdc_user_id` column.** Use `user_id` and `quarter_type = 'Current Qtr'`.

7. **`parse_most_recent_past_date()` is mandatory for heat scoring.** The NS field contains future go-live dates. Without filtering to past dates, recency scores are wrong and deals appear cold when they are actually hot.

8. **The cap rule matters: SlippageCount ≥ 2 → max label is DRIFTING.** Without this, a deal with 4 slips and a recent [Green] entry gets classified ACTIVE and inflates pipeline. Always apply the slip cap regardless of NS sentiment.

9. **QUALIFY is supported in Databricks SQL.** Use it freely for deduplication.

10. **Full-year (Q1–Q4) always reveals the clearest story.** The Q4 target ramp is where YELLOW teams become RED. Don't show only Q1–Q3.

11. **For GREEN teams, frame actions as "maintain the lead" not "close a gap."** The risk flags and acceleration candidates are still valuable — but the framing changes the director's reaction entirely.

12. **Always send Slack to both the director AND the FE manager.** The director is the primary recipient; the FE manager needs a copy for their own tracking.

13. **Never hardcode fiscal dates.** Always use `../../resources/fiscal_calendar.py --quarters` (the shared `four_quarter_context()` function) to derive `Q_BOUNDS`, `Q_LABELS`, and `FY_LABEL` from today's date. The skill is valid in any quarter of any fiscal year.

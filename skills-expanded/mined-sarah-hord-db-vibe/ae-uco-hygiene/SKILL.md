---
name: ae-uco-hygiene
description: Review UCO hygiene across a team of AEs and notify them via Slack DM about stale or incomplete UCOs. Use when a manager or lead wants to audit their team's UCO health, identify hygiene issues, and send personalized Slack reminders to AEs. Triggers on phrases like "UCO hygiene", "audit my team's UCOs", "check AE hygiene", "send UCO reminders", "team UCO health".
user-invocable: true
---

# AE UCO Hygiene Auditor

Review the UCO (Use Case Object) health across a team of Account Executives, identify hygiene issues, and draft personalized Slack messages for each AE summarizing what needs attention.

> **Note:** This skill creates Slack message **drafts only** — it does NOT send any messages. All composed messages are presented to the user for review. The user sends them manually.

## Prerequisites

Before running this skill, ensure:
1. **fe-ee installed** — provides `uco_hygiene.py` (hygiene engine) in `skills/ae-uco-hygiene/resources/`
2. **Logfood (Databricks) authenticated** — run `/databricks-authentication` with the `logfood` profile if needed
3. **Salesforce CLI authenticated** — run `/salesforce-authentication` if needed (for resolving Salesforce UCO URLs)

---

## Step 1: Query Logfood for Team UCOs

Use the `logfood-querier` skill or run the query below directly against the logfood workspace to retrieve all active UCOs for the team.

**Logfood profile:** `logfood`
**Logfood workspace:** `https://adb-2548836972759138.18.azuredatabricks.net/`

This skill covers **all EE teams** under `region_level_2 = 'AMER Enterprise & Emerging - EE & Startup - EE'`. No profile configuration is needed — the query pulls all teams at once.

```sql
SELECT
  Usecase_ID,
  Usecase,
  Account,
  Account_AE,
  AE_Manager,
  Account_SA,
  UCO_Stage,
  health_status,
  LEFT(Next_Steps, 500) AS Next_Steps,
  next_steps_modified_date,
  Implementation_Start_Date,
  Full_Prod_Date,
  Monthly_UCO_Dollar_DBUs,
  UCO_Description,
  Partner,
  onboard_fy_quarter,
  golive_fy_quarter,
  current_fy_quarter,
  days_in_stage,
  region_level_3
FROM main.field_usage_dashboard.uco_data
WHERE region_level_2 = 'AMER Enterprise & Emerging - EE & Startup - EE'
  AND UCO_stage NOT IN ('U6-Live', 'U7-Lost')
  AND Monthly_UCO_Dollar_DBUs > 1000
```

> **Manager CC notes:**
> - Use the following overrides regardless of what `AE_Manager` contains for these teams:
>
> | region_level_3 suffix | CC manager email |
> |---|---|
> | EE | `zach.jordan@databricks.com` |
> | EE Core CME & Retail & Tech | `dustin.flores@databricks.com` |
> | EE Core FINS | `dustin.flores@databricks.com` |
> | EE Core Geo | `adam.roberts@databricks.com` |
> | EE Core HLS & MFG | `tessa.prescott@databricks.com` |
> | EE Hunter FINS & HLS & MFG | `travis.thompson@databricks.com` |
> | EE Hunter Geo | `travis.thompson@databricks.com` |
> | EE Hunter Retail & CME & Tech & Geo | `travis.thompson@databricks.com` |
>
> - Match on the suffix of `region_level_3` (the part after the last ` - `).
> - Manager email format: `first.last@databricks.com`.
>
> **SA Manager CC (keyed by team, same suffix as above):**
>
> | region_level_3 suffix | SA Manager email |
> |---|---|
> | EE | `waqar.shaikh@databricks.com` |
> | EE Core CME & Retail & Tech | `elliott.herz@databricks.com` |
> | EE Core FINS | `waqar.shaikh@databricks.com` |
> | EE Core Geo | `charko.patterson@databricks.com` |
> | EE Core HLS & MFG | `charko.patterson@databricks.com` |
> | EE Hunter FINS & HLS & MFG | `ethan.ferdosi@databricks.com` |
> | EE Hunter Geo | `ethan.ferdosi@databricks.com` |
> | EE Hunter Retail & CME & Tech & Geo | `ethan.ferdosi@databricks.com` |
>
> Both the AE manager and the SA manager should be CC'd on every email.

Run the query using the `databricks-query` skill with `--profile logfood`, or via the file-based approach below.

> **CRITICAL — write JSON to a file before running.** The SQL contains single-quoted values like `NOT IN ('U6-Live', 'U7-Lost')`. Embedding these in a `--json='...'` shell argument (single-quoted) will cause a `BAD_REQUEST` error because the single quotes conflict. Always write the request body to a file and use `--json=@file`:

```python
import json
query = """SELECT
  Usecase_ID, Usecase, Account, Account_AE, AE_Manager, Account_SA, UCO_Stage, health_status,
  LEFT(Next_Steps, 500) AS Next_Steps, next_steps_modified_date,
  Implementation_Start_Date, Full_Prod_Date, Monthly_UCO_Dollar_DBUs,
  UCO_Description, Partner,
  onboard_fy_quarter, golive_fy_quarter, current_fy_quarter, days_in_stage, region_level_3
FROM main.field_usage_dashboard.uco_data
WHERE region_level_2 = 'AMER Enterprise & Emerging - EE & Startup - EE'
  AND UCO_stage NOT IN ('U6-Live', 'U7-Lost')
  AND Monthly_UCO_Dollar_DBUs > 1000"""

with open("/tmp/uco_query.json", "w") as f:
    json.dump({"statement": query, "warehouse_id": "<WAREHOUSE_ID>",
               "format": "JSON_ARRAY", "wait_timeout": "50s"}, f)
```

```bash
databricks api post /api/2.0/sql/statements/ \
  --json=@/tmp/uco_query.json \
  --profile logfood > /tmp/uco_data.json
```

The result includes these key fields (actual logfood column names):
- `Usecase_ID` — Salesforce UCO ID (used to build the UCO URL)
- `Usecase` — Use case name
- `Account` — Account name
- `Account_AE` — AE name (used to group UCOs per AE)
- `UCO_Stage` — Stage (e.g. `U3-Evaluating`, `U4-Confirming`)
- `health_status` — Health status field (values: `Red`, `Yellow`, `Green`)
- `Next_Steps` — Full next steps text (`Demand_Plan_Next_Steps__c`)
- `next_steps_modified_date` — Date next steps were last updated (ISO format)
- `Implementation_Start_Date` — Onboarding date
- `Full_Prod_Date` — Go-live date
- `Monthly_UCO_Dollar_DBUs` — Monthly $DBU consumption
- `UCO_Description` — UCO description text (used for C7 sizing check and C8 partner check)
- `Partner` — Partner attached to the UCO (empty string or null if none; used for C8)
- `onboard_fy_quarter` — FY quarter of onboarding date (e.g. `FY27-Q1`)
- `golive_fy_quarter` — FY quarter of go-live date
- `current_fy_quarter` — Current FY quarter (use this, do not compute manually)
- `days_in_stage` — Days the UCO has been in its current stage
- `AE_Manager` — Name of the AE's manager (used to determine CC recipient for email drafts; may be a `"TBH..."` placeholder for vacant roles)
- `Account_SA` — Name of the SA assigned to the account (used to determine AE-SA pairs for email drafts)
- `region_level_3` — Team identifier (used to group UCOs by team when running across all EE)

> **Important — save results to a file before processing:** The query result can be ~150KB+ and will be truncated if read directly through a tool. Always save the raw JSON response to a file (e.g., `/tmp/uco_data.json`) and use Python to parse and analyze it:
> ```bash
> databricks api post /api/2.0/sql/statements/ --profile=logfood --json='...' > /tmp/uco_data.json
> ```
> Then in Python: `data = json.load(open("/tmp/uco_data.json"))` and `rows = data["result"]["data_array"]`.
> **Do not attempt to read or summarize the raw JSON directly** — process all rows programmatically.

---

## Step 2: Identify Problem UCOs

Apply the following inspection rules to the UCO list from Step 1. A UCO is a **problem UCO** if it meets **any** of the conditions below.

> **Implementation — parallel subagent approach:** Step 2 uses a three-phase workflow designed for maximum parallelism:
> 1. **Phase 1 (Python):** A single script runs `evaluate_conditions()`, applies all rule-based checks (C2, C3, C5, C6), and writes candidate files for all AI-judgment conditions (C1, C4, C7, C8, C9) to `/tmp/`.
> 2. **Phase 2 (parallel subagents):** Launch all judgment subagents simultaneously. C1 is split into batches of 50 UCOs (e.g. 130 candidates → 3 subagents), each writing its own output file. C4, C7, C8, C9 each get one subagent. All subagents run concurrently and are waited on before proceeding.
> 3. **Phase 3 (Python):** A single script merges all C1 batch files into one, loads all judgment files, merges them with rule-based issues, groups by AE, and writes `/tmp/uco_issues_by_ae.json`.
>
> Similarly, **Step 3 (message drafting) uses parallel subagents** — one subagent per AE — so all messages are drafted simultaneously.

For each flagged UCO, record:
- Which condition(s) it triggered
- A plain-English explanation of why it was flagged
- The specific remediation steps the account team needs to take

### Inspection Conditions

Conditions fall into two buckets that determine how they appear in the Slack message:

**Take Action** — Definitive problems requiring immediate remediation:
- Condition 1: U2–U5 UCO stuck in stage with no clear plan to progress (>40 days for U2/U3, >50 days for U4/U5)
- Condition 2: UCO with stale next steps (>14 days, or >7 days if >$10,000/mo and U3+)
- Condition 3: Breached onboarding or go-live date
- Condition 7: Large UCO (>$5,000/mo) without sizing justification in description

**Possible Issue Identified, Please Review** — Potential problems requiring AE judgment:
- Condition 4: Wrong stage based on next steps content
- Condition 5: Risky onboarding or go-live timeline
- Condition 6: U1–U3 UCO with onboarding date this month
- Condition 8: Partner mentioned in description/next steps but not attached to UCO
- Condition 9: Blocker mentioned in next steps but no blocker attached to UCO

> **Label priority:** If a UCO triggers any Condition 4, 5, 6, 8, or 9 — regardless of what other conditions also fire — always use the **"Possible Issue Identified, Please Review"** label. Combine all triggered conditions into a single issue/action entry.

---

#### Condition 1: UCO Stuck in Stage with No Clear Path Forward

Flag a UCO if **all** of the following are true:
- Stage is **U2, U3, U4, or U5**
- `days_in_stage` exceeds the stage-specific threshold: **40 days** for U2/U3, **50 days** for U4/U5
- The last two Next Steps entries do **not** describe a clear plan for how this use case will progress to the next stage

> **80% warning rule:** If a UCO's `days_in_stage` is ≥80% of its threshold (≥32 days for U2/U3, ≥40 days for U4/U5) but has not yet crossed it, do **not** flag it as Take Action. Instead, include it under **"Possible Issue Identified, Please Review"** with a note that it is approaching the threshold and will be flagged if not updated.

**Implementation: Multi-phase inline AI judgment**

Condition 1 uses inline AI judgment — not regex pattern matching — because the question requires understanding _intent_, not just detecting keywords. Activity logs, meeting notes, and vague follow-ups must be distinguished from actual plans.

**What "clear plan to progress" means:**
- The entries describe a specific milestone or action that will advance the project to the next stage
- AND when that milestone will happen (a date, quarter, or timeframe)
- Activity logs, meeting notes, check-ins, past-dated entries, and vague "we'll follow up" language do NOT count
- Blocked UCOs with no resolution path do NOT count

**Examples:**
- *Clear:* `"2/19/26 AG - Expecting to move to U4 in early March after partner decision"` — specific milestone + timing
- *Clear:* `"2/16/26 SL - Tableau parity review targeted for Q2 FY27"` — specific milestone + quarter
- *Clear:* `"2/17/26 AJF - Technical win secured. April onboarding and July go live correct."` — forward confirmation with dates
- *Unclear:* `"Feb-09 - SL - meeting with Lovelytics tomorrow"` — scheduling note, no description of what advances the UCO
- *Unclear:* `"Feb-16 - SL - BLOCKED - ring system blocker. No resolution path."` — explicitly blocked, no plan
- *Unclear:* `"Jan-23 - LC - working to do demo next week to new stakeholder"` — activity, entry is now stale
- *Unclear:* `"Feb-03 - CK - RSA Engagement starts this Friday"` — past-dated reference to a meeting, no milestone

**Phase 1: Extract candidates (Python)**

Run a Python script to identify all UCOs that _might_ be Condition 1 violations (U2–U5, exceeding stage-specific thresholds of 40/50 days) and extract their last two log entries. Save to `/tmp/c1_candidates.json`.

This script uses the shared `uco_hygiene` module for helper functions. It applies all rule-based conditions and writes candidate files for every AI-judgment condition in one pass.

```python
import json, sys, glob, os
from datetime import date

# Import shared hygiene engine
paths = glob.glob(os.path.expanduser(
    "~/.claude/plugins/cache/fe-vibe/fe-ee/*/skills/ae-uco-hygiene/resources"
))
if paths:
    sys.path.insert(0, paths[0])
import uco_hygiene

data = json.load(open("/tmp/uco_data.json"))
cols = [c["name"] for c in data["manifest"]["schema"]["columns"]]
ucoes = [dict(zip(cols, r)) for r in data["result"]["data_array"]]
TODAY = date.today()
cq = ucoes[0]["current_fy_quarter"] if ucoes else None

# Run all rule-based checks and extract all AI-judgment candidates
result = uco_hygiene.evaluate_conditions(ucos=[], today=TODAY, logfood_data=ucoes)

# Filter C1 candidates to only urgent/needs_attention UCOs (C1 is urgency-gated)
c1_candidates = []
for c in result["c1_candidates"]:
    orig = next((u for u in ucoes if u.get("Usecase_ID") == c["uco_id"]), {})
    urgency = uco_hygiene.get_urgency(
        orig.get("onboard_fy_quarter"), orig.get("golive_fy_quarter"), cq
    )
    if urgency is not None:
        c1_candidates.append({
            "uco_id": c["uco_id"], "uco_name": c["uco_name"],
            "Account": orig.get("Account", ""), "stage": c["stage"],
            "days_in_stage": c["days_in_stage"], "recent_entries": c["recent_entries"],
        })

# C4 candidates: all UCOs in current/next quarter with non-empty next steps
c4_candidates = []
for c in result["c4_candidates"]:
    orig = next((u for u in ucoes if u.get("Usecase_ID") == c["uco_id"]), {})
    if uco_hygiene.get_urgency(
        orig.get("onboard_fy_quarter"), orig.get("golive_fy_quarter"), cq
    ) is not None:
        c4_candidates.append(c)

# Write all candidate files (subagents will read these in parallel)
with open("/tmp/c1_candidates.json", "w") as f:
    json.dump(c1_candidates, f, indent=2, default=str)
with open("/tmp/c4_candidates.json", "w") as f:
    json.dump(c4_candidates, f, indent=2, default=str)
with open("/tmp/c7_candidates.json", "w") as f:
    json.dump(result["c7_candidates"], f, indent=2, default=str)
with open("/tmp/c8_candidates.json", "w") as f:
    json.dump(result["c8_candidates"], f, indent=2, default=str)
with open("/tmp/c9_candidates.json", "w") as f:
    json.dump(result["c9_candidates"], f, indent=2, default=str)

# Also save rule-based issues for Phase 3
with open("/tmp/rule_issues.json", "w") as f:
    json.dump(result["rule_issues"], f, indent=2, default=str)

print(f"C1: {len(c1_candidates)} | C4: {len(c4_candidates)} | C7: {len(result['c7_candidates'])} | C8: {len(result['c8_candidates'])} | C9: {len(result['c9_candidates'])}")
print(f"Rule-based issues: {len(result['rule_issues'])}")
```

**Phase 2: Parallel subagent AI judgment**

Before launching subagents, run the following Python snippet to split C1 candidates into batches of 50 and write each batch to a numbered file:

```python
import json, math

c1_candidates = json.load(open("/tmp/c1_candidates.json"))
batch_size = 50
num_batches = max(1, math.ceil(len(c1_candidates) / batch_size))
for i in range(num_batches):
    batch = c1_candidates[i * batch_size : (i + 1) * batch_size]
    with open(f"/tmp/c1_candidates_batch_{i}.json", "w") as f:
        json.dump(batch, f, indent=2, default=str)
print(f"C1 split into {num_batches} batch(es) of up to {batch_size}")
```

Then **launch all subagents simultaneously** — one per C1 batch plus one each for C4, C7, C8, C9. Do not wait for one before starting the next.

**C1 batches** (one subagent per batch file):

| Subagent | Input file | Output file | Question |
|---|---|---|---|
| C1 batch 0 | `/tmp/c1_candidates_batch_0.json` | `/tmp/c1_judgments_batch_0.json` | Does this UCO have a clear plan to progress? (YES/NO) |
| C1 batch 1 | `/tmp/c1_candidates_batch_1.json` | `/tmp/c1_judgments_batch_1.json` | (same) |
| C1 batch N | `/tmp/c1_candidates_batch_N.json` | `/tmp/c1_judgments_batch_N.json` | (same) |

**Other conditions** (one subagent each, launched at the same time as the C1 batches):

| Subagent | Input file | Output file | Question |
|---|---|---|---|
| C4 | `/tmp/c4_candidates.json` | `/tmp/c4_judgments.json` | Is this UCO in the wrong stage based on next steps? (YES/NO) |
| C7 | `/tmp/c7_candidates.json` | `/tmp/c7_judgments.json` | Does this UCO description contain sizing justification? (YES/NO) |
| C8 | `/tmp/c8_candidates.json` | `/tmp/c8_judgments.json` | Is a partner mentioned in the text but not attached? (YES/NO) |
| C9 | `/tmp/c9_candidates.json` | `/tmp/c9_judgments.json` | Does an active blocker appear in next steps? (YES/NO) |

Each subagent reads its input file, evaluates every entry, and writes a JSON array to its output file using this schema:

```json
[
  {
    "uco_id": "aAvVp...",
    "uco_name": "Use Case Name",
    "stage": "U3-Evaluating",
    "judgment": "YES",
    "reason": "One-sentence explanation."
  }
]
```

For **C1**: `judgment = "NO"` means no clear plan (will be flagged). For **C4**: `judgment = "YES"` means wrong stage (flagged). For **C7**: `judgment = "NO"` means no sizing justification (flagged). For **C8**: `judgment = "YES"` means partner mentioned but not attached (flagged). For **C9**: `judgment = "YES"` means active blocker in next steps (flagged).

Wait for all subagents to complete before proceeding to Phase 3.

**Phase 3: Apply all judgments (Python)**

Load all judgment files and merge with rule-based issues:

```python
import json, sys, glob, os
paths = glob.glob(os.path.expanduser(
    "~/.claude/plugins/cache/fe-vibe/fe-ee/*/skills/ae-uco-hygiene/resources"
))
if paths:
    sys.path.insert(0, paths[0])
import uco_hygiene

data = json.load(open("/tmp/uco_data.json"))
cols = [c["name"] for c in data["manifest"]["schema"]["columns"]]
ucoes = [dict(zip(cols, r)) for r in data["result"]["data_array"]]
by_id = {u["Usecase_ID"]: u for u in ucoes}
cq = ucoes[0]["current_fy_quarter"] if ucoes else None

rule_issues   = json.load(open("/tmp/rule_issues.json"))
# Merge all C1 batch judgment files into one list
import glob as _glob
c1_batch_files = sorted(_glob.glob("/tmp/c1_judgments_batch_*.json"))
c1_judgments = []
for bf in c1_batch_files:
    c1_judgments.extend(json.load(open(bf)))
c4_judgments  = json.load(open("/tmp/c4_judgments.json"))
c7_judgments  = json.load(open("/tmp/c7_judgments.json"))
c8_judgments  = json.load(open("/tmp/c8_judgments.json"))
c9_judgments  = json.load(open("/tmp/c9_judgments.json"))
c1_candidates = json.load(open("/tmp/c1_candidates.json"))

all_issues = (
    rule_issues
    + uco_hygiene.apply_c1_judgments(c1_judgments, c1_candidates)
    + uco_hygiene.apply_c4_judgments(c4_judgments)
    + uco_hygiene.apply_c7_judgments(c7_judgments)
    + uco_hygiene.apply_c8_judgments(c8_judgments)
    + uco_hygiene.apply_c9_judgments(c9_judgments)
)

# Group by AE, attach urgency, sort by $DBUs
from collections import defaultdict
by_ae = defaultdict(list)
for issue in all_issues:
    orig = by_id.get(issue["uco_id"], {})
    urgency = uco_hygiene.get_urgency(
        orig.get("onboard_fy_quarter"), orig.get("golive_fy_quarter"), cq
    )
    if urgency is None:
        continue
    ae = orig.get("Account_AE", "Unknown")
    by_ae[ae].append({**issue, "urgency": urgency,
                       "monthly_dbu": float(orig.get("Monthly_UCO_Dollar_DBUs") or 0),
                       "account": orig.get("Account", "")})

with open("/tmp/uco_issues_by_ae.json", "w") as f:
    json.dump(dict(by_ae), f, indent=2, default=str)
print(f"AEs with issues: {len(by_ae)} | Total flagged: {len(all_issues)}")
```

**Remediation to include in message:**
- Update Next Steps with a clear plan: what's happening, what the blocker is (if any), and when this project is expected to advance to the next stage

---

#### Condition 2: UCO with Stale Next Steps

Flag a UCO if **all** of the following are true:
- Stage is **U2, U3, U4, or U5**
- The `next_steps_modified_date` field is stale:
  - **More than 7 days ago** — if the UCO's monthly $DBU is >$10,000 AND the stage is U3 or higher
  - **More than 14 days ago** — for all other UCOs in U2–U5

> Use `next_steps_modified_date` — do NOT parse dates from the Next Steps text, which can contain typos and inconsistent formats.

**Implementation:** Condition 2 is evaluated by `uco_hygiene.evaluate_conditions()` in the Phase 1 script using the shared thresholds (`STALE_DAYS = 14`, `STALE_DAYS_HIGH_SPEND = 7`, `HIGH_SPEND_THRESHOLD = 10000`). Results appear in `result["rule_issues"]` with `condition == 2`.
```

**Remediation to include in message:**
- Update Next Steps with current status

---

#### Condition 3: Breached UCO

Flag a UCO if either of the following is true:
- The UCO has an **onboarding date in the past** but has **not yet reached U5** (Onboarding)
- The UCO has a **go-live date in the past** but has **not yet reached U6** (Live)

**Remediation to include in message:**
- If the project is still active: update the onboarding/go-live date to reflect the new expected timeline
- If the project has progressed: advance the UCO stage to match reality (U5 or U6)
- If the project is stalled or lost: update the stage/status accordingly

---

#### Condition 4: Wrong Stage Based on Next Steps

Flag a UCO if the content of the **Next Steps** field indicates the project is in a **different stage** than what Salesforce currently shows.

**Implementation:** Phase 1 saves C4 candidates (current/next quarter UCOs with non-empty next steps) to `/tmp/c4_candidates.json`. A dedicated subagent in Phase 2 reads this file and assesses whether each UCO's next steps are consistent with the current stage, using the stage definitions below as its rubric.

**Stage definitions:**
- **U1 (Validating):** Initial interest, exploring fit, no formal evaluation commitment
- **U2 (Scoping):** Requirements defined, solution approach agreed, POC scope documented
- **U3 (Evaluating):** Active POC or technical evaluation underway
- **U4 (Confirming):** Technical win secured, POC complete, customer committed to moving forward — awaiting deployment
- **U5 (Onboarding):** Active technical deployment in progress, customer has started building
- **U6 (Live):** In steady-state production use

**Signal phrases that suggest a stage mismatch (examples):**
- Next steps say "technical win secured" or "customer committed" → likely should be U4+, not U3
- Next steps say "POC complete" or "approved to proceed" → likely should be U4+, not U3
- Next steps say "actively deploying" or "in production" → likely should be U5/U6, not U3/U4
- Next steps say "still scoping" or "requirements TBD" → likely should be U2, not U3+

Only flag if the mismatch is clearly supported by the next steps text. When in doubt, do not flag.

**This condition falls under "Possible Issue Identified, Please Review"** — the AE needs to confirm.

**Remediation to include in message:**
- Review the current stage and advance if appropriate, using hedging language (e.g. "Next steps suggest this may be ready to advance to U4 — please review and update the stage if appropriate.")

---

#### Condition 5: Risky Onboarding or Go-Live Timeline

Flag a UCO if the onboarding or go-live dates appear unrealistic given the current stage. Examples:

- A UCO in **U1** with an onboarding date **within the next 1 month**
  _(A project that hasn't been scoped can't onboard within a month)_
- A UCO where the **go-live month is the same as the onboarding month**
  _(Onboarding and going live in the same month is rarely realistic)_

Use judgment on other timing mismatches — the goal is to flag dates that create false pipeline expectations.

**Language note:** Because these are flagged as "Possible Issue", use hedging language — not definitive statements. Both the issue description and the action should be non-prescriptive. The AE needs to review and decide, not be told what the problem is.
- Issue: say "this may be too compressed" not "this is too compressed"
- Action: say "if appropriate" — e.g. "Update go-live date to allow adequate onboarding time if appropriate."

**Remediation to include in message:**
- Review and update the onboarding/go-live dates if appropriate given the current stage

---

#### Condition 6: U1–U3 UCO with Onboarding Date This Month

Flag a UCO if **all** of the following are true:
- Stage is **U1, U2, or U3**
- The onboarding date falls in the **current calendar month**

A project that is still being validated, scoped, or evaluated has a very short runway to complete technical confirmation, deployment setup, and reach U5 (Onboarding) within the current month. This may indicate the date is a placeholder or hasn't been updated to reflect reality.

**This condition falls under "Possible Issue Identified, Please Review"** — the AE needs to confirm whether the month is accurate.

**Language note:** Use hedging language — the AE may have a legitimate reason for the date.

**Implementation:** Condition 6 is evaluated by `uco_hygiene.evaluate_conditions()` in the Phase 1 script. Results appear in `result["rule_issues"]` with `condition == 6`.

**Remediation to include in message:**
- Confirm that the onboarding month is accurate given the current stage and update if needed

---

#### Condition 7: Large UCO Without Sizing Justification

Flag a UCO if **all** of the following are true:
- Stage is **U3, U4, or U5**
- Monthly $DBU is **> $5,000**
- The UCO description does **not** contain a justification for the size (e.g., a breakdown of how the estimate was derived, or a link to a sizing tool's output)

**Judgment type:** AI judgment. Claude reads the `UCO_Description` field and determines whether it contains a credible sizing rationale.

**What counts as justification:** A description of the workload (e.g., job types, cluster sizes, data volumes) that plausibly explains the $DBU estimate, OR a link to a sizing tool (Quicksizer, etc.). A vague mention of "large production workload" or a placeholder does NOT count.

**This condition falls under "Take Action"** — large UCOs need to be defensible.

**Implementation:** Phase 1 extracts C7 candidates (U3/U4/U5, >$5,000/mo) into `/tmp/c7_candidates.json`. A dedicated subagent in Phase 2 evaluates each and writes `/tmp/c7_judgments.json` with `judgment: "NO"` (no justification — flagged) or `"YES"` (justification present — not flagged).

**Remediation to include in message:**
- Add a description that explains how the UCO size was determined, or link to a sizing tool's output.

---

#### Condition 8: Partner Mentioned, Not Attached to UCO

Flag a UCO if **all** of the following are true:
- Stage is **U3, U4, or U5**
- An implementation partner (e.g., Zeb, V4C, Koantek, Deloitte, Accenture, or similar SI/consulting firm) is mentioned in the `UCO_Description` or `Next_Steps` text
- The `Partner` field for the UCO is empty or null

**Judgment type:** AI judgment. Claude reads the description and next steps text, identifies any partner references, and compares against whether the `Partner` field is populated.

**This condition falls under "Possible Issue Identified, Please Review"** — the AE needs to confirm.

**Implementation:** Phase 1 extracts C8 candidates (U3/U4/U5, `Partner` field empty) into `/tmp/c8_candidates.json`. A dedicated subagent in Phase 2 evaluates each and writes `/tmp/c8_judgments.json` with `judgment: "YES"` if a partner is mentioned but not attached.

**Remediation to include in message:**
- If a partner is involved in delivery, attach them to the UCO using the Partner field.

---

#### Condition 9: Blocker Mentioned, Not Attached to UCO

Flag a UCO if **all** of the following are true:
- Stage is **U3, U4, or U5**
- The `Next_Steps` text mentions a blocker (e.g., "BLOCKED", "blocker", "blocking issue", "no resolution path")
- The UCO has no blockers attached (use AI judgment on the next steps text to determine if a blocker is actively mentioned)

**Judgment type:** AI judgment. Claude reads the next steps and determines whether an active blocker is described.

**This condition falls under "Possible Issue Identified, Please Review"** — the AE needs to confirm and attach the blocker if appropriate.

**Implementation:** Phase 1 extracts C9 candidates (U3/U4/U5 with blocker language in next steps) into `/tmp/c9_candidates.json`. A dedicated subagent in Phase 2 evaluates each and writes `/tmp/c9_judgments.json` with `judgment: "YES"` if an active blocker is described.

**Remediation to include in message:**
- If the UCO is blocked, create and attach a Blocker record to the UCO so it is tracked and visible to leadership.

---

### Next Steps Recency

Always use the **`next_steps_modified_date`** field (ISO format, e.g. `2026-02-03`) to determine how recently Next Steps were updated. Do not parse dates from the Next Steps text — the free-form text can contain typos (e.g. `02/167/2026`) and inconsistent formats that make parsing unreliable.

**Date parsing:** Use `uco_hygiene.parse_iso_date(s)` from the shared module. It handles `%Y-%m-%d`, ISO datetime variants, and the `Z` suffix correctly.

---

## Step 3: Draft Slack Messages Per AE (Parallel)

Load `/tmp/uco_issues_by_ae.json`. For each AE with problem UCOs, **launch a subagent** to compose their Slack message draft. All AE subagents run simultaneously — do not draft messages sequentially.

Each subagent receives: the AE's name, their list of flagged UCOs (with urgency, issues, monthly $DBUs, and Salesforce URLs), and the message template below. It writes its output to `/tmp/ae_draft_<ae_lastname>.md`.

Wait for all subagents to complete, then concatenate their outputs into `/tmp/uco_hygiene_drafts.md` for Google Doc conversion in Step 4.

> **IMPORTANT: Do NOT send any messages.** Present all drafts to the user for review. The user will send them manually.

### Message Structure

Messages have **two top-level sections** based on date urgency, and within each, UCOs are further grouped by inspection bucket:

**🚨 Urgent** (top level) — UCO has an onboarding or go-live date within the **current** Databricks fiscal quarter.

**Needs Attention** (top level) — UCO has an onboarding or go-live date within the **next** Databricks fiscal quarter.

**UCOs whose onboarding and go-live dates fall outside the current or next fiscal quarter are excluded from the message entirely.**

Within each section, UCOs are ordered by **monthly $DBUs descending** (highest spend first).

The inspection bucket ("Take Action" or "Possible Issue Identified, Please Review") is shown as a label on each UCO line item — not as a sub-section header.

#### Stale Next Steps Consolidation

UCOs that **only** trigger Condition 2 (stale next steps, no other conditions) are grouped into a compact **📋 Stale Next Steps** summary block at the top of their section, rather than being listed individually. This avoids repeating the same boilerplate action for every UCO.

> **ORDERING RULE — strictly enforced:** Within each urgency section (Urgent / Needs Attention), the **📋 Stale Next Steps block ALWAYS comes first**, before the **📋 Other Issues block**. Never reverse this order.

- State the action once at the top of the block: _"please update each with current status"_
- List each UCO on one line with: account name, use case name, stage, monthly $DBUs, and days since last update
- Place the Salesforce URL on the line below each UCO
- Still sort by monthly $DBUs descending within the block

UCOs that trigger **any other condition** in addition to (or instead of) Condition 2 are always shown in the full individual format with their own Issue and Action lines.

> Databricks fiscal year begins in **February**. Fiscal quarters:
> - Q1: Feb, Mar, Apr
> - Q2: May, Jun, Jul
> - Q3: Aug, Sep, Oct
> - Q4: Nov, Dec, Jan
>
> Use the `current_fy_quarter` field from the logfood query to determine the current quarter — do not compute it manually.
>
> To compute the next quarter:
> - Q1 → Q2 (same FY year)
> - Q2 → Q3 (same FY year)
> - Q3 → Q4 (same FY year)
> - Q4 → Q1 of the next FY year (e.g., FY27-Q4 → FY28-Q1)

Omit any section or subsection that has no UCOs. If an AE has no UCOs in the current or next quarter, do not draft a message for them.

### Message Template

```
Hey [First Name]! Quick UCO hygiene check-in.

I reviewed your active use cases and have some flagged for attention:

---

🚨 Urgent (onboarding or go-live this quarter)

📋 Stale Next Steps — please update each with current status:
  • [Account Name] — [Use Case Name] | [Stage] | $X,XXX/mo | [N] days since update
    [Salesforce UCO URL]
  • [Account Name] — [Use Case Name] | [Stage] | $X,XXX/mo | [N] days since update
    [Salesforce UCO URL]

📋 Failing hygiene checks — please look at the Issue field for details:

[Account Name] — [Use Case Name]
[Salesforce UCO URL]
Monthly $DBUs: $X,XXX  |  ⚡ Take Action
Stage: [UCO Stage]
Issue: [Plain-English explanation]
Action: [Specific remediation steps]

[Account Name] — [Use Case Name]
[Salesforce UCO URL]
Monthly $DBUs: $X,XXX  |  👀 Possible Issue Identified, Please Review
Stage: [UCO Stage]
Issue: [Plain-English explanation]
Action: [Specific remediation steps]

---

Needs Attention (onboarding or go-live next quarter)

📋 Stale Next Steps — please update each with current status:
  • [Account Name] — [Use Case Name] | [Stage] | $X,XXX/mo | [N] days since update
    [Salesforce UCO URL]

---

Let me know if you have questions or anything looks off!
```

> **Note:** Only include a 📋 Stale Next Steps block if there are UCOs that trigger Condition 2 only. Omit it (and its header) if no such UCOs exist in that section.

> **Note on condition labels:** Do **not** include condition reference numbers (e.g., "C1:", "C2:", "C7:") in the Issue or Action fields. Recipients don't know what these codes mean. Write in plain English only. When a UCO triggers multiple conditions, join each condition's explanation with ` | ` — no prefixes.

UCOs within each section are ordered by monthly $DBUs descending.

**Tone:** Friendly and collegial — this is a heads-up, not a reprimand.

**If an AE has no problem UCOs:** Do not draft a message for them. Note them in the summary as "clean."

### Salesforce UCO URL Format

```
https://databricks.lightning.force.com/lightning/r/UseCase__c/[UCO_ID]/view
```

---

## Step 4: Deliver Drafts as a Google Doc

**Always deliver the audit results as a Google Doc** — do NOT print messages in the terminal. Google Docs preserves bold and bullet formatting when copy-pasted into Slack, which makes it easy for the manager to send the messages.

### 4a: Write the Markdown File

Write the full audit output to `/tmp/uco_hygiene_drafts.md` using this structure:

```markdown
# UCO Hygiene Audit — [DATE]

**Summary:** X AEs reviewed · Y AEs with problem UCOs · Z UCOs flagged

**AEs with clean hygiene:** [Name], [Name]

---

## [AE First Name Last Name]

Hey [First Name]! Quick UCO hygiene check-in.

I reviewed your active use cases and have some flagged for attention:

---

### URGENTICON Urgent (onboarding or go-live this quarter)

#### STALEICON Stale Next Steps — please update each with current status:

- [Account — Use Case](Salesforce UCO URL) | [Stage] | $X,XXX/mo | [N] days since update

#### STALEICON Failing hygiene checks — please look at the Issue field for details:

[Account Name — Use Case Name](Salesforce UCO URL)
Monthly $DBUs: $X,XXX | ⚡ Take Action
Stage: [UCO Stage]
Issue: [Plain-English explanation]
Action: [Specific remediation steps]
BLANKLINEMARKER

---

### Needs Attention (onboarding or go-live next quarter)

...

---

Let me know if you have questions or anything looks off!

---

## [Next AE Name]

...
```

**Formatting rules — CRITICAL for correct rendering:**

1. **No non-BMP emoji in the markdown file.** Emoji above Unicode U+FFFF (🚨 U+1F6A8, 📋 U+1F4CB, 👀 U+1F440) count as 1 Python character but 2 UTF-16 code units in Google Docs, causing `insertText` index drift that merges paragraphs. Use ASCII placeholders instead, then swap after doc creation:
   - `🚨` → write `URGENTICON` in markdown
   - `📋` → write `STALEICON` in markdown
   - `👀` → write `EYESICON` in markdown
   - `⚡` (U+26A1) is BMP-safe — use directly

2. **No bold link syntax.** `**[text](url)**` causes the bold pattern to match first, rendering `[text](url)` as literal bold text with no hyperlink. Use `[text](url)` (no bold wrapper) for all UCO name links.

3. **Use `### ` headings** for section labels (Urgent / Needs Attention) and `#### ` for Stale Next Steps subheading.

4. **Use `- ` bullet lists** for stale next steps blocks.

5. **Blank line between full UCO entries**: after each entry's last Action line, add a line containing `BLANKLINEMARKER` (no underscores — underscores trigger the italic parser and split the placeholder across runs, breaking `replaceAllText`). Then in the post-processing step, replace `BLANKLINEMARKER` with `""` — leaving each paragraph containing only Google Docs' implicit `\n`, which renders as a blank line.

6. Each AE's message starts with a `## [Full Name]` heading so sections are easy to navigate in the doc.

6. Only include sections (Urgent / Needs Attention) that have UCOs.

### 4b: Convert to Google Doc and Swap Emoji Back

First, convert the markdown to a Google Doc:

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/uco_hygiene_drafts.md \
  --title "UCO Hygiene Audit — [DATE]"
```

Then, replace the placeholders with the actual emoji using `replaceAllText`:

```bash
TOKEN=$(gcloud auth application-default print-access-token)
curl -s -X POST "https://docs.googleapis.com/v1/documents/${DOC_ID}:batchUpdate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{
    "requests": [
      {"replaceAllText": {"containsText": {"text": "URGENTICON",      "matchCase": true}, "replaceText": "🚨"}},
      {"replaceAllText": {"containsText": {"text": "STALEICON",       "matchCase": true}, "replaceText": "📋"}},
      {"replaceAllText": {"containsText": {"text": "EYESICON",        "matchCase": true}, "replaceText": "👀"}},
      {"replaceAllText": {"containsText": {"text": "BLANKLINEMARKER", "matchCase": true}, "replaceText": ""}}
    ]
  }'
```

### 4c: Present the Result

After the Google Doc is created, present a brief summary in the terminal and share the link:

```
UCO Hygiene Audit Complete — [DATE]

Summary:
  • X AEs reviewed
  • Y AEs have problem UCOs
  • Z total UCOs flagged

AEs with clean hygiene: [Name], [Name]

📄 Draft messages: [Google Doc URL]

To send: open the doc, find the section for each AE, and copy/paste their message into a Slack DM.
Bold text and bullets will carry over correctly when pasting from Google Docs into Slack.
```

### 4d: Suggest TAP Review for Flagged Accounts

After presenting the audit results, review the flagged UCOs. If any **account** has 3 or more flagged UCOs, or has any UCO flagged with Condition 1 (stuck in stage), suggest running a full TAP review:

```
Accounts with significant hygiene issues may benefit from a full TAP review:
  - <Account Name> (X flagged UCOs) — consider running `/tap-review <Account Name>`
```

This is a **suggestion only** — do not automatically invoke the TAP review skill. The manager can decide whether to run it for specific accounts.

---

## References

- `references/hygiene-rules.md` — Detailed hygiene rule rationale and edge cases
- `resources/uco_hygiene.py` — UCO hygiene condition evaluation engine (C1-C6)
- [UCO Stage Definitions (Slide 21)](https://docs.google.com/presentation/d/1_z0IaADnLGw0xvO8mc-vHs4OtMxGrioqZdZtF2VTa3k/edit?slide=id.g2c55090f353_6_2449)
- [UCO Management Guidelines](https://docs.google.com/document/d/1cLx2xjQ8YqdxvJeFRIi3Z20xPgnaD-Mu_RNEKdzT8oM)

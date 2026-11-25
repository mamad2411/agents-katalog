---
name: uco-hygiene-review
description: Review UCO hygiene for a sales territory — identify stale records, missing fields, and stage issues. Use when the user says "UCO hygiene", "review UCOs", "check UCO health", "audit UCOs", or "hygiene review".
user-invocable: true
---

# UCO Hygiene Review

Reviews active UCOs for a territory, identifies hygiene issues, and drafts remediation guidance.

## Step 1: Ensure Territory Context

Check whether a territory has already been set in this session (i.e., `sfdc_region_l2` is known from a prior `set-territory` invocation).

- **If territory is already set:** confirm it with the user before proceeding.
  > "Using territory: **[User Name]** — [Region L2]. Proceed?"
- **If not set:** invoke the `set-territory` skill now before continuing.

The key value needed downstream is **`sfdc_region_l2`** (e.g., `FINS ProServ & FinTech SLM`). This maps directly to `region_level_2` in `main.gtm_silver.use_case_detail`.

---

## Step 2: Query UCOs

### Prerequisites

1. Verify logfood auth: `databricks auth profiles | grep logfood`
2. Use warehouse **Shared SQL Endpoint - Stable** (`927ac096f9833442`) on `--profile=logfood`

### Run the UCO Query

> **CRITICAL:** Write the request body to a file — do NOT inline the SQL in a `--json='...'` shell argument. The SQL contains single-quoted `IN` lists that will break single-quoted shell strings.

Read `sql/get-ucos.sql` and substitute the three placeholders, then write `/tmp/uco_query.json`:

```python
import json

REGION_L1 = "<sfdc_region_l1 if set, else 'All'>"       # e.g. "FINS" or "All"
REGION_L2 = "<sfdc_region_l2 if set, else 'All'>"       # e.g. "FINS ProServ & FinTech SLM" or "All"
REGION_L3 = "<sfdc_region_l3 if set, else 'All'>"       # e.g. "FINS PS - Audit/Advisory" or "All"

sql = open("sql/get-ucos.sql").read()
query = (sql
    .replace("<region_l1>", REGION_L1)
    .replace("<region_l2>", REGION_L2)
    .replace("<region_l3>", REGION_L3))

with open('/tmp/uco_query.json', 'w') as f:
    json.dump({
        'statement': query,
        'warehouse_id': '927ac096f9833442',
        'format': 'JSON_ARRAY',
        'wait_timeout': '50s'
    }, f)
```

```bash
databricks api post /api/2.0/sql/statements/ \
  --json=@/tmp/uco_query.json --profile=logfood > /tmp/uco_data.json
```

### Region Mapping

`sfdc_users_mapping` fields → `main.gtm_silver.use_case_detail` fields:

| Territory context | Query filter | Pass `'All'` when |
|---|---|---|
| `sfdc_region_l1` | `region_level_1` | not set |
| `sfdc_region_l2` | `region_level_2` | not set |
| `sfdc_region_l3` | `region_level_3` | not set |

Use the most specific level(s) that are set. Unset levels pass `'All'` and include everything beneath them.

### Confirm Results

After the query succeeds, print a summary grouped by AE:

```python
import json
from collections import defaultdict

data = json.load(open('/tmp/uco_data.json'))
cols = [c['name'] for c in data['manifest']['schema']['columns']]
rows = data.get('result', {}).get('data_array', [])
ucoes = [dict(zip(cols, r)) for r in rows]

by_ae = defaultdict(list)
for u in ucoes:
    by_ae[u['account_executive']].append(u)

CQ = "FY'27 Q1"
CQ1 = "FY'27 Q2"
print(f"Total UCOs: {len(ucoes)} across {len(by_ae)} AEs")
print(f"{'AE':<30} {'Total':>5}  {'$/mo':>12}  {'CQ':>4}  {'CQ+1':>5}")
print("-" * 65)
for ae, ulist in sorted(by_ae.items()):
    total_dbu = sum(float(u['estimated_monthly_dollar_dbus'] or 0) for u in ulist)
    cq_n  = sum(1 for u in ulist if u.get('target_go_live_fiscal_year_quarter') == CQ)
    cq1_n = sum(1 for u in ulist if u.get('target_go_live_fiscal_year_quarter') == CQ1)
    print(f"  {ae:<28} {len(ulist):>5}  ${total_dbu:>10,.0f}  {cq_n:>4}  {cq1_n:>5}")
```

Show the user the summary and confirm before proceeding to hygiene analysis.

---

## Step 3: Hygiene Analysis

### 3a — Deterministic Flag Pass (Python)

**Before running the flag pass**, use `AskUserQuestion` to ask:

```
Which quarters would you like to include in this review?
  A) CQ only  (FY'XX QN — ends [date])
  B) CQ+1 only  (FY'XX QN+1 — ends [date])
  C) Both CQ and CQ+1
```

Set `SELECTED_QUARTERS` based on the answer before running the code block below.

Run this block against the loaded UCOs. It scores every UCO against six rule-based conditions and produces a flag summary. No AI judgment is needed here.

```python
import json
from datetime import date, datetime, timedelta
from collections import defaultdict

# --- Load data ---
data = json.load(open('/tmp/uco_data.json'))
cols = [c['name'] for c in data['manifest']['schema']['columns']]
rows = data.get('result', {}).get('data_array', [])
ucoes = [dict(zip(cols, r)) for r in rows]

today = date.today()
start_of_month = today.replace(day=1)  # Dates are always written as the 1st; any day in the month is valid

def parse_date(s):
    return datetime.strptime(s, '%Y-%m-%d').date() if s else None

def as_float(v):
    try: return float(v)
    except: return 0.0

# --- Quarter setup ---
# Databricks FY: Q1=Feb–Apr, Q2=May–Jul, Q3=Aug–Oct, Q4=Nov–Jan
m = today.month
if m in (2, 3, 4):   q_num, fy = 1, today.year + 1
elif m in (5, 6, 7): q_num, fy = 2, today.year + 1
elif m in (8, 9,10): q_num, fy = 3, today.year + 1
elif m in (11, 12):  q_num, fy = 4, today.year + 1
else:                q_num, fy = 4, today.year   # January

CQ_LABEL  = f"FY'{str(fy)[2:]} Q{q_num}"
CQ1_LABEL = f"FY'{str(fy)[2:]} Q{q_num+1}" if q_num < 4 else f"FY'{str(fy+1)[2:]} Q1"

# End date of current quarter (for stage velocity calculations)
if   q_num == 1: cq_end_date = date(today.year, 4, 30)
elif q_num == 2: cq_end_date = date(today.year, 7, 31)
elif q_num == 3: cq_end_date = date(today.year, 10, 31)
elif m in (11, 12): cq_end_date = date(today.year + 1, 1, 31)
else:            cq_end_date = date(today.year, 1, 31)  # January

days_remaining_in_cq = (cq_end_date - today).days

# Set from AskUserQuestion answer before running this block:
#   'CQ'      → SELECTED_QUARTERS = [CQ_LABEL]
#   'CQ+1'    → SELECTED_QUARTERS = [CQ1_LABEL]
#   'Both'    → SELECTED_QUARTERS = [CQ_LABEL, CQ1_LABEL]
SELECTED_QUARTERS = [CQ_LABEL, CQ1_LABEL]  # default: both

# --- Flag definitions ---
# Each flag returns (flag_code, message) or None

# Days-in-stage thresholds for U2–U4:
#   base       — flag regardless of live date (genuinely slow-moving)
#   pressure   — flag when days_in_stage > pressure AND live date is within pressure_live days
#   (U2 has no live-date pressure because a near-term live date from a U2 is itself a separate problem)
# U5 uses a different approach — see flag_long_in_stage below.
LONG_IN_STAGE_THRESHOLDS = {
    'U1': {'base': 180, 'pressure': None, 'pressure_live': None},
    'U2': {'base': 180, 'pressure': None, 'pressure_live': None},
    'U3': {'base': 120, 'pressure': 75,   'pressure_live': 90},
    'U4': {'base': 90,  'pressure': 60,   'pressure_live': 90},
}

def flag_long_in_stage(u):
    """Stage velocity — days_in_stage exceeds stage-appropriate threshold.

    U5 is treated differently: implementation windows vary widely (weeks to 12+ months),
    so a fixed threshold would produce false positives on large, planned-long projects.
    Instead, U5 is flagged only when days_in_stage has overrun the planned window
    (target_live_date - target_onboarding_date). If both dates are missing, fall back to 120d.
    """
    stage = u.get('stage', '')
    days = as_float(u.get('days_in_stage'))
    live = parse_date(u.get('target_live_date'))
    days_to_live = (live - today).days if live else None

    if stage == 'U5':
        onboard = parse_date(u.get('target_onboarding_date'))
        if onboard and live and live > onboard:
            planned = (live - onboard).days
            if days > planned:
                return ('LONG_IN_STAGE', f'{int(days)}d in U5, planned window {planned}d (overrun)')
        else:
            # Fallback: no valid onboarding/live dates — use fixed threshold
            if days > 120:
                return ('LONG_IN_STAGE', f'{int(days)}d in U5 (no planned window)')
        return None

    t = LONG_IN_STAGE_THRESHOLDS.get(stage)
    if not t:
        return None

    ns_date = parse_date(u.get('next_steps_last_modified_date'))
    recently_updated = ns_date is not None and (today - ns_date).days <= 14

    # Suppress both base and pressure hits when the team is actively managing —
    # STALE already covers "no recent activity"; LONG_IN_STAGE should only fire
    # on UCOs that are both slow AND going quiet.
    base_hit = days > t['base'] and not recently_updated
    pressure_hit = (
        t['pressure'] is not None
        and days > t['pressure']
        and days_to_live is not None
        and 0 <= days_to_live <= t['pressure_live']
        and not recently_updated
    )
    if base_hit or pressure_hit:
        msg = f'{int(days)}d in {stage}'
        if pressure_hit and not base_hit:
            msg += f' + live in {days_to_live}d'
        return ('LONG_IN_STAGE', msg)
    return None

def flag_stale(u):
    """Next steps not updated in >14 days (for UCOs $5K+)."""
    dbu = as_float(u.get('estimated_monthly_dollar_dbus'))
    ns_date = parse_date(u.get('next_steps_last_modified_date'))
    if dbu < 5000:
        return None
    if ns_date and (today - ns_date).days > 14:
        return ('STALE', f'No NS update in {(today - ns_date).days}d (last: {ns_date})')
    return None

def flag_breached_dates(u):
    """Target onboarding or live date is in a prior month without advancing stage.

    Dates are always written as the 1st of the month by Salesforce.
    Any day within the current month is still valid — breach only occurs
    when the entire month has passed (i.e., date < start_of_month).
    """
    stage = u.get('stage', '')
    live = parse_date(u.get('target_live_date'))
    onboard = parse_date(u.get('target_onboarding_date'))
    msgs = []
    if live and live < start_of_month and stage in ('U1','U2','U3','U4','U5'):
        msgs.append(f'live date {live.strftime("%b %Y")}')
    if onboard and onboard < start_of_month and stage in ('U1','U2','U3','U4'):
        msgs.append(f'onboarding {onboard.strftime("%b %Y")}')
    return ('BREACHED', ' | '.join(msgs)) if msgs else None

# Shrinkage is NOT a flag — this review is about pipeline hygiene, not forecasting.
# Slippage is NOT a flag — it is shown as informational metadata on the stats line.
# Use slippage_count to display "Nx slip" inline (e.g., "U4 · $30K/mo · Live Apr 2026 · 90d · 2x slip · BREACHED").
# Do not include flag_slippage in FLAG_FNS.

def flag_risky_timeline(u):
    """Live date within 45 days (or current month) but still in U3 or U4.

    Uses start_of_month for the lower bound since dates are always written as the 1st —
    a live date of the 1st of the current month is still valid (not breached).
    """
    stage = u.get('stage', '')
    live = parse_date(u.get('target_live_date'))
    if stage in ('U3', 'U4') and live and live >= start_of_month and (live - start_of_month).days <= 45:
        return ('RISKY_TIMELINE', f'Live {live.strftime("%b %Y")} but still in {stage}')
    return None

def flag_stage_velocity(u):
    """Stage is too early to realistically close in its target quarter.

    As the quarter progresses, UCOs with an early stage relative to their target
    quarter should either accelerate or be pushed out to a later quarter.

    CQ rules (based on days remaining in the current quarter):
    - U2 targeting CQ: flag when < 45d remaining (past mid-quarter — ~90d to close is impossible)
    - U3 targeting CQ: flag when < 30d remaining (final month — U3→U5 in <30d is very risky)

    CQ+1 rules:
    - U2 targeting CQ+1: flag when < 45d remaining in CQ — a U2 needs 90+ days to reach live,
      so it must advance to U3+ before CQ+1 starts or it will be late again.
    """
    stage = u.get('stage', '')
    q = u.get('target_go_live_fiscal_year_quarter', '')

    if stage not in ('U2', 'U3'):
        return None

    if q == CQ_LABEL:
        if stage == 'U2' and days_remaining_in_cq < 45:
            return ('STAGE_VELOCITY', f'U2 in CQ with {days_remaining_in_cq}d left — advance to U3+ or push to CQ+1')
        if stage == 'U3' and days_remaining_in_cq < 30:
            return ('STAGE_VELOCITY', f'U3 in CQ with {days_remaining_in_cq}d left — advance to U4+ or push to CQ+1')

    elif q == CQ1_LABEL:
        if stage == 'U2' and days_remaining_in_cq < 45:
            return ('STAGE_VELOCITY', f'U2 in CQ+1 with {days_remaining_in_cq}d until CQ+1 — needs U3+ to close in {CQ1_LABEL}')

    return None

def flag_blockers(u):
    """Hard blocker on a UCO within the reviewed quarters.

    Only flags when ALL three conditions are met:
    1. Blocker type is 'Blocked' (not 'Friction' — friction is noise)
    2. Blocker category is NOT 'Customer Blocker (unrelated to Databricks)' — not actionable by us
    3. Live date is in SELECTED_QUARTERS — blockers outside the review scope can wait
    """
    if u.get('has_blockers_ind') not in (True, 'true'):
        return None
    btype = u.get('last_modified_blocker_type') or ''
    bcat  = u.get('last_modified_blocker_category') or ''
    q     = u.get('target_go_live_fiscal_year_quarter') or ''
    if btype != 'Blocked':
        return None
    if 'unrelated to Databricks' in bcat:
        return None
    if q not in SELECTED_QUARTERS:
        return None
    n = u.get('num_blockers', '?')
    detail = f'{n} blocker(s) [{bcat}]' if bcat else f'{n} blocker(s)'
    return ('BLOCKER', detail)

def flag_notes_risk(u):
    """Scan demand_plan_next_steps for signals that contradict stage/live date.

    Catches paused deals, active competitor evaluations, stage regression signals,
    explicit push-out or at-risk language, status color flags (Red/Yellow),
    timeline push-outs, new AE takeovers, and product GA dependencies.
    This is the only flag that reads free text — it surfaces cases where the notes
    say one thing and Salesforce shows another (e.g., stage still U5 but notes say
    "paused, evaluating Dataproc, EoY timing, need to requalify").

    Only fires for UCOs in SELECTED_QUARTERS with $5K+ DBU/mo to reduce noise.
    """
    import re
    dbu = as_float(u.get('estimated_monthly_dollar_dbus'))
    if dbu < 5000:
        return None
    q = u.get('target_go_live_fiscal_year_quarter') or ''
    if q not in SELECTED_QUARTERS:
        return None
    raw_notes = (u.get('demand_plan_next_steps') or '').strip()
    if not raw_notes:
        return None

    def most_recent_entry(text):
        """Return only the first (most recent) entry to avoid firing on stale language.

        Entries are separated by blank lines or by a new date stamp at the start of a line.
        Common date formats: '2/26 AB:', 'CR 2/18:', 'Feb-23 - AB -', '02/24/26 SK:', '3.3 CK-', '1/29:'.
        Handles initials-prefixed dates like 'CR 2/18' or 'RB 11/24' (1-3 uppercase letters + space before date).
        Also stops at C:/N:/R:/W: structural section headers — these mark the historical log section
        in notes using Current/Next/Risk format, not the AE's current status line.
        """
        DATE_START = re.compile(
            r'^([A-Z]{1,3}\s+)?'
            r'(\d{1,2}[\/\.\-]\d{1,2}|[A-Za-z]{3}[\s-]\d{1,2}|\d{4}-\d{2}-\d{2})'
        )
        SECTION_HEADER = re.compile(r'^[CNRW]:\s')
        lines = text.strip().split('\n')
        entry_lines, entry_started = [], False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                if entry_started:
                    break   # blank line ends first entry
                continue
            if entry_started and (DATE_START.match(stripped) or SECTION_HEADER.match(stripped)):
                break       # second date stamp or C:/N:/R: section header = stop
            entry_started = True
            entry_lines.append(stripped)
        if entry_lines:
            return ' '.join(entry_lines)
        return ' '.join(l.strip() for l in lines[:3] if l.strip())  # fallback

    notes = most_recent_entry(raw_notes).lower()
    if not notes:
        return None

    signals = []

    # Pause / hold / stalled / dark
    if re.search(
        r'\b(paused?|on[\s-]hold|halted|frozen|not moving forward|'
        r'stalled?|gone\s+dark|going\s+dark|radio\s+silence|no\s+response|'
        r'unresponsive|gone\s+quiet|lost\s+momentum|not\s+engaged)\b',
        notes
    ):
        signals.append('paused/held')

    # Competitor evaluation — broadened trigger verbs + extended competitor list
    COMPETITORS = [r'dataproc', r'snowflake', r'redshift', r'synapse', r'bigquery',
                   r'microsoft\s+fabric', r'azure\s+fabric', r'dbt\s+cloud',
                   r'palantir', r'c3\.ai', r'informatica', r'talend', r'alteryx',
                   r'teradata', r'cloudera', r'oracle', r'\bsas\b', r'power\s+bi',
                   r'qlik', r'looker', r'hadoop', r'hive']
    EVAL_TRIGGER = re.compile(
        r'\b(eval(uating)?|considering|looking\s+at|piloting|'
        r'benchmarking|poc\s+with|comparing)\b'
    )
    # Migration source check: skip if the competitor name appears in the UCO name
    # (e.g., "Synapse Takeout" or "FiveTran Data Ingest" — the competitor is the source being replaced)
    uco_name_lower = (u.get('usecase_name') or '').lower()
    if EVAL_TRIGGER.search(notes) or re.search(r'\bcompetitive\s+eval\b', notes):
        for comp in COMPETITORS:
            if re.search(comp, notes) and not re.search(comp, uco_name_lower):
                signals.append('evaluating competitor')
                break

    # Stage regression / rescoping / lost traction
    if re.search(
        r'\b(re[\s-]?qualif\w*|restart\b|re[\s-]start|not\s+in\s+queue|'
        r'start\s+over|restart\s+the\s+process|back\s+to\s+square\s+one|'
        r're[\s-]?scop|de[\s-]?scop|reducing\s+scope|lost\s+traction|'
        r'lost\s+the\s+deal|re[\s-]?evaluat|need\s+to\s+revisit|'
        r'pulled\s+back|going\s+back\s+to)\b',
        notes
    ):
        signals.append('stage regression')

    # Explicit push-out beyond near term
    # Suppress when EOY appears as a duration ("through EOY", "training through end of year")
    # rather than a push-out signal. "through/thru/into/all of" + EOY = ongoing work, not delay.
    EOY_MATCH = re.search(
        r'\b(end\s+of\s+(the\s+)?year|eoy|next\s+(fiscal\s+)?year|'
        r'h2\s+(fy|of\s+fy|\d{2,4})|second\s+half|back\s+half|'
        r'not\s+(this|in\s+this)\s+quarter|fy[\s\']?2[89])\b',
        notes
    )
    THROUGH_EOY = re.search(
        r'\b(through|thru|all\s+of|into|towards?)\s+(eoy|end\s+of\s+(the\s+)?year)\b',
        notes
    )
    if EOY_MATCH and not THROUGH_EOY:
        signals.append('end-of-year push-out')

    # Explicit risk / deprioritization / champion loss / org change / budget freeze / low priority
    if re.search(
        r'\b(at[\s-]risk|deprioritized|de[\s-]prioritized|not\s+a\s+priority|'
        r'low(?:er)?\s+priority|put\s+on\s+.*low\s+priority|'
        r'budget\s+(frozen|cut|eliminated|removed|cancelled|on\s+hold)|'
        r'cost\s+constraint|no\s+budget|unfunded|not\s+funded|'
        r'hiring\s+freeze|headcount\s+(reduction|freeze)|'
        r'company[\s-]?wide\s+reorg|org\s+(change|reorg)|reorgani[sz]ation|'
        r'leadership\s+change|personnel\s+changes?|change\s+in\s+(project\s+)?ownership|'
        r'\bpm\s+.*\bleft\b|\bpm\s+(quit|departed)|lost\s+champion|champion\s+(left|changed|gone)|'
        r'legal\s+hold|procurement\s+hold|lost\s+exec\s+support)\b',
        notes
    ):
        signals.append('at risk/deprioritized')

    # Plan off track — explicit statement that plan/project is not on track
    if re.search(
        r'\b(?:plan|project)\s+(?:is\s+)?(?:not\s+on\s+track|off[\s-]track)\b',
        notes
    ):
        signals.append('off track')

    # Fully blocked / no workaround / product blocker in notes
    if re.search(
        r'\b(fully\s+blocked|completely\s+blocked|blocked\s+by\s+product|'
        r'no\s+workaround|not\s+feasible|no\s+viable\s+(?:path|option|solution)|'
        r'(?:no|don.t\s+have\s+a)\s+(?:clear\s+)?path(?:\s+forward|\s+through)|'
        r'product\s+challenges|product\s+limitations|'
        r'continues\s+to\s+be\s+a\s+blocker|blocker\s+due\s+to|'
        r'clients?\s+(?:are\s+)?blocking)\b',
        notes
    ):
        signals.append('fully blocked')

    # Explicit status color (Red/Yellow) — AEs often write "Status: Red" or "[Red]"
    if re.search(
        r'(?:status[:\s]*(?:red|yellow)|'
        r'\[(?:red|yellow)\]|'
        r'scoping\s+status[:\s]*(?:red|yellow)|'
        r'evaluating\s+status[:\s]*(?:red|yellow))',
        notes
    ):
        color = 'red' if re.search(r'(?:(?:\w+\s+)?status[:\s]*red|\[red\])', notes) else 'yellow'
        signals.append(f'status {color}')

    # Pushing out / delayed timeline
    if re.search(
        r'\b(pushing\s+(out|this\s+out|go[\s-]live|use\s+case\s+out|live\s+date)|'
        r'moved\s+go[\s-]?live|delayed|slip(?:ping|ped|\b)|'
        r'pushing\s+(?:onboarding|target)\s+(?:out|back|date)|'
        r'pushed\s+out\s+to|not\s+targeted\s+at\s+the\s+moment|'
        r'recommends?\s+.*(?:moved?\s+out|pushed))\b',
        notes
    ):
        signals.append('timeline pushed')

    # New AE takeover — UCO may need requalification
    if re.search(
        r'\b(just\s+took\s+over|new\s+(?:ae|account\s+(?:exec|team))|'
        r'recently\s+(?:took\s+over|transitioned|inherited)|'
        r'account\s+transition|new\s+to\s+(?:this\s+)?account)\b',
        notes
    ):
        signals.append('new AE takeover')

    # Stage incorrect / needs requalification or more discovery
    if re.search(
        r'\b(stages?\s+(?:are?\s+)?incorrect|more\s+discovery\s+needed|'
        r'needs?\s+(?:to\s+be\s+)?requalif|recommends?\s+.*moved?\s+out)\b',
        notes
    ):
        signals.append('stage incorrect')

    # Waiting on product GA / feature dependency
    if re.search(
        r'\b(waiting\s+(?:for|on)\s+(?:ga|general\s+availability|product|feature)|'
        r'awaiting\s+ga|not\s+(?:yet\s+)?(?:ga|ready)|'
        r'pending\s+(?:ga|product\s+release)|blocked\s+on\s+(?:ga|product)|'
        r'until\s+.*\s+is\s+ga|depends\s+on\s+.*\s+ga)\b',
        notes
    ):
        signals.append('waiting on product GA')

    if signals:
        return ('NOTES_RISK', ' · '.join(signals))
    return None

FLAG_FNS = [flag_long_in_stage, flag_stale, flag_breached_dates,
            flag_risky_timeline, flag_stage_velocity, flag_blockers, flag_notes_risk]
# Note: slippage and shrinkage are NOT in FLAG_FNS — slippage shown as "Nx slip" metadata on the stats line

# --- Score all UCOs ---
flagged = []
for u in ucoes:
    flags = [fn(u) for fn in FLAG_FNS]
    flags = [f for f in flags if f]
    if flags:
        u['_flags'] = flags
        flagged.append(u)

# --- Print summary ---
by_ae = defaultdict(list)
for u in flagged:
    by_ae[u['account_executive']].append(u)

flag_counts = defaultdict(int)
for u in flagged:
    for code, _ in u['_flags']:
        flag_counts[code] += 1

print(f"\n=== Hygiene Flag Summary ===")
print(f"UCOs reviewed: {len(ucoes)} | Flagged: {len(flagged)}\n")
print("Flag breakdown:")
for code, cnt in sorted(flag_counts.items(), key=lambda x: -x[1]):
    print(f"  {code}: {cnt}")

print(f"\n=== By AE ===")
for ae in sorted(by_ae):
    ulist = by_ae[ae]
    total_dbu = sum(as_float(u.get('estimated_monthly_dollar_dbus')) for u in ulist)
    codes = [c for u in ulist for c, _ in u['_flags']]
    print(f"  {ae}: {len(ulist)} flagged UCOs, ${total_dbu:,.0f}/mo  [{', '.join(sorted(set(codes)))}]")
```

Save the results for Step 3b:

```python
import pickle
with open('/tmp/uco_flagged.pkl', 'wb') as f:
    pickle.dump({'ucoes': ucoes, 'flagged': flagged}, f)
print(f"Saved {len(flagged)} flagged UCOs to /tmp/uco_flagged.pkl")
```

Show the summary table to the user. Ask if they want to review all flagged UCOs or scope to a specific AE before proceeding.

---

### 3b — Report Generation (Python)

Generate the full report programmatically. This is always Python-generated — do not write prose narratives per UCO.

```python
import pickle, re
from collections import defaultdict
from datetime import datetime

data = pickle.load(open('/tmp/uco_flagged.pkl', 'rb'))
flagged = data['flagged']
ucoes   = data['ucoes']

# --- Helpers ---

def as_float(v):
    try: return float(v)
    except: return 0.0

def fmt_money(v):
    f = as_float(v)
    return "$0/mo" if f == 0 else f"${f:,.0f}/mo"

def fmt_days(v):
    return f"{int(as_float(v))}d"

def sf_link(uid, name):
    url = f"https://databricks.lightning.force.com/lightning/r/UseCase__c/{uid}/view"
    prefix = ''
    remainder = name
    while True:
        m = re.match(r'^\[([^\]]{1,30})\]\s*', remainder)
        if m:
            prefix += m.group(0).rstrip() + ' '
            remainder = remainder[m.end():]
        else:
            m2 = re.match(r'^(\w[\w\s&]+:\s+)', remainder)
            if m2 and re.match(r'^\[', remainder[m2.end():]):
                prefix += m2.group(1)
                remainder = remainder[m2.end():]
            else:
                break
    link_text = remainder.strip().replace('[','(').replace(']',')') if remainder.strip() else name.replace('[','(').replace(']',')')
    return (prefix.rstrip() + ' [' + link_text + '](' + url + ')').lstrip()

def flag_order_key(code):
    ORDER = ['BREACHED','NOTES_RISK','RISKY_TIMELINE','STAGE_VELOCITY','LONG_IN_STAGE','STALE','BLOCKER']
    return ORDER.index(code) if code in ORDER else 99

def format_flag_string(flags):
    sorted_flags = sorted(flags, key=lambda x: flag_order_key(x[0]))
    parts = []
    for code, msg in sorted_flags:
        parts.append(f"**{code}** ({msg})")
    return ' · '.join(parts)

def get_last_note(u):
    """Return the most recent next-steps entry as a quoted excerpt (max 220 chars).

    Captures the entire first entry — all lines until the next blank line or a new
    date stamp — joined into a single line. No date prefix: the note text itself
    contains the date (e.g. '1/20 RC CS: ...'), so prepending the SF date is redundant.
    """
    ns = u.get('demand_plan_next_steps', '') or ''
    if not ns.strip():
        return '(no next steps)'

    DATE_START = re.compile(
        r'^([A-Z]{1,3}\s+)?'
        r'(\d{1,2}[\/\.\-]\d{1,2}|[A-Za-z]{3}[\s-]\d{1,2}|\d{4}-\d{2}-\d{2})'
    )
    SECTION_HEADER = re.compile(r'^[CNRW]:\s')

    lines = ns.strip().split('\n')
    entry_lines, entry_started = [], False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if entry_started:
                break
            continue
        if entry_started and (DATE_START.match(stripped) or SECTION_HEADER.match(stripped)):
            break
        entry_started = True
        entry_lines.append(stripped)

    if not entry_lines:
        entry_lines = [l.strip() for l in lines if l.strip()][:3]

    excerpt = ' '.join(entry_lines)
    if len(excerpt) > 220:
        excerpt = excerpt[:220] + '...'
    return f'"{excerpt}"'

def gen_recommendation(u, flags):
    """
    Derive the Recommendation line from the flag set.

    Condition rules (in priority order):
    - BREACHED:        Always "Update [onboarding/live] date in Salesforce"
    - NOTES_RISK:      Name the signal; AE to validate deal status with champion
    - RISKY_TIMELINE:  U3 → SA to confirm tech win + AE to draft onboarding plan;
                       U4 → AE to lock budget + finalize onboarding plan
    - STAGE_VELOCITY:  AE to accelerate with firm milestone plan or push live date to CQ+1
    - BLOCKER:         AE to assign owner and timeline for [type/category] blocker
    - LONG_IN_STAGE:   SA and AE to review [stage] exit criteria and set firm advancement date
    - STALE:           AE to add dated next steps update ([$/mo] at risk) or close UCO if inactive
    - default:         Review with AE to confirm current status and update forecast
    """
    flag_codes = {c: m for c, m in flags}
    parts = []

    if 'BREACHED' in flag_codes:
        msg = flag_codes['BREACHED']
        if 'nboarding' in msg:
            parts.append("Update onboarding date in Salesforce")
        if 'live date' in msg:
            parts.append("Update live date in Salesforce")

    if 'NOTES_RISK' in flag_codes:
        signals = flag_codes['NOTES_RISK']
        parts.append(f"Notes flag risk ({signals}) — AE to validate deal status with champion")

    if 'RISKY_TIMELINE' in flag_codes:
        stage = u.get('stage', '')
        if stage == 'U3':
            parts.append("SA to confirm technical win; AE to draft onboarding plan before live date")
        elif stage == 'U4':
            parts.append("AE to lock budget confirmation and finalize onboarding plan before live date")

    if 'STAGE_VELOCITY' in flag_codes:
        parts.append("AE to accelerate with a firm milestone plan or push live date to CQ+1")

    if 'BLOCKER' in flag_codes:
        btype = u.get('last_modified_blocker_type', '') or ''
        bcat  = u.get('last_modified_blocker_category', '') or ''
        label = btype or bcat
        parts.append(f"AE to assign owner and timeline for {label} blocker" if label else "AE to assign blocker owner and resolution timeline")

    if 'LONG_IN_STAGE' in flag_codes and 'RISKY_TIMELINE' not in flag_codes:
        stage = u.get('stage', '')
        parts.append(f"SA and AE to review {stage} exit criteria and set a firm advancement date")

    if 'STALE' in flag_codes:
        dbu = as_float(u.get('estimated_monthly_dollar_dbus', 0))
        parts.append(f"AE to add dated next steps update ({fmt_money(dbu)} at risk) or close UCO if inactive")

    if not parts:
        parts.append("Review with AE to confirm current status and update forecast")

    return '; '.join(parts) + '.'

def render_uco(u):
    account  = u.get('account_name', 'Unknown')
    name     = u.get('usecase_name', 'Unknown UCO')
    uid      = u.get('usecase_id', '')
    stage    = u.get('stage', '')
    dbu      = fmt_money(u.get('estimated_monthly_dollar_dbus'))
    days     = fmt_days(u.get('days_in_stage'))
    flags    = u.get('_flags', [])

    live_raw   = u.get('target_live_date')
    live_label = f" · Live {datetime.strptime(live_raw, '%Y-%m-%d').strftime('%b %Y')}" if live_raw else ""

    slip_count = as_float(u.get('slippage_count', 0))
    slip_label = f" · {int(slip_count)}x slip" if slip_count > 0 else ""

    link      = sf_link(uid, name)
    flag_str  = format_flag_string(flags)
    last_note = get_last_note(u)
    rec       = gen_recommendation(u, flags)

    return '\n'.join([
        f"- [ ] **{account}** | {link}",
        f"  * {stage} · {dbu}{live_label} · {days}{slip_label} · {flag_str}",
        f"  * {last_note}",
        f"  * **Recommendation**: {rec}",
    ])

# --- Build report ---
# SELECTED_QUARTERS must be set in step 3a from the AskUserQuestion answer.
# IS_L2_REPORT = True  when REGION_L3 == 'All' (VP/director covering multiple L3 sub-teams)
# IS_L2_REPORT = False when REGION_L3 is set  (single sub-territory or single-AE scope)

IS_L2_REPORT = (REGION_L3 == 'All')

# Filter to selected quarters only
flagged_in_scope = [u for u in flagged if u.get('target_go_live_fiscal_year_quarter', '') in SELECTED_QUARTERS]

def sort_ucos(ulist):
    return sorted(ulist, key=lambda u: (flag_order_key(u['_flags'][0][0]), -as_float(u.get('estimated_monthly_dollar_dbus'))))

def render_ae_block(ae, qdata, ae_total_dbu, heading_level='####'):
    """Render one AE's CQ/CQ+1 block.
    heading_level='####' for L3 reports (AE is top grouping).
    heading_level=None   for L2 reports (AE shown as bold text under L3 heading).
    """
    block = []
    cq_ucos  = sort_ucos(qdata.get('CQ',  []))
    cq1_ucos = sort_ucos(qdata.get('CQ+1', []))
    if not cq_ucos and not cq1_ucos:
        return block
    cq_n, cq1_n = len(cq_ucos), len(cq1_ucos)
    label = f"{ae} — CQ: {cq_n} · CQ+1: {cq1_n} · ${ae_total_dbu:,.0f}/mo"
    if heading_level:
        block.append(f"{heading_level} {label}")
    else:
        block.append(f"**{label}**")
    block.append("")
    if cq_ucos:
        block.append(f"**CQ — {CQ_LABEL}**")
        block.append("")
        for u in cq_ucos:
            block.append(render_uco(u))
            block.append("")
    if cq1_ucos:
        block.append(f"**CQ+1 — {CQ1_LABEL}**")
        block.append("")
        for u in cq1_ucos:
            block.append(render_uco(u))
            block.append("")
    return block

total_ucos    = len(ucoes)
total_aes     = len(set(u.get('account_executive','') for u in ucoes))
total_flagged = len(flagged_in_scope)

# Quarter summary line
if set(SELECTED_QUARTERS) == {CQ_LABEL}:
    q_header = f"CQ = {CQ_LABEL} (ends {CQ_END_DATE}) · {total_flagged} flagged"
elif set(SELECTED_QUARTERS) == {CQ1_LABEL}:
    q_header = f"CQ+1 = {CQ1_LABEL} (ends {CQ1_END_DATE}) · {total_flagged} flagged"
else:
    q_header = f"CQ = {CQ_LABEL} (ends {CQ_END_DATE}) · CQ+1 = {CQ1_LABEL} (ends {CQ1_END_DATE}) · {total_flagged} flagged"

lines = []
territory_name = REGION_L2 if IS_L2_REPORT else REGION_L3
lines.append(f"### UCO Hygiene Review — {territory_name}")
lines.append(f"**[Person Name] · [Title] · {date.today()}**")
lines.append(f"{total_ucos} UCOs · {total_aes} AEs · {q_header}")
lines.append("")
lines.append("---")
lines.append("")

if IS_L2_REPORT:
    # Group: L3 sub-territory → AE → CQ/CQ+1
    by_l3_ae = defaultdict(lambda: defaultdict(lambda: {'CQ': [], 'CQ+1': []}))
    for u in flagged_in_scope:
        l3 = u.get('region_level_3', 'Unknown')
        ae = u.get('account_executive', 'Unknown')
        q  = u.get('target_go_live_fiscal_year_quarter', '')
        if q in SELECTED_QUARTERS:
            key = 'CQ' if q == CQ_LABEL else 'CQ+1'
            by_l3_ae[l3][ae][key].append(u)

    # L3 order: by total flagged DBU descending
    def l3_total_dbu(l3):
        return sum(as_float(u.get('estimated_monthly_dollar_dbus'))
                   for ae_data in by_l3_ae[l3].values()
                   for q_list in ae_data.values() for u in q_list)

    for l3 in sorted(by_l3_ae.keys(), key=lambda x: -l3_total_dbu(x)):
        ae_dict = by_l3_ae[l3]
        ae_tots = {
            ae: sum(as_float(u.get('estimated_monthly_dollar_dbus'))
                    for q_list in qd.values() for u in q_list)
            for ae, qd in ae_dict.items()
        }
        ae_order_l3 = sorted(ae_dict.keys(), key=lambda ae: -ae_tots[ae])
        l3_dbu = l3_total_dbu(l3)
        l3_aes = len(ae_dict)

        lines.append(f"#### {l3} — {l3_aes} AEs · ${l3_dbu:,.0f}/mo flagged")
        lines.append("")
        for ae in ae_order_l3:
            block = render_ae_block(ae, ae_dict[ae], ae_tots[ae], heading_level=None)
            lines.extend(block)
        lines.append("---")
        lines.append("")

else:
    # Group: AE → CQ/CQ+1
    by_ae = defaultdict(lambda: {'CQ': [], 'CQ+1': []})
    for u in flagged_in_scope:
        ae = u.get('account_executive', 'Unknown')
        q  = u.get('target_go_live_fiscal_year_quarter', '')
        if q in SELECTED_QUARTERS:
            key = 'CQ' if q == CQ_LABEL else 'CQ+1'
            by_ae[ae][key].append(u)

    ae_totals = {
        ae: sum(as_float(u.get('estimated_monthly_dollar_dbus')) for q_list in qd.values() for u in q_list)
        for ae, qd in by_ae.items()
    }
    for ae in sorted(by_ae.keys(), key=lambda ae: -ae_totals[ae]):
        block = render_ae_block(ae, by_ae[ae], ae_totals[ae], heading_level='####')
        if block:
            lines.extend(block)
            lines.append("---")
            lines.append("")

output = '\n'.join(lines)
territory_slug = territory_name.lower().replace(' ', '-').replace('/', '-')
outfile = f'/tmp/uco_hygiene_{territory_slug}.md'
with open(outfile, 'w') as f:
    f.write(output)
print(f"Generated: {outfile}  ({len(lines)} lines, {len(output):,} bytes)")

# Quick broken-link check
broken = [l for l in lines if re.search(r'\[\[', l)]
print(f"Broken links: {len(broken)}")
```

**Variables used above** — must be defined before this block runs (carry them over from step 3a):
- `CQ_LABEL`, `CQ1_LABEL` — quarter labels (e.g. `"FY'27 Q1"`, `"FY'27 Q2"`)
- `CQ_END_DATE`, `CQ1_END_DATE` — human-readable end dates (e.g. `"Apr 30"`, `"Jul 31"`)
- `REGION_L2`, `REGION_L3` — from territory context (L3 = `"All"` if not set)

**Recommendation logic** (`gen_recommendation`) — the rules above are applied in priority order. Every BREACHED UCO **must** say "Update [onboarding/live] date in Salesforce." Every NOTES_RISK UCO must name the detected signal(s). Keep recommendations to one sentence; name AE or SA as responsible role.

#### Output format

**Each UCO is a checkbox item** under its section heading. Format:

```
- [ ] **[Account Name]** | [[Use Case Name]](https://databricks.lightning.force.com/lightning/r/UseCase__c/[usecase_id]/view)
  * U# · $[dbu]/mo · Live [Mon YYYY] · [N]d · [Nx slip] · FLAG1 · FLAG2
  * "[most recent demand_plan_next_steps entry — full first entry, max 220 chars]"
  * **Recommendation**: [specific action, naming responsible role (AE or SA).]
```

- **`- [ ]` checkbox prefix** — the UCO account/use-case line uses `- [ ]` (GFM task list syntax). When converted to Google Docs with the patched converter (`resources/markdown_to_gdocs_patched.py`), this renders as an interactive checkbox so reviewers can check off UCOs as they're fixed.
- The **Account Name is bolded**; the Use Case Name is the hyperlink (plain text, not bold).
- Account Name and Use Case Name are separated by ` | `.
- **Indented sub-bullets** — the 3 detail lines (flags, last note, recommendation) use `  * ` (2-space indent + asterisk). The patched converter renders these as visually indented nested bullets under the checkbox line, keeping each UCO block visually self-contained.
- **Flag ordering** — always sort flags in this order: `BREACHED` → `NOTES_RISK` → `RISKY_TIMELINE` → `STAGE_VELOCITY` → `LONG_IN_STAGE` → `STALE` → `BLOCKER`. The flag category name is always bolded: `**BREACHED** (onboarding Jan 2026)`, `**STALE** (No NS update in 16d)`, `**NOTES_RISK** (status red · timeline pushed)`. The detail message stays in plain text. Note: the BREACHED message is lowercase and compact — `**BREACHED** (live date Feb 2026)` or `**BREACHED** (onboarding Feb 2026)` — not "breached" repeated inside.
- **Category-prefixed use case names** — many territories (especially PS/Audit accounts like PwC and EY) prefix use case names with one or more `[Tag]` groups (e.g., `[IT] [US Assurance] Financial Benchmarking MVP` or `[IT][Mexico Tax] Data Estate Modernization`). These break the markdown link parser because `[[Tag] Name](url)` creates nested brackets. Strip all leading `[Short Tag]` groups (≤30 chars each) as plain text before the hyperlink. Also handle `AccountAbbr: [Tag]...` patterns (e.g., `CLA: [IT][Data Science] Name`). Replace any remaining `[` / `]` in the link text with `(` / `)`. Implementation:

  ```python
  import re
  def sf_link(uid, name):
      url = f"https://databricks.lightning.force.com/lightning/r/UseCase__c/{uid}/view"
      prefix = ''
      remainder = name
      while True:
          m = re.match(r'^\[([^\]]{1,30})\]\s*', remainder)
          if m:
              prefix += m.group(0).rstrip() + ' '
              remainder = remainder[m.end():]
          else:
              m2 = re.match(r'^(\w[\w\s&]+:\s+)', remainder)
              if m2 and re.match(r'^\[', remainder[m2.end():]):
                  prefix += m2.group(1)
                  remainder = remainder[m2.end():]
              else:
                  break
      link_text = remainder.strip().replace('[','(').replace(']',')') if remainder.strip() else name.replace('[','(').replace(']',')')
      return (prefix.rstrip() + ' [' + link_text + '](' + url + ')').lstrip()
  ```
- **Note excerpt** — the full first entry of `demand_plan_next_steps`, all lines until the next blank line or date stamp, joined and truncated to 220 chars, wrapped in double quotes. No "Last note" label or date prefix — the embedded date in the note text (e.g. `1/20 RC`) is sufficient. If no note exists, write `  * (no next steps)`.
- **Recommendation** — bold the label: `**Recommendation**:`. One specific action. Name the role (AE or SA). For any UCO with a BREACHED flag, the recommendation MUST include "Update [onboarding/live] date in Salesforce."

**Report scope determines grouping structure:**

- **L3-level report** (territory context has `sfdc_region_l3` set, or user scoped to a single AE): group by AE, then by quarter section.
- **L2-level report** (territory context has only `sfdc_region_l2` set): group by AE as above, but include the L3 sub-territory name in the AE header so the reader can scan sub-team health.

**Section structure (applies to both L2 and L3 reports):**

```
### UCO Hygiene Review — [Territory Name]

**[Person Name] · [Title] · [Date]**
[N] UCOs · [N] AEs · CQ = [FY'XX QN] (ends [date]) · CQ+1 = [FY'XX QN] (ends [date])

---

#### [AE Name] — CQ: [N] · CQ+1: [N] · $[total_cq_cq1_dbu]/mo

**CQ — [FY'XX QN]**

- [ ] **[Account Name]** | [[Use Case Name]](url)
  * U# · $[dbu]/mo · Live [Mon YYYY] · [N]d · [Nx slip] · **BREACHED** (onboarding Jan 2026) · **BREACHED** (live date Jan 2026) · **RISKY_TIMELINE** (Live Apr 2026 but still in U4) · **LONG_IN_STAGE** (90d in U4)
  * "[summary]"
  * **Recommendation**: [action. Update onboarding date in Salesforce.]

**CQ+1 — [FY'XX QN]**

- [ ] **[Account Name]** | [[Use Case Name]](url)
  * U# · $[dbu]/mo · Live [Mon YYYY] · [N]d · FLAG1 · FLAG2
  * "[summary]"
  * **Recommendation**: [action.]

---
```

#### Priority tiers

Report only flagged UCOs in `SELECTED_QUARTERS` (set from user's quarter selection — CQ, CQ+1, or both). UCOs in CQ+2 and beyond are never included. Determine CQ from today's date (Databricks FY quarters: Q1=Feb–Apr, Q2=May–Jul, Q3=Aug–Oct, Q4=Nov–Jan).

- **CQ (current quarter)** — highest urgency; time to act is shortest
- **CQ+1** — elevated; begin mitigation now

Within each quarter, order by flag severity: BREACHED / RISKY_TIMELINE first, then LONG_IN_STAGE (pressure hit), then SLIPPAGE with compound risk (2x+ slip + high days_in_stage), then STALE / LONG_IN_STAGE (base), then BLOCKER.

---

### 3c — Deliver the Report

After completing the narrative analysis, present the full hygiene report to the user in the chat. Write it as clean prose — no raw field names, no JSON artifacts.

Use `AskUserQuestion` to ask:

```
Please paste the Google Doc URL where I should write the report.
The doc MUST have a tab named "UCO Hygiene Review" — please create it first if it doesn't exist.
```

Collect the Google Doc URL as plain text input. Parse the doc ID from the URL:

- Doc ID: the long alphanumeric string in `https://docs.google.com/document/d/<DOC_ID>/edit`

> **Important:** The document **must** contain a tab named **"UCO Hygiene Review"**. Tell the user: *"The doc must have a tab named 'UCO Hygiene Review' — please create it first if it doesn't exist."* The script will error if the tab is not found.

The converter path (use glob `*` for the cached version):
```bash
CONVERTER=~/.claude/plugins/cache/fe-vibe/fins-ps-fintech-data/*/skills/uco-hygiene-review/resources/markdown_to_gdocs_patched.py
```

The patched converter supports:
- **Checkbox bullets** for `- [ ]` lines (interactive Google Docs checkboxes)
- **Indented nested bullets** for `  * ` sub-items
- **Tab targeting** via `--tab-title`

**Write into the "UCO Hygiene Review" tab:**
```bash
python3 $CONVERTER \
  --input /tmp/uco_hygiene_<territory>.md \
  --doc-id "<DOC_ID>" \
  --tab-title "UCO Hygiene Review" \
  --insert-top
```

- `--insert-top` **inserts new content above existing content** — the most recent hygiene review always appears at the top, with prior reviews preserved below a separator line.
- Do **not** use `--overwrite`. Each run layers the new report on top of whatever is already in the tab.
- The tab title is matched case-insensitively. The script raises a clear error if the tab is not found.

## SQL Resources

- `sql/get-ucos.sql` — main UCO query with `<region_l1>`, `<region_l2>`, and `<region_l3>` placeholders

## References

- `references/stage-definitions.md` — official U1–U5 stage definitions, exit criteria, and accountability by role. **Read this before performing hygiene evaluation.** It is the authoritative rubric for:
  - Condition 1: what constitutes a "clear plan to progress" at each stage
  - Condition 4: whether next steps content matches the declared stage
- `references/field-definitions.md` — complete `UseCase__c` field reference: API names, data types, picklist values, and a mapping of which fields are relevant to each hygiene condition

## Source Tables

| Table | Purpose |
|---|---|
| `main.gtm_silver.use_case_detail` | Current snapshot of all UCOs — stage, dates, next steps, health, slippage, blockers, and region fields in a single table. No processDate filter needed. |

## Important Notes

- Always write the query body to a file — never inline SQL with single-quoted values in a shell `--json='...'` argument
- Use `--profile=logfood` for all queries
- `sfdc_region_l2` from `sfdc_users_mapping` maps directly to `region_level_2` in `use_case_detail` (values are identical, no transformation needed)
- `use_case_detail` is a current snapshot — no `processDate` or snapshot date parameter is needed
- Results saved to `/tmp/uco_data.json` — used by subsequent hygiene analysis steps

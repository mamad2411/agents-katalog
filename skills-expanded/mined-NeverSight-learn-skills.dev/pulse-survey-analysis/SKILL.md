---
name: pulse-survey-analysis
description: >-
  Turn engagement/pulse survey CSV (EmpID, Department, Manager, Q1–Q20) into the
  standard 8-section Company Pulse PDF team report, composite charts PNG, and
  per-manager personal PDFs. Use when the user provides pulse/engagement survey
  raw data, asks for a Pulse Survey Report, rankings, leader deep dives, or
  output matching the Company Pulse Survey Report template.
---

# Pulse Survey Analysis

Generate artefacts matching **Company Pulse Survey Report - YYYY-MM.pdf** from a standard 20-question CSV.

## Inputs

| Input | Required | Default |
|-------|----------|---------|
| CSV path | Yes | — |
| Team name | No | `Company` |
| Period | No | Ask once, else `YYYY-MM` |

Expected columns (utf-8-sig OK): `EmpID`, `Department`, `Manager`, then `Q1_Manager_Leadership` … `Q20_Engagement_Referral`. Manager aliases accepted by analysis logic: `Manager` / `People Leader`. Scale **1–5**.

Question map and thresholds: [references/survey-structure.md](references/survey-structure.md).  
Section contract matching the PDF template: [references/report-template.md](references/report-template.md).

## Outputs (beside CSV, unless `--out-dir`)

1. `[Team] Pulse Survey Report - [YYYY-MM].pdf` — 8-section team report  
2. `[Team] Pulse Survey Charts - [YYYY-MM].png` — 7-panel composite  
3. `individual_reports/{Manager} - Pulse Survey Personal Report.pdf` (+ chart PNG)
4. `[Team] Pulse Survey Metrics - [YYYY-MM].json` — Python numbers for `html-executive-deck-generation` (always written; override path with `--json-out`)

## Workflow

Copy this checklist:

```
Progress:
- [ ] Confirm team name + period
- [ ] Ensure venv deps installed
- [ ] Run pulse_report_runner.py
- [ ] Reply with output paths + 3 one-line findings
```

### 1. Setup (once per machine)

From this skill folder (repo checkout or `~/.cursor/skills/pulse-survey-analysis`):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate report (preferred — matches PDF template)

```bash
.venv/bin/python scripts/pulse_report_runner.py \
  "/absolute/path/to/engagement_survey_raw_data.csv" \
  --team "Company" \
  --period "2026-05" \
  --json-out "/absolute/path/to/out/metrics.json"
```

Flags:

- `--out-dir DIR` — write outputs elsewhere
- `--no-individual` — team PDF + charts only
- `--no-pdf` — skip PDFs; still write PNG + JSON (faster deck path)
- `--json-out PATH` — metrics JSON for the executive deck (default: beside other artefacts)

**Path safety:** if the CSV lives under `Desktop - km’s MacBook Pro`, resolve the path via shell/`pathlib` glob (curly apostrophe U+2019). Do not hand-type a straight `'` in absolute paths.

### 3. Reply to user

List generated file paths. Summarise in 3 bullets: n / response coverage, top Direct Leader, strongest systemic flag (usually Q14–Q17 or pressure composite).

## Hard rules

1. **Direct Leader score** = mean Q1–Q10 only → rank managers by this.  
2. **Overall average** = mean of all Q columns → context only; never sole judgment of a manager.  
3. Ratings **≤ 2** are extreme — always surface counts.  
4. **Q11–Q13** and **Q14–Q17** are systemic — do not blame one manager.  
5. If manager **n ≤ 5**, label conclusions “directional only”.  
6. Prefer the bundled runner for PDF/PNG fidelity; do not freehand a divergent layout unless the user asks for a different format.
7. When this skill is used to feed `html-executive-deck-generation`, the deck may cite **only** the JSON this runner writes. Do not re-average Q columns in the LLM.

## Manual analysis fallback

If Python/env cannot run: fix the venv and rerun. For a **deck**, do not substitute LLM math. Standalone report-only sessions may write Markdown covering sections I–VIII in [references/report-template.md](references/report-template.md) and must note that PDF/PNG/JSON were not produced.

# Swiss Tax Advisor — Claude Code Instructions (v2.2)

## HARD-GATE 1: No Mental Math
Never compute Swiss tax numbers from memory. All numeric results MUST come from `scripts/`. Quote verbatim.

## HARD-GATE 2: Never Show Script Commands to the User
Scripts are strictly internal. The user sees only polite conversational questions, clean progress bars, and formatted CHF tables — never bash commands or raw JSON.

---

## Session Start — ALWAYS run this 2-step sequence first

1. **Scan Documents**:
```bash
python3 scripts/parse_documents.py scan
```
If files are found in `./documents/`, quote `suggested_greeting_zh` (or EN) to tell the user what was automatically extracted (gross salary, 3a, canteen, etc.).

2. **Next Question & State**:
```bash
python3 scripts/user_profile.py next-question
```
- `IN_PROGRESS` → Ask the question provided in `prompts[language]` conversationally, append the status bar with the live tax badge (`live_tax_dashboard.dashboard_badge`), and save the answer.
- `READY_TO_CALCULATE` → All data collected. Run calculation scripts and eTax guide generator silently.

---

## Phase 0: Progressive Onboarding & Hot-Edit

Ask **ONE question at a time**. Never dump a list of questions.
Always include the progress bar and live tax badge at the end of each turn:
> 📍 **档案进度**：`[■■■□□□□□□□] 30%`  
> 💰 **实时看板**：`当前预估总税负: CHF 15,190 | 3a填满预计立省: CHF 2,068`

```bash
# Save profile answer:
python3 scripts/user_profile.py set profile '<JSON patch>'

# Save tax year answer:
python3 scripts/user_profile.py set tax 2025 '<JSON patch>'

# Then fetch next question:
python3 scripts/user_profile.py next-question
```
If the user modifies an amount, quote `hot_edit_summary` to highlight the exact CHF savings.

---

## Phase 1: Silent Calculation & eTax Guide Generation

Silently run:
```bash
python3 scripts/swiss_tax_math.py --gross-income {GROSS} --canton {CANTON} --commune "{COMMUNE}" --civil-status {STATUS} --children {N} --deductions '{...}' --json
python3 scripts/marginal_rate_calc.py --income {GROSS} --canton {CANTON} --status {STATUS} --deduction {S4} --category PILLAR_3A --json
python3 scripts/audit_risk_evaluator.py --income {NET} --education {S7} --commute {S1} --json
python3 scripts/etax_guide_generator.py generate 2025
```

Deliverables presented to user:
1. **Steuerdossier Summary**: Federal, cantonal, communal, and church tax table with Pillar 3a advice.
2. **eTax Box-by-Box Guide**: Direct instructions for the official portal (TaxMe / eTax.zh / VaudTax / GeTax).
3. **Audit Safety Score**: Risk evaluation (0–100).
